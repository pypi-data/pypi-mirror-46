'''

workspace management 



'''
import sys
import os
import virtualenv
import platform
import subprocess

from devpi_plumber.client import DevpiClient

from . import project
from . import autopack


def is_workspace_path(path):
    return os.path.exists(
        os.path.join(
            path, '.workspace'
        )
    )

def is_workspace_group_path(path):
    return os.path.exists(
        os.path.join(
            path, '.workspace_group'
        )
    )

def find_workspace_path(from_path):
    print 'Resolving workspace path', from_path
    current = os.path.abspath(from_path)
    dot_workspace = '.workspace'
    while current:
        this_dot_workspace = os.path.join(current, dot_workspace)
        if os.path.exists(this_dot_workspace):
            print 'Found workspace at', current
            return current
        dirname = os.path.dirname(current)
        if dirname == current:
            # case like D:\
            break
        current = dirname
    raise ValueError(
        'Could not find the workspace path for {!r}'.format(
            from_path
        )
    )

def get_workspace_path(project_path, workspace_name):
    raise Exception('Is this OBSOLETE ?')

    #TODO: this should be able to handle workspaces outside the project (local workspace for example)
    path = os.path.join(
        project_path, 'workspaces', workspace_name
    )
    if not is_workspace_path(path):
        raise ValueError(
            'Could not find workspace {!r} in project {!r}'.format(
                workspace_name, project_path
            )
        )
    return path

def get_workspace_src_path(workspace_path):
    if not is_workspace_path(workspace_path):
        raise ValueError(
            'Path "{}" is not a workspace. '
            'Can\'t get src path. :/'.format(
                workspace_path
            )
        )

    return os.path.join(workspace_path, 'src')

def _create_workspace_group(path):
    print 'Creating workspace group', path
    dot_workspace_group = os.path.join(path, '.workspace_group')
    os.mkdir(path)
    with open(dot_workspace_group, 'w') as fh:
        fh.write('# This is a {} group\n\n'.format(__name__))

def _create_workspace(path, name=None):
    print 'Creating workspace', path
    os.mkdir(path)
    dot_workspace = os.path.join(path, '.workspace')
    with open(dot_workspace, 'w') as fh:
        fh.write('# This is a {}\n\n'.format(__name__))

    src_path = os.path.join(path, 'src')
    print 'Creating src dir', src_path
    os.mkdir(src_path)
        
    venv_prompt = '{%s}' %(name or os.path.basename(path),)
    venv_name = '.VENV'
    venv_path = os.path.join(path, venv_name)

    print 'Creating virtual env', venv_path
    virtualenv.create_environment(
        home_dir=venv_path,
        # This used to be True so that pipl can be imported from the workspace
        # But pipl may (should) be installed in a virtualenv so it would 
        # work... A cleaner isolated env is made without global site package
        # so this is now False.
        site_packages=False,
        prompt=venv_prompt,
        # This would clear the env if it already exists,
        # Maybe we should ?
        clear=False,
    )

    venv_prompt_file = os.path.join(path, venv_name, 'venv_prompt.txt')
    with open(venv_prompt_file, 'w') as fh:
        fh.write(venv_prompt)


def create_workspace(project_path, workspace_path):
    dirnames = os.path.normpath(workspace_path).split(os.path.sep)

    current = os.path.join(project_path, 'workspaces')
    while dirnames:
        dirname = dirnames.pop(0)
        current = os.path.join(current, dirname)
        if dirnames:
            if not os.path.exists(current):
                _create_workspace_group(current)
            elif not is_workspace_group_path(current):
                raise ValueError(
                    'Cannot create workspaces {!r}, {!r} is not a workspace group'.format(
                        workspace_path, current
                    )
                )
        else:
            if os.path.exists(current):
                raise ValueError(
                    'Path {!r} already exists !'.format(current)
                )
            _create_workspace(current, workspace_path)
            print 'Workspace {} Created for project {}'.format(
                workspace_path, project_path
            )

def get_workspace_namespace(workspace_path):
    project_path = project.find_project_path(workspace_path)
    workspaces_path = os.path.join(project_path, 'workspaces')
    namespace = workspace_path[len(workspaces_path):].replace(
        os.path.sep, "-"
    ).strip('-')
    return namespace

def make_package_name(namespace, short_name):
    return '{}-{}'.format(
        namespace, short_name
        ).lower().replace('-', '_')


