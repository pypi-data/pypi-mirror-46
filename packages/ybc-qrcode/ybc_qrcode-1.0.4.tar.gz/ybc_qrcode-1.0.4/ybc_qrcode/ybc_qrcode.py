from ybc_exception import *
import qrcode
import time


@exception_handler('ybc_qrcode')
@params_check([
    ParamCheckEntry('data', str, is_length_in_range, Range(1, 2000)),
    ParamCheckEntry('filename', str, is_correct_file_format, {'jpg', 'png'})
])
def make(data='', filename=''):
    """
    功能：根据data生成一张二维码图片。

    参数：data：二维码的内容，必填，长度小于等于 600
         filename：生成的图片名称，选填，默认为"当前时间戳_qrcode.jpg"

    返回：图片名称
    """
    if not filename:
        filename = str(int(time.time())) + '_qrcode.jpg'
    file = qrcode.make(data)
    file.save(filename)
    return filename


if __name__ == '__main__':
    file = make('结果')
