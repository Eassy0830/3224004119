"""TextProcessor模块单元测试"""

import unittest
import os
import tempfile

# 将项目根目录加入搜索路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, PROJECT_ROOT)

from text_processor import TextProcessor
from exceptions import FileReadError


class TestTextProcessor(unittest.TestCase):
    """TextProcessor单元测试"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.test_data_dir = os.path.join(PROJECT_ROOT, 'test_data')
        self.temp_dir = tempfile.mkdtemp()

    # ===== 测试用例1：读取UTF-8编码文件 =====
    def test_read_utf8_file(self):
        """测试读取UTF-8编码文件，应正常返回内容"""
        file_path = os.path.join(self.test_data_dir, 'orig.txt')
        content = TextProcessor.read_file(file_path)
        self.assertTrue(len(content) > 0)
        self.assertIn('今天', content)

    # ===== 测试用例2：读取不存在的文件 =====
    def test_read_nonexistent_file(self):
        """测试读取不存在的文件，应抛出FileReadError"""
        with self.assertRaises(FileReadError):
            TextProcessor.read_file('nonexistent_file_12345.txt')

    # ===== 测试用例3：读取空文件 =====
    def test_read_empty_file(self):
        """测试读取空文件，应返回空字符串"""
        file_path = os.path.join(self.test_data_dir, 'empty.txt')
        content = TextProcessor.read_file(file_path)
        self.assertEqual(content, '')

    # ===== 测试用例4：读取目录路径 =====
    def test_read_directory_path(self):
        """测试传入目录路径而非文件，应抛出FileReadError"""
        with self.assertRaises(FileReadError):
            TextProcessor.read_file(self.test_data_dir)

    # ===== 测试用例5：中文分词 =====
    def test_segment_chinese_text(self):
        """测试中文分词，应正确切分词语并过滤停用词"""
        text = "今天是星期天，天气晴，今天晚上我要去看电影。"
        words = TextProcessor.segment(text)
        self.assertTrue(len(words) > 0)
        # '今天' 应在分词结果中（虽然它不在停用词表里）
        self.assertIn('今天', words)
        # '的' 不在文本中，'了' 也不在，验证停用词被过滤
        self.assertNotIn('的', words)

    # ===== 测试用例6：空文本分词 =====
    def test_segment_empty_text(self):
        """测试空文本分词，应返回空列表"""
        words = TextProcessor.segment('')
        self.assertEqual(words, [])

    # ===== 测试用例7：停用词过滤 =====
    def test_stop_words_filtered(self):
        """测试停用词是否被正确过滤"""
        text = "我今天去看了电影"
        words = TextProcessor.segment(text)
        # '我' 是停用词，应被过滤
        self.assertNotIn('我', words)
        # '今天' 和 '电影' 不是停用词，应保留
        self.assertIn('今天', words)
        self.assertIn('电影', words)

    # ===== 测试用例8：词频统计 =====
    def test_get_word_frequency(self):
        """测试词频统计，重复词语应正确计数"""
        text = "今天是星期天 今天是星期天 天气晴"
        freq = TextProcessor.get_word_frequency(text)
        self.assertTrue(len(freq) > 0)
        # '今天' 出现两次
        if '今天' in freq:
            self.assertEqual(freq['今天'], 2)
        if '星期天' in freq:
            self.assertEqual(freq['星期天'], 2)


if __name__ == '__main__':
    unittest.main()
