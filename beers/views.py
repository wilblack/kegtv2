from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return HttpResponse("Made it beers index.")