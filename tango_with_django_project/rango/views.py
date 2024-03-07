from django.shortcuts import render
# import the http response object from the django.http module
from django.http import HttpResponse

# each view exists within the views.py file as a series of individual functions
# each view takes in at least one argument - a Http Request object, which also lives in the django.http module
# each view must return a http response object
# for a user to see a view, you must map a URL to the view

# view called index
def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")