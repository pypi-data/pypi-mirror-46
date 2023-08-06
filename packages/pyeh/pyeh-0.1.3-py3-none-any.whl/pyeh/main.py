import json
import requests
import time
from requests.auth import HTTPBasicAuth

domain = '.elastichosts.com'

distros = {
  'centos73': 'CentOS 7.3',
  'debian9': 'Debian 9',
  'ubuntu1804': 'Ubuntu 18.04'
}

class Instance:
  # TODO: Handle disk size on VM
  def __init__(self, params):
    # All available keys, and their defaults
    default = {
      'cpusize': 500,
      'disk': None,
      'disksize': 10,
      'distro': 'ubuntu1804',
      'memsize': 512,
      'name': None,
      'net': {},
      'password': None,
      'persistent': 'true',
      'ssh_key': None,
      'type': 'container'
    }

    # Update params with supplied values
    default.update(params)
    self.params = default

    # Check params
    if self.params['distro'] not in distros.keys():
      raise Exception('Unsupported distribution')

  def get_params(self):
    return self.params

  def instance_to_json(self):
    # Build JSON payload from supplied values
    res = {
      'cpu': self.params['cpusize'],
      'mem': self.params['memsize'],
      'name': self.params['name'],
      'nic:0:model': 'e1000',
      'nic:0:dhcp': 'auto',
      'password': 'Tr0l0l0',
      'type': self.params['type']
    }
    # Type
    if self.params['type'] == 'vm':
      res['boot'] = 'ide:0:0'
      res['ide:0:0'] = self.params['disk']
      res['vnc'] = 'auto'
    else:
      res['fs:0:mount'] = '/'
      res['fs:0'] = self.params['disk']
    # Other vars
    if self.params['persistent'] == 'true':
      # BUG: If persistent=false, we don't add it to JSON
      # This is a bug in the EH API itself
      res['persistent'] = 'true'
    if self.params['password'] != None:
      res['password'] = self.params['password']
    if self.params['ssh_key'] != None:
      res['ssh:0:key'] = self.params['ssh_key']
    return res

  def json_to_instance(self, data):
    # IN: json input (from server/create API)
    # OUT: a dict of instance params
    # This also renames container-specific attributes such as 'fs:0'
    # into generic ones, e.g. 'disk'
    res = {
      'name': data['name'],
      'uuid': data['server'],
      'type': data['type'],
      'cpu': data['cpu'],
      'status': data['status'],
    }

    if 'nic:0:ip' in data:
      res['ip'] = data['nic:0:ip']
    if 'persistent' in data:
      res['persistent'] = data['persistent']
    else:
      res['persistent'] = 'false'

    if data['type'] == 'vm':
      if 'ide:0:0' in data:
        res['disk'] = data['ide:0:0']
      elif 'block:0' in data:
        res['disk'] = data['block:0']
    else:
      res['disk'] = data['fs:0']
    return res

