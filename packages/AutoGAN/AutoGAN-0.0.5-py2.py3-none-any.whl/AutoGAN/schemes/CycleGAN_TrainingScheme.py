# =========================================================================================================
# File: CycleGAN_TrainingScheme.py
# Author: Elad Dvash
#
# Description:
# This file contains an implementation of a CycleGAN (https://arxiv.org/abs/1703.10593) and a CycleWGAN -
# a CycleGAN with an IWGAN-GP-like discriminator.
# Both classes support multi-input, multi-output generators and discriminators
# =========================================================================================================

import keras
import numpy as np
from .Base_TrainingScheme import GAN_TrainingScheme
from keras.models import Model
from functools import partial
from .IWGAN_TrainingScheme import RandomWeightedAverage, wasserstein_loss, gradient_penalty_loss
from ..utils.gan_utils import get_model_input, get_model_output, set_layer_name, extend, prepare_compile, listify


# -----------------------------------------------------------------------------------------------------------------
#  CycleWGAN Training Scheme
# -----------------------------------------------------------------------------------------------------------------


class CycleGAN_TrainingScheme(GAN_TrainingScheme):
    def __init__(self, **kwargs):
        super(CycleGAN_TrainingScheme, self).__init__(**kwargs)

    def compile_discriminator(self, model, generator, discriminator, optimizer=None, loss=None, metrics=[], **kwargs):
        for dis in discriminator:
            dis.trainable = True

        for gen in generator:
            gen.trainable = False

        model_shape = get_model_input(generator[0])
        img_a = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        model_shape = get_model_input(generator[1])
        img_b = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        inputs = []
        extend(inputs, img_a)
        extend(inputs, img_b)

        g_ba, g_ab = generator[0], generator[1]
        d_a, d_b = discriminator[0], discriminator[1]

        fake_b = g_ab(img_a)
        fake_a = g_ba(img_b)

        dis_out_real_b, dis_out_real_names_b = set_layer_name(d_b(img_b), d_b.name+"_real")
        dis_out_fake_b, dis_out_fake_names_b = set_layer_name(d_b(fake_b), d_b.name+"_fake")

        dis_out_real_a, dis_out_real_names_a = set_layer_name(d_a(img_a), d_a.name+"_real")
        dis_out_fake_a, dis_out_fake_names_a = set_layer_name(d_a(fake_a), d_a.name+"_fake")

        outputs = []
        extend(outputs, dis_out_real_a)
        extend(outputs, dis_out_real_b)
        extend(outputs, dis_out_fake_a)
        extend(outputs, dis_out_fake_b)

        names = dis_out_real_names_a + dis_out_real_names_b + dis_out_fake_names_a + dis_out_fake_names_b
        loss = listify(loss)
        metrics = listify(metrics)
        if len(metrics) == 1:
            metrics = [metrics[0]] * len(dis_out_real_names_a)
        elif all([not isinstance(m, list) for m in metrics]):
            metrics = [metrics] * len(dis_out_real_names_a)

        l, m, _ = prepare_compile(names,
                                  loss * 4,
                                  metrics * 4)

        discriminator_model = Model(inputs=inputs, outputs=outputs)
        discriminator_model.compile(optimizer=optimizer, loss=l, metrics=m)

        for gen in generator:
            gen.trainable = True
        return discriminator_model

    def compile_generator(self, model, generator, discriminator, optimizer=None,
                          translation_weight=1, cycle_weight=10, identity_weight=1,
                          translation_loss='mse', cycle_loss='mae', identity_loss='mae',
                          translation_metrics=[], cycle_metrics=[], identity_metrics=[], **kwargs):

        if 'metrics' in kwargs:
            if len(translation_metrics) == 0:
                translation_metrics = kwargs['metrics']
            if len(cycle_metrics) == 0:
                cycle_metrics = kwargs['metrics']
            if len(identity_metrics) == 0:
                identity_metrics = kwargs['metrics']

        for dis in discriminator:
            dis.trainable = False

        for gen in generator:
            gen.trainable = True

        model_shape = get_model_input(generator[0])
        img_a = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        model_shape = get_model_input(generator[1])
        img_b = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        g_ba, g_ab = generator[0], generator[1]
        d_a, d_b = discriminator[0], discriminator[1]

        fake_a = g_ba(img_b)
        fake_b = g_ab(img_a)
        # Translate images back to original domain
        reconstr_a = g_ba(fake_b)
        reconstr_b = g_ab(fake_a)

        reconstr_a, reconstr_a_names = set_layer_name(reconstr_a, g_ba.name+"_reconstruct_a")
        reconstr_b, reconstr_b_names = set_layer_name(reconstr_b, g_ab.name+"_reconstruct_b")

        # Identity mapping of images
        img_a_id = g_ba(img_a)
        img_b_id = g_ab(img_b)

        img_a_id, id_a_names = set_layer_name(img_a_id, g_ba.name + "_id_a")
        img_b_id, id_b_names = set_layer_name(img_b_id, g_ab.name + "_id_b")

        valid_a = d_a(fake_a)
        valid_b = d_b(fake_b)

        valid_a, valid_a_names = set_layer_name(valid_a, d_a.name + "_valid_a")
        valid_b, valid_b_names = set_layer_name(valid_b, d_b.name + "_valid_b")

        # ----- Discriminator -----
        outputs = []
        extend(outputs, valid_a)
        extend(outputs, valid_b)
        extend(outputs, reconstr_a)
        extend(outputs, reconstr_b)
        extend(outputs, img_a_id)
        extend(outputs, img_b_id)

        inputs = []
        extend(inputs, img_a)
        extend(inputs, img_b)

        translation_loss,  translation_weight = listify(translation_loss), listify(translation_weight)
        cycle_loss, cycle_weight = listify(cycle_loss), listify(cycle_weight)
        identity_loss, identity_weight = listify(identity_loss), listify(identity_weight)
        translation_metrics = listify(translation_metrics)
        cycle_metrics = listify(cycle_metrics)
        identity_metrics = listify(identity_metrics)

        l, m, w = prepare_compile(valid_a_names + valid_b_names +
                                  reconstr_a_names + reconstr_b_names +
                                  id_a_names + id_b_names,
                                  translation_loss * 2 +       # translation loss
                                  cycle_loss * 2 +       # cycle losses
                                  identity_loss * 2,                 # identity losses
                                  [translation_metrics] * len(valid_a_names + valid_b_names) +  # translation metrics
                                  [cycle_metrics] * len(reconstr_a_names + reconstr_b_names) +  # cycle metrics
                                  [identity_metrics] * len(id_a_names + id_a_names),            # identity metrics
                                  translation_weight * 2 +     # translation weights
                                  cycle_weight * 2 +     # cycle weights
                                  identity_weight * 2)               # identity weights

        generator_model = Model(inputs=inputs, outputs=outputs)
        generator_model.compile(loss=l, metrics=m, loss_weights=w, optimizer=optimizer)

        # ----- Discriminator -----
        for dis in discriminator:
            dis.trainable = True
        return generator_model

    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None, **kwargs):
        # Discriminator Training
        out_shape = get_model_output(model.discriminator_model()[0], batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.train_on_batch(x + y,        # a, b
                                            self.ones +   # discriminator_output_from_real_samples a
                                            self.ones +   # discriminator_output_from_real_samples b
                                            self.zeros +  # discriminator_output_from_fake_samples a
                                            self.zeros,   # discriminator_output_from_fake_samples b
                                            sample_weight=sample_weight)

        return loss

    def train_generator(self, model, generator, x, y, batch_size, sample_weight=None, **kwargs):
        # Discriminator Training
        out_shape = get_model_output(model.discriminator_model()[0], batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = generator.train_on_batch(x + y,  # a, b
                                        self.ones + self.ones +  # discriminator outs a, b
                                        x + y +  # a, b - reconstruction
                                        x + y,  # a, b - identity
                                        sample_weight=sample_weight)

        return loss

    def test_on_generator(self, model, generator, x, y, batch_size, sample_weight=None):
        # Generator Testing
        out_shape = get_model_output(model.discriminator_model()[0], batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = generator.test_on_batch(x + y,  # a, b
                                       self.ones + self.ones +  # discriminator outs a, b
                                       x + y +  # a, b - reconstruction
                                       x + y,  # a, b - identity
                                       sample_weight=sample_weight)

        return loss

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        # Discriminator Testing
        out_shape = get_model_output(model.discriminator_model()[0], batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.test_on_batch(x + y,        # a, b
                                           self.ones +   # discriminator_output_from_real_samples a
                                           self.ones +   # discriminator_output_from_real_samples b
                                           self.zeros +  # discriminator_output_from_fake_samples a
                                           self.zeros,   # discriminator_output_from_fake_samples b
                                           sample_weight=sample_weight)

        return loss


class CycleWGAN_TrainingScheme(CycleGAN_TrainingScheme):
    def __init__(self, batch_size, **kwargs):
        super(CycleWGAN_TrainingScheme, self).__init__(**kwargs)
        self.batch_size = batch_size
        self.mones = None

    def compile_discriminator(self, model, generator, discriminator, optimizer=None, metrics=[], gp_weight=10,
                              **kwargs):
        for dis in discriminator:
            dis.trainable = True

        for gen in generator:
            gen.trainable = False

        model_shape = get_model_input(generator[0])
        img_a = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        model_shape = get_model_input(generator[1])
        img_b = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        inputs = []
        extend(inputs, img_a)
        extend(inputs, img_b)

        g_ba, g_ab = generator[0], generator[1]
        d_a, d_b = discriminator[0], discriminator[1]

        fake_b = g_ab(img_a)
        fake_a = g_ba(img_b)

        dis_out_real_b, dis_out_real_names_b = set_layer_name(d_b(img_b), d_b.name+"_real")
        dis_out_fake_b, dis_out_fake_names_b = set_layer_name(d_b(fake_b), d_b.name+"_fake")

        dis_out_real_a, dis_out_real_names_a = set_layer_name(d_a(img_a), d_a.name+"_real")
        dis_out_fake_a, dis_out_fake_names_a = set_layer_name(d_a(fake_a), d_a.name+"_fake")

        if isinstance(img_a, list):
            averaged_samples_a = [RandomWeightedAverage(self.batch_size)([img_a[i], fake_a[i]])
                                  for i in range(len(img_a))]
        else:
            averaged_samples_a = RandomWeightedAverage(self.batch_size)([img_a, fake_a])

        averaged_samples_out_a, avg_samples_out_a_names = set_layer_name(d_a(averaged_samples_a), d_a.name+"_avg")

        partial_gp_loss_a = [partial(gradient_penalty_loss, averaged_samples=averaged_samples_a,
                                     gradient_penalty_weight=gp_weight) for _ in range(len(averaged_samples_out_a))]
        for i, gp in enumerate(partial_gp_loss_a):
            gp.__name__ = 'gradient_penalty_a_%d' % i

        if isinstance(img_b, list):
            averaged_samples_b = [RandomWeightedAverage(self.batch_size)([img_b[i], fake_b[i]])
                                  for i in range(len(img_b))]
        else:
            averaged_samples_b = RandomWeightedAverage(self.batch_size)([img_b, fake_b])

        averaged_samples_out_b, avg_samples_out_b_names = set_layer_name(d_b(averaged_samples_b), d_b.name+"_avg")

        partial_gp_loss_b = [partial(gradient_penalty_loss, averaged_samples=averaged_samples_b,
                                     gradient_penalty_weight=gp_weight) for _ in range(len(averaged_samples_out_b))]
        for i, gp in enumerate(partial_gp_loss_b):
            gp.__name__ = 'gradient_penalty_b_%d' % i

        outputs = []
        extend(outputs, dis_out_real_a)
        extend(outputs, dis_out_real_b)
        extend(outputs, dis_out_fake_a)
        extend(outputs, dis_out_fake_b)
        extend(outputs, averaged_samples_out_a)
        extend(outputs, averaged_samples_out_b)

        names = dis_out_real_names_a + dis_out_real_names_b + dis_out_fake_names_a + dis_out_fake_names_b + \
                avg_samples_out_a_names + avg_samples_out_b_names

        loss = [wasserstein_loss]
        metrics = listify([metrics])
        if len(metrics) == 1:
            metrics = [metrics[0]] * len(dis_out_real_names_a)
        elif all([not isinstance(m, list) for m in metrics]):
            metrics = [metrics] * len(dis_out_real_names_a)

        l, m, _ = prepare_compile(names,
                                  loss * 4 + partial_gp_loss_a + partial_gp_loss_b,
                                  metrics * 4)

        discriminator_model = Model(inputs=inputs, outputs=outputs)
        discriminator_model.compile(optimizer=optimizer, loss=l, metrics=m)

        for gen in generator:
            gen.trainable = True
        return discriminator_model

    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None, **kwargs):
        # Discriminator Training

        out_shape = get_model_output(model.discriminator_model()[0], batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in out_shape]
            self.mones = [-np.ones(out_shape)] if not isinstance(out_shape, list) else [-np.ones(shape) for shape in out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.train_on_batch(x + y,  # a, b
                                            self.ones +  # discriminator_output_from_real_samples a
                                            self.ones +  # discriminator_output_from_real_samples b
                                            self.mones +  # discriminator_output_from_fake_samples a
                                            self.mones +  # discriminator_output_from_fake_samples b
                                            self.zeros +  # averaged_samples_out a
                                            self.zeros,   # averaged_samples_out b
                                            sample_weight=sample_weight)
        return loss

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        # Discriminator Testing
        out_shape = get_model_output(model.discriminator_model()[0], batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in out_shape]
            self.mones = [-np.ones(out_shape)] if not isinstance(out_shape, list) else [-np.ones(shape) for shape in out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.test_on_batch(x + y,  # a, b
                                           self.ones +  # discriminator_output_from_real_samples a
                                           self.ones +  # discriminator_output_from_real_samples b
                                           self.mones +  # discriminator_output_from_fake_samples a
                                           self.mones +  # discriminator_output_from_fake_samples b
                                           self.zeros +  # averaged_samples_out a
                                           self.zeros,   # averaged_samples_out b
                                           sample_weight=sample_weight)
        return loss
