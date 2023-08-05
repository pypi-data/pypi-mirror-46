import os


def put(local,remote):
    cmd="mega-put -c --ignore-quota-warn {} {}".format(local,remote)
    return os.popen(cmd).read()
def get(local,remote):
    cmd="mega-get -m --ignore-quota-warn {} {}".format(remote,local)
    return os.popen(cmd).read()
def find(name,remote="/"):
    cmd="mega-find {} --pattern={}".format(remote,name)
    return os.popen(cmd).read()
def is_exist(name,remote="/"):
    return remote in find(name,remote)
