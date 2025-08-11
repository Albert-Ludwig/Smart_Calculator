import tkinter as tk
import math
from tkinter import messagebox, scrolledtext

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级科学计算器")
        self.root.geometry("400x550")  # 增加高度以容纳历史记录
        self.root.configure(bg="#f0f0f0")
        
        # 角度模式设置（默认为角度模式）
        self.degree_mode = True
        
        # 主界面显示屏
        self.display_var = tk.StringVar()
        
        # 历史记录系统
        self.history = []  # 存储历史记录
        self.max_history = 20  # 最大历史记录数
        
        # 创建主计算器界面
        self.create_basic_calculator()

    def create_basic_calculator(self):
        """创建基础计算器界面"""
        # 清除当前所有控件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 配置网格
        for i in range(10):  # 增加行数
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
        
        # 功能按钮行
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        
        # 科学计算切换按钮
        sci_button = tk.Button(
            button_frame, text="科学计算", font=("Arial", 12),
            command=self.show_scientific_calculator,
            bg="#ff9900", fg="white", relief=tk.RAISED
        )
        sci_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        sci_button.bind("<Enter>", lambda e: e.widget.config(bg="#ffaa33"))
        sci_button.bind("<Leave>", lambda e: e.widget.config(bg="#ff9900"))
        
        # 历史记录按钮
        history_button = tk.Button(
            button_frame, text="历史记录", font=("Arial", 12),
            command=self.show_history,
            bg="#9c27b0", fg="white", relief=tk.RAISED
        )
        history_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        history_button.bind("<Enter>", lambda e: e.widget.config(bg="#b350c5"))
        history_button.bind("<Leave>", lambda e: e.widget.config(bg="#9c27b0"))
        
        # 基础计算器按钮布局
        button_layout = [
            ['C', '√', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['(', '0', ')', '.'],
            ['=']  # 单独一行
        ]
        
        # 起始行从第2行开始（0:显示屏，1:功能按钮）
        start_row = 2
        for row_idx, row in enumerate(button_layout):
            for col_idx, text in enumerate(row):
                btn = self.create_button(
                    text, row_idx + start_row, col_idx,
                    bg="#ff9999" if text in ('C', '√', '^') else ("#4d94ff" if text == "=" else "SystemButtonFace"),
                    fg="white" if text in ('C', '√', '^', '=') else "black"
                )
                # "=" 按钮单独一行跨4列
                if text == "=":
                    btn.grid(row=row_idx + start_row, column=0, columnspan=4, 
                             sticky="nsew", padx=2, pady=2)
    
    def show_scientific_calculator(self):
        """显示科学计算器界面"""
        # 清除当前所有控件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 配置科学计算器网格
        for i in range(10):  # 增加行数
            self.root.rowconfigure(i, weight=1)
        for i in range(6):  # 增加列数容纳更多按钮
            self.root.columnconfigure(i, weight=1)
        
        # 显示屏
        display = tk.Entry(
            self.root, textvariable=self.display_var, 
            font=("Arial", 24), bd=10, relief=tk.SUNKEN,
            justify=tk.RIGHT, bg="#e6f2ff"
        )
        display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
        
        # 功能按钮行
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=5, sticky="nsew")
        
        # 返回基础计算器按钮
        back_button = tk.Button(
            button_frame, text="返回", font=("Arial", 12),
            command=self.create_basic_calculator,
            bg="#ff4444", fg="white", relief=tk.RAISED
        )
        back_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        back_button.bind("<Enter>", lambda e: e.widget.config(bg="#ff6666"))
        back_button.bind("<Leave>", lambda e: e.widget.config(bg="#ff4444"))
        
        # 历史记录按钮
        history_button = tk.Button(
            button_frame, text="历史记录", font=("Arial", 12),
            command=self.show_history,
            bg="#9c27b0", fg="white", relief=tk.RAISED
        )
        history_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        history_button.bind("<Enter>", lambda e: e.widget.config(bg="#b350c5"))
        history_button.bind("<Leave>", lambda e: e.widget.config(bg="#9c27b0"))
        
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
        
        # 创建科学计算器按钮（起始行从第3行开始）
        start_row = 3
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
                    text, row_idx + start_row, col_idx,
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
                command=self.toggle_angle_mode,
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
        """切换角度/弧度模式"""
        self.degree_mode = not self.degree_mode
        # 更新模式标签
        self.mode_label.config(text="当前模式: DEG" if self.degree_mode else "当前模式: RAD")
        # 更新按钮文本
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") in ("DEG", "RAD"):
                widget.config(text="RAD" if self.degree_mode else "DEG")
    
    def add_to_history(self, expression, result):
        """添加记录到历史记录"""
        # 限制历史记录数量
        if len(self.history) >= self.max_history:
            self.history.pop(0)
        
        # 添加新记录
        self.history.append(f"{expression} = {result}")
    
    def show_history(self):
        """显示历史记录窗口"""
        history_window = tk.Toplevel(self.root)
        history_window.title("计算历史记录")
        history_window.geometry("400x400")
        history_window.configure(bg="#f0f0f0")
        
        # 标题
        title_label = tk.Label(
            history_window, text="计算历史记录", 
            font=("Arial", 16, "bold"), bg="#f0f0f0", pady=10
        )
        title_label.pack(fill=tk.X)
        
        # 滚动文本框显示历史记录
        history_frame = tk.Frame(history_window, bg="#f0f0f0")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_text = tk.Text(
            history_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
            font=("Arial", 12), bg="white", padx=10, pady=10
        )
        history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_text.yview)
        
        # 填充历史记录
        if not self.history:
            history_text.insert(tk.END, "暂无历史记录")
        else:
            for entry in reversed(self.history):  # 最新记录在顶部
                history_text.insert(tk.END, entry + "\n")
        
        history_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 底部按钮
        button_frame = tk.Frame(history_window, bg="#f0f0f0", pady=10)
        button_frame.pack(fill=tk.X, padx=10)
        
        # 清除历史按钮
        clear_button = tk.Button(
            button_frame, text="清除历史", font=("Arial", 12),
            command=lambda: self.clear_history(history_text),
            bg="#ff4444", fg="white", padx=15
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 关闭窗口按钮
        close_button = tk.Button(
            button_frame, text="关闭", font=("Arial", 12),
            command=history_window.destroy,
            bg="#4d94ff", fg="white", padx=15
        )
        close_button.pack(side=tk.RIGHT, padx=5)
    
    def clear_history(self, history_text=None):
        """清除历史记录"""
        self.history = []
        if history_text:
            history_text.config(state=tk.NORMAL)
            history_text.delete(1.0, tk.END)
            history_text.insert(tk.END, "历史记录已清除")
            history_text.config(state=tk.DISABLED)
    
    def button_click(self, value):
        """处理所有按钮点击事件"""
        current = self.display_var.get()
        
        # 特殊功能处理
        if value == "C":
            self.display_var.set("")
        elif value == "⌫":
            self.display_var.set(current[:-1])
        elif value == "←":
            self.create_basic_calculator()
            return
        elif value == "±":
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
                result = math.factorial(num)
                self.display_var.set(str(result))
                self.add_to_history(f"{num}!", result)  # 添加到历史记录
            except:
                self.display_var.set("错误")
        elif value == "√":  # 新增：平方根处理
            # 情况1：当前为空或最后是运算符/左括号 → 追加一个函数起始
            if (not current) or current[-1] in "+-*/([{" :
                self.display_var.set(current + "sqrt(")
            else:
                # 情况2：把当前整体包进 sqrt(...)
                self.display_var.set(f"sqrt({current})")
            return
        elif value in ('sin', 'cos', 'tan', 'log', 'ln'):
            self.display_var.set(f"{value}({current})")
        elif value == "=":
            try:
                expression = current  # 保存原始表达式
                
                safe_expr = current.replace("^", "**")
                safe_expr = safe_expr.replace("π", "3.1415926535")
                safe_expr = safe_expr.replace("e", "2.7182818284")
                # 兜底：如果还有 '√' 直接替换成 sqrt
                safe_expr = safe_expr.replace("√", "sqrt")

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

                if self.degree_mode:
                    def wrap(func):
                        def inner(x):
                            return func(math.radians(x))
                        return inner
                    namespace["sin"] = wrap(math.sin)
                    namespace["cos"] = wrap(math.cos)
                    namespace["tan"] = wrap(math.tan)

                result = eval(safe_expr, {}, namespace)
                formatted = f"{result:.8f}".rstrip('0').rstrip('.')
                final_result = formatted if '.' in formatted else str(int(result))
                
                self.display_var.set(final_result)
                self.add_to_history(expression, final_result)  # 添加到历史记录
            except Exception as e:
                self.display_var.set("错误")
        else:
            if value in ('+', '-', '*', '/') and current and current[-1] in ('+', '-', '*', '/'):
                return
            if value == '.' and (current and '.' in current.split()[-1]):
                return
            self.display_var.set(current + value)

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()