import setuptools
import os
import sys
import setuptools.command.build_py
import typing
from pathlib import Path

def maybe_cythonize(exts: typing.List[setuptools.Extension]):
    do_it = False
    for ext in exts:
        for i in ext.sources:
            c = Path(i)
            pyx = Path(i.replace('.c', '.pyx'))
            if pyx.exists() and ((not c.exists()) or pyx.stat().st_mtime > c.stat().st_mtime):
                ext.sources.remove(i)
                ext.sources.append(str(pyx))
                do_it = True

    if do_it:
        from Cython.Build import cythonize
        exts = cythonize(exts)
    return exts


class DeannotateAndBuild(setuptools.command.build_py.build_py):

    def build_packages(self):
        super().build_packages()
        if sys.version_info[0] == 3 and sys.version_info[1] < 6:
            print("Installing for older python, trying to clean up annotations...", file=sys.stderr)
            if sys.platform.startswith('darwin'):
                sed_i = 'sed -i""'
            else:
                sed_i = 'sed -i'
            os.system(r'''set -x; cd %s; find . -name '*.py' | xargs -n1 %s 's@^\( *[a-zA-Z._]*\):.*=@\1 = @g' ''' % (self.build_lib, sed_i))


setuptools.setup(
    cmdclass={
        'build_py': DeannotateAndBuild,
    },
    name='debus',
    version='0.1.12.1',
    description='DBus wire protocol implementation',
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    author='Vladimir Shapranov',
    author_email='equidamoid@gmail.com',
    url='https://github.com/Equidamoid/debus',
    ext_modules=maybe_cythonize([setuptools.Extension('debus.marshalling', ["debus/marshalling.c"])]),
    packages=setuptools.find_packages(),
    install_requires=[
        'lxml',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ]

)
