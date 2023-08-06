"""
Contains the methods to decipher the equation cipher method.
"""
import base64
import sys
sys.path.append('..')

from cipher.equation_cipher import Encrypter


class Decrypter(Encrypter):
    """
    Class to decrypt the equation cipher encryption.
    Note: This decryption can not be done complete decryption but partial
    decryption can be done and string passed can be verified at some stage of
    encryption.
    """

    def match_decrypt(self, target: str, hash_str: bytes) -> bool:
        """
        Checks if the passed hash_str is representation of passed
        target string or not.
        :param target: <data type: str>
        :param hash_str: <data type: str(bytes)>
        :return: <data type: bool>
        """
        decrypted_hash = base64.b64decode(hash_str).decode('utf-8')
        equation = decrypted_hash.split('@')[0]
        date_obj = self.converter.epoch_to_datetime(float(
            decrypted_hash.split('@')[1]))
        en_str = self._form_equation(target, date_obj)

        return True if equation == en_str else False
