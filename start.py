import requests
import json
import tkinter as tk
import threading

# 从 config.py 引入密钥
from config import API_KEY, SECRET_KEY

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DebugThinker-PythonUI")
        self.root.geometry("399x666")

        # 输入框和标签
        self.context_code_label = tk.Label(root, text="在此输入代码：")
        self.context_code_label.pack(pady=5)
        self.context_code_entry = tk.Text(root, height=10, width=50)
        self.context_code_entry.pack(pady=5)

        self.context_word_label = tk.Label(root, text="补充描述内容：")
        self.context_word_label.pack(pady=5)
        self.context_word_entry = tk.Text(root, height=10, width=50)
        self.context_word_entry.pack(pady=5)

        # 输出文本框
        self.result_label = tk.Label(root, text="诊断结果：")
        self.output_text = tk.Text(root, height=16, width=50)
        self.output_text.pack(pady=10)

        # 运行按钮
        self.run_button = tk.Button(root, text="运行", command=self.run_program_threaded)
        self.run_button.pack(pady=10)

    def run_program_threaded(self):
        # 在单独的线程中运行 run_program 方法
        thread = threading.Thread(target=self.run_program)
        thread.start()

    def run_program(self):
        context_preset = "假设你是一个有丰富经验的软件开发工程师。我可能会提供一些关于软件开发的具体问题，这些问题信息可能是需要您修改的有Bug无法运行的程序，也有可能是终端中的报错代码，还有可能是其他相关内容。您的工作是简明扼要地站在初学者的角度，分析程序故障原因，作出修改，并指出错在哪里和为什么这样修改，这可能包括建议代码、代码逻辑思路策略。请直接针对下面输入的报错代码与补充描述内容进行回答，无需多说其他内容。"
        context_code = "以下是报错的代码：" + self.context_code_entry.get("1.0", tk.END)
        context_word = "以下是补充描述内容：" + self.context_word_entry.get("1.0", tk.END)
        context = context_preset + context_code + context_word

        self.output_text.delete(1.0, tk.END)  # 清空输出框内容

        self.print_to_output("正在处理中，请稍后...")

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + self.get_access_token()

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": context
                },
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        try:
            result = response.json()
            self.print_to_output(result.get('result'))
        except json.JSONDecodeError:
            self.print_to_output("无法解析响应 JSON 数据")

        self.print_to_output("已完成运行")

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    def print_to_output(self, text):
        # 使用 after 方法确保在主线程中更新 GUI
        self.root.after(0, self.output_text.insert, tk.END, text + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)

    # 将按钮的命令更改为 run_program_threaded
    app.run_button["command"] = app.run_program_threaded

    root.mainloop()
