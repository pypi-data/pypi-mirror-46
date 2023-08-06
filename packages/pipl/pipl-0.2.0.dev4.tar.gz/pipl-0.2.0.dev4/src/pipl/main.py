
import os
import getpass

import click

from . import autopack, packl, project


@click.group()
def pipl():
    pass

#
#   PROJECT
#

@pipl.group()
def proj():
    pass

@proj.command('create')
@click.argument('path')
def new_project(path):
    '''
    Creates a new project at path
    '''
    click.echo(
        "Create project at {!r}".format(
            path
        )
    )
    project.Project.create_project(path)

@proj.command('start')
@click.argument(
    'project-path', default='.', 
)
def start_server(project_path='.'):
    '''
    Start project's server in **foreground**.
    '''
    proj = project.Project.from_path(project_path)
    click.echo('Staring server for "{}"'.format(proj.path()))
    proj.start_server()

#
#   PROJECT USERS
#


@proj.group()
def user():
    '''
    Project users administration.
    '''
    pass

@user.command('list')
@click.argument(
    'project-path', default='.', 
)
def list_users(project_path='.'):
    '''
    List the users in the project.
    '''
    proj = project.Project.from_path(project_path)
    with proj.connected():
        users = proj.list_users()
        if users:
            click.echo(
                'Found {} user(s) in project {}:'.format(
                    len(users), proj.path()
                )
            )
            for user in users:
                click.echo('{:>10}'.format(user))
        else:
            click.echo(
                'Found no user in project {}'.format(proj.path())
            )
            
@user.command('add')
@click.argument('root_password')
@click.argument('login')
@click.argument('password')
@click.argument('email')
@click.argument('project_path', default='.')
def add_user(root_password, login, password, email, project_path='.'):
    '''
    Add a user to the project.
    '''
    proj = project.Project.from_path(project_path)
    with proj.connected('root', root_password):
        proj.add_user(
            login, 
            password,
            email,
        )

@user.command('set')
@click.argument('root_password')
@click.argument('login')
@click.argument('project_path', default='.')
@click.option('-p', '--password', default=None, help='set user password')
@click.option('-e', '--email', default=None, help='set user email')
def set_user(root_password, login, password=None, email=None, project_path='.'):
    '''
    Update the given user password or email.
    '''
    proj = project.Project.from_path(project_path)
    with proj.connected('root', root_password):
        proj.update_user(
            login, 
            password,
            email,
        )

#
#   PROJECT INDEXES
#

@proj.group()
def index():
    '''
    Project indexes administration.
    '''

@index.command('list-indexes')
@click.argument('project-path', default='.')
def list_indexes(project_path='.'):
    '''
    List the indexes in the project.
    '''
    proj = project.Project.from_path(project_path)
    with proj.connected():
        names = proj.list_indices()
        if names:
            click.echo(
                'Found {} Index(es) in project {}:'.format(
                    len(names), proj.path()
                )
            )
            for name in names:
                click.echo('{:>20}'.format(name))
        else:
            click.echo(
                'Found no index in project {}'.format(
                    proj.path()
                )
            )

@index.command('create-default')
@click.argument('root_password')
@click.argument('project-path', default='.')
def create_default_index(root_password, project_path='.'):
    '''
    Create the project's default index (root/PROJ).
    '''
    proj = project.Project.from_path(project_path)
    click.echo(
        'Creating default project index for "{}"'.format(
            project_path
        )
    )
    with proj.connected('root', root_password):
        proj.create_proj_index()

@index.command('create-sub')
@click.argument('root_password')
@click.argument('index_name')
@click.argument('project-path', default='.')
def create_sub_index(
    root_password, index_name, project_path='.'
):
    '''
    Create a volatile index with the default one as base.
    '''
    proj = project.Project.from_path(project_path)
    user_name = 'root'
    click.echo(
        'Creating volatile public index {}/{} for "{}"'.format(
            user_name, index_name, proj.path()
        )
    )
    with proj.connected('root', root_password):
        proj.create_sub_index(
            user_name, index_name,
            True, # volatile
            ':ANONYMOUS:', # acl_upload
        )

@index.command('list')
@click.argument('project-path', default='.')
@click.option('-i', '--index_name', default=None)
def list_index_packages(index_name=None, project_path='.'):
    '''
    List packages inside the index (defaults to "root/PROJ")
    '''
    proj  = project.Project.from_path(project_path)
    with proj.connected():
        names = proj.list_packages(index_name)
        click.echo(
            'Found {} Package(s) in index {} of project {}:'.format(
                len(names),
                index_name or '*default*',
                proj.path()
            )
        )
        for name in names:
            click.echo('{:>30}'.format(name))



