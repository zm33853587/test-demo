import math
import sys
import time
import keyboard
from PIL import ImageGrab
from PIL import Image
import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import pytesseract




pytesseract.pytesseract.tesseract_cmd = r'c:\leo\Tesseract-OCR\tesseract.exe'

# 获取当前鼠标位置
print(pyautogui.position())
# 获取当前屏幕的分辨率
print(pyautogui.size())

def getWindowPos(title):
    # 获取所有打开的窗口
    windows = gw.getAllTitles()
    # 遍历窗口，查找特定标题的窗口
    for winTitle in windows:
        if winTitle == title:
            # 找到窗口后，获取窗口对象
            win = gw.getWindowsWithTitle(title)[0]
            return (win.left, win.top, win.width, win.height)
    else:
        return None  # 如果没有找到窗口，返回 None

def saveBak(path, img):
    cv2.imwrite(path, img)

while True:
    filename = 'num'
    fileext = '.png'
    if keyboard.is_pressed('space'):
        print('start !')
        sys.exit()
    pos = getWindowPos("逍遥模拟器")
    # region = (84, 336, 411, 55)
    # pyautogui.screenshot(region=region)
    ImageGrab.grab(bbox=(pos[0] + 150, pos[1] + 200, pos[0] + 400, pos[1] + 280)).save(filename + fileext)
    time.sleep(2)

    # 打开图像
    tmpImage = Image.open(filename + fileext)

    # 获取图像尺寸
    imgWidth, imgHeight = tmpImage.size
    print(f"Image size: {imgWidth}x{imgHeight}")

    # 指定要获取颜色的像素坐标
    x, y = 50, 150  # 这是你要查询的图像坐标点
    # 获取指定位置的像素值
    bgColor = tmpImage.getpixel((x, y))
    print(bgColor)

    # 关闭图像文件
    tmpImage.close()

    # opencv 加载图像
    image = cv2.imread(filename + fileext)

    # TODO 去除特定背景色
    # 将图像转换为HSV颜色空间（便于颜色过滤）
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义要去除的背景颜色范围（例如，蓝色背景）
    lower_color = np.array([bgColor[0] - 10, bgColor[1] - 10, bgColor[2] - 10])
    upper_color = np.array([bgColor[0] + 10, bgColor[1] + 10, bgColor[2] + 10])

    # 创建掩码，去除指定颜色范围内的背景
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # 反转掩码，保留前景
    mask_inv = cv2.bitwise_not(mask)

    # 保留图像中的前景
    foreground = cv2.bitwise_and(image, image, mask=mask_inv)
    saveBak(filename + '-clear' + fileext, img)

    # 将图像转换为灰度图
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    saveBak(filename + '-gray' + fileext, img)

    # 使用高斯滤波去除噪声
    img = cv2.GaussianBlur(img, (5, 5), 0)
    saveBak(filename + '-gb' + fileext, img)

    # 应用自适应直方图均衡化 (CLAHE) 提高对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    saveBak(filename + '-clahe' + fileext, img)

    # 应用Otsu二值化，将图像转换为黑白图
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    saveBak(filename + '-thresh' + fileext, img)

    # 将图像转换为HSV颜色空间（便于颜色过滤）
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 转换为灰度图像
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用二值化处理（可选，用于进一步清晰化前景）
    #_, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    # 使用 Tesseract 进行 OCR 识别
    result = pytesseract.image_to_string(thresh, config='--psm 6').split('?')
    print(result)

    try:
        result[0] = result[0].strip()
        result[1] = result[1].strip()
        if result[0] == '0':
            result[0] = 0
        if result[1] == '0':
            result[1]=0
        num1 = math.floor(float(result[0]))
        num2 = math.floor(float(result[1]))
        # pyautogui.moveTo(277, 700, duration=0.1)
        pyautogui.moveTo(pos[0] + pos[2]/2, pos[1] + 500, duration=0.1)
        if num1 > num2:
            pyautogui.mouseDown()
            pyautogui.move(100,100, duration=0.1)
            pyautogui.move(-100, 100, duration=0.1)
            pyautogui.mouseUp()
            print(f'{num1} >{num2}')
        else:
            pyautogui.mouseDown()
            pyautogui.move(-100, 100, duration=0.1)
            pyautogui.move(100, 100, duration=0.1)
            pyautogui.mouseUp()
            print(f'{num1} < {num2}')
    except IndexError as e:
        print('未捕获到内容!')
        print(e)
    except ValueError as e:
        print('未捕获到内容!')
        print(e)
