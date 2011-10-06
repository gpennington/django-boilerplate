from fabric.api import *
from project import *

import time

env.id = PROJECT_ID
env.user = PROJECT_USER
env.hosts = PROJECT_HOSTS
env.directory = '~/projects/%s' % PROJECT_ID
env.virtual_dir = '~/.virtualenvs'
env.static_dir = '~/static/prod'
env.project_virtual = '~/.virtualenvs/%s' % PROJECT_ID
env.activate = 'source ~/.virtualenvs/%s/bin/activate' % PROJECT_ID
env.deploy_user = PROJECT_USER
env.apache_bin_dir = "~/webapps/myproj/apache2/bin"

def setup():
    pass
    #makrvirtual environment
    #git init

#Local Commands
def run_local():
    local('python manage.py runserver --settings=settings.local')

def push():
    local('git push webfaction master')

     
#Server Commands
def pull():
    with cd(env.directory):
        run('git pull origin production')


def install_requirements():
    virtualenv('pip install -r conf/requirements.txt') 

def deploy():
    samuel_l_jackson()
    install_requirements()        
    local('touch ~/projects/%s/conf/%s.wsgi' % env.id)
    print('Deployment of %s complete' % env.id)

#Utils    
def samuel_l_jackson():
    local('clear')
    print('access main program')
    time.sleep(1)
    print('access main security')
    time.sleep(1)    
    print('access main program grid')
    time.sleep(3)    
    print('')
    print('')
    print('Hold on to yer butts...')
    print('')
    print('')
    
def kick_apache():
    with cd(env.apache_bin_dir):
        run("./restart")

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)

def sync_db(env):
    if env == "local":
        local("python manage.py syncdb --settings=settings.local")
    else:
        virtualenv('python manage.py syncdb --settings=settings.production')
    
def migrate(env):
    if env == "local":
        local("python manage.py syncdb --settings=settings.local")
    else:
        virtualenv('python manage.py migrate --settings=settings.production')

def build_migration(app):
    local("python manage.py schemamigration %s --auto --settings=settings.local" % app)
 