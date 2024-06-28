
from handler import MouseHandler, MouseOpportunityKey

class LifeCycleController:
    def __init__(self):
        print('''按键提示：
ctrl + i 开始录制
ctrl + s 保存录制
ctrl + r 开始播放
ctrl + q 退出播放
ctrl + c 强制终止
              
按 ctrl + i 开始录制...

        ''')
        # 数据处理
        self.mouse_handler = MouseHandler()

    # 每个周期执行前的钩子
    def beforeCycle(self, mouse_controller, keyboard_controller):
        # print("beforeCycle")
        pass
    
    # 每个周期执行后的钩子
    def afterCycle(self, mouse_controller, keyboard_controller):
        # print("afterCycle")
        pass

    # 每次录制执行前钩子
    def beforeReplay(self, mouse_controller, keyboard_controller):
        # print("beforeReplay")
        pass
    
    # 每次录制执行后钩子
    def afterReplay(self, mouse_controller, keyboard_controller):
        # print("afterReplay")
        pass

    # 每次循环执行前的钩子
    def beforeInteration(self, mouse_controller, keyboard_controller):
        # print("beforeInteration")
        pass

    # 每次循环执行后的钩子
    def afterInteration(self, mouse_controller, keyboard_controller):
        # print("afterInteration")
        pass

    # 鼠标抬起前的钩子
    def beforeMouseUp(self, index, click_num, mouse_controller, keyboard_controller):
        self.do_mouse_click_handle(MouseOpportunityKey.BEFORE, index, click_num, keyboard_controller)
    
    # 鼠标抬起后的钩子
    def afterMouseUp(self, index, click_num, mouse_controller, keyboard_controller):
        self.do_mouse_click_handle(MouseOpportunityKey.OFTER, index, click_num, keyboard_controller)

    # 鼠标按下前的钩子
    def beforeMouseDown(self, index, click_num, mouse_controller, keyboard_controller):
        self.do_mouse_click_handle(MouseOpportunityKey.BEFORE, index, click_num, keyboard_controller)

    # 鼠标按下后的钩子
    def afterMouseDown(self, index, click_num, mouse_controller, keyboard_controller):
        self.do_mouse_click_handle(MouseOpportunityKey.OFTER, index, click_num, keyboard_controller)

    # 处理动作
    def do_mouse_click_handle(self, mouse_opportunity, index, click_num, keyboard_controller):
        self.mouse_handler.handle(mouse_opportunity, index, click_num, keyboard_controller)