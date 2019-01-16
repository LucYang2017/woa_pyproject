# -*- coding: utf-8 -*-

# @Time    : 2019/1/13 9:03
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : agent_dict.py


import random
from configs import *
import numpy as np
import field

Agent = {
    'step_no': 0,
    'position': np.array([0, 0, 0]),
    'concentration': 0
}


def init_agents_random(agents_no, c_field):
    agents = []
    leader = []
    for i in range(agents_no):
        agents.append([])
    for agent in agents:
        agent.append(Agent)
        agent[-1]['step_no'] = len(agent)
        agent[-1]['position'] = np.array(
            [round(random.uniform(X_MIN, X_MAX), 2), round(random.uniform(Y_MIN, Y_MAX), 2),
             round(random.uniform(Z_MIN, Z_MAX), 2)])
    return agents, leader


def get_agents_positions(agents):
    positions = []
    for agent in agents:
        positions.append(agent[-1]['step_no'])
    return np.array(positions)


a, b = init_agents_random(10, 123)
for i in a:
    print(i)
print(b)
