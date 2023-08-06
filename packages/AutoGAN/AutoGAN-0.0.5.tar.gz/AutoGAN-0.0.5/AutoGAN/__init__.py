import keras 
import numpy as np
from keras.utils import plot_model
from .utils.gan_utils import listify
from .schemes.Base_TrainingScheme import Abstract_TrainingScheme


class GAN(keras.models.Model):
    """A basic architecture to build and train Generative Adverserial Networks easily in Keras"""
    def __init__(self, generator, discriminator, **kwargs):
        """Create a GAN object.
        
        Keyword arguments:
        generator: a keras model or list of models which will be the basic generator
        discriminator: a keras model or list of models which will be the basic discriminator
        name: the name of the model
       """

        try:
            super(GAN, self).__init__(**kwargs)
        except:
            print("encountered an error during init")
        
        assert isinstance(generator, keras.models.Model) or (isinstance(generator, list) and
                                                             isinstance(generator[0], keras.models.Model)), \
            "Generator is not a model or a model list!"
        assert isinstance(discriminator, keras.models.Model) or (isinstance(discriminator, list) and
                                                                 isinstance(discriminator[0], keras.models.Model)), \
            "Discriminator is not a model or a model list!"

        self._training_scheme = None

        self._generator_model = generator
        self._discriminator_model = discriminator

        self._discriminator = None
        self._generator = None
        self.metrics_names = None
        self.optimizer = []
        self.loss = []
        self.metrics = []
        self.loss_weights = None
        self.sample_weight_mode = None
        self.weighted_metrics = None
        self.generator_kwargs, self.discriminator_kwargs = None, None
        self.History = None
        self.Progbar, self.valProgbar = None, None
        self._is_compiled = False

    def compile(self, generator_kwargs={}, discriminator_kwargs={}, training_scheme=Abstract_TrainingScheme(),
                **kwargs):
        """compile a GAN object into the desired GAN architecture

         Keyword arguments:
         generator_kwargs: a dictionary to be passed as kwargs to the "compile_generator" function of the training scheme.
         discriminator_kwargs: a dictionary to be passed as kwargs to the "compile_discriminator" function of the training scheme.
         training_scheme: a subclass of Base_TrainingScheme , will determain how to construct and train the GAN.
         """

        assert training_scheme is not None, "No training scheme selected!"
        assert type(generator_kwargs) is dict, "generator kwargs are not a dictionary!"
        assert type(discriminator_kwargs) is dict, "discriminator kwargs are not a dictionary!"

        self.generator_kwargs, self.discriminator_kwargs = generator_kwargs, discriminator_kwargs
        self._training_scheme = training_scheme
        
        self._discriminator = self._training_scheme.compile_discriminator(self, self._generator_model,
                                                                          self._discriminator_model,
                                                                          **discriminator_kwargs)

        self._generator = self._training_scheme.compile_generator(self, self._generator_model,
                                                                  self._discriminator_model,
                                                                  **generator_kwargs)
        self._is_compiled = True

    def generator_model(self): return self._generator_model

    def discriminator_model(self): return self._discriminator_model

    def generator(self): return self._generator

    def discriminator(self): return self._discriminator

    def summary(self, save_plot=False, path_and_prefix='', **kwargs):
        print("\n\n\nGenerator Summary: \n")
        try:
            _ = iter(self._generator_model)
            for i, gen in enumerate(self._generator_model):
                gen.summary()
                if save_plot:
                    plot_model(gen, show_shapes=True, to_file=path_and_prefix+'GAN_Generator_Model'+str(i)+'.png')
        except TypeError:
            if isinstance(self._generator_model, keras.models.Model):
                self._generator_model.summary()
            if save_plot:
                plot_model(self._generator_model, show_shapes=True, to_file=path_and_prefix+'GAN_Generator_Model.png')

        print("\n\n\nDiscriminator Summary: \n")
        try:
            _ = iter(self._discriminator_model)
            for i, dis in enumerate(self._discriminator_model):
                dis.summary()
                if save_plot:
                    plot_model(dis, show_shapes=True, to_file=path_and_prefix+'GAN_Discriminator_Model'+str(i)+'.png')
        except TypeError:

            if isinstance(self._discriminator_model, keras.models.Model):
                self._discriminator_model.summary()
            if save_plot:
                plot_model(self._discriminator_model, show_shapes=True,
                           to_file=path_and_prefix+'GAN_Discriminator_Model.png')

        print("\n\n\nGenerator Training Model Summary: \n")
        self._generator.summary()
        if save_plot:
            plot_model(self._generator, show_shapes=True, to_file=path_and_prefix+'GAN_Generator_Training_Model.png')
       
        print("\n\n\nDiscriminator Training Model Summary: \n")
        self._discriminator.summary()
        if save_plot:
            plot_model(self._discriminator, show_shapes=True,
                       to_file=path_and_prefix+'GAN_Discriminator_Training_Model.png')

    def fit(self,
            x=None,
            y=None,
            batch_size=None,
            epochs=1,
            verbose=1,
            callbacks=None,
            validation_split=0.,
            validation_data=None,
            shuffle=True,
            sample_weight=None,
            initial_epoch=0,
            steps_per_epoch=None,
            validation_steps=None,
            validation_freq=1,
            generator_training_kwargs={}, discriminator_training_kwargs={},
            generator_training_multiplier=1, discriminator_training_multiplier=1,
            generator_callbacks=None, discriminator_callbacks=None,
            generator_validation=False, discriminator_validation=False,
            **kwargs):

        """Fit a GAN on provided training examples.
        
        Keyword arguments:
        x: inputs to the generator
        y: real samples
        verbose: whether to print losses on each batch
        epochs: number of epochs to train for
        steps_per_epoch: number of steps within each epoch
        batch_size: number of examples within each training batch
        generator_training_kwargs: a dictionary to be passed as kwargs to the
                                   "train_generator" function of the training scheme.
        discriminator_training_kwargs: a dictionary to be passed as kwargs to the
                                       "train_discriminator" function of the training scheme.
        generator_training_multiplier: on how many batchs to train the generator on each step
        discriminator_training_multiplier: on how many batchs to train the generator on each step
        generator_callbacks: callbacks to call on generator
        discriminator_callbacks: callbacks to call on discriminator
        """
        assert type(generator_training_kwargs) is dict, "discriminator training kwargs are not a dictionary!"
        assert type(discriminator_training_kwargs) is dict, "generator training kwargs are not a dictionary!"
        callbacks_generator, callbacks_discriminator = [], []
        self.History = keras.callbacks.History()
        self.Progbar = keras.callbacks.ProgbarLogger()
        batch_size = 32 if batch_size is None else batch_size
        assert batch_size is not None, "batch size is None, please provide batch size"

        if generator_validation or discriminator_validation:
            if validation_split != 0. and validation_data is None:
                val_idxs = np.random.choice(np.arange(x[0].shape[0]), int(x[0].shape[0] * validation_split)) \
                    if isinstance(x, list) else np.random.choice(np.arange(x.shape[0]), int(x.shape[0] * validation_split))
                mask = np.ones(x[0].shape[0], dtype=bool) if isinstance(x, list) else np.ones(x.shape[0], dtype=bool)
                mask[val_idxs] = 0
                if isinstance(x, list):
                    val_x = [m[val_idxs] for m in x]
                    x = [m[mask] for m in x]
                else:
                    val_x = x[val_idxs]
                    x = x[mask]
                if isinstance(y, list):
                    val_y = [m[val_idxs] for m in y]
                    y = [m[mask] for m in y]
                else:
                    val_y = y[val_idxs]
                    y = y[mask]
                val_sample_weight = sample_weight[val_idxs] if sample_weight is not None else None

            elif validation_split == 0. and validation_data is not None:
                val_x, val_y = validation_data[0], validation_data[1]
                if len(validation_data) > 2:
                    val_sample_weight = validation_data[2]
                else:
                    val_sample_weight = None

            elif validation_split != 0. and validation_data is not None:
                raise AttributeError("Please choose validation_split or validation_data")

            else:
                val_x = val_y = val_sample_weight = None

        else:
            val_x = val_y = val_sample_weight = None

        if generator_callbacks is not None:
            try:
                _ = iter(generator_callbacks)
            except TypeError:
                assert False, "generator callbacks are not iterable!"
        else:
            generator_callbacks = []

        if discriminator_callbacks is not None:
            try:
                _ = iter(discriminator_callbacks)
            except TypeError:
                assert False, "discriminator callbacks are not iterable!"
        else:
            discriminator_callbacks = []

        params = {}

        if steps_per_epoch is None:
            steps_per_epoch = 1

        params.update({'verbose': verbose})
        params.update({'samples': steps_per_epoch*batch_size})
        params.update({'steps': steps_per_epoch})

        self.Progbar.set_params({'verbose': verbose, 'epochs': epochs, 
                                 'samples': steps_per_epoch*batch_size, 
                                 'steps': steps_per_epoch})
        if epochs is not None:
            params.update({'epochs': epochs})

        if batch_size is not None:
            params.update({'batch_size': batch_size})
            params.update({'samples': batch_size*steps_per_epoch*epochs})
        
        for c in generator_callbacks:
            if c is None:
                continue
            c.set_model(self._generator)
            c.set_params(params)
            callbacks_generator.append(c)
        
        for c in discriminator_callbacks:
            if c is None:
                continue
            c.set_model(self._discriminator)
            c.set_params(params)
            callbacks_discriminator.append(c)

        callbacks_constant = []
        if verbose:
            callbacks_constant = [self.Progbar]
        
        for callback in callbacks_generator + callbacks_discriminator + [self.History] + callbacks_constant:
            if callback is None:
                continue
            callback.on_train_begin()
        for k in range(initial_epoch, epochs):
            for callback in callbacks_constant + callbacks_generator + callbacks_discriminator:
                if callback is None:
                    continue
                callback.on_epoch_begin(k)
            loss_discriminator, loss_generator = None, None
            for i in range(steps_per_epoch):
                temp_loss_discriminator, temp_loss_generator = \
                    self.__fit_on_batch(x=x, y=y, step=i, epoch=k, verbose=verbose,
                                        generator_training_kwargs=generator_training_kwargs,
                                        discriminator_training_kwargs=discriminator_training_kwargs,
                                        shuffle=shuffle,
                                        steps_per_epoch=steps_per_epoch,
                                        batch_size=batch_size,
                                        sample_weight=sample_weight,
                                        generator_training_multiplier=generator_training_multiplier,
                                        discriminator_training_multiplier=discriminator_training_multiplier,
                                        callbacks_generator=callbacks_generator,
                                        callbacks_discriminator=callbacks_discriminator,)

                if loss_discriminator is None:
                    loss_discriminator = temp_loss_discriminator

                elif hasattr(loss_discriminator, '__iter__'):
                    loss_discriminator = [a+b for a, b in zip(loss_discriminator, temp_loss_discriminator)]

                else:
                    loss_discriminator += temp_loss_discriminator

                if loss_generator is None:
                    loss_generator = temp_loss_generator

                elif hasattr(loss_generator, '__iter__'):
                    loss_generator = [a+b for a, b in zip(loss_generator, temp_loss_generator)]

                else:
                    loss_generator += temp_loss_generator

            loss_discriminator = [item * 1.0/steps_per_epoch for item in loss_discriminator]
            loss_generator = [item * 1.0/steps_per_epoch for item in loss_generator]

            for callback in callbacks_generator:
                if callback is None:
                    continue
                callback.on_epoch_end(k, logs={self._generator.metrics_names[i]:
                                               item for i, item in enumerate(loss_generator)})

            for callback in callbacks_discriminator:
                if callback is None:
                    continue
                callback.on_epoch_end(k, logs={self._discriminator.metrics_names[i]:
                                               item for i, item in enumerate(loss_discriminator)})

            loss_discriminator = {('discriminator_'+self._discriminator.metrics_names[i]):
                                  item for i, item in enumerate(loss_discriminator)}
            loss_generator = {('generator_'+self._generator.metrics_names[i]):
                              item for i, item in enumerate(loss_generator)}
            
            losses = loss_discriminator.copy()
            losses.update(loss_generator)
            self.History.on_epoch_end(k, losses)  # populate history
            if verbose:
                self.Progbar.on_epoch_end(k, losses)

            if validation_data is not None or validation_split != 0.:
                if validation_steps is None:
                    validation_steps = val_x[0].shape[0] if isinstance(val_x, list) else val_x.shape[0]
                    validation_steps /= batch_size
                self.evaluate(x=val_x, y=val_y, batch_size=batch_size, verbose=verbose, sample_weight=val_sample_weight,
                              steps=validation_steps, get_generator_results=generator_validation,
                              get_discriminator_results=discriminator_validation)

        for callback in callbacks_generator + callbacks_discriminator:
            if callback is None:
                continue
            callback.on_train_end()

        return self.History

    def __fit_on_batch(self, x, y, step, generator_training_kwargs, discriminator_training_kwargs,
                       epoch, steps_per_epoch, generator_training_multiplier=1, sample_weight=None,
                       discriminator_training_multiplier=1, batch_size=None, shuffle=False, verbose=0,
                       callbacks_generator=None, callbacks_discriminator=None):

        callbacks_constant = []
        if verbose:
            callbacks_constant = [self.Progbar]
            
        steps = step + (epoch * steps_per_epoch)
        if callbacks_generator is not None:
            try:
                _ = iter(callbacks_generator)
            except TypeError:
                assert False, "generator callbacks are not iterable!"
        else:
            callbacks_generator = []

        if callbacks_discriminator is not None:
            try:
                _ = iter(callbacks_discriminator)
            except TypeError:
                assert False, "discriminator callbacks are not iterable!"
        else:
            callbacks_discriminator = []

        for callback in callbacks_constant + callbacks_generator + callbacks_discriminator:
            if callback is None:
                continue
            callback.on_batch_begin(steps, logs={'batch': steps, 'size': batch_size})

        # Discriminator Training
        loss = None
        if isinstance(x, list):
            shape_len = x[0].shape[0]
        else:
            shape_len = x.shape[0]

        if isinstance(y, list):
            shape_len_y = y[0].shape[0]
        else:
            shape_len_y = y.shape[0]

        for j in range(discriminator_training_multiplier): 
            curr = (steps*discriminator_training_multiplier + j) * batch_size
            nex = curr + batch_size
            idxs = [i % shape_len for i in range(curr, nex)]
            if shuffle:
                    idxs = np.random.randint(0, shape_len, size=batch_size)
            idxs_y = [idx % shape_len_y for idx in idxs]

            if isinstance(x, list):
                train_x = [x[ind][idxs] for ind in range(len(x))]
                weights = sample_weight[idxs] if sample_weight is not None else None
            else:
                train_x = x[idxs]
                weights = sample_weight[idxs] if sample_weight is not None else None

            if y is not None:
                if isinstance(y, list):
                    train_y = [y[ind][idxs_y] for ind in range(len(y))]
                else:
                    train_y = y[idxs_y]
            else:
                train_y = None

            temp_loss = self._training_scheme.train_discriminator(model=self, discriminator=self._discriminator,
                                                                  x=train_x, y=train_y,
                                                                  batch_size=batch_size, sample_weight=weights,
                                                                  **discriminator_training_kwargs)
            if loss is None:
                loss = temp_loss

            elif hasattr(loss, '__iter__'):
                loss = [a+b for a, b in zip(loss, temp_loss)]

            else:
                loss += temp_loss

        if loss is None:
            loss = 0

        if isinstance(loss, list):
            loss_discriminator = [item * 1.0/discriminator_training_multiplier for item in loss]
        else:
            loss_discriminator = [loss * 1.0/discriminator_training_multiplier]
     
        # Generator Training
        loss = None
        for j in range(generator_training_multiplier): 
            curr = (steps*generator_training_multiplier + j) * batch_size
            nex = curr + batch_size
            idxs = [i % shape_len for i in range(curr, nex)]
            if shuffle:
                idxs = np.random.randint(0, shape_len, size=batch_size)
            idxs_y = [idx % shape_len_y for idx in idxs]

            if isinstance(x, list):
                train_x = [x[ind][idxs] for ind in range(len(x))]
                weights = sample_weight[idxs] if sample_weight is not None else None
            else:
                train_x = x[idxs]
                weights = sample_weight[idxs] if sample_weight is not None else None

            if y is not None:
                if isinstance(y, list):
                    train_y = [y[ind][idxs_y] for ind in range(len(y))]
                else:
                    train_y = y[idxs_y]
            else:
                train_y = None

            temp_loss = self._training_scheme.train_generator(model=self, generator=self._generator,
                                                              x=train_x, y=train_y,
                                                              batch_size=batch_size, sample_weight=weights,
                                                              **generator_training_kwargs)
            if loss is None:
                loss = temp_loss

            elif hasattr(loss, '__iter__'):
                loss = [a+b for a, b in zip(loss, temp_loss)]

            else:
                loss += temp_loss

        if loss is None:
            loss = 0

        if isinstance(loss, list):
            loss_generator = [item * 1.0/generator_training_multiplier for item in loss]
        else:
            loss_generator = [loss * 1.0/generator_training_multiplier]

        for callback in callbacks_generator:  # callbacks for generator
            callback.on_batch_end(step, logs={self._generator.metrics_names[i]:
                                              item for i, item in enumerate(loss_generator)})

        for callback in callbacks_discriminator:  # callbacks for discriminator
            callback.on_batch_end(step, logs={self._discriminator.metrics_names[i]:
                                              item for i, item in enumerate(loss_discriminator)})

        loss_discriminator_a = {(''+self._discriminator.metrics_names[i]):
                                item for i, item in enumerate(loss_discriminator)}
        loss_generator_a = {(''+self._generator.metrics_names[i]):
                            item for i, item in enumerate(loss_generator)}

        if verbose > 0:
            losses = loss_generator_a.copy()
            for key in losses.keys():
                if key in loss_discriminator_a:
                    val = loss_discriminator_a.pop(key, 0)
                    loss_discriminator_a['discriminator_model_'+key] = val
                    val = losses.pop(key, 0)
                    losses['generator_model_'+key] = val
            
            losses.update(loss_discriminator_a)
            self.Progbar.params['metrics'] = losses
            
            losses2 = losses.copy()
            losses2.update({'size': batch_size})
            self.Progbar.on_batch_end(step, losses2)

        return loss_discriminator, loss_generator

    def evaluate(self, x=None, y=None,
                 batch_size=None,
                 verbose=1,
                 sample_weight=None,
                 steps=None,
                 generator_callbacks=None,
                 discriminator_callbacks=None,
                 get_generator_results=True,
                 get_discriminator_results=True,
                 **kwargs):

        self.valProgbar = keras.callbacks.ProgbarLogger()
        if generator_callbacks is not None:
            try:
                _ = iter(generator_callbacks)
            except TypeError:
                assert False, "generator callbacks are not iterable!"
        else:
            generator_callbacks = []

        if discriminator_callbacks is not None:
            try:
                _ = iter(discriminator_callbacks)
            except TypeError:
                assert False, "discriminator callbacks are not iterable!"
        else:
            discriminator_callbacks = []

        params = {}

        params.update({'verbose': verbose})
        params.update({'samples': x.shape[0] if not isinstance(x, list) else x[0].shape[0]})
        params.update({'steps': steps})
        params.update({'epochs': 1})

        self.valProgbar.set_params({'epochs': 1,
                                    'batch_size': batch_size,
                                    'verbose': verbose,
                                    'samples': x.shape[0] if not isinstance(x, list) else x[0].shape[0],
                                    'steps': steps})

        if batch_size is not None:
            params.update({'batch_size': batch_size})

        callbacks_generator = []
        for c in generator_callbacks:
            if c is None:
                continue
            c.set_model(self._generator)
            c.set_params(params)
            callbacks_generator.append(c)

        callbacks_discriminator = []
        for c in discriminator_callbacks:
            if c is None:
                continue
            c.set_model(self._discriminator)
            c.set_params(params)
            callbacks_discriminator.append(c)

        if steps is None:
            if isinstance(x, list):
                steps = x[0].shape[0] % batch_size + 1
            else:
                steps = x.shape[0] % batch_size + 1

        shape_len = x[0].shape[0] if isinstance(x, list) else x.shape[0]
        shape_len_y = y[0].shape[0] if isinstance(y, list) else y.shape[0]
        for callback in callbacks_discriminator + callbacks_generator:
            callback.on_test_begin()
        self.valProgbar.on_train_begin()
        self.valProgbar.on_epoch_begin(0)
        total_loss_gen, total_loss_dis = [], []
        for i in range(steps):
            for callback in callbacks_discriminator + callbacks_generator:
                callback.on_test_batch_begin(i, {'batch': i, 'size': batch_size})

            self.valProgbar.on_batch_begin(i, logs={'batch': i, 'size': batch_size})
            curr = i * batch_size
            nex = curr + batch_size
            idxs = [i % shape_len for i in range(curr, nex)]
            idxs_y = [idx % shape_len_y for idx in idxs]

            if isinstance(x, list):
                val_x = [x[ind][idxs] for ind in range(len(x))]
                val_weights = sample_weight[idxs] if sample_weight is not None else None
            else:
                val_x = x[idxs]
                val_weights = sample_weight[idxs] if sample_weight is not None else None

            if y is not None:
                if isinstance(y, list):
                    val_y = [y[ind][idxs_y] for ind in range(len(y))]
                else:
                    val_y = y[idxs_y]
            else:
                val_y = None

            loss_gen, loss_dis = self._training_scheme.test_on_batch(model=self, x=val_x, y=val_y,
                                                                     batch_size=batch_size, sample_weight=val_weights,
                                                                     get_generator_results=get_generator_results,
                                                                     get_discriminator_results=get_discriminator_results,
                                                                     **kwargs)
            loss_dis, loss_gen = listify(loss_dis), listify(loss_gen)
            if get_discriminator_results:
                loss_discriminator_a = {('' + self._discriminator.metrics_names[i]):
                                        item for i, item in enumerate(loss_dis)}
            else:
                loss_discriminator_a = {}
            if get_generator_results:
                loss_generator_a = {('' + self._generator.metrics_names[i]):
                                    item for i, item in enumerate(loss_gen)}
            else:
                loss_generator_a = {}
            if not total_loss_gen:
                total_loss_gen, total_loss_dis = [d for d in loss_gen], [d for d in loss_dis]
            else:
                total_loss_gen, total_loss_dis = [a + b for a, b in zip(total_loss_gen, loss_gen)], \
                                                 [a + b for a, b in zip(total_loss_dis, loss_dis)]

            for callback in callbacks_discriminator + callbacks_generator:
                callback.on_batch_end(i, logs={self._generator.metrics_names[i]:
                                               item for i, item in enumerate(loss_gen)})

            if verbose > 0:
                losses = loss_generator_a.copy()
                for key in losses.keys():
                    if key in loss_discriminator_a:
                        val = loss_discriminator_a.pop(key, 0)
                        loss_discriminator_a['discriminator_model_' + key] = val
                        val = losses.pop(key, 0)
                        losses['generator_model_' + key] = val

                losses.update(loss_discriminator_a)

                losses2 = {}
                for key, value in losses.items():
                    losses2["val_" + key] = value

                self.valProgbar.params['metrics'] = losses2.keys()

                losses2.update({'size': batch_size})
                self.valProgbar.on_batch_end(i, losses2)

        self.valProgbar.on_epoch_end(0)
        self.valProgbar.on_train_end()
        for callback in callbacks_discriminator + callbacks_generator:
            callback.on_test_end()
        total_loss_gen, total_loss_dis = [a / float(steps) for a in total_loss_gen], \
                                         [a / float(steps) for a in total_loss_dis]
        output = []
        if get_discriminator_results:
            output = output + total_loss_dis

        if get_generator_results:
            output = output + total_loss_gen

        return output

    def predict(self, x,
                batch_size=None,
                verbose=0,
                steps=None,
                predict_discriminator=False,
                **kwargs):

        if predict_discriminator:
            model = self.discriminator_model()
            if isinstance(model, list):
                return [m.predict(x=x, batch_size=batch_size, verbose=verbose, steps=steps)
                        for m in model]
            elif isinstance(model, keras.models.Model):
                return model.predict(x=x, batch_size=batch_size, verbose=verbose, steps=steps)
            else:
                raise AttributeError
        else:
            model = self.generator_model()
            if isinstance(model, list):
                return [m.predict(x=x, batch_size=batch_size, verbose=verbose, steps=steps)
                        for m in model]
            elif isinstance(model, keras.models.Model):
                return model.predict(x=x, batch_size=batch_size, verbose=verbose, steps=steps)
            else:
                raise AttributeError

    def train_on_batch(self, x, y,
                       sample_weight=None,
                       class_weight=None,
                       generator_training_kwargs=None,
                       discriminator_training_kwargs=None,
                       generator_training_multiplier=1,
                       discriminator_training_multiplier=1):
        batch_size = x[0].shape[0] if isinstance(x, list) else x.shape[0]
        return self.__fit_on_batch(x=x, y=y, step=0, epoch=0, steps_per_epoch=1, batch_size=batch_size,
                                   discriminator_training_kwargs=discriminator_training_kwargs,
                                   generator_training_kwargs=generator_training_kwargs,
                                   discriminator_training_multiplier=discriminator_training_multiplier,
                                   generator_training_multiplier=generator_training_multiplier)

    def predict_on_batch(self, x, predict_discriminator=False, **kwargs):
        if predict_discriminator:
            model = self.discriminator_model()
            if isinstance(model, list):
                return [m.predict_on_batch(x) for m in model]
            elif isinstance(model, keras.models.Model):
                return model.predict_on_batch(x)
            else:
                raise AttributeError
        else:
            model = self.generator_model()
            if isinstance(model, list):
                return [m.predict_on_batch(x) for m in model]
            elif isinstance(model, keras.models.Model):
                return model.predict_on_batch(x)
            else:
                raise AttributeError

    def __call__(self, inputs,  return_discriminator=False, **kwargs):
        if return_discriminator:
            if isinstance(self._discriminator_model, list):
                return [m(inputs, **kwargs) for m in self._discriminator_model]
            elif isinstance(self._discriminator_model, keras.models.Model):
                return self._discriminator_model(inputs, **kwargs)
            else:
                raise AttributeError
        else:
            if isinstance(self._generator_model, list):
                return [m(inputs, **kwargs) for m in self._generator_model]
            elif isinstance(self._generator_model, keras.models.Model):
                return self._generator_model(inputs, **kwargs)
            else:
                raise AttributeError

    def get_layer(self, name=None, index=None, get_from_generator=True):
        if get_from_generator:
            return self._generator.get_layer(name, index)
        else:
            return self._discriminator.get_layer(name, index)

    def get_weights(self):
        """Retrieves the weights of the model.
        # Returns
            A flat list of Numpy arrays.
        """
        return self._generator.get_weights(), self._discriminator.get_weights()

    def set_weights(self, weights):
        self._generator.set_weights(weights[0])
        self._discriminator.set_weights(weights[1])

    def get_config(self):
        return self._generator.get_config(), self._discriminator.get_config()

    def compute_output_shape(self, **kwargs):
        return self._generator.compute_output_shape(**kwargs)

    def save(self, filepath, overwrite=True, include_optimizer=True):
        self._generator.save(filepath[:-3]+'_generator.h5', overwrite=overwrite, include_optimizer=include_optimizer)
        self._discriminator.save(filepath[:-3]+'_discriminator.h5', overwrite=overwrite,
                                 include_optimizer=include_optimizer)

    def from_config(self, config, custom_objects=None):
        self._generator.from_config(config[0], custom_objects)
        self._discriminator.from_config(config[1], custom_objects)

    def load_weights(self, filepath, by_name=False,
                     skip_mismatch=False, reshape=False):
        self._generator.load_weights(filepath[:-3]+'_generator.h5', by_name=by_name, skip_mismatch=skip_mismatch,
                                     reshape=reshape)
        self._discriminator.load_weights(filepath[:-3]+'_discriminator.h5', by_name=by_name,
                                         skip_mismatch=skip_mismatch, reshape=reshape)
