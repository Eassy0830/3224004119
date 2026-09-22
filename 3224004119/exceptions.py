"""论文查重模块自定义异常定义"""


class PlagiarismCheckError(Exception):
    """论文查重基础异常类"""
    pass


class FileReadError(PlagiarismCheckError):
    """文件读取异常：文件不存在或无法解码"""
    pass


class EmptyContentError(PlagiarismCheckError):
    """空内容异常：文件内容为空或分词后无有效词语"""
    pass


class InvalidArgumentError(PlagiarismCheckError):
    """参数异常：命令行参数数量不正确"""
    pass
