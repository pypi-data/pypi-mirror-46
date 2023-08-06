import sys
import setuptools
import os

from angreal_meeting_minutes import NAME,DESCRIPTION,LONG_DESCRIPTION,AUTHOR,AUTHOR_EMAIL,URL,FILES_TO_COPY,generate_data_files


try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

# noinspection PyProtectedMember
try:
    from pip._internal.download import PipSession
except:
    from pip.download import PipSession


VERSION = open(os.path.join('VERSION')).read().strip()
py_version_tag = '-%s.%s'.format(sys.version_info[:2])
if not sys.version_info >= (3, 0):
    print('Python 3 is required', file=sys.stderr)
    exit(1)





# SHOULDNT NEED TO GO BELOW THIS LINE




setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    py_modules=['angreal_meeting_minutes'],
    license='GPLv3',
    zip_safe=False,
    version=VERSION,
    python_requires='>=3',
    data_files=generate_data_files(*FILES_TO_COPY),
)