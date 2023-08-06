import setuptools


long_description = """
# test.helper.gae

Class for autotests GoogleAppEngine python apps
"""

setuptools.setup(
    name = 'tester_gae',
    version = '1.3.0',
    author = 'Vitaly Bogomolov',
    author_email = 'mail@vitaly-bogomolov.ru',
    description = 'Class for autotests GoogleAppEngine python apps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/vb64/test.helper.gae',
    packages = ['tester_gae'],
    download_url = 'https://github.com/vb64/test.helper.gae/archive/v1.3.tar.gz',
    keywords = ['python', 'Python27', 'GAE', 'GoogleAppEngine', 'unittest'],
    classifiers = [
      "Programming Language :: Python :: 2.7",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    install_requires = [
      'Pillow',
      'gae_installer>=1.9.54'
    ]
)
