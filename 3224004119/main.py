#!/usr/bin/env python3
"""
论文查重工具 - 基于SimHash算法的中文论文查重系统

用法:
    python main.py [原文文件路径] [抄袭版文件路径] [答案文件路径]

示例:
    python main.py C:\\tests\\orig.txt C:\\tests\\orig_add.txt C:\\tests\\ans.txt

输出:
    在答案文件中写入重复率（浮点数，精确到小数点后两位）
"""

import sys

from text_processor import TextProcessor
from simhash import SimHash
from exceptions import FileReadError, EmptyContentError, InvalidArgumentError


def check_plagiarism(orig_path, plagia_path, answer_path):
    """
    论文查重主函数

    流程：
    1. 读取原文文件和抄袭版文件
    2. 中文分词并统计词频
    3. 使用SimHash算法计算文档指纹
    4. 通过汉明距离计算相似度
    5. 将重复率写入答案文件

    Args:
        orig_path: 原文文件的绝对路径
        plagia_path: 抄袭版论文文件的绝对路径
        answer_path: 输出答案文件的绝对路径

    Returns:
        float: 重复率（0.00 ~ 1.00）

    Raises:
        FileReadError: 文件读取失败
        EmptyContentError: 文件内容为空
    """
    # 步骤1：读取文件
    orig_text = TextProcessor.read_file(orig_path)
    plagia_text = TextProcessor.read_file(plagia_path)

    # 步骤2：处理空文件情况
    if not orig_text or not plagia_text:
        similarity = 0.0
    else:
        # 步骤3：分词并统计词频
        orig_freq = TextProcessor.get_word_frequency(orig_text)
        plagia_freq = TextProcessor.get_word_frequency(plagia_text)

        # 步骤4：计算SimHash相似度
        if not orig_freq or not plagia_freq:
            # 分词后无有效词语（如全是标点或停用词）
            similarity = 0.0
        else:
            orig_hash = SimHash(orig_freq)
            plagia_hash = SimHash(plagia_freq)
            similarity = orig_hash.similarity(plagia_hash)

    # 步骤5：写入结果（保留两位小数）
    with open(answer_path, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2f}")

    return similarity


def main():
    """
    主函数：解析命令行参数并执行查重

    命令行参数格式：
        python main.py [原文文件] [抄袭版文件] [答案文件]
    """
    # 校验参数数量
    if len(sys.argv) != 4:
        raise InvalidArgumentError(
            "参数数量错误！\n"
            "用法: python main.py [原文文件路径] [抄袭版文件路径] [答案文件路径]\n"
            "示例: python main.py orig.txt orig_add.txt ans.txt"
        )

    orig_path = sys.argv[1]
    plagia_path = sys.argv[2]
    answer_path = sys.argv[3]

    check_plagiarism(orig_path, plagia_path, answer_path)


if __name__ == '__main__':
    try:
        main()
    except InvalidArgumentError as e:
        print(f"参数错误: {e}")
        sys.exit(1)
    except FileReadError as e:
        print(f"文件读取错误: {e}")
        sys.exit(1)
    except EmptyContentError as e:
        print(f"内容错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        sys.exit(1)
