'''

manage project structure:

    parent/project_name/
            .pipl                       <- identifies a pipl project
            server/                     <- devpi server files
            workspaces/
                user/
                    workspace_name

as well as administration
    
    new_project(name, path)
    exists(projct_path)
    start_server(project_path)          <- blocking (test server for now...)
    add_user(login, mail, pass)
    list_indexes()
    create_index(user, index_name, bases=[], volatile=False)

'''
from __future__ import print_function

'''

    TODO: 
        Use devpi "-getjson" for listing infos instead of "user --list" and "use -l" ?


'''
import sys
import platform
import os
import json
import contextlib
import virtualenv
import subprocess
from devpi_plumber.client import DevpiClient

from .utils import find_parent_dir, DirNotFoundError
from .utils import get_user_and_ctime


class Workspace(object):

    _ROOT_SENTINEL = '.workspace'
    _VENV_DIR_NAME = '.VENV'

    @classmethod
    def find_workspace_path(cls, from_path):
        return find_parent_dir(
            'Workspace', from_path, cls._ROOT_SENTINEL
        )

    @classmethod
    def create(cls, name, workarea_path):
        workarea_path = Workarea.find_workarea_path(
            workarea_path
        )
        print(
            'Creating workspace {} in {}'.format(
                name, workarea_path
            )
        )

        path = os.path.join(workarea_path, name)
        if os.path.exists(path):
            raise ValueError(
                'Can\'t create workspace: '
                'The path "{}" exists.'.format(
                    path
                )
            )
        
        os.mkdir(path)
        sentinel = os.path.join(path, cls._ROOT_SENTINEL)
        with open(sentinel, 'w') as fh:
            fh.write('# This is a pipl workspace.\n\n')
            
        venv_prompt = '{%s}'%(name,)
        venv_path = os.path.join(path, cls._VENV_DIR_NAME)

        print(
            'Creating virtual env "{}"'.format(
                venv_path
            )
        )
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

        venv_prompt_file = os.path.join(
            path, cls._VENV_DIR_NAME, 'venv_prompt.txt'
        )
        with open(venv_prompt_file, 'w') as fh:
            fh.write(venv_prompt)

        return cls(path)
    
    @classmethod
    def from_path(cls, path):
        '''
        Returns the Workspace managing the given path.
        The path may be:
            - the path of the Workspace
            - a path inside the Workspace
        '''
        path = cls.find_workspace_path(path)
        return cls(path)

    def __init__(self, path):
        super(Workspace, self).__init__()
        
        if not os.path.exists(
            os.path.join(
                path, self._ROOT_SENTINEL
            )
        ):
            raise ValueError(
                'Not a Workspace: "{}"'.format(
                    path
                )
            )

        self._path = path
        self._venv_prompt_file = os.path.join(
            path, self._VENV_DIR_NAME, 'venv_prompt.txt'
        )
        self._workarea = None # lazy created

    def path(self):
        return self._path

    def name(self):
        return os.path.basename(self.path())
    
    def workarea(self):
        if self._workarea is None:
            self._workarea = Workarea.from_path(
                self.path()
            )
        return self._workarea


    def get_venv_prompt(self):
        if not os.path.exists(self._venv_prompt_file):
            return '?!Unamed!?'

        with open(self._venv_prompt_file) as fh:
            venv_prompt = fh.read().strip()
        return venv_prompt

    def shell(self):
        venv_prompt = self.get_venv_prompt()
        project_name = self.workarea().project().name()

        title = '[{}] {}'.format(project_name, venv_prompt)
        extra_env = {
            #WhyTF ? 'PYTHONPATH': str(get_workspace_src_path(self.path())),
        }
        shell_env = os.environ.copy()
        shell_env.update(extra_env)

        python = os.path.basename(sys.executable)
        system = platform.system()
        if system in ('Linux',):
            starter = [
                'lxterminal', '-t', title,
                '--working-directory='+self.path(),
                '-e',
            ]
            activate_path = os.path.join(
                self.path(), self._VENV_DIR_NAME, 'bin', 'activate'
            )
            command_args = [os.environ['SHELL'], '--rcfile', activate_path]
            shell = False
        else:
            starter = ['start', 'cmd', '/K']
            activate_path = os.path.join(
                self.path(), self._VENV_DIR_NAME, 'Scripts', 'activate'
            )
            command_args = [
                '{} & cd /D {}'.format(
                    activate_path,
                    self.path()
                )
            ]
            shell = True

        command_args = starter + command_args # use /K instead of /C to keep shell open ?

        print('CMD', subprocess.list2cmdline(command_args))
        subprocess.Popen(command_args, shell=shell, env=shell_env)

    def python(self):
        venv_prompt = self.get_venv_prompt()
        project_name = self.workarea().project().name()

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
                self.path(), self._VENV_DIR_NAME, 'bin', python
            )
            shell = False
        else:
            starter = ['start', 'cmd', '/C']
            python_path = os.path.join(
                self.path(), self._VENV_DIR_NAME, 'Scripts', python
            )
            shell = True

        command_args = [python_path, '-i', '-c', 'import sys; sys.ps1 = %r'%ps1]
        command_args = starter + command_args # use /K instead of /C to keep shell open ?

        print('CMD:', subprocess.list2cmdline(command_args))
        subprocess.Popen(command_args, shell=shell, env=shell_env)


