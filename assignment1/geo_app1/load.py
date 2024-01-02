import json
from django.contrib.gis.geos import Point
from .models import Restaurant, Hotel, Park, Library
from pathlib import Path

data_file_path = Path("geo_app1") / "data" / "Hotel-Restaurant_export.json"

with open(data_file_path, 'r', encoding="utf8") as hotelRestaurant_datafile:
    data = json.load(hotelRestaurant_datafile)

for element in data['elements']:
    if 'amenity' in element['tags'] and element['tags']['amenity'] == 'restaurant':
        Restaurant.objects.create(
            name=element['tags'].get('name'),
            location=Point(element['lat'], element['lon']),
            cuisine=element['tags'].get('cuisine'),
            opening_hours=element['tags'].get('opening_hours'),
            city=element['tags'].get('addr:city'),
            street=element['tags'].get('addr:street'),
            website=element['tags'].get('website'),
            wheelchair=element['tags'].get('wheelchair'),
        )
    elif 'amenity' in element['tags'] and element['tags']['amenity'] == 'library':
        Library.objects.create(
            name=element['tags'].get('name'),
            location=Point(element['lat'], element['lon']),
            city=element['tags'].get('addr:city'),
            street=element['tags'].get('addr:street'),
            website=element['tags'].get('website'),
            wheelchair=element['tags'].get('wheelchair'),
        )

    elif 'tourism' in element['tags'] and element['tags']['tourism'] == 'hotel':
        Hotel.objects.create(
            name=element['tags'].get('name'),
            location=Point(element['lat'], element['lon']),
            phone=element['tags'].get('phone'),
            city=element['tags'].get('addr:city'),
            street=element['tags'].get('addr:street'),
            website=element['tags'].get('website'),
            wheelchair=element['tags'].get('wheelchair'),
        )

    elif 'leisure' in element['tags'] and element['tags']['leisure'] == 'park':
        Park.objects.create(
            name=element['tags'].get('name'),
            location=Point(element['lat'], element['lon']),
        )
