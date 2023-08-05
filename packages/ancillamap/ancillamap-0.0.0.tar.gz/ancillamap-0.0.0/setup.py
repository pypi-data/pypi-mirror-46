from setuptools import setup, find_packages
import logging
logger = logging.getLogger(__name__)

name = 'ancillamap'
version = '0.0.0'

try:
    with open('README.md', 'r') as f:
        long_desc = f.read()
except:
    logger.warning('Could not open README.md.  '
                   'long_description will be set to None.')
    long_desc = None

setup(
    name = name,
    packages = find_packages(),
    version = version,
    description = 'TODO',
    long_description = long_desc,
    long_description_content_type = 'text/markdown',
    author = 'Casey Duckering',
    #author_email = '',
    url = 'https://github.com/cduck/{}'.format(name),
    download_url = 'https://github.com/cduck/{}/archive/{}.tar.gz'
                   .format(name, version),
    keywords = ['quantum computing'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: IPython',
        'Framework :: Jupyter',
    ],
    install_requires = [
        'sortedcontainers',
        'numpy',
        'scipy',
        'networkx',
        'cirq==0.4.*',
    ],
    extras_require = {
        'dev': [
            'twine',
        ],
        'vis': [
            'matplotlib',
            'drawSvg',
            'latextools',
            'imageio',
            'imageio-ffmpeg',
        ]
    },
)

