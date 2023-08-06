import sys
import setuptools
from setuptools.command.install import install
import tempfile
from pathlib import Path
import os
from shutil import copy2,rmtree

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

# noinspection PyProtectedMember
try:
    from pip._internal.download import PipSession
except:
    from pip.download import PipSession

NAME = 'angreal-meeting-minutes'
DESCRIPTION='An angreal template for meeting minutes'
LONG_DESCRIPTION=''''''
AUTHOR='dylanbstorey'
AUTHOR_EMAIL='dylan.storey@gmail.com'
URL='https://gitlab.com/angreal/meeting-minutes'
files_to_copy = [
    "cookiecutter.json",
    "{{cookiecutter.name}}"
    ]

VERSION = open(os.path.join('VERSION')).read().strip()
py_version_tag = '-%s.%s'.format(sys.version_info[:2])
if not sys.version_info >= (3, 0):
    print('Python 3 is required', file=sys.stderr)
    exit(1)





# SHOULDNT NEED TO GO BELOW THIS LINE

def generate_data_files(*args):
    """
    generate data_files parameter for setup tools

    takes files and directories to be added.

    :param args:
    :return:
    """
    sys_exe = Path(sys.executable)
    sys_root = sys_exe.anchor or sys_exe.anchor
    temp_drive = tempfile.gettempdir()
    data_files = []

    def package_files(directory):
        """
        get all the files in a directory

        :param directory:
        :return:
        """
        paths = []
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join(path, filename))
        return paths

    for path in args:
        if os.path.isfile(path):
            data_files.append( ( NAME , [path]) )
        elif os.path.isdir(path):
            for p in package_files(path):
                data_files.append( ( os.path.dirname(os.path.join(NAME,p)), [p]) )



    return data_files

class PostInstallCommand(install):
    """
    Over ride the install command to copy files to a tmpfolder
    """
    def run(self):
        paths = generate_data_files(*files_to_copy)
        tempdir = tempfile.gettempdir()
        for p in paths:
            dst_dir = os.path.dirname(os.path.join(tempdir,NAME,p[1][0]))
            os.makedirs(dst_dir,exist_ok=True)
            copy2(p[1][0],dst_dir)
        install.run(self)



setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='GPLv3',
    zip_safe=False,
    version=VERSION,
    python_requires='>=3',
    data_files=generate_data_files(*files_to_copy),
    cmdclass={'install': PostInstallCommand},
)