# =========================================================================================================
# File: Base_TrainingScheme.py
# Author: Elad Dvash
#
# Description:
# This file contains an implementation of a basic GAN (https://arxiv.org/abs/1406.2661) and an abstract
# training scheme class definition.
# The GAN class supports multi-input, multi-output generators and discriminators
# =========================================================================================================

import keras
from keras.models import Model
import numpy as np
from ..utils.gan_utils import get_model_input, get_model_output, set_layer_name, extend, prepare_compile, listify


class Abstract_TrainingScheme(object):
    def __init__(self, **kwargs):
        pass

    def compile_discriminator(self, model, generator, discriminator, **kwargs):
        """Compile a Discriminator."""
        raise NotImplementedError("Please Implement")

    def compile_generator(self, model, generator, discriminator, **kwargs):
        """Compile a Generator."""
        raise NotImplementedError("Please Implement this method")

    def train_discriminator(self, model, discriminator, x, y, batch_size, **kwargs):
        """Train a Discriminator on a batch."""
        raise NotImplementedError("Please Implement this method")

    def train_generator(self, model, generator, x, y, batch_size, **kwargs):
        """Train a Generator on a batch."""
        raise NotImplementedError("Please Implement this method")

    def test_on_batch(self, model, x, y, batch_size, sample_weight=None,
                      get_generator_results=False,
                      get_discriminator_results=False):
        raise NotImplementedError("Please Implement this method")

    def test_on_generator(self, model, generator, x, y, batch_size, sample_weight=None):
        raise NotImplementedError("Please Implement this method")

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        raise NotImplementedError("Please Implement this method")


