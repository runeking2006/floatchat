import os

# Base directory containing 9 folders
base_path = r"D:\sih 25\2025"

# Expected number of files per folder (adjust if known differently)
# If unknown, we can just report the count per folder
expected_files = None  # set to int if you know expected count

print("Checking .nc files in all folders...\n")

for folder in sorted(os.listdir(base_path)):
    folder_path = os.path.join(base_path, folder)
    if os.path.isdir(folder_path):
        nc_files = [f for f in os.listdir(folder_path) if f.endswith(".nc")]
        print(f"{folder}: {len(nc_files)} .nc files found")
        if expected_files and len(nc_files) != expected_files:
            print(f"  ⚠️ Warning: Expected {expected_files} files, found {len(nc_files)}")
        # Optional: list missing or unusual filenames
        for f in nc_files:
            if not f.endswith("_prof.nc"):
                print(f"  ⚠️ Unusual file: {f}")
