from django.http import HttpResponse

from billboard.models import Menu  

from json import dumps as json

def pong(request, menu_id):
    """
    
    """
    get = request.GET
    
    try:
        menu = Menu.objects.get(pk=menu_id)
    except:
        return HttpResponse(json({'error':'Menu %s not found.' %menu_id}))
    rs={'need_update':True}
    return HttpResponse(json(rs))
    