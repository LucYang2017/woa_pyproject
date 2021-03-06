# -*- coding: utf-8 -*-

# @Time    : 2019/1/20 13:38
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : tarcking_methods.py


from configs import *
import random
import math
import basic_functions
import numpy as np
import field


def woa_3d(agents, leader):
    agents_no = len(agents)
    counter = len(leader.history)
    airflow_field = field.load_airflow_field()
    for agent in agents:
        v = field.query_v(positions=[agent.position], airflow_field=airflow_field)
        v = v[0]
        # v = np.array([0, 0, 0])
        c_gradient = np.array([0, 0, 0])
        # if counter > 0:
        #     c_gradient = agent.position - agent.history[-1][0]

        # a = 2 - counter * (2.0 / float(COUNTER_MAX))
        a = 1
        p = random.uniform(0, 1)

        C = np.array([random.uniform(0, 2) for i in range(len(leader.position))])
        A = random.uniform(-a, a)

        choice = 0
        if p < 0.5:
            if abs(A) < 1:
                choice = 0
                D = C * abs(leader.position - agent.position)
                new_position = leader.position - A * D + c_gradient - v
            elif abs(A) >= 1:
                choice = 1
                random_agent_no = random.randint(0, agents_no - 1)
                random_agent = agents[random_agent_no]
                D = C * abs(random_agent.position - agent.position)
                new_position = random_agent.position - A * D + c_gradient - v
        elif p >= 0.5:
            choice = 2
            D = abs(leader.position - agent.position)
            b = 1  # 用来定义螺旋大小的常数
            l = random.uniform(-1, 1)
            new_position = D * math.exp(b * l) * math.cos(2 * math.pi * l) + leader.position + c_gradient - v

        if np.linalg.norm(new_position - agent.position) > STEP_LEN_TRACKING:
            new_position = agent.position + STEP_LEN_TRACKING * (new_position - agent.position) / np.linalg.norm(
                new_position - agent.position)  # 限制步长
        # import print_colors
        # if choice == 0:
        #     print_colors.red('agent no. %d  a = %f  p = %f A = %s C = %s D = %s choice = %d' % (
        #         agents.index(agent), a, p, str(A), str(C), str(D), choice))
        # elif choice == 1:
        #     print_colors.green('agent no. %d  a = %f  p = %f A = %s C = %s D = %s choice = %d' % (
        #         agents.index(agent), a, p, str(A), str(C), str(D), choice))
        # elif choice == 2:
        #     print_colors.blue('agent no. %d  a = %f  p = %f A = %s C = %s D = %s choice = %d' % (
        #         agents.index(agent), a, p, str(A), str(C), str(D), choice))
        # print_colors.yellow('last_position %s ' % (str(agent.position)))
        # print_colors.yellow('new_position_before_check_boundary %s ' % (str(new_position)))
        new_position = basic_functions.check_boundary_3d_finding(new_position)
        # print_colors.yellow('new_position_after_check_boundary %s ' % (str(new_position)))
        agent.position = new_position
    return agents


def woa_2d(agents, leader, height):
    agents_no = len(agents)
    counter = len(leader.history)
    for agent in agents:

        c_gradient = np.array([0, 0, 0])
        # if counter > 0:
        #     c_gradient = agent.position - agent.history[-1][0]

        # a = 2 - counter * (2.0 / float(COUNTER_MAX))
        a = 1
        p = random.uniform(0, 1)

        C = np.array([random.uniform(0, 2) for i in range(len(leader.position))])
        A = random.uniform(-a, a)

        choice = 0
        if p < 0.5:
            if abs(A) < 1:
                choice = 0
                D = C * abs(leader.position - agent.position)
                new_position = leader.position - A * D + c_gradient
            elif abs(A) >= 1:
                choice = 1
                random_agent_no = random.randint(0, agents_no - 1)
                random_agent = agents[random_agent_no]
                D = C * abs(random_agent.position - agent.position)
                new_position = random_agent.position - A * D + c_gradient
        elif p >= 0.5:
            choice = 2
            D = abs(leader.position - agent.position)
            b = 1  # 用来定义螺旋大小的常数
            l = random.uniform(-1, 1)
            new_position = D * math.exp(b * l) * math.cos(2 * math.pi * l) + leader.position + c_gradient

        new_position[-1] = height
        if np.linalg.norm(new_position - agent.position) > STEP_LEN_TRACKING:
            new_position = agent.position + STEP_LEN_TRACKING * (new_position - agent.position) / np.linalg.norm(
                new_position - agent.position)  # 限制步长
        # import print_colors
        # if choice == 0:
        #     print_colors.red('agent no. %d  a = %f  p = %f A = %s C = %s D = %s choice = %d' % (
        #         agents.index(agent), a, p, str(A), str(C), str(D), choice))
        # elif choice == 1:
        #     print_colors.green('agent no. %d  a = %f  p = %f A = %s C = %s D = %s choice = %d' % (
        #         agents.index(agent), a, p, str(A), str(C), str(D), choice))
        # elif choice == 2:
        #     print_colors.blue('agent no. %d  a = %f  p = %f A = %s C = %s D = %s choice = %d' % (
        #         agents.index(agent), a, p, str(A), str(C), str(D), choice))
        # print_colors.yellow('last_position %s ' % (str(agent.position)))
        # print_colors.yellow('new_position_before_check_boundary %s ' % (str(new_position)))
        new_position = basic_functions.check_boundary_3d_tracking(new_position)
        # print_colors.yellow('new_position_after_check_boundary %s ' % (str(new_position)))
        agent.position = new_position
    return agents


def pso_3d(agents, leader):
    airflow_field = field.load_airflow_field()

    def get_local_maximum_position(agent):
        max_c = float('-inf')
        max_index = -1

        for i in range(len(agent.history)):
            c = agent.history[i][1]
            if c > max_c:
                max_index = i

        return agent.history[max_index][0]

    for agent in agents:
        local_maximum_position = get_local_maximum_position(agent)
        global_maximum_position = leader.position

        local_m_p_direction = local_maximum_position - agent.position
        global_m_p_direction = global_maximum_position - agent.position
        last_direction = agent.history[-1][0] - agent.history[-2][0]

        # local_m_p_direction = local_m_p_direction / np.linalg.norm(local_m_p_direction)
        # global_m_p_direction = global_m_p_direction / np.linalg.norm(global_m_p_direction)
        # last_direction = last_direction / np.linalg.norm(last_direction)

        v = field.query_v(positions=[agent.position], airflow_field=airflow_field)
        v = v[0]
        v = np.array([0, 0, 0])

        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        r3 = random.uniform(0, 1)

        direction = last_direction + 2 * r1 * local_maximum_position + 2 * r2 * global_maximum_position + 2 * r3 * v
        direction = direction / np.linalg.norm(direction)

        new_position = direction * STEP_LEN_TRACKING + agent.position

        new_position = basic_functions.check_boundary_3d_finding(new_position)
        agent.position = new_position
    return agents