class Workarea(object):

    _ROOT_SENTINEL = '.workarea'

    @classmethod
    def find_workarea_path(cls, from_path):
        return find_parent_dir(
            'Workarea', from_path, cls._ROOT_SENTINEL
        )

    @classmethod
    def create(cls, workarea_path, project_path):
        area_parent, area_name = os.path.split(workarea_path)
        if not os.path.isdir(area_parent):
            raise ValueError(
                'Cant create workarea in {}: '
                'parent is not a folder.'.format(
                    workarea_path
                )
            )

        os.mkdir(workarea_path)
        config_path = os.path.join(workarea_path, cls._ROOT_SENTINEL)
        user, ctime = get_user_and_ctime()
        config = {
            'created_by': user,
            'created_on': ctime,
            'project_path': project_path,
        }
        with open(config_path, 'w') as fh:
            json.dump(config, fh)

        return cls(workarea_path)

    @classmethod
    def from_path(cls, path):
        '''
        Returns the Workarea managing the given path.
        The path may be:
            - the path of the Workarea
            - a path inside the Workarea
        '''
        path = cls.find_workarea_path(path)
        return cls(path)
        
    def __init__(self, path):
        '''
        Returns the workkarea at path.
        The path must be a valid Workarea path.
        (Use from_path() to find a Workarea from a path)
        
        '''
        super(Workarea, self).__init__()
        
        if not os.path.exists(
            os.path.join(
                path, self._ROOT_SENTINEL
            )
        ):
            raise ValueError(
                'Not a Workarea: "{}"'.format(
                    path
                )
            )

        self._path = path
        self._config_path = os.path.join(
            path, self._ROOT_SENTINEL
        )
        self._project = None # lazy created
        
    def path(self):
        return self._path

    def name(self):
        return os.path.basename(self.path())
    
    def _get_config(self):
        with open(self._config_path, 'r') as fh:
            config = json.load(fh) # read Workarea config
        return config

    def _make_project(self):
        path = self._get_config()['project_path']
        project = Project(path)
        return project

    def project(self):
        if self._project is None:
            self._project = self._make_project()
        return self._project

    def create_workspace(self, name):
        workspace = Workspace.create(
            name, self.path()
        )
        return workspace


