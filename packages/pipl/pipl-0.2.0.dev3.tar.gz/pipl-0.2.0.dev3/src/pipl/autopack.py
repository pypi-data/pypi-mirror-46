'''

autopack
=========

A package that use package._setup to configure setuptools.setup()

the package to setup must be like:

.../package_name/
        setup.py            <- should contain only import autopack; autopack.setup()
        package_name/
            __init__.py
            _setup.py       <- used as a namespace for all setuptools.setup(kwargs)
            _use_reqs.py    <- must import all required products (packages)
            _edit_reqs.py   <- must import all required editors/builders (packages)

Usage:

    In your package's setup.py:
        from pypipipe.autopack import setup
        setup()

    This will discover the package or module named like the parent dir,
    then import the submodule _setup and use it as a namespace for
    setuptools.setup(__file__) kwargs.

    to manipulate the _setup content, edita by hand or use methods defined here:
    
    import my_package
    autopack.set_version(my_package, '1.0.1')
    autopack.add_classifier('Private ::')
    ...



OLD:

                                        A package that provides an API to create and manage packages.
                                        It uses setuptools under the hood.

                                        Restriction:

                                        metapack is not for python dev. It's just a hack.
                                        Most notably, it doesn't work with modules.

                                        Synopsis:

                                        import metapack

                                        # This will create an editable package with the default setup.py:
                                        package_dir = '/path/to/packages'
                                        package = metapack.create_package(package_dir, package_name)

                                        # Now you can configure some aspects of the package:
                                        package = metapack.get_packate(package_dir, package_name)
                                        package.set_auto_version_incr(0,0,1)
                                        package.set_description('This package is awesome')
                                        package.set_long_description('This package is awesome', content_type="text/markdown")
                                        package.add_keywords('meta', 'pypipipe')

                                        import some_other_package
                                        package.add_required_package(some_other_package)
                                        package.add_require('yer_another_package')

                                        package.set_author('John Doe', 'john@doe.net')
                                        package.set_package_data('', ['*.css', '*.json'])

                                        # You can also query aspects of the package:
                                        print package.get_version()
                                        print package.get_description()
                                        print package.has_keyword('meta')
                                        print package.get_author()
                                        print package.get_author_email()

'''

import setuptools
import importlib
import os
import sys
import types
import time
import getpass

import semantic_version

def is_package_path(path):
    exists = os.path.exists(
        os.path.join(
            path, 'setup.py'
        )
    )
    return exists

def find_package_setup_file(from_path):
    print 'Resolving package path', from_path
    current = os.path.abspath(from_path)
    setup_py = 'setup.py'
    while current:
        this_setup_py = os.path.join(current, setup_py)
        if os.path.exists(this_setup_py):
            print 'Found package at', current
            return this_setup_py
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

def _list_imports(module_name):
    try:
        _reqs = importlib.import_module(module_name)
    except ImportError:
        return []

    names = [
        k for k, v in _reqs.__dict__.items()
        if (
            not k.startswith('_') 
            and isinstance(v, types.ModuleType)
        ) 
    ]
    return names

def get_use_reqs(package_name):
    return _list_imports(package_name+'._use_reqs')

def get_edit_reqs(package_name):
    return _list_imports(package_name+'._edit_reqs')

def get_pack_name(setup_filename):
    setup_filename = os.path.abspath(setup_filename)
    root = os.path.dirname(setup_filename)

    pack_name = os.path.basename(root)
    pack_name = pack_name.replace('-', '_')

    return pack_name

def _get_setup_module(setup_filename):
    '''
    Returns the _setup module given an autopack setup.py
    '''
    setup_filename = os.path.abspath(setup_filename)
    root = os.path.dirname(setup_filename)

    pack_name = get_pack_name(setup_filename)
    
    revert_path = sys.path[:]
    try:
        os.chdir(root)
        sys.path.insert(0, root)
        _setup = importlib.import_module(pack_name+'._setup')
    finally:
        sys.path[:] = revert_path

    return _setup

def _get_setup_attr(setup_filename, attr_name):
    setup_mod = _get_setup_module(setup_filename)
    return getattr(setup_mod, attr_name)

