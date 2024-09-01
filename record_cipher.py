import os
import sys
from cryptography.fernet import Fernet

# Hidden directory path
CRED_DIR = '.cred'
KEY_FILE = os.path.join(CRED_DIR, 'secret.key')
OLD_KEY_FILE = os.path.join(CRED_DIR, 'old_secret.key')

def ensure_cred_dir():
    """Ensure the hidden directory exists; create it if not."""
    if not os.path.exists(CRED_DIR):
        os.makedirs(CRED_DIR)
        # Set directory permissions to 700
        os.chmod(CRED_DIR, 0o700)

def generate_key():
    """Generate a new key and save it in the hidden directory."""
    ensure_cred_dir()
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    # Set file permissions to 600
    os.chmod(KEY_FILE, 0o600)
    print(f"A new key has been generated and saved to {KEY_FILE}.")

def load_key(file_path):
    """Load the key from the specified file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    return open(file_path, 'rb').read()

def re_encrypt_files(directory, old_key):
    """Re-encrypt files with the new key after decrypting them with the old key."""
    f_old = Fernet(old_key)
    f_new = Fernet(load_key(KEY_FILE))
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
            decrypted_data = f_old.decrypt(file_data)
            encrypted_data = f_new.encrypt(decrypted_data)
            with open(file_path, 'wb') as file:
                file.write(encrypted_data)
    print(f"All files in {directory} have been re-encrypted with the new key.")

def encrypt_file(filename):
    """Encrypt the specified file."""
    key = load_key(KEY_FILE)
    f = Fernet(key)
    
    with open(filename, 'rb') as file:
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    
    with open(filename, 'wb') as file:
        file.write(encrypted_data)
    print(f"{filename} has been encrypted.")

def decrypt_file(filename):
    """Decrypt the specified file."""
    key = load_key(KEY_FILE)
    f = Fernet(key)
    
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    
    decrypted_data = f.decrypt(encrypted_data)
    
    with open(filename, 'wb') as file:
        file.write(decrypted_data)
    print(f"{filename} has been decrypted.")

def process_directory(directory, encrypt=True):
    """Encrypt or decrypt all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if encrypt:
                encrypt_file(file_path)
            else:
                decrypt_file(file_path)

def rotate_keys(directory):
    """Rotate the encryption key: re-encrypt files with the new key."""
    if os.path.exists(KEY_FILE):
        # Save the current key as old key
        old_key = load_key(KEY_FILE)
        with open(OLD_KEY_FILE, 'wb') as old_key_file:
            old_key_file.write(old_key)
        # Generate a new key
        generate_key()
        # Re-encrypt files with the new key
        re_encrypt_files(directory, old_key)
        # Remove the old key file
        if os.path.exists(OLD_KEY_FILE):
            os.remove(OLD_KEY_FILE)
            print(f"Old key file {OLD_KEY_FILE} has been deleted.")
    else:
        print("Current key file does not exist. Please generate a key first.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python record_cipher.py [command] [directory_path]")
        print("Commands:")
        print("  generate  - Generate and save a new key.")
        print("  encrypt   - Encrypt files in the specified directory.")
        print("  decrypt   - Decrypt files in the specified directory.")
        print("  rotate    - Rotate the encryption key and re-encrypt files.")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'generate':
        generate_key()
    elif command in ['encrypt', 'decrypt']:
        if len(sys.argv) < 3:
            print("Usage: python record_cipher.py [command] [directory_path]")
            sys.exit(1)
        dir_path = sys.argv[2]
        if command == 'encrypt':
            process_directory(dir_path, encrypt=True)
        else:
            process_directory(dir_path, encrypt=False)
    elif command == 'rotate':
        if len(sys.argv) < 3:
            print("Usage: python record_cipher.py rotate [directory_path]")
            sys.exit(1)
        dir_path = sys.argv[2]
        rotate_keys(dir_path)
    else:
        print("Invalid command. Usage: python record_cipher.py [generate|encrypt|decrypt|rotate] [directory_path]")
        sys.exit(1)
