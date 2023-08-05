import base64
import os
import tempfile
import time
from io import BytesIO

import requests
from PIL import Image

import ybc_config
from ybc_exception import *

__BASIC_URL = ybc_config.config['prefix'] + ybc_config.uri
__MERGE_URL = __BASIC_URL + '/faceMerge/base64'
__FACE_DETECTION_URL_V2 = __BASIC_URL + '/face-detect'
__FACE_COMPARE_URL_V2 = __BASIC_URL + '/face-compare'
__MAX_FACE_NUM = 5


def _resize_img(file_path, temp_file=None):
    """
    对图片进行缩放, 如果是临时图片文件, 则必须传文件对象,
    因为在 windows 系统下 NamedTemporaryFile 不能二次打开, 但是可以直接读写

    :param file_path: 原文件路径
    :param temp_file: 临时文件对象
    :return:
        如果传入临时文件对象, 返回临时文件路径, 否则返回原文件路径
    """
    try:
        im = Image.open(file_path)
        src_w = im.size[0]
        src_h = im.size[1]
        dst_w = 500
        dst_h = (src_h / src_w) * 500
        dst_size = dst_w, dst_h

        im.thumbnail(dst_size)
        if temp_file:
            im.save(temp_file)
            temp_file.seek(0)
            return temp_file.name
        else:
            im.save(file_path)
            return file_path
    except Exception as e:
        raise InternalError(e, 'ybc_face')


