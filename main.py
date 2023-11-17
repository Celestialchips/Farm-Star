import os
import traceback
import geopandas as gpd
from shapely.geometry import Point
from app.auth.db_conn import DatabaseManager
from app.attom.processing import GeoDataFrameManager
from app.geopoints.processing import GeoprocessingManager
from app.etc.data_manager import DataManager
from app.auth.arcg import GisUploader
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        host = os.getenv('MYSQL_HOST')
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DATABASE')
        table_name_original = os.getenv('MYSQL_TABLE_1')
        table_name_attom = os.getenv('MYSQL_TABLE_2')
        esri_api_key = os.getenv('ESRI_API_KEY')
        output_dir = "all_gen_figures"
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        db_manager = DatabaseManager(host, user, password, database)
        
        original_data = db_manager.fetch_data(table_name_original)
        attom_data = db_manager.fetch_data(table_name_attom)

        gdf_manager = GeoDataFrameManager()
        geo_manager = GeoprocessingManager(original_data, attom_data)

        concave_hull = geo_manager.generate_concave_hull(alpha=20)
        gdf_concave_hull = gpd.GeoDataFrame(geometry=[concave_hull], crs="EPSG:4326")
        gdf_manager.save_gdf_as_geojson(gdf_concave_hull, output_dir, "concave_hull.geojson")

        distance = 0.01
        expanded_hull = concave_hull.buffer(distance)
        gdf_expanded_hull = gpd.GeoDataFrame(geometry=[expanded_hull], crs="EPSG:4326")
        gdf_manager.save_gdf_as_geojson(gdf_expanded_hull, output_dir, "expanded_hull.geojson")

        gdf_original = GeoDataFrameManager.create_gdf_from_data(original_data)
        gdf_attom = GeoDataFrameManager.create_gdf_from_data(attom_data)

        filtered_points_concave = geo_manager.filter_points_within_polygon(gdf_attom, concave_hull)
        geo_manager.save_filtered_points(filtered_points_concave, output_dir, "filtered_points_concave.geojson")

        filtered_points_expanded = geo_manager.filter_points_within_polygon(gdf_attom, expanded_hull)
        geo_manager.save_filtered_points(filtered_points_expanded, output_dir, "filtered_points_expanded.geojson")

        directory_path = 'all_gen_figures'
        table_prefix = table_name_attom
        GisUploader.upload_geojson_to_arcgis(esri_api_key, directory_path, prefix=table_prefix)

        gdf_original_points = GeoDataFrameManager.create_gdf_from_attom_data(original_data)
        gdf_manager.save_gdf_as_geojson(gdf_original_points, output_dir, "original_points.geojson")

        data_manager = DataManager(output_directory=output_dir)
        data_manager.save_all_attom_points_as_geojson(attom_data)

        db_manager.close_connection()

        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