def _set_setup_attr(setup_filename, comment=None, **attr_name_to_value):
    content = [
        ''
        '# on {} by {}'.format(
            time.ctime(),
            getpass.getuser()
        )
    ]
    if comment is not None:
        content += ['# {}'.format(comment)]
    for attr_name, value in attr_name_to_value.items():
        content += [
            '{} = {!r}'.format(attr_name, value), 
            ''
        ]

    content = '\n'.join(content)

    setup_mod = _get_setup_module(setup_filename)
    path = setup_mod.__file__
    if path.endswith('.pyc'):
        path = path[:-1]

    with open(path, 'a') as fh:
        fh.write(content)
    print 'Updated', path

    reload(setup_mod)

def get_version(setup_filename):
    return _get_setup_attr(setup_filename, 'version')

def bump_version_major(setup_filename, comment=None):
    comment = comment or 'Major Version Bump'
    version = get_version(setup_filename)
    version = semantic_version.Version(version)
    version = version.next_major()
    _set_setup_attr(setup_filename, version=str(version), comment=comment)

def bump_version_minor(setup_filename, comment=None):
    print '?????', setup_filename
    comment = comment or 'Minor Version Bump'
    version = get_version(setup_filename)
    version = semantic_version.Version(version)
    version = version.next_minor()
    _set_setup_attr(setup_filename, version=str(version), comment=comment)

def bump_version_patch(setup_filename, comment=None):
    comment = comment or 'Patch Version Bump'
    version = get_version(setup_filename)
    version = semantic_version.Version(version)
    version = version.next_patch()
    _set_setup_attr(setup_filename, version=str(version), comment=comment)

def get_setup_kwargs(setup_filename):
    '''
    Return kwargs for setuptools.setup()
    '''
    _setup = _get_setup_module(setup_filename)
    kwargs = dict(
        [ 
            (k,v) 
            for k,v in _setup.__dict__.iteritems() 
            if not k.startswith('_') 
        ]
    )

    pack_name = get_pack_name(setup_filename)
    kwargs['name'] = pack_name
    kwargs['packages'] = [pack_name]

    use_reqs = get_use_reqs(pack_name)
    if use_reqs:
        kwargs['install_requires'] = use_reqs
    
    edit_reqs = get_edit_reqs(pack_name)
    if edit_reqs:
        kwargs['extras_requires'] = {'edit': edit_reqs}

    return kwargs

def show_setup(setup_filename):
    setup_kwargs = get_setup_kwargs(setup_filename)
    print 'Package {}:'.format(os.path.dirname(setup_filename))
    for k, v in sorted(setup_kwargs.items()):
        print '{:>20s}={!r}'.format(k, v)

def setup(setup_filename):
    setup_kwargs = get_setup_kwargs(setup_filename)
    setuptools.setup(**setup_kwargs)

def new_package(path, name):
    '''
    Creates a new package in path with the name name.

    The path folder must exist
    '''
    if not os.path.isdir(path):
        raise ValueError('Folder {!r} does not exists'.format(path))

    root = os.path.join(path, name)
    if os.path.exists(root):
        raise ValueError('Path {!r} already exists'.format(root))

    os.mkdir(root)
    setup_py = os.path.join(root, 'setup.py')
    with open(setup_py, 'w') as fh:
        fh.write(
            '\n'.join((
            'from {} import setup'.format(__name__),
            'setup(__file__)',
            ))
        )

    content_dir = os.path.join(root, name)
    os.mkdir(content_dir)

    init_py = os.path.join(content_dir, '__init__.py')
    with open(init_py, 'w') as fh:
        fh.write('"""\n{}\n"""\n\n'.format(name))
    
    _setup_py = os.path.join(content_dir, '_setup.py')
    with open(_setup_py, 'w') as fh:
        fh.write(
            '\n'.join((
                '"""\n{} setup file\n"""\n\n'.format(name),
                'version = "1.0.0"',
            ))
        )
        
    _user_reqs_py = os.path.join(content_dir, '_use_reqs.py')
    with open(_user_reqs_py, 'w') as fh:
        fh.write('"""\n{} usage requirement (add imports here)\n"""\n\n'.format(name))
        



