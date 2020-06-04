import os
import hashlib
import logging
import sys
import time
from os import walk, path, mkdir
from hashlib import md5
from shutil import copy, move

def logger():
    """ 获取logger"""
    logger = logging.getLogger()
    if not logger.handlers:
        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        # 文件日志
        file_handler = logging.FileHandler("dup.log")
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值
        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)
    return logger


def get_md5(fname):
    m = md5()
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def get_file_size(filename):
    filesize = os.path.getsize(filename)
    return filesize


def check_empty_folder(base):
    empty_folders = []
    for root, dirs, files in os.walk(base):  # ignore subdirectories here
        if dirs == [] and files == []:
            empty_folders.append(root)
    return empty_folders


if __name__ == '__main__':
    log = logger()
    sizedict = dict()
    md5dict = dict()
    base = "F:\\yellow\\"
    # urlList = get_urllist(base)
    count = 0
    total = 0
    # 删除重复文件
    print("开始删除重复文件")
    time_start = time.time()
    the_time = time.time()
    for root, dirs, files in os.walk(base):  # ignore subdirectories here
        for name in files:
            file = os.path.join(root, name)
    # for file in urlList:
            total += 1
            if total % 10000 == 0:
                print("运行到了", total)
            if total % 10000 == 0:
                print(time.time()-the_time,"s")
                the_time = time.time()
            filesize = get_file_size(file)

            if filesize in sizedict:  # 存在相同大小的文件

                md51 = get_md5(file)  # 获取当前文件md5值
                for path in sizedict[filesize]:  # 获取之前文件md5
                    if path in md5dict:
                        the_md5 = md5dict[path]
                    else:
                        the_md5 = get_md5(path)
                        md5dict[path] = the_md5
                    if the_md5 == md51:  # 相同,删除当前文件
                        try:
                            os.remove(file)
                            print("重复：" + file + " | " + path)
                            log.info("重复：" + file + "\n                                  " + path)
                            count += 1
                        except Exception as ex:
                            print("出错: %s" % ex)
                            log.info("出错: %s" % ex)
            else:  # 存储文件大小和路径
                if filesize in sizedict:
                    sizedict[filesize].append(file)
                else:
                    sizedict[filesize] = [file]
    print("一共 " + str(len(sizedict)) + " 文件,删除了 " + str(count) + " 文件")

    # 删除空文件夹
    print("\n开始删除重复文件夹")
    empty_folders = check_empty_folder(base)
    for folder in empty_folders:
        try:
            os.rmdir(folder)
            print("空文件夹：%s" % folder)
            log.info("空文件夹：%s" % folder)
        except Exception as ex:
            print("出错: %s" % ex)
            log.info("出错: %s" % ex)
    print("一共删除了 " + str(len(empty_folders)) + " 个空文件夹")
    print("total time: ", time.time()-time_start)