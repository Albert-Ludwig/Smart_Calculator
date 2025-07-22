# # original
# import os
# import re

# path = r"C:\Users\Administrator\Downloads\BRHelp#4\BRHelp"

# for root, dirs, files in os.walk(path, topdown=False):
#     for name in files:
#         # 对于 Markdown 文件进行处理
#         if name.endswith(".md") or name.endswith(".markdown"):
#             with open(os.path.join(root, name), "r+", encoding="UTF-8") as f:
#                 # 读取文件内容
#                 content = f.read()
#                 # 替换内容
#                 content = re.sub(r'^# ', '!!! ', content, flags=re.MULTILINE)
#                 content = re.sub(r'^## ', '@@@ ', content, flags=re.MULTILINE)
#                 # 将指针移动到文件开头
#                 f.seek(0)
#                 # 清空文件
#                 f.truncate()
#                 # 将修改后的内容写入文件
#                 f.write(content)
#                 # 关闭文件
#                 f.close()

# new full embed #4
import os
import re

path = r"C:\Users\Administrator\Downloads\BRHelp#4\BRHelp"

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        # 对于 Markdown 文件进行处理
        if name.endswith(".md") or name.endswith(".markdown"):
            file_path = os.path.join(root, name)
            with open(os.path.join(root, name), "r+", encoding="UTF-8") as f:
                content = f.read()
                char_count = len(content) # 获取文档总字符数
                if char_count < 1000:
                # 短文档规则：一级标题替换为 @@@
                    content = re.sub(r'^# ', '@@@ ', content, flags=re.MULTILINE)
                else:
                    # 长文档规则：
                    content = re.sub(r'^# ', '!!! ', content, flags=re.MULTILINE)  # 一级标题
                    content = re.sub(r'^## ', '@@@ ', content, flags=re.MULTILINE)  # 二级标题加换行
                # 将指针移动到文件开头
                f.seek(0)
                # 清空文件
                f.truncate()
                # 将修改后的内容写入文件
                f.write(content)
                # 关闭文件
                f.close()