# Record Cipher

`record_cipher.py` is a Python script for file encryption and decryption using symmetric key encryption (Fernet). It includes functionalities for key generation, file encryption, decryption, and key rotation.

## Features

- **Generate**: Generate a new encryption key and save it securely.
- **Encrypt**: Encrypt files in a specified directory using the current key.
- **Decrypt**: Decrypt files in a specified directory using the current key.
- **Rotate**: Rotate the encryption key by generating a new key, re-encrypting files with the new key, and removing the old key.

## Usage

1. **Generate a New Key**

   ```sh
   python record_cipher.py generate
   ```

   This command will generate a new encryption key and save it to a hidden directory (`.cred`).

2. **Encrypt Files**

   ```sh
   python record_cipher.py encrypt [directory_path]
   ```

   This command will encrypt all files in the specified directory using the current encryption key.

3. **Decrypt Files**

   ```sh
   python record_cipher.py decrypt [directory_path]
   ```

   This command will decrypt all files in the specified directory using the current encryption key.

4. **Rotate Keys**

   ```sh
   python record_cipher.py rotate [directory_path]
   ```

   This command will rotate the encryption key: generate a new key, re-encrypt all files in the specified directory with the new key, and delete the old key.

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/Nachtburg/record_cipher.git
   ```

2. Install dependencies:

   ```sh
   pip install cryptography
   ```

3. Run the script as needed using the commands listed above.

## Notes

- Ensure the `.cred` directory has appropriate permissions for security (e.g., `chmod 700` for the directory and `chmod 600` for the key file).
- Make sure to securely back up the generated key, as losing it will make it impossible to decrypt the encrypted files.