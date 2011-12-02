from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from json import dumps as json
from json import loads

from beers.models import Beer
from billboard.models import Menu, MenuItem, DisplaySettings

from math import floor

#TODO Put these config settings in the backend

display_settings = [{'id':1,
                     'name':"Wil's House",
                     'width':785,
                     'aspect_ratio': 4.0/2.9 },
                    {'id':2,
                     'name':"Bier One Original TV",
                     'width':785,
                     'aspect_ratio': 16.0/9.0 },
                    {'id':3,
                     'name':"Mac Book Pro",
                     'width':785,
                     'aspect_ratio':4.0/2.9,},
                    {'id':4,
                     'name':"LG Monitor",
                     'width':1425,
                     'aspect_ratio':4.0/2.47,},
                    ]
ASPECT_RATIO = 4.0/2.9  # My House 

#ASPECT_RATIO = 4.0/2.25  # (16:9) For Beir One
# Luke's TV WIDTH = 785     # Width in pixel of display device.
WIDTH = 785
def make_dims(WIDTH=785, ASPECT_RATIO=.75):
    """
    Given a width and Aspect ratio (0-1) returns a dictionary of various CSS 
    values needed. All values are in sting notation so can be %, px, or whatever
    
    
    """
    
    HEIGHT = int(floor(WIDTH/ASPECT_RATIO))
    HEIGHT = HEIGHT
    menu_item_height = int(floor(100.0/8))*.01*HEIGHT
    
    
    return {'ASPECT_RATIO':ASPECT_RATIO,
            'WIDTH':WIDTH,              # used by billboard_css.html
            
            
            'HEIGHT':HEIGHT,            # used by billboard_css.html
            'MENU_ITEM_HEIGHT': str(menu_item_height)+"px",
            'MENU_GRID_HEIGHT':"86%",
            'MENU_GRID_WIDTH':"99.9%",
            'COL_HEIGHT':"99%",
            'COL_WIDTH':32.5,
            'GRID_CELL_HEIGHT':24,
            'GRID_CELL_WIDTH':100,
            'MENU_FOOTER_HEIGHT':"5%",   # used by billboard_css.html
          }


def index(request):
    menus = Menu.objects.all()
    tv = {'menus':menus
          
          }
    return render_to_response("billboard/menu_list.html", tv, context_instance=RequestContext(request))

def show(request, menu_id):
    """
      Optional parameters in the query string
      ds_id
      
    """
    menu = Menu.objects.get(pk=menu_id)
    menuItems = menu.menuitem_set.all()
    
    if 'ds_id' in request.GET:
        ds = DisplaySettings.objects.get(pk = request.GET['ds_id'])
    else:
        ds = menu.display_settings
    
    try: 
        menuItems = menu.menuitem_set.all()
        menuItems = [item.json() for item in menuItems]
    except AttributeError:
        menuItems = []
    
    THEME = {'TITLE_COLOR':'#8C8572',
             'ACCENT_BORDER_COLOR':'#E0491B',
             'ACCENT_COLOR_LIGHT':"#F08752",
             'ACCENT_COLOR_MED':"#E05D18",
             'ACCENT_COLOR_DARK':"#923709",
             }
    
    tv = {'menu':menu,
          'menuItems':json(menuItems), # These are on the menu         
          }
    
    tv.update(THEME)
    dims = make_dims(ds.width, ds.aspect_ratio)
    tv.update(dims)
    tv.update({'display_settings':json(ds.json)})
    
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
          'menuItems':json(menuItems),  # On menu
          'beerItems':json(beerItems),  # Beer choices 
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
    
    
        
    
        