class Project(object):

    _ROOT_SENTINEL = '.pipl'

    @classmethod
    def find_project_path(cls, from_path):
        return find_parent_dir(
            'Project', from_path, cls._ROOT_SENTINEL
        )
    
    @classmethod
    def create_project(cls, path, server_host='localhost', server_port=3141):
        path = os.path.abspath(path)
        try:
            existing_project = cls.find_project_path(path)
        except DirNotFoundError:
            pass
        else:
            raise ValueError(
                'Cannot create project at {}, a project exists at {}'.format(
                    path, existing_project
                )
            )

        parent_path, name = os.path.split(path)
        if not os.path.isdir(parent_path):
            raise ValueError(
                'Cant create project in {}: '
                'parent is not a folder.'.format(
                    parent_path
                )
            )

        os.mkdir(path)

        system = os.path.join(path, 'system')
        os.mkdir(system)

        sentinel = os.path.join(path, cls._ROOT_SENTINEL)
        with open(sentinel, 'w') as fh:
            fh.write(
                '# this is the root of the pipl project\n\n'
            )

        project = cls(path)
        project.create_workarea(
            os.path.join(path, 'workspaces')
        )

        server_path = os.path.abspath(
            os.path.join(system, 'server')
        )
        os.mkdir(server_path)

        server_config = os.path.join(system, 'server_config.yaml')
        config_content = [
            'devpi-server:',
            '  serverdir: {}'.format(server_path),
            '  host: {}'.format(server_host),
            '  port: {}'.format(server_port),
            '  role: standalone',
            '  no-root-pypi: 1',
            
        ]
        config_content = '\n'.join(config_content)
        print('Writting server config:\n'+config_content)
        with open(server_config, 'w') as fh:
            fh.write(config_content)

        print('Initializing Server')
        os.system('devpi-server -c {} --init'.format(server_config))

        print('Project Initialized')
        return project

    @classmethod
    def from_path(cls, path):
        '''
        Returns the project managing the given path.
        The path may be:
            - the path of the Project
            - a path inside the Project
            - a path inside a Workarea connected to the project
        '''
        try:
            path = cls.find_project_path(path)
        except DirNotFoundError as err:
            try:
                workarea = Workarea.from_path(path)
            except DirNotFoundError:
                raise err
            else:
                return workarea.project()
        else:
            return cls(path)
    
    def __init__(self, path):
        '''
        Returns the project at path.
        The path must be a valid project path.
        (Use from_path() to find a Project from a path)
        
        '''
        super(Project, self).__init__()
        if not os.path.exists(
            os.path.join(
                path, self._ROOT_SENTINEL
            )
        ):
            raise ValueError(
                'Not a pipl project: "{}"'.format(
                    path
                )
            )

        self._path = path
        self._server_config_file = os.path.join(
            path, 'system', 'server_config.yaml'
        )
        self._server_url_file = os.path.join(
            path, 'system', '.server_url'
        )

        self._devpi = None

    def path(self):
        return self._path

    def name(self):
        return os.path.basename(self.path())
    
    def create_workarea(self, workarea_path):
        workarea = Workarea.create(workarea_path, self.path())
        print('Workarea "{}" created.'.format(workarea_path))
        return workarea
    
    def _get_server_url_from_config(self):
        with open(self._server_config_file, 'r') as fh:
            content = fh.read()

        host = 'localhost'
        port = ''
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('host'):
                host = line.split(':')[-1].strip()
            elif line.startswith('port'):
                port = line.split(':')[-1].strip()

        if port:
            port = ':'+port
        return 'http://{}{}'.format(host, port or '')

    def start_server(self):
        '''
        Starts the project devpi-server (blocking).
        '''
        if os.path.exists(self._server_url_file):
            raise ValueError(
                'The server already seems to be running (see {})'.format(
                    self._server_url_file
                )
            )

        server_url = self._get_server_url_from_config()
        print('Serving at', server_url)
        with open(self._server_url_file, 'w') as fh:
            fh.write(server_url+'\n')
        try:
            os.system(
                'devpi-server -c {}'.format(
                    self._server_config_file
                )
            )
        finally:
            os.unlink(self._server_url_file)
        print('Server down from', server_url)


    def get_server_url(self):
        if not os.path.exists(self._server_url_file):
            raise ValueError(
                'The server does not seems to be running '
                '(File "{}" not found)'.format(
                    self._server_url_file
                )
            )
        with open(self._server_url_file) as fh:
            url = fh.read().strip()
        return url

    @contextlib.contextmanager
    def connected(self, user=None, password=None):
        '''
        Contexted connection.
        Usage:
            with project.connected('root', '123'):
                project.add_user(login, password, email)
                project.add_user(login, password, email)

            with project.connected():
                packages = project.list_index()
                
        '''
        if self._devpi is not None:
            raise Exception('Already connected.')

        url = self.get_server_url()
        print(
            'Connecting to {} '
            '(user:{}, pass:{})'.format(
                url,
                user,
                password and '*'*len(password or '') or None
            )
        )
        try:
            with DevpiClient(url, user, password) as devpi:
                self._devpi = devpi
                yield
        finally:
            self._devpi = None
            print('Disconnected.')
            
    def assert_connected(self, as_user=None):
        if self._devpi is None:
            raise Exception(
                'Not connected ! '
                'Please use Project.connected() before calling this'
            )
        if as_user is not None:
            user = self._devpi.user
            if user != as_user:
                raise Exception(
                    'Not connected as {user} ! '
                    'Please use Project.connected({user}, password) '
                    'before calling this.'.format(
                        user=as_user
                    )
                )
            
    def add_user(self, login, password, email):
        '''
        Project needs to be connected as root to use this.
        '''
        self.assert_connected('root')
        self._devpi.create_user(login, password=password, email=email)

    def update_user(self, login, password=None, email=None):
        '''
        Project needs to be connected as root to use this.
        '''
        kwargs = {}
        if password is not None:
            kwargs['password'] = password
        if email is not None:
            kwargs['email'] = email
        if not kwargs:
            raise ValueError('No password or email given, nothing to update')

        self.assert_connected('root')
        self._devpi.modify_user(login, **kwargs)

    def list_users(self):
        '''
        Project needs to be connected to use this.
        '''
        self.assert_connected()
        return self._devpi.list_users()

    def list_indices(self, user=None):
        '''
        Project needs to be connected to use this.
        '''
        self.assert_connected()
        return self._devpi.list_indices(user)

    def create_proj_index(self):
        '''
        Project needs to be connected as root to use this.
        '''
        index = 'root/PROJ'
        self.assert_connected('root')
        self._devpi.create_index(
            index, volatile=False, acl_upload=':ANONYMOUS:'
        )

    def create_sub_index(
        self, user_name, index_name, volatile=True, *acl_upload
    ):
        '''
        Project needs to be connected as root to use this.
        
        Create an new index. 
        All *acl_upload must be user logins or ':ANONYMOUS:'.
        If no acl_upload given, ':ANONYMOUS:' is used.
        '''
        index = '{}/{}'.format(user_name, index_name)
        bases = 'root/PROJ'
        acl_upload_str = acl_upload and ','.join(acl_upload) or ':ANONYMOUS:'
        self.assert_connected('root')
        self._devpi.create_index(
            index, 
            bases=bases,
            volatile=volatile, 
            acl_upload=acl_upload_str
        )

    def list_packages(self, index=None):
        '''
        Project needs to be connected to use this.

        Returns a list of all packages inside this index.
        If index is None, root/PROJ index is used.
        '''
        self.assert_connected()
        index_name = index or 'root/PROJ'
        self._devpi.use(index_name)
        return self._devpi.list()

