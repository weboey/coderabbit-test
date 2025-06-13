import tkinter as tk
import re
from game import *

class MathExpressionGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("24点游戏")
        self.root.geometry("1200x600") # Set the window size to 400x200
        
        # Create a frame to hold the input fields and buttons
        self.frame = tk.Frame(self.root, bg="gray", highlightthickness=0)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.answer=""
        self.num_cnt_label = tk.Label(self.frame, text="数字个数:", font=("Arial", 14))
        self.num_cnt_entry = tk.Entry(self.frame,textvariable=tk.StringVar(value='4'), font=("Arial", 14))
        self.level_label = tk.Label(self.frame, text="难度 (1 or 2):", font=("Arial", 14))
        self.level_entry = tk.Entry(self.frame,textvariable=tk.StringVar(value='1'), font=("Arial", 14))
        self.generate_button = tk.Button(self.frame, text="生成数字", command=self.generate_expressions, font=("Arial", 14))
        self.result_text = tk.Text(self.frame, width=40, font=("Arial", 14))
        self.show_button = tk.Button(self.frame, text="显示答案", command=self.show_answer, font=("Arial", 14))
        self.answer_text=tk.Text(self.frame, width=40, font=("Arial", 14))
        
    def show_answer(self):
        self.answer_text.insert(tk.END,f"{self.answer}\n")
        
    def generate_expressions(self):
        num_cnt = int(self.num_cnt_entry.get())
        level = int(self.level_entry.get())
        # response = requests.get(f"http://localhost:5000/expressions?num_cnt={num_cnt}&level={level}")
        # if response.status_code == 200:
        #     self.answer = response.json()["expression"]
        #     nums = re.findall(r'\d+', self.answer.split('=')[0])
        #     test=f",\t".join(nums)        
        #     self.result_text.insert(tk.END, f"{test}\n")
        # else:
        #     messagebox.showerror("Error", "Failed to generate expressions")
        self.answer=generate(num_cnt,level)
        nums = re.findall(r'\d+', self.answer.split('=')[0])
        test=f",\t".join(nums)
        self.result_text.insert(tk.END, f"{test}\n")

    def run(self):
        self.num_cnt_label.grid(row=0, column=0)
        self.num_cnt_entry.grid(row=1, column=0)
        self.level_label.grid(row=2, column=0)
        self.level_entry.grid(row=3, column=0)
        self.generate_button.grid(row=4, column=0)
        self.show_button.grid(row=5,column=0)
        self.result_text.grid(row=6, column=0,columnspan=2)
        self.answer_text.grid(row=6, column=2)
        
        self.root.mainloop()

if __name__ == "__main__":
    generator = MathExpressionGenerator()
    generator.run()