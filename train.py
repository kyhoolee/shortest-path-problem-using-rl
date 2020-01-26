"""
generate data, learning, check sorting
"""
from config import CFG
from generate_data import gen_data
from make_target_state import gen_tar_state
from copy import deepcopy
import datetime
from test import sort

class Train:
    """generate data with A* algorithm, train with neural network.
    Attributes:
        env: environment.
        net: neural network.
    """
    def __init__(self, env, net):
        self.env = env
        self.net = net


    def start(self):
        start_time = datetime.datetime.now()
        T_state = gen_tar_state(self.env.columns, self.env.rows, len(self.env.containers))
        generate_data = gen_data(self.net, self.env)
        test = sort(self.net, self.env)

        for difficulty in range(1, CFG.difficulty + 1):
            print('=' * 80)
            print('difficulty', difficulty, 'start')
            print('-' * 25)

            game_start_time = datetime.datetime.now()
            gen_data_start_time = datetime.datetime.now()

            # list for storing data
            value_data = []
            value_pi_data = []

            # repeat generating data until its bigger than CFG.maximum data
            while len(value_data) < CFG.maximum_data:
                # generate random target state
                T_state.containers = deepcopy(self.env.containers)
                tar_state = T_state.make_tar_state()

                # generate data with A* algorithm
                tmp_value_data, tmp_value_pi_data = generate_data.generate_data(tar_state, difficulty=difficulty)
                # add data
                value_data = value_data + tmp_value_data
                value_pi_data = value_pi_data + tmp_value_pi_data

            print(len(value_data), 'data generated')
            gen_data_end_time = datetime.datetime.now()
            print('data generating time: ', gen_data_end_time - gen_data_start_time)
            print('generate data complete time: ', datetime.datetime.now())

            # train value
            train_start_time = datetime.datetime.now()
            self.net.train_value(value_data)
            self.net.train_value_pi(value_pi_data)
            train_end_time = datetime.datetime.now()
            print('training time: ', train_end_time - train_start_time)
            print('difficulty', difficulty, ' generating data and training complete')
            print('-' * 25)


            ###
            T_state.containers = deepcopy(self.env.containers)
            tar_state = T_state.make_tar_state()
            value = self.net.predict_value([tar_state, tar_state])
            value_policy = self.net.predict_value_policy([tar_state, tar_state])
            print(tar_state)
            print(f'출력된 value: {value}')
            print(f'출력된 value_policy: {value_policy}')
            self.env.state = deepcopy(tar_state)
            valid_moves = self.env.get_valid_moves()
            for i in range(len(valid_moves)):
                if valid_moves[i][0] != 0:
                    action_num = i
                    break
            self.env.execute_action(valid_moves[action_num])
            value = self.net.predict_value([self.env.state, tar_state])
            #value_policy = self.net.predict_value_policy([self.env.state, tar_state])
            print(self.env.state)
            print(f'출력된 value: {value}')
            #print(f'출력된 value_policy: {value_policy}')
            print('-' * 25)
            ###



            #if difficulty > 5:
            # check sorting with CFG.sn(initial state)
            print('start test')
            test.search(difficulty)

            # print time consumption
            print('-' * 25, 'summary', '-'*25)
            print('difficulty', difficulty, ' complete')
            print('completed time: ', datetime.datetime.now())
            print('data generating time: ', gen_data_end_time - gen_data_start_time)
            print('training time: ', train_end_time - train_start_time)
            print('this difficulty time: ', datetime.datetime.now() - game_start_time)
            print('total time: ', datetime.datetime.now() - start_time)




