"""
starting main file
"""
from container_terminal import Container_stockyard
from neural_net import NeuralNetworkWrapper
from train import Train
import tensorflow as tf


from itertools import product
from config import CFG

def get_num_shapes():
    num_stack = CFG.num_stack
    max_stack = CFG.max_tier
    num_containers = len(CFG.containers)

    tiers = list(range(0, max_stack+1))
    list_for_iter = [tiers]*num_stack
    potential_shape = list(product(*list_for_iter))

    shape_count = 0
    shape_list = []
    for i in range(len(potential_shape)):
        if sum(potential_shape[i]) == num_containers:
            shape_list.append(potential_shape[i])
            shape_count += 1

    return shape_count


import operator
from collections import Counter
from math import factorial
from functools import reduce

def npermutations():
    num = factorial(len(CFG.containers))
    mults = Counter(CFG.containers).values()
    den = reduce(operator.mul, (factorial(v) for v in mults), 1)
    return int(num / den)


if __name__ == '__main__':
    """Initializes game state, neural network and the training loop"""

    # Initialize the game object with the chosen game
    game = Container_stockyard()

    sess = tf.compat.v1.Session()
    net = NeuralNetworkWrapper(game, sess)
    sess.run(tf.compat.v1.global_variables_initializer())

    num_possible_states = get_num_shapes()*npermutations()
    print('|'*30, 'START', '|'*30)
    print(f'Number of possible states:{format(num_possible_states, "10.2e")}')
    print('Number of target state: 1')
    print(f'Goal is to reach 1 target state among{format(num_possible_states, "10.2e")} different states')

    train = Train(game, net)
    train.start()

