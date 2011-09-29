from fabric.api import *
from project import *

import time

env.id = PROJECT_ID
env.user = PROJECT_USER
env.hosts = PROJECT_HOSTS


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
    local('cd ~/projects/%s' % env.id)
    local('git pull origin')

def install_requirements():
    local('workon %s' % env.id)
    local('pip install -r ~/projects/%s/conf/requirements.txt')

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