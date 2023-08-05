from setuptools import setup


setup(
    name='setuptools-git-version-cc',
    version='1.0.0',
    url='https://github.com/rokubun/setuptools-git-version-cc',
    author='Rokubun',
    author_email='info@rokubun.cat',
    description='Automatically set package version from Git using Conventional Commit standard.',
    license='http://opensource.org/licenses/MIT',
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    py_modules=['setuptools_git_version_cc'],
    install_requires=[
        'setuptools >= 8.0',
    ],
    entry_points="""
        [console_scripts]
        get_version = setuptools_git_version_cc:get_git_version
    """,
)
