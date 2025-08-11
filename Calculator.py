import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级科学计算器")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
        # 角度模式设置（默认为角度模式）
        self.degree_mode = True  # True: 角度模式, False: 弧度模式
        
        # 主界面显示屏（两个界面共享）
        self.display_var = tk.StringVar()
        
        # 创建主计算器界面
        self.create_basic_calculator()

    def create_basic_calculator(self):
        """创建基础计算器界面"""
        # 清除当前所有控件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 配置网格
        for i in range(7):
            self.root.rowconfigure(i, weight=1)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        
        # 显示屏
        display = tk.Entry(
            self.root, textvariable=self.display_var, 
            font=("Arial", 24), bd=10, relief=tk.SUNKEN,
            justify=tk.RIGHT, bg="#e6f2ff"
        )
        display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # 添加科学计算按钮
        sci_button = tk.Button(
            self.root, text="科学计算", font=("Arial", 12),
            command=self.show_scientific_calculator,
            bg="#ff9900", fg="white", relief=tk.RAISED
        )
        sci_button.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        sci_button.bind("<Enter>", lambda e: e.widget.config(bg="#ffaa33"))
        sci_button.bind("<Leave>", lambda e: e.widget.config(bg="#ff9900"))
        
        # 基础计算器按钮布局
        button_layout = [
            ['C', '√', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        # 创建基础计算器按钮
        for row_idx, row in enumerate(button_layout):
            for col_idx, text in enumerate(row):
                btn = self.create_button(
                    text, row_idx+2, col_idx, 
                    bg="#ff9999" if text in ('C', '√', '^') else "SystemButtonFace",
                    fg="black"
                )
                
                # 特殊按钮处理
                if text == "0":
                    btn.grid(columnspan=2, sticky="nsew")
                elif text == "=":
                    btn.config(bg="#4d94ff", fg="white")
    
    def show_scientific_calculator(self):
        """显示科学计算器界面"""
        # 清除当前所有控件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 配置科学计算器网格
        for i in range(8):
            self.root.rowconfigure(i, weight=1)
        for i in range(6):  # 增加列数容纳更多按钮
            self.root.columnconfigure(i, weight=1)
        
        # 显示屏（保持与基础计算器相同）
        display = tk.Entry(
            self.root, textvariable=self.display_var, 
            font=("Arial", 24), bd=10, relief=tk.SUNKEN,
            justify=tk.RIGHT, bg="#e6f2ff"
        )
        display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
        
        # 返回基础计算器按钮
        back_button = tk.Button(
            self.root, text="返回", font=("Arial", 12),
            command=self.create_basic_calculator,
            bg="#ff4444", fg="white", relief=tk.RAISED
        )
        back_button.grid(row=1, column=0, columnspan=6, padx=10, pady=5, sticky="nsew")
        back_button.bind("<Enter>", lambda e: e.widget.config(bg="#ff6666"))
        back_button.bind("<Leave>", lambda e: e.widget.config(bg="#ff4444"))
        
        # 角度/弧度模式标签
        self.mode_label = tk.Label(
            self.root, text="当前模式: DEG" if self.degree_mode else "当前模式: RAD",
            font=("Arial", 10), bg="#f0f0f0"
        )
        self.mode_label.grid(row=2, column=4, columnspan=2, sticky="e")
        
        # 科学计算器按钮布局
        sci_layout = [
            ['sin', 'cos', 'tan', 'π', '(', ')'],
            ['log', 'ln', 'e', 'x²', 'x³', '10^x'],
            ['C', '√', '^', '/', '⌫', 'rad/deg'],  # 将AC改为角度/弧度切换按钮
            ['7', '8', '9', '*', '(', ')'],
            ['4', '5', '6', '-', '[', ']'],
            ['1', '2', '3', '+', '{', '}'],
            ['0', '.', '=', '±', '!', '←']
        ]
        
        # 创建科学计算器按钮
        for row_idx, row in enumerate(sci_layout):
            for col_idx, text in enumerate(row):
                bg_color = "SystemButtonFace"
                if text in ('C', '⌫', '←'):
                    bg_color = "#ff9999"
                elif text in ('sin', 'cos', 'tan', 'log', 'ln'):
                    bg_color = "#99ccff"
                elif text == "=":
                    bg_color = "#4d94ff"
                elif text == "rad/deg":  # 角度/弧度切换按钮特殊颜色
                    bg_color = "#99cc99"
                
                self.create_button(
                    text, row_idx+3, col_idx,  # 注意：行索引+3（因为新增了标签行）
                    bg=bg_color,
                    fg="black" if bg_color == "SystemButtonFace" else "white"
                )
    
    def create_button(self, text, row, col, bg="SystemButtonFace", fg="black"):
        """创建带样式的按钮"""
        # 特殊处理角度/弧度切换按钮
        if text == "rad/deg":
            btn = tk.Button(
                self.root, text="RAD" if self.degree_mode else "DEG", 
                font=("Arial", 14),
                command=self.toggle_angle_mode,  # 绑定角度切换函数
                padx=5, pady=5, bd=2, relief=tk.RAISED,
                bg=bg, fg=fg
            )
        else:
            btn = tk.Button(
                self.root, text=text, font=("Arial", 14),
                command=lambda t=text: self.button_click(t),
                padx=5, pady=5, bd=2, relief=tk.RAISED,
                bg=bg, fg=fg
            )
        
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # 悬停效果
        btn.bind("<Enter>", lambda e: e.widget.config(bg="#e0e0e0"))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=bg))
        
        return btn
    
    def toggle_angle_mode(self):
        """切换角度/弧度模式[2,3](@ref)"""
        self.degree_mode = not self.degree_mode
        # 更新模式标签
        self.mode_label.config(text="当前模式: DEG" if self.degree_mode else "当前模式: RAD")
        # 更新按钮文本
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") in ("DEG", "RAD"):
                widget.config(text="RAD" if self.degree_mode else "DEG")
    
    def button_click(self, value):
        """处理所有按钮点击事件"""
        current = self.display_var.get()
        
        # 特殊功能处理[1,2](@ref)
        if value == "C":
            self.display_var.set("")
        elif value == "⌫":  # 删除最后一个字符
            self.display_var.set(current[:-1])
        elif value == "←":  # 返回基础计算器
            self.create_basic_calculator()
            return
        elif value == "±":  # 正负号切换
            if current.startswith('-'):
                self.display_var.set(current[1:])
            else:
                self.display_var.set('-' + current)
        elif value == "π":
            self.display_var.set(current + "3.1415926535")
        elif value == "e":
            self.display_var.set(current + "2.7182818284")
        elif value == "x²":
            self.display_var.set(f"({current})**2")
        elif value == "x³":
            self.display_var.set(f"({current})**3")
        elif value == "10^x":
            self.display_var.set(f"10**({current})")
        elif value == "!":
            try:
                num = int(float(current))
                self.display_var.set(str(math.factorial(num)))
            except:
                self.display_var.set("错误")
        # 三角函数处理（添加函数名和括号）[1,5](@ref)
        elif value in ('sin', 'cos', 'tan', 'log', 'ln'):
            self.display_var.set(f"{value}({current})")
        elif value == "=":
            try:
                # 安全替换数学函数
                safe_expr = current.replace("^", "**")
                safe_expr = safe_expr.replace("π", "3.1415926535")
                safe_expr = safe_expr.replace("e", "2.7182818284")
                
                # 创建安全的计算环境[1](@ref)
                namespace = {
                    "__builtins__": None,
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "log": math.log10,
                    "ln": math.log,
                    "sqrt": math.sqrt,
                    "exp": math.exp
                }
                
                # 根据角度模式调整三角函数[2,3,5](@ref)
                if self.degree_mode:
                    # 角度模式下，将三角函数参数转换为弧度
                    def deg_to_rad_wrapper(func):
                        def wrapper(x):
                            # 先将输入值转换为弧度（角度转弧度公式：rad = deg * π / 180）
                            radians = math.radians(x)
                            return func(radians)
                        return wrapper
                    
                    # 应用包装器
                    namespace["sin"] = deg_to_rad_wrapper(math.sin)
                    namespace["cos"] = deg_to_rad_wrapper(math.cos)
                    namespace["tan"] = deg_to_rad_wrapper(math.tan)
                
                # 使用eval计算表达式
                result = eval(safe_expr, {}, namespace)
                
                # 格式化结果（保留最多8位小数，移除不必要的零）
                formatted_result = f"{result:.8f}".rstrip('0').rstrip('.')
                if '.' in formatted_result:
                    self.display_var.set(formatted_result)
                else:
                    self.display_var.set(str(int(result)))
            except Exception as e:
                self.display_var.set("错误")
        else:
            # 防止连续运算符[1](@ref)
            if value in ('+', '-', '*', '/') and current and current[-1] in ('+', '-', '*', '/'):
                return
            # 防止多个小数点
            if value == '.' and '.' in current.split()[-1] if current else False:
                return
            self.display_var.set(current + value)

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()