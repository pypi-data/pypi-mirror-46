#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:杨涛
@file: operate_excel.py
@time: 2019/05/22
"""
import xlrd


class OperationExcel():
    def __init__(self,file_name):
        # 获取文件名
        self.file_name = file_name
        # 获取excel表格中所有数据，以sheel表名为key，数据为value
        self.sheel_data = self.get_sheel_data()
        # 获取各sheel表的总行数，以sheel表名为key，总行数为value
        self.sheel_nrows = self.get_sheel_nrows()
        # 获取各sheel表的总列数，以sheel表名为key，总列数为value
        self.sheel_ncols = self.get_sheel_ncols()
        # 获取excel文件中各sheel表的表名，列表展示
        self.sheel_names = self.get_sheel_names()
        # 获取excel文件中，所有sheel的总行数
        self.nrows = self.get_nrows()
        # 获取excel文件中，所有sheel的总列数
        self.ncols = self.get_ncols()
        # 获取excel表对象
        self.excel_obj = self.get_excel_obj()

    def get_excel_obj(self):
        """
        获取excel表对象
        :return:
        """
        excel = xlrd.open_workbook(self.file_name)
        return excel

    def get_sheel_names(self):
        """
        # 获取excel文件中各sheel表的表名，列表展示
        :return:
        """
        excel = xlrd.open_workbook(self.file_name)
        sheel_names = excel.sheet_names()
        return sheel_names

    def get_sheels(self):
        """
        获取excel对象和所有sheel表名
        :return:
        """
        excel = xlrd.open_workbook(self.file_name)
        sheel_names = excel.sheet_names()
        return excel,sheel_names

    def get_sheel_data(self):
        """
        获取excel表格中所有数据，以sheel表名为key，数据为value
        :return:
        """
        excel, sheel_names = self.get_sheels()
        data_dict = {}
        for name in sheel_names:
            sheel = excel.sheet_by_name(name)
            row,col = sheel.nrows,sheel.ncols
            # 表为空表
            if row == 0 and col==0:
                data_dict[name] = []
            else:
                header = sheel.row_values(0)
                sheel_list = []
                for r in range(1, sheel.nrows):
                    d = dict(zip(header, sheel.row_values(r)))
                    sheel_list.append(d)
                data_dict[name] = sheel_list
        return data_dict

    def get_sheel_nrows(self):
        """
        获取各sheel表的总行数，以sheel表名为key，总行数为value
        :return:
        """
        excel, sheel_names = self.get_sheels()
        nrows_dict = {}
        for name in sheel_names:
            sheel = excel.sheet_by_name(name)
            nrows = sheel.nrows
            nrows_dict[name] = nrows
        return nrows_dict

    def get_sheel_ncols(self):
        """
        获取各sheel表的总列数，以sheel表名为key，总列数为value
        :return:
        """
        excel, sheel_names = self.get_sheels()
        ncols_dict = {}
        for name in sheel_names:
            sheel = excel.sheet_by_name(name)
            ncols = sheel.ncols
            ncols_dict[name] = ncols
        return ncols_dict

    def get_nrows(self):
        """
        excel中，所有sheel表的总行数
        :return:
        """
        num = 0
        excel, sheel_names = self.get_sheels()
        for name in sheel_names:
            sheel = excel.sheet_by_name(name)
            nrows = sheel.nrows
            num += nrows
        return num

    def get_ncols(self):
        """
        excel中，所有sheel表的总列数
        :return:
        """
        num = 0
        excel, sheel_names = self.get_sheels()
        for name in sheel_names:
            sheel = excel.sheet_by_name(name)
            ncols = sheel.ncols
            num += ncols
        return num






if __name__ == "__main__":
    da = OperationExcel()
    tt = da.sheel_data
    print("数据",tt)
    sheel_nrows = da.sheel_nrows
    print("各表总行数",sheel_nrows)
    sheel_ncols = da.sheel_ncols
    print("各表总列数", sheel_ncols)
    sheel_names = da.sheel_names
    print("表名", sheel_names)
    nrows = da.nrows
    print("总行数", nrows)
    ncols = da.ncols
    print("总列数", ncols)