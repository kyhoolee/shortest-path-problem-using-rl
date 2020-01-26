"""
network for learning
"""
import tensorflow as tf
import numpy as np
from config import CFG
import random


class value_network:
    def __init__(self, sess, game, filter_size = 256):
        self.sess = sess
        self.name = 'value_network'
        self.rows = game.rows
        self.columns = game.columns
        self.action_size = game.action_size
        self.filter_size = filter_size
        self.num_actions = game.columns*(game.columns-1)
        self._build_net()

    def _build_net(self):
        with tf.variable_scope(self.name):
            self.state = tf.placeholder(tf.float32, shape=[None, self.rows * 2 * self.columns])
            input_layer = tf.reshape(self.state, [-1, self.rows * 2, self.columns, 1])

            self.value = tf.placeholder(tf.float32, shape=[None])

            conv1 = tf.layers.conv2d(inputs=input_layer, filters=self.filter_size, kernel_size=[2, 2], padding='SAME',
                                     kernel_initializer=tf.contrib.layers.xavier_initializer(), strides=1)
            conv1_batch_norm = tf.layers.batch_normalization(inputs=conv1)
            resnet_in_out = tf.nn.relu(conv1_batch_norm)

            for _ in range(CFG.value_head_layers):
                res_conv1 = tf.layers.conv2d(inputs=resnet_in_out, filters=self.filter_size, kernel_size=[2, 2],
                                             kernel_initializer=tf.contrib.layers.xavier_initializer(), padding='SAME', strides=1)
                batch_norm1 = tf.layers.batch_normalization(inputs=res_conv1)
                activate_batch_norm1 = tf.nn.relu(batch_norm1)

                res_conv2 = tf.layers.conv2d(inputs=activate_batch_norm1, filters=self.filter_size, kernel_size=[2, 2],
                                             kernel_initializer=tf.contrib.layers.xavier_initializer(), padding='SAME', strides=1)
                batch_norm2 = tf.layers.batch_normalization(inputs=res_conv2)
                added_layer = tf.add(batch_norm2, resnet_in_out)
                resnet_in_out = tf.nn.relu(added_layer)

            flatten_resnet = tf.reshape(resnet_in_out, [-1, self.filter_size * self.rows * 2 * self.columns])
            dense1 = tf.layers.dense(inputs=flatten_resnet, units=self.filter_size * self.rows * self.columns/4, activation=tf.nn.relu,
                                     kernel_initializer=tf.contrib.layers.xavier_initializer())
            dense2 = tf.layers.dense(inputs=dense1, units=self.filter_size * self.rows * self.columns / 16,
                                     activation=tf.nn.relu,
                                     kernel_initializer=tf.contrib.layers.xavier_initializer())
            vs = tf.layers.dense(inputs=dense2, units=1)
            self.vs = tf.nn.sigmoid(vs)

            self.v_cost = tf.losses.mean_squared_error(self.vs, tf.reshape(self.value, shape=[-1, 1]))

            # l2_regularization
            total_vars = tf.compat.v1.trainable_variables()
            weights_name_list = [var for var in total_vars if "kernel" in var.name]
            loss_holder = []
            for w in range(len(weights_name_list)):
                l2_loss = tf.nn.l2_loss(weights_name_list[w])
                loss_holder.append(l2_loss)
            self.regular_cost = tf.reduce_mean(loss_holder) * CFG.l2_val

            self.total_cost = self.v_cost + self.regular_cost

            self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=CFG.learning_rate).minimize(self.total_cost)


