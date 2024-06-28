import pyautogui
from datetime import datetime
import os
import settings
from PIL import Image, ImageDraw
import threading

class EventListener:
    def __init__(self):
        # 加载数据读取对象
        self.click_listeners = [ScreenshotListener()]
    
    def on_mouse_click(self, click_num, pressed):
        for listener in self.click_listeners:
            listener.listen(click_num, pressed)

class ScreenshotListener:
    def __init__(self):
        # 加载数据读取对象
        now = datetime.now()
        self.id = now.strftime("%Y%m%d_%H%M%S")

    def listen(self, click_num, pressed):
        if not pressed:
            # 获取当前的鼠标光标位置
            mouse_x, mouse_y = pyautogui.position()
            # 文件名称
            filename = f"mouse_click_{click_num}.png"
            # 异步截图
            threading.Thread(target=lambda: self.capture_and_save_screenshot(filename, mouse_x, mouse_y), daemon=True).start()

    def capture_and_save_screenshot(self, file_name, mouse_x, mouse_y):
        # 获取当前时间
        now = datetime.now()

        # 设置保存路径并创建目录（如果不存在）
        save_path = f'{settings.SCREENSHOT_SAVE_PATH}{self.id}/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 设置文件名
        full_path = os.path.join(save_path, file_name)

        # 捕捉屏幕截图
        screenshot = pyautogui.screenshot()
        
        # 绘制光标
        self.draw_cursor(screenshot, mouse_x, mouse_y)

        # 保存截图
        screenshot.save(full_path)
        print(f"Screenshot saved to {full_path}")

    # 绘制光标
    def draw_cursor(self, screenshot, mouse_x, mouse_y):

        # 打开截图为图像对象
        # _screenshot = Image.open(screenshot.fp)

        # 创建一个用于绘制的对象
        draw = ImageDraw.Draw(screenshot)

        # 定义光标的大小和形状（例如一个小圆圈）
        cursor_size = 10
        cursor_color = (255, 0, 0)  # 红色
        draw.ellipse((mouse_x - cursor_size, mouse_y - cursor_size, 
                    mouse_x + cursor_size, mouse_y + cursor_size), 
                    fill=cursor_color)