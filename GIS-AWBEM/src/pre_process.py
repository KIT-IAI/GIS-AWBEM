import numpy as np
import pandas as pd
import os
import re
import json
import utm
from pathlib import Path

# Get files locations
path_src = Path(__file__).resolve().parent
path_input = path_src.parent


def to_float(value):
    """
    Normalize numeric values: German to English
    - '1,5'  -> 1.5
    - '0,04' -> 0.04
    - numbers stay unchanged
    - '-' or None -> None
    """
    if value in ('-', None):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.replace(',', '.'))
    return None


def extract_layers(data, element):
    """
    Extract material layers for a given element (wall, roof, floor, foundation).
    """
    layer_pattern = re.compile(
        rf"^{element}_const_material_name_(\d+)$"
    )

    layers = {}
    for key, name in data.items():
        match = layer_pattern.match(key)
        if not match or name in ('-', None):
            continue

        idx = int(match.group(1))

        layers[idx] = {
            "name": name,
            "thickness": to_float(data.get(f"{element}_const_material_thick_{idx}")),
            "lambda": to_float(data.get(f"{element}_const_material_lambda_{idx}")),
            "rho": to_float(data.get(f"{element}_const_material_rho_{idx}")),
            "c": to_float(data.get(f"{element}_const_material_c_{idx}")),
        }

    # return layers ordered by index
    return dict(sorted(layers.items()))


def get_bldg_mat(mat_dict, B_type, B_year):

    if B_type in ['SFH', 'TH', 'MFH', 'AB']:

        # TH is not availabe in HUB4LCA and is replaced with SFH due to their high similarities
        if B_type == 'TH': B_type = 'SFH'

        candidates = []
        for k in mat_dict.keys():
            if B_type in k:
                # construction year bounds
                cy_bound = k.split('_')[1]
                cy_lb = int(cy_bound.split('-')[0]) if cy_bound.split('-')[0] else float("-inf")
                cy_ub = int(cy_bound.split('-')[1]) if cy_bound.split('-')[1] else float("inf")
                if B_year >= cy_lb and B_year <= cy_ub:
                    candidates.append(k)
        
        if len(candidates)>1: 
            rnd = np.random.choice(candidates)
            return mat_dict[rnd]
        elif len(candidates) == 1:
            return mat_dict[candidates[0]]


    elif B_type in ['Culture', 'School', 'Education', 'Health', 'Hospitality', 'Industrial', 'Office', 'Retail']:
        if B_type == 'School':
            B_type = 'Education'
        return mat_dict[B_type]

    else:
        return print(f'{B_type} and {B_year} does not exist')







def geo_process(path_input, osm_file):

    with open(path_input + f"{osm_file}", "r", encoding="utf-8") as f:
        geojson = json.load(f)

    # Extract the features
    rows = []
    for f in geojson["features"]:
        props = f["properties"]
    
        # Only keep features with a registered address
        if "addr:street" in props and "addr:housenumber" in props:
            row = props.copy()
            row["osm_id"] = f["id"]
            row.pop("@id")
            row["geometry_type"] = f["geometry"]["type"]
            row["coordinates"] = f["geometry"]["coordinates"]
            rows.append(row)
    df_geo = pd.DataFrame(rows)
    
    cols = []
    for col in df_geo.columns:
        if ":" in col:
            col = col.replace(":", "_")
        cols.append(col)
    
    df_geo.columns = cols

    
    # Geospatial coordinates to Cartesian coordinates
    df_geo = df_geo.rename(columns={"coordinates": "geo_coordinates"})
    df_geo['xy_coordinates'] = pd.Series(index=df_geo.index, dtype=object)
    for idx, (b_id, coords) in enumerate(zip(df_geo["osm_id"], df_geo["geo_coordinates"])):
    
        # osm id from building id
        osm_id = b_id.split("/")[1]
        df_geo.loc[idx, 'osm_id'] = osm_id
    
        # first and last vertices are the same. so we drop one of them.
        coords = coords[0][:-1]
        B1xy = []
        for coord in coords:
            lon = coord[0]
            lat = coord[1]
            x, y,_,__ = utm.from_latlon(lat, lon) # utm gets (lat,lon) as input and NOT (lon,lat)
            B1xy.append([x,y])
    
        # Define a refenrence vertice and move the other vertices accordingly
        B1xy = np.array(B1xy)
        Vref = B1xy[B1xy[:,1].argmin()] # reference vertice is the vertice with lowest y.
        XYs = B1xy - Vref
        XYs_list = [list(item) for item in XYs]
    
        # add the cartesian coordinates to the df_geo
        df_geo.loc[idx, 'xy_coordinates'] = [XYs_list]

    return df_geo


