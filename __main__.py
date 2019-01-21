# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 20:37
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : __main__.py

import field
import agent
import basic_functions as bf
import robotic_active_olfaction as rao
from configs import *
import time
import numpy as np


def source_localization(agents_no, finding_threshold, tracing_threshold, start_position=[0, 0, 0]):
    SUCCESS = False
    state = 0
    t = 1
    c_field = field.load_field(t)
    finding_end = COUNTER_MAX
    serial_no = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    # agents, leader = agent.init_agents_fixed(agents_no, c_field, start_position)
    agents, leader = agent.init_agents_random(agents_no, c_field)

    while len(leader.history) < COUNTER_MAX and (not SUCCESS):
        if state == 0:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_finding(agents, leader, c_field)
                # bf.show_info(agents, leader, t, state)
                if leader.concentration > finding_threshold:
                    state = 1
                    break
            finding_end = len(leader.history)
        elif state == 1:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_tracking(agents, leader, c_field)
                if leader.concentration > tracing_threshold:
                    SUCCESS = True
                    break
                if agent.get_leader_age(leader) > 5:
                    local_maximum = leader.concentration
                    state = 2
                    break
        elif state == 2:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_finding(agents, leader, c_field)
                if leader.concentration > local_maximum + 0.05:
                    state = 1
                    break
                # bf.show_info(agents, leader, t, state)
    tracing_end = len(leader.history)

    if np.linalg.norm(leader.history[-1][0] - np.array([0, -0.3, 1.3])) < 0.6:
        SUCCESS = True
    else:
        SUCCESS = False

    bf.save_trajectory(agents, leader, serial_no)
    bf.save_results(agents, leader, serial_no, finding_end)

    return finding_end, tracing_end, SUCCESS


def source_localization_2d(agents_no, finding_threshold, tracing_threshold, height):
    SUCCESS = False
    state = 0
    t = 1
    c_field = field.load_field(t)
    finding_end = COUNTER_MAX
    serial_no = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    agents, leader = agent.init_agents_fixed(agents_no, c_field, [-2, -2, height])
    # agents, leader = init_agents_random(agents_no, c_field)

    while len(leader.history) < COUNTER_MAX and (not SUCCESS):
        if state == 0:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_finding_2d(agents, leader, c_field, height)

                # bf.show_info(agents, leader, t, state)
                if leader.concentration > finding_threshold:
                    state = 1
                    break
            finding_end = len(leader.history)
        elif state == 1:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_tracking_2d(agents, leader, c_field, height)

                bf.show_info(agents, leader, t, state)
                if leader.concentration > tracing_threshold:
                    SUCCESS = True
                    break
                if agent.get_leader_age(leader) > 5:
                    local_maximum = leader.concentration
                    state = 2
                    break
        elif state == 2:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_finding_2d(agents, leader, c_field, height)

                bf.show_info(agents, leader, t, state)
                if leader.concentration > tracing_threshold:
                    SUCCESS = True
                    break
                if leader.concentration > local_maximum + (tracing_threshold * 0.1):
                    state = 1
                    break
    tracing_end = len(leader.history)

    if np.linalg.norm(leader.history[-1][0] - np.array([0, -0.3, height])) < 0.3:
        SUCCESS = True
    else:
        SUCCESS = False

    bf.save_trajectory(agents, leader, serial_no)
    bf.save_results(agents, leader, serial_no, finding_end)

    return finding_end, tracing_end, SUCCESS


def source_localization_pso(agents_no, finding_threshold, tracing_threshold, start_position=[0, 0, 0]):
    SUCCESS = False
    state = 0
    t = 1
    c_field = field.load_field(t)
    finding_end = COUNTER_MAX
    serial_no = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    # agents, leader = agent.init_agents_fixed(agents_no, c_field, start_position)
    agents, leader = agent.init_agents_random(agents_no, c_field)

    while len(leader.history) < COUNTER_MAX and (not SUCCESS):
        if state == 0:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_finding(agents, leader, c_field)
                # bf.show_info(agents, leader, t, state)
                if leader.concentration > finding_threshold:
                    state = 1
                    break
            finding_end = len(leader.history)
        elif state == 1:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_tracking_pso(agents, leader, c_field)
                if leader.concentration > tracing_threshold:
                    SUCCESS = True
                    break
                if agent.get_leader_age(leader) > 5:
                    local_maximum = leader.concentration
                    state = 2
                    break
        elif state == 2:
            while len(leader.history) < COUNTER_MAX:
                t = len(leader.history) * 2
                if t >= 200:
                    t = 200
                c_field = field.load_field(t)
                agents, leader = rao.plume_finding(agents, leader, c_field)
                if leader.concentration > local_maximum + 0.05:
                    state = 1
                    break
                # bf.show_info(agents, leader, t, state)
    tracing_end = len(leader.history)

    if np.linalg.norm(leader.history[-1][0] - np.array([0, -0.3, 1.3])) < 0.6:
        SUCCESS = True
    else:
        SUCCESS = False

    bf.save_trajectory(agents, leader, serial_no)
    bf.save_results(agents, leader, serial_no, finding_end)

    return finding_end, tracing_end, SUCCESS


if __name__ == "__main__":

    success = 0
    step_consuming = []
    start_p = [2, -2, 0.5]
    for i in range(100):
        finding_end, tracing_end, success_flag = source_localization_pso(agents_no=5,
                                                                         finding_threshold=10,
                                                                         tracing_threshold=1000,
                                                                         start_position=start_p)
        # finding_end, tracing_end, success_flag = source_localization_2d(agents_no=6,
        #                                                                 finding_threshold=10,
        #                                                                 tracing_threshold=5000,
        #                                                                 height=1.3)
        if success_flag:
            success += 1
        step_consuming.append(tracing_end)
        print('Trial no. %d' % (i))
    print("The start position is %s" % (str(start_p)))
    print("The success rate is %d%%" % (success))
    print("The average step is %d" % (sum(step_consuming) / len(step_consuming)))
