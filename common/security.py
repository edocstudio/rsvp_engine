from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag
from os import urandom
from base64 import b64encode, b64decode


class SymmetricData:
    """
    Utility for AES-GCM symmetric encryption/decryption with password-based key derivation.
    """
    def __init__(
        self,
        salt_bytes: int = 16,
        iv_bytes: int = 12,
        tag_bytes: int = 16,
        key_length: int = 32,
        iters: int = 100_000,
        hash_algorithm: str = '256'
    ) -> None:
        """
        Initialize with default cryptographic parameters.
        """
        self.salt_bytes = salt_bytes
        self.iv_bytes = iv_bytes
        self.tag_bytes = tag_bytes
        self.key_length = key_length
        self.iters = iters
        
        # Supported hash algorithms
        self._hash_algorithm = {
            '256': hashes.SHA256(),
            '512': hashes.SHA512()
        }.get(hash_algorithm)
        
        if self._hash_algorithm is None:
            raise ValueError("Unsupported hash algorithm: choose '256' or '512'")
        
        # Precompute slices for decoding
        self._salt_slice = self.salt_bytes
        self._iv_slice = self.salt_bytes + self.iv_bytes
        self._tag_slice = self._iv_slice + self.tag_bytes

    def __derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derives a key from password and salt using PBKDF2.
        """
        kdf = PBKDF2HMAC(
            algorithm=self._hash_algorithm,
            length=self.key_length,
            salt=salt,
            iterations=self.iters,
        )
        return kdf.derive(password.encode('utf-8'))

    def encrypt_aes_gcm(self, plaintext: str, password: str) -> str:
        """
        Encrypt plaintext using AES-GCM with a password.
        Returns base64-encoded string with format: salt + iv + tag + ciphertext
        """
        salt = urandom(self.salt_bytes)
        iv = urandom(self.iv_bytes)
        key = self.__derive_key(password, salt)
        encryptor = Cipher(algorithms.AES(key), modes.GCM(iv)).encryptor()
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        encrypted = salt + iv + encryptor.tag + ciphertext
        return b64encode(encrypted).decode('utf-8')

    def decrypt_aes_gcm(self, encrypted_data: str, password: str) -> str:
        """
        Decrypts base64-encoded AES-GCM data with the provided password.
        Returns the decrypted plaintext string.
        Raises ValueError if decryption fails.
        """
        try:
            decoded = b64decode(encrypted_data)
            salt = decoded[:self._salt_slice]
            iv = decoded[self._salt_slice:self._iv_slice]
            tag = decoded[self._iv_slice:self._tag_slice]
            ciphertext = decoded[self._tag_slice:]
            key = self.__derive_key(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext_bytes.decode('utf-8')
        except (InvalidTag, Exception) as e:
            raise ValueError("Decryption failed: invalid password or corrupted data.")
