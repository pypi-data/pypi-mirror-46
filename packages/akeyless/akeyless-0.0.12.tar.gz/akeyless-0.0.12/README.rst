#######################
AKEYLESS SDK for Python
#######################

The AKEYLESS SDK for Python enables Python developers to easily interface with the Akeyless encryption key protection system.

AKEYLESS innovative Key and Secret Management as-a Service solution enables Encryption Key Management, Secret Management, Data-at-rest Encryption, Client-side Encryption and Digital Signature where the encryption key’s material never exists in one place throughout its lifecycle including creation, in-use and at-rest. It functions completely as a service, and there is no need for the customer to deploy secure virtual machines for storing keys or secrets. For more information about the technology, please visit `our website`_.

***************
Getting Started
***************
Sign up for AKEYLESS
====================

Before you begin, you need an AKEYLESS account. Please sign up `here`_ and receive your admin user access credentials.


Minimum requirements
====================

* Python 3.4+
* cryptography >= 1.8.1

Installation
============

.. note::
    If you have not already installed `cryptography`_, you might need to install additional prerequisites as
    detailed in the `cryptography installation guide`_ for your operating system.

.. code::

    $pip install akeyless

*************
Documentation
*************

You can find the AKEYLESS Python SDK full documentation at `Read the Docs`_.

*****
Usage
*****

The following code sample demonstrates how to encrypt/decrypt data via the Akeyless system where the key fragments are stored in multiple locations and are never combined:

.. code::

    from akeyless import AkeylessClientConfig, AkeylessClient


    def encrypt_decrypt_string(policy_id, api_key, key_name, plaintext):
        """Encrypts and then decrypts a string using an AES key from your Akeyless account.

        :param str policy_id: The user access policy id.
        :param str api_key: The user access key.
        :param str key_name: The name of the key to use in the encryption process
        :param str plaintext: Data to encrypt
        """

        # Akeyless playground environment.
        akeyless_server_dns = "playground-env.akeyless-security.com"

        conf = AkeylessClientConfig(akeyless_server_dns, policy_id, api_key)
        client = AkeylessClient(conf)

        # Encrypt the plaintext source data
        ciphertext = client.encrypt_string(key_name, plaintext)

        # Decrypt the ciphertext
        decrypt_res = client.decrypt_string(key_name, ciphertext)

        # Verify that the decryption result is identical to the source plaintext
        assert decrypt_res == plaintext

        client.close()


The following code sample demonstrates how to create keys, users, roles, and associations between them

.. code::

    from akeyless import AkeylessClientConfig, AkeylessAdminClient, AkeylessClient
    from akeyless.crypto import CryptoAlgorithm


    def key_and_user_management(policy_id, api_key):
        """Create keys, users, roles, and associations between them.

        :param str policy_id: An admin user access policy id.
        :param str api_key: An admin user access key.
        """

        # Akeyless playground environment.
        akeyless_server_dns = "playground-env.akeyless-security.com"

        conf = AkeylessClientConfig(akeyless_server_dns, policy_id, api_key)
        admin_client = AkeylessAdminClient(conf)

        # Create new AES-256-GCM key named "key1"
        admin_client.create_aes_key("key1", CryptoAlgorithm.AES_256_GCM, "testing", 2)

        # Get key details
        key_des = admin_client.describe_key("key1")
        print(key_des)

        # Create new user named "user1". The returned object contains the user policy id and api key.
        user1_access_api = admin_client.create_user("user1")
        print(user1_access_api)

        #  Replacing the access API key of "user1". The returned object contains the new api key.
        user1_new_api_key = admin_client.reset_user_access_key("user1")
        print(user1_new_api_key)

        # Get user details
        user_des = admin_client.get_user("user1")
        print(user_des)

        # Create new role named "role1"
        admin_client.create_role("role1")

        #  Create an association between the role "role1" and the key "key1".
        admin_client.create_role_item_assoc("role1", "key1")

        #  Create an association between the role "role1" and the user "user1".
        admin_client.create_role_user_assoc("role1", "user1")

        #  Now the user has access to the key and can encrypt/decrypt with it as follows:

        user1_config = AkeylessClientConfig(akeyless_server_dns, user1_access_api.policy_id,
                                            user1_new_api_key.get_key_seed_str())

        user1_client = AkeylessClient(user1_config)
        plaintext = "Encrypt Me!"
        ciphertext = user1_client.encrypt_string("key1", plaintext)
        decrypt_res = user1_client.decrypt_string("key1", ciphertext)

        assert decrypt_res == plaintext

        user1_client.close()

        # Delete an association between the role "role1" and the user "user1" So
        # that the user's "user1" access to the key is blocked.
        admin_client.delete_role_user_assoc("role1", "user1")

        # Delete an association between the role "role1" and the key "key1".
        admin_client.delete_role_item_assoc("role1", "key1")

        admin_client.delete_user("user1")
        admin_client.delete_role("role1")

        #  Warning! - After deleting a key, all data encrypted with that key will no longer be accessible.
        admin_client.delete_key("key1")

        admin_client.close()

The following code sample demonstrates how to save and load secrets

.. code::

    from akeyless import AkeylessClientConfig, AkeylessAdminClient


    def secret_management(policy_id, api_key, secret_name, secret_value, secret_metadata=""):
        """Create a new secret.

        :param str policy_id: The user access policy id.
        :param str api_key: The user access key.
        :param str secret_name: The name of the new secret
        :param str secret_value: The value of the new secret
        :param str secret_metadata: Metadata about the secret
        """

        akeyless_server_dns = "playground-env.akeyless-security.com"  # Akeyless playground environment.

        conf = AkeylessClientConfig(akeyless_server_dns, policy_id, api_key)
        client = AkeylessAdminClient(conf)

        # Create new secret
        client.create_secret(secret_name, secret_value, secret_metadata)

        # Get secret value
        secret_val_res = client.get_secret_value(secret_name)
        assert secret_val_res == secret_value

        # Get secret details
        secret_des = client.describe_item(secret_name)
        print(secret_des)

        # Update secret value
        new_secret_value = "this is a new secret"
        client.update_secret_value(secret_name, new_secret_value)
        secret_val_res = client.get_secret_value(secret_name)
        assert secret_val_res == new_secret_value

        client.close()


You can find more examples in the `examples directory`_


*******
License
*******
This SDK is distributed under the `Apache License, Version 2.0`_ see LICENSE.txt for more information.


.. _our website: https://www.akeyless-security.com/
.. _here: http://portal.akeyless-security.com/signup
.. _cryptography: https://cryptography.io/en/latest/
.. _cryptography installation guide: https://cryptography.io/en/latest/installation/
.. _Read the Docs:
.. _Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
.. _examples directory: https://github.com/akeylesslabs/akeyless-python-sdk-examples/tree/master/examples/src
