"""文本处理模块：负责文件读取、中文分词和词频统计"""

import os
import re

import jieba

from exceptions import FileReadError

# 中文停用词表：过滤无实际语义的高频功能词，提高查重准确度
STOP_WORDS = {
    '的', '了', '是', '在', '我', '你', '他', '她', '它', '们', '个', '也',
    '就', '都', '还', '又', '才', '只', '对', '和', '与', '或', '但', '而',
    '且', '为', '把', '被', '让', '使', '给', '到', '向', '从', '跟', '由',
    '这', '那', '要', '会', '能', '可', '以', '有', '无', '之', '于', '其',
    '所', '一', '不', '没', '吧', '呢', '啊', '呀', '哦', '嗯', '嘛', '哈',
    '着', '地', '得', '将', '已', '正', '该', '此', '每', '各', '另', '别',
    '本', '上', '下', '里', '中', '去', '来', '过', '看', '说', '做', '想',
}


class TextProcessor:
    """文本处理器：负责文件读取、中文分词和词频统计"""

    # 支持的文件编码列表（按优先级排序）
    SUPPORTED_ENCODINGS = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']

    @staticmethod
    def read_file(file_path):
        """
        读取文件内容，自动尝试多种编码

        Args:
            file_path: 文件绝对路径

        Returns:
            str: 文件内容（已去除首尾空白）

        Raises:
            FileReadError: 文件不存在或无法解码
        """
        if not os.path.exists(file_path):
            raise FileReadError(f"文件不存在: {file_path}")

        if not os.path.isfile(file_path):
            raise FileReadError(f"路径不是文件: {file_path}")

        for encoding in TextProcessor.SUPPORTED_ENCODINGS:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read().strip()
            except (UnicodeDecodeError, UnicodeError):
                continue

        raise FileReadError(f"无法解码文件（尝试了所有支持的编码）: {file_path}")

    @staticmethod
    def segment(text):
        """
        中文分词，过滤停用词和标点符号

        Args:
            text: 文本内容

        Returns:
            list: 词语列表（已过滤停用词和标点）
        """
        if not text:
            return []

        # 使用jieba精确模式分词
        words = jieba.lcut(text)

        # 过滤：只保留包含中文、字母或数字的词，且不在停用词表中
        pattern = re.compile(r'[\u4e00-\u9fff\w]+')
        result = []
        for word in words:
            word = word.strip()
            if word and pattern.match(word) and word not in STOP_WORDS:
                result.append(word)

        return result

    @staticmethod
    def get_word_frequency(text):
        """
        统计词频

        Args:
            text: 文本内容

        Returns:
            dict: 词频字典 {词语: 出现次数}
        """
        words = TextProcessor.segment(text)
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        return freq
