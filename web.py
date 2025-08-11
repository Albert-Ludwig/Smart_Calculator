import tkinter as tk
import math
# 创建主窗口
root = tk.Tk()
root.title("计算器")
root.geometry("600x500")  # 设置窗口大小

# 创建显示屏 - 用于显示输入和结果
display = tk.Entry(root, font=("Arial", 20), bd=10, width=18, borderwidth=4)
display.grid(row=0, column=0, columnspan=8)  # 跨8列显示

# 按钮布局定义
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]
buttons.append('√')
buttons.append('^')

# 动态创建按钮
row_val = 1
col_val = 0
for button in buttons:
    def cmd(x=button):  # 闭包保存当前按钮值
        current = display.get()
        if x == "=":
            try:
                result = eval(current)  # 执行计算
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except:
                display.delete(0, tk.END)
                display.insert(0, "错误")
        else:
            display.insert(tk.END, x)  # 追加输入

    # 创建按钮并绑定事件
    tk.Button(
        root, text=button, 
        padx=20, pady=20, font=("Arial", 15),
        command=cmd
    ).grid(row=row_val, column=col_val)

    # 更新网格位置
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

def clear():
    display.delete(0, tk.END)

tk.Button(
    root, text="C", padx=20, pady=20, 
    font=("Arial", 15), command=clear
).grid(row=0, column=0, columnspan=1)

# 修改按钮命令函数
def cmd(x=button):
    current = display.get()
    if x in ('+', '-', '*', '/'):
        if current and current[-1] in ('+', '-', '*', '/'):  # 检查最后一个字符
            return  # 阻止连续输入运算符
    if x == '.':
        if '.' in current.split()[-1]:  # 检查当前数字是否已有小数点
            return
    try:
        result = eval(current)
    except ZeroDivisionError:
        display.delete(0, tk.END)
        display.insert(0, "除零错误")
    if x == "√":
        try:    
            num = float(display.get())
            display.delete(0, tk.END)
            display.insert(0, str(math.sqrt(num)))
        except:
            display.insert(0, "错误")
    elif x == "^":
        display.insert(tk.END, "**")  # Python幂运算符

# 设置按钮悬停效果
def on_enter(e):
    e.widget['bg'] = '#d9d9d9'  # 浅灰色

def on_leave(e):
    e.widget['bg'] = 'SystemButtonFace'  # 恢复默认

# 创建按钮时绑定事件
btn = tk.Button(root, text="测试")
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)
btn.grid(row=row_val+1, column=0)

# 最后执行主循环
root.mainloop()