def _detect_face(filename='', max_face_num=1):
    """
    功能: 对图片进行人脸检测

    :param filename: 图片名
    :param max_face_num: 检测人脸数量范围 1 ~ 5
    :return:
        成功: 返回包含人脸信息的字典
        失败: -1
    """
    file = os.path.abspath(filename)
    image_b64 = _get_image_b64(file)

    url = __FACE_DETECTION_URL_V2
    payload = {'image': image_b64, 'maxFaceNum': max_face_num}

    r = requests.post(url, data=payload)
    if r.status_code != 200:
        raise ConnectionError("获取人脸信息失败", r.content)

    if len(r.json()) <= 0:
        raise ReturnValueError("图片中找不到人哦~")
    else:
        data = [data['faceAttributesInfo'] for data in r.json()]
        return data if max_face_num > 1 else data[0]


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def gender1(filename=''):
    """
    功能：识别人脸图片的性别信息。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的性别信息[0(女性)~100(男性)]。
    """
    def _gender(data):
        return data['gender']

    return _gender(_detect_face(filename, 1))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def gender(filename=''):
    """
    功能：识别人脸图片的性别。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的性别。
    """
    def _gender(data):
        return '男' if data['gender'] > 50 else '女'

    return _gender(_detect_face(filename, 1))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def age(filename=''):
    """
    功能：识别人脸图片的年龄信息。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的年龄信息[0~100]。
    """
    def _age(data):
        return data['age']

    return _age(_detect_face(filename))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def glass1(filename=''):
    """
    功能：识别人脸图片的是否戴眼镜。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的是否戴眼镜。
    """
    def _glass(data):
        return bool(data['glass'])

    return _glass(_detect_face(filename))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def glass(filename=''):
    """
    功能：识别人脸图片的是否戴眼镜。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的是否戴眼镜。
    """
    def _glass(data):
        return data['glass']

    return _glass(_detect_face(filename))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def beauty(filename=''):
    """
    功能：识别人脸图片的魅力值。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的魅力值 [0~100]。
    """
    def _beauty(data):
        return data['beauty']

    return _beauty(_detect_face(filename))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def info(filename=''):
    """
    功能：识别图片中一张人脸信息。

    参数 filename 是待识别的人脸图片，

    返回：识别出的人脸信息。
    """
    def _info(data):
        return _compose_message(data)

    return _info(_detect_face(filename))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty)
])
def info_all(filename=''):
    """
    功能：识别图片中所有人脸信息。

    参数 filename 是待识别的图片，

    返回：识别出的所有人脸信息。
    """
    def _info_all(data):
        messages = ['第{}个人脸信息：'.format(i + 1) + _compose_message(data) for i, data in enumerate(data)]
        return '图片中总共发现{}张人脸：'.format(len(messages)) + os.linesep + os.linesep.join(messages)

    return _info_all(_detect_face(filename, __MAX_FACE_NUM))


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty),
    ParamCheckEntry('decoration', int, is_in_range, Range(1, 22))
])
def ps(filename='', decoration=21):
    """
    功能：人脸变妆。

    参数 filename 是待变妆的图片，

    可选参数 decoration 是变妆编码，范围 1-22，默认为 21(萌兔妆)，

    返回：变妆后的图片。
    """
    try:
        file_path = os.path.abspath(filename)
        # 为了检测 file_path 参数是否合法，不合法抛出异常
        f = open(file_path)
        f.close()
        basename, suffix = os.path.splitext(filename)
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        _resize_img(file_path, temp_file)
        url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceDecoration.php'

        b64img = base64.b64encode(temp_file.read()).rstrip().decode('utf-8')
        data = {'b64img': b64img, 'decoration': decoration}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            if res['ret'] == 0 and res['data']:
                new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + os.path.splitext(filename)[1]
                with open(new_file, 'wb') as f:
                    f.write(base64.b64decode(res['data']['image']))
                temp_file.close()
                return new_file
            else:
                raise ReturnValueError("图片中找不到人哦~")
        temp_file.close()
        raise ConnectionError("获取变妆图片失败", r.content)

    except (ParameterValueError, ParameterTypeError, ReturnValueError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face')


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str, is_not_empty),
    ParamCheckEntry('model', int, is_in_range, Range(1, 10))
])
def mofa(filename='', model=1):
    """
    功能：人脸融合。

    参数 filename 是待融合的图片，

    可选参数 model 是模特编码，范围 1-10，默认为 1，

    返回：融合后的图片。
    """
    try:
        file_path = os.path.abspath(filename)
        # 为了检测 file_path 参数是否合法，不合法抛出异常
        f = open(file_path)
        f.close()
        basename, suffix = os.path.splitext(filename)
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        _resize_img(file_path, temp_file)
        url = __MERGE_URL

        b64img = base64.b64encode(temp_file.read()).rstrip().decode('utf-8')
        data = {'image': b64img, 'model': model}

        headers = {'content-type': "application/json"}

        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                res = r.text
                if res:
                    new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_ronghe' + '.png'
                    with open(new_file, 'wb') as f:
                        f.write(requests.get(res).content)
                    temp_file.close()
                    return _resize_img(new_file)
                else:
                    temp_file.close()
                    raise ReturnValueError("图片中找不到人哦~")
        temp_file.close()
        raise ConnectionError("获取融合图片失败", r.content)

    except (ParameterValueError, ParameterTypeError, ReturnValueError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face')


def _compose_message(data):
    _gender = '男' if data['gender'] > 50 else '女'
    _glass = '' if data['glass'] else '不'
    return '{}，{}岁左右，{}戴眼镜，颜值打分：{}分'.format(_gender, data['age'], _glass, data['beauty'])


def _get_image_b64(file):
    buf = BytesIO()
    im = Image.open(file)

    _resize_if_too_large(im)

    im.save(buf, 'PNG')
    image_bytes = buf.getvalue()
    image_str = base64.b64encode(image_bytes)

    return image_str


def _resize_if_too_large(im):
    default_max_length = 500

    original_width, original_height = im.size
    max_len = max(original_width, original_height)

    if max_len <= default_max_length:
        return

    ratio = default_max_length / max_len
    new_size = (original_width * ratio, original_height * ratio)
    im.thumbnail(new_size)


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename1', str, is_not_empty),
    ParamCheckEntry('filename2', str, is_not_empty)
])
def compare(filename1='', filename2=''):
    file1 = os.path.abspath(filename1)
    file2 = os.path.abspath(filename2)
    image1_base64 = _get_image_b64(file1)
    image2_base64 = _get_image_b64(file2)

    url = __FACE_COMPARE_URL_V2
    payload = {'imageA': image1_base64, 'imageB': image2_base64}

    r = requests.post(url, data=payload)
    if r.status_code != 200:
        raise ConnectionError("获取人脸信息失败", r.content)

    return r.json()


def main():
    # pass
    # import ybc_box as box
    # print(info('test.jpg'))
    # print(info_all('SNH48-2.jpg'))
    # print(_get_info('test.jpg'))
    # print(info('rgba.png'))
    # print(mofa(123, ''))
    # ps(decoration=22)
    # filename = camera()
    # res = age(None)
    # print(res)
    # res = gender(filename)
    # print(res)
    # res = glass(filename)
    # print(res)
    # res = beauty(filename)
    # print(res)
    # res = info('2.jpg')
    # print(res)
    # res = info_all('3.jpg')
    # print(res)
    # res = age('5.jpg')
    # print(res)
    # res = gender('5.jpg')
    # print(res)
    # res = glass('5.jpg')
    # print(res)
    # res = beauty('5.jpg')
    # print(res)
    print(mofa('test2.jpg'))


if __name__ == '__main__':
    main()
