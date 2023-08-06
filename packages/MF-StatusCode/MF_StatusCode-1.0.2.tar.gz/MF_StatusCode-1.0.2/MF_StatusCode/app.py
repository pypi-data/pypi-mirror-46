#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import copy


class StatusCode():
    def __init__(self):  # 初始化并加载统一状态码
        self.statusCode = {}

    def get_code(self, code):
        try:
            statusCode = copy.deepcopy(self.statusCode[str(code)])
            return statusCode
        except Exception as e:
            return {
                "code": "STATUS4002",
                "msg": "获取状态代码失败",
                "error": str(e)
            }

    def add_status_code(self, file_path):
        try:
            statusCode = ""
            file_txt = open(file_path, 'r', encoding='utf8')
            for line in file_txt.readlines():  # 依次读取每行
                if line != "":
                    statusCode += line

            # 关闭文件
            file_txt.close()
            statusCode = json.loads(statusCode)
            for x in statusCode:
                self.statusCode[x] = statusCode[x]
        except Exception as e:
            return {
                "code": "STATUS4003",
                "msg": "添加状态代码失败",
                "error": str(e)
            }
