"""
draw graph of container stacked states
this file can draw graph using only setting from config file

"""

import networkx as nx
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from config import CFG


class container_env:
    def __init__(self):
        self.action_list = self.make_action_list(CFG.st)


    def make_action_list(self, state):
        action_list = []
        for i in range(len(state[0])):
            for j in range(len(state[0])):
                if i != j:
                    action_list.append([1, i, j])

        return action_list


    def get_valid_moves(self, state, action_list):
        valid_moves = deepcopy(action_list)
        stack_size = []
        for i in range(len(state[0])):
            tmp_stack_size = 0
            for j in range(len(state)):
                if state[j][i] != 0:
                    tmp_stack_size += 1
            stack_size.append(tmp_stack_size)

        for i in range(len(stack_size)):
            for j in range(len(valid_moves)):

                if stack_size[i] == 0 and valid_moves[j][1] == i:
                    valid_moves[j][0] = 0
                if stack_size[i] == len(state) and valid_moves[j][2] == i:
                    valid_moves[j][0] = 0

        return valid_moves


    def get_valid_action_index(self, valid_moves):
        valid_action_index = []
        for i in range(len(valid_moves)):
            if valid_moves[i][0] == 1:
                valid_action_index.append(i)

        return valid_action_index


    def execute_action(self, state, action_index):
        rot_action_list = np.rot90(self.action_list, 3)
        new_action_list = []
        new_action_list.append(rot_action_list[1])
        new_action_list.append(rot_action_list[2])
        new_action_list = np.rot90(new_action_list, 1)
        action = new_action_list[action_index]

        target_plate = 0
        out_zone_tier = -1
        in_zone_tier = -1

        for i in range(len(state)):
            if state[i][action[0]] != 0:
                out_zone_tier = i
                break

        for i in range(1, len(state) + 1):
            if state[-i][action[1]] == 0:
                in_zone_tier = len(state) - i
                break

        if in_zone_tier == -1 or out_zone_tier == -1:
            pass
        else:
            for i in range(len(state)):
                if state[i][action[0]] != 0:
                    target_plate = state[i][action[0]]
                    state[i][action[0]] = 0
                    break

            for i in range(1, len(state) + 1):
                if state[-i][action[1]] == 0:
                    in_zone_tier = len(state) - i
                    state[-i][action[1]] = target_plate
                    break

        return state


    def get_neighbor_states(self, state):
        neighbor_states = []
        valid_moves = self.get_valid_moves(state, self.action_list)
        valid_action_index = self.get_valid_action_index(valid_moves)

        for i in range(len(valid_action_index)):
            tmpstate = deepcopy(state)
            tmpstate = deepcopy(self.execute_action(tmpstate, valid_action_index[i]))
            neighbor_states.append(tmpstate)

        return neighbor_states


class draw_graph:
    def __init__(self):
        self.G = nx.Graph()
        self.path_node_list = []
        self.other_node_list = []
        self.initial_node = -1
        self.target_node = 0
        self.path_edge_list = []


    def start(self, state_history, difficulty):
        Initial_state = CFG.st

        node_num = 0

        self.G.add_node(node_num)
        self.G.node[node_num]['state'] = Initial_state
        self.G.node[node_num]['neighbor_states'] = container_env().get_neighbor_states(Initial_state)

        while True:
            self.expand(node_num)
            node_num += 1

            if len(self.G.node) == node_num+1:
                break

        print(f'number of nodes: {len(self.G.nodes)}')
        print(f'number of edges: {len(self.G.edges)}')

        self.get_path_node_list(state_history)

        positions = [[nx.fruchterman_reingold_layout(self.G),'fruchterman_reingold_layout'],
                     [nx.spring_layout(self.G),'spring_layout'], [nx.kamada_kawai_layout(self.G),'kamada_kawai_layout'],
                     [nx.spectral_layout(self.G),'spectral_layout']]

        for position in positions:
            pos = position[0]
            name = str(position[1]) + str(difficulty)
            nx.draw_networkx_edges(self.G, pos, width=0.1, edge_color='#adadad')
            nx.draw_networkx_nodes(self.G, pos, nodelist=self.other_node_list, node_color='#000000', node_size=0.5, alpha=0.3)
            nx.draw_networkx_edges(self.G, pos, edgelist=self.path_edge_list, width=0.2, edge_color='#000000')
            nx.draw_networkx_nodes(self.G, pos, nodelist=self.path_node_list, node_color='#000000', node_size=1)
            nx.draw_networkx_nodes(self.G, pos, nodelist=[self.initial_node], node_color='#0026ff', node_size=1.5)
            nx.draw_networkx_nodes(self.G, pos, nodelist=[self.target_node], node_color='#ff0000', node_size=1.5)
            plt.savefig(str(name) + '.jpg', dpi=1000)
            plt.close()


    def get_path_node_list(self, state_history):
        for i in range(len(self.G.node)):
            path_node_found = False
            for j in range(len(state_history)):
                if np.array_equal(self.G.node[i]['state'], state_history[j]):
                    if np.array_equal(state_history[j], CFG.s0):
                        self.initial_node = i

                    self.path_node_list.append(i)
                    path_node_found = True
                    del state_history[j]
                    break
            if not path_node_found:
                self.other_node_list.append(i)

        for i in range(len(self.path_node_list)):
            self.path_edge_list.append((self.path_node_list[i], self.path_node_list[i+1]))
            if i+2 == len(self.path_node_list):
                break


    def expand(self, node_num):
        for j in range(len(self.G.node[node_num]['neighbor_states'])):

            same_exist = False

            for k in range(len(self.G.node)):
                tmp_num_nodes = len(self.G.node)
                if self.G.node[node_num]['neighbor_states'][j] == self.G.node[tmp_num_nodes - k - 1]['state']:
                    same_exist = True
                    self.G.add_edge(node_num, tmp_num_nodes - k - 1)
                    break

            if same_exist == False:
                self.G.add_node(len(self.G.node))
                self.G.add_edge(node_num, len(self.G.node) - 1)
                self.G.node[len(self.G.node) - 1]['state'] = self.G.node[node_num]['neighbor_states'][j]
                self.G.node[len(self.G.node) - 1]['neighbor_states'] = container_env().get_neighbor_states(self.G.node[len(self.G.node) - 1]['state'])







