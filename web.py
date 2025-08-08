import tkinter as tk
import time
from tkinter import filedialog, messagebox

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("系统控制面板")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)  # 固定窗口大小
        
        # 创建三个主要区域
        self.create_info_bar()
        self.create_main_interface()
        self.create_button_panel()
        
        # 启动时间更新
        self.update_time()
    
    def create_info_bar(self):
        """创建顶部信息显示栏"""
        info_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        info_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # 日期和时间标签
        self.date_label = tk.Label(
            info_frame, 
            text="日期: 加载中...", 
            fg="white", 
            bg="#2c3e50",
            font=("微软雅黑", 10)
        )
        self.date_label.pack(side=tk.LEFT, padx=20)
        
        self.time_label = tk.Label(
            info_frame, 
            text="时间: 加载中...", 
            fg="white", 
            bg="#2c3e50",
            font=("微软雅黑", 10, "bold")
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        # 状态信息
        self.status_label = tk.Label(
            info_frame, 
            text="系统状态: 就绪", 
            fg="#1abc9c", 
            bg="#2c3e50",
            font=("微软雅黑", 10)
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)
    
    def create_main_interface(self):
        """创建主界面区域"""
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # 主界面标题
        title_label = tk.Label(
            main_frame, 
            text="主控制面板", 
            font=("微软雅黑", 16, "bold"), 
            bg="#ecf0f1",
            pady=20
        )
        title_label.pack(fill=tk.X)
        
        # 内容区域（可扩展）
        content_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SUNKEN)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 示例内容
        info_text = (
            "欢迎使用系统控制面板\n\n"
            "此区域用于显示主要内容和操作结果\n"
            "• 上传的文件将在此处显示详细信息\n"
            "• 系统状态信息可在此查看\n"
            "• 支持多种数据可视化展示\n\n"
            "请使用右侧操作栏开始工作"
        )
        
        content_label = tk.Label(
            content_frame, 
            text=info_text, 
            font=("微软雅黑", 12), 
            bg="white",
            justify=tk.LEFT,
            padx=20,
            pady=20
        )
        content_label.pack(anchor=tk.NW)
    
    def create_button_panel(self):
        """创建右侧按钮操作栏"""
        button_frame = tk.Frame(self.root, bg="#34495e", width=200)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=(0, 5))
        
        # 标题
        panel_title = tk.Label(
            button_frame, 
            text="操作面板", 
            font=("微软雅黑", 12, "bold"), 
            fg="white", 
            bg="#34495e",
            pady=15
        )
        panel_title.pack(fill=tk.X)
        
        # 上传文件按钮
        upload_btn = tk.Button(
            button_frame,
            text="上传文件",
            command=self.upload_file,  
            bg="#3498db",
            fg="white",
            font=("微软雅黑", 10),
            padx=15,
            pady=8,
            width=15,
            relief=tk.FLAT
        )
        upload_btn.pack(pady=15)
        
        # 第二个按钮（示例）
        
        # 分隔线
        separator = tk.Frame(button_frame, height=2, bg="#2c3e50")
        separator.pack(fill=tk.X, pady=20)
        
        # 系统操作按钮
        exit_btn = tk.Button(
            button_frame,
            text="退出系统",
            command=self.exit_application,
            bg="#e74c3c",
            fg="white",
            font=("微软雅黑", 10),
            padx=15,
            pady=8,
            width=15,
            relief=tk.FLAT
        )
        exit_btn.pack(pady=15)
    
    def update_time(self):
        """更新时间显示"""
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y年%m月%d日")
        
        self.time_label.config(text=f"时间: {current_time}")
        self.date_label.config(text=f"日期: {current_date}")
        
        # 每秒更新一次时间
        self.root.after(1000, self.update_time)
    
    def upload_file(self):
        """上传文件功能"""
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt"), ("图像文件", "*.jpg *.png")]
        )
        
        if file_path:
            self.status_label.config(text=f"系统状态: 已选择文件 - {file_path.split('/')[-1]}")
            messagebox.showinfo("上传成功", f"文件已成功加载:\n{file_path}")
        else:
            self.status_label.config(text="系统状态: 文件选择已取消")
    
    def process_data(self):
        """处理数据功能（示例）"""
        self.status_label.config(text="系统状态: 数据处理中...")
        self.root.after(2000, lambda: self.status_label.config(text="系统状态: 数据处理完成"))
    
    def exit_application(self):
        """退出应用程序"""
        if messagebox.askyesno("退出确认", "确定要退出系统吗？"):
            self.root.destroy()
    def create_main_interface(self):
        """创建主界面区域"""
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
        # 主界面标题
        title_label = tk.Label(
            main_frame, 
            text="主控制面板", 
            font=("微软雅黑", 16, "bold"), 
            bg="#ecf0f1",
            pady=20
        )
        title_label.pack(fill=tk.X)
    
        # 内容区域（可扩展）
        content_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SUNKEN)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 示例内容
        info_text = (
            "欢迎使用系统控制面板\n\n"
            "此区域用于显示主要内容和操作结果\n"
            "• 上传的文件将在此处显示详细信息\n"
            "• 系统状态信息可在此查看\n"
            "• 支持多种数据可视化展示\n\n"
            "请使用右侧操作栏开始工作"
        )
        
        content_label = tk.Label(
            content_frame, 
            text=info_text, 
            font=("微软雅黑", 12), 
            bg="white",
            justify=tk.LEFT,
            padx=20,
            pady=20
        )
        content_label.pack(anchor=tk.NW)
        
        # 添加地图显示（示例，需安装 Pillow 包）
        try:
            from PIL import Image, ImageTk
            # 请将以下路径替换为你实际的地图图片路径
            map_image = Image.open(r"C:/Users/Administrator/Pictures/照片/芙宁娜.png")
            # 设置最大尺寸, 等比例缩小图片
            max_size = (600, 600)
            map_image.thumbnail(max_size, Image.Resampling.LANCZOS)
            map_photo = ImageTk.PhotoImage(map_image)
            map_label = tk.Label(content_frame, image=map_photo, bg="white") 
            map_label.image = map_photo  # 保持对图像的引用
            map_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(content_frame, text=f"地图加载失败: {e}", fg="red", bg="white")
            error_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()