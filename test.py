"""
test soring
"""
from copy import deepcopy
import numpy as np
from config import CFG
import datetime
import helper
from A_star_algorithm import A_star
from draw_container_state_graph import draw_graph

class sort:
    def __init__(self, net, env):
        self.net = net
        self.env = env
        self.s0 = np.array(CFG.s0, dtype=float)
        self.st = np.array(CFG.st, dtype=float)
        self.A_star = A_star(self.net, A_star_sim = CFG.num_A_star_sims, check_repeat_state=CFG.A_star_graph)


    def search(self, difficulty):
        self.env.state = deepcopy(self.s0)
        self.env.target_state = deepcopy(self.st)

        count_step = 0
        state_history = []
        state_history.append(deepcopy(self.env.state))

        start_time = datetime.datetime.now()

        while True:
            # get policy
            policy = self.get_policy()

            # execute policy
            self.exe_policy(policy)
            count_step += 1

            state_history.append(deepcopy(self.env.state))

            done, _ = self.env.check_target_state_reached()

            if done:
                print('sorting complete')
                print('step: ', count_step)
                if CFG.store_gif:  # make gif image
                    name = str(difficulty) + ' difficulty' + ' - ' + str(count_step) + 'steps'
                    helper.print_gif(name, CFG.max_tier, CFG.num_stack, state_history)
                break
            if count_step == CFG.maximum_moves-1:
                print('sorting failed')
                print(self.env.state)
                break

        if CFG.draw_graph:  # draw graph
            draw_graph().start(state_history, difficulty)

        end_time = datetime.datetime.now()
        print('sorting time:', end_time - start_time)
        print('-'*30)


    def exe_policy(self, policy):
        action_list = self.env.get_valid_moves()
        policy = np.array([policy])

        selected_act_num = np.random.choice(range(policy.shape[1]), p=policy.ravel())

        self.env.execute_action(action_list[selected_act_num])


    def get_policy(self):
        pi = self.A_star.search(self.env)
        calculated_pi = self.calculate_policy(pi)

        return calculated_pi


    def calculate_policy(self, policy):
        # apply temperature parameter
        for i in range(len(policy)):
            policy[i] = policy[i]**CFG.sorting_temp_value
        sum_policy = sum(policy)
        new_policy = []
        for i in range(len(policy)):
            new_policy.append(policy[i]/sum_policy)
        return new_policy
