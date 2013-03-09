from fabric.api import *

def rsync(args):
    return 'rsync --exclude=repodata -av %s' % args

def sync_local_down():
    local(rsync('dl.rockstack.org:build/epel/6/ rpm/build/epel/6/'))

def sync_local():
    local(rsync('rpm/build/epel/6/ dl.rockstack.org:build/epel/6/'))

def sync_repo(name):
    root = '/srv/dl.rockstack.org/rpm/%s/el/6' % name

    sudo(rsync('build/epel/6/ %s' % root))

    for arch in ('SRPMS', 'i386', 'x86_64'):
        with cd('%s/%s' % (root, arch)):
            sudo('createrepo --update .')

def sync_testing():
    sync_repo('testing')

def sync_stable():
    sync_repo('stable')
