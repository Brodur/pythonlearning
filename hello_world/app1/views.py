from django.shortcuts import render, HttpResponse

# Create your views here.
def hello_world(request):
  return HttpResponse("<h1>Hello and welcome to Django</h1>")

def a(request):
  return HttpResponse("<h1>AAAAAAAAAAAAAAAAAAA</h1>")

def b(request):
  return HttpResponse("<h1>Beeeees!</h1>")