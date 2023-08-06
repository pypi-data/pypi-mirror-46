import unittest
from ybc_art import *


class MyTestCase(unittest.TestCase):
    def test_text2art(self):
        self.assertIsNotNone(text2art('nihao'))

    def test_text2art_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用text2art方法时，'text'、'font'、'chr_ignore'参数类型错误。$"):
            text2art(1, 1, 1)

    def test_text2art_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用text2art方法时，'text'、'font'参数不在允许范围内。$"):
            text2art('我', 'asd')


if __name__ == '__main__':
    unittest.main()
