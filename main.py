from unified_planning.shortcuts import *
from unified_planning.io.pddl_writer import SequentialPlan


def convert_state_string_to_dict(state_string):
    state_dict = {}

    # Remove the curly braces and whitespace characters from the state string
    state_string = state_string.strip("{} ")

    # Split the state string into key-value pairs
    state_pairs = state_string.split(", ")

    # Extract the key-value pairs and store them in the state_dict
    for pair in state_pairs:
        key, value = pair.split(": ")

        # Convert boolean values
        if value == "true":
            state_dict[key] = True
        elif value == "false":
            state_dict[key] = False
        else:
            state_dict[key] = eval(value)

    return state_dict

def generate_n_solve_problem(maintenance_data, tasks, technician_matrix):
    fluent_dict = {}  # Dictionary to store dynamically generated fluents
    action_dict = {}  # Dictionary to store dynamically generated actions
    initial_value_dict = {}  # Dictionary to store dynamically generated initial values

    # Generate fluents for each task and their durations
    for task, maintenance_type in tasks.items():
        fluent = Fluent(f"{task}_{maintenance_type}") # boolean variable represents task
        duration_fluent = Fluent(f"{task}_{maintenance_type}_duration", IntType()) # integer variable for duration of the task

        fluent_dict[f"{task}_{maintenance_type}"] = fluent
        fluent_dict[f"{task}_{maintenance_type}_duration"] = duration_fluent

        initial_value_dict[fluent] = False
        initial_value_dict[duration_fluent] = maintenance_data[maintenance_type]["duration"] # get initial value from maintenance_data

    # Generate fluents for technician time left
    technician_time_left = {}
    for technician, qualifications in technician_matrix.items():
        technician_time_left[technician] = Fluent(f"{technician}_time_left", IntType())
        fluent_dict[technician_time_left[technician]] = technician_time_left[technician]
        initial_value_dict[technician_time_left[technician]] = qualifications["shift_end"] - qualifications["shift_start"]

    # Generate actions for assignments
    assign_counter = Fluent("assign_counter", IntType())
    fluent_dict[assign_counter] = assign_counter
    initial_value_dict[assign_counter] = 0

    # create actions with considering technician qualifications
    # ex : do not create t1_m1_mt5 if t1 is not able to perform maintenance type 5
    for technician, qualifications in technician_matrix.items():
        for task, maintenance_type in tasks.items():
            if maintenance_type in qualifications["qualification"]:
                action_name = f"{technician}_{task}_{maintenance_type}"
                action = InstantaneousAction(action_name)
                action.add_precondition(Not(fluent_dict[f"{task}_{maintenance_type}"])) # ex : action of t1_m1_mt1 has precondition as task m1_mt1 == False (no assignment)
                action.add_precondition(
                    GE(technician_time_left[technician], fluent_dict[f"{task}_{maintenance_type}_duration"]) # duration of the action < technician time left
                )
                action.add_effect(fluent_dict[f"{task}_{maintenance_type}"], True) # ex : after initiation action t1_m1_mt1 the task m1_mt1 == True (assignment made)
                action.add_effect(
                    technician_time_left[technician],
                    technician_time_left[technician] - fluent_dict[f"{task}_{maintenance_type}_duration"], # update technician time left
                )
                action.add_increase_effect(assign_counter, 1) # increment assign counter because assignment has been made

                action_dict[action_name] = action

    # Create the problem and add the dynamically generated components
    problem = Problem("minimize_skipped_maintenance_cost")

    # targeted number of tasks to be assigned fluent variable
    target_n_task_assigned = Fluent("target_n_task_assigned", IntType())
    problem.add_fluent(target_n_task_assigned)
    problem.set_initial_value(target_n_task_assigned, len(tasks)) # initially == total task amount

    # add all fluents and give the initial values
    for fluent in fluent_dict.values():
        problem.add_fluent(fluent)

    for action in action_dict.values():
        problem.add_action(action)

    for fluent, initial_value in initial_value_dict.items():
        problem.set_initial_value(fluent, initial_value)

    # calculate the action cost for each action created
    # ex : the action cost of t1_m1_mt1 will be the summation of skip costs of remaining tasks
    def calculate_action_cost(action_name, tasks):
        # Split the action name into technician, machine, and maintenance type
        technician, machine, maintenance_type = action_name.split("_")

        # Create a copy of the tasks dictionary
        task_costs = tasks.copy()

        # Remove the machine associated with the action from the task_costs dictionary
        del task_costs[machine]

        # Sum the remaining skip costs
        total_cost = sum([cost[1] for cost in task_costs.values()])

        return total_cost

    # create new tasks dict for action cost calculation
    # ex : {"m1" : "mt1" , 500}
    # 500 is obtained from maintenance_data
    def create_tasks_data(maintenance_data, tasks):
        tasks_data = {}

        for task, maintenance_type in tasks.items():
            skip_cost = maintenance_data[maintenance_type]["skip_cost"]
            tasks_data[task] = [maintenance_type, skip_cost]

        return tasks_data

    task_cost = create_tasks_data(maintenance_data, tasks)

    # create action_costs dictionary to pass it into quality metric
    action_costs = {}
    for action_name, action in action_dict.items():
        action_cost = calculate_action_cost(action_name, task_cost)
        action_costs[action] = action_cost

    problem.add_quality_metric(
        up.model.metrics.MinimizeActionCosts(action_costs)
    )

    goal_condition = GE(assign_counter, target_n_task_assigned) # number of assignments =< targeted number of tasks to be closed
    problem.add_goal(goal_condition)

    # solve the problem
    with OneshotPlanner(name = 'enhsp-opt') as planner:
        final_report = planner.solve(problem)
        plan = final_report.plan

    print(plan)
    i = len(tasks) # target_n_task_assigned counter

    # if plan = None, iteratively decrease the targeted number of tasks to be assigned and use replanner
    while plan is None:
        print(f"No plan found for goal of assigning {i} tasks")
        with Replanner(problem=problem, name='replanner[enhsp]') as replanner:
            try:
                i -= 1
                replanner.update_initial_value(target_n_task_assigned, i)
                new_plan = replanner.resolve().plan.actions
                plan = SequentialPlan(new_plan)

                # Simulation of the SequentialPlan found after Replanner
                with SequentialSimulator(problem) as simulator:
                    state = simulator.get_initial_state()
                    # print the applied action
                    final_state = simulator.apply(state, plan.actions[0])
                    print("\n")
                    for ai in plan.actions:
                        state = simulator.apply(state, ai)
                        print(f"Applied action: {ai}. ")
                        # print("Current state" , state)


                    final_state = convert_state_string_to_dict(str(state)) # final state dictionary


                    # Extract assigned tasks
                    assigned_tasks = [task for task, value in final_state.items() if value is True]
                    print("\nAssigned Tasks:")
                    for task in assigned_tasks:
                        print(task)

                    # Get remaining tasks
                    remaining_tasks = [task for task, value in final_state.items() if value is False and "_duration" not in task]
                    print("\nRemaining Tasks:")
                    for task in remaining_tasks:
                        print(task)

                    # Calculate the total cost for remaining tasks
                    total_cost = 0
                    for task in remaining_tasks:
                        maintenance_type = task.split("_")[1]
                        skip_cost = maintenance_data[maintenance_type]["skip_cost"]
                        total_cost += skip_cost

                    print("\nTotal Cost Occured:", total_cost)


                    # Get time left for each technician
                    technician_times = {
                        technician.split("_")[0]: value for technician, value in final_state.items() if technician.endswith("_time_left")
                    }
                    print("\nTechnician Time Left:")
                    for technician, time_left in technician_times.items():
                        print(f"{technician}: {time_left}")
            except Exception as e:
                pass

    return problem