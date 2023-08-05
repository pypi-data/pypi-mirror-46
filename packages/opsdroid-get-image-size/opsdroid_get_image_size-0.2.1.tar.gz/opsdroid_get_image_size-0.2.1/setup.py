import os
import codecs
from setuptools import setup
import versioneer


def read_long_description():
    long_desc = []
    with codecs.open('README.rst', 'r', 'utf8') as longdesc:
        long_desc.append(longdesc.read())
    if os.path.exists("HISTORY.rst"):
        with codecs.open('HISTORY.rst', 'r', 'utf8') as history:
            long_desc.append(history.read())
    return u'\n\n'.join(long_desc)

LONG_DESCRIPTION = read_long_description()

setup(
    name='opsdroid_get_image_size',
    url='https://github.com/opsdroid/image_size',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=LONG_DESCRIPTION,
    author='github.com/scardine',
    author_email=' ',
    license='MIT',
    py_modules=['get_image_size'],
    entry_points={
        'console_scripts': [
            'get-image-size = get_image_size:main',
            ],
    },
)
