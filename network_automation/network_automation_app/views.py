import paramiko
import time

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Device, Log
from datetime import datetime

# Create your views here.
def home(request):
  all_devices = Device.objects.all()
  ciscos = Device.objects.filter(vendor='cisco')
  mikrotiks = Device.objects.filter(vendor='mikrotik')

  last_events = Log.objects.all().order_by('-id')[:10]


  context = {
    'all_devices': len(all_devices),
    'cisco_devices': len(ciscos),
    'mikrotik_devices': len(mikrotiks),
    'last_event': last_events
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
      try:
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

        log = Log(target=device.ip_address, action="Configure", status="Success", time=datetime.now(), messages="No Error")
        log.save()

      except Exception as e:
        log = Log(target=device.ip_address, action="Configure", status="Error", time=datetime.now(), messages=e)
        log.save()
    return redirect('/')
  else:
    devices = Device.objects.all()
    context = {
      'devices': devices,
      'mode': 'Configure'
    }

    return render(request, 'configure.html', context)

def verify_config(request):
  if request.method == "POST":
      result = []
      selected_device_id = request.POST.getlist('device')
      mikrotik_command = request.POST['mikrotik_command'].splitlines()
      cisco_command = request.POST['cisco_command'].splitlines()

      for device_id in selected_device_id:
        try:
          device = get_object_or_404(Device, pk=device_id)

          ssh_client = paramiko.SSHClient()
          ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
          ssh_client.connect(hostname=device.ip_address,username=device.username, password=device.password, look_for_keys=False)

          if device.vendor.lower() == 'cisco':
            conn = ssh_client.invoke_shell()
            conn.send("terminal length 0\n")

            for command in cisco_command:
              result.append("Result on {}".format(device.ip_address))
              conn.send(command + "\n")
              time.sleep(1)
              output = conn.recv(65535)
              result.append(output.decode())

          else:
            for command in mikrotik_command:
              stdin,stdout,stderr = ssh_client.exec_command(command)
              result.append("Result on {}".format(device.ip_address))
              result.append(stdout.read().decode())

          log = Log(target=device.ip_address, action="Verify Config", status="Success", time=datetime.now(), messages="No Error")
          log.save()

        except Exception as e:
          log = Log(target=device.ip_address, action="Verify Config", status="Error", time=datetime.now(), messages=e)
          log.save()

      result = '\n'.join(result)
      return render(request, 'verify_result.html', {'result':result})
  else:
    devices = Device.objects.all()
    context = {
      'devices': devices,
      'mode': 'Verify Configuration'
    }

    return render(request, 'configure.html', context)

def log(request):
  logs = Log.objects.all()

  context = {
    'logs': logs
  }

  return render(request, 'log.html', context)