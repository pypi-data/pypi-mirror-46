from cli import pyke, behavior, commands
import click

@click.command('logs', help='Tail logs for an editable container.')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--container', '-c', prompt=True, help='The ID or the url-ref of the container the editable version belongs to.')
@click.option('--version', '-v', help='The version ID or the version-number')
@pyke.auth.profile_context_required
def tail(container, version, profile):
  behavior.ContainerVersionBehavior(profile=profile).tail_logs(container, version)


@click.command(help='This force updates your docker service. This can recover a process in a bad state.')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--container', '-c', prompt=True, help='The ID or the url-ref of the container the editable version belongs to.')
@click.option('--version', '-v', help='The version ID or the version-number')
@pyke.auth.profile_context_required
def force(container, version, profile):
  behavior.ContainerVersionBehavior(profile=profile).force_update(container, version)

@click.command('download', help='Download a zip file that contains this containers application source code')
@click.option('--profile', '-p', prompt=True, help='The name of the profile to use as the context for the command.', autocompletion=pyke.auth.get_profile_names)
@click.option('--container', '-c', prompt=True, help='The ID or the url-ref of the container the editable version belongs to.')
@click.option('--version', '-v', help='The version ID or the version-number')
@click.option('--path', help='Path to save zip file')
@pyke.auth.profile_context_required
def download_app_zip(container, version, profile, path):
  behavior.ContainerVersionBehavior(profile=profile).download_app_zip(container, version, path)



commands.microservice_version.add_command(download_app_zip)
commands.widget_version.add_command(download_app_zip)

commands.microservice_version.add_command(force)
commands.widget_version.add_command(force)

commands.microservice_version.add_command(tail)
commands.widget_version.add_command(tail)
