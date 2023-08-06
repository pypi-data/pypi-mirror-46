import click
import os
from urllib.parse import urlparse
from . import __version__
from .project import Project
from .package import Package

# click entrypoint
@click.group()
def main():
    """Startin'Blox installer"""
    pass

@main.command()
@click.argument('name', nargs=1)
@click.argument('directory', required=False)
@click.option('-m', '--modules', multiple=True, help='List of modules to install')
@click.option('--site-url', default='http://localhost:8000', help='Setup the site URL')
@click.option('--production', is_flag=True, default=False, help='Configure project for production')
@click.option('--db-host', help='Configure host for the database')
@click.option('--db-name', help='Configure name for the database')
@click.option('--db-user', help='Configure user for the database')
@click.option('--db-pass', help='Configure password for the database')
@click.option('--smtp-host', help='Configure host for the SMTP server')
@click.option('--smtp-user', help='Configure user for the SMTP server')
@click.option('--smtp-pass', help='Configure password for the SMTP server')
@click.option('--smtp-port', default=587, help='Configure port for the SMTP server')
@click.option('--smtp-tls', default=True, help='Configure TLS for the SMTP server')
def startproject(name, production, site_url, directory, modules, db_host, db_name, db_user, db_pass, smtp_host, smtp_user, smtp_pass, smtp_port, smtp_tls):

    """Start a new startin'blox project"""

    # set absolute path to project directory
    if directory:
        directory = os.path.abspath(directory)
    else:
        # set a directory from project name in pwd
        directory = os.path.abspath(name)

    # split modules and distributions in dependencies
    deps = []
    for module in modules:
        try:
            pkg, dist = module.split('@', 1)
        except ValueError:
            pkg = module
            dist = module

        deps.append((pkg, dist))

    # designed mandatory option for producrion
    if production:
        if not db_host:
            print('Error: Missing option "--db-host" for production')
            return
        if not db_name:
            print('Error: Missing option "--db-name" for production')
            return
        if not db_user:
            print('Error: Missing option "--db-user" for production')
            return
        if not db_pass:
            print('Error: Missing option "--db-pass" for production')
            return

    # build allowed_hosts from site_url
    allowed_hosts = urlparse(site_url).hostname

    project = Project(
        name=name,
        folder=directory,
        modules=deps
    )

    project.create(
        production=production,
        site_url=site_url,
        allowed_hosts=allowed_hosts,
        db_host=db_host,
        db_name=db_name,
        db_user=db_user,
        db_pass=db_pass,
        smtp_host=smtp_host,
        smtp_user=smtp_user,
        smtp_pass=smtp_pass,
        smtp_port=smtp_port,
        smtp_tls=smtp_tls
    )

@main.command()
@click.argument('directory', required=False)
@click.option('--production', is_flag=True, default=False, help='Configure project for production')
@click.option('--admin-name', help='Setup admin username')
@click.option('--admin-pass', help='Setup admin password')
@click.option('--admin-email', help='Setup admin email')
def initproject(directory, production, admin_name, admin_pass, admin_email):

    """Initialize a startin'blox project"""

    # set absolute path to project directory
    if directory:
        directory = os.path.abspath(directory)
    else:
        # get path from current dir
        directory = os.getcwd()

    # resolve project name from directory
    name = os.path.basename(directory)

    # designed mandatory option for producrion
    if production:
        if not admin_name:
            print('Error: Missing option "--admin-name" for production')
        if not admin_email:
            print('Error: Missing option "--admin-email" for production')
        if not admin_pass:
            print('Error: Missing option "--admin-pass" for production')
    else:
        if not admin_name:
            admin_name = 'admin'
        if not admin_email:
            admin_email = ''
        if not admin_pass:
            admin_pass = 'admin'

    project = Project(name, directory)

    project.load(admin_name, admin_pass, admin_email)


@main.command()
@click.argument('name', nargs=1)
@click.argument('directory', required=False)
def startpackage(name, directory):

    """Create a new startin'blox package"""

    # set absolute path to package directory (given directory is the project path)
    if directory:
        directory = os.path.join(os.path.abspath(directory), name)
    else:
        # get path from current dir
        directory = os.path.join(os.getcwd(), name)

    package = Package(name, directory)
    package.create()

@main.command()
def version():
    """Print module version"""
    click.echo(__version__)
