import subprocess
import sys
from os import mkdir, path, environ
from importlib import import_module
from pkg_resources import resource_filename


class Project(object):

    """
    This class initialize a new SIB project by installing the required components and configuring the project
    """

    def __init__(self, name, folder, modules=[]):

        """
        Initialization
        modules is a list of tuple (package, distrib)
        """

        # set project params
        self.project_name = name
        self.project_folder = folder

        # store packages (python module or packages)
        self.packages = [m[0] for m in modules]

        # store distribution (pip distributions)
        self.dists = [m[1] for m in modules]
        self.dists.append('djangoldp')  # add required distribution

    def get_template(self, production):

        """Return the path of django project template from package resouces"""

        if production:
            return resource_filename(__name__, 'templates/production')

        return resource_filename(__name__, 'templates/development')

    def create(self, site_url, allowed_hosts, production=False, db_host=None, db_name=None, db_user=None, db_pass=None, smtp_host=None, smtp_user=None, smtp_pass=None, smtp_port=587, smtp_tls=True):

        """Create the SIB project"""

        try:
            # create project folder
            mkdir(self.project_folder)

            # add psycopg2 for production
            if production:
                self.dists.append('psycopg2_binary')

            # install distributions
            cmd = ['pip', 'install']
            cmd.extend(self.dists)
            subprocess.run(cmd).check_returncode()

        except subprocess.CalledProcessError as e:
            print('Installation failed: {}'.format(e))
            return False

        try:
            from django.core import management
            from django.template.exceptions import TemplateSyntaxError

            # init django project
            management.call_command(
                'startproject',
                self.project_name,
                self.project_folder,
                template=self.get_template(production),
                packages=self.packages,
                site_url=site_url,
                allowed_hosts=allowed_hosts,
                db_host=db_host,
                db_name=db_name,
                db_user=db_user,
                db_pass=db_pass,
                smtp_host=smtp_host,
                smtp_user=smtp_user,
                smtp_pass=smtp_pass
            )

        except ModuleNotFoundError as e:
            print('[ERROR] Django not imported: {}'.format(e))
            return False

        except TemplateSyntaxError as e:
            print('[ERROR] Project template is wrong: {}'.format(e))
            return False

        return True

    def load(self, admin_name='admin', admin_pass='admin', admin_email=''):

        try:
            # load sib project settings
            sys.path.append(self.project_folder)
            sib_settings = import_module(self.project_name + '.settings')
            environ.setdefault('DJANGO_SETTINGS_MODULE', sib_settings.__name__)

            # django imports
            import django
            from django.core.exceptions import ImproperlyConfigured
            from django.core.management.base import CommandError
            from django.core import management

            # setup the django sib project
            django.setup()

        except ModuleNotFoundError as e:
            print('[ERROR] {}'.format(e))
            return False

        except ImportError as e:
            print('[ERROR] Project not initialized: {}'.format(e))
            return False

        try:
            # migrate data
            management.call_command('migrate', interactive=False)

        except ImproperlyConfigured as e:
            print('[ERROR] Django configuration failed: {}'.format(e))
            return False

        except CommandError as e:
            print('[ERROR] Django migration failed: {}'.format(e))
            return False

        try:
            # create superuser
            from django.contrib.auth.models import User
            User.objects.create_superuser(admin_name, admin_email, admin_pass)
        except ValueError as e:
            print('[ERROR] Super user creation failed: {}'.format(e))
            return False

        try:
            # creatersakey
            management.call_command('creatersakey', interactive=False)

        except CommandError:
            pass

        return True
