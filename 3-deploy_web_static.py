#!/usr/bin/python3
""" Fabric File """

from fabric.api import local, env, put, run
from datetime import datetime
import os.path


env.hosts = ['3.80.127.172', '54.86.53.211']


def deploy():
    """Deploy a file"""
    archive = do_pack()
    if archive is None:
        return False
    status = do_deploy(archive)
    return status


def do_deploy(archive_path):
    """Deploy an archive"""

    if not os.path.exists(archive_path):
        return False

    try:
        archiveName = archive_path[9:]
        archiveNameNoExt = archiveName[:-4]

        put(archive_path, '/tmp/' + archiveName)
        run("mkdir -p /data/web_static/releases/" + archiveNameNoExt)
        run("tar -xzvf /tmp/" + archiveName + " -C " +
            "/data/web_static/releases/" +
            archiveNameNoExt + " --strip-components=1")
        run("rm -f /tmp/" + archiveName)
        run("rm -f /data/web_static/current")
        run("rm -rf /data/web_static/releases" +
            archiveNameNoExt + " /data/web_static/current")
        run("sudo ln -sf /data/web_static/releases/" +
            archiveNameNoExt + " /data/web_static/current")

        return True
    except:
        return False


def do_pack():
    """ Pack up web_static dir """

    try:
        now = datetime.now()

        tarArchiveName = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"
        tarArchivePath = "versions/" + tarArchiveName

        local("mkdir -p versions")
        local("tar -czvf " + tarArchivePath + " web_static")

        return tarArchivePath

    except:
        return None
