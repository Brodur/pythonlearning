from django.shortcuts import render, HttpResponse

# Create your views here.
def hello_world(request):
  return render(request, 'hello_world.html')

def a(request):
  return render(request, 'a.html')

def b(request):
  return render(request, 'b.html')