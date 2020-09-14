from django.shortcuts import render, HttpResponse

# Create your views here.
def hello_world(request):
  context = {
    'title': 'Hello World',
    'name': 'Brodie Giesbrecht',
    'age': 23
  }
  return render(request, 'hello_world.html', context)

def a(request):
  context = {
    'title': 'EH'
  }
  return render(request, 'a.html', context)

def b(request):
  context = {
    'title': 'BEE',
  }
  return render(request, 'b.html', context)