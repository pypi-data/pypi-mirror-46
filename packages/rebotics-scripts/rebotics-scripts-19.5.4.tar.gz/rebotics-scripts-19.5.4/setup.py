"""
Collection of scripts for rebotics
"""
from setuptools import setup

__VERSION__ = '19.5.4'

requirements = [
    'click>=7.0',
    'ffmpeg-python==0.1.17',
    'numpy==1.16.2',
    'requests==2.21.0',
    'PySocks!=1.5.7,>=1.5.6',
    'requests[socks]',
    'requests-toolbelt==0.9.1',
    'tqdm==4.31.1',
    'xlrd==1.2.0',
    'six==1.12.0',
    'pytz',
    'ptable',
    'python-dateutil',
    'humanize',
]

setup(
    name='rebotics-scripts',
    version=__VERSION__,
    url='http://retechlabs.com/',
    license='BSD',
    author='Malik Sulaimanov',
    author_email='malik@retechlabs.com',
    description='Collection of scripts for rebotics',
    long_description=__doc__,
    long_description_content_type='text/markdown',
    packages=[
        'sdk',
        'sdk.providers',
        'scripts',
    ],
    package_dir={
        '': '.',
        'sdk': 'sdk',
        'sdk.providers': 'sdk/providers',
    },
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'rebotics = scripts.cli:main',
            'admin = scripts.admin_api_client:api',
            'admin-api = scripts.admin_api_client:api',
            'retailer = scripts.retailer_api_client:api',
            'retailer-api = scripts.retailer_api_client:api',
            'dataset-api = scripts.dataset_api_client:api',
            'dataset = scripts.dataset_api_client:api',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
