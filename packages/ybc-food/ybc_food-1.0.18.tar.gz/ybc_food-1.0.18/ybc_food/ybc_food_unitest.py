import unittest
from ybc_food import *


class MyTestCase(unittest.TestCase):
    def test_check(self):
        self.assertEqual(True, check('test.jpg'))

    def test_food_name(self):
        self.assertEqual('汉堡', food_name('test.jpg'))

    def test_check_error(self):
        self.assertEqual(False, check('error_test.jpg'))

    def test_food_name_error(self):
        self.assertEqual('非菜', food_name('error_test.jpg'))

    def test_check_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用check方法时，'filename'参数类型错误。$"):
            check(123)

    def test_food_name_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用food_name方法时，'filename'参数类型错误。$"):
            food_name(123)

    def test_food_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用food方法时，'filename'参数类型错误。$"):
            food(123)

    def test_check_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用check方法时，'filename'参数不在允许范围内。$"):
            check('')

    def test_food_name_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用food_name方法时，'filename'参数不在允许范围内。$"):
            food_name('')

    def test_food_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用food方法时，'filename'参数不在允许范围内。$"):
            food('')


if __name__ == '__main__':
    unittest.main()
