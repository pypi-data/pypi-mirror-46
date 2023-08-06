'''
pipl.packl
=============

Extension of setuptools to manage pipl packages (packls):
- Create a packl with pipl.setupl.create(path, name). It will create:
    <path>/<name>/setup.py
    <path>/<name>/<name>/__init__.py
    <path>/<name>/<name>/__setupl__.py
- All packages meta data are stored in the package <name>/__setupl__.py file
- The __setupl__.py file is edited by pipl.setupl.set_<data_name>() functions
- The __setupl__.py file contains the whole history of edition, this history
can be inspected with pipl.setupl.get_history(module_name)


'''
from __future__ import print_function

import os
import warnings
import getpass
import time
import pprint

import semantic_version
from devpi_plumber.client import DevpiClient

from . import project


def find_packl_path(from_path):
    print('Resolving package path', from_path)
    current = os.path.abspath(from_path)
    to_find = 'setup.py'
    while current:
        this_one = os.path.join(current, to_find)
        if os.path.exists(this_one):
            print('Found package at', current)
            return current
        dirname = os.path.dirname(current)
        if dirname == current:
            # case like D:\
            break
        current = dirname
    raise ValueError(
        'Could not find the package path for {!r}'.format(
            from_path
        )
    )
    
def assert_free_packl_name(packl_name, index_name=None):
    '''
    Raises if such package exists in the index.
    Default index_name is 'root/PROJ'
    '''
    warnings.warn(
        'assert_free_pack_name({!r}) : not implemented'.format(
            packl_name
        )
    )

def get_packl_name(packl_path):
    return os.path.basename(packl_path).replace('-', '_')

def _create_setup(folder):
    content = '''
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
name = os.path.basename(here).replace('-', '_')

# Load the package's __setupl__.py module as a dictionary.
setupl = os.path.join(here, name, '__setupl__.py')
d = dict(name=name, packages=[name])
with open(setupl) as fh:
    exec(fh.read(), d)
setup_kwargs = dict([ (k,v) for k, v in d.items() if not k.startswith('_') ])


setup(**setup_kwargs)

'''
    filename = os.path.join(folder, 'setup.py')
    with open(filename, 'w') as fh:
        fh.write(content)
    print('Created {}.'.format(filename))

def _create_init(src_path, packl_name):
    filename = os.path.join(src_path, '__init__.py')
    content = [
        "'''",
        '',
        packl_name,
        '='*len(packl_name),
        '',
        "'''",
        'from __future__ import print_function'
        '',
    ]
    with open(filename, 'w') as fh:
        fh.write('\n'.join(content))
    print('Created {}.'.format(filename))

def _create_setupl(src_path, packl_name):
    filename = os.path.join(src_path, '__setupl__.py')
    content = [
        "'''",
        '',
        '{}\'s setup kwargs'.format(packl_name),
        ' - names with leading _ are ommited, you can add some',
        '   but other than those, only setup() kwarg names are allowed.',
        ' - comments staring like "#>>> " are managed, dont edit them...',
        '',
        "'''",
        '',
    ]
    with open(filename, 'w') as fh:
        fh.write('\n'.join(content))
    print('Created {}.'.format(filename))

def create(path, packl_name):
    assert_free_packl_name(packl_name)
    if not os.path.exists(path):
        raise ValueError(
            'Cannot create packl in {}, path does not exists.'.format(
                path
            )
        )
    packl_path = os.path.join(path, packl_name)
    if os.path.exists(packl_path):
        raise Exception(
            'Cannot create packl {}, path already exists.'.format(
                packl_path
            )
        )
    os.mkdir(packl_path)

    src_path = os.path.join(packl_path, packl_name)
    os.mkdir(src_path)
    _create_init(src_path, packl_name)
    _create_setupl(src_path, packl_name)
    set_setupl_md(
        packl_path,
        'Packl creation, settings default values.',
        name=packl_name,
        version='0.0.1.wip0',
        author=getpass.getuser(),
        include_package_data=True,
        install_requires=[],
        extra_requires={},
        entry_points={},
        classifiers=[
            'Framework :: pipl',
            'Development Status :: 3 - Alpha',
        ],
    )
    _create_setup(packl_path)

def _get_setupl_path(packl_path):
    return os.path.join(
        packl_path,
        get_packl_name(packl_path),
        '__setupl__.py'
    )

def _get_setupl_md_edit_header(comment):
    user = getpass.getuser()
    ctime = time.ctime()
    content = [
        '',
        '#>>> _edited_ by {} on {}'.format(user, ctime)
    ]
    comment_lines = '#>>> '.join(comment.split('\n'))
    content.append('#>>> '+comment_lines)
    return content

def _load_setupl(packl_path):
    packl_name = get_packl_name(packl_path)
    setupl = os.path.join(packl_path, packl_name, '__setupl__.py')
    if not os.path.exists(setupl):
        raise ValueErr(
            'Not a packl path: "{}"'.format(
                packl_path
            )
        )
    d = dict(name=packl_name, packages=[packl_name])
    with open(setupl, 'r') as fh:
        exec(fh.read(), d)

    setupl_dict = dict([ (k,v) for k, v in d.items() if not k.startswith('_') ])
    return setupl_dict

def get_setupl_md(packl_path, md_name):
    setupl_dict = _load_setupl(packl_path)
    return setupl_path[md_name]

