import numpy as np
import pandas as pd
import os


def analyze(res_dir, HVAC_type):

    print("\n---------- Post-processing --------------")

    # Read district geospatial data
    dist_info_dir = os.path.realpath(os.path.join(res_dir, ".."))
    df_geo = pd.read_csv(dist_info_dir + "\District_geo.csv", index_col=["osm_id"], dtype={"osm_id":str})

    # Collect the csv files of the E+ results
    res_files = []
    for file in os.listdir(res_dir):
        if file.endswith("out.csv"):
            res_files.append(file)

    summary = {}
    for idx, file in enumerate(res_files):
        file_name, file_extension = os.path.splitext(file)
        file_name = file_name.split("out")[0]
        osm_id = file_name.split("_")[0]

        result = pd.read_csv(os.path.join(res_dir, file_name + "out.csv"))
        ts = pd.to_datetime(result["Date/Time"].str.strip(), infer_datetime_format=True, errors="coerce")
        result["Time"] = ts
        result.drop(columns="Date/Time", inplace=True)
        result.set_index("Time", inplace=True)

        # time step size in seconds
        t_step_size = (ts[1]-ts[0]).total_seconds()


        # Read result variables
        Tamb_EP = result["Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)"]
        Tzone_EP = result["ZONE1:Zone Air Temperature [C](TimeStep)"]
        Pel = result["Electricity:Facility [J](TimeStep)"] / t_step_size
        Pel.name = "Electricity:Facility [W](TimeStep)"
        Tset_h = result["ZONE1:Zone Thermostat Heating Setpoint Temperature [C](TimeStep)"]
        Tset_c = result["ZONE1:Zone Thermostat Cooling Setpoint Temperature [C](TimeStep)"]
        Tset_type = result["ZONE1:Zone Thermostat Control Type [](TimeStep)"]

        if HVAC_type == "IdealHVAC":

            heat = result["HVAC1:Zone Ideal Loads Supply Air Total Heating Rate [W](TimeStep)"]
            cool = result["HVAC1:Zone Ideal Loads Supply Air Total Cooling Rate [W](TimeStep)"]


        elif HVAC_type == "Boiler_DXcoil":

            # Tin_boiler = result["BOILER1:Boiler Inlet Temperature [C](TimeStep)"]
            # Tout_boiler = result["BOILER1:Boiler Outlet Temperature [C](TimeStep)"]
            # mdot_boiler = result["BOILER1:Boiler Mass Flow Rate [kg/s](TimeStep)"]
            # rad_power = result["BASEBOARD1:Baseboard Total Heating Rate [W](TimeStep)"]
            # Tin_rad = Tin_DH = result["BASEBOARD1:Baseboard Water Inlet Temperature [C](TimeStep)"]
            # Tout_rad = Tin_DH = result["BASEBOARD1:Baseboard Water Outlet Temperature [C](TimeStep)"]
            # mdot_rad = result["BASEBOARD1:Baseboard Hot Water Mass Flow Rate [kg/s](TimeStep)"]#/rho_fluid # m3/s
            # rad_power = result["BASEBOARD1:Baseboard Total Heating Rate [W](TimeStep)"]
            heat = result["BOILER1:Boiler Heating Rate [W](TimeStep)"]
            cool = result["COOLING_COIL1:Cooling Coil Total Cooling Rate [W](TimeStep)"]
            Pel_hvac = result["Electricity:HVAC [J](TimeStep)"] / t_step_size
            Pel_hvac.name = "Electricity:HVAC [W](TimeStep)"
            En_boiler = result["NaturalGas:Facility [J](TimeStep)"]
            LHV = 35_800_000 # LHV of natural gas (J/m3)
            gas_cons = En_boiler / LHV

        

        elif HVAC_type == "PTHP":
            heat = result["HEAT_PUMP1:Zone Packaged Terminal Heat Pump Total Heating Rate [W](TimeStep)"]
            cool = result["HEAT_PUMP1:Zone Packaged Terminal Heat Pump Total Cooling Rate [W](TimeStep)"]
            # el_hp = result["HEAT_PUMP1:Zone Packaged Terminal Heat Pump Electricity Rate [W](TimeStep)"]
            Pel_hvac = result["Electricity:HVAC [J](TimeStep)"] / t_step_size
            Pel_hvac.name = "Electricity:HVAC [W](TimeStep)"


        else:
            print("HVAC not in the list of [IdealHVAC, Boiler_DXcoil, PTHP]")


        # geospatial data
        addr = df_geo.loc[df_geo.index==osm_id, "addr_street"][0]
        addr_no = df_geo.loc[df_geo.index==osm_id, "addr_housenumber"][0]
        area = df_geo.loc[df_geo.index==osm_id, "area"][0]
        height = df_geo.loc[df_geo.index==osm_id, "height"][0]
        vol = np.round(area * height, 2)

        # District summary
        summary[osm_id] = {
            "Street": addr,
            "No": addr_no,
            "Area [m2]": area,
            "Volume [m3]": vol,
            "Heat [kWh]": np.round(heat.sum()*t_step_size/3600/1000, 2),              # [kWh]
            "Max. Heat [kW]": np.round(heat.max()/1000, 2),                           # [kW]
            "Cool [kWh]": np.round(cool.sum()*t_step_size/3600/1000, 2),              # [kWh]
            "Max. Cool [kW]": np.round(cool.max()/1000, 2),                           # [kW]
            "Electricity [kWh]": np.round(Pel.sum()*t_step_size/3600/1000, 2),        # [kWh]
            "Max. Electricity [kW]": np.round(Pel.max()/1000, 2)                      # [kW]
            }
        print(f"{idx+1}) {osm_id} --> Processed")
    
    # District summary
    dist_sum_dir = os.path.join(res_dir, "Summary")
    if not os.path.exists(dist_sum_dir):
        os.makedirs(dist_sum_dir)
    
    # save the summary dataframe
    df_summary = pd.DataFrame.from_dict(summary, orient="index")
    df_summary.index.name = "OSM_ID"
    df_summary.to_csv(dist_sum_dir + "\\District_summary.csv")

    # log general district results
    heat_tot = np.round(df_summary["Heat [kWh]"].sum()/1000, 2) # [MWh]
    cool_tot = np.round(df_summary["Cool [kWh]"].sum()/1000, 2) # [MWh]
    el_tot = np.round(df_summary["Electricity [kWh]"].sum()/1000, 2)     # [MWh]

    print("\n---------- District performance summary --------------")
    print("Heat: ", heat_tot, "MWh")
    print("Cool: ", cool_tot, "MWh")
    print("Electricity: ", el_tot, "MWh")
    print(f"Full results stored in '{res_dir}'")

    return df_summary

