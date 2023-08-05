from urllib.parse import urlparse
from datetime import datetime
from cli import pyke
import subprocess
import click
import json
import os

class ContainerVersionBehavior:
  def __init__(self, profile=None):
    self.util = pyke.Util(profile=profile)
    self.object_type = 'container'

  def force_update (self, container, version):
    container_id = self.util.lookup_object_id(self.object_type, container)
    version_id = self.util.get_version_id(self.object_type, container, version)

    req_data = {'force': True}
    resp = self.util.cli_request('PUT',
        self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}',
          {'container_id': container_id, 'version_id': version_id}), json=req_data)

    click.echo(resp)

  def create_editable_version(self, container_id, from_version, env, format):
    if from_version is None:
      raise click.ClickException(click.style("An editable version must come from an exsisting version", fg='red'))

    version = self.util.get_container_version(container_id, from_version)

    if not version.get('editorPort'):
      raise click.ClickException(click.style("An editable version must come from an exsisting version with an editor port", fg='red'))

    versions = self.util.cli_request('GET', self.util.build_url('{app}/iot/v1/containers/{container_id}/versions?major={major}&minor={minor}&sort=patch+desc',\
          { 'container_id': version['containerId'], 'major': version['major'], 'minor': version['minor'] }))['payload']['data']

    if versions is not None and len(versions) > 0:
      latest_version = versions[0]

    version['patch'] = latest_version['patch'] + 1
    version['isEditable'] = True
    version['label'] = 'dev'

    del version['versionNumber']

    if 'env' not in version.keys():
      version['env'] = {}

    for var in env:
      try:
        env_dict = json.loads(var)
        version['env'] = { **version['env'], **env_dict}
      except Exception as e:
        print("Could not serialize {}".format(var))
        print(e)

    resp = self.util.cli_request('POST', self.util.build_url('{app}/iot/v1/containers/{container_id}/versions',\
      {'container_id': container_id}), data=json.dumps(version))

    # TO DO: Add progress bar after create for loading/validating microservice
    progress = 0
    status_id = None
    error = None

    if 'results' in resp['payload']['data'].keys():
      status_id = resp['payload']['data']['results']['statusId']
    if status_id:
      status_resp = self.util.show_progress(status_id, label='Creating Editable Version')
      error_msg = status_resp.get('payload', {}).get('data', {}).get('errorMessage')
      if error_msg is not None:
        raise pyke.CliException('Create version failed. {}'.format(error_msg))

    handlers = {
        'actualState': lambda x: click.style(x, fg='red') if x not in ['running'] else click.style(x, fg='green')
    }

    click.echo(click.style("Using the --is-editable flag ignores all options other than --format and --env", fg='yellow'))
    click.echo(click.style("The editable version will increment the patch number to the first available", fg='yellow'))

    self.util.print_table([resp['payload']['data']], format, handlers=handlers)

  def __touch(self, path):
    # Helper function
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
      os.makedirs(basedir)

    # Write an empty file into the dir
    open(path, 'a').close()

  def download_app_zip(self, container, version, path):
    home = os.path.expanduser('~')
    if path is None:
      path = home

    if not path.startswith(home):
      path = home + path

    container_id = self.util.lookup_object_id(self.object_type, container)

    try:
      container = self.util.cli_request('GET',
          self.util.build_url('{app}/iot/v1/containers?id={id}', {'id': container_id} ))['payload']['data']
    except:
      raise click.ClickException('Container not found')

    url_ref = container[0].get('urlRef')
    version_id = self.util.get_version_id(self.object_type, container_id, version)

    resp = self.util.cli_request('POST',
        self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}/token',
          {'container_id': container_id, 'version_id': version_id}), json={'type': 'editor'})

    token = resp.get('payload', {}).get('data', {}).get('token')

    p = urlparse(self.util.context.get('app'))
    service_url = '{}://experience.{}'.format(p.scheme, '.'.join(p.hostname.split('.')[1:]))

    # TODO: Dynamically get integration cloud
    editor_url = '{}/ic/{}/luma-editor/download/application.zip'.format(service_url, url_ref)

    time = datetime.now().time()

    zip_path = '{}/application-{}.zip'.format(path, time)
    #self.__touch(zip_path)

    command_list = 'curl -L -f --create-dirs --output {} {} -H '.format(zip_path, editor_url).split()
    command_list.append("Authorization: Bearer {}".format(token))

    click.echo("Zip file path: {}".format(zip_path))
    subprocess.run(command_list)

    click.echo("Saved zip file to: {}".format(path))

  def tail_logs(self, container, version):
    container = self.util.get_container(container)
    container_id = container.get('id')
    click.echo(container_id)

    version = self.util.get_container_version(container_id, version)
    version_id = version.get('id')

    url_ref = container.get('urlRef')

    is_editable = version.get('isEditable')
    if not is_editable:
      return self.old_logs(container_id, version_id)

    resp = self.util.cli_request('POST',
        self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}/token',
          {'container_id': container_id, 'version_id': version_id}), json={'type': 'editor'})

    token = resp.get('payload', {}).get('data', {}).get('token')

    p = urlparse(self.util.context.get('app'))
    service_url = '{}://experience.{}'.format(p.scheme, '.'.join(p.hostname.split('.')[1:]))

    # TODO: Dynamically get integration cloud
    editor_url = '{}/ic/{}/luma-editor/logs'.format(service_url, url_ref)

    command_list = 'curl {} -H '.format(editor_url).split()
    command_list.append("Authorization: Bearer {}".format(token))
    subprocess.run(command_list)

  def old_logs(self, container_id, version_id):
    resp = self.util.cli_request('GET', self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}/logs',\
      {'container_id': container_id, 'version_id': version_id}))

    for x in resp['payload']['data']:
      click.echo(x)


