"""SimHash模块单元测试"""

import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from simhash import SimHash


class TestSimHash(unittest.TestCase):
    """SimHash算法单元测试"""

    # ===== 测试用例9：相同文本相似度为1.0 =====
    def test_identical_texts_similarity(self):
        """测试相同文本的SimHash相似度，应为1.0"""
        freq = {'今天': 2, '星期天': 1, '电影': 1, '天气': 1}
        hash1 = SimHash(freq)
        hash2 = SimHash(freq)
        self.assertEqual(hash1.similarity(hash2), 1.0)

    # ===== 测试用例10：完全不同文本相似度较低 =====
    def test_different_texts_similarity(self):
        """测试完全不同文本的相似度，应较低"""
        freq1 = {'今天': 2, '星期天': 1, '电影': 1, '天气': 1, '晴': 1}
        freq2 = {'计算机': 3, '科学': 2, '编程': 1, '算法': 1, '数据': 1}
        hash1 = SimHash(freq1)
        hash2 = SimHash(freq2)
        similarity = hash1.similarity(hash2)
        self.assertLess(similarity, 0.7)

    # ===== 测试用例11：相似文本相似度较高 =====
    def test_similar_texts_similarity(self):
        """测试相似文本（部分词语相同）的相似度，应较高"""
        freq1 = {'今天': 2, '星期天': 1, '电影': 1, '天气': 1, '晴': 1}
        freq2 = {'今天': 2, '周天': 1, '电影': 1, '天气': 1, '晴朗': 1}
        hash1 = SimHash(freq1)
        hash2 = SimHash(freq2)
        similarity = hash1.similarity(hash2)
        # 共享 '今天'(权重2) 和 '电影'(权重1) 和 '天气'(权重1)
        # 应该有较高相似度
        self.assertGreater(similarity, 0.5)

    # ===== 测试用例12：空词频指纹全零 =====
    def test_empty_word_freq(self):
        """测试空词频字典，指纹应全为0"""
        hash1 = SimHash({})
        self.assertEqual(hash1.fingerprint, '0' * 64)

    # ===== 测试用例13：汉明距离计算 =====
    def test_hamming_distance(self):
        """测试汉明距离计算，相同指纹距离为0"""
        freq = {'测试': 1, '数据': 1}
        hash1 = SimHash(freq)
        hash2 = SimHash(freq)
        self.assertEqual(hash1.hamming_distance(hash2), 0)

    # ===== 测试用例14：指纹长度为64位 =====
    def test_fingerprint_length(self):
        """测试SimHash指纹长度是否为64位"""
        freq = {'今天': 1, '星期天': 1}
        hash_obj = SimHash(freq)
        self.assertEqual(len(hash_obj.fingerprint), 64)

    # ===== 测试用例15：相似度范围在[0, 1]之间 =====
    def test_similarity_range(self):
        """测试相似度始终在[0, 1]范围内"""
        freq1 = {'苹果': 5, '香蕉': 3, '橘子': 2}
        freq2 = {'电脑': 4, '手机': 2, '平板': 1}
        hash1 = SimHash(freq1)
        hash2 = SimHash(freq2)
        similarity = hash1.similarity(hash2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)


if __name__ == '__main__':
    unittest.main()
