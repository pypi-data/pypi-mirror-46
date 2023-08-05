import setuptools

setuptools.setup(
            name = 'cklass',
         version = '0.0.7',
         license = 'MIT',
          author = 'Artur Tamborski',
    author_email = 'tamborskiartur@gmail.com',
     description = 'Python module for loading config from files and env variables to class',
             url = 'https://github.com/arturtamborski/cklass',
    download_url = 'https://github.com/arturtamborski/cklass/archive/0.0.7.tar.gz',
        keywords = 'configuration config loader',
     classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ], long_description = open('readme.md').read(),
    long_description_content_type = 'text/markdown',
    zip_safe = False, include_package_data = True,
    packages = setuptools.find_packages())