class value_pi_network:
    def __init__(self, sess, game, filter_size = 256):
        self.sess = sess
        self.name = 'value_pi_network'
        self.rows = game.rows
        self.columns = game.columns
        self.action_size = game.action_size
        self.filter_size = filter_size
        self.num_actions = game.columns*(game.columns-1)
        self._build_net()

    def _build_net(self):
        with tf.variable_scope(self.name):
            self.state = tf.placeholder(tf.float32, shape=[None, self.rows * 2 * self.columns])
            input_layer = tf.reshape(self.state, [-1, self.rows * 2, self.columns, 1])

            self.value_pi = tf.placeholder(tf.float32, shape=[None, self.num_actions])

            conv1 = tf.layers.conv2d(inputs=input_layer, filters=self.filter_size, kernel_size=[2, 2], padding='SAME',
                                     kernel_initializer=tf.contrib.layers.xavier_initializer(), strides=1)
            conv1_batch_norm = tf.layers.batch_normalization(inputs=conv1)
            resnet_in_out = tf.nn.relu(conv1_batch_norm)

            for _ in range(CFG.value_pi_head_layers):
                res_conv1 = tf.layers.conv2d(inputs=resnet_in_out, filters=self.filter_size, kernel_size=[2, 2],
                                             kernel_initializer=tf.contrib.layers.xavier_initializer(), padding='SAME', strides=1)
                batch_norm1 = tf.layers.batch_normalization(inputs=res_conv1)
                activate_batch_norm1 = tf.nn.relu(batch_norm1)

                res_conv2 = tf.layers.conv2d(inputs=activate_batch_norm1, filters=self.filter_size, kernel_size=[2, 2],
                                             kernel_initializer=tf.contrib.layers.xavier_initializer(), padding='SAME', strides=1)
                batch_norm2 = tf.layers.batch_normalization(inputs=res_conv2)
                added_layer = tf.add(batch_norm2, resnet_in_out)
                resnet_in_out = tf.nn.relu(added_layer)


            flatten_resnet = tf.reshape(resnet_in_out, [-1, self.filter_size * self.rows * self.columns * 2])
            dense1 = tf.layers.dense(inputs=flatten_resnet, units=self.filter_size * self.rows * self.columns/4, activation=tf.nn.relu,
                                     kernel_initializer=tf.contrib.layers.xavier_initializer())
            dense2 = tf.layers.dense(inputs=dense1, units=self.filter_size * self.rows * self.columns / 16,
                                     activation=tf.nn.relu,
                                     kernel_initializer=tf.contrib.layers.xavier_initializer())

            value_policy = tf.layers.dense(inputs=dense2, units=self.num_actions, kernel_initializer=tf.contrib.layers.xavier_initializer())
            self.value_policy = tf.nn.sigmoid(value_policy)

            self.value_pi_cost = tf.losses.mean_squared_error(self.value_policy, self.value_pi)


            # l2_regularization
            total_vars = tf.compat.v1.trainable_variables()
            weights_name_list = [var for var in total_vars if "kernel" in var.name]
            loss_holder = []
            for w in range(len(weights_name_list)):
                l2_loss = tf.nn.l2_loss(weights_name_list[w])
                loss_holder.append(l2_loss)
            self.regular_cost = tf.reduce_mean(loss_holder) * CFG.l2_val

            self.total_cost = self.value_pi_cost + self.regular_cost

            self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=CFG.learning_rate).minimize(self.total_cost)


class NeuralNetworkWrapper:
    def __init__(self, game, sess):
        self.game = game
        self.value_net = value_network(sess, self.game)
        self.value_pi_net = value_pi_network(sess, self.game)
        self.sess = sess


    def predict_value(self, state):
        state = np.reshape(state, newshape=[-1, self.game.rows * 2 * self.game.columns])

        v = self.sess.run(self.value_net.vs, feed_dict={self.value_net.state: state})

        return v[0][0]


    def predict_value_policy(self, state):
        state = np.reshape(state, newshape=[-1, self.game.rows * 2 * self.game.columns])

        value_policy = self.sess.run(self.value_pi_net.value_policy, feed_dict={self.value_pi_net.state: state})
        value_policy = np.array(value_policy, dtype=float)

        return value_policy[0]


    def train_value(self, training_data):
        for epoch in range(CFG.epochs):

            examples_num = len(training_data)

            random.shuffle(training_data)

            for i in range(0, examples_num, CFG.batch_size):
                state_data, value_data = map(list, zip(*training_data[i:i + CFG.batch_size]))

                state_data = np.reshape(state_data, newshape=[-1, self.game.rows * 2 * self.game.columns])

                feed_dict = {self.value_net.state: state_data, self.value_net.value: value_data}

                self.sess.run(self.value_net.optimizer, feed_dict=feed_dict)
        print("value train complete")

    def train_value_pi(self, training_data):
        for epoch in range(CFG.epochs):

            examples_num = len(training_data)

            random.shuffle(training_data)

            for i in range(0, examples_num, CFG.batch_size):
                state_data, value_pi_data = map(list, zip(*training_data[i:i + CFG.batch_size]))

                state_data = np.reshape(state_data, newshape=[-1, self.game.rows * 2 * self.game.columns])

                feed_dict = {self.value_pi_net.state: state_data, self.value_pi_net.value_pi: value_pi_data}

                self.sess.run(self.value_pi_net.optimizer, feed_dict=feed_dict)

        print("value policy train complete")