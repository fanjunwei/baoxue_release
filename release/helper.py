import re

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

    return {
        'project': project,
        'custom': custom,
        'branch_number': branch_number,
    }