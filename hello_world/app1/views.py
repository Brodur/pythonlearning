from django.shortcuts import render, HttpResponse
# Import friends so we can pass them in the context
from .models import Friends

# Create your views here.
def hello_world(request):
  all_friends = Friends.objects.all()
  context = {
    'title': 'Hello World',
    'name': 'Brodie Giesbrecht',
    'age': 23,
    'all_friends': all_friends
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