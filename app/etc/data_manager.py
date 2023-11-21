import os
import json
import zipfile
import geopandas as gpd

from shapely.geometry import Point
from app.polygon.processing import PolygonCreator

class DataManager:
    '''
    This class manages attom data processing

    save attom points to a geojson
    &&
    processing attom data for filtering
    &&
    saving a shapefile
    '''
    def __init__(self, output_directory):
        self.output_directory = output_directory
        # os.makedirs(self.output_directory, exist_ok=True)
    
    def save_all_attom_points_as_geojson(self, gdf, filename="all_attom_points.geojson"):
        """
        Save a GeoDataFrame with point geometries to a GeoJSON file.

        Parameters:
        gdf (GeoDataFrame): The GeoDataFrame containing point geometries.
        filename (str): The name of the file to save.
        """
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
        
        geojson_path = os.path.join(self.output_directory, filename)
        gdf.to_file(geojson_path, driver='GeoJSON')
        
        print(f"All ATTOM points saved successfully to {geojson_path}")

    def process_attom_data(attom_data_file_path, convex_hull_polygon):
        with open(attom_data_file_path, 'r') as file:
            attom_data = json.load(file)

        inside_points = {
            key: value for key, value in attom_data.items()
            if Point(value['longitude'], value['latitude']).within(convex_hull_polygon)
        }
        all_points = [{key: value} for key, value in attom_data.items()]
        
        gdf_points = PolygonCreator.create_gdf_from_points(inside_points.values())
        gdf_all_points = PolygonCreator.create_gdf_from_points(all_points)

        output_dir_points = "filtered_points"
        os.makedirs(output_dir_points, exist_ok=True)
        
        # Save filtered points
        geojson_path_points = os.path.join(output_dir_points, "filtered_points.geojson")
        gdf_points.to_file(geojson_path_points, driver='GeoJSON')
        
        # Save all points (not filtered)
        geojson_path_all_points = os.path.join(output_dir_points, "all_points.geojson")
        gdf_all_points.to_file(geojson_path_all_points, driver='GeoJSON')
        
        return geojson_path_points, geojson_path_all_points

    def create_shapefile(gdf_polygon, output_dir_polygon, shapefile_name="polygon"):
        shapefile_path = os.path.join(output_dir_polygon, f"{shapefile_name}.shp")
        geojson_path_polygon = os.path.join(output_dir_polygon, f"{shapefile_name}.geojson")
        
        gdf_polygon.to_file(shapefile_path)
        gdf_polygon.to_file(geojson_path_polygon, driver='GeoJSON')

        shapefile_base_name = os.path.splitext(shapefile_path)[0]
        zipfile_path = shapefile_base_name + '.zip'
        
        with zipfile.ZipFile(zipfile_path, 'w') as zipf:
            for ext in ['.shp', '.shx', '.dbf', '.prj']:
                filename = shapefile_base_name + ext
                if os.path.exists(filename):
                    zipf.write(filename, arcname=os.path.basename(filename))

        return zipfile_path
