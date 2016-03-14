try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

desc = "A miniature Quora clone"

setup(
    name='Kingsmoot',
    author='Daniel Oliver King',
    author_email='daniel.oliver.king@gmail.com',
    requires=['nose', 'flask', 'flask_login', 'flask_bcrypt', 'flask_wtf', 'peewee'],
    scripts=[],
    description=desc
)
