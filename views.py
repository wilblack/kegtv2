from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    tv = {}
    return render_to_response("homepage.html",tv, context_instance=RequestContext(request))