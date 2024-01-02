from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from . import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import JsonResponse

from geopy.distance import geodesic

# Create your views here.
from .models import Hotel, Restaurant, Library, Park, Profile
from django.core.serializers import serialize


def update_location(request):
    try:
        print(request.POST.get('point', ''))
        user_profile = models.Profile.objects.get(user=request.user)
        if not user_profile:
            raise ValueError("Can't get User details")
        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)
        print(point)
        user_profile.location = point
        user_profile.save()
        return JsonResponse({"message": f"Set location to {point.wkt}."}, status=200)
    except Exception as e:
        raise e


def get_location_data(request):
    hotels = serialize('geojson', Hotel.objects.all(), fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
    restaurants = serialize('geojson', Restaurant.objects.all(), fields=('name', 'location', 'cuisine', 'opening_hours', 'website', 'city', 'street', 'wheelchair'))
    libraries = serialize('geojson', Library.objects.all(), fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
    parks = serialize('geojson', Park.objects.all(), fields=('name', 'location'))
    data = {'hotels': hotels, 'restaurants': restaurants, 'libraries': libraries, 'parks': parks}
    return JsonResponse(data)


def search_name(request):
    search_term = request.GET.get('search_result', '').lower()

    searched_hotels = Hotel.objects.all().filter(name__icontains=search_term)
    searched_restaurants = Restaurant.objects.all().filter(name__icontains=search_term)
    searched_libraries = Library.objects.all().filter(name__icontains=search_term)
    searched_parks = Park.objects.all().filter(name__icontains=search_term)

    hotels_geo = serialize('geojson', searched_hotels, fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
    restaurants_geo = serialize('geojson', searched_restaurants, fields=('name', 'location', 'cuisine', 'opening_hours', 'website', 'city', 'street', 'wheelchair'))
    libraries_geo = serialize('geojson', searched_libraries, fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
    parks_geo = serialize('geojson', searched_parks, fields=('name', 'location'))

    data = {'hotels': hotels_geo, 'restaurants': restaurants_geo, 'libraries': libraries_geo, 'parks': parks_geo}
    return JsonResponse(data)


def offline(request):
    return render(request, "offline.html")


def nearest_data(request):
    user_location = request.GET.get('point')

    nearest_hotel = None
    nearest_restaurant = None
    nearest_library = None
    nearest_park = None

    nearest_restplace = None

    minHotelDistance = float('inf')
    minRestaurantDistance = float('inf')
    minLibraryDistance = float('inf')
    minParkDistance = float('inf')

    nearest_distance = float('inf')

    for hotel in Hotel.objects.all():
        hotel_location = hotel.location
        hotel_distance = geodesic(user_location, hotel_location).km

        if hotel_distance < minHotelDistance:
            minHotelDistance = hotel_distance
            nearest_hotel = hotel

    for restaurant in Restaurant.objects.all():
        restaurant_location = restaurant.location
        restaurant_distance = geodesic(user_location, restaurant_location).km

        if restaurant_distance < minRestaurantDistance:
            minRestaurantDistance = restaurant_distance
            nearest_restaurant = restaurant

    for library in Library.objects.all():
        library_location = library.location
        library_distance = geodesic(user_location, library_location).km

        if library_distance < minLibraryDistance:
            minLibraryDistance = library_distance
            nearest_library = library

    for park in Park.objects.all():
        park_location = park.location
        park_distance = geodesic(user_location, park_location).km

        if park_distance < minParkDistance:
            minParkDistance = park_distance
            nearest_park = park


    nearest_distance = minHotelDistance

    nearest_restplace = serialize('geojson', [nearest_hotel], fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))

    if minRestaurantDistance < nearest_distance:
        nearest_restplace = serialize('geojson', [nearest_restaurant], fields=('name', 'location', 'cuisine', 'opening_hours', 'website', 'city', 'street', 'wheelchair'))
        nearest_distance = minRestaurantDistance

    if minLibraryDistance < nearest_distance:
        nearest_restplace = serialize('geojson', [nearest_library], fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
        nearest_distance = minLibraryDistance

    if minParkDistance < nearest_distance:
        nearest_restplace = serialize('geojson', [nearest_park], fields=('name', 'location'))
        nearest_distance = minParkDistance

    data = {'Nearest Place': nearest_restplace}

    return JsonResponse(data)




