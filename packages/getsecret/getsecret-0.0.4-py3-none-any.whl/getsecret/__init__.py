import yaml
from os.path import expanduser, isfile
import os

def getsecret(key):
  environ_value = os.environ.get(key)
  if environ_value != None:
    return environ_value
  secrets = {}
  if isfile('.getsecret.yaml'):
    secrets = yaml.load(open('.getsecret.yaml'), Loader=yaml.SafeLoader)
  elif isfile(expanduser('~/.getsecret.yaml')):
    secrets = yaml.load(open(expanduser('~/.getsecret.yaml')), Loader=yaml.SafeLoader)
  else:
    raise FileNotFoundError('cannot find .getsecret.yaml')
  if key not in secrets:
    raise ValueError('.getsecret.yaml does not contain key ' + key)
  return secrets[key]
