import tkinter as tk
import math
import re
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级科学计算器")
        self.root.geometry("400x550")  # 增加高度以容纳历史记录
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)  # 允许调整
        
        # 角度模式设置（默认为角度模式）
        self.degree_mode = True
        
        # 主界面显示屏
        self.display_var = tk.StringVar()
        
        # 历史记录系统
        self.history = []  # 存储历史记录
        self.max_history = 20  # 最大历史记录数

         # 新增：历史面板与模式状态初始化
        self.is_scientific = False 
        self.history_frame = None
        self.history_text = None
        self.history_visible = False

        #函数图像
        self.plot_frame = None
        self.plot_canvas = None
        self.plot_ax = None
        self.plot_func_entry = None
        self.plot_range_entry = None
        self.plot_visible = False
        
        # 创建主计算器界面
        self.create_basic_calculator()

    def create_basic_calculator(self):
        """创建基础计算器界面"""
        # 清除当前所有控件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.is_scientific = False
        
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

        #函数图像按钮
        plot_button = tk.Button(
            button_frame, text="函数图像", font=("Arial", 12),
            command=self.show_plot_panel,
            bg="#4caf50", fg="white", relief=tk.RAISED
        )
        plot_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
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
                    bg="#ff9999" if text in ('C') else ("#4d94ff" if text == "=" else "SystemButtonFace"),
                    fg="white" if text in ('C','=') else "black"
                )
                # "=" 按钮单独一行跨4列
                if text == "=":
                    btn.grid(row=row_idx + start_row, column=0, columnspan=4, 
                             sticky="nsew", padx=2, pady=2)
        # 在基础界面创建完后自适应
        self.resize_to_fit(min_w=400, min_h=520)
    
    def show_scientific_calculator(self):
        """显示科学计算器界面"""
        # 清除当前所有控件
        for widget in self.root.winfo_children():
            widget.destroy()

        self.is_scientific = True
        
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
        plot_button = tk.Button(
            button_frame, text="函数图像", font=("Arial", 12),
            command=self.show_plot_panel,
            bg="#4caf50", fg="white", relief=tk.RAISED
        )
        plot_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # 角度/弧度模式标签
        self.mode_label = tk.Label(
            self.root, text="当前模式: DEG" if self.degree_mode else "当前模式: RAD",
            font=("Arial", 10), bg="#f0f0f0"
        )
        self.mode_label.grid(row=2, column=4, columnspan=2, sticky="e")
        
        # 科学计算器按钮布局
        sci_layout = [
            ['sin', 'cos', 'tan', 'π', 'nCk', 'nPk'],
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
                elif text in ('sin', 'cos', 'tan', 'log', 'ln','nCk','nPk'):
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
        # 在科学界面创建完后自适应
        self.resize_to_fit(min_w=520, min_h=640)
    
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
    
    def add_to_history(self, expression, result=None):
        """添加记录到历史记录"""
        # 限制历史记录数量
        if len(self.history) >= self.max_history:
            self.history.pop(0)
        if result is None:
            self.history.append(expression)
        else:
            self.history.append(f"{expression} = {result}")
        self.refresh_history_panel()
    
    def refresh_history_panel(self):
        """如果历史面板已展开，则刷新显示"""
        if self.history_visible and self.history_text and self.history_text.winfo_exists():
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            for entry in reversed(self.history):
                self.history_text.insert(tk.END, entry + "\n")
            self.history_text.config(state=tk.DISABLED)
        
    def resize_to_fit(self, min_w=380, min_h=520, extra_pad=(10, 10)):
        """根据当前布局自动调整窗口大小"""
        self.root.update_idletasks()  # 刷新布局计算
        self.root.minsize(min_w, min_h) #最小尺寸
        w = max(self.root.winfo_reqwidth(), min_w) + extra_pad[0]
        h = max(self.root.winfo_reqheight(), min_h) + extra_pad[1]
        self.root.geometry(f"{w}x{h}")
    
    def show_history(self):
        """显示历史记录窗口"""
        if self.history_visible and self.history_frame and self.history_frame.winfo_exists():
            self.history_frame.destroy()
            self.history_frame = None
            self.history_text = None
            self.history_visible = False
            self.resize_to_fit()
            return

        # 计算面板应放置的位置与跨列
        if self.is_scientific:
            row_for_history = 10   # 科学布局按钮最后一行是 9，历史放 10
            col_span = 6
        else:
            row_for_history = 8    # 基础布局按钮最后一行是 7，历史放 8
            col_span = 4

        # 历史面板容器
        self.history_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.history_frame.grid(row=row_for_history, column=0, columnspan=col_span,
                                padx=10, pady=4, sticky="nsew")

        # 让历史面板行无伸展权重
        self.root.rowconfigure(row_for_history, weight=1)

        # 标题
        title = tk.Label(self.history_frame, text="计算历史记录",
                         font=("Arial", 12, "bold"), bg="#f0f0f0")
        title.pack(fill=tk.X, pady=(5, 3))

        # 文本+滚动条
        list_frame = tk.Frame(self.history_frame, bg="#f0f0f0")
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_text = tk.Text(
            list_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
            font=("Arial", 11), bg="white", padx=8, pady=8, height=6
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)

        # 填充历史
        if not self.history:
            self.history_text.insert(tk.END, "暂无历史记录")
        else:
            for entry in reversed(self.history):
                self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state=tk.DISABLED)

        # 底部按钮
        btn_bar = tk.Frame(self.history_frame, bg="#f0f0f0")
        btn_bar.pack(fill=tk.X, pady=6)

        # 平分两列
        btn_bar.grid_columnconfigure(0, weight=1)
        btn_bar.grid_columnconfigure(1, weight=1)

        clear_btn = tk.Button(btn_bar, text="清除历史",
                              font=("Arial", 10),
                              command=self.clear_history,
                              bg="#ff4444", fg="white")
        clear_btn.grid(row=0, column=0, padx=6, pady=4, sticky="nsew", ipady=5)

        close_btn = tk.Button(btn_bar, text="关闭",
                              font=("Arial", 10),
                              command=self.show_history,  # 再次调用以收起
                              bg="#4d94ff", fg="white")
        close_btn.grid(row=0, column=1, padx=6, pady=4, sticky="nsew", ipady=5)

        self.history_visible = True
        # 展开后自适应
        self.resize_to_fit()

        # 若历史展开且图像面板也展开，再调整
        if self.plot_visible:
            self.resize_to_fit()
        # ...existing code...
    def show_plot_panel(self):
        """展开/收起函数图像面板"""
        if self.plot_visible and self.plot_frame and self.plot_frame.winfo_exists():
            self.plot_frame.destroy()
            self.plot_frame = None
            self.plot_canvas = None
            self.plot_ax = None
            self.plot_visible = False
            self.resize_to_fit()
            return
       # 计算放置行：历史面板之后
        if self.is_scientific:
            base_last = 9   # 科学按钮最后一逻辑行索引参考
            row_for_history = 10 if self.history_visible else None
            row_for_plot = 11 if self.history_visible else 10
            col_span = 6
        else:
            base_last = 7
            row_for_history = 8 if self.history_visible else None
            row_for_plot = 9 if self.history_visible else 8
            col_span = 4
        self.plot_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.plot_frame.grid(row=row_for_plot, column=0, columnspan=col_span,
                            padx=10, pady=4, sticky="nsew")
        self.root.rowconfigure(row_for_plot, weight=2)
        # 控制栏
        ctrl = tk.Frame(self.plot_frame, bg="#f0f0f0")
        ctrl.pack(fill=tk.X)
        tk.Label(ctrl, text="f(x) =", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT)
        self.plot_func_entry = tk.Entry(ctrl, font=("Arial", 11), width=20)
        self.plot_func_entry.insert(0, "sin(x)")
        self.plot_func_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(ctrl, text="范围 x_min,x_max:", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT, padx=(6, 0))
        self.plot_range_entry = tk.Entry(ctrl, font=("Arial", 11), width=12)
        self.plot_range_entry.insert(0, "-10,10")
        self.plot_range_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="绘制", font=("Arial", 11),
                 command=self.plot_function, bg="#4d94ff", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="关闭", font=("Arial", 11),
                 command=self.show_plot_panel, bg="#9e9e9e", fg="white").pack(side=tk.LEFT, padx=5)
        # 图像区域
        fig = Figure(figsize=(5, 2.6), dpi=100)
        self.plot_ax = fig.add_subplot(111)
        self.plot_ax.grid(True, alpha=0.3)
        self.plot_ax.set_title("函数图像", fontsize=11)
        self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.plot_visible = True
        self.resize_to_fit()

    def plot_function(self):
        """绘制 y = f(x)"""
        if not (self.plot_canvas and self.plot_ax):
            return
        expr_raw = (self.plot_func_entry.get() if self.plot_func_entry else "").strip()
        rng = (self.plot_range_entry.get() if self.plot_range_entry else "").strip()
        if not expr_raw:
            messagebox.showerror("错误", "请输入函数表达式，例如 sin(x)")
            return
        try:
            xmin_s, xmax_s = [s.strip() for s in rng.split(",")]
            xmin, xmax = float(xmin_s), float(xmax_s)
            if xmin >= xmax:
                raise ValueError
        except:
            messagebox.showerror("错误", "范围格式应为: -10,10 且左小右大")
            return
        x = np.linspace(xmin, xmax, 1000)
        # 处理表达式
        expr = expr_raw.replace("^", "**").replace("π", "pi").replace("e", "e")
        # 函数映射
        if self.degree_mode:
            sin = lambda v: np.sin(np.radians(v))
            cos = lambda v: np.cos(np.radians(v))
            tan = lambda v: np.tan(np.radians(v))
        else:
            sin, cos, tan = np.sin, np.cos, np.tan
        env = {"__builtins__": None}
        names = {
            "x": x,
            "sin": sin, "cos": cos, "tan": tan,
            "log": np.log10, "ln": np.log,
            "sqrt": np.sqrt, "abs": np.abs,
            "exp": np.exp, "pow": np.power,
            "pi": np.pi, "e": np.e
       }
        try:
            y = eval(expr, env, names)
        except Exception as ex:
            messagebox.showerror("表达式错误", f"无法计算: {ex}")
            return
        self.plot_ax.clear()
        self.plot_ax.grid(True, alpha=0.3)
        self.plot_ax.plot(x, y, color="#1976d2")
        self.plot_ax.set_xlabel("x")
        self.plot_ax.set_ylabel("y")
        self.plot_ax.set_title(f"y = {expr_raw}", fontsize=11)
        self.plot_canvas.draw()
        self.add_to_history(f"图像: y={expr_raw}  x∈[{xmin},{xmax}]", result=None)
    
    def clear_history(self, history_text=None):
        """清除历史记录"""
        self.history = []
        self.refresh_history_panel()
        # 兼容旧参数，但优先使用内嵌面板的文本控件
        target = self.history_text if self.history_text else history_text
        if target and target.winfo_exists():
            target.config(state=tk.NORMAL)
            target.delete(1.0, tk.END)
            target.insert(tk.END, "历史记录已清除")
            target.config(state=tk.DISABLED)
    
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
        elif value == "nCk":
            self.display_var.set(current+"C(")
        elif value == "nPk":
            self.display_var.set(current + "P(")
        elif value == "=":
            try:
                expression = current  # 保存原始表达式
                
                safe_expr = current.replace("^", "**")
                safe_expr = safe_expr.replace("π", "3.1415926535")
                safe_expr = safe_expr.replace("e", "2.7182818284")
                # 兜底：如果还有 '√' 直接替换成 sqrt
                safe_expr = safe_expr.replace("√", "sqrt")

                def repl_comb(m):
                    n, k = m.group(1), m.group(2)
                    return f"comb({n},{k})"

                def repl_perm(m):
                    n, k = m.group(1), m.group(2)
                    return f"perm({n},{k})"

                safe_expr = expression
                safe_expr = safe_expr.replace("^", "**").replace("π", "3.1415926535").replace("e", "2.7182818284").replace("√", "sqrt")
                safe_expr = re.sub(r'(\d+)C\((\d+)\)', repl_comb, safe_expr)
                safe_expr = re.sub(r'(\d+)P\((\d+)\)', repl_perm, safe_expr)

                namespace = {
                    "__builtins__": None,
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "log": math.log10,
                    "ln": math.log,
                    "sqrt": math.sqrt,
                    "exp": math.exp,
                    "comb": (math.comb if hasattr(math, "comb") else self.combination),
                    "perm": (math.perm if hasattr(math, "perm") else self.permutation)
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
               # 3. 结果格式化
                if isinstance(result, float):
                    formatted = f"{result:.8f}".rstrip('0').rstrip('.')
                    final_result = formatted if '.' in formatted else str(int(result))
                else:
                    final_result = str(result)

                self.display_var.set(final_result)
                self.add_to_history(expression, final_result)
                if "C(" in current:
                    n, k = self.parse_nk_function(current,"C")
                    result = math.comb(n,k) if hasattr(math, 'comb') else self.combination(n, k)
                    self.display_var.set(str(result))
                    self.add_to_history(current, result)
                    return
                if "P(" in current:
                    n, k = self.parse_nk_function(current, "P")
                    result = math.perm(n, k) if hasattr(math, 'perm') else self.permutation(n, k)
                    self.display_var.set(str(result))
                    self.add_to_history(current, result)
                    return 
                
            except Exception as e:
                self.display_var.set("错误")

        else:
            if value in ('+', '-', '*', '/') and current and current[-1] in ('+', '-', '*', '/'):
                return
            if value == '.' and (current and '.' in current.split()[-1]):
                return
            self.display_var.set(current + value)
    def parse_nk_function(self, expr, func_type):
        parts = expr.split(func_type + "(")
        n = int(parts[0])
        k = int(parts[1].rstrip(")"))
        if k > n:
            raise ValueError(f"k值({k})不能大于n值({n})")
        return n, k
    def combination(self, n, k):
        return math.factorial(n)//(math.factorial(k)*math.factorial(n-k))
    
    def permutation(self, n, k):
        return math.factorial(n)//math.factorial(n-k)

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()