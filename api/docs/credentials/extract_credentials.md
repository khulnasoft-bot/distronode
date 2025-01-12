Extracting Credential Values
============================

API stores a variety of secrets in the database that are either used for automation or are a result of automation. These secrets include:

- all secret fields of all credential types (passwords, secret keys, authentication tokens, secret cloud credentials)
- secret tokens and passwords for external services defined in API settings
- "password" type survey fields entries

To encrypt secret fields, API uses AES in CBC mode with a 256-bit key for encryption, PKCS7 padding, and HMAC using SHA256 for authentication.

If necessary, credentials and encrypted settings can be extracted using the API shell:

```python
$ api-manage shell_plus
>>> from api.main.utils import decrypt_field
>>> print(decrypt_field(Credential.objects.get(name="my private key"), "ssh_key_data")) # Example for a credential
>>> print(decrypt_field(Setting.objects.get(key='setting'), 'value')) # Example for a setting
```

If you are running a kubernetes based deployment, you can execute api-manage like this:
```bash
$ kubectl exec --stdin --tty [instance name]-task-[...] -c [instance name]-task -- api-manage shell_plus
```