#!/usr/bin/env python3
import dns.resolver
import requests
import time
import traceback
from datetime import datetime

resolver = dns.resolver.Resolver()

def ping(server, resolver):
  resolver.nameservers = [server]

  try:
    resolver.resolve('google.com')
  except dns.resolver.LifetimeTimeout:
    return False
  except dns.resolver.NoNameservers:
    return False

  return True

def restart(server):
  try:
    requests.put(f'http://%s:5380/restart' % server)
  except Exception:
    print('restart failed')
    print(traceback.format_exc())

servers = ['192.168.1.2', '192.168.1.9']

while True:
  for server in servers:

    print(
      f'%s: Pinging server %s... ' % (
        datetime.now().isoformat(timespec='seconds'),
        server
      ),
      end=''
    )
    if not ping(server, resolver):
      print('failed, rebooting.')
      restart(server)
    else:
      print('succeeded.')

  time.sleep(15)
