from main import generate_n_solve_problem

maintenance_data = {'mt1': {'skip_cost': 163, 'duration': 2},
 'mt2': {'skip_cost': 368, 'duration': 3},
 'mt3': {'skip_cost': 449, 'duration': 6},
 'mt4': {'skip_cost': 349, 'duration': 4},
 'mt5': {'skip_cost': 108, 'duration': 2},
 'mt6': {'skip_cost': 144, 'duration': 4}}

tasks = {'m1': 'mt1',
 'm2': 'mt6',
 'm3': 'mt6',
 'm4': 'mt1',
 'm5': 'mt5',
 'm6': 'mt1',
 'm7': 'mt5',
 'm8': 'mt5',
 'm9': 'mt2',
 'm10': 'mt6',
 'm11': 'mt1',
 'm12': 'mt2',
 'm13': 'mt3'}

technician_matrix = {
 't2': {'qualification': ['mt1', 'mt3', 'mt6', 'mt4', 'mt2', 'mt5'],
        'shift_start': 8,
        'shift_end': 15},
 't3': {'qualification': ['mt1', 'mt5', 'mt3'],
        'shift_start': 11,
        'shift_end': 19},
 't4': {'qualification': ['mt3', 'mt5', 'mt6', 'mt1', 'mt2'],
        'shift_start': 12,
        'shift_end': 19},
 't6': {'qualification': ['mt6'], 'shift_start': 9, 'shift_end': 17}}

# results
problem = generate_n_solve_problem(maintenance_data, tasks, technician_matrix)

# PDDL format
# print(problem)