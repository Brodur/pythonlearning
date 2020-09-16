import paramiko
import time

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
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

def configure(request):
  if request.method == "POST":
    selected_device_id = request.POST.getlist('device')
    mikrotik_command = request.POST['mikrotik_command'].splitlines()
    cisco_command = request.POST['cisco_command'].splitlines()

    for device_id in selected_device_id:
      device = get_object_or_404(Device, pk=device_id)

      ssh_client = paramiko.SSHClient()
      ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh_client.connect(hostname=device.ip_address,username=device.username, password=device.password, look_for_keys=False)

      if device.vendor.lower() == 'cisco':
        conn = ssh_client.invoke_shell()
        conn.send("conf t\n")

        for command in cisco_command:
          conn.send(command + "\n")
          time.sleep(1)

      else:
        for command in mikrotik_command:
          ssh_client.exec_command(command)

    return redirect('/')
  else:
    devices = Device.objects.all()
    context = {
      'devices': devices,
      'mode': 'Configure'
    }

    return render(request, 'configure.html', context)