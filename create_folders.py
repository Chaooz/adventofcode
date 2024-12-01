import os

# Base directory where folders will be created
base_dir = '/home/simon/src/adventofcode/2024'

for day in range(1, 26):
    day_folder = os.path.join(base_dir, f'{day:02d}')
    os.makedirs(day_folder, exist_ok=True)

    thor_folder = os.path.join(day_folder, 'Thor')
    simon_folder = os.path.join(day_folder, 'Simon')

    os.makedirs(thor_folder, exist_ok=True)
    os.makedirs(simon_folder, exist_ok=True)
    