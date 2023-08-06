from __future__ import print_function

import os
import getpass
import time

class DirNotFoundError(ValueError):
    pass

def find_parent_dir(path_name, from_path, sentinel_name):
    '''
    Return the ancestor folder of from_path that contains
    a file named sentinel_name.

    The path_name is a descriptive name of the looked up
    path to use in logs
    '''
    print(
        'Resolving {} path from {}'.format(
            path_name, from_path
        )
    )
    current = os.path.abspath(from_path)
    while current:
        if not os.path.exists(current):
            raise DirNotFoundError(
                'Could not find the {} path under {!r} '
                '({!r} does not exists)'.format(
                    path_name, from_path, current
                )
            )
        sentinel = os.path.join(current, sentinel_name)
        if os.path.exists(sentinel):
            print(
                'Found {} at {}'.format(
                    path_name, current
                )
            )
            return current
        dirname = os.path.dirname(current)
        if dirname == current:
            # cases like dirname == "D:\"
            break
        current = dirname
    raise DirNotFoundError(
        'Could not find the {} path under {!r}'.format(
            path_name, from_path
        )
    )

def get_user_and_ctime():
    return getpass.getuser(), time.ctime()

