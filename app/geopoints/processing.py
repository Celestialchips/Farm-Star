import os
import alphashape
import geopandas as gpd
from decimal import Decimal
from shapely.geometry import Point

class GeoprocessingManager:
    def __init__(self, original_data, attom_data):
        self.original_data_points = [
            (float(data['longitude']), float(data['latitude'])) for data in original_data
        ]
        self.attom_data_points = [
            (float(data['longitude']), float(data['latitude'])) for data in attom_data
        ]
    
    def filter_points_within_polygon(self, gdf_points, polygon):
        """Filter points that fall within the given polygon."""
        polygon_geo = gpd.GeoSeries([polygon], crs="EPSG:4326")
        points_within_polygon = gpd.sjoin(gdf_points, polygon_geo.to_frame(
            'geometry'), how="inner", predicate='within')
        return points_within_polygon.drop(columns='index_right')

    def save_filtered_points(self, gdf_filtered_points, output_dir, filename):
            """Save the filtered points to a GeoJSON file."""
            for col in gdf_filtered_points.columns:
                if gdf_filtered_points[col].apply(lambda x: isinstance(
                    x, Decimal)).any():
                    gdf_filtered_points[col] = gdf_filtered_points[col].apply(
                        lambda x: float(x) if isinstance(x, Decimal) else x)
            
            output_path = os.path.join(output_dir, filename)
            gdf_filtered_points.to_file(output_path, driver='GeoJSON')

    def generate_concave_hull(self, alpha):
        '''
        Build concave hull
        '''
        return alphashape.alphashape(self.original_data_points, alpha)

    def points_within_radius(self, center_point, radius):
        if not isinstance(center_point, Point):
            center_point = Point(center_point)
        circle = center_point.buffer(radius)
        return [point for point in 
                self.attom_data_points if circle.contains(point)]
