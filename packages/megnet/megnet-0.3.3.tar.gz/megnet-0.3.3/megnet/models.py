from keras.optimizers import Adam
from keras.layers import Dense, Input, Concatenate, Add, Embedding, Dropout
from megnet.layers import MEGNetLayer, Set2Set
from megnet.activations import softplus2
from megnet.losses import mse_scale
from keras.regularizers import l2
from keras.models import Model
from megnet.callbacks import ModelCheckpointMAE, ManualStop, ReduceLRUponNan
from megnet.data.graph import GraphBatchDistanceConvert, GraphBatchGenerator, GaussianDistance
from megnet.data.crystal import CrystalGraph
from megnet.utils.preprocessing import DummyScaler
import numpy as np
import os
from warnings import warn
from monty.serialization import dumpfn, loadfn
import keras.backend as K


pjoin = os.path.join


class GraphModel:
    """
    Composition of keras model and convertor class for transfering structure
    object to input tensors. We add methods to train the model from
    (structures, targets) pairs

    Args:
        model: (keras model)
        graph_convertor: (object) a object that turns a structure to a graph,
            check `megnet.data.crystal`
        target_scaler: (object) a scaler object for converting targets, check
            `megnet.utils.preprocessing`
        metadata: (dict) An optional dict of metadata associated with the model.
            Recommended to incorporate some basic information such as units,
            MAE performance, etc.

    """

    def __init__(self,
                 model,
                 graph_convertor,
                 target_scaler=DummyScaler(),
                 metadata=None,
                 **kwargs):
        self.model = model
        self.graph_convertor = graph_convertor
        self.target_scaler = target_scaler
        self.metadata = metadata or {}

    def __getattr__(self, p):
        return getattr(self.model, p)

    def train(self,
              train_structures,
              train_targets,
              validation_structures=None,
              validation_targets=None,
              epochs=1000,
              batch_size=128,
              verbose=1,
              callbacks=None,
              scrub_failed_structures=False,
              prev_model=None,
              **kwargs):
        """
        Args:
            train_structures: (list) list of pymatgen structures
            train_targets: (list) list of target values
            validation_structures: (list) list of pymatgen structures as validation
            validation_targets: (list) list of validation targets
            epochs: (int) number of epochs
            batch_size: (int) training batch size
            verbose: (int) keras fit verbose, 0 no progress bar, 1 only at the epoch end and 2 every batch
            callbacks: (list) megnet or keras callback functions for training
            scrub_failed_structures: (bool) whether to scrub structures with failed graph computation
            prev_model: (str) file name for previously saved model
            **kwargs:
        """
        train_graphs, train_targets = self.get_all_graphs_targets(train_structures, train_targets,
                                                                  scrub_failed_structures=scrub_failed_structures)
        if validation_structures is not None:
            val_graphs, validation_targets = self.get_all_graphs_targets(
                validation_structures, validation_targets, scrub_failed_structures=scrub_failed_structures)
        else:
            val_graphs = None

        self.train_from_graphs(train_graphs,
                               train_targets,
                               validation_graphs=val_graphs,
                               validation_targets=validation_targets,
                               epochs=epochs,
                               batch_size=batch_size,
                               verbose=verbose,
                               callbacks=callbacks,
                               prev_model=prev_model,
                               **kwargs
                               )

    def train_from_graphs(self,
                          train_graphs,
                          train_targets,
                          validation_graphs=None,
                          validation_targets=None,
                          epochs=1000,
                          batch_size=128,
                          verbose=1,
                          callbacks=None,
                          prev_model=None,
                          **kwargs
                          ):

        # load from saved model
        if prev_model:
            self.load_weights(prev_model)
        is_classification = 'entropy' in self.model.loss
        monitor = 'val_acc' if is_classification else 'val_mae'
        mode = 'max' if is_classification else 'min'
        dirname = kwargs.pop('dirname', 'callback')
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if callbacks is None:
            # with this call back you can stop the model training by `touch STOP`
            callbacks = [ManualStop()]
        callbacks.append(ReduceLRUponNan())
        train_nb_atoms = [len(i['atom']) for i in train_graphs]
        train_targets = [self.target_scaler.transform(i, j) for i, j in zip(train_targets, train_nb_atoms)]

        if validation_graphs is not None:
            filepath = pjoin(dirname, 'val_mae_{epoch:05d}_{%s:.6f}.hdf5' % monitor)
            val_nb_atoms = [len(i['atom']) for i in validation_graphs]
            validation_targets = [self.target_scaler.transform(i, j) for i, j in zip(validation_targets, val_nb_atoms)]
            val_inputs = self.graph_convertor.get_flat_data(validation_graphs, validation_targets)

            val_generator = self._create_generator(*val_inputs,
                                                   batch_size=batch_size)
            steps_per_val = int(np.ceil(len(validation_graphs) / batch_size))
            callbacks.extend([ModelCheckpointMAE(filepath=filepath,
                                                 monitor=monitor,
                                                 mode=mode,
                                                 save_best_only=True,
                                                 save_weights_only=False,
                                                 val_gen=val_generator,
                                                 steps_per_val=steps_per_val,
                                                 y_scaler=None)])
        else:
            val_generator = None
            steps_per_val = None
        train_inputs = self.graph_convertor.get_flat_data(train_graphs, train_targets)
        # check dimension match
        self.check_dimension(train_graphs[0])
        train_generator = self._create_generator(*train_inputs, batch_size=batch_size)
        steps_per_train = int(np.ceil(len(train_graphs) / batch_size))
        self.fit_generator(train_generator, steps_per_epoch=steps_per_train,
                           validation_data=val_generator, validation_steps=steps_per_val,
                           epochs=epochs, verbose=verbose, callbacks=callbacks, **kwargs)

    def check_dimension(self, graph):
        """
        Check the model dimension against the graph convertor dimension
        Args:
            graph: structure graph

        Returns:

        """
        test_inp = self.graph_convertor.graph_to_input(graph)
        input_shapes = [i.shape for i in test_inp]

        model_input_shapes = [K.int_shape(i) for i in self.model.inputs]

        def _check_match(real_shape, tensor_shape):
            if len(real_shape) != len(tensor_shape):
                return False
            matched = True
            for i, j in zip(real_shape, tensor_shape):
                if j is None:
                    continue
                else:
                    if i == j:
                        continue
                    else:
                        matched = False
            return matched

        for i, j, k in zip(['atom features', 'bond features', 'state features'],
                           input_shapes[:3], model_input_shapes[:3]):
            matched = _check_match(j, k)
            if not matched:
                raise ValueError("The data dimension for %s is %s and does not match model "
                                 "required shape of %s" % (i, str(j), str(k)))

    def get_all_graphs_targets(self, structures, targets, scrub_failed_structures=False):
        """
        Compute the graphs from structures and spit out (graphs, targets) with options to
        automatically remove structures with failed graph computations

        Args:
            structures: (list) pymatgen structure list
            targets: (list) target property list
            scrub_failed_structures: (bool) whether to scrub those failed structures

        Returns:
            graphs, targets

        """
        graphs_valid = []
        targets_valid = []

        for i, (s, t) in enumerate(zip(structures, targets)):
            try:
                graph = self.graph_convertor.convert(s)
                graphs_valid.append(graph)
                targets_valid.append(t)
            except Exception as e:
                if scrub_failed_structures:
                    warn("structure with index %d failed the graph computations" % i,
                         UserWarning)
                    continue
                else:
                    raise RuntimeError(str(e))
        return graphs_valid, targets_valid

    def predict_structure(self, structure):
        """
        Predict property from structure

        Args:
            structure: pymatgen structure or molecule

        Returns:
            predicted target value
        """
        graph = self.graph_convertor.convert(structure)
        return self.predict_graph(graph)

    def predict_graph(self, graph):
        """
        Predict property from graph

        Args:
            graph: a graph dictionary, see megnet.data.graph

        Returns:
            predicted target value

        """
        inp = self.graph_convertor.graph_to_input(graph)
        return self.target_scaler.inverse_transform(self.predict(inp).ravel(), len(graph['atom']))

    def _create_generator(self, *args, **kwargs):
        if hasattr(self.graph_convertor, 'bond_convertor'):
            kwargs.update({'distance_convertor': self.graph_convertor.bond_convertor})
            return GraphBatchDistanceConvert(*args, **kwargs)
        else:
            return GraphBatchGenerator(*args, **kwargs)

    def save_model(self, filename):
        """
        Save the model to a keras model hdf5 and a json config for additional
        convertors

        Args:
            filename: (str) output file name

        Returns:
            None
        """
        self.model.save(filename)
        dumpfn(
            {
                'graph_convertor': self.graph_convertor,
                'target_scaler': self.target_scaler,
                'metadata': self.metadata
            },
            filename + '.json'
        )

    @classmethod
    def from_file(cls, filename):
        """
        Class method to load model from
            filename for keras model
            filename.json for additional convertors

        Args:
            filename: (str) model file name

        Returns
            GraphModel
        """
        configs = loadfn(filename + '.json')
        from keras.utils import get_custom_objects
        from keras.models import load_model

        custom_objs = get_custom_objects()
        custom_objs.update({'mean_squared_error_with_scale': mse_scale,
                            'softplus2': softplus2,
                            'MEGNetLayer': MEGNetLayer,
                            'Set2Set': Set2Set})
        model = load_model(filename, custom_objects=custom_objs)
        configs.update({'model': model})
        return GraphModel(**configs)


