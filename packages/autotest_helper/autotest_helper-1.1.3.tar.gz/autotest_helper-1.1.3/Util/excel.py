#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/1/25 14:33
@Describe: 
"""
import xlrd
import xlwt
from xlutils.copy import copy


class Excel:
    """
        Excel工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def create_xml(list_name=None, excel_path="", list_width=None):
        """
            创建初始的excel表格
        :param list_name: list类型，每一列表格的title
        :param excel_path: excel表格的存储位置
        :param list_width: list类型，每一列表格的宽度
        """
        if list_width is None:
            list_width = []
        if list_name is None:
            list_name = []
        workbook = xlwt.Workbook()
        # 创建居中
        alignment = xlwt.Alignment()
        # 可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER
        # 创建样式
        style = xlwt.XFStyle()
        # 给样式添加文字居中属性
        style.alignment = alignment
        # 设置字体大小
        style.font.height = 430
        sheet = workbook.add_sheet("user Information")
        for i in range(len(list_name)):
            sheet.write(0, i, list_name[i].__str__(), style)
            sheet.col(i).width = int(list_width[i].__str__()) * 30
        workbook.save(excel_path)

    @staticmethod
    def add_excel(excel_path="", list_value=None):
        """
            为excel追加数据
        :param excel_path:
        :param list_value:
        """
        # 创建居中
        if list_value is None:
            list_value = []
        alignment = xlwt.Alignment()
        # 可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER
        # 创建样式
        style = xlwt.XFStyle()
        # 给样式添加文字居中属性
        style.alignment = alignment
        # 设置字体大小
        style.font.height = 215
        workbook = xlrd.open_workbook(excel_path, formatting_info=True)
        sheet = workbook.sheet_by_name("user Information")
        nrows = sheet.nrows
        print("当前文件的行数为：" + nrows.__str__())
        workbook_now = copy(workbook)
        sheet_now = workbook_now.get_sheet("user Information")
        for i in range(len(list_value)):
            sheet_now.write(nrows, i, list_value[i].__str__(), style)
        workbook_now.save(excel_path)

    @staticmethod
    def get_excel(excel_path=""):
        """
            获取excel表格中的内容，返回list【】【】的形式
        :param excel_path:
        :return:
        """
        workbook = xlrd.open_workbook(excel_path, formatting_info=True)
        sheet = workbook.sheet_by_name("user Information")
        nrows = sheet.nrows  # 获取excel表格的行数
        rows = sheet.ncols  # 获取excel表格的列数
        list_result = []
        for i in range(1, nrows):
            list_col = []
            for t in range(rows):
                list_col.append(sheet.cell(i, t).value)
            list_result.append(list_col)
        return list_result

    @staticmethod
    def change_excel(excel_path="", rows=0, cols=0, date=""):
        """
            修改已存在的指定行列内的内容
        :param cols: 需要修改的列数
        :param excel_path:
        :param rows: 需要修改的行数
        :param date: 希望修改填充的数据
        """
        # 创建居中
        alignment = xlwt.Alignment()
        # 可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER
        # 创建样式
        style = xlwt.XFStyle()
        # 给样式添加文字居中属性
        style.alignment = alignment
        # 设置字体大小
        style.font.height = 215
        workbook = xlrd.open_workbook(excel_path, formatting_info=True)
        workbook_now = copy(workbook)
        sheet_now = workbook_now.get_sheet("user Information")
        sheet_now.write(rows, cols, date, style)
        workbook_now.save(excel_path)
