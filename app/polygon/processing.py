from shapely.geometry import Point, MultiPoint
import geopandas as gpd
from fiona.crs import from_epsg

class PolygonCreator:
    @staticmethod
    def create_polygon_from_points(point_list):
        points = [Point(lon, lat) for lon, lat in point_list]
        return MultiPoint(points).convex_hull

    @staticmethod
    def create_gdf_from_points(points, geometry_field='geometry'):
        gdf_points = gpd.GeoDataFrame(points, geometry=geometry_field)
        gdf_points.set_crs(epsg=4326, inplace=True)
        return gdf_points
