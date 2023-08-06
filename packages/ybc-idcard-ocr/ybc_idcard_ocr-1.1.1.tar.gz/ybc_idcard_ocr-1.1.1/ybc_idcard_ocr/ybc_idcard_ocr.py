import os
import time
import cv2
import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__IDCARD_URL = __PREFIX + ybc_config.uri + '/idCardOcr'

__CARD_TYPE = 0


@exception_handler('ybc_face')
@params_check([
    ParamCheckEntry('filename', str)
])
def camera(filename=''):
    """
    功能：拍照。

    参数：无，

    返回：拍摄照片的文件名。
    """
    try:
        cap = cv2.VideoCapture(0)
        while 1:
            ret, frame = cap.read()
            cv2.imshow("capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                now = time.localtime()
                if filename == '':
                    filename = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + '.jpg'
                cv2.imwrite(filename, frame)
                break
        cap.release()
        cv2.destroyAllWindows()
        return filename
    except Exception as e:
        raise InternalError(e, 'ybc_idcard_ocr')


def idcard_info(filename=''):
    """
    功能：身份证识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：识别出的身份证信息。
    """

    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    try:
        ybc_config.resize_if_too_large(filename)
        url = __IDCARD_URL
        filepath = os.path.abspath(filename)
        fo = open(filepath, 'rb')
        files = {
            'file': fo
        }

        data = {
            'cardType': __CARD_TYPE
        }

        for i in range(3):
            r = requests.post(url, files=files, data=data)
            if r.status_code == 200:
                result = r.json()
                # 识别不到身份证不会通过该检查
                if 'result_list' in result and result['result_list'][0]['code'] == 0:
                    result = result['result_list'][0]['data']
                    # 只提取有用字段，其余字段丢弃
                    res = dict()
                    res['name'] = result['name']
                    res['sex'] = result['sex']
                    res['nation'] = result['nation']
                    res['birth'] = result['birth']
                    res['address'] = result['address']
                    res['id'] = result['id']
                    fo.close()
                    return res
                else:
                    fo.close()
                    return -1
        fo.close()
        raise ConnectionError('识别身份证图片失败', r._content)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_idcard_ocr')


def main():
    res = idcard_info('test.jpg')
    print(res)


if __name__ == '__main__':
    main()
