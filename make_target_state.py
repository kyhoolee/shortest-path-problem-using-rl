"""
makes target state
"""
import numpy as np
from copy import deepcopy

class gen_tar_state:
    def __init__(self, num_stack, max_stack, num_of_containers):
        self.num_stack = num_stack
        self.max_stack = max_stack
        self.num_of_containers = num_of_containers
        self.containers = []

    def make_tar_state(self):
        while True:
            self.height_of_stacks = []
            for _ in range(self.num_stack):
                self.height_of_stacks.append(0)
            num_of_containers = deepcopy(self.num_of_containers)
            for i in range(self.num_stack):
                if num_of_containers != 0:
                    if i == self.num_stack-1:
                        self.height_of_stacks[i] = num_of_containers
                    else:
                        while True:
                            height = int(np.random.randn()+int(self.num_of_containers/self.num_stack)+1)
                            if height >= 0 and height <= self.max_stack:
                                break
                        self.height_of_stacks[i] = height
                        num_of_containers = num_of_containers - height
                else:
                    break

            proper_nums = True

            for i in range(self.num_stack):
                if self.height_of_stacks[i] < 0 or self.height_of_stacks[i] > self.max_stack:
                    proper_nums = False
                    break
            if proper_nums:
                break

        tmp_stack = np.zeros([self.num_stack, self.max_stack])
        for i in range(self.num_stack):
            for j in range(self.height_of_stacks[i]):
                left_containers = len(self.containers)
                container_idx = np.random.randint(0, left_containers)
                tmp_stack[i,j] = self.containers[container_idx]
                del self.containers[container_idx]

        tar_state = np.rot90(tmp_stack, k=1)

        return tar_state

