import base64
import os
import time
import requests
from PIL import Image
import ybc_config
from ybc_exception import *
import sys

__BASIC_URL = ybc_config.config['prefix']+ ybc_config.uri
__MERGE_URL = __BASIC_URL + "/faceMerge/base64"
__DECORATATION_URL = __BASIC_URL + "/faceDecoration/base64"


def _resize_img(filepath,max_size=512000):
    # MAX_FILE_SIZE = max_size
    filesize = os.path.getsize(filepath)
    # if filesize > MAX_FILE_SIZE :
    im = Image.open(filepath)
    src_w = im.size[0]
    src_h = im.size[1]
    dst_w = 460
    dst_h = (src_h/src_w) * 460
    dst_size = dst_w , dst_h
    im.thumbnail(dst_size)
    im.save(filepath)
    return filepath


def meizhuang(filename='', meitype='日系妆-芭比粉'):
    """
    功能：人脸美妆。

    参数 filename 是待美妆的图片名字，

    可选参数 meitype 是美妆类型，默认是 "日系妆-芭比粉"，

    返回：美妆后的图片。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(meitype, str):
        if error_flag == -1:
            error_msg += "、'meitype'"
        else:
            error_flag = -1
            error_msg += "'meitype'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if meitype not in meizhuang_type():
        if error_flag == -1:
            error_msg += "、'meitype'"
        else:
            error_flag = -1
            error_msg += "'meitype'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        cosmetic_type = meizhuang_type()
        cosmetic = cosmetic_type.index(meitype) + 1

        filepath = os.path.abspath(filename)
        filepath = _resize_img(filepath)
        url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceCosmetic.php'
        with open(filepath, 'rb') as fp:
            b64img= base64.b64encode(fp.read()).rstrip().decode('utf-8')
        data = {}
        data['b64img'] = b64img
        data['cosmetic'] = cosmetic
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            # 识别不到人脸时不会通过该检查
            if res['ret'] == 0 and res['data']:
                new_file = os.path.splitext(filename)[0] +  '_' + str(int(time.time())) + '_meizhuang' + os.path.splitext(filename)[1]
                with open(new_file,'wb') as f:
                    f.write(base64.b64decode(res['data']['image']))
                return new_file
            else:
                return '图片中找不到人哦~'
        raise ConnectionError("获取美妆图片失败", r.content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face_ps')


def meizhuang_type(flag=1):
    """
    功能：获取美妆类型。

    可选参数 flag，1 代表返回列表，默认为 1，

    返回：美妆类型列表或字典。
    """
    MEIZHUANG_TYPE = {
    1:'日系妆-芭比粉',
    2:'日系妆-清透',
    3:'日系妆-烟灰',
    4:'日系妆-自然',
    5:'日系妆-樱花粉',
    6:'日系妆-原宿红',
    7:'韩妆-闪亮',
    8:'韩妆-粉紫',
    9:'韩妆-粉嫩',
    10:'韩妆-自然',
    11:'韩妆-清透',
    12:'韩妆-大地色',
    13:'韩妆-玫瑰',
    14:'裸妆-自然',
    15:'裸妆-清透',
    16:'裸妆-桃粉',
    17:'裸妆-橘粉',
    18:'裸妆-春夏',
    19:'裸妆-秋冬',
    20:'主题妆-经典复古',
    21:'主题妆-性感混血',
    22:'主题妆-炫彩明眸',
    23:'主题妆-紫色魅惑',
    }
    if flag == 1:
        return list(MEIZHUANG_TYPE.values())
    else:
        return MEIZHUANG_TYPE


def bianzhuang(filename='', biantype='灰姑娘妆'):
    """
    功能：人脸变妆。

    参数 filename 是待处理的人脸图片，

    可选参数 biantype 是妆容类型，默认是 灰姑娘妆，

    返回：美妆过的人脸图片。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(biantype, str):
        if error_flag == -1:
            error_msg += "、'biantype'"
        else:
            error_flag = -1
            error_msg += "'biantype'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if biantype not in bianzhuang_type():
        if error_flag == -1:
            error_msg += "、'biantype'"
        else:
            error_flag = -1
            error_msg += "'biantype'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        decoration_type = bianzhuang_type()
        decoration = decoration_type.index(biantype) + 1

        filepath = os.path.abspath(filename)
        filepath = _resize_img(filepath)

        url = __DECORATATION_URL
        with open(filepath, 'rb') as fp:
            b64img= base64.b64encode(fp.read()).rstrip().decode('utf-8')
        data = {}
        data['image'] = b64img
        data['decoration'] = decoration
        headers = {'content-type': "application/json"}
        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                res = r.json()
                # 识别不到人脸时不会通过该检查
                if res['ret'] == 0 and res['data']:
                    new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_bianzhuang' + \
                               os.path.splitext(filename)[1]
                    with open(new_file, 'wb') as f:
                        f.write(base64.b64decode(res['data']['image']))
                    return new_file
                else:
                    return '图片中找不到人哦~'
        raise ConnectionError('人脸美妆失败', r._content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face_ps')


def bianzhuang_type(flag=1):
    """
    功能：获取变妆类型。

    可选参数 flag，1 代表返回列表，默认为 1，

    返回：变妆类型列表或字典。
    """
    BIANZHUANG_TYPE = {
    1:'埃及妆',
    2:'巴西土著妆',
    3:'灰姑娘妆',
    4:'恶魔妆',
    5:'武媚娘妆',
    6:'星光薰衣草',
    7:'花千骨',
    8:'僵尸妆',
    9:'爱国妆',
    10:'小胡子妆',
    11:'美羊羊妆',
    12:'火影鸣人妆',
    13:'刀马旦妆',
    14:'泡泡妆',
    15:'桃花妆',
    16:'女皇妆',
    17:'权志龙',
    18:'撩妹妆',
    19:'印第安妆',
    20:'印度妆',
    21:'萌兔妆',
    22:'大圣妆'
    }
    if flag == 1:
        return list(BIANZHUANG_TYPE.values())
    else:
        return BIANZHUANG_TYPE


def ronghe(filename='', rongtype='东营小枫'):
    """
    功能：人脸融合。

    参数 filename 是待处理的人脸图片，

    可选参数 rongtype 是融合类型，默认是 篮球队长，

    返回：融合过的人脸图片。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(rongtype, str):
        if error_flag == -1:
            error_msg += "、'rongtype'"
        else:
            error_flag = -1
            error_msg += "'rongtype'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if rongtype not in ronghe_type():
        if error_flag == -1:
            error_msg += "、'rongtype'"
        else:
            error_flag = -1
            error_msg += "'rongtype'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        model_type = ronghe_type()
        model = model_type.index(rongtype) + 1

        filepath = os.path.abspath(filename)
        filepath = _resize_img(filepath)
        url = __MERGE_URL
        with open(filepath, 'rb') as fp:
            b64img= base64.b64encode(fp.read()).rstrip().decode('utf-8')
        data = {}
        data['image'] = b64img
        data['model'] = model
        headers = {'content-type': "application/json"}
        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                res = r.text
                if res:
                    new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_ronghe' + '.png'
                    with open(new_file, 'wb') as f:
                        f.write(requests.get(res).content)
                    return _resize_img(new_file)
                else:
                    return '图片中找不到人哦~'
        raise ConnectionError('人脸融合失败', r._content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face_ps')


def ronghe_type(flag=1):
    """
    功能：获取融合类型。

    可选参数 flag，1 代表返回列表，默认为 1，

    返回：融合类型列表或字典。
    """
    RONGHE_TYPE = {
	1: '东宫小枫',
	2: '江湖侠女',
	3: '青春风采',
	4: '花园公主',
	5: '玛丽学院',
	6: '诗仙李白',
	7: '江湖侠客',
	8: '白衣少年',
	9: '青春少年',
	10: '刘海少年'
    }
    if flag == 1:
        return list(RONGHE_TYPE.values())
    else:
        return RONGHE_TYPE


def datoutie(filename='', sticker='NewDay'):
    """
    功能：制作大头贴。

    参数 filename 是用来制作大头贴的照片名字，

    可选参数 sticker 是大头贴背景类型，默认是 NewDay，

    返回：制作的大头贴图片。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(sticker, str):
        if error_flag == -1:
            error_msg += "、'sticker'"
        else:
            error_flag = -1
            error_msg += "'sticker'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if sticker not in datoutie_type():
        if error_flag == -1:
            error_msg += "、'sticker'"
        else:
            error_flag = -1
            error_msg += "'sticker'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        sticker_type = datoutie_type()
        sticker = sticker_type.index(sticker) + 1

        url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceSticker.php'
        filepath = os.path.abspath(filename)
        with open(filepath, 'rb') as fp:
            b64img= base64.b64encode(fp.read()).rstrip().decode('utf-8')
        data = {}
        data['b64img'] = b64img
        data['sticker'] = sticker
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            # 识别不到人脸时不会通过该检查
            if res['ret'] == 0 and res['data']:
                new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_datoutie'+os.path.splitext(filename)[1]
                with open(new_file,'wb') as f:
                    f.write(base64.b64decode(res['data']['image']))
                return new_file
            else:
                return '图片中找不到人哦~'
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face_ps')


def datoutie_type(flag=1):
    """
    功能：获取大头贴背景类型。

    可选参数 flag，1 代表返回列表，默认为 1，

    返回：大头贴背景类型列表或字典。
    """
    STICKER_TYPE = {
    1:	'NewDay',
    2:	'欢乐球吃球1:',
    3:	'Bonvoyage',
    4:	'Enjoy',
    5:	'ChickenSpring',
    6:	'ChristmasShow',
    7:	'ChristmasSnow',
    8:	'CircleCat',
    9:	'CircleMouse',
    10:	'CirclePig',
    11:	'Comicmn',
    12:	'CuteBaby',
    13:	'Envolope',
    14:	'Fairytale',
    15:	'GoodNight',
    16:	'HalloweenNight',
    17:	'LovelyDay',
    18:	'Newyear2017',
    19:	'PinkSunny',
    20:	'KIRAKIRA',
    21:	'欢乐球吃球2:',
    22:	'SnowWhite',
    23:	'SuperStar',
    24:	'WonderfulWork',
    25:	'Cold',
    26:	'狼人杀守卫',
    27:	'狼人杀猎人',
    28:	'狼人杀预言家',
    29:	'狼人杀村民',
    30:	'狼人杀女巫',
    31:	'狼人杀狼人'
    }
    if flag == 1:
        return list(STICKER_TYPE.values())
    else:
        return STICKER_TYPE


def main():
    print(meizhuang('cup.jpg'))
    print(bianzhuang('cup.jpg'))
    print(ronghe('cup.jpg'))
    print(datoutie('cup.jpg'))
    # res = meizhuang('test.jpg','日系妆-烟灰')
    # print(res)
    # res = bianzhuang('test.jpg')
    # print(res)
    # res = ronghe('test.jpg')
    # print(res)
    # bianzhuang('test.jpg')
    # ronghe('test.jpg')


if __name__ == '__main__':
    # main()
    print(ronghe('test.jpg'))