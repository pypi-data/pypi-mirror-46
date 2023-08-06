#!/usr/bin/env python
# -*- coding: utf-8 -*-
from MF_Version.config import STATUS_CODE
from MF_File import File


class Version(File):  # 版本号操作类
    def __init__(self):
        File.__init__(self)
        self.add_status_code(STATUS_CODE)

    def set_version_path(self, file_path):  # 设置版本号文件地址
        try:
            self.versionPath = file_path
        except BaseException as e:
            errorCode = self.get_code("V4001")
            errorCode["error"] = e
            return errorCode

    def set_version(self):  # 修改版本号
        try:
            # 读取版本文件

            version_txt = self.read_file(self.versionPath)
            new_version = ""
           
            version_length = len(version_txt["data"].split("."))

            # 修改版本文件
            for i in version_txt["data"].split("."):
                if version_length == 1:
                    version_length = version_length - 1
                    new_version += str(int(i) + 1)
                else:
                    version_length = version_length - 1
                    new_version += i + "."
            # 写入版本号
            self.cover_file(self.versionPath, new_version)
            return self.get_code("V2000")
        except BaseException as e:
            errorCode = self.get_code("V4002")
            errorCode["error"] = e
            return errorCode
