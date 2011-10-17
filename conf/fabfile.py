from __future__ import with_statement
from project import *
from fabric.api import *
import os
import glob
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
env.log_location = "~/webapps/logs/user/error_myproj.log"
env.git_repo = "git@github.com:myuser/%s.git" % PROJECT_ID
env.production_branch = "production"

# Utility Methods
def view_log():
    run('sudo cat %s' % env.log_location)

def kick_apache():
    with cd(env.apache_bin_dir):
        run("./restart")

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)

def install_requirements():
    virtualenv('pip install -r conf/requirements.txt')

def build_migration(app):
    local("python manage.py schemamigration %s --auto --settings=settings.local" % app)

def run_local_server():
    local('python manage.py runserver --settings=settings.local')

# Copy static dir to your production static server.
def copy_static():
    with cd(env.directory + '/static'):
        run('cp -r * ' + env.static_dir)
        
# Memory check - Using default from Webfaction
def memory():
    run("ps -u %s -o pid,rss,command" % env.deploy_user)

# Quick fix, adds everything, commits to dev, checkouts prod, merges, and then pushes both.  At the end it checks out dev again.
def quick_fix(msg):
    local("git add .&&git commit -m '%s'&&git checkout production&&git merge develop&&git push origin production develop&&git checkout develop" % msg)
    deploy()

def push():
    local('git push %s master' % env.production_branch)

def pull():
    with cd(env.directory):
        run('git pull origin %s' % env.production_branch)

def sync_db(env):
    if env == "local":
        local("python manage.py syncdb --settings=settings.local")
    else:
        virtualenv('python manage.py syncdb --settings=settings.%s' % env)
    
def migrate(env):
    if env == "local":
        local("python manage.py migrate --settings=settings.local")
    else:
        virtualenv('python manage.py migrate --settings=settings.%s' % env)

def setup():
    local("clear")
    print("Running Setup Script..I think..")
    run("mkdir " + env.directory)
    run("mkdir " + env.static_dir)
    run("mkdir " + env.static_dir + "/media")
    with cd(env.virtual_dir):
        run('virtualenv %s --no-site-packages' % PROJECT_ID)
    run("git clone " + env.git_repo + " " + env.directory)
    with cd(env.directory):
        run('git checkout %s' % env.production_branch)
    virtualenv("easy_install http://downloads.sourceforge.net/project/mysql-python/mysql-python-test/1.2.3c1/MySQL-python-1.2.3c1.tar.gz?use_mirror=voxel")
    deploy()

def destroy():
    run('sudo rm -R -f ' + env.directory)
    run('sudo rm -R -f ' + env.project_virtual)
    run("sudo rm -R -f " + env.static_dir)
    run("sudo rm -R -f " + env.static_dir + "/media")
    local('clear')
    print("Entire Filesystem for %s destroyed." % PROJECT_ID)
    time.sleep(3)
    

#Combo Deploy commands.

def nuke():
    print("You have decided to NUKE the project %s" % PROJECT_ID)
    time.sleep(3)
    print("Nuking......")
    time.sleep(1)
    print("...")
    destroy()
    local('clear')
    print("Rebuild started..")
    time.sleep(2)
    setup()
    print("Nuked.")
    
def deploy():
    samuel_l_jackson()
    install_requirements()
    pull()
    copy_static()
    sync_db("production")
    migration("production")
    # Either touch or restart of apache.
    local('touch ~/projects/%s/conf/%s.wsgi' % env.id)
    #kick_apache()
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
    


# Local Run.
def run_local():
    sync_db('local')
    migrate('local')
    run_local_server()

 
