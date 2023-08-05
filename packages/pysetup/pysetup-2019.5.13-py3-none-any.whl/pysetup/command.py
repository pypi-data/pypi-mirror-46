from pathlib import Path
import shutil
import os


class Command:
    @classmethod
    def exec(cls, cmd='help', *args):
        """Execute command."""
        return getattr(cls(), cmd, Command.help)(*args)

    @staticmethod
    def create_setup(*args):
        """Create a setup.py file."""
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write('''import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Detail see: https://packaging.python.org/tutorials/packaging-projects/#creating-setup-pypip install -i https://test.pypi.org/simple/ pysetup
setuptools.setup(
    name='<package_name>',
    version='<version>',
    author='<author>',
    author_email='<author_email>',
    description='<description>',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='<url>',
    packages=setuptools.find_packages(exclude=('<directory_name>',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['<package_name>'],
    entry_points={
        'console_scripts': ['<command>=<package>.<filename>:<function>'],
    },
)
''')
        return 'Successfully!'

    @staticmethod
    def upload(*args):
        """Package the project and upload it to pypi."""
        if len(args) == 2: username, password = args
        else: return 'Error: please check the command (pysetup upload <username> <password>).'
        Command.package()
        result = os.system(f'twine upload -u {username} -p {password} dist/*')
        return 'Successfully!' if result == 0 else 'Failure!'

    @staticmethod
    def upload_test(*args):
        """Package the project and upload it to testpypi."""
        if len(args) == 2: username, password = args
        else: return 'Error: please check the command (pysetup upload_test <username> <password>).'
        Command.package()
        result = os.system(f'twine upload -u {username} -p {password} --repository-url https://test.pypi.org/legacy/ dist/*')
        return 'Successfully!' if result == 0 else 'Failure!'

    @staticmethod
    def help(*args):
        """View command list."""
        return '''Command list:
        create_setup --- Create a setup.py file.
        upload <username> <password> --- Upload to https://upload.pypi.org/legacy.
        upload_test <username> <password> --- Upload to https://test.pypi.org/legacy.
        help --- View command list.
        package --- Package the project(create build, dist, *.egg-info file).
        clear --- Clear packaged file(clear build, dist, *.egg-info file).
        '''

    @staticmethod
    def package(*args):
        """Package the project."""
        assert Path('setup.py').exists(), 'The setup.py not found.'
        if os.system('python setup.py sdist bdist_wheel') != 0:
            raise Exception('[Error] please check the setup.py file')
        return 'Successfully!'

    @staticmethod
    def clear(*args):
        """clear packaged files (build/dist/*.egg-info)."""
        for p in [Path('build'), Path('dist'), *Path.cwd().glob('*.egg-info')]:
            if p.exists(): shutil.rmtree(p)
        return 'Successfully!'
