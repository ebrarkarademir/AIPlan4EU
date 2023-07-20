import random
from main import generate_n_solve_problem
def generate_random_input(num_machines, num_tasks, num_technicians, num_maintenance_types):
    maintenance_data = {}
    tasks = {}
    technician_matrix = {}

    # Generate random maintenance_data
    for i in range(num_maintenance_types):
        maintenance_type = f"mt{i+1}"
        skip_cost = random.randint(100, 500)
        duration = random.randint(2, 6)
        maintenance_data[maintenance_type] = {"skip_cost": skip_cost, "duration": duration}

    # Generate random tasks
    maintenance_types = list(maintenance_data.keys())
    for i in range(num_tasks):
        task = f"m{i+1}"
        maintenance_type = random.choice(maintenance_types)
        tasks[task] = maintenance_type

    # Generate random technician_matrix
    for i in range(num_technicians):
        technician = f"t{i+1}"
        num_qualifications = random.randint(1, num_maintenance_types)
        qualifications = random.sample(maintenance_types, num_qualifications)
        shift_start = random.randint(8, 12)
        shift_end = random.randint(shift_start + 5, 24)
        technician_matrix[technician] = {"qualification": qualifications, "shift_start": shift_start, "shift_end": shift_end}

    return maintenance_data, tasks, technician_matrix

# num_machines = 8
# num_tasks = 12
# num_technicians = 6
# num_maintenance_types = 6

# maintenance_data, tasks, technician_matrix = generate_random_input(num_machines, num_tasks, num_technicians, num_maintenance_types)

# problem = generate_n_solve_problem(maintenance_data, tasks, technician_matrix)