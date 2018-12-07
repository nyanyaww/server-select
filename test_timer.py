import threading
# 定义函数


def fun_timer():
    print('hello timer')  # 打印输出
    global timer  # 定义变量
    timer = threading.Timer(5, fun_timer)  # 60秒调用一次函数
    timer.start()  #(1, ) 启用定时器


timer = threading.Timer(1, fun_timer)  # 首次启动
timer.start()
