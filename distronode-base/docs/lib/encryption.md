# Encryption and Decryption

The `django-distronode-base` package includes built-in methods for encrypting and decrypting strings. These features are provided by the `distronode_base.lib.utils.encryption` module.

## Importing Encryption Utility
To use the encryption utility, you need to import the necessary components:
```python
from distronode_base.lib.utils.encryption import distronode_encryption
```

## Encryption
To encrypt a string, use the `encrypt_string` method provided by `distronode_encryption`.
- The `encrypt_string` method takes a text string and returns the encrypted version of the input string.
- If the input string is detected as already encrypted according to the module's algorithm, `encrypt_string` will return the input string unchanged.

## Decryption
To decrypt a string, use the `decrypt_string` method provided by `distronode_encryption`.
- The `decrypt_string` method takes in an encrypted string and returns the original text version of the encrypted string.
- If the input string is detected as not-encrypted according to the module's algorithm, `decrypt_string` will return the input string unchanged.

## Example Usage:
Below is a complete example that demonstrates both encryption and decryption of a string:

```python
from distronode_base.lib.utils.encryption import distronode_encryption

# Encrypting a string
my_secret = "keep_calm_and_run_distronode"
encrypted_string = distronode_encryption.encrypt_string(my_secret)
print(f"Encrypted: {encrypted_string}")

# Decrypting the string
decrypted_string = distronode_encryption.decrypt_string(encrypted_string)
print(f"Decrypted: {decrypted_string}")
```

This code will output:
```
Encrypted: <encrypted_value>
Decrypted: keep_calm_and_run_distronode
```
