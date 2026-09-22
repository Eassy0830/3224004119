"""SimHash算法实现：用于中文论文查重的文本相似度计算"""

import hashlib


class SimHash:
    """
    SimHash算法实现类

    SimHash是一种局部敏感哈希（LSH）算法，特别适用于
    近似文档的查重和相似度检测。其核心思想是：
    1. 对文档中的每个特征词计算哈希值
    2. 根据词频对哈希值进行加权累加
    3. 生成固定长度的文档指纹
    4. 通过比较两个文档指纹的汉明距离计算相似度
    """

    # SimHash指纹位数
    HASH_BITS = 64

    def __init__(self, word_freq):
        """
        根据词频字典计算SimHash指纹

        Args:
            word_freq: 词频字典 {词语: 频率}
        """
        self.fingerprint = self._compute(word_freq)

    def _hash_word(self, word):
        """
        计算单个词语的64位哈希值

        使用MD5取前64位，保证哈希的均匀分布和确定性

        Args:
            word: 词语

        Returns:
            str: 64位二进制字符串
        """
        hash_hex = hashlib.md5(word.encode('utf-8')).hexdigest()
        # 取前16个十六进制字符 = 64位
        hash_int = int(hash_hex[:16], 16)
        return format(hash_int, '064b')

    def _compute(self, word_freq):
        """
        计算SimHash指纹

        算法步骤：
        1. 初始化长度为HASH_BITS的权重向量v，全部为0
        2. 对每个词语，计算其64位哈希
        3. 遍历哈希的每一位：若该位为1则v对应位加上词频权重，否则减去
        4. 最终：v[i] > 0 则指纹第i位为1，否则为0

        Args:
            word_freq: 词频字典

        Returns:
            str: 64位二进制指纹字符串
        """
        if not word_freq:
            return '0' * self.HASH_BITS

        # 初始化权重向量
        v = [0] * self.HASH_BITS

        for word, freq in word_freq.items():
            bits = self._hash_word(word)
            weight = freq

            for i in range(self.HASH_BITS):
                if bits[i] == '1':
                    v[i] += weight
                else:
                    v[i] -= weight

        # 生成最终指纹
        return ''.join('1' if v[i] > 0 else '0' for i in range(self.HASH_BITS))

    def hamming_distance(self, other):
        """
        计算两个SimHash指纹之间的汉明距离

        汉明距离 = 两个等长字符串对应位不同的数量

        Args:
            other: 另一个SimHash对象

        Returns:
            int: 汉明距离
        """
        if len(self.fingerprint) != len(other.fingerprint):
            raise ValueError("指纹长度不一致，无法比较")

        return sum(1 for a, b in zip(self.fingerprint, other.fingerprint) if a != b)

    def similarity(self, other):
        """
        计算两个文档的相似度

        相似度 = 1 - 汉明距离 / 指纹位数
        范围：[0, 1]，1表示完全相同，0表示完全不同

        Args:
            other: 另一个SimHash对象

        Returns:
            float: 相似度，范围[0, 1]
        """
        distance = self.hamming_distance(other)
        return 1.0 - distance / self.HASH_BITS
