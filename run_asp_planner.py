#!/usr/bin/python
import subprocess
import os
import sys

DIR_NAME_BASE = os.path.dirname(__file__)
DIR_NAME_ASP = os.path.abspath(DIR_NAME_BASE + "/floor_plan_vlm/asp_planner")
query_filename = DIR_NAME_ASP + "/query.asp"
SOLVER = "clingo "
OPTION_STEP = lambda x: "-c n={0} ".format(x)
OPTION_ANS = "-n 0 "
OPTION_FILES = DIR_NAME_ASP + "/*.asp " + DIR_NAME_ASP + "/cost.lua"

def parse_plans(output):
    lines = str(output).split("\\n")

    plans_list = []
    total_cost_list = []
    for i, line in enumerate(lines):
        if line.find("Answer") != -1:
            plans_list.append(lines[i + 1])
        if line.find("Optimization") != -1:
            tmp = line.split(" ")
            total_cost_list.append(int(tmp[-1]))

    #Remove duplicate costs ('Optimization' appears twice per plan set)
    total_cost_list = total_cost_list[:-1]
    parsed_plans = []

    #Extract "at" predicates, along with all actions
    for plan_list in plans_list:
        plan = plan_list.split()
        at_list = []
        action_list = []
        for p in plan:
            prefix = p[:p.find("(")]
            location_step_pair = p[p.find("(") + 1:p.find(")")]
            tmp = location_step_pair.split(",")
            if prefix == "at":
                at_list.append([prefix] + tmp)
            else:
                action_list.append([prefix] + tmp)

        #parsed_plans.append([at_list, action_list])
        parsed_plans.append(action_list)

    return parsed_plans, total_cost_list


def find_plan(init_state, goal_state):
    # Make file which plans paths.
    initial_at = "at(" + init_state + ", 0)."

    final_at = "\n:- not at(" + goal_state + ", n-1)."

    show_text = """    
                    \n#minimize { L,X,Y,I: path(X,Y,I), cost(X,Y,L)}. 
                    \n#show approach/2.
                    \n#show gothrough/2.
                    \n#show opendoor/2.
                    \n#show goto/2.
                """

    query2 = initial_at + final_at + show_text
    f = open(query_filename, "w")
    f.write(query2)
    f.close()

    # Parse the output from clingo
    output = "UNSATISFIABLE"
    i = 0
    while "UNSATISFIABLE" in str(output):
        if (i > 20):
            print("Cant find plan! Exiting...")
            sys.exit()
        i = i + 1
        p = subprocess.Popen(SOLVER + OPTION_STEP(i) + OPTION_ANS + OPTION_FILES,
                             stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
    
    minimal_step = i

    all_plans = []
    all_costs = []

    #We don't expect lowest cost plans to have more than 2 steps more than shortest plans
    for j in range(minimal_step, minimal_step + 2):
        p = subprocess.Popen(SOLVER + OPTION_STEP(j) + OPTION_ANS + OPTION_FILES,
                             stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        plans, costs = parse_plans(output)
        all_plans.extend(plans)
        all_costs.extend(costs)

    #Choose the minimum cost plan
    min_cost_plan = all_plans[(all_costs.index(min(all_costs)))]
    cost = min(all_costs)

    #Sort plan for sequentially ordered actions
    plan_dict = {}
    for action in min_cost_plan:
        plan_dict[int(action[2])] = action
    sorted_plan = [plan_dict[i] for i in range(len(min_cost_plan))]

    return sorted_plan, cost
