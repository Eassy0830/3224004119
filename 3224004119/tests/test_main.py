"""主函数模块单元测试"""

import unittest
import os
import tempfile
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from main import check_plagiarism
from exceptions import FileReadError, InvalidArgumentError


class TestMain(unittest.TestCase):
    """主函数check_plagiarism的单元测试"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.test_data_dir = os.path.join(PROJECT_ROOT, 'test_data')
        self.temp_dir = tempfile.mkdtemp()
        self.answer_path = os.path.join(self.temp_dir, 'ans.txt')

    # ===== 测试用例16：正常查重（原文 vs 修改版） =====
    def test_normal_plagiarism_check(self):
        """测试正常查重流程，相似度应在(0, 1]范围内"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        plagia = os.path.join(self.test_data_dir, 'orig_mod.txt')
        result = check_plagiarism(orig, plagia, self.answer_path)
        self.assertGreater(result, 0.0)
        self.assertLessEqual(result, 1.0)

    # ===== 测试用例17：相同文件查重（相似度应为1.0） =====
    def test_identical_files(self):
        """测试原文与自身比较，相似度应为1.0"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        result = check_plagiarism(orig, orig, self.answer_path)
        self.assertEqual(result, 1.0)

    # ===== 测试用例18：完全不同文件查重 =====
    def test_different_files(self):
        """测试完全不同的文本，相似度应较低"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        plagia = os.path.join(self.test_data_dir, 'different.txt')
        result = check_plagiarism(orig, plagia, self.answer_path)
        self.assertLess(result, 0.7)

    # ===== 测试用例19：空文件查重 =====
    def test_empty_file(self):
        """测试空文件查重，相似度应为0.0"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        plagia = os.path.join(self.test_data_dir, 'empty.txt')
        result = check_plagiarism(orig, plagia, self.answer_path)
        self.assertEqual(result, 0.0)

    # ===== 测试用例20：文件不存在异常 =====
    def test_nonexistent_file(self):
        """测试文件不存在时应抛出FileReadError"""
        with self.assertRaises(FileReadError):
            check_plagiarism('nonexistent.txt', 'also_nonexistent.txt', self.answer_path)

    # ===== 测试用例21：输出文件格式验证 =====
    def test_output_format(self):
        """测试输出文件内容是否为两位小数的浮点数"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        plagia = os.path.join(self.test_data_dir, 'orig_mod.txt')
        check_plagiarism(orig, plagia, self.answer_path)

        with open(self.answer_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # 应为有效的浮点数
        value = float(content)
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)

        # 应精确到小数点后两位
        if '.' in content:
            decimal_part = content.split('.')[1]
            self.assertEqual(len(decimal_part), 2)

    # ===== 测试用例22：增删改混合查重 =====
    def test_mixed_modification_check(self):
        """测试增删改混合的抄袭版本查重"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        plagia = os.path.join(self.test_data_dir, 'orig_mix.txt')
        result = check_plagiarism(orig, plagia, self.answer_path)
        # 混合修改版本应有中等以上相似度
        self.assertGreater(result, 0.3)

    # ===== 测试用例23：仅增删内容查重 =====
    def test_addition_deletion_check(self):
        """测试仅增删内容的抄袭版本查重"""
        orig = os.path.join(self.test_data_dir, 'orig.txt')
        plagia_add = os.path.join(self.test_data_dir, 'orig_add.txt')
        plagia_del = os.path.join(self.test_data_dir, 'orig_del.txt')

        result_add = check_plagiarism(orig, plagia_add, self.answer_path)
        result_del = check_plagiarism(orig, plagia_del, self.answer_path)

        # 增加版和删减版都应有较高相似度
        self.assertGreater(result_add, 0.3)
        self.assertGreater(result_del, 0.3)


if __name__ == '__main__':
    unittest.main()
