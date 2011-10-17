##Django Boilerplate

Django Boilerplate is a set of project layouts that through trial and error we use
as a best practice.  Details about each project are stored in conf/project.py and are imported to
allow for maximum re-usability.


#Assumptions

* Python 2.7, PIP, and virtualenv installed.
* Use south
* Django 1.3.1 is the latest version of django at the current time.

## Setup

Setup a new virtualenv

    virtualenv projectname --no-site-packages
    
Activate the virtualenv
    
    source project/bin/activate
    
Install the build requirement of fabric

    pip install fabric

Add any vendor apps to requirements.txt.

## Method Reference (Fab)

### Helper Methods

View Log

    def view_log():
        run('sudo cat %s' % env.log_location)

Kicking Apache (Restart)

    def kick_apache():
        with cd(env.apache_bin_dir):
            run("./restart")

Use Virtualenv

    def virtualenv(command):
        with cd(env.directory):
            run(env.activate + '&&' + command)

Install PIP Requirements

    def install_requirements():
        virtualenv('pip install -r conf/requirements.txt')

Build migration (Local)

    def build_migration(app):
        local("python manage.py schemamigration %s --auto --settings=settings.local" % app)


Copy static directory to server static directory

    def copy_static():
        with cd(env.directory + '/static'):
            run('cp -r * ' + env.static_dir)
        
Memory check - Using default from Webfaction

    def memory():
        run("ps -u %s -o pid,rss,command" % env.deploy_user)

Quick fix, adds everything, commits to dev, checkouts prod, merges, and then pushes both.  At the end it checks out dev again.

    def quick_fix(msg):
        local("git add .&&git commit -m '%s'&&git checkout production&&git merge develop&&git push origin production develop&&git checkout develop" % msg)
        deploy()

Push code to your production branch

    def push():
        local('git push production master')

Pull from prodution branch

    def pull():
        with cd(env.directory):
            run('git pull origin production')

SyncDB, pass in environment

    def sync_db(env):
        if env == "local":
            local("python manage.py syncdb --settings=settings.local")
        else:
            virtualenv('python manage.py syncdb --settings=settings.%s' % env)

Run migrations, pass in environment

    def migrate(env):
        if env == "local":
            local("python manage.py syncdb --settings=settings.local")
        else:
            virtualenv('python manage.py migrate --settings=settings.%s' % env)

### Deployment Commands

Setup a clean virtualenv, static directory, and code directory.  It then installs MysqlDB and deploys.

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
            run('git checkout production')
        virtualenv("easy_install http://downloads.sourceforge.net/project/mysql-python/mysql-python-test/1.2.3c1/MySQL-python-1.2.3c1.tar.gz?use_mirror=voxel")
        deploy()

Destroy the entire environment.

    def destroy():
        run('sudo rm -R -f ' + env.directory)
        run('sudo rm -R -f ' + env.project_virtual)
        run("sudo rm -R -f " + env.static_dir)
        run("sudo rm -R -f " + env.static_dir + "/media")
        local('clear')
        print("Entire Filesystem for %s destroyed." % PROJECT_ID)
        time.sleep(3)
    

Nuke.  Nuke destorys everything, and then rebuilds the project from latest commits.
    
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

Main deploy method    

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

Prep the Mind..    

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
    
Run Locally

    def run_local():
        sync_db('local')
        migrate('local')
        run_local_server()

    

