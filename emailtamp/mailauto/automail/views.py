from tempfile import template
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def home(request):
    print("enterd")
    template = loader.get_template('index.html')  
    name = {  
        'student':'rahul'  
    }  
    return HttpResponse(template.render(name))