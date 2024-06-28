import threading
import pickle
import time
from pynput import mouse, keyboard
from controller import LifeCycleController
from event_listener import EventListener
from datetime import datetime
import settings

mouse_listener = None
keyboard_listener = None
events = []
is_recording = False
ctrl_pressed = False
is_playing = False
lifecycle_controller = LifeCycleController()
event_listener = EventListener()
click_num = 0
replay_count = settings.REPLAY_COUNT
debug_mode =  False

# 共享变量的锁
lock = threading.Lock()

# 中断播放
interrupt_replay = True

# 记录上一次点击时间和位置
last_click_time = None
last_click_position = None

def on_click(x, y, button, pressed):
    global last_click_time, last_click_position, click_num

    if is_recording:
        current_time = datetime.now()
        event_type = 'click'
        click_num += 1
        # print(click_num)
        
        if last_click_time is not None and pressed:
            time_diff = (current_time - last_click_time).total_seconds()
            position_diff = ((x - last_click_position[0]) ** 2 + (y - last_click_position[1]) ** 2) ** 0.5

            # 判断两次点击事件在200毫秒（0.2秒）内且位置差异在一定范围内为双击
            if time_diff < 0.2 and position_diff < 5:
                event_type = 'double_click'
        
        event = (event_type, x, y, button, pressed, click_num, current_time)
        with lock:
            events.append(event)
        # print(f"Recorded {event_type} at {(x, y)} - {button} {'pressed' if pressed else 'released'} - click num: {click_num}")
        
        # 点击事件发布
        event_listener.on_mouse_click(click_num, pressed)

        if pressed:
            last_click_time = current_time
            last_click_position = (x, y)

def on_move(x, y):
    if is_recording and settings.ENABLE_MOUSE_TRACK:
        event = ('move', x, y, datetime.now())
        with lock:
            events.append(event)
        # print(f"Recorded move to {(x, y)}")

def start_recording():
    global is_recording, events

    if is_recording:
        return
    
    with lock:
        is_recording = True
        events = []
    print("录制中...")

def stop_recording():
    global is_recording
    with lock:
        is_recording = False
        with open('recorded_events.pkl', 'wb') as f:
            pickle.dump(events, f)
    print("录制已保存")

def replay_events():
    print("录制播放中...")
    global is_playing
    if is_playing:
        return
    
    is_playing = True
    # TODO: 按多次ctrl+r时，如果有一个线程已经运行了，那么就不再运行

    with open('recorded_events.pkl', 'rb') as f:
        loaded_events = pickle.load(f)
    
    # 鼠标控制器
    mouse_controller = mouse.Controller()
    # 键盘控制器
    keyboard_controller = keyboard.Controller()

    global interrupt_replay
    with lock:
        interrupt_replay = False

    lifecycle_controller.beforeCycle(mouse_controller, keyboard_controller)

    for cycle in range(replay_count):
        with lock:
            if interrupt_replay:
                break
        
        lifecycle_controller.beforeReplay(mouse_controller, keyboard_controller)
        
        for i in range(len(loaded_events)):
            event = loaded_events[i]
            if i > 0:
                # 计算与前一个事件的时间差
                time_diff = (event[-1] - loaded_events[i-1][-1]).total_seconds()
                time.sleep(time_diff)

            lifecycle_controller.beforeInteration(mouse_controller, keyboard_controller)
            with lock:
                if interrupt_replay:
                    break
            if event[0] == 'move':
                x, y = event[1], event[2]
                mouse_controller.position = (x, y)
                # print(f"Replayed move to {(x, y)}")
            elif event[0] == 'click':
                x, y, button, pressed, click_num = event[1], event[2], event[3], event[4], event[5]
                mouse_controller.position = (x, y)
                if pressed:
                    lifecycle_controller.beforeMouseDown(cycle, click_num, mouse_controller, keyboard_controller)
                    mouse_controller.press(button)
                    lifecycle_controller.afterMouseDown(cycle, click_num, mouse_controller, keyboard_controller)
                    # print(f"Replayed press at {(x, y)} - {button}")
                else:
                    lifecycle_controller.beforeMouseUp(cycle, click_num, mouse_controller, keyboard_controller)
                    mouse_controller.release(button)
                    lifecycle_controller.afterMouseUp(cycle, click_num, mouse_controller, keyboard_controller)
                    # print(f"Replayed release at {(x, y)} - {button}")
            elif event[0] == 'double_click':
                x, y, button, pressed, click_num = event[1], event[2], event[3], event[4], event[5]
                mouse_controller.position = (x, y)
                if pressed:
                    lifecycle_controller.beforeMouseDown(cycle, click_num, mouse_controller, keyboard_controller)
                    mouse_controller.click(button, 2)  # 这里用click方法的count参数模拟双击
                    lifecycle_controller.afterMouseDown(cycle, click_num, mouse_controller, keyboard_controller)
                    # print(f"Replayed double click at {(x, y)} - {button}")
            lifecycle_controller.afterInteration(mouse_controller, keyboard_controller)
        
        lifecycle_controller.afterReplay(mouse_controller, keyboard_controller)
        # 每个循环间隔一段时间
        if cycle < replay_count - 1:
            time.sleep(settings.REPLAY_INTERVAL_TIME)
            
        if interrupt_replay:
            break
    lifecycle_controller.afterCycle(mouse_controller, keyboard_controller)
    is_playing = False
    print("录制播放已完成")

def on_press(key):
    global ctrl_pressed, interrupt_replay, debug_mode
    try:
        if key == keyboard.Key.ctrl_l:
            ctrl_pressed = True
        elif ctrl_pressed and key == keyboard.KeyCode.from_char('i') or key == keyboard.KeyCode.from_char('\t'):
            threading.Thread(target=start_recording, daemon=True).start()
        elif ctrl_pressed and key == keyboard.KeyCode.from_char('s') or key == keyboard.KeyCode.from_char('\x13'):
            threading.Thread(target=stop_recording, daemon=True).start()
        elif ctrl_pressed and key == keyboard.KeyCode.from_char('r') or key == keyboard.KeyCode.from_char('\x12'):
            threading.Thread(target=replay_events, daemon=True).start()
        elif ctrl_pressed and key == keyboard.KeyCode.from_char('q') or key == keyboard.KeyCode.from_char('\x11'):
            with lock:
                interrupt_replay = True
                print("已关闭播放")
    except AttributeError:
        pass

def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False

if __name__ == "__main__":
    with mouse.Listener(on_click=on_click, on_move=on_move) as mouse_listener, \
         keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
        try:
            mouse_listener.join()
            keyboard_listener.join()
        except KeyboardInterrupt:
            pass
