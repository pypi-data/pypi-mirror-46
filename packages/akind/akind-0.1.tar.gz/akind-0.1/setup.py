from setuptools import setup

setup(
    name='akind',
    version='0.1',
    py_modules=['akind'],
    install_requires=[
        'img2pdf'
    ],
    entry_points='''
        [console_scripts]
        akind=akind:main
    ''',
)
