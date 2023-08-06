from setuptools import setup
from distutils.core import setup




setup(name='sharedpy',
      version='0.0.106',
      url='https://pypi.python.org/pypi/sharedpy',
      author='bosco',
      author_email='no@email.com',
      install_requires=['Pillow', 'requests', 'django', 'ldap3', 'cchardet', 'requests_ntlm', 'django-ipware', 'cryptography', 'exrex',], # http://python-packaging.readthedocs.io/en/latest/dependencies.html
      packages=['sharedpy',
                'sharedpy.collection',
                'sharedpy.datetime',
                'sharedpy.django',
                'sharedpy.cryptography',
                'sharedpy.html',
                'sharedpy.io',
                'sharedpy.ldap',
                'sharedpy.misc',
                'sharedpy.net',
                'sharedpy.number',
                'sharedpy.pillow',
                'sharedpy.text',],)
