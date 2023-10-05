#!/usr/bin/python3
from datetime import datetime
from fabric.api import local


def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of this repo.
    """
    d = datetime.now()
    now = d.strftime('%Y%m%d%H%M%S')

    local('sudo mkdir -p ./versions')
    path = './versions/web_static_{}'.format(now)
    local('sudo tar -czvf {}.tgz web_static'.format(path))