class GAN_TrainingScheme(Abstract_TrainingScheme):
    def __init__(self, **kwargs):
        super(GAN_TrainingScheme, self).__init__(**kwargs)
        self.has_generator_multioutput = False
        self.out_shape = None
        self.ones, self.zeros = None, None

    def compile_discriminator(self, model, generator, discriminator, optimizer=None, loss=None, metrics=[], **kwargs):
        """Compile a Discriminator."""
        discriminator.trainable = True
        generator.trainable = False

        model_shape = get_model_input(discriminator)
        in_real = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        model_shape = get_model_input(generator)
        inp = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        in_gen = generator(inp)  # get generator outputs

        dis_out_real, dis_out_real_names = set_layer_name(discriminator(in_real), discriminator.name+"_real")
        dis_out_fake, dis_out_fake_names = set_layer_name(discriminator(in_gen), discriminator.name+"_fake")
        # ----- Discriminator -----
        inputs = []
        extend(inputs, in_real)
        extend(inputs, inp)

        outputs = []
        extend(outputs, dis_out_real)
        extend(outputs, dis_out_fake)

        loss = listify(loss)
        metrics = listify(metrics)
        if len(metrics) == 1:
            metrics = [metrics[0]] * len(dis_out_real_names)
        elif all([not isinstance(m, list) for m in metrics]):
            metrics = [metrics] * len(dis_out_real_names)

        l, m, _ = prepare_compile(dis_out_real_names + dis_out_fake_names,
                                  loss + loss,
                                  metrics + metrics)
        discriminator_model = Model(inputs=inputs, outputs=outputs)
        discriminator_model.compile(optimizer=optimizer, loss=l, metrics=m)
        # ----- Discriminator -----
        # discriminator_model.summary()
        generator.trainable = True

        return discriminator_model

    def compile_generator(self, model, generator, discriminator, discriminator_loss=None, generator_loss=None,
                          generator_metrics=[], discriminator_metrics=[],
                          generator_loss_weight=1, discriminator_loss_weight=1, optimizer=None, **kwargs):
        """Compile a Generator."""
        if 'loss' in kwargs and discriminator_loss is None:
            discriminator_loss = kwargs['loss']
        if 'metrics' in kwargs and discriminator_metrics is None:
            discriminator_metrics = kwargs['metrics']
        if 'loss_weight' in kwargs and discriminator_loss_weight is None:
            discriminator_loss_weight = kwargs['loss_weight']

        discriminator.trainable = False
        generator.trainable = True

        model_shape = get_model_input(generator)
        inp = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        gen_out, gen_names = set_layer_name(generator(inp), generator.name)
        dis_out, dis_names = set_layer_name(discriminator(gen_out), discriminator.name)
        # ----- Generator -----

        inputs = []
        extend(inputs, inp)

        outputs = []
        if generator_loss is not None:
            self.has_generator_multioutput = True
            extend(outputs, gen_out)
        else:
            gen_names = []

        if discriminator_loss is not None:
            extend(outputs, dis_out)
        else:
            dis_names = []

        generator_loss = listify(generator_loss) * (len(gen_names) if len(listify(generator_loss)) == 1 else 1)
        discriminator_loss = listify(discriminator_loss) * (len(dis_names) if len(listify(discriminator_loss)) == 1 else 1)
        generator_metrics = listify(generator_metrics) * (len(gen_names) if len(listify(generator_metrics)) == 1 else 1)
        discriminator_metrics = listify(discriminator_metrics) * (len(dis_names) if len(listify(discriminator_metrics)) == 1 else 1)
        generator_loss_weight = listify(generator_loss_weight) * (len(gen_names) if len(listify(generator_loss_weight)) == 1 else 1)
        discriminator_loss_weight = listify(discriminator_loss_weight) * (len(dis_names) if len(listify(discriminator_loss_weight)) == 1 else 1)

        l, m, w = prepare_compile(gen_names + dis_names,
                                  generator_loss + discriminator_loss,
                                  generator_metrics + discriminator_metrics,
                                  generator_loss_weight + discriminator_loss_weight)

        generator_model = Model(inputs=inputs, outputs=outputs)
        generator_model.compile(optimizer=optimizer, loss=l, metrics=m, loss_weights=w)
        # ----- Generator -----

        discriminator.trainable = True
        return generator_model

    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None, **kwargs):
        # Discriminator Training
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape
        y = listify(y)
        x = listify(x)

        loss = discriminator.train_on_batch(y + x, self.ones + self.zeros, sample_weight=sample_weight)
        return loss

    def train_generator(self, model, generator, x, y, batch_size, sample_weight=None, **kwargs):
        # Generator Training
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape
        y = listify(y)

        if self.has_generator_multioutput:
            loss = generator.train_on_batch(x, y + self.ones, sample_weight=sample_weight)  # x, [y, 1]
        else:
            loss = generator.train_on_batch(x, self.ones, sample_weight=sample_weight)  # x, 1
        return loss

    def test_on_batch(self, model, x, y, batch_size, sample_weight=None,
                      get_generator_results=False,
                      get_discriminator_results=False):
        gen_loss = self.test_on_generator(model=model, generator=model.generator(), x=x, y=y, batch_size=batch_size,
                                          sample_weight=sample_weight) if get_generator_results else []
        dis_loss = self.test_on_discriminator(model=model, discriminator=model.discriminator(), x=x, y=y,
                                              batch_size=batch_size,
                                              sample_weight=sample_weight) if get_discriminator_results else []
        return gen_loss, dis_loss

    def test_on_generator(self, model, generator, x, y, batch_size, sample_weight=None):
        # Generator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape
        y = listify(y)

        if self.has_generator_multioutput:
            loss = generator.test_on_batch(x, y + self.ones, sample_weight=sample_weight)  # x, [y, 1]
        else:
            loss = generator.test_on_batch(x, self.ones, sample_weight=sample_weight)  # x, 1
        return loss

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        # Discriminator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape
        y = listify(y)
        x = listify(x)

        loss = discriminator.test_on_batch(y + x, self.ones + self.zeros, sample_weight=sample_weight)
        return loss
