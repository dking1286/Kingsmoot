try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

desc = "A miniature Quora clone"

setup(
    name='Kingsmoot',
    author='Daniel Oliver King',
    author_email='daniel.oliver.king@gmail.com',
    install_requires=['nose', 'flask', 'peewee'],
    scripts=[],
    description=desc
)