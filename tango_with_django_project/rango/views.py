from django.shortcuts import render
# import the http response object from the django.http module
# from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm

# each view exists within the views.py file as a series of individual functions
# each view takes in at least one argument - a Http Request object, which also lives in the django.http module
# each view must return a http response object
# for a user to see a view, you must map a URL to the view

# view called index
#def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
 #   top_pages = Page.objects.order_by('-views')[:5]
  #  category_list = Page.objects.order_by('-likes')[:5]
   # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    #context_dict['categories']=category_list
    #context_dict['top_pages']=top_pages
    #context_dict = {}
def index(request):
    # Query the Page model for the top five most viewed pages
    top_pages = Page.objects.order_by('-views')[:5]

    context = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': Category.objects.order_by('-likes')[:5],  # Include the top five most liked categories as before
        'top_pages': top_pages,  # Add the top five most viewed pages to the context
    }

    return render(request, 'rango/index.html', context=context)
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Shannon'}
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    # a HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # have we been provided with a valid form?
        if form.is_valid():
            # save the new category to the db
            form.save(commit=True)
            # now that the cat is saved, we could confirm this
            # for now, just redirect the user back to the index view
            return redirect('/rango/')
        else:
            # the supplied form contained errors -
            # just print them to the terminal
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    # you cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', 
                                        kwargs={'category_name_slug': category_name_slug}))
            
            else:
                print(form.errors)
        
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
