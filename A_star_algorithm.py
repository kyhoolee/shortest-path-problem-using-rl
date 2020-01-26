'''
A* algorithm
use networkx
'''

import networkx as nx
from copy import deepcopy
import numpy as np
from config import CFG
import datetime
import time
import math

class A_star:
    def __init__(self, net, A_star_sim = 1024, check_repeat_state = True):
        '''
        :param net: neural network
        :param A_star_sim: number of simulation
        :param check_repeat_state
            if True: graph
            if False: tree
        '''
        self.env = None
        self.net = net
        self.A_star_sim = A_star_sim
        self.check_repeat_state = check_repeat_state
        if self.check_repeat_state:
            self.check_parent_node = False
        else:
            self.check_parent_node = True


    def expand_node(self):
        # execute all possible action from selected node
        self.env.state = deepcopy(self.G.node[self.selected_node]['state'])
        valid_moves = self.env.get_valid_moves()
        value_pi = self.net.predict_value_policy([self.env.state, self.env.target_state])
        do_not_check_parent = False
        for i in range(len(valid_moves)):
            if valid_moves[i][0] != 0:
                self.env.state = deepcopy(self.G.node[self.selected_node]['state'])
                self.env.execute_action(valid_moves[i])
                same_state = False
                same_parent_state = False
                if self.check_repeat_state:
                    same_state = self.check_same_state()
                if self.check_parent_node:  # check if selected nodes state and generated child state is same
                    if not do_not_check_parent:
                        same_parent_state = self.check_same_parent_node()
                        if same_parent_state:
                            do_not_check_parent = True

                if not same_state and not same_parent_state:
                    self.store_node_infos(i, value_pi[i])  # add new node

            # if selected node is root node and impossible action
            else:
                if self.selected_node == 0:
                    self.child_node_Nsa.append([-1, 0, i])

        # add expanded node to closed node list
        self.closed_node_list.append([self.selected_node, self.G.node[self.selected_node]['score']])

        for open_idx in self.open_node_list:
            if open_idx[0] == self.selected_node:
                self.open_node_list.remove([self.selected_node, open_idx[1]])
                break


    def check_same_parent_node(self):
        same_state = np.array_equal(self.G.node[self.G.node[self.selected_node]['parent_node']]['state'], self.env.state)
        if same_state:
            return True
        else:
            return False


    def check_same_state(self):
        same_state_exist = False
        # check for same state in open node list
        for i in range(len(self.open_node_list)):
            # if same state exist
            if np.array_equal(self.env.state, self.G.node[self.open_node_list[i][0]]['state']):
                same_state_exist = True
                self.get_score(self.selected_node)
                tmp_score = self.G.node[self.selected_node]['score'] + 1

                if self.open_node_list[i][1] > tmp_score:
                    self.open_node_list[i][1] = deepcopy(tmp_score)
                    self.G.node[self.open_node_list[i][0]]['parent_node'] = self.selected_node
                break

        # check for same state in closed node list
        if not same_state_exist:
            for i in range(len(self.closed_node_list)):
                if np.array_equal(self.env.state, self.G.node[self.closed_node_list[i][0]]['state']):
                    same_state_exist = True
                    break

        return same_state_exist


    def store_node_infos(self, action_num, predicted_value):
        # create new node and store infos
        new_node_num = len(self.G.node)
        self.G.add_node(new_node_num)
        self.G.add_edge(self.selected_node, new_node_num)
        self.G.node[new_node_num]['state'] = deepcopy(self.env.state)
        self.get_value(new_node_num, predicted_value)
        self.G.node[new_node_num]['dist_from_root'] = self.G.node[self.selected_node]['dist_from_root'] + 1
        self.get_score(new_node_num)
        self.G.node[new_node_num]['parent_node'] = self.selected_node

        self.open_node_list.append([new_node_num, self.G.node[new_node_num]['score']])

        if self.selected_node == 0:
            self.child_node_Nsa.append([new_node_num, 0, action_num])


    def select_node(self):
        '''
        selected node with lowest score in open node list
        '''
        open_node_score_list =[i[1] for i in self.open_node_list]

        chosen_score = min(open_node_score_list)

        chosen_idx = open_node_score_list.index(chosen_score)
        self.selected_node = self.open_node_list[chosen_idx][0]


    def get_Nsa(self):
        for closed_node_idx in range(len(self.closed_node_list)):
            node_num = self.closed_node_list[closed_node_idx][0]

            child_node_found = False

            while True:
                for child_node_num in range(len(self.child_node_Nsa)):
                    if self.child_node_Nsa[child_node_num][0] == node_num:
                        child_node_found = True
                        self.child_node_Nsa[child_node_num][1] += 1
                        break
                if child_node_found == True:
                    break
                node_num = self.G.node[node_num]['parent_node']

        for i in range(len(self.child_node_Nsa)):
            self.pi_Nsa.append(self.child_node_Nsa[i][1])


    def get_score(self, node_num):
        self.G.node[node_num]['score'] = math.log(self.G.node[node_num]['value'], CFG.value_decay_rate) + self.G.node[node_num]['dist_from_root']


    def get_value(self, node_num, predicted_value):
        done, _ = self.env.check_target_state_reached()

        if done:
            predicted_value = 1.
            self.target_state_reached = True
            self.target_node_num = node_num
        else:
            if predicted_value == 0:
                # store value very small number if predicted value is 0, since h(n) use log
                predicted_value = 10**(-100)

        self.G.node[node_num]['value'] = predicted_value

    ## 작성 완료, 디버그 확인 필요
    def get_tar_reached_child_node(self):
        child_node_found = False
        node_num = self.target_node_num
        action_num = -1
        while True:
            for child_node_num in range(len(self.child_node_Nsa)):
                if self.child_node_Nsa[child_node_num][0] == node_num:
                    child_node_found = True
                    action_num = child_node_num
                    break
            if child_node_found:
                break
            node_num = self.G.node[node_num]['parent_node']

        return action_num


    def get_pi(self):
        # calculate pi with Nsa list
        if not self.target_state_reached:
            self.get_Nsa()

            sum_Nsa = sum(self.pi_Nsa)

            Nsa_list = []
            for i in range(len(self.pi_Nsa)):
                Nsa_list.append(self.pi_Nsa[i]/sum_Nsa)
            psa_vector = np.array(Nsa_list)
        else:
            child_node_num = self.get_tar_reached_child_node()
            psa_vector = [0] * self.env.action_size
            psa_vector[child_node_num] = 1

        return psa_vector


    def search(self, env):
        self.env = env
        self.open_node_list = []  # [node number, f(n)]
        self.closed_node_list = []
        self.selected_node = 0
        self.pi_Nsa = []
        self.target_state_reached = False
        self.target_node_num = -1

        self.child_node_Nsa = []

        self.G = nx.Graph()
        self.G.add_node(0)

        self.G.node[0]['state'] = self.env.state
        self.get_value(0, 0)  # (node number, predicted value(value pi))
        self.G.node[0]['dist_from_root'] = 0
        self.get_score(0)  # in this code f(n) will be called score
        self.G.node[0]['parent_node'] = 0
        self.open_node_list.append([0, self.G.node[0]['score']])


        for _ in range(self.A_star_sim):
            self.expand_node()
            self.select_node()

            if self.target_state_reached:
                break


        del self.closed_node_list[0]
        self.env.state = deepcopy(self.G.node[0]['state'])

        psa_vector = self.get_pi()


        return psa_vector
