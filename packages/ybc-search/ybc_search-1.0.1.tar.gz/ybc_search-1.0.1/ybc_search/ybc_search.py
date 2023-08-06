import os.path
import time
from random import randint
import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__PIC_SEARCH_URL = __PREFIX + ybc_config.uri + '/picSearch'
__ARTICLE_SEARCH_URL = __PREFIX + ybc_config.uri + '/articles/search'


def pic_search(keyword='', total=10):
    """
    功能：搜索图片并下载。
    参数 keyword: 搜索关键词。
    可选参数 total: 本次下载图片数量，默认为10，最大为 30。
    返回: 无。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(keyword, str):
        error_flag = -1
        error_msg += "'keyword'"
    if not isinstance(total, int):
        if error_flag == -1:
            error_msg += "、'total'"
        else:
            error_flag = -1
            error_msg += "'total'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not keyword:
        error_flag = -1
        error_msg += "'keyword'"
    if total < 1 or total > 30:
        if error_flag == -1:
            error_msg += "、'total'"
        else:
            error_flag = -1
            error_msg += "'total'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        url = __PIC_SEARCH_URL
        data = {
            'keyWord': keyword,
            'total': total
        }
        headers = {'content-type': "application/json"}

        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                pic_url = r.json()
                break
            elif i == 2:
                raise ConnectionError("搜索图片失败", r.content)

        url_count = len(pic_url)
        if url_count < 1:
            print("搜索不到相关图片")
            return -1

        print('找到关键词为: ' + keyword + ' 的图片，现在开始下载图片...')
        count = 0
        for key in pic_url:
            if count == total:
                break
            print('正在下载第' + str(count + 1) + '张图片，图片地址:' + str(key))
            try:
                pic = requests.get(key, timeout=10)
            except requests.exceptions.ConnectionError:
                print('【错误】当前图片无法下载')
                continue

            dir_path = keyword
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            tag = time.strftime('%H%M%S', time.localtime(time.time())) + '.' + str(randint(1000, 9999))
            filename = dir_path + '/' + keyword + '_' + str(count) + '_' + tag + '.jpg'
            fp = open(filename, 'wb')
            fp.write(pic.content)
            fp.close()
            count += 1
        print('下载完成！')
        return 0
    except Exception as e:
        raise InternalError(e, 'ybc_search')


def article_search(keyword=''):
    """
    功能：搜索小学课文，并返回文本文件。

    参数 keyword: 搜索关键词。
    返回: 文件名称。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(keyword, str):
        error_flag = -1
        error_msg += "'keyword'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not keyword:
        error_flag = -1
        error_msg += "'keyword'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        url = __ARTICLE_SEARCH_URL
        data = {
            'keyword': keyword
        }
        for i in range(3):
            r = requests.get(url, data)
            if r.status_code == 200:
                res = r.json()
                file = open(res['title'] + '.txt', 'w', encoding= 'utf-8')
                file.write(res['content'])
                file.close()
                return file.name
            elif r.status_code == 404:
                print("未找到对应课文")
                return -1
        raise ConnectionError("搜索文章失败", r.content)

    except Exception as e:
        raise InternalError(e, 'ybc_search')


def main():
    pic_search('彭于晏')
    article_search('称赞')


if __name__ == '__main__':
    main()
