"""
environment
"""
from copy import deepcopy
from config import CFG
import numpy as np


class Container_stockyard:
    def __init__(self, num_stack = CFG.num_stack, max_tier = CFG.max_tier, containers = CFG.containers):
        self.columns = num_stack
        self.rows = max_tier
        self.action_size = self.columns*(self.columns-1)
        self.make_action_list()
        self.state = []
        self.containers = containers
        self.target_state = []


    def make_action_list(self):
        # make action list
        self.action_list = []
        for i in range(self.columns):
            for j in range(self.columns):
                if i != j:
                    self.action_list.append([1, i, j])


    def execute_action(self, in_action):
        # move container from stack to stack
        action = [-1, -1]
        action[0] = in_action[1]
        action[1] = in_action[2]

        target_container = 0
        out_zone_tier = -1
        in_zone_tier = -1

        for i in range(self.rows):
            if self.state[i, action[0]] != 0:
                out_zone_tier = i
                break

        for i in range(1, self.rows + 1):
            if self.state[-i, action[1]] == 0:
                in_zone_tier = self.rows - i
                break

        if in_zone_tier == -1 or out_zone_tier == -1:
            pass
        else:
            for i in range(self.rows):
                if self.state[i, action[0]] != 0:
                    target_container = self.state[i, action[0]]
                    self.state[i, action[0]] = 0
                    break

            for i in range(1, self.rows+1):
                if self.state[-i, action[1]] == 0:
                    in_zone_tier = self.rows - i
                    self.state[-i, action[1]] = target_container
                    break


    def get_valid_moves(self):
        # get possible action and impossible action
        valid_moves = deepcopy(self.action_list)
        stack_size = []
        for i in range(self.columns):
            tmp_stack_size = 0
            for j in range(self.rows):
                if self.state[j, i] != 0:
                    tmp_stack_size += 1
            stack_size.append(tmp_stack_size)

        for i in range(len(stack_size)):
            for j in range(len(valid_moves)):
                if stack_size[i] == 0 and valid_moves[j][1] == i:
                    valid_moves[j][0] = 0
                if stack_size[i] == self.rows and valid_moves[j][2] == i:
                    valid_moves[j][0] = 0

        return valid_moves


    def check_target_state_reached(self):
        '''
        check if self.state and self.target_state is same state
        if its terminal state than return True and reward(1)
        '''
        target_reached = np.array_equal(self.state, self.target_state)

        if target_reached:
            return True, 1
        else:
            return False, 0












