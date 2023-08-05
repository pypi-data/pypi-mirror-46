from setuptools import setup

from carrot_mc import meta

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='carrot_mc',
    version=meta.VERSION,
    description='Command-line Minecraft mod manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Misza',
    author_email='misza@misza.net',
    url='https://github.com/Misza13/carrot',
    license='MIT',
    packages=['carrot_mc', 'carrot_mc.web_gui'],
    entry_points={
        'console_scripts': [
            'carrot = carrot_mc.cli:main'
        ]
    },
    install_requires=[
        'requests',
        'Flask',
        'Flask-SocketIO',
        'eventlet'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment'
    ],
    include_package_data=True,
    zip_safe=False
)