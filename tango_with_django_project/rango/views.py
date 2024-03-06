from django.shortcuts import render
# import the http response object from the django.http module
from django.http import HttpResponse

# each view exists within the views.py file as a series of individual functions
# each view takes in at least one argument - a Http Request object, which also lives in the django.http module
# each view must return a http response object
# for a user to see a view, you must map a URL to the view

# view called index
def index(request):
    return HttpResponse("Rango says hey there partner!")