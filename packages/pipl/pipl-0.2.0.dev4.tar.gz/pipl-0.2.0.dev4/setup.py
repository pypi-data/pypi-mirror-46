
import os
import sys
from setuptools import setup, find_packages


# (
#    (Major, Minor, [Micros]),
#    [(releaselevel, serial)],
# )
#__version_info__ = ((1, 0, 0),)
#__version_info__ = ((1, 0, 0),(rc,))
#__version_info__ = ((1, 0, 0),(rc,1))
__version_info__ = ((0, 2, 0), ('dev', 4))


readme = os.path.normpath(os.path.join(__file__, '..', 'README.md'))
with open(readme, 'r') as fh:
    long_description = fh.read()

# long_description += '\n\n'
# changelog = os.path.normpath(os.path.join(__file__, '..', 'CHANGELOG.md'))
# with open(changelog, 'r') as fh:
#     long_description += fh.read()


def get_version():
    global __version_info__
    return (
        '.'.join(str(x) for x in __version_info__[0])
        + ''.join(str(x) for x in __version_info__[1])
    )

setup(
    name='pipl',
    version=get_version(),
    description='Package Index PipeLine',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/open-minds-group/pipl',
    author='Damien "dee" Coureau',
    author_email='dee909@gmail.com',
    license='LGPLv3+',
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',

        'Topic :: Desktop Environment :: File Managers',

        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    ],
    keywords='pipeline dataflow dependency asset',
    install_requires=[
        'click',
        'semantic_version',
        'devpi-server',
        'devpi-client',
        'devpi-plumber',

    ],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
    #packages=find_packages('src'),
    packages=['pipl'],
    package_dir={'': 'src'},
    package_data={
        #'': ['*.css', '*.png', '*.svg', '*.gif'],
    },
    entry_points = {
        'console_scripts': ['pipl=pipl.main:main'],
    }
)