def enrich(df_geo, execute, path_enrichment, region, mun_growth, mun_size):

    mat_dict = {}
    Tabula = pd.read_csv(path_input + 'Tabula_Uvalues.csv', sep=';')

    if execute in ['Yes', 'YES', 'yes', 'y']:
        path_residential = os.path.join(path_enrichment, 'Residential')
        for folder in os.listdir(path_residential):
            Excel_dir = os.path.join(path_residential, folder)
            for file in os.listdir(Excel_dir):
        
                # SH and MFH
                if all(feature in file for feature in [region, mun_growth, mun_size]):
                    # print(file)
                    
                    df = pd.read_excel(Excel_dir + '\\' + file).T
                    res_dict = df[0].to_dict()
                    bldg_type = res_dict['bldg_type']
                    age_class = str(res_dict['age_class'])
                    wall_const_type = res_dict['wall_const_type']
                    # if bldg_type in ['SH', 'MFH']: # the adjacency is available only for SFH and MFH
                    #     bldg_adj = res_dict['bldg_adjacency']
                    
                    try: 
                        bldg_adj = res_dict['bldg_adjacency']
                        key = bldg_type + '_' + age_class + '_' + wall_const_type + '_' + bldg_adj
                    except:
                        key = bldg_type + '_' + age_class + '_' + wall_const_type
                    
                    mat_dict_res = {}
                    mat_dict_res['WWR'] = res_dict['window_wall_share']
                    # mat_dict_res['window_glazing'] = res_dict['window_glazing']
                    mat_dict_res['wall'] = extract_layers(res_dict, 'wall')
                    mat_dict_res['roof'] = extract_layers(res_dict, 'roof')
                    mat_dict_res['floor'] = extract_layers(res_dict, 'floor')
                    mat_dict[key] = mat_dict_res
                    
                    
                else: #AB
                    if any(feature in file for feature in [region, mun_growth, mun_size]):
        
                        df = pd.read_excel(Excel_dir + '\\' + file).T
                        res_dict = df[0].to_dict()
                        bldg_type = res_dict['bldg_type'] 
                        age_class = str(res_dict['age_class'])
                        wall_const_type = res_dict['wall_const_type']
                        # if bldg_type in ['SH', 'MFH']: # the adjacency is available only for SFH and MFH
                        #     bldg_adj = res_dict['bldg_adjacency']
                        
                        try: 
                            bldg_adj = res_dict['bldg_adjacency']
                            key = bldg_type + '_' + age_class + '_' + wall_const_type + '_' + bldg_adj
                        except:
                            key = bldg_type + '_' + age_class + '_' + wall_const_type
                        
                        mat_dict_res = {}
                        mat_dict_res['WWR'] = res_dict['window_wall_share']
                        # mat_dict_res['window_glazing'] = res_dict['window_glazing']
                        mat_dict_res['wall'] = extract_layers(res_dict, 'wall')
                        mat_dict_res['roof'] = extract_layers(res_dict, 'roof')
                        mat_dict_res['floor'] = extract_layers(res_dict, 'floor')
                        mat_dict[key] = mat_dict_res
    
    
        non_res_list = ['Culture', 'Education', 'Health', 'Hospitality', 'Industrial', 'Office', 'Retail']
        for nr in non_res_list:
            df_nr = pd.read_excel(fr'C:\Users\yf9777\Desktop\ABEMOD\Inputs\HUB4LCA\{nr}\minimal_excel_{nr}_only_window.xlsx').T
            nr_dict = df_nr[0].to_dict()
            mat_dict[nr] = {}
            mat_dict[nr]['WWR'] = nr_dict['window_wall_share']
            # mat_dict[nr]['window_glazing'] = nr_dict['window_glazing']
            mat_dict[nr]['wall'] = extract_layers(nr_dict, 'wall')
            mat_dict[nr]['roof'] = extract_layers(nr_dict, 'roof')
            mat_dict[nr]['floor'] = extract_layers(nr_dict, 'floor')


        # building heights and archetypes
        ethos = pd.read_csv(path_input + 'building_data_241_enriched.csv', sep=';', dtype={'osm_id': 'string'})
        
        # Fill the non-existing building types with existing OSM building types,
        ethos['building_type'] = ethos['building_type'].fillna(df_geo['building'])
        
        
        # Unify the building type terminologies
        # for idx, bldg_type in enumerate(ethos['building_type']):
        for idx, bldg_type in enumerate(df_geo['building']):
            if not bldg_type in ['SFH', 'TH', 'MFH', 'AB', 'School', 'Retail', 'Office', 'Commercial']:
                if bldg_type == 'apartments':
                    bldg_type = 'AB'
                elif bldg_type == 'terrace':
                    bldg_type = 'TH'
                elif bldg_type == 'detached':
                    bldg_type = 'SFH'
                elif bldg_type == 'school':
                    bldg_type = 'School'
                elif bldg_type == 'commercial':
                    bldg_type = 'Commercial'
            
                # Unknown building types are labeled as "yes". Assumption --> SFH
                elif bldg_type == 'yes':
                    bldg_type = 'SFH'
            
                # Other minor building classifications are assumed to be residential
                else:
                    bldg_type = 'SFH'
        
            ethos.loc[idx, 'building_type'] = bldg_type
        
        
        # Fill the non-existing construction year with the average of all building construction years
        ethos['construction_year'] = ethos['construction_year'].fillna(int(ethos['construction_year'].mean()))

        dict_enrich = {}
        for idx, osm_id in enumerate(ethos['osm_id']):
            dict_enrich[osm_id] = {}    
            B_year = int(ethos.loc[idx, 'construction_year'])
            B_height = ethos.loc[idx, 'height']
            B_type = ethos.loc[idx, 'building_type']
            
            dict_enrich[osm_id]['construction_year'] = B_year
            dict_enrich[osm_id]['building_type'] = B_type
            dict_enrich[osm_id]['height'] = B_height
        
            bldg_prop = get_bldg_mat(mat_dict, B_type, B_year)
            dict_enrich[osm_id]['WWR'] = bldg_prop['WWR']
            dict_enrich[osm_id]['roof'] = bldg_prop['roof']
            dict_enrich[osm_id]['floor'] = bldg_prop['floor']
            dict_enrich[osm_id]['wall'] = bldg_prop['wall']


            # Window material properties from Tabula. Only residential buildings are avaialable (12.03.2026)
            bldg_type = dict_enrich[osm_id]['building_type']
            if not bldg_type in ['SFH', 'TH', 'MFH', 'AB']:
                bldg_type = 'SFH'

            tab_win = Tabula[(Tabula['building_type']==bldg_type) &
                             (dict_enrich[osm_id]['construction_year'] >= Tabula['construction_year_lb']) &
                             (dict_enrich[osm_id]['construction_year'] <= Tabula['construction_year_ub'])]['window'].values[0]

            dict_enrich[osm_id]['window'] = tab_win


        # combine the enrichment and envelope data
        for idx, osm_id in enumerate(df_geo['osm_id']):
            df_geo.loc[idx, 'construction_year'] = dict_enrich[osm_id]['construction_year']
            df_geo.loc[idx, 'building_type'] = dict_enrich[osm_id]['building_type']

            # Note: missing values of 'building_levels' is suggested to be manually corrected in the OSM file. If not, mean of district is assumed for nans.
            if pd.isna(df_geo.loc[idx, 'building_levels']):
                df_geo.loc[idx, 'building_levels'] = df_geo['building_levels'].astype(float).mean()

            # Enrich the height with ETHOS
            if dict_enrich[osm_id]['height']:
                df_geo.loc[idx, 'height'] = dict_enrich[osm_id]['height']

                # Check for inaccurate building heights
                storey_height_min = 2.5 # [m]
                building_height_min = storey_height_min * float(df_geo.loc[idx, 'building_levels'])
                df_geo.loc[idx, 'height'] = max(building_height_min, dict_enrich[osm_id]['height'])

            # If ETHOS has no data, use the building levels
            elif df_geo.loc[idx, 'building_levels']:
                storey_height_replace = 3.0 # m
                df_geo.loc[idx, 'height'] = df_geo.loc[idx, 'building_levels'] * storey_height_replace

    return dict_enrich, df_geo



