'''
 * @Descripttion : 主方法
 * @Author       : Tommy
 * @Date         : 2021-01-07 17:16:12
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-11-17 11:35:02
'''
import os
import datetime
from loguru import logger
from download_tool import DownloadTool
from excel_operation import Excel_operation
from handle_excel import excel


def downloadtime_statistics(Downobject, filename):
    logger.debug("资源开始下载")
    now_time = datetime.datetime.now()
    # TODO: 下载资源方法
    Downobject.download_file(filename)
    end_time = datetime.datetime.now()
    download_singlefile_time = (end_time - now_time).microseconds / 1000
    logger.debug("资源下载结束,耗时(ms)：" + str(download_singlefile_time))
    return download_singlefile_time


def remove_suffix(filename):
    file_name_without_suffix = os.path.splitext(filename)[0]
    return file_name_without_suffix


def main(excel_filename, sheet_name, host_url, sheet_index):
    # # 打开excel文件
    # excel_operation = Excel_operation(excel_filename)
    # excel_object = excel_operation.excel_open()
    # # 获取excel表对象
    # table = excel_operation.get_table_by_sheetname(excel_object, sheet_name)
    # # 获取table行数
    # rows = excel_operation.get_table_rows(table)
    rows = excel.get_rows(sheet_index)
    # 进入循环
    for row in range(1, int(rows)):
        resource_name = excel_operation.excel_celldata_return(row, 0, table)
        # 根据sheet_name来重组color的host_url
        if sheet_name == "coloring":
            file_name_without_suffix = remove_suffix(resource_name)
            host_url = host_url + file_name_without_suffix
        logger.debug("资源名称：" + resource_name)
        # TODO: 调用下载方法，返回资源下载时间
        Downobject = DownloadTool(host_url)
        download_singlefile_time = downloadtime_statistics(
            Downobject, resource_name)
        # TODO: 调用写入excel方法，写入资源下载时间
        excel_operation.excel_celldata_add(
            row, 2, sheet_name, download_singlefile_time)


if __name__ == "__main__":
    booking_host = "http://zhangxiaobog.cdn-doodlemobile.com/color_book_b/zips/"
    coloring_host = "http://tapcolor-google-cdn.weplayer.cc/color/1.0/pics/"
    main("resource.xls", "booking", booking_host)
    main("resource.xls", "coloring", coloring_host)
