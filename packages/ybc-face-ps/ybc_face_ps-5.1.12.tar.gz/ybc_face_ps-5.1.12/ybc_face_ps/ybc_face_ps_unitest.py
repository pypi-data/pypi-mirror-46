import unittest
from ybc_face_ps import *


class MyTestCase(unittest.TestCase):

    def test_bianzhuang_type(self):
        self.assertIsNotNone(bianzhuang_type())

    def test_meizhuang_type(self):
        self.assertIsNotNone(meizhuang_type())

    def test_ronghe_type(self):
        self.assertIsNotNone(ronghe_type())

    def test_datoutie_type(self):
        self.assertIsNotNone(datoutie_type())

    def test_bianzhuang(self):
        self.assertIsNotNone(bianzhuang('test.jpg'))

    def test_meizhuang(self):
        self.assertIsNotNone(meizhuang('test.jpg'))

    def test_ronghe(self):
        self.assertIsNotNone(ronghe('test.jpg'))

    def test_datoutie(self):
        self.assertIsNotNone(datoutie('test.jpg'))

    def test_bianzhuang_error(self):
        self.assertEqual('图片中找不到人哦~', bianzhuang('cup.jpg'))

    def test_meizhuang_error(self):
        self.assertEqual('图片中找不到人哦~', meizhuang('cup.jpg'))

    def test_ronghe_error(self):
        self.assertEqual('图片中找不到人哦~', ronghe('cup.jpg'))

    def test_datoutie_error(self):
        self.assertEqual('图片中找不到人哦~', datoutie('cup.jpg'))

    def test_bianzhuang_typeError(self):
        with self.assertRaises(ParameterTypeError):
            bianzhuang(123)

    def test_meizhuang_typeError(self):
        with self.assertRaises(ParameterTypeError):
            meizhuang(123)

    def test_ronghe_typeError(self):
        with self.assertRaises(ParameterTypeError):
            ronghe(123)

    def test_datoutie_typeError(self):
        with self.assertRaises(ParameterTypeError):
            datoutie(123)

    def test_bianzhuang_valueError(self):
        with self.assertRaises(ParameterValueError):
            bianzhuang('')

    def test_meizhuang_valueError(self):
        with self.assertRaises(ParameterValueError):
            meizhuang('')

    def test_ronghe_valueError(self):
        with self.assertRaises(ParameterValueError):
            ronghe('')

    def test_datoutie_valueError(self):
        with self.assertRaises(ParameterValueError):
            datoutie('')


if __name__ == '__main__':
    unittest.main()
