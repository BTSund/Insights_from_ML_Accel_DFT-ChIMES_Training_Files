import numpy as np  # type: ignore
import glob
import re

import numpy as np

def process_files_from_list(trajlist_path: str):
    result_table = []

    with open(trajlist_path, 'r') as trajlist:
        lines = trajlist.readlines()

    # Skip the first line (it's the number of files)
    for line in lines[1:]:
        filepath = line.strip().split()[-1]  # support cases with number + path or just path
        averages = []
        file_data = []
        First = True

        try:
            with open(filepath, 'r') as file:
                # print(file)
                for line in file:
                    parts = line.split()
                    # Start of new block
                    if len(parts) == 1:
                        Natoms = int(parts[0])
                        if not First and file_data:
                            averages.append(np.mean(np.abs(np.concatenate(file_data))))
                        file_data = []
                        First = False
                        n = 0
                        continue

                    if n == 0:
                        n += 1
                        continue

                    if n <= Natoms:
                        cols = parts
                        file_data.append([float(cols[4]), float(cols[5]), float(cols[6])])
                        n += 1

                # Final block
                if file_data:
                    averages.append(np.mean(np.abs(np.concatenate(file_data))))

            result_table+=averages

        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            result_table.append([])
    # print(result_table.shape)
    return result_table

# Usage
result = process_files_from_list("trajlist.dat")
# print(result)


def print_grouped_cases(result_row, median, group_sizes):
    """
    result_row: e.g. result[0]
    median: the global median
    group_sizes: list of ints, how many frames in each case
    """
    start = 0
    for i, size in enumerate(group_sizes):
        end = start + size
        group_avg = np.mean(result_row[start:end])
        print(f"case-{i}: {median / group_avg:.6f}")
        start = end


# === USAGE ===

# 1) process all your files into a big table
# result = process_files("all.OUTCAR.xyzf")

# 2) pick off the first row and its median
first_row = np.array(result)
median = np.median(first_row)

print(median)

# 3) define your grouping:
group_sizes = ([25, 25, 25, 25, 24])+[18]*2+ ([5]*35+[4]) +([5]*20+[3]+[3])+[1]+[14]+([1]*36)+[5]+[2]
stresses = np.array(43*[200]+60*[500]+[500]+[500])*2
print(len(group_sizes))
energies = np.array(([3,3,3,.1,.1,1,1]) + ([5]*36) + ([25]*22) + ([5]*38)+[5]+[5])
print(sum(group_sizes))
# 4) print each case as median divided by the **average** of its group
print_grouped_cases(first_row, median, group_sizes)
print(len(energies))




frame = 0
energies_count = 0
group_forces = []
group_energies = []
group_stresses = []

start = 0
for i, size in enumerate(group_sizes):
    end = start + size
    group_forces.append(np.min([5,(median/np.mean(first_row[start:end]))]))
    group_energies.append(energies[i])
    group_stresses.append(stresses[i])
    start = end

# 2) expand back out so each frame “knows” its group’s value
Force_grouped  = np.repeat(group_forces, group_sizes)
Energy_grouped = np.repeat(group_energies, group_sizes)
Stress_grouped = np.repeat(group_stresses, group_sizes)

# ─── now write the file using the grouped arrays ───
frame = 0
energies_count = 0

with open('b-labeled.txt', 'r') as infile, open('weights.txt', 'w') as outfile:
    for line in infile:
        if frame >= len(Force_grouped):
            break

        label, _ = line.strip().split()[:2]

        # treat any 's_*' as 's_'
        if label.startswith('s_'):
            label = 's_'

        if label == 'Si':
            outfile.write(f"{Force_grouped[frame]:.6f}\n")

        elif label == '+1':
            outfile.write(f"{Energy_grouped[frame]:.6f}\n")
            energies_count += 1
            if energies_count == 3:
                frame += 1
                energies_count = 0

        elif label == 's_':
            outfile.write(f"{Stress_grouped[frame]:.6f}\n")

        else:
            print(f"Unrecognized label: {label}")

            