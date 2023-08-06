import os
import sys
import re
import textwrap
import glob
import setuptools

min_numpy_version = '1.2.0'

# Some functions for showing errors and warnings.
def _print_admonition(kind, head, body):
    tw = textwrap.TextWrapper(
        initial_indent='   ', subsequent_indent='   ')

    print(".. %s:: %s" % (kind.upper(), head))
    for line in tw.wrap(body):
        print(line)

def exit_with_error(head, body=''):
    _print_admonition('error', head, body)
    sys.exit(1)

def print_warning(head, body=''):
    _print_admonition('warning', head, body)

# Check for Python
if not (sys.version_info[0] >= 2 and sys.version_info[1] >= 6):
    exit_with_error("You need Python 2.6.x or Python 2.7.x to install MDKit package!")

if (sys.version_info[0] >= 3 and sys.version_info[1] >= 0):
    exit_with_error("You need Python 2.6.x or Python 2.7.x to install MDKit package!")

# Check for required Python packages
def check_import(pkgname, pkgver):
    try:
        mod = __import__(pkgname)
    except ImportError:
        exit_with_error("You need %(pkgname)s %(pkgver)s or greater to run MDKit!"
            % {'pkgname': pkgname, 'pkgver': pkgver} )
    else:
        if len(mod.__version__)>6:
            mod_ver = mod.__version__[:6]
        else:
            mod_ver = mod.__version__

        def mycmp(version1, version2):
            def normalize(v):
                return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
            return cmp(normalize(version1), normalize(version2))

        # code for mycmp() taken from http://stackoverflow.com/questions/1714027/version-number-comparison
        if mycmp(mod_ver,pkgver) < 0:
            exit_with_error("You need %(pkgname)s %(pkgver)s or greater to install this package!"
                % {'pkgname': pkgname, 'pkgver': pkgver})
    print(( "* Found %(pkgname)s %(pkgver)s package installed."
            % {'pkgname': pkgname, 'pkgver': mod.__version__} ))
    globals()[pkgname] = mod

setuptools.setup(name='mdkit',
    version="0.0.9",
    packages=['mdkit', 'mdkit.amber', 'mdkit.namd', 'mdkit.utility'],
    package_data = {'mdkit.amber': ['PROTON_INFO', 'atomic_ions.cmd']},
    scripts = ['bin/prepare_md.py', 'bin/run_mmpbsa.py', 'bin/cluster_w_amber.py', 'bin/minimize_w_amber.py', 'bin/pdb2mol2'],
    install_requires = ['networkx==2.2', 'numpy==1.8.0'],
    license='LICENSE.txt',
    description='Tools to prepare and analyze MD simulations conducted with popular MD packages',
    long_description=open('README.md').read(),
)
