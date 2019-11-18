from PIL import Image
import pytesseract


def recognize_code_image(image_file='image\\captcha_code_01.png'):
    """
    识别图片上的验证码,这个步骤真是蛋疼死人了，现在一定要折腾到底
    1. 早先不知道pytesseract这个库还需要一个pytesser，所以运行image_to_string总是出错，根本就得不到验证码，哪怕是错的验证码
    2. 后来知道了这个pytesser，但却不知道怎么用，一度忽略了它，以为是其他地方出问题了
    3. 终于，我知道了，这个pytesser就像是driver的驱动器一样，需要让pytesseract识别，只是，大家没拿到明面上说，代码里面也没有明确的体现
    4.
    """
    # 打开图片
    image = Image.open(image_file)
    # image.show()
    # 转为灰度图片
    image_grey = image.convert('L')
    # image_grey.show()
    # 二值化
    table = []
    for i in range(256):
        if i < 140:
            table.append(0)
        else:
            table.append(1)
    image_bi = image_grey.point(table, '1')
    # 识别验证码
    verify_code = pytesseract.image_to_string(image_bi)
    print(verify_code)
    return verify_code


if __name__ == '__main__':
    a = recognize_code_image('image/yzm6.jpg')
    print(a)