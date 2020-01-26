"""
generating data
"""
from copy import deepcopy
import numpy as np
import random
from config import CFG
from A_star_algorithm import A_star


class gen_data:
    def __init__(self, net, env):
        self.net = net
        self.env = env
        # A* algorithm for generate pi
        self.value_pi_A_star = A_star(self.net, A_star_sim=CFG.num_A_star_sims, check_repeat_state=False)


    def generate_data(self, tar_state, difficulty):
        # main function
        self.env.state = deepcopy(tar_state)
        self.env.target_state = deepcopy(tar_state)
        # list for storing data
        self.generated_data = []

        # number of action to execute to generate initial state
        num_actions = round(difficulty * CFG.adjust_difficulty)
        self.set_difficulty(num_actions)

        while True:
            # generate/store value_pi data
            value_pi = self.get_value_pi()
            combined_state = [self.env.state, self.env.target_state]
            self.generated_data.append(deepcopy([combined_state, value_pi, 0]))

            # if terminal state is reached stop generating data
            done, _ = self.env.check_target_state_reached()
            if done:
                self.generated_data.reverse()
                break
            # if sorting is incomplete in less than num_actions action than erase all stored data
            if len(self.generated_data) > num_actions:
                self.generated_data = []
                break

            # get policy through A* algorithm
            pi = self.value_pi_A_star.search(self.env)

            # apply temperature parameter to policy
            temped_pi = self.apply_temp_parameter(pi)

            # execute pi
            self.exe_policy(temped_pi)

        # store value for each states in data list
        self.get_value()

        # augment data
        training_data = []
        generated_value_data = []
        generated_value_pi_data = []
        if len(self.generated_data) > 0:
            for current_data in self.generated_data:
                tmp_training_data = []
                tmp_training_data = self.augment_data(current_data, tmp_training_data)
                training_data = training_data + tmp_training_data

            training_data = np.array(training_data)
            generated_value_data = training_data[:, [0,2]]
            generated_value_pi_data = training_data[:, 0:2]

        return list(generated_value_data), list(generated_value_pi_data)


    def get_value_pi(self):
        '''
        generate value pi data for training
        '''
        valid_moves = self.env.get_valid_moves()
        current_state = deepcopy(self.env.state)

        value_list = []
        for i in range(self.env.action_size):
            # if action idx is possible, execute action and get child state
            if valid_moves[i][0] == 1:
                self.env.execute_action(valid_moves[i])
                combined_state = deepcopy([self.env.state, self.env.target_state])
                # if generated child state is terminal state, store value as 1.0
                done, _ = self.env.check_target_state_reached()
                if done:
                    v = 1.
                else:
                    v = self.net.predict_value(combined_state)
                value_list.append(v)
                self.env.state = deepcopy(current_state)
            # if action idx is impossible, store value as 0
            else:
                value_list.append(0)

        return value_list


    def exe_policy(self, policy):
        # execute policy
        action_list = self.env.get_valid_moves()
        policy = np.array([policy])

        selected_act_num = np.random.choice(range(policy.shape[1]), p=policy.ravel())

        self.env.execute_action(action_list[selected_act_num])


    def apply_temp_parameter(self, policy):
        '''
        apply temperature parameter like Alphago zero
        '''
        for idx, p in enumerate(policy):
            policy[idx] = p ** CFG.train_temp_value

        sum_policy = sum(policy)
        for i in range(len(policy)):
            policy[i] = policy[i] / sum_policy

        return policy


    def set_difficulty(self, num_actions):
        '''
        execute random actions 'num_actions' times
        generate initial state
        '''
        step = 0
        while True:
            policy = self.create_pi_rand()

            self.exe_policy(policy)

            step += 1

            done, _ = self.env.check_target_state_reached()
            if done: step = 0
            if step == num_actions: break


    def create_pi_rand(self):
        '''
        create random policy with possible actions
        random policy is used for difficulty settings
        '''
        valid_move = self.env.get_valid_moves()
        policy = []
        possible_actions = 0
        for i in range(len(valid_move)):
            if valid_move[i][0] != 0:
                policy.append(1)
                possible_actions += 1
            else:
                policy.append(0)

        for i in range(len(policy)):
            if policy[i] == 1:
                policy[i] = 1 / possible_actions

        return policy


    def get_value(self):
        '''
        store value in data list
        '''

        for i in range(len(self.generated_data)):
            value = CFG.value_decay_rate ** i
            self.generated_data[i][2] = value


    def augment_data(self, current_data, training_data):
        # augment data
        import itertools

        column_index = []
        for i in range(self.env.columns):
            column_index.append(i)

        index_permuatation = itertools.permutations(column_index)
        possible_indexes = []

        for i in index_permuatation:
            possible_indexes.append(i)

        if CFG.augment_size != False:
            sampled_index = random.sample(possible_indexes, CFG.augment_size)
            possible_indexes = sampled_index

        original_state = deepcopy(current_data[0][0])
        target_state = deepcopy(current_data[0][1])

        tmp_list = []
        for i in range(len(original_state[0])):
            tmp_list.append(i)
        original_state = np.vstack((original_state, tmp_list))
        target_state = np.vstack((target_state, tmp_list))

        original_list = []
        original_psa_vector = deepcopy(current_data[1])

        for i in range(len(self.env.action_list)):
            original_list.append([])
            original_list[i].append(self.env.action_list[i][1])
            original_list[i].append(self.env.action_list[i][2])
            original_list[i].append(original_psa_vector[i])

        rotated_state = np.rot90(original_state, 3)
        rotated_target_state = np.rot90(target_state, 3)

        for i in range(len(possible_indexes)):

            new_index = possible_indexes[i]
            new_state = []
            for j in range(len(rotated_state)):
                new_state.append(rotated_state[new_index[j]])
            new_state = np.rot90(new_state, 1)

            new_target_state = []
            for j in range(len(rotated_target_state)):
                new_target_state.append(rotated_target_state[new_index[j]])
            new_target_state = np.rot90(new_target_state, 1)


            new_list = []
            for j in range(len(self.env.action_list)):
                new_list.append([])
                new_list[j].append(self.env.action_list[j][1])
                new_list[j].append(self.env.action_list[j][2])
                retrieving_stack = new_state[-1][new_list[j][0]]
                stacking_stack = new_state[-1][new_list[j][1]]

                for k in range(len(original_list)):
                    if original_list[k][0] == retrieving_stack and original_list[k][1] == stacking_stack:
                        new_list[j].append(original_list[k][2])
                        break

            new_psa_vector = []
            for j in range(len(new_list)):
                new_psa_vector.append(new_list[j][2])

            new_state = np.delete(new_state, -1, 0)
            new_target_state = np.delete(new_target_state, -1, 0)
            new_combined_state = [new_state, new_target_state]

            training_data.append([new_combined_state, new_psa_vector, current_data[2]])

        return training_data

