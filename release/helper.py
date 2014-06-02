import json
import re
from django.http import HttpResponse
import os

__author__ = 'fanjunwei'


def split_full_version(custom_version):
    if custom_version.startswith('eng.'):
        type = 'eng'
    else:
        type = 'user'
    custom_version = custom_version.replace('eng.', '').replace('user.', '')
    re1 = re.compile(r'^([^-_]+)_([^-_]+)_([^-_]+)_([^-_]+)$')
    match = re1.match(custom_version)
    if match:
        groups = match.groups()
        project = groups[0]
        custom = groups[1]
        branch = groups[2]
        version = groups[3]
        subversion = None
    else:
        re2 = re.compile(r'^([^-_]+)_([^-_]+)_([^-_]+)-([^-_]+)_([^-_]+)$')
        match = re2.match(custom_version)

        groups = match.groups()
        project = groups[0]
        custom = groups[1]
        branch = groups[2]
        subversion = groups[3]
        version = groups[4]

    return {'type': type,
            'project': project,
            'custom': custom,
            'branch': branch,
            'subversion': subversion,
            'version': version,

    }


def split_branch_full_name(full_name):
    re1 = re.compile(r'^([^-_]+)_([^-_]+)_([^-_]+)$')
    match = re1.match(full_name)
    if match:
        groups = match.groups()
        project = groups[0]
        custom = groups[1]
        branch_number = groups[2]
    else:
        project = None
        custom = None
        branch_number = None

    return project, custom, branch_number


def JsonResponse(success, message=None, result=None):
    map = {'success': success}
    if not result == None:
        map['result'] = result
    if not message == None:
        map['message'] = message
    return HttpResponse(json.dumps(map), 'application/json')


def getImageSize(path):
    pip = os.popen('identify %s' % path)
    res = pip.readline()
    pip.close()
    size_re = re.compile('\S* \S* (\S*)')
    match = size_re.search(res)
    if match:
        sizex = match.groups()[0]
        size = sizex.lower().split('x')
        if len(size) == 2:
            return int(size[0]), int(size[1])

    return None, None


def getFileType(name):
    n, e = os.path.splitext(name)
    e = e.lower()
    if e == '.jpg' or e == '.bmp' or e == '.png' or e == '.gif':
        return 'image'
    elif e == '.apk':
        return 'apk'
    else:
        return None


def getApkPackageName(path):
    try:
        pop = os.popen('aapt d badging ' + path)
        line = pop.readline()
        pop.close()
        re_name = re.compile(r"name=\'(.*?)\'")
        match = re_name.search(line)
        if match:
            packageName = match.groups()[0]
            return packageName
    except:
        pass

    return None


def delDir(dir):
    os.system('rm -r %s >/dev/null 2>&1' % dir)
