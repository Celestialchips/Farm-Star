import os
import traceback
import requests
import shutil
import json
import geopandas as gpd
import decimal
import yaml
import traceback
from pathlib import Path
from shapely.geometry import Point
from app.auth.db_conn import DatabaseManager
from app.attom.processing import GeoDataFrameManager
from app.geopoints.processing import GeoprocessingManager
from app.etc.data_manager import DataManager
from app.utils import Utility
from dotenv import load_dotenv


load_dotenv()

def load_config():
    config_path = Path('config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(os.path.expandvars(file.read()))
    return config

# app = Flask(__name__, static_folder='static', template_folder='templates')

def fetch_and_prepare_data(db_manager, table_name):
    data = db_manager.fetch_data(table_name)
    gdf = GeoDataFrameManager.create_gdf_from_data(data)
    return gdf

def generate_and_save_hulls(geo_manager, gdf_manager, output_dir, alpha=20, distance=0.005):
    concave_hull = geo_manager.generate_concave_hull(alpha=alpha)
    gdf_concave_hull = gpd.GeoDataFrame(geometry=[concave_hull], crs="EPSG:4326")
    gdf_manager.save_gdf_as_geojson(gdf_concave_hull, output_dir, "concave_hull.geojson")

    expanded_hull = concave_hull.buffer(distance)
    gdf_expanded_hull = gpd.GeoDataFrame(geometry=[expanded_hull], crs="EPSG:4326")
    gdf_manager.save_gdf_as_geojson(gdf_expanded_hull, output_dir, "expanded_hull.geojson")
    return concave_hull, expanded_hull

def filter_and_save_points(geo_manager, gdf_attom, hull, output_dir, filename):
    filtered_points = geo_manager.filter_points_within_polygon(gdf_attom, hull)
    geo_manager.save_filtered_points(filtered_points, output_dir, filename)

def gdf_to_geojson(gdf):
    # Convert GeoDataFrame to a GeoJSON string
    return json.dumps(json.loads(gdf.to_json()))

def convert_decimals_to_floats(gdf):
    for column in gdf.columns:
        if gdf[column].apply(lambda x: isinstance(x, decimal.Decimal)).any():
            gdf[column] = gdf[column].astype(float)
    return gdf

def post_coordinates_to_endpoint(url, geojson_path):
    with open(geojson_path, 'r') as file:
        geojson = json.load(file)
    coordinates = geojson['features'][0]['geometry']['coordinates']
    payload = {
        'coordinates': coordinates
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Successfully uploaded coordinates from {geojson_path} to the endpoint.")
    else:
        print(f"Failed to upload coordinates from {geojson_path}. Status code: {response.status_code}, Response: {response.text}")

def process_geodata(config):
    db_manager = DatabaseManager(
        config['MYSQL_HOST'],
        config['MYSQL_USER'],
        config['MYSQL_PASSWORD'],
        config['MYSQL_DATABASE']
    )
    
    gdf_original = fetch_and_prepare_data(db_manager, config['MYSQL_TABLE_1'])
    gdf_attom = fetch_and_prepare_data(db_manager, config['MYSQL_TABLE_2'])

    gdf_original = convert_decimals_to_floats(gdf_original)
    gdf_attom = convert_decimals_to_floats(gdf_attom)

    gdf_manager = GeoDataFrameManager()
    geo_manager = GeoprocessingManager(gdf_original, gdf_attom)


    concave_hull, expanded_hull = generate_and_save_hulls(geo_manager, gdf_manager, config['OUT_DIR'])

    concave_hull_path = os.path.join(config['OUT_DIR'], "concave_hull.geojson")
    expanded_hull_path = os.path.join(config['OUT_DIR'], "expanded_hull.geojson")

    # with open(concave_hull_path, 'r') as file:
    #     concave_geojson = json.load(file)
    # concave_coordinates = concave_geojson['features'][0]['geometry']['coordinates']
    # concave_payload = {
    #     'coordinates': concave_coordinates
    # }
    # print("Payload for concave hull:", json.dumps(concave_payload, indent=4))

    post_coordinates_to_endpoint('https://1138-174-70-22-131.ngrok-free.app/polygons', concave_hull_path)
    post_coordinates_to_endpoint('https://1138-174-70-22-131.ngrok-free.app/polygons', expanded_hull_path)

    os.remove(concave_hull_path)
    os.remove(expanded_hull_path)

    gdf_manager.save_gdf_as_geojson(gdf_original, config['OUT_DIR'], "original_points.geojson")
    data_manager = DataManager(output_directory=config['OUT_DIR'])
    data_manager.save_all_attom_points_as_geojson(gdf_attom)

    db_manager.close_connection()

def main():
    config = load_config()
    # No need to set up output directory if we're not saving files there
    # setup_output_directory(config_manager.get_setting('output_dir'))

    try:
        successful = process_geodata(config)
        if successful:
            print('SUCCESS!')
            all_gen_figures_path = Path(config['OUT_DIR']) / 'all_gen_figures'
            Utility.empty_output_directory(all_gen_figures_path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()
