from fabric.api import *

env.roledefs['dl'] = ['dl.rockstack.org']

def rsync(args):
    return 'rsync --exclude=repodata -av %s' % args

def sync_local_down():
    local(rsync('%s:build/epel/6/ rpm/build/epel/6/' % env.roledefs['dl'][0]))

def sync_local():
    local(rsync('rpm/build/epel/6/ %s:build/epel/6/' % env.roledefs['dl']))

def sync_repo(name):
    root = '/srv/dl.rockstack.org/rpm/%s/el/6' % name

    sudo(rsync('build/epel/6/ %s' % root))

    for arch in ('SRPMS', 'i386', 'x86_64'):
        with cd('%s/%s' % (root, arch)):
            sudo('createrepo --update .')

@roles('dl')
def sync_testing():
    sync_repo('testing')

@roles('dl')
def sync_stable():
    sync_repo('stable')
