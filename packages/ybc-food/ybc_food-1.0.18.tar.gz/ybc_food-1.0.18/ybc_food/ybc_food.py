import operator
import os
import requests
import ybc_config
from ybc_exception import *
import sys

__PREFIX = ybc_config.config['prefix']
__FOOD_URL = __PREFIX + ybc_config.uri + '/food'


__TOP_NUM = 3
__NOT_FOOD = '非菜'


def check(filename=''):
    """
    功能：识别一个图片是否为美食图片。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：是否为美食。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    ybc_config.resize_if_too_large(filename)
    res = food_name(filename, 1)
    if res == __NOT_FOOD:
        return False
    return True


def food(filename='', topNum=__TOP_NUM):
    """
    功能：美食识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，范围为 1-10，默认为 3 ，

    返回：图片的美食信息。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(topNum, int):
        if error_flag == -1:
            error_msg += "、'topNum'"
        else:
            error_flag = -1
            error_msg += "'topNum'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if topNum < 1 or topNum > 10:
        if error_flag == -1:
            error_msg += "、'topNum'"
        else:
            error_flag = -1
            error_msg += "'topNum'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        ybc_config.resize_if_too_large(filename)
        url = __FOOD_URL
        filepath = os.path.abspath(filename)
        fo = open(filepath, 'rb')
        files = {
            'file': fo
        }
        data = {
            'topNum': topNum
        }
        for i in range(3):
            r = requests.post(url, files=files, data=data)
            if r.status_code == 200:
                res = r.json()
                # 不论是否识别出图片均有 result 字段
                if res['result']:
                    fo.close()
                    res = res['result']
                    for j in range(len(res)):
                        res[j]['calorie'] = int(res[j]['calorie'])
                        res[j]['probability'] = float(res[j]['probability'])
                    return res

        fo.close()
        raise ConnectionError('识别美食图片失败', r._content)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except ValueError:
        return -1
    except Exception as e:
        raise InternalError(e, 'ybc_food')


def food_name(filename='', topNum=__TOP_NUM):
    """
    功能：美食名字识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：美食的名字。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(topNum, int):
        if error_flag == -1:
            error_msg += "、'topNum'"
        else:
            error_flag = -1
            error_msg += "'topNum'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if topNum < 1 or topNum > 10:
        if error_flag == -1:
            error_msg += "、'topNum'"
        else:
            error_flag = -1
            error_msg += "'topNum'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    ybc_config.resize_if_too_large(filename)
    res = food(filename, topNum)
    if res == -1:
        return res
    if topNum == 1:
        return res[0]['name']
    else:
        sorted_res = sorted(res, key=operator.itemgetter('probability'), reverse=True)
        return sorted_res[0]['name']


def main():
    print(food('test.jpg', 2))
    # print(food_name('test.jpg'))
    # print(check('test.jpg'))
    pass


if __name__ == '__main__':
    main()
