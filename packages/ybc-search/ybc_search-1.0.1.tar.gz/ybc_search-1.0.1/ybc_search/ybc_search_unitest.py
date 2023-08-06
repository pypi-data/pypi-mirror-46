import unittest
from ybc_search import *


class MyTestCase(unittest.TestCase):
    def test_article_search(self):
        article_file_name = '称赞.txt'
        self.assertEqual(article_file_name, article_search('称赞'))
        article_file_name = '纸船和风筝.txt'
        self.assertEqual(article_file_name, article_search('纸船'))

    def test_article_search_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用article_search方法时，'keyword'参数类型错误。$"):
            article_search(1)

    def test_article_search_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用article_search方法时，'keyword'参数不在允许范围内。$"):
            article_search('')

    def test_pic_search(self):
        self.assertEqual(0, pic_search('彭于晏'))

    def test_pic_search_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用pic_search方法时，'keyword'、'total'参数类型错误。$"):
            pic_search(123, '')

    def test_pic_search_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用pic_search方法时，'keyword'、'total'参数不在允许范围内。$"):
            pic_search('', 50)


if __name__ == '__main__':
    unittest.main()
