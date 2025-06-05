#!/usr/bin/env python3
import os
import requests
import time
import traceback
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from dns.resolver import Resolver, LifetimeTimeout, NoNameservers
from dns.nameserver import Nameserver, Do53Nameserver

class Server:
  def __init__(self, addr: str):
    self.addr = addr
    self.nameserver = Do53Nameserver(addr)
    self.restart_uri = f'http://%s:5380/restart' % addr
    self.resolver = Resolver()
    self.resolver.nameservers = [self.nameserver]

  def __str__(self) -> str:
    return self.addr

  def __repr__(self) -> str:
    return f"Server(addr='%s',restart_uri='%s')" % (self.addr, self.restart_uri)

  def restart(self) -> Optional[Exception]:
    try:
      requests.put(self.restart_uri)
    except Exception as e:
      return e

  def alive(self, name: Optional[str]) -> bool:
    try:
      self.resolver.resolve(name if name is not None else 'google.com')
    except LifetimeTimeout:
      return False
    except NoNameservers:
      return False

    return True


def read_servers(value: str) -> list[Server]:
  return [Server(ns) for ns in value.split(';') if ns != '']


timeout = int(os.environ.get('TIMEOUT', 15))
servers = read_servers(os.environ.get('SERVERS', '192.168.1.2;192.168.1.9'))
test_name = os.environ.get('TEST_NAME')


while True:
  for server in servers:
    print(
      f'%s: Pinging server %s... ' % (
        datetime.now().isoformat(timespec='seconds'),
        server
      ),
      end=''
    )
    if not server.alive(test_name):
      print('failed, rebooting.')
      server.restart()
    else:
      print('succeeded.')

  time.sleep(timeout)
