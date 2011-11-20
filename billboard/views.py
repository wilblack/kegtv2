from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from json import dumps as json
from json import loads

from beers.models import Beer
from billboard.models import Menu, MenuItem

from math import floor

#TODO Put these config settings in the backend
ASPECT_RATIO = 4.0/2.9  # My House 
#ASPECT_RATIO = 4.0/2.25  #For Beir One
# Luke's TV WIDTH = 785     # Width in pixel of display device.
WIDTH = 785

NROWS = 4
NCOLS = 3

ABV_COLOR="red"

def make_dims(WIDTH, ASPECT_RATIO, NROWS, NCOLS):
    
    HEIGHT = int(floor(WIDTH/ASPECT_RATIO))
    HEIGHT = HEIGHT
    
    ROW_HEIGHT = int(floor(HEIGHT/NROWS))
    ROW_HEIGHT = ROW_HEIGHT-30
    COL_WIDTH = int(floor(WIDTH/NCOLS))
    
    return {'ASPECT_RATIO':ASPECT_RATIO,
            'WIDTH':WIDTH,
            'HEIGHT':HEIGHT,
            'NROWS':range(NROWS),
            'NCOLS':range(NCOLS),
                  
            'MENU_TITLE_HEIGHT':6,
            'MENU_GRID_HEIGHT':86,
            'MENU_GRID_WIDTH':99.9,
            'COL_HEIGHT':99,
            'COL_WIDTH':32.5,
            'GRID_CELL_HEIGHT':24,
            'GRID_CELL_WIDTH':100,
            'MENU_FOOTER_HEIGHT':5,
          }


def index(request):
    menus = Menu.objects.all()
    tv = {'menus':menus
          
          }
    return render_to_response("billboard/menu_list.html", tv, context_instance=RequestContext(request))

def show(request, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    menuItems = menu.menuitem_set.all()
    
    try: 
        menuItems = menu.menuitem_set.all()
        menuItems = [item.json() for item in menuItems]
    except AttributeError:
        menuItems = []
    
    tv = {'menu':menu,
          'menuItems':json(menuItems),
          'ABV_COLOR':ABV_COLOR,
          'TITLE_COLOR':'#8C8572'
          }
    
    dims = make_dims(WIDTH, ASPECT_RATIO, NROWS, NCOLS)
    tv.update(dims)
    
    return render_to_response("billboard/show.html", tv, context_instance=RequestContext(request))
    
def edit(request, menu_id):
    
    # Get menu items for a given menu
    menu = Menu.objects.get(pk=menu_id)
    try: 
        menuItems = menu.menuitem_set.all()
        menuItems = [item.json() for item in menuItems]
    except AttributeError:
        menuItems = []
        
    # Get beer choices
    beers = Beer.objects.all()
    beerItems = [item.json() for item in beers]
    
    
    tv = {'menu':menu,
          'menuItems':json(menuItems),
          'beerItems':json(beerItems),
          'request':request,
          'ABV_COLOR':ABV_COLOR,
          }
    
    dims = make_dims(WIDTH, ASPECT_RATIO, NROWS, NCOLS)
    tv.update(dims)
    
    return render_to_response("billboard/edit.html", tv, context_instance=RequestContext(request))
        
   
def menu_item_JSON(request, menu_item_id):
    if request.method == 'POST': # If the form has been submitted...
        form = MenuItemForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = MenuItemForm() # An unbound form
 
    html = render_to_response('billboard/menu_item_form.html', {
        'form': form,
    }).content
    return HttpResponse(json(html))

def menu_item_save(request):
    if request.method == "POST":
        post = request.POST
        data = loads(post.keys()[0])
        beer = Beer.objects.get(pk=data['beer_id'])
        menu = Menu.objects.get(pk=data['menu_id'])
        
        # Delete old menu item at the location
        old_menuitem = MenuItem.objects.filter(menu=menu, position=data['position'])
        for item in old_menuitem:
            item.delete()
            
        menuitem = MenuItem(menu=menu,
                            beer=beer,
                            position=data['position'],
                            slogan=data['slogan']
                            )
            
        menuitem.save()
        return HttpResponse(json("Successfully saved form"))    
        
        return HttpResponse(json(data))
    return HttpResponse("Not a post")
    
    
        
    
        