def internal_gains(file_name):

    IG_profile = {}
    IG_intensity = {}
    Tset = {}
    for i, name in enumerate(['Residential', 'School', 'Office', 'Commercial']):
        IG_profile[name] = pd.read_excel(path_input + file_name, sheet_name=name, nrows=24, usecols=range(5))
        Tset[name] = pd.read_excel(path_input + file_name, sheet_name=name, nrows=24, usecols=range(5,8))
        
        # Creat a dictionary for internal gain intensities
        IG_int = {}
        IG_int['People_activity [W/person]'] = pd.read_excel(path_input + file_name, sheet_name=name, nrows=1, usecols=['People_activity [W/person]']).values[0][0]
        IG_int['People_density [person/m2]'] = pd.read_excel(path_input + file_name, sheet_name=name, nrows=1, usecols=['People_density [person/m2]']).values[0][0]
        IG_int['Electric_equipment [W/m2]'] = pd.read_excel(path_input + file_name, sheet_name=name, nrows=1, usecols=['Electric_equipment [W/m2]']).values[0][0]
        IG_int['Lighting_level [W/m2]'] = pd.read_excel(path_input + file_name, sheet_name=name, nrows=1, usecols=['Lighting_level [W/m2]']).values[0][0]
        IG_intensity[name] = IG_int

    return IG_profile, IG_intensity, Tset
