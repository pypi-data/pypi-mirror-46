import unittest
import sys
import datetime
sys.path.append('..')

from cipher.equation_cipher import Encrypter
from cipher.equation_decipher import Decrypter


class TestEncrypt(unittest.TestCase):
    """
    Unit tests for encryption and decryption using encryption_cipher.
    """

    def test_unique_encryption(self):
        """
        Test if algorithm gives unique encryption every second or not.
        :return:
        """
        string = 'Hello@123'
        enc = Encrypter()
        encrypted_string = enc.encrypt(string)
        self.assertNotEqual(encrypted_string, enc.encrypt(string))

    def test_similar_encryption_by_datetime(self):
        """
        Check if algoritm provides similar type of encryption for a string for
        passed date.
        :return:
        """
        string = 'today@123'
        enc = Encrypter()
        date_obj = datetime.datetime.now()
        encrypted_string = enc.encrypt_by_date(string, date_obj)
        self.assertEqual(encrypted_string, enc.encrypt_by_date(string,
                                                               date_obj))

    def test_general_decryption(self):
        """
        Check if algorithm can decrypt the worked encryption as expected.
        :return:
        """
        string = 'check_decrypt_1122'
        enc = Encrypter()
        dec = Decrypter()

        encrypted_string = enc.encrypt(string)
        self.assertTrue(dec.match_decrypt(string, encrypted_string))

    def test_by_date_decryption(self):
        """
        Test if the passed encryption with date can be decrypted by the
        provided decryption logic.
        :return:
        """
        string = 'check_decrypt_1122'
        enc = Encrypter()
        dec = Decrypter()
        date_obj = datetime.datetime.now()

        encrypted_string = enc.encrypt_by_date(string, date_obj)
        self.assertTrue(dec.match_decrypt(string, encrypted_string))


if __name__ == '__main__':
    unittest.main()