class MEGNetModel(GraphModel):
    """
    Construct a graph network model with or without explicit atom features
    if n_feature is specified then a general graph model is assumed,
    otherwise a crystal graph model with z number as atom feature is assumed.

    Args:
        nfeat_edge: (int) number of bond features
        nfeat_global: (int) number of state features
        nfeat_node: (int) number of atom features
        nblocks: (int) number of MEGNetLayer blocks
        lr: (float) learning rate
        n1: (int) number of hidden units in layer 1 in MEGNetLayer
        n2: (int) number of hidden units in layer 2 in MEGNetLayer
        n3: (int) number of hidden units in layer 3 in MEGNetLayer
        nvocal: (int) number of total element
        embedding_dim: (int) number of embedding dimension
        nbvocal: (int) number of bond types if bond attributes are types
        bond_embedding_dim: (int) number of bond embedding dimension
        ngvocal: (int) number of global types if global attributes are types
        global_embedding_dim: (int) number of global embedding dimension
        npass: (int) number of recurrent steps in Set2Set layer
        ntarget: (int) number of output targets
        act: (object) activation function
        l2_coef: (float or None) l2 regularization parameter
        is_classification: (bool) whether it is a classifiation task
        loss: (object or str) loss function
        dropout: (float) dropout rate
        graph_convertor: (object) object that exposes a "convert" method for structure to graph conversion
        optimizer_kwargs (dict): extra keywords for optimizer, for example clipnorm and clipvalue
    """

    def __init__(self,
                 nfeat_edge=None,
                 nfeat_global=None,
                 nfeat_node=None,
                 nblocks=3,
                 lr=1e-3,
                 n1=64,
                 n2=32,
                 n3=16,
                 nvocal=95,
                 embedding_dim=16,
                 nbvocal=None,
                 bond_embedding_dim=None,
                 ngvocal=None,
                 global_embedding_dim=None,
                 npass=3,
                 ntarget=1,
                 act=softplus2,
                 is_classification=False,
                 loss="mse",
                 l2_coef=None,
                 dropout=None,
                 graph_convertor=None,
                 optimizer_kwargs=None
                 ):

        int32 = 'int32'

        if nfeat_node is None:
            x1 = Input(shape=(None,), dtype=int32)  # only z as feature
            x1_ = Embedding(nvocal, embedding_dim)(x1)
        else:
            x1 = Input(shape=(None, nfeat_node))
            x1_ = x1

        if nfeat_edge is None:
            x2 = Input(shape=(None,), dtype=int32)
            x2_ = Embedding(nbvocal, bond_embedding_dim)(x2)
        else:
            x2 = Input(shape=(None, nfeat_edge))
            x2_ = x2

        if nfeat_global is None:
            x3 = Input(shape=(None,), dtype=int32)
            x3_ = Embedding(ngvocal, global_embedding_dim)(x3)
        else:
            x3 = Input(shape=(None, nfeat_global))
            x3_ = x3

        x4 = Input(shape=(None,), dtype=int32)
        x5 = Input(shape=(None,), dtype=int32)
        x6 = Input(shape=(None,), dtype=int32)
        x7 = Input(shape=(None,), dtype=int32)

        if l2_coef is not None:
            reg = l2(l2_coef)
        else:
            reg = None

        # two feedforward layers
        def ff(x, n_hiddens=[n1, n2]):
            out = x
            for i in n_hiddens:
                out = Dense(i, activation=act, kernel_regularizer=reg)(out)
            return out

        # a block corresponds to two feedforward layers + one MEGNetLayer layer
        # Note the first block does not contain the feedforward layer since
        # it will be explicitly added before the block
        def one_block(a, b, c, has_ff=True):
            if has_ff:
                x1_ = ff(a)
                x2_ = ff(b)
                x3_ = ff(c)
            else:
                x1_ = a
                x2_ = b
                x3_ = c
            out = MEGNetLayer(
                [n1, n1, n2], [n1, n1, n2], [n1, n1, n2],
                pool_method='mean', activation=act, kernel_regularizer=reg)(
                [x1_, x2_, x3_, x4, x5, x6, x7])

            x1_temp = out[0]
            x2_temp = out[1]
            x3_temp = out[2]
            if dropout:
                x1_temp = Dropout(dropout)(x1_temp)
                x2_temp = Dropout(dropout)(x2_temp)
                x3_temp = Dropout(dropout)(x3_temp)
            return x1_temp, x2_temp, x3_temp

        x1_ = ff(x1_)
        x2_ = ff(x2_)
        x3_ = ff(x3_)
        for i in range(nblocks):
            if i == 0:
                has_ff = False
            else:
                has_ff = True
            x1_1 = x1_
            x2_1 = x2_
            x3_1 = x3_
            x1_1, x2_1, x3_1 = one_block(x1_1, x2_1, x3_1, has_ff)
            # skip connection
            x1_ = Add()([x1_, x1_1])
            x2_ = Add()([x2_, x2_1])
            x3_ = Add()([x3_, x3_1])

        # set2set for both the atom and bond
        node_vec = Set2Set(T=npass, n_hidden=n3, kernel_regularizer=reg)([x1_, x6])
        edge_vec = Set2Set(T=npass, n_hidden=n3, kernel_regularizer=reg)([x2_, x7])
        # concatenate atom, bond, and global
        final_vec = Concatenate(axis=-1)([node_vec, edge_vec, x3_])
        if dropout:
            final_vec = Dropout(dropout)(final_vec)
        # final dense layers
        final_vec = Dense(n2, activation=act, kernel_regularizer=reg)(final_vec)
        final_vec = Dense(n3, activation=act, kernel_regularizer=reg)(final_vec)

        if is_classification:
            final_act = 'sigmoid'
            loss = 'binary_crossentropy'
        else:
            final_act = None
            loss = loss

        out = Dense(ntarget, activation=final_act)(final_vec)
        model = Model(inputs=[x1, x2, x3, x4, x5, x6, x7], outputs=out)

        opt_params = {'lr': lr}
        if optimizer_kwargs is not None:
            opt_params.update(optimizer_kwargs)
        model.compile(Adam(**opt_params), loss)

        if graph_convertor is None:
            graph_convertor = CrystalGraph(cutoff=4, bond_convertor=GaussianDistance(np.linspace(0, 5, 100), 0.5))

        super().__init__(model=model, graph_convertor=graph_convertor)
