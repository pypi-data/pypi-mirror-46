# -*- coding: utf-8 -*-
# author:      hj
# create_time: 2018/11/30 16:28
# update_time: 2018/11/30 16:28
import re


class RegexUtils:
    """
    正则表达式辅助类
    """
    def __init__(self):
        pass

    @staticmethod
    def is_match(regex, contents):
        """
        判别是否能匹配到某一表达式
        :param regex:正则表达式
        :param contents:待匹配内容
        :return:
        """
        _search = re.search(regex, contents)
        if _search:
            return True
        else:
            return False

    @staticmethod
    def is_match_ignore_case(regex, contents):
        """
        忽视大小写判断是否满足
        :param regex: 正则表达式
        :param contents:
        :return:
        """
        _search = re.search(regex, contents, re.I)
        if _search:
            return True
        else:
            return False

    @staticmethod
    def find(regex, contents, pos=0, flags=0):
        """
        查找匹配到正则的内容
        :param regex:正则表达式
        :param contents:待匹配内容
        :param pos:表达式中，待匹配位置
        :param flags:
        :return:
        """
        _searches = re.findall(regex, contents, flags=flags)
        if _searches:
            _search = _searches[0]
            if isinstance(_search, tuple):
                return _search[pos]
            else:
                return _search
        else:
            return None

    @staticmethod
    def find_all(regex, contents, flags=0):
        return re.findall(regex, contents, flags=flags)