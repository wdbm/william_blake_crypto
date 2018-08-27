"""
################################################################################
#                                                                              #
# william_blake_crypto                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# The program is a Python cryptography library.                                #
#                                                                              #
# copyright (C) 2018 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

import sys
if sys.version_info[0] <= 2:
    print("Python >2 required")
    sys.exit(1)
import getpass
import logging
if sys.version_info[0] <= 2:
    from pathlib2 import Path
else:
    from pathlib import Path
import yaml

from cryptography.fernet import Fernet
import technicolor

name        = "william_blake_crypto"
__version__ = "2018-08-27T2215Z"

log = logging.getLogger(name)
log.addHandler(technicolor.ColorisingStreamHandler())
log.setLevel(logging.INFO)
log.debug(name + " " + __version__)

global _key
_key = None

def generate_key():
    return Fernet.generate_key()

def input_key(prompt="enter key: "):
    global _key
    _key = getpass.getpass(prompt=prompt).encode("utf8")

def load_key(path_key="~/.config/william_blake_crypto/key"):
    """
    Load a key to globals. This function is intended for development, not for production.
    """
    path_key = Path(path_key).expanduser()
    if not path_key.exists():
        log.error("{path} not found".format(path = path_key))
        return False
    else:
        with open(str(path_key), "r") as _file:
            contents_file = _file.read()
        key = contents_file.strip("\n")
        global _key
        _key = key.encode("utf8")

def encrypt_yaml(key=None, content=None):
    """
    Encrypt a YAML object to an encrypted token.
    """
    if not key:
        global _key
        key = _key
    if not key:
        log.error("key not set")
        return False
    f = Fernet(key)
    token = f.encrypt(yaml.dump(content).encode("utf8"))
    return token

def decrypt_yaml(key=None, token=None):
    """
    Decrypt an encrypted token to a YAML object.
    """
    if not key:
        global _key
        key = _key
    if not key:
        log.error("key not set")
        return False
    f = Fernet(key)
    content = yaml.load(f.decrypt(token))
    return content

def yaml_to_encrypted_file(key=None, filepath=None, content=None):
    """
    Encrypt a YAML object to an encrypted token and save it to a file.
    """
    token = encrypt_yaml(key=key, content=content)
    with open(str(filepath), "w") as _file:
        _file.write(token.decode("utf8"))
        _file.write("\n")

def yaml_file_to_encrypted_file(key=None, filepath_yaml=None, filepath_encrypted=None):
    filepath_yaml = Path(filepath_yaml).expanduser()
    if not filepath_yaml.exists():
        log.error("{filepath} not found".format(filepath = filepath_yaml))
        return False
    else:
        with open(str(filepath_yaml), "r") as _file:
            content = yaml.load(_file)
    yaml_to_encrypted_file(key=key, filepath=filepath_encrypted, content=content)

def encrypted_file_to_yaml(key=None, filepath=None):
    """
    Read an encrypted token from a file and decrypt it to a YAML object.
    """
    filepath = Path(filepath).expanduser()
    if not filepath.exists():
        log.error("{filepath} not found".format(filepath = filepath))
        return False
    with open(str(filepath), "r") as _file:
        contents_file = _file.read()
    token = contents_file.strip("\n").encode("utf8")
    content = decrypt_yaml(key=key, token=token)
    return content

def encrypted_file_to_yaml_file(key=None, filepath_yaml=None, filepath_encrypted=None):
    """
    Convert an encrypted file to a decrypted YAML file.
    """
    filepath_encrypted = Path(filepath_encrypted).expanduser()
    if not filepath_encrypted.exists():
        log.error("{filepath} not found".format(filepath = filepath_encrypted))
        return False
    content = encrypted_file_to_yaml(key=key, filepath=filepath_encrypted)
    with open(filepath_yaml, "w") as _file:
        yaml.dump(content, _file)
