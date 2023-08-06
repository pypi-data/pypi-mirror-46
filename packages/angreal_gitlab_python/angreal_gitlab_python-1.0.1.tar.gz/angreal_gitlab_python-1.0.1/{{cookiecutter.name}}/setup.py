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


VERSION = open(os.path.join('{{cookiecutter.name}}', 'VERSION')).read().strip()


py_version_tag = '-%s.%s'.format(sys.version_info[:2])
if not sys.version_info >= (3, 0):
    print('Python 3 is required', file=sys.stderr)
    exit(1)


def read_requirements(f):
    """
    Get requirements from a requirements file, will follow links.
    :param f:
    :return:
    """

    install_reqs = parse_requirements(f, session=PipSession())
    reqs = [str(ir.req) for ir in install_reqs]
    return reqs


setuptools.setup(
    name='{{cookiecutter.name}}',
    description='',
    long_description='''
    ''',
    url='https://gitlab.com/{{cookiecutter.namespace}}/{{cookiecutter.name}}',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.author_email}}',
    license='GPLv3',
    packages=setuptools.find_packages(),
    install_requires=read_requirements('requirements/requirements.txt'),
    zip_safe=False,
    version=VERSION,
    entry_points={
        'console_scripts': [
            '{{cookiecutter.name}}={{cookiecutter.name}}.cli:main'
        ]
    },
    python_requires='>=3',
    include_package_data=True,
    tests_require=['nose'],
    test_suite='nose.collector',
    extras_requires={
        'dev': read_requirements('requirements/dev.txt')
    }
)
