import tempfile
import shutil
import os
import sys
from pathlib import Path

NAME = 'angreal_meeting_minutes'
DESCRIPTION='An angreal template for meeting minutes'
LONG_DESCRIPTION=''''''
AUTHOR='dylanbstorey'
AUTHOR_EMAIL='dylan.storey@gmail.com'
URL='https://gitlab.com/angreal/meeting-minutes'
FILES_TO_COPY = [
    "cookiecutter.json",
    "{{cookiecutter.name}}"
    ]



## SHOULDN'T NEED TO GO BELOW THIS LINE"

def generate_data_files(*args):
    """
    generate data_files parameter for setup tools

    takes files and directories to be added.

    :param args:
    :return:
    """


    sys_exe = Path(sys.executable)
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

def setup():
    """
    This feels hacky but it works so ... revisit later.
    :return:
    """
    import setuptools

    #patch setuptools so we can import w/o executing
    ori_setup = setuptools.setup
    setuptools.setup = lambda *a, **k: 0


    TEMP = tempfile.gettempdir()


    for f in generate_data_files(*FILES_TO_COPY):
        dst = os.path.join(TEMP,f[0])
        src = os.path.join(sys.prefix,NAME,f[1][0])
        os.makedirs(dst,exist_ok=True)
        shutil.copy(src, dst)



