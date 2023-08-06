import sys
import setuptools
import os

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
VERSION = open(os.path.join('VERSION')).read().strip()

py_version_tag = '-%s.%s'.format(sys.version_info[:2])

if not sys.version_info >= (3, 0):
    print('Python 3 is required', file=sys.stderr)
    exit(1)


def generate_data_files(*args):
    """
    generate data_files parameter for setup tools

    takes files and directories to be added.

    :param args:
    :return:
    """

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
            data_files.append( (NAME, [path]) )
        elif os.path.isdir(path):
            for p in package_files(path):
                data_files.append( ( os.path.dirname(os.path.join(NAME,p)), [p]) )

    import sys
    print(data_files, file=sys.stderr)

    return data_files



setuptools.setup(
    name=NAME,
    description='An angreal template for taking meeting minutes',
    long_description='''''',
    url='https://gitlab.com/angreal/meeting-minutes',
    author='dylanbstorey',
    author_email='dylan.storey@gmail.com',
    license='GPLv3',
    zip_safe=False,
    version=VERSION,
    python_requires='>=3',
    data_files=generate_data_files("cookiecutter.json","{{cookiecutter.name}}")
)