class Client:
  def __init__(self, zone, user, pwd, debug=False):
    self.debug = debug
    self.req = Request(zone, user, pwd, debug=debug)

  def log(self, msg):
    if self.debug:
      print(msg)

  def create_instance(self, params):
    # Create instance ('container' or 'vm')
    try:
      # Get disk for distro
      instance = Instance(params)
      params = instance.get_params()
      disk_img = self.get_disk_for_distro(params['distro'], params['type'])
    except Exception as e:
      raise Exception('No disk for distro {}'.format(params['distro']))

    # Create disk, and sync distro to it
    params['disk'] = self.clone_disk(disk_img, params)
    while self.is_cloning(params['disk'], params['type']):
      time.sleep(1)

    # Regenerate instance after adding disk
    instance = Instance(params)
    data = instance.instance_to_json()
    ret = self.req.post('/servers/create', data)
    return instance.json_to_instance(ret)

  def clone_disk(self, disk_img, params):
    # Returns disk uuid
    disk_data = { 'name': params['name'] }
    if params['type'] == 'vm':
      disk_data['size'] = params['disksize']*1024*1024*1024
      url = '/drives/{}/clone/gunzip'.format(disk_img)
    else:
      disk_data['tier'] = 'ssd'
      url = '/folders/{}/clone'.format(disk_img)
    disk = self.req.post(url, disk_data)
    if params['type'] == 'vm':
      return disk['drive']
    else:
      return disk['folder']

  def delete_disk(self, uuid):
    # Delete disk: automatic detect if vm or container (drive/folder)
    absent = True
    try:
      # Check if drive
      self.req.get('/drives/{}/info'.format(uuid))
      instancetype = 'vm'
    except requests.exceptions.HTTPError as e:
      if e.response.status_code == requests.codes.not_found:
        # 404, instance doesn't exist
        pass
    except Exception as e:
      raise Exception('Could not get drive: {}'.format(uuid))
    try:
      # Check if folder
      self.req.get('/folders/{}/info'.format(uuid))
      instancetype = 'container'
    except requests.exceptions.HTTPError as e:
      if e.response.status_code == requests.codes.not_found:
        # 404, instance doesn't exist
        pass
    except Exception as e:
      raise Exception('Could not get folder: {}'.format(uuid))

    try:
      # Delete
      if instancetype == 'vm':
        url = '/drives/{}/destroy'.format(uuid)
      else:
        url = '/folders/{}/destroy'.format(uuid)
      url = self.req.post(url)
    except requests.exceptions.HTTPError as e:
      if e.response.status_code == requests.codes.no_content:
        # 204, successful delete
        return None
    except Exception as e:
      raise Exception('Could not delete disk: {}'.format(uuid))

  def delete_instance(self, uuid):
    # Delete instance (does not check if active)
    try:
      self.req.post('/servers/{}/destroy'.format(uuid))
    except requests.exceptions.HTTPError as e:
      if e.response.status_code == requests.codes.no_content:
        # 204, successful delete
        return None
    except Exception as e:
      raise Exception('Could not delete instance: {}'.format(uuid))

  def get_disk_for_distro(self, distro, app_type):
    # Return uuid of distro's disk image
    #   app_type: 'vm', 'container'
    #   distro: e.g. 'debian9'
    self.log('Get image for {}'.format(distro))
    if app_type == 'vm':
      url = '/drives/info/standard'
    else:
      url = '/folders/info/standard'
    try:
      l = self.req.get(url)
    except Exception as e:
      raise Exception('Could not get standard disks')

    for i in l:
      if i['name'].startswith(distros[distro]):
        if app_type == 'vm':
          return i['drive']
        else:
          return i['folder']
    # /for
    raise Exception('Could not find distro')


  def get_instance(self, uuid):
    # Get instance. Return None if not present
    try:
      # Get instance info
      data = self.req.get('/servers/{}/info/full'.format(uuid))
      instance = Instance(data)
      return instance.json_to_instance(data)
    except requests.exceptions.HTTPError as e:
      if e.response.status_code == requests.codes.not_found:
        # 404, instance doesn't exist
        return None
      raise Exception('Unknown exception {}'.format(e))
    except Exception as e:
      raise Exception('Instance does not exist: '.format(e))

  def get_servers(self):
    return self.req.get('/servers/list')

  def is_cloning(self, uuid, app_type):
    # Given uuid of a disk, return True if the disk is cloning
    # app_type = 'vm' or 'container'
    if app_type == 'vm':
      if 'imaging' in self.req.get('/drives/{}/info'.format(uuid)).keys():
        return True
    else:
      if 'syncing' in self.req.get('/folders/{}/info'.format(uuid)).keys():
        return True
    return False

  def stop_instance(self, uuid, graceful=False):
    # Stop instance
    # Return:
    # - True if stopped
    # - False if could not stop in the time given
    # BUG: If a instance is persistent=false, we MUST 'shutdown' it (graceful=True)
    # BUG: If a instance has no 'persistent', then it is persistent=false
    try:
      if graceful:
        # Shutdown and wait until powered off
        instance = self.req.post('/servers/{}/shutdown'.format(uuid))
        is_active = False
        i = 0
        while i < 240:
            i = i + 1
            time.sleep(1)
            if self.get_instance(uuid)['status'] == 'stopped':
                return True
        # Failed
        return False
      else:
        # Stop (force)
        instance = self.req.post('/servers/{}/stop'.format(uuid))
    except Exception as e:
      raise Exception('Could not stop instance: {}'.format(uuid))
    return None

class Request:
  def __init__(self, zone, user, pwd, debug=False):
    self.url = 'https://api.' + zone + domain
    self.auth = HTTPBasicAuth(user, pwd)
    self.debug = debug

  def log(self, msg):
    if self.debug:
      print(msg)

  # PRIVATE
  # HTTP REST wrappers
  def get(self, url):
    return self.request('GET', url)

  def post(self, url, data=None):
    return self.request('POST', url, data)

  # Request
  def request(self, method, url, data=None):
    url = self.url + url
    self.log('{} {}'.format(method, url))
    headers = {'Accept': 'application/json'}
    try:
      if method == 'POST':
        if data != None:
          self.log('DATA')
          self.log(json.dumps(data, indent=2))
          f = requests.post(url, auth=self.auth, headers=headers, json=data)
        else:
          f = requests.post(url, auth=self.auth, headers=headers)
      else:
        f = requests.get(url, auth=self.auth, headers=headers)
      f.raise_for_status()
      if f.text:
        self.log(f.text)
        return json.loads(f.text)
      else:
        return None
    except requests.exceptions.HTTPError as e:
      self.log(e.response.content) # DEBUG
      raise e
    except requests.exceptions.RequestException as e:
      print('Other error: %s' %e)
