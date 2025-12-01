import os

# Base directory where folders will be created
base_dir = './2025/'
num_days = 12

for day in range(1, num_days + 1):
    day_folder = os.path.join(base_dir, f'{day:02d}')
    os.makedirs(day_folder, exist_ok=True)

    thor_folder = os.path.join(day_folder, 'Thor')
    simon_folder = os.path.join(day_folder, 'Simon')
    os.makedirs(thor_folder, exist_ok=True)
    os.makedirs(simon_folder, exist_ok=True)

    # Only create files in Thor and Simon folders if they are empty
    for folder in [thor_folder, simon_folder]:
        # Check if the folder is empty
        if not os.listdir(folder):
            # Folder is empty, so create the files
            for filename in ['input.txt', 'unittest1.txt', 'solution.py']:
                file_path = os.path.join(folder, filename)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        pass  # Create an empty file
        else:
            print(f"Skipping {folder} because it already contains files.")

    