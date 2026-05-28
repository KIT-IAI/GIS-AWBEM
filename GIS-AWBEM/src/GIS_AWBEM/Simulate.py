import numpy as np
import pandas as pd
import os, shutil
import subprocess
from datetime import datetime

def Run_IDF(file_name, file, epw_file, output_dir):
    """
    Run the EnergyPlus IDF and save the results in the output directory.
    """
    EP_dir = r'C:\EnergyPlusV25-1-0'    
    obj = (f'"{EP_dir}\\EnergyPlus" '
            # + '--readvars '  # included to create a .csv file of the results
            + f'--output-directory "{output_dir}" '
            + f'--output-prefix "{file_name}_" '
            + f'--weather "{epw_file}" '
            + f'"{file}"')
    
    result = subprocess.run(obj, capture_output=True)

    # print(file_name, '--> SUCCESS' if result.returncode==0 else 'FAIL')
    # print('Return code: ',result.returncode, '--> SUCCESS' if result.returncode==0 else 'FAIL')
    # print('---ARGS---\n',result.args)
    # print('---STDOUT---\n',result.stdout.decode())
    # print('---STDERR---\n',result.stderr.decode())
    return result.returncode


def parse_err(output_dir, err_file):
    """
    Parse the .err file to extract warnings and severe errors, and save them in separate text files."""

    file_name, file_extension = os.path.splitext(err_file)

    warnings, severes = [], []
    supressed_warnings = [
        "Requested number (1) is less than the suggested minimum of 4",
        "Feb29 data encountered but will not be processed"]

    with open(os.path.join(output_dir, err_file), "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("   ** Warning **"):
                # suppression filter
                if not any(warn in line for warn in supressed_warnings):
                    warnings.append(line.strip())

            elif line.startswith("   ** Severe  **"):
                severes.append(line.strip())

    # write warnings and severes to txt files
    if len(warnings) > 0:
        with open (output_dir + f"\Warnings\{file_name}_warning.txt", "w") as f:
            f.write("\n".join(warnings))

    if len(severes) > 0:
        with open (output_dir + f"\Severs\{file_name}_severe.txt", "w") as f:
            f.write("\n".join(severes))

    return warnings, severes


def simulate_district(idf_dir, epw_file, output_dir):
    """
    Simulate all the district buildings.
    """

    # Clear the output directory before running the simulations
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # List of IDF files
    idf_list = []
    for x in os.listdir(idf_dir):
        if x.endswith(".idf"):
            idf_list.append(x)

    # Run the simulations
    print("\n---------- EnergyPlus simulation --------------")
    run_time = {}
    for idx, file in enumerate(idf_list):
            
        idf_path = os.path.join(idf_dir, file)
        file_name, file_extension = os.path.splitext(file)
        osm_id = file_name.split("_")[0]
    
        # # check if the building is already simulated
        # if file_name + "out.csv" in os.listdir(idf_dir):
        #     continue
    
        # Run the IDF file
        sim_start = datetime.now()    
        ret_code = Run_IDF(file_name, idf_path, epw_file, output_dir)
        sim_end = datetime.now()
        elapsed_time = sim_end - sim_start
        rt = np.round(elapsed_time.microseconds/1e6, 2)
        run_time[osm_id] = rt
        print(f"{idx+1}) {osm_id} --> SUCCESS [{rt} s]" if ret_code==0 else f"{idx+1}) {osm_id} --> FAIL")
        # print("Runtime:", rt, "seconds")

    # save the simulation runtime results
    df_runtime = pd.DataFrame(run_time.items(), columns=["osm_id", "Time (s)"])
    df_runtime.to_csv(output_dir + "\..\Simulation_time.csv", index=False)
    
    # Folders to parse .err file
    folders = ["Warnings", "Severs"]
    for fld in folders:
        full_path = os.path.join(output_dir, fld)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    warnings, severes, err_list = [], [], []
    for x in os.listdir(output_dir):
        if x.endswith(".err"):
            err_list.append(x)
            w, s = parse_err(output_dir, x)
            warnings.extend(w)
            severes.extend(s)
    
    # print("\nParsing error files...")
    print(f"Total errors: {len(severes)}")  
    print(f"Total warnings: {len(warnings)}")

    return



