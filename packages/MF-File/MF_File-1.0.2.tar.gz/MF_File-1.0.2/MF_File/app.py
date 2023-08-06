#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from MF_StatusCode import StatusCode
from MF_File.config import ROOT_DIR, STATUS_CODE


class File(StatusCode):  # txt文件操作类

    def __init__(self):
        StatusCode.__init__(self)
        self.add_status_code(STATUS_CODE)

    def read_file(self, data_path):  # 读文件
        try:
            txt_list = ""
            file_txt = open(data_path, 'r', encoding='utf8')
            for line in file_txt.readlines():  # 依次读取每行
                if line != "":
                    txt_list += line

            file_txt.close()  # 关闭文件
            statusCode = self.get_code("F2000")
            statusCode["data"] = txt_list
            return statusCode
        except BaseException as e:
            statusCode = self.get_code("F4001")
            statusCode["error"] = str(e)
            return statusCode

    def read_file_strip(self, data_path):  # 读文件并去除空格
        try:
            txt_list = []
            file_txt = open(data_path, 'r', encoding='utf8')
            for line in file_txt.readlines():  # 依次读取每行
                line = line.strip()  # 去掉每行头尾空白
                if line != "":
                    txt_list.append(line)

            file_txt.close()  # 关闭文件
            statusCode = self.get_code("F2000")
            statusCode["data"] = txt_list
            return statusCode
        except BaseException as e:
            statusCode = self.get_code("F4002")
            statusCode["error"] = str(e)
            return statusCode

    def read_file_buffer(self, data_path):  # 读取二进制文件
        try:
            file_txt = open(data_path, 'rb')
            txt_list = file_txt.read()
            file_txt.close()  # 关闭文件
            statusCode = self.get_code("F2000")
            statusCode["data"] = txt_list
            return statusCode
        except BaseException as e:
            statusCode = self.get_code("F4005")
            statusCode["error"] = str(e)
            return statusCode

    def write_file(self, data_path, txt):  # 写文件
        try:
            file_txt = open(data_path, mode='a', encoding='utf8')
            file_txt.write(txt)
            file_txt.close()  # 关闭文件
            statusCode = self.get_code("F2000")
            return statusCode
        except BaseException as e:
            statusCode = self.get_code("F4003")
            statusCode["error"] = str(e)
            return statusCode

    def cover_file(self, data_path, txt):  # 覆盖写入文件
        try:
            file_txt = open(data_path, mode='w', encoding='utf8')
            file_txt.write(txt)
            file_txt.close()  # 关闭文件
            statusCode = self.get_code("F2000")
            return statusCode
        except BaseException as e:
            statusCode = self.get_code("F4004")
            statusCode["error"] = str(e)
            return statusCode

    def cover_file_buffer(self, data_path, txt):  # 覆盖写入二进制文件
        try:
            file_txt = open(data_path, mode='wb')
            file_txt.write(txt)
            file_txt.close()  # 关闭文件
            statusCode = self.get_code("F2000")
            return statusCode
        except BaseException as e:
            statusCode = self.get_code("F4006")
            statusCode["error"] = str(e)
            return statusCode
