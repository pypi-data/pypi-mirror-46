from setuptools import setup
with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='ApiLeagueOfLegends',
    packages=['', 'league_of_legends_api', 'league_of_legends_api/Api', 'league_of_legends_api/Database',
              'league_of_legends_api/Tools'],
    package_dir={'': 'src'},
    version='0.06',
    license='MIT',
    description='Wrapper for the League of Legends Api',
    long_description=long_description,
    author='Lukas Mahr',
    author_email='LukasMahr@gmx.de',
    url='https://github.com/Lkgsr/League-of-Legends-Api',
    keywords=['API', 'Api', 'api', 'LeagueOfLegends', 'LeagueofLegends', 'league-of-legends', 'lol',
              'League-of-Legends', 'League-Of-Legends'],
    install_requires=[
        'requests',
        'SQLAlchemy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
)
