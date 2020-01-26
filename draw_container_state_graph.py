"""
draw graph of container stacked states
"""

import networkx as nx
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import datetime
from config import CFG


class container_env:
    def __init__(self):
        self.action_list = self.make_action_list(CFG.st)


    # 가능한 action을 구함
    def make_action_list(self, state):
        action_list = []  # action의 종류
        for i in range(len(state[0])):
            for j in range(len(state[0])):
                if i != j:  # 강재를 빼는 stack과 넣는 stack이 달라야 함, 리스트의 크기는 num_stack*(num_stack)이 됨
                    action_list.append([1, i, j])  # zone i 에서 zone j로 강재를 옮김

        return action_list


    # 가능한 action을 구함[1/0, stack1, stack2]를 출력
    def get_valid_moves(self, state, action_list):
        valid_moves = deepcopy(action_list)
        stack_size = []
        # 각 stack의 강재 갯수 확인
        for i in range(len(state[0])):
            tmp_stack_size = 0
            for j in range(len(state)):
                if state[j][i] != 0:
                    tmp_stack_size += 1
            stack_size.append(tmp_stack_size)

        for i in range(len(stack_size)):
            for j in range(len(valid_moves)):
                # 만약 i번째 stack에 강재가 0개이고, j번째 action의 강재를 빼는 stack이 i번째 stack이라면
                # 해당 action은 불가능한 action으로 설정
                if stack_size[i] == 0 and valid_moves[j][1] == i:
                    valid_moves[j][0] = 0
                # 만약 i번째 stack에 강재가 max_stack개이고, j번째 action의 강재를 쌓는 stack이 i번째 stack이라면
                # 해당 action은 부가능한 action으로 설정
                if stack_size[i] == len(state) and valid_moves[j][2] == i:
                    valid_moves[j][0] = 0

        return valid_moves


    # 가능한 action
    def get_valid_action_index(self, valid_moves):
        valid_action_index = []
        for i in range(len(valid_moves)):
            if valid_moves[i][0] == 1:
                valid_action_index.append(i)

        return valid_action_index


    # 강재를 옮기는 함수
    def execute_action(self, state, action_index):
        # action은 (1*2) array, action[0]은 뺄 강재가 있는 zone의 번호/action[1]은 강재를 쌓을 zone의 번호

        rot_action_list = np.rot90(self.action_list, 3)
        new_action_list = []
        new_action_list.append(rot_action_list[1])
        new_action_list.append(rot_action_list[2])
        new_action_list = np.rot90(new_action_list, 1)
        action = new_action_list[action_index]

        target_plate = 0
        out_zone_tier = -1  # 강재를 빼는 zone의 층 수(이동 작업 전)
        in_zone_tier = -1  # 강재가 들어가는 zone의 층 수(이동 작업 후), zone의 max로 꽉 차있으면 -1

        for i in range(len(state)):  # 빼는 강재의 높이(index로) 구하기
            if state[i][action[0]] != 0:
                out_zone_tier = i
                break

        for i in range(1, len(state) + 1):  # 강재를 쌓는 zone의 강재가 쌓일 높이(index로) 구하기
            if state[-i][action[1]] == 0:  # 강재가 max로 차 있지 않은다면 아래 문구 실행
                in_zone_tier = len(state) - i  # index 구하기
                break

        if in_zone_tier == -1 or out_zone_tier == -1:
            pass
        else:
            for i in range(len(state)):  # 강재를 빼는 작업
                if state[i][action[0]] != 0:
                    target_plate = state[i][action[0]]
                    state[i][action[0]] = 0
                    break

            for i in range(1, len(state) + 1):  # 강재를 쌓는 작업
                if state[-i][action[1]] == 0:
                    in_zone_tier = len(state) - i  # 강재가 쌓인 index 구하기
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


        if not len(self.G.node) > 0:
            start_time = datetime.datetime.now()
            print('계산 시작 시간:', start_time)

            Initial_state = CFG.st

            node_num = 0

            self.G.add_node(node_num)
            self.G.node[node_num]['state'] = Initial_state
            self.G.node[node_num]['neighbor_states'] = container_env().get_neighbor_states(Initial_state)

            # 모든 node를 생성하고 edge 연결
            while True:
                # 현재 node[i]의 neighbor_node의 모든 state를 대상으로 함
                self.expand(node_num)
                node_num += 1

                if node_num % 500 == 0 and node_num != 0:
                    print('현재 생성된 node 개수:', node_num)
                    print('시간:', datetime.datetime.now())

                # 만약 더이상 확인 할 node가 없다면
                if len(self.G.node) == node_num+1:
                    break

            end_time = datetime.datetime.now()
            print(f'종료 시각: {end_time}')
            print(f'소요 시간: {end_time-start_time}')


            num_nodes = len(self.G.nodes)
            num_edges = len(self.G.edges)
            yard_num_actions = (len(self.G.node[0]['state'][0])*(len(self.G.node[0]['state'][0]) - 1))
            total_possible_actions = num_nodes * yard_num_actions
            possible_actions = 2*num_edges
            impossible_actions = total_possible_actions - possible_actions

            print('node의 개수:', num_nodes)
            print('edge의 개수:', num_edges)
            print('전체 가능한 action의 수:', possible_actions)
            print('불가능한 action의 수:', impossible_actions)
            print('가능한 action의 비율:', possible_actions/total_possible_actions)
            print('node당 가능한 action의 평균:', 2*len(self.G.edges)/len(self.G.nodes))

            self.get_path_node_list(state_history)

            positions = [[nx.fruchterman_reingold_layout(self.G),'fruchterman_reingold_layout'],
                         [nx.spring_layout(self.G),'spring_layout'], [nx.kamada_kawai_layout(self.G),'kamada_kawai_layout'],
                         [nx.spectral_layout(self.G),'spectral_layout']]

            for position in positions:
                pos = position[0]
                name = str(position[1]) + str(difficulty)
                nx.draw_networkx_edges(self.G, pos, width=0.1, edge_color='#adadad')
                nx.draw_networkx_nodes(self.G, pos, nodelist=self.other_node_list, node_color='#adadad', node_size=0.5)
                nx.draw_networkx_edges(self.G, pos, edgelist=self.path_edge_list, width=0.2, edge_color='#000000')
                nx.draw_networkx_nodes(self.G, pos, nodelist=self.path_node_list, node_color='#000000', node_size=1)
                nx.draw_networkx_nodes(self.G, pos, nodelist=[self.initial_node], node_color='#0026ff', node_size=1.5)
                nx.draw_networkx_nodes(self.G, pos, nodelist=[self.target_node], node_color='#ff0000', node_size=1.5)

                # 특정 edge만 색과 두께를 조정할 수 있는지 확인하기

                plt.savefig(str(name) + '.jpg', dpi=1000)
                plt.close()


            print(f'path_node_list의 크기: {len(self.path_node_list)}')
            print(f'other_node_list의 크기: {len(self.other_node_list)}')


            print('종료 시간:', datetime.datetime.now())
        else:
            print()


    def get_path_node_list(self, state_history):
        '''
        for i in range(len(self.G.node)):
            path_node_found = False
            for j in range(len(state_history)):
                if np.array_equal(self.G.node[i]['state'], state_history[j]):
                    if np.array_equal(state_history[j], CFG.s0):
                        self.initial_node = i
                    else:
                        self.path_node_list.append(i)
                    path_node_found = True
                    del state_history[j]
                    break
            if not path_node_found:
                self.other_node_list.append(i)

        '''


        for i in range(len(state_history)):
            path_node_found = False
            other_node_num = -1
            for j in range(len(self.G.node)):
                if np.array_equal(self.G.node[j]['state'], state_history[i]):
                    if np.array_equal(state_history[i], CFG.s0):
                        self.initial_node = j
                    else:
                        self.path_node_list.append(j)
                    path_node_found = True
                    other_node_num = j
                    break
            if not path_node_found:
                self.other_node_list.append(other_node_num)


        for i in range(len(self.path_node_list)):
            self.path_edge_list.append((self.path_node_list[i], self.path_node_list[i+1]))
            if i+2 == len(self.path_node_list):
                break




    def expand(self, node_num):
        for j in range(len(self.G.node[node_num]['neighbor_states'])):

            same_exist = False

            # G 그래프의 모든 node의 state와 현재 node[node_num]['state']를 비교해 새로운 node의 생성 여부 결정
            for k in range(len(self.G.node)):
                tmp_num_nodes = len(self.G.node)
                # neighbor_state와 같은 state가 다른 node중에 있는지 모든 node를 대상으로 확인
                if self.G.node[node_num]['neighbor_states'][j] == self.G.node[tmp_num_nodes - k - 1]['state']:
                    # 같은 state를 가진 node가 있음
                    same_exist = True
                    # edge만 연결해줌
                    self.G.add_edge(node_num, tmp_num_nodes - k - 1)
                    break

            # 같은 state가 없다면 새로운 node와 state, 연결된 edge를 생성
            if same_exist == False:
                # node 생성
                self.G.add_node(len(self.G.node))
                # edge 생성
                # 위에서 node를 생성하는 순간 len(G.node)가 1이 늘어났으므로 아래에서 부터 -1을 붙혀줘야함
                self.G.add_edge(node_num, len(self.G.node) - 1)
                # 속성 입력
                self.G.node[len(self.G.node) - 1]['state'] = self.G.node[node_num]['neighbor_states'][j]
                self.G.node[len(self.G.node) - 1]['neighbor_states'] = container_env().get_neighbor_states(self.G.node[len(self.G.node) - 1]['state'])


'''
성공 episode의 state history를 가져와 state 비교를 통해 다른색 node로 표현 하는 부분 구현
'''








