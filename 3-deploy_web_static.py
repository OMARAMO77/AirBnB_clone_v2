#!/usr/bin/python3
from datetime import datetime
from fabric.api import local, put, run, env

env.user = 'ubuntu'
env.hosts = ['35.229.93.37', '54.196.213.127']


def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of this repo.
    """
    d = datetime.now()
    now = d.strftime('%Y%m%d%H%M%S')

    local('sudo mkdir -p ./versions')
    path = './versions/web_static_{}'.format(now)
    local('sudo tar -czvf {}.tgz web_static'.format(path))
    return path

def do_deploy(archive_path):
    """Distributes an .tgz archive to my web servers
    """
    from os import path
    if path.exists(archive_path):
        archive = archive_path.split('/')[1]
        uploaded_tgz = "/tmp/{}".format(archive)
        fold_name = archive.split('.')[0]
        fold_path = "/data/web_static/releases/{}/".format(fold_name)

        put(archive_path, uploaded_tgz)
        run("sudo mkdir -p {}".format(fold_path))
        run("sudo tar -xzf {} -C {}".format(uploaded_tgz, fold_path))
        run("sudo rm {}".format(uploaded_tgz))
        run("sudo mv -f {}web_static/* {}".format(fold_path, fold_path))
        run("sudo rm -rf {}web_static".format(fold_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(fold_path))
        print('New version deployed!')
        return True
    return False


def deploy():
    """Creates and Distributes a .tgz archive through web servers
    """

    archive = do_pack()
    status = do_deploy(archive)
    return status
