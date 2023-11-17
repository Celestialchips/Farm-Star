import os
import traceback
import requests
import geopandas as gpd
import decimal
from shapely.geometry import Point
from app.auth.db_conn import DatabaseManager
from app.attom.processing import GeoDataFrameManager
from app.geopoints.processing import GeoprocessingManager
from app.etc.data_manager import DataManager
from app.auth.arcg import GisUploader
from dotenv import load_dotenv
from flask import Flask, jsonify, request


load_dotenv()

app = Flask(__name__)
class Artemis:
    def __init__(self):
        self.settings = {
            'host': os.getenv('MYSQL_HOST'),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'table_name_original': os.getenv('MYSQL_TABLE_1'),
            'table_name_attom': os.getenv('MYSQL_TABLE_2'),
            'esri_api_key': os.getenv('ESRI_API_KEY'),
            'output_dir': os.getenv('OUT_DIR')
        }

    def get_setting(self, key):
        return self.settings.get(key)

def setup_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

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

def upload_to_gis(esri_api_key, directory_path, prefix):
    GisUploader.upload_geojson_to_arcgis(esri_api_key, directory_path, prefix=prefix)

def convert_decimals_to_floats(gdf):
    for column in gdf.columns:
        if gdf[column].apply(lambda x: isinstance(x, decimal.Decimal)).any():
            gdf[column] = gdf[column].astype(float)
    return gdf

def process_geodata(config_manager):
    db_manager = DatabaseManager(
        config_manager.get_setting('host'),
        config_manager.get_setting('user'),
        config_manager.get_setting('password'),
        config_manager.get_setting('database')
    )
    
    gdf_original = fetch_and_prepare_data(db_manager, config_manager.get_setting('table_name_original'))
    gdf_attom = fetch_and_prepare_data(db_manager, config_manager.get_setting('table_name_attom'))

    gdf_original = convert_decimals_to_floats(gdf_original)
    gdf_attom = convert_decimals_to_floats(gdf_attom)

    gdf_manager = GeoDataFrameManager()
    geo_manager = GeoprocessingManager(gdf_original, gdf_attom)

    concave_hull, expanded_hull = generate_and_save_hulls(geo_manager, gdf_manager, config_manager.get_setting('output_dir'))

    filter_and_save_points(geo_manager, gdf_attom, concave_hull, config_manager.get_setting('output_dir'), "filtered_points_concave.geojson")
    filter_and_save_points(geo_manager, gdf_attom, expanded_hull, config_manager.get_setting('output_dir'), "filtered_points_expanded.geojson")

    gdf_manager.save_gdf_as_geojson(gdf_original, config_manager.get_setting('output_dir'), "original_points.geojson")
    data_manager = DataManager(output_directory=config_manager.get_setting('output_dir'))
    data_manager.save_all_attom_points_as_geojson(gdf_attom)
    upload_to_gis(config_manager.get_setting('esri_api_key'), config_manager.get_setting('output_dir'), 'all_gen_figures')
    db_manager.close_connection()

@app.route('/process_data', methods=['POST'])
def process_data_endpoint():
    config_manager = Artemis()
    try:
        process_geodata(config_manager)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

def main():
    config_manager = Artemis()
    setup_output_directory(config_manager.get_setting('output_dir'))
    
    try:
        process_geodata(config_manager)
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    main()
    # not really sure how to change this to run the flask app WIP
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True)