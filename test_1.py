from main import generate_n_solve_problem

maintenance_data = {
    "mt1": {"skip_cost": 100, "duration": 8},
    "mt2": {"skip_cost": 150, "duration": 4},
    "mt3": {"skip_cost": 300, "duration": 4},

}

tasks = {
    "m1": "mt1",
    "m2": "mt1",
    "m3": "mt2",
    "m4": "mt3", # task 4
    "m5": "mt3"
}

technician_matrix = {
    "t1": {"qualification": ["mt1", "mt2"], "shift_start": 8, "shift_end": 16},
    "t2": {"qualification": ["mt2", "mt3"], "shift_start": 8, "shift_end": 16},
    "t3": {"qualification": ["mt1", "mt3"], "shift_start": 8, "shift_end": 16}
}

problem = generate_n_solve_problem(maintenance_data, tasks, technician_matrix)

# PDDL format
# print(problem)