#
#
#
# OLD API
#
#

##def new_project(name, path):
##
##    if not os.path.isdir(path):
##        raise ValueError('Folder {!r} does not exists !'.format(path))
##
##    root = os.path.join(path, name)
##    if os.path.exists(root):
##        raise ValueError('Folder {!r} already exists !'.format(root))
##
##    os.mkdir(root)
##
##    system = os.path.join(root, 'system')
##    os.mkdir(system)
##
##    dot_pipl = os.path.join(root, '.pipl')
##    with open(dot_pipl, 'w') as fh:
##        fh.write('# This is the root of the pipl project\n\n')
##
##    server_path = os.path.abspath(
##        os.path.join(system, 'server')
##    )
##    os.mkdir(server_path)
##
##    server_config = os.path.join(system, 'server_config.yaml')
##    with open(server_config, 'w') as fh:
##        fh.write(
##'''
##devpi-server:
##  serverdir: {}
##  host: localhost
##  port: 4040
##  role: standalone
##  no-root-pypi: 1
##
##'''.format(server_path)
##        )
##
##    print 'Initializing Server'
##    os.system('devpi-server -c {} --init'.format(server_config))
##
##    workspaces_path = os.path.join(root, 'workspaces')
##    os.mkdir(workspaces_path)
##
##def find_project_path(from_path):
##    find_parent_dir('Project', from_path, '.pipl')
####    print 'Resolving project path', from_path
####    current = os.path.abspath(from_path)
####    dot_pipl = '.pipl'
####    while current:
####        this_dot_pipl = os.path.join(current, dot_pipl)
####        if os.path.exists(this_dot_pipl):
####            print 'Found project at', current
####            return current
####        dirname = os.path.dirname(current)
####        if dirname == current:
####            # case of D:\
####            break
####        current = dirname
####    raise ValueError(
####        'Could not find the project root path under {!r}'.format(
####            from_path
####        )
####    )
##
##def _get_server_url_from_config(server_config):
##    with open(server_config, 'r') as fh:
##        content = fh.read()
##
##    host = 'localhost'
##    port = ''
##    for line in content.split('\n'):
##        line = line.strip()
##        if not line or line.startswith('#'):
##            continue
##        if line.startswith('host'):
##            host = line.split(':')[-1].strip()
##        elif line.startswith('port'):
##            port = line.split(':')[-1].strip()
##
##    if port:
##        port = ':'+port
##    return 'http://{}{}'.format(host, port or '')
##
##def start_server(project_path):
##    if not os.path.exists(
##        os.path.join(
##            project_path, '.pipl'
##        )
##    ):
##        raise ValueError(
##            'Folder {!r} is not a pipl project !'.format(
##                project_path
##            )
##        )
##
##    server_url_file = os.path.join(project_path, 'system', '.running_url')
##    if os.path.exists(server_url_file):
##        raise ValueError(
##            'The server seems to be running (see {})'.format(
##                server_url_file
##            )
##        )
##
##    server_config = os.path.join(
##        project_path, 'system', 'server_config.yaml'
##    )
##    server_url = _get_server_url_from_config(server_config)
##
##    with open(server_url_file, 'w') as fh:
##        print 'Running Server on', server_url
##        fh.write(server_url+'\n')
##    try:
##        os.system('devpi-server -c {}'.format(server_config))
##    finally:
##        os.unlink(server_url_file)
##    print 'Sever down from', server_url
##
##def get_server_url(project_path):
##    server_url_file = os.path.join(project_path, 'system', '.running_url')
##    if not os.path.exists(server_url_file):
##        raise ValueError(
##            'The server does not seem to be running (missing {})'.format(
##                server_url_file
##            )
##        )
##    with open(server_url_file) as fh:
##        url = fh.read()
##
##    return url.strip()
##
##def add_user(project_path, root_password, login, password, email):
##    url = get_server_url(project_path)
##    with DevpiClient(url, 'root', root_password) as devpi:
##        devpi.create_user(login, password=password, email=email)
##
##def update_user(project_path, root_password, login, password=None, email=None):
##    kwargs = {}
##    if password is not None:
##        kwargs['password'] = password
##    if email is not None:
##        kwargs['email'] = email
##    if not kwargs:
##        raise ValueError('No password or email given, nothing to update')
##
##    url = get_server_url(project_path)
##    with DevpiClient(url, 'root', root_password) as devpi:
##        devpi.modify_user(login, **kwargs)
##
##def list_users(project_path):
##    url = get_server_url(project_path)
##    with DevpiClient(url) as devpi:
##        return devpi.list_users()
##
##def list_indices(project_path, user=None):
##    url = get_server_url(project_path)
##    with DevpiClient(url) as devpi:
##        indices_names = devpi.list_indices(user)
##    return indices_names
##
##def create_proj_index(project_path, root_password):
##    url = get_server_url(project_path)
##    index = 'root/PROJ'
##    with DevpiClient(url, 'root', root_password) as devpi:
##        devpi.create_index(index, volatile=False, acl_upload=':ANONYMOUS:')
##
##def create_sub_index(project_path, root_password, user_name, index_name, volatile=True, *acl_upload):
##    '''
##    Create an new index. 
##    All *acl_upload must be user logins or ':ANONYMOUS:'. Defaults to ':ANONYMOUS:'
##    '''
##    url = get_server_url(project_path)
##    index = '{}/{}'.format(user_name, index_name)
##    bases = 'root/PROJ'
##    acl_upload_str = acl_upload and ','.join(acl_upload) or ':ANONYMOUS:'
##    with DevpiClient(url, 'root', root_password) as devpi:
##        devpi.create_index(
##            index, 
##            bases=bases,
##            volatile=volatile, 
##            acl_upload=acl_upload_str
##        )
##
##def list_index_packages(project_path, index=None):
##    '''
##    Returns a list of all packages inside this index.
##    If index is None, the default index is used.
##    '''
##    url = get_server_url(project_path)
##    index_name = index or 'root/PROJ'
##    with DevpiClient(url) as devpi:
##        devpi.use(index_name)
##        package_names = devpi.list()
##
##    return package_names
