import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级计算器")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
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
                    bg="#ec7e7e" if text in ('C', '√', '^') else "SystemButtonFace"
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
        
        # 科学计算器按钮布局
        sci_layout = [
            ['sin', 'cos', 'tan', 'π', '(', ')'],
            ['log', 'ln', 'e', 'x²', 'x³', '10^x'],
            ['C', '√', '^', '/', '⌫', 'AC'],
            ['7', '8', '9', '*', '(', ')'],
            ['4', '5', '6', '-', '[', ']'],
            ['1', '2', '3', '+', '{', '}'],
            ['0', '.', '=', '±', '!', '←']
        ]
        
        # 创建科学计算器按钮
        for row_idx, row in enumerate(sci_layout):
            for col_idx, text in enumerate(row):
                bg_color = "SystemButtonFace"
                if text in ('C', 'AC', '⌫', '←'):
                    bg_color = "#ff9999"
                elif text in ('sin', 'cos', 'tan', 'log', 'ln'):
                    bg_color = "#99ccff"
                elif text == "=":
                    bg_color = "#4d94ff"
                
                self.create_button(
                    text, row_idx+2, col_idx, 
                    bg=bg_color,
                    fg="black" if bg_color == "SystemButtonFace" else "white"
                )
    
    def create_button(self, text, row, col, bg="SystemButtonFace", fg="black"):
        """创建带样式的按钮"""
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
    
    def button_click(self, value):
        """处理所有按钮点击事件"""
        current = self.display_var.get()
        
        # 特殊功能处理[1,4](@ref)
        if value == "C":
            self.display_var.set("")
        elif value == "AC":
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
        # 三角函数处理（添加函数名和括号）[3](@ref)
        elif value in ('sin', 'cos', 'tan', 'log', 'ln'):
            self.display_var.set(f"{value}({current})")
        elif value == "=":
            try:
                # 安全替换数学函数
                safe_expr = current.replace("^", "**")
                safe_expr = safe_expr.replace("π", "3.1415926535")
                safe_expr = safe_expr.replace("e", "2.7182818284")
                
                # 使用eval计算表达式
                result = eval(safe_expr, {"__builtins__": None}, {
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "log": math.log10, "ln": math.log
                })
                self.display_var.set(str(result))
            except Exception as e:
                self.display_var.set("错误")
        else:
            # 防止连续运算符
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