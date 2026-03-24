import numpy as np
import pandas as pd
import os
from pathlib import Path
import subprocess
from datetime import datetime


def Run_IDF(file_name, file, epw_file, output_dir):
    EP_dir = r'C:\EnergyPlusV25-1-0'    
    obj = (f'"{EP_dir}\\EnergyPlus" '
            # + '--readvars '  # included to create a .csv file of the results
            + f'--output-directory "{output_dir}" '
            + f'--output-prefix "{file_name}" '
            + f'--weather "{epw_file}" '
            + f'"{file}"')
    
    result = subprocess.run(obj, capture_output=True)
    print('--------------------------------------------')
    print(file_name, '--> SUCCESS' if result.returncode==0 else 'FAIL')
    # print('Return code: ',result.returncode, '--> SUCCESS' if result.returncode==0 else 'FAIL')
    # print('---ARGS---\n',result.args)
    # print('---STDOUT---\n',result.stdout.decode())
    # print('---STDERR---\n',result.stderr.decode())
    return



def run_district(idf_dir, epw_file, output_dir):

    idf_list = []
    for x in os.listdir(idf_dir):
        if x.endswith('.idf'): idf_list.append(x)

    run_time = {}
    for file in idf_list:
            
        idf_path = idf_dir + file
        file_name, file_extension = os.path.splitext(file)
    
        # # check if the building is already simulated or not    
        # if file_name + 'out.csv' in os.listdir(idf_dir):
        #     continue
    
        # Run the IDF file
        sim_start = datetime.now()    
        Run_IDF(file_name, idf_path, epw_file, output_dir)
        sim_end = datetime.now()
        elapsed_time = sim_end - sim_start
        # run_time[file_name] = elapsed_time.seconds
        rt = np.round(elapsed_time.microseconds/1e6, 2)
        run_time[file_name] = rt
        print('Run Time:', rt, 'seconds')
    
    print('--------------------------')
    print('End of simulation')
    print('--------------------------')
    return


def parse_err(output_dir, err_file):

    file_name, file_extension = os.path.splitext(err_file)

    warnings, severes, fatals = [], [], []
    supressed_warnings = [
        'Requested number (1) is less than the suggested minimum of 4',
        'Feb29 data encountered but will not be processed']

    with open(os.path.join(output_dir, err_file), "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("   ** Warning **"):
                # suppression filter
                if not any(warn in line for warn in supressed_warnings):
                    warnings.append(line.strip())

            elif line.startswith("   ** Severe  **"):
                severes.append(line.strip())

            elif line.startswith("   ** Fatal  **"):
                fatals.append(line.strip())

    # write errors, warning and fatals in a file
    with open (output_dir + f"\Warnings\{file_name}_warning.txt", "w") as f:
        for w in warnings:
            if w in supressed_warnings:
                continue
            else:
                f.write(w)

    with open (output_dir + f"\Severs\{file_name}_severe.txt", "w") as f:
        for s in severes:
            f.write(s)

    with open (output_dir + f"\Fatals\{file_name}_fatal.txt", "w") as f:
        for ft in fatals:
            f.write(ft)

    return warnings, severes, fatals




# source path
path_src = Path(__file__).resolve().parent

# input path
path_input = path_src.parent

# IDF directory
idf_dir = path_src / "Generated_IDFs"

# Select weather data
epw_file = path_input / "Rheinstetten_04177.epw"

# Output dir
output_dir = os.path.join(path_src, 'Results\IdealHVAC')

# Run all buildings in the district
run_district(idf_dir, epw_file, output_dir)

# Folders to parse .err file
folders = ["Warnings", "Severs", "Fatals"]
for fld in folders:
    full_path = os.path.join(output_dir, fld)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

err_list = []
for x in os.listdir(output_dir):
    if x.endswith('.err'):
        err_list.append(x)
        parse_err(output_dir, x)







