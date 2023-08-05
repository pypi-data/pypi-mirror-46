# PySetup
Pypi upload tool.

## Install
```
pip3 install pysetup --upgrade
```

## Usage
1. enter the project directory and open the command line interface.
2. input `pysetup create_setup` command to create a `setup.py` file.
3. modify the `setup.py` file information.
4. input `pysetup upload <username> <password>` to package the project and upload to pypi.

## Commands
- `pysetup help`: view command list.
- `pysetup create_setup`: create a setup.py file.
- `pysetup upload <username> <password>`: package the project and upload it to pypi (https://upload.pypi.org/legacy). note: please clear the old version packaged files before uploading.
- `pysetup upload_test <username> <password>`: package the project and upload it to testpypi (https://test.pypi.org/legacy). note: please clear the old version packaged files before uploading.
- `pysetup package`: package the project.
- `pysetup clear`: clear packaged files (build/dist/*.egg-info).
