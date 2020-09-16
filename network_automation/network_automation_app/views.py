from django.shortcuts import render, HttpResponse
from .models import Device

# Create your views here.
def home(request):
  all_devices = Device.objects.all()
  ciscos = Device.objects.filter(vendor='cisco')
  mikrotiks = Device.objects.filter(vendor='mikrotik')

  context = {
    'all_devices': len(all_devices),
    'cisco_devices': len(ciscos),
    'mikrotik_devices': len(mikrotiks)
  }

  return render(request, 'home.html', context)

def devices(request):
  all_devices = Device.objects.all()

  context = {
    'all_devices': all_devices
  }

  return render(request, 'devices.html', context)