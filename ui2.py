"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_m18nomlh = self.__tk_label_m18nomlh(self)
        self.tk_input_m18npgs6 = self.__tk_input_m18npgs6(self)
        self.tk_text_m18npm1i = self.__tk_text_m18npm1i(self)
        self.tk_text_m18nq02g = self.__tk_text_m18nq02g(self)
        self.tk_label_m18nq5ks = self.__tk_label_m18nq5ks(self)
        self.tk_input_m18nqkfq = self.__tk_input_m18nqkfq(self)
        self.tk_button_m18nr7cm = self.__tk_button_m18nr7cm(self)
        self.tk_button_m18nrpsm = self.__tk_button_m18nrpsm(self)
        self.tk_frame_m18ns4xo = self.__tk_frame_m18ns4xo(self)
    def __win(self):
        self.title("Tkinter布局助手")
        # 设置窗口大小、居中
        width = 462
        height = 368
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_label_m18nomlh(self,parent):
        label = Label(parent,text="标签",anchor="center", )
        label.place(x=69, y=27, width=121, height=30)
        return label
    def __tk_input_m18npgs6(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=237, y=29, width=120, height=30)
        return ipt
    def __tk_text_m18npm1i(self,parent):
        text = Text(parent)
        text.place(x=63, y=181, width=150, height=100)
        return text
    def __tk_text_m18nq02g(self,parent):
        text = Text(parent)
        text.place(x=242, y=180, width=150, height=100)
        return text
    def __tk_label_m18nq5ks(self,parent):
        label = Label(parent,text="标签",anchor="center", )
        label.place(x=69, y=78, width=119, height=30)
        return label
    def __tk_input_m18nqkfq(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=237, y=80, width=120, height=30)
        return ipt
    def __tk_button_m18nr7cm(self,parent):
        btn = Button(parent, text="按钮", takefocus=False,)
        btn.place(x=70, y=130, width=118, height=30)
        return btn
    def __tk_button_m18nrpsm(self,parent):
        btn = Button(parent, text="按钮", takefocus=False,)
        btn.place(x=241, y=134, width=111, height=30)
        return btn
    def __tk_frame_m18ns4xo(self,parent):
        frame = Frame(parent,)
        frame.place(x=40, y=10, width=379, height=325)
        return frame
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        pass
    def __style_config(self):
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()