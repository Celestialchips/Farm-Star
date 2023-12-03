# ArcGIS mapping

To use the application simply run

```bash
python3 main.py
```

The application converts datapoints

such as an address gets the geolocation and geocodes those locations afterwards the points are sent back to the Database using SQLAlchemy, but also outputs a geojson to send back to a GIS map.

Here is the paper for the Alpha-concave Hull and how we achieve this result.

https://arxiv.org/pdf/1309.7829.pdf