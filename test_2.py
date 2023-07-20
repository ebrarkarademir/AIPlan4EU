from main import generate_n_solve_problem

maintenance_data =  {'mt1': {'skip_cost': 118, 'duration': 4},
                    'mt2': {'skip_cost': 388, 'duration': 5},
                    'mt3': {'skip_cost': 436, 'duration': 6},
                    'mt4': {'skip_cost': 395, 'duration': 2},
                    'mt5': {'skip_cost': 332, 'duration': 5},
                    'mt6': {'skip_cost': 375, 'duration': 2},
                    'mt7': {'skip_cost': 291, 'duration': 2}}

tasks = {'m1': 'mt6',
        'm2': 'mt3',
        'm3': 'mt3',
        'm4': 'mt4',
        'm5': 'mt6',
        'm6': 'mt5',
        'm7': 'mt1',
        'm8': 'mt7',
        'm9': 'mt6',
        'm10': 'mt2'}

technician_matrix = {'t1': {'qualification': ['mt5', 'mt1'], 'shift_start': 10, 'shift_end': 23},
                    't2': {'qualification': ['mt7', 'mt2', 'mt4', 'mt1', 'mt6'],
                    'shift_start': 12,
                    'shift_end': 18},
                    't3': {'qualification': ['mt4', 'mt7', 'mt2', 'mt5', 'mt3', 'mt1', 'mt6'],
                    'shift_start': 9,
                    'shift_end': 16},
                    't4': {'qualification': ['mt7'], 'shift_start': 12, 'shift_end': 18}}


# results
problem = generate_n_solve_problem(maintenance_data, tasks, technician_matrix)

# PDDL format
# print(problem)