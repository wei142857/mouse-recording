# 鼠标录制功能

### 功能：
可录制鼠标动作，用于测试或解决重复性的操作。解放双手，提升效率。同时支持每个鼠标点击时的定制逻辑，比如点击后，读取某个文件的内容将某个内容复制到鼠标点击的位置的输入框中。录制完毕后使用 `ctrl + r` 即可循环完成动作。注意：具体循环播放的次数需要查看`settings.py`相关的配置

### Function:
Can record mouse actions for testing or solving repetitive operations. Free your hands and improve efficiency. It also supports custom logic for each mouse click, such as reading the content of a file and copying the content to the input box at the location where the mouse is clicked. After recording, use `ctrl + r` to loop the action. Note: The specific number of loop playbacks needs to be checked in the configuration of `settings.py`

### 按键说明
- `ctrl + i`: 开始录制
- `ctrl + s`: 保存录制
- `ctrl + r`: 开始播放
- `ctrl + q`: 退出播放
- `ctrl + c`: 强制终止

### Keyboard Instructions
- `ctrl + i`: Start recording
- `ctrl + s`: Save recording
- `ctrl + r`: Start playback
- `ctrl + q`: Exit playback
- `ctrl + c`: Force termination

### 定制钩子
* `beforeCycle`: 每个周期执行前的钩子
* `afterCycle`: 每个周期执行后的钩子
* `beforeReplay`: 每次录制执行前钩子
* `afterReplay`: 每次录制执行后钩子
* `beforeInteration`: 每次循环执行前的钩子
* `afterInteration`: 每次循环执行后的钩子
* `beforeMouseDown`: 鼠标按下前的钩子
* `afterMouseDown`: 鼠标按下后的钩子
* `beforeMouseUp`: 鼠标抬起前的钩子
* `afterMouseUp`: 鼠标抬起后的钩子

以上这下钩子都需要在`controller.py`文件中实现

### Custom hooks
* `beforeCycle`: Hook before each cycle is executed
* `afterCycle`: Hook after each cycle is executed
* `beforeReplay`: Hook before each recording is executed
* `afterReplay`: Hook after each recording is executed
* `beforeInteration`: Hook before each cycle is executed
* `afterInteration`: Hook after each cycle is executed
* `beforeMouseDown`: Hook before mouse is pressed
* `afterMouseDown`: Hook after mouse is pressed
* `beforeMouseUp`: Hook before mouse is lifted
* `afterMouseUp`: Hook after mouse is lifted

All of the above hooks need to be implemented in the `controller.py` file

### 文件说明
- `main.py`: 调度类，用于控制录制。通常不需要修改
- `controller.py`: 生命周期的钩子，用于定制逻辑。
- `handler.py`: 处理鼠标动作的逻辑
- `reader.py`: 读取数据的定制逻辑
- `event_listener.py`: 监听器，监听事件并处理
- `recorded_events.pkl`: 鼠标录制的结果文件
- `settings.py`: 全局配置
- `secreenshot/{日期_时间}/mouse_click_{click_num}.png`: 每次点击位置的截图，截图中包含一个红色的点，用于辨识点击了哪里。当地定制点击动作的后续逻辑时，需要找到具体点击的位置的`截图名称中的click_num`来定制点击逻辑。

### File Description
- `main.py`: Scheduling class, used to control recording. Usually no modification is required
- `controller.py`: Lifecycle hook, used to customize logic.
- `handler.py`: Logic for handling mouse actions
- `reader.py`: Custom logic for reading data
- `event_listener.py`: Listener, listen to events and handle them
- `recorded_events.pkl`: Mouse recording result file
- `settings.py`: Global configuration
- `secreenshot/{date_time}/mouse_click_{click_num}.png`: Screenshot of each click position, with a red dot in the screenshot to identify where the click was made. When customizing the subsequent logic of the click action, you need to find the `click_num` in the screenshot name of the specific click position to customize the click logic.

### 使用
- 修改 `controller.py` 定制鼠标相关事件后的逻辑。
- 修改 `handler.py` 中的 `handle` 方法处理每个鼠标动作之后的逻辑，如：读取某个文件的内容并复制到鼠标点击的位置。
- 鼠标的每次点击会截图并保存到本地，保存位置在 `settings.py` 中通过 `SCREENSHOT_SAVE_PATH` 属性配置，注意这个配置必须以 `/`
 结尾。
- 修改 `reader.py` 中的 `read` 方法内容，定制读取的数据方式。
- 查看截图，方便识别鼠标点击的位置及其`click_num`, 截图位置在 `settings.py` 中通过 `SCREENSHOT_SAVE_PATH` 属性配置。录制过程中如有鼠标点击动作，会在 `secreenshot/{date_time}/mouse_click_{click_num}.png` 中保存

### Usage
- Modify `controller.py` to customize the logic after mouse-related events.
- Modify the `handle` method in `handler.py` to handle the logic after each mouse action, such as: reading the contents of a file and copying it to the location where the mouse is clicked.
- Each mouse click will take a screenshot and save it locally. The save location is configured in `settings.py` through the `SCREENSHOT_SAVE_PATH` property. Note that this configuration must end with `/`

.
- Modify the `read` method content in `reader.py` to customize the data reading method.
- View the screenshot to easily identify the location of the mouse click and its `click_num`. The screenshot location is configured in `settings.py` through the `SCREENSHOT_SAVE_PATH` property. If there is a mouse click during recording, it will be saved in `secreenshot/{date_time}/mouse_click_{click_num}.png`



# 欢迎一起维护这个项目
# Welcome to maintain this project together