def new_package(workspace_path, name):
    '''
    Create a package in this workspace
    '''
    namespace = get_workspace_namespace(
        workspace_path
    )
    pack_name = make_package_name(namespace, name)
    workspace_src_path = get_workspace_src_path(workspace_path)
    autopack.new_package(workspace_src_path, pack_name)
    print 'Created', pack_name, 'in', workspace_path

def upload_package(workspace_path, package_name, user, password):
    '''
    Uploads the package to the project index.
    The package_name may be the short or namespaced
    name
    '''
    src_path = get_workspace_src_path(workspace_path)

    package_path = os.path.join(src_path, package_name)
    if not autopack.is_package_path(package_path):
        namespace = get_workspace_namespace(workspace_path)
        full_package_name = make_package_name(namespace, package_name)
        full_package_path = os.path.join(src_path, full_package_name)
        if not autopack.is_package_path(full_package_path):
            raise ValueError(
                'Could not find package "{}" or "{}" '
                'in workspace "{}".'.format(
                    package_name, full_package_name,
                    workspace_path
                )
            )
        package_path = full_package_path

    package_name = os.path.join(package_path, 'setup.py')
    project_path = project.find_project_path(workspace_path)
    url = project.get_server_url(project_path)
    pwd =  os.path.abspath('.')
    try:
        os.chdir(package_path)
        with DevpiClient(url, user, password) as devpi:
            devpi.use('root/PROJ')
            devpi.upload(
                *('-y',),
                **{'--format':'sdist',}
            )
    finally:
        os.chdir(pwd)

def get_venv_prompt(workspace_path):
    venv_prompt_file = os.path.join(
        workspace_path, '.VENV', 'venv_prompt.txt'
    )
    if not os.path.exists(venv_prompt_file):
        return '?!Unamed!?'

    with open(venv_prompt_file) as fh:
        venv_prompt = fh.read().strip()
    return venv_prompt

def shell(workspace_path):
    venv_prompt = get_venv_prompt(workspace_path)
    project_name = os.path.basename(project.find_project_path(workspace_path))

    title = '[{}] {}'.format(project_name, venv_prompt)
    extra_env = {
        #WhyTF ? 'PYTHONPATH': str(get_workspace_src_path(workspace_path)),
    }
    shell_env = os.environ.copy()
    shell_env.update(extra_env)

    python = os.path.basename(sys.executable)
    system = platform.system()
    if system in ('Linux',):
        starter = [
            'lxterminal', '-t', title,
            '--working-directory='+workspace_path,
            '-e',
        ]
        activate_path = os.path.join(
            workspace_path, '.VENV', 'bin', 'activate'
        )
        command_args = [os.environ['SHELL'], '--rcfile', activate_path]
        shell = False
    else:
        starter = ['start', 'cmd', '/C']
        activate_path = os.path.join(
            workspace_path, '.VENV', 'Scripts', 'activate'
        )
        command_args = [
            '{} & cd /D {}'.format(
                activate_path,
                workspace_path
            )
        ]
        shell = True

    command_args = starter + command_args # use /K instead of /C to keep shell open ?

    print '>>>', subprocess.list2cmdline(command_args)
    subprocess.Popen(command_args, shell=shell, env=shell_env)

def python(workspace_path):
    venv_prompt = get_venv_prompt(workspace_path)
    project_name = os.path.basename(project.find_project_path(workspace_path))

    ps1 = '[{}] {} >>>'.format(project_name, venv_prompt)

    extra_env = {
        #WhyTF ? 'PYTHONPATH': str(get_workspace_src_path(workspace_path)),
    }
    shell_env = os.environ.copy()
    shell_env.update(extra_env)

    python = os.path.basename(sys.executable)
    system = platform.system()
    if system in ('Linux',):
        starter = ['lxterminal', '-t', ps1[:-4], '-e', ]
        python_path = os.path.join(
            workspace_path, '.VENV', 'bin', python
        )
        shell = False
    else:
        starter = ['start', 'cmd', '/C']
        python_path = os.path.join(
            workspace_path, '.VENV', 'Scripts', python
        )
        shell = True

    command_args = [python_path, '-i', '-c', 'import sys; sys.ps1 = %r'%ps1]
    command_args = starter + command_args # use /K instead of /C to keep shell open ?

    print '>>>', subprocess.list2cmdline(command_args)
    subprocess.Popen(command_args, shell=shell, env=shell_env)
