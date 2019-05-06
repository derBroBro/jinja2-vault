import unittest
import os

os.environ["JINJA2_VAULT_DEBUG"] = "ERROR"

jinja2Vault = __import__('jinja2-vault')

# This tests expect that vault instance runs as follow:
# Endpoint      = http://localhost:8200
# valid token   = myroot
# mount         = test/secret
# key           = test-key
# path          = test-path
# value         = valid-value

endpoint= "http://localhost:8200"
token   = "myroot"
mount   = "test/secret"
key     = "test-key" 
path    = "test-path"
valid   = "valid-value"


class TestGetSecret(unittest.TestCase):
    # path, key, mount):
    def test_get_secret_ok(self):
        os.environ["VAULT_ADDR"]  = endpoint
        os.environ["VAULT_TOKEN"] = token
        result = jinja2Vault.VaultExtension.get_secret(self, path, key, mount)
        self.assertEqual(result, valid)

    def test_get_secret_invalid_path(self):
        os.environ["VAULT_ADDR"] = endpoint
        os.environ["VAULT_TOKEN"] = token
        result = jinja2Vault.VaultExtension.get_secret(self, "invalid-path", key, mount)
        self.assertEqual(result, "failed-find-path")

    def test_get_secret_invalid_key(self):
        os.environ["VAULT_ADDR"] = endpoint
        os.environ["VAULT_TOKEN"] = token
        result = jinja2Vault.VaultExtension.get_secret(
            self, path, "invalid-key", mount)
        self.assertEqual(result, "failed-find-key")

    def test_get_secret_invalid_mount(self):
        os.environ["VAULT_ADDR"] = endpoint
        os.environ["VAULT_TOKEN"] = token
        result = jinja2Vault.VaultExtension.get_secret(
            self, path, key, "invalid-mount")
        self.assertEqual(result, "failed-find-path")

    def test_get_secret_invalid_host(self):
        os.environ["VAULT_ADDR"] = "https://no-valid.local"
        os.environ["VAULT_TOKEN"] = token
        result = jinja2Vault.VaultExtension.get_secret(
            self, path, key, "invalid-mount")
        self.assertEqual(result, "failed-to-connect")

    def test_get_secret_invalid_token(self):
        os.environ["VAULT_ADDR"] = endpoint
        os.environ["VAULT_TOKEN"] = "invalid-token"
        result = jinja2Vault.VaultExtension.get_secret(
            self, path, key, "invalid-mount")
        self.assertEqual(result, "failed-to-auth")

if __name__ == '__main__':
    unittest.main()