def set_setupl_md(packl_path, comment, **name_values):
    setupl_path = _get_setupl_path(packl_path)
    content = _get_setupl_md_edit_header(comment)
    for name, value in name_values.items():
        content.append(
            '{} = {!r}'.format(name, value)
        )
    content.append('')
    
    with open(setupl_path, 'a') as fh:
        fh.write('\n'.join(content)+'\n')

def add_to_setup_md(packl_path, comment, list_name, added, dict_name=None):
    setupl_path = _get_setupl_path(packl_path)
    content = _get_setupl_md_edit_header(comment)
    content.append(
        'added = {!r}'.format(added)
    )
    if dict_name is not None:
        content += [
            'values = {}.get({!r})'.format(dict_name, list_name),
            'if values is None:',
            '    values = []',
            '    {}[{!r}] = values'.format(dict_name, list_name),
        ]
        list_name = 'values'
    content.append(
        'if added not in {l}:\n    {l}.append(added)'.format(l=list_name)
    )
                                        
    content.append('')
    
    with open(setupl_path, 'a') as fh:
        fh.write('\n'.join(content)+'\n')
    
def show_setup(packl_path):
    setup_kwargs = _load_setupl(packl_path)
    for k, v in sorted(setup_kwargs.items()):
        pf = pprint.pformat(v)
        if '\n' in pf:
            pf = ('\n'+21*' ').join(pf.split('\n'))
            pf = pf[0]+'\n'+pf[1:-1]+pf[-1]
        print('{:>20s}={}'.format(k, pf))

def get_venv_path(packl_path):
    return os.path.join(
        os.path.dirname(packl_path),
        '.VENV'
    )

def get_venv_bin(packl_path):
    venv_path = get_venv_path(packl_path)
    system = platform.system()
    if system in ('Linux',):
        return os.path.join(venv_path, 'bin')
    else:
        return os.path.join(venv_path, 'Scripts')

def get_venv_python(packl_path):
    '''
    Returns the path to the python for this packl virtual env.
    '''
    return os.path.join(
        get_venv_bin(packl_path),
        os.path.basename(sys.executable)
    )

# def do_pip(packl_path, *args):
#     env = os.environ.copy()
#     # prevent all pip config files, event site-wide
#     # nb: this was deduced from pip.utils.appdirs.user_config_dir
#     # and may be a uggly-ass-hack :/
#     env['PIP_CONFIG_FILE'] = os.devnull
    
#     python = self.get_venv_python(packl_path)
#     cmd = [python, '-m', 'pip'] + args

#     ret = subprocess.call(cmd, env=env)
#     return ret is 0
    
##def do_pip_install(packl_path, index_url, *packl_specs):
##    args = ['install'] + packl_specs
##    if index_url is not None:
##        args += ['--index-url', index_url]
##    return do_pip(packl_path, *args)

def _install_dependencies(packl_path, dependency_names, index_name=None):
    assert(isinstance(dependency_names, (list, tuple))) # must be strings list
    packl_name = get_packl_name(packl_path)
    project_path = project.find_project_path(packl_path)
    url = project.get_server_url(project_path)
    index_name = index_name or 'root/PROJ'
    venv_path = get_venv_path(packl_path)
    print('Installing into venv '+venv_path)
    pwd =  os.path.abspath('.')
    try:
        os.chdir(packl_path)
        with DevpiClient(url) as devpi:
            devpi.use(index_name)
            devpi._execute(
                *(['install']+list(dependency_names)),
                **{'--venv':venv_path,}
            )
    finally:
        os.chdir(pwd)

def add_dependency(packl_path, dependency_name, comment, as_extra=None):
    '''
    Adds a dependency to the packl.
    The name will be added to 
    '''
    _install_dependencies(
        packl_path, [dependency_name], index_name=None
    )
    print('Installed {}, updating setupl...'.format(dependency_name))
    if as_extra:
        add_to_setup_md(
            packl_path, comment, as_extra, dependency_name, 'extra_requires'
        )
    else:
        add_to_setup_md(
            packl_path, comment, 'install_requires', dependency_name
        )
    print('setupl updated.')

def bump_version_major(packl_path, comment=None):
    version = get_setupl_md(packl_path, 'version')

    comment = comment or 'Major Version Bump'
    version = semantic_version.Version(version)
    version = version.next_major()

    set_setupl_md(packl_path, comment, version=version)
    
def bump_version_minor(packl_path, comment=None):
    version = get_setupl_md(packl_path, 'version')

    comment = comment or 'Minor Version Bump'
    version = semantic_version.Version(version)
    version = version.next_minor()

    set_setupl_md(packl_path, comment, version=version)
    
def bump_version_patch(packl_path, comment=None):
    version = get_setupl_md(packl_path, 'version')

    comment = comment or 'Patch Version Bump'
    version = semantic_version.Version(version)
    version = version.next_patch()

    set_setupl_md(packl_path, comment, version=version)
    
def upload(packl_path, user, password, index_name=None):
    '''
    Uploads the packl to the project index.
    index_name defaults to 'root/PROJ'
    '''
    packl_name = get_packl_name(packl_path)
    project_path = project.find_project_path(packl_path)
    url = project.get_server_url(project_path)
    index_name = index_name or 'root/PROJ'
    pwd =  os.path.abspath('.')
    try:
        os.chdir(packl_path)
        with DevpiClient(url, user, password) as devpi:
            devpi.use(index_name)
            devpi.upload(
                **{'--format':'sdist',}
            )
    finally:
        os.chdir(pwd)
