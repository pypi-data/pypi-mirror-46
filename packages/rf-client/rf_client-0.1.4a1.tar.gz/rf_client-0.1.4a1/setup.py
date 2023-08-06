from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()


setup(name='rf_client',
      version='0.1.4a1',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='Python Red Forester async client',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ],
      url='https://redforester.com',
      author='Red Forester',
      author_email='tech@redforester.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'aiohttp ~= 3.4',
          'ujson ~= 1.35',
          'python-dateutil ~= 2.7'
      ],
      include_package_data=True,
      zip_safe=False)
