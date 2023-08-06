import os
from setuptools import setup, find_packages


def _read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__),
            fname)).read()
    except IOError:
        return ''


setup(
    name='m3-next',
    version='0.5.8',
    url='https://stash.bars-open.ru/projects/BUDG/repos/m3-next',
    license='MIT',
    author='BARS Group',
    author_email='bars@bars-open.ru',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description='Генерация интерфейса m3 в виде json-конфигурации ExtJS',
    install_requires=(
        'm3-core',
        'm3-ui',
    ),
    long_description=_read('README.md'),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ]
)

