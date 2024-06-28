import enum
from reader import DataReader
import settings

class MouseOpportunityKey(enum.Enum):
    BEFORE = 1
    OFTER = 2

class MouseHandler:
    def __init__(self):
        # 加载数据读取对象
        self.data_reader = DataReader(data_file=settings.DATA_FILE)

    # 当前鼠标单击的位置的处理函数
    def handle(self, mouse_opportunity, row_offset, click_num, keyboard_controller):
        # 鼠标事件之前的动作不处理
        if mouse_opportunity == MouseOpportunityKey.BEFORE:
            return
        
        # 判断是否执行复制
        # 点击编号为n的时候，执行复制
        if click_num == 6:
            # 复制文件第11列
            self.do_paste(row_offset, 4, keyboard_controller)
        elif click_num == 8:
            # 复制文件第11列
            self.do_paste(row_offset, 11, keyboard_controller)

    # 指定复制动作
    def do_paste(self, data_row, data_col, keyboard_controller):
        # 读取文件数据
        data = self.read_data(data_row, data_col)

        if data is not None:
            # 粘贴到鼠标点击的位置
            self.paste(data, keyboard_controller)

    # 读取数据
    def read_data(self, row, col):
        return self.data_reader.read(row, col)
    
    # 电脑执行粘贴动作
    def paste(self, data, keyboard_controller):
        if data is not None:
            keyboard_controller.type(str(data))