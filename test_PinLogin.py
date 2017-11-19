import unittest
import pin_login

class PinLoginTestCase(unittest.TestCase):
    """Test for pin_login"""
    def test_encode_decode(self):
        """Test encode/decode process"""
        pin = "5421"
        msg = "Test msg."
        encoded_msg = pin_login.encode(pin, msg)
        return_msg = pin_login.decode(pin, encoded_msg)
        self.assertEqual(msg, return_msg)

if __name__ == '__main__':
    unittest.main()