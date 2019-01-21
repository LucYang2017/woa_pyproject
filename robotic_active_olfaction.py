# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 20:26
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : robotic_active_olfaction.py


import basic_functions as bf
import woa
import agent
import tarcking_methods


def plume_finding(agents, leader, c_field):
    agents = bf.go_forward(agents)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    leader_age = agent.get_leader_age(leader)
    # print('leader_age = %d' % (leader_age))
    return agents, leader


def plume_finding_2d(agents, leader, c_field, height):
    agents = bf.go_forward_2d(agents, height)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    leader_age = agent.get_leader_age(leader)
    # print('leader_age = %d' % (leader_age))
    return agents, leader


def plume_tracking(agents, leader, c_field):
    agents = woa.woa_3d(agents, leader)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    leader_age = agent.get_leader_age(leader)
    # print('leader_age = %d' % (leader_age))
    return agents, leader


def plume_tracking_2d(agents, leader, c_field, height):
    agents = woa.woa_2d(agents, leader, height)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    leader_age = agent.get_leader_age(leader)
    # print('leader_age = %d' % (leader_age))
    return agents, leader


def plume_tracking_pso(agents, leader, c_field):
    agents = tarcking_methods.pso_3d(agents, leader)
    agents = agent.update_agents_c(agents, c_field)
    agents = agent.update_agents_history(agents)
    leader = agent.update_leader(agents, leader)
    leader_age = agent.get_leader_age(leader)
    # print('leader_age = %d' % (leader_age))
    return agents, leader