#
#
#   WORKSPACES
#
#

@pipl.group()
def work():
    pass

@work.command('create-area')
@click.argument('workarea_path')
@click.argument('project-path', default='.')
def create_workarea(workarea_path, project_path='.'):
    '''
    Create a workarea for the project.
    '''
    proj = project.Project.from_path(project_path)
    click.echo(
        'Creating workarea "{}" in project "{}"'.format(
            workarea_path, proj.path()
        )
    )
    proj.create_workarea(workarea_path)
    
@work.command('create')
@click.argument('workspace_name')
@click.argument('workarea_path', default='.')
def create_workspace(workspace_name, workarea_path='.'):
    '''
    Create a new workspace in the workarea.

    If the workarea_path is not an absolute path, it must
    be the name of a workarea in the project.
    '''
    workarea = project.Workarea.from_path(workarea_path)
    click.echo(
        'Create workspace "{}" in area "{}"'.format(
            workspace_name, workarea_path
        )
    )
    workarea.create_workspace(workspace_name)

@work.command('shell')
@click.argument('workspace_path', default='.')
def workspace_shell(workspace_path='.'):
    '''
    Open a shell with this workspace's virtualenv
    '''
    workspace = project.Workspace.from_path(workspace_path)
    workspace.shell()


@work.command('py')
@click.argument('workspace_path', default='.')
def workspace_python(workspace_path='.'):
    '''
    Launch a python REPL with this workspace virtual env
    '''
    workspace = project.Workspace.from_path(workspace_path)
    workspace.python()

#
#
#   PACKLS (will replace 'pack' commands soon)
#
#

@pipl.group('packl')
def packl_cmds():
    pass

@packl_cmds.command('create')
@click.argument('name')
@click.option(
    '-p', '--workspace-path', default='.', 
    help='Override current path'
)
def create_packl(name, workspace_path='.'):
    '''
    Create a new packl.
    '''
    workspace_path = project.Workspace.find_workspace_path(workspace_path)
    click.echo(
        'Creating new packl "{}" in workspace "{}"'.format(
            name, workspace_path
        )
    )
    packl.create(workspace_path, name)

@packl_cmds.command('show')
@click.option(
    '-p', '--packl-path', default='.', 
    help='Override current path'
)
def show_packl(packl_path='.'):
    '''
    Show setup for the given packl.
    '''
    packl_path = packl.find_packl_path(packl_path)
    packl.show_setup(packl_path)

@packl_cmds.command('add')
@click.argument('dependency_name')
@click.argument('comments')
@click.option(
    '-x', '--as-extra', default=None,
    help='Optional extra-require name'
)
@click.option(
    '-p', '--packl-path', default='.', 
    help='Override current path'
)
def add_dependency(dependency_name, comments, as_extra=None, packl_path='.'):
    '''
    Adds a dependency to this packl.

    The dependency will be installed first.
    '''
    packl_path = packl.find_packl_path(packl_path)
    packl.add_dependency(packl_path, dependency_name, comments, as_extra)

@packl_cmds.group()
def bump():
    '''
    Version number bumping.
    '''
    pass

@bump.command('major')
@click.argument('comment', default=None)
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def bump_version_major(comment=None, package_path='.'):
    '''Major version bump'''
    packl.bump_version_major(packl_path)

@bump.command('minor')
@click.argument('comment', default=None)
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def bump_version_minor(comment=None, package_path='.'):
    '''Minor version bump'''
    setup_filename = autopack.find_package_setup_file(package_path)
    autopack.bump_version_minor(setup_filename)

@bump.command('patch')
@click.argument('comment', default=None)
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def bump_version_patch(comment=None, package_path='.'):
    '''Patch version bump'''
    setup_filename = autopack.find_package_setup_file(package_path)
    autopack.bump_version_patch(setup_filename)


@packl_cmds.command('upload')
@click.argument('password')
@click.option('-u', '--user', default=None)
@click.option('-i', '--index-name', default=None)
@click.option(
    '-p', '--packl-path', default='.', 
    help='Override current path'
)
def upload_packl(
    password, user=None,
    index_name=None, packl_path='.'
):
    '''
    Build and upload a packl.

    index-name defaults to 'root/PROJ'.
    user defaults to the current user.
    packl_path defaults to the current directory.

    '''
    user = user or getpass.getuser()
    packl_path = packl.find_packl_path(packl_path)
    packl.upload(
        packl_path, user, password, index_name
    )


def main():
    pipl()

if __name__ == '__main__':
    main()
