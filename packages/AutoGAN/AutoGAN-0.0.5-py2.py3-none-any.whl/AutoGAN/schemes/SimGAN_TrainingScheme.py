# =========================================================================================================
# File: SimGAN_TrainingScheme.py
# Author: Elad Dvash
#
# Description:
# This file contains an implementation of a SimGAN (https://arxiv.org/abs/1612.07828)
# and supports multi-input, multi-output generators and discriminators
# =========================================================================================================

import numpy as np
from .Base_TrainingScheme import GAN_TrainingScheme
from ..utils.gan_utils import get_model_output, listify


# -----------------------------------------------------------------------------------------------------------------
#  SimGAN Training Scheme
# -----------------------------------------------------------------------------------------------------------------


class SimGAN_TrainingScheme(GAN_TrainingScheme):
    def __init__(self, buffer_length=100000, **kwargs):
        super(SimGAN_TrainingScheme, self).__init__(**kwargs)

        if buffer_length is None:
            assert False, "Must provide buffer length!"
        self.history_buffer = None
        self.history_buffer_weight = None
        self.batch_num = 0
        self.buffer_length = buffer_length

    def init_history_buffer(self, x):
        in_shape = [tuple([self.buffer_length] + list(data.shape[1:])) for data in x] if isinstance(x, list) else \
            tuple([self.buffer_length] + list(x.shape[1:]))
        self.history_buffer = [np.zeros(shape) for shape in in_shape] if isinstance(in_shape, list) else \
            np.zeros(in_shape)
        self.history_buffer_weight = np.ones(in_shape[0] if isinstance(in_shape, list) else in_shape)
        if isinstance(in_shape, list):
            for i in range(len(self.history_buffer)):
                for j in range(self.buffer_length):
                    self.history_buffer[i][j] = x[i][j % x[i].shape[0]]

        else:
            for i in range(self.buffer_length):
                self.history_buffer[i] = x[i % x.shape[0]]

    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None, **kwargs):
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        if self.history_buffer is None:
            self.init_history_buffer(x)

        historical_idxs = np.random.choice(np.arange(self.buffer_length), batch_size // 2)
        place_idxs = np.random.choice(np.arange(x[0].shape[0]), batch_size // 2) if isinstance(x, list) \
            else np.random.choice(np.arange(x.shape[0]), batch_size // 2)

        historical = [data[historical_idxs] for data in self.history_buffer] if isinstance(self.history_buffer, list) \
            else self.history_buffer[historical_idxs]

        replace_idx = np.random.choice(np.arange(x[0].shape[0]), batch_size // 2) if isinstance(x, list) \
            else np.random.choice(np.arange(x.shape[0]), batch_size // 2)

        data_insert = [data[replace_idx] for data in x] if isinstance(x, list) else x[replace_idx]
        insert_data = model.generator_model().predict_on_batch(data_insert)  # add to the buffer

        replaced_idxs = np.random.choice(np.arange(self.buffer_length), batch_size // 2)

        self.history_buffer_weight[replaced_idxs] = sample_weight[replace_idx] if sample_weight is not None else 1
        if sample_weight is not None:
            sample_weight[replace_idx] = self.history_buffer_weight[historical_idxs]

        if isinstance(x, list):
            for i in range(len(x)):
                x[i][place_idxs] = historical[i]
                self.history_buffer[i][replaced_idxs] = insert_data[i]

        else:
            x[place_idxs] = historical
            self.history_buffer[replaced_idxs] = insert_data

        y = listify(y)
        x = listify(x)

        loss = discriminator.train_on_batch(y + x, self.ones + self.zeros,  # [real_samples, fake_samples], [1, 0]
                                            sample_weight=sample_weight)
        return loss

    def train_generator(self, model, generator, x, y, batch_size, sample_weight=None, **kwargs):
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        if self.history_buffer is None:
            self.init_history_buffer(x)

        x = listify(x)
        loss = generator.train_on_batch(x, x + self.ones, sample_weight=sample_weight)  # x, [x, 1]
        return loss

    def test_on_generator(self, model, generator, x, y, batch_size, sample_weight=None):
        # Generator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        x = listify(x)
        loss = generator.test_on_batch(x, x + self.ones, sample_weight=sample_weight)  # x, [x, 1]
        return loss
