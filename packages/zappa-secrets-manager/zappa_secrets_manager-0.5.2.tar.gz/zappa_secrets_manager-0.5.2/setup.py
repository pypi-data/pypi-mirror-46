import os

from setuptools import setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'zappa_secrets_manager', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(name='zappa_secrets_manager',
      version=about['__version__'],
      description='Enables seamless zappa integration with AWS Secrets '
                  'Manager while still allowing local development via '
                  'environment variables',
      long_description=readme,
      author='AgileTek Engineering',
      author_email='',
      license='MIT',
      packages=['zappa_secrets_manager', ],
      install_requires=['python-dotenv', 'boto3',],
      include_package_data=True,
      zip_safe=False)
