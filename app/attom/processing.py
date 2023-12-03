import os
import geopandas as gpd
from shapely.geometry import Point, MultiPoint
from shapely.ops import unary_union
import alphashape

class GeoDataFrameManager:
    @staticmethod
    def create_gdf_from_attom_data(attom_data):
        for record in attom_data:
            record['longitude'] = float(record['longitude'])
            record['latitude'] = float(record['latitude'])
        
        gdf_all_attom_points = gpd.GeoDataFrame(
            attom_data,
            geometry=[Point(data['longitude'], data['latitude']) for data in attom_data],
            crs='EPSG:4326'
        )
        gdf_all_attom_points['hide'] = False
        
        return gdf_all_attom_points

    @staticmethod
    def save_gdf_as_geojson(gdf, output_dir, filename):
        os.makedirs(output_dir, exist_ok=True)
        geojson_path = os.path.join(output_dir, filename)
        gdf.to_file(geojson_path, driver='GeoJSON')

    @staticmethod
    def create_gdf_from_data(data):
        """Create a GeoDataFrame from a list of data with longitude and latitude."""
        gdf = gpd.GeoDataFrame(
            data,
            geometry=[Point(float(record['longitude']), float(record['latitude'])) for record in data],
            crs="EPSG:4326"
        )
        gdf['hide'] = False
        return gdf
    
    @staticmethod
    def generate_concave_hull(gdf, alpha=1.0):
        """Generate a concave hull (alpha shape) from a GeoDataFrame."""
        points = MultiPoint(gdf.geometry.tolist())
        concave_hull = alphashape.alphashape(points, alpha)
        return gpd.GeoDataFrame(geometry=[concave_hull], crs=gdf.crs)
    
    @staticmethod
    def expand_polygon(gdf, distance):
        """Expand a polygon in a GeoDataFrame by a given distance."""
        expanded_polygon = gdf.buffer(distance)
        return gpd.GeoDataFrame(geometry=[expanded_polygon], crs=gdf.crs)