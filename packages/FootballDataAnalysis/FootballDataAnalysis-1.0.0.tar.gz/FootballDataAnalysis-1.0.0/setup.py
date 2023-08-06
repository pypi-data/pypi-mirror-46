from distutils.core import setup

setup(
    name='FootballDataAnalysis',
    version='1.0.0',
    author='Bohdan Yatskiv',
    author_email='yatskiv.b@ucu.edu.ua',
    url='https://github.com/yatskivbohdan/Football_data_analisys_project',
    description='this package allows to get detailed team statistics from top 5 football leagues',
    keywords=['football', 'football statistics'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved ",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment"
        ],
    scripts=['main.py', 'updater.py']
)
