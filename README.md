# william_blake_crypto

![](https://raw.githubusercontent.com/wdbm/william_blake_crypto/master/william_blake_crypto.png)

This package can

- convert a YAML object to an encrypted string object and back,
- convert a YAML file to an encrypted file and back,
- decrypt an encrypted file to a YAML object,
- and can generate, input and load a key for these purposes.

This package should be used in addition to other security measures.

Using this module, a key should be generated and saved securely. In production, a script using this package can request the key as a manual input and then can use the key to decrypt an encrypted file to a YAML object; for example, an encrypted configuration file. In development, a key can be generated and saved to a file such as `~/.config/william_blake_crypto/key` which can be loaded by the package without the need for manual input, but this is not a secure approach so should be used only for development, not production.

# future

Under consideration are ways to use time-based one-time passcodes (TOTP) in place of a static key, perhaps using [che_guevara_otp](https://github.com/wdbm/che_guevara_otp).

# setup

```Bash
pip install william_blake_crypto
```

# generate key

```Python
>>> import william_blake_crypto as wbc
>>> wbc.generate_key()
b'rojTAcN-Tjy6W43BUozbFIhIA2jq076KysjUj8l8N4E='
```

# input key (for production)

```Python
>>> import william_blake_crypto as wbc
>>> wbc.input_key()
key: 
>>> wbc._key
b'rojTAcN-Tjy6W43BUozbFIhIA2jq076KysjUj8l8N4E='
```

# load key (for development)

```Python
>>> import william_blake_crypto as wbc
>>> wbc.load_key()
>>> wbc._key
b'rojTAcN-Tjy6W43BUozbFIhIA2jq076KysjUj8l8N4E='
```

# encrypting and decrypting YAML objects

```Python
>>> import william_blake_crypto as wbc
>>> wbc.load_key()
>>> config = {"passcode": 12345}
>>> token = wbc.encrypt_yaml(content=config)
>>> token
b'gAAAAABbhGbVUVbbneKoz7wvV8aOF9K6r1hSNQvDexfAflIML33iyNa_Nf7Nm6g6syIXBkyANTHw3RlGMIsCgDligdts78a6VxrBaxbOIhGqSkzNtA5GDK4='
>>> wbc.decrypt_yaml(token=token)
{'passcode': 12345}
```

# converting a YAML file to an encrypted YAML file and decrypting it

```Bash
$ echo "{'passcode': 12345}" > test.yaml
```

```Python
>>> import william_blake_crypto as wbc
>>> wbc.load_key()
>>> wbc.yaml_file_to_encrypted_file(filepath_yaml="test.yaml", filepath_encrypted="test.cyaml")
```

```Bash
$ cat test.cyaml 
b'gAAAAABbhGzog6kLduLbflVx49jUD6WmIuRw8h0V7X25LrW6LnKjxbLN0pE7jMMeY9qaeGysjLsz-XA8EZ_LQVGslXhicpxLtt9K0CYFFYv2UZ3XEDt8oEI='
```

```Python
>>> import william_blake_crypto as wbc
>>> wbc.load_key()
>>> config = wbc.encrypted_file_to_yaml(filepath="test.cyaml")
>>> config
{'passcode': 12345}
```

# converting an encrypted YAML file to a YAML file

```Python
>>> import william_blake_crypto as wbc
>>> wbc.load_key()
>>> wbc.encrypted_file_to_yaml_file(filepath_yaml="test2.yaml", filepath_encrypted="test.cyaml")
```

```Bash
$ cat test2.yaml 
{passcode: 12345}
```
