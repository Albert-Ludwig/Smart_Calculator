import tkinter as tk
import math

# 创建主窗口
root = tk.Tk()
root.title("高级计算器")
root.geometry("400x500")  # 设置窗口大小
root.configure(bg="#f0f0f0")  # 设置背景色

# 配置网格行和列的权重，使按钮随窗口缩放[6,7](@ref)
for i in range(7):
    root.rowconfigure(i, weight=1)
for i in range(4):
    root.columnconfigure(i, weight=1)

# 创建显示屏 - 使用StringVar实现动态更新[2,3](@ref)
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Arial", 24), 
                   bd=10, relief=tk.SUNKEN, justify=tk.RIGHT, bg="#e6f2ff")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# 按钮命令处理函数
def button_click(value):
    current = display_var.get()
    
    # 处理特殊功能按钮[1,4](@ref)
    if value == "C":
        display_var.set("")
    elif value == "=":
        try:
            # 使用eval计算表达式[1](@ref)
            result = eval(current)
            display_var.set(str(result))
        except Exception as e:
            display_var.set("错误")
    elif value == "√":
        try:
            num = float(current)
            display_var.set(str(math.sqrt(num)))
        except:
            display_var.set("错误")
    elif value == "^":
        display_var.set(current + "**")
    else:
        # 防止连续运算符[1,3](@ref)
        if value in ('+', '-', '*', '/') and current and current[-1] in ('+', '-', '*', '/'):
            return
        # 防止多个小数点[1](@ref)
        if value == '.' and '.' in current.split()[-1] if current else False:
            return
        display_var.set(current + value)

# 按钮悬停效果[3](@ref)
def on_enter(e):
    e.widget.config(bg="#d9d9d9")

def on_leave(e):
    e.widget.config(bg="SystemButtonFace")

# 定义按钮布局 - 使用二维列表清晰组织[2,4](@ref)
button_layout = [
    ['C', '√', '^', '/'],
    ['7', '8', '9', '*'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', '=', '']
]

# 创建按钮并布局
for row_idx, row in enumerate(button_layout):
    for col_idx, text in enumerate(row):
        if text:  # 跳过空按钮位置
            btn = tk.Button(root, text=text, font=("Arial", 18), 
                            command=lambda t=text: button_click(t),
                            padx=10, pady=10, bd=2, relief=tk.RAISED)
            
            # 特殊按钮样式[5](@ref)
            if text == "=":
                btn.config(bg="#4d94ff", fg="white")
            elif text in ('C', '√', '^'):
                btn.config(bg="#f2f2f2")
            
            # 按钮布局 - 使用sticky="nsew"填满单元格[6,7](@ref)
            if text == "0":  # 0按钮跨两列
                btn.grid(row=row_idx+1, column=col_idx, columnspan=2, 
                         padx=5, pady=5, sticky="nsew")
            elif text == "=":  # =按钮跨两行
                btn.grid(row=row_idx+1, column=col_idx, rowspan=2, 
                         padx=5, pady=5, sticky="nsew")
            else:
                btn.grid(row=row_idx+1, column=col_idx, 
                         padx=5, pady=5, sticky="nsew")
            
            # 绑定悬停效果
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

# 最后执行主循环
root.mainloop()