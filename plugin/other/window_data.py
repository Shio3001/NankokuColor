import tkinter as tk
import copy
import os


class SendWindowData:  # window生成のためのデータ
    def __init__(self, main_window, all_data, UI_parts, UI_auxiliary, all_UI_data):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window
        self.operation = all_data.operation
        self.all_data = all_data
        self.all_UI_data = all_UI_data

        self.GUI_base_color = "#1a1a1a"
        self.GUI_alpha_color = "#000000"

        if not self.main_window is None:
            self.window = tk.Toplevel(self.main_window)
        else:
            self.window = tk.Tk()

        self.UI_parts = UI_parts
        self.UI_auxiliary = UI_auxiliary
        # self.UI_operation =

        self.window.configure(bg=self.GUI_base_color)

    def window_open_close(self, select):
        if select == True:
            self.window.deiconify()
        if select == False:
            self.window.withdraw()

    def window_event(self, processing=None, user_event=None):
        if not processing is None and not user_event is None:
            self.window.bind("<{0}>".format(user_event), processing, "+")

    def new_parts(self, parts_name=None):
        new_parts_obj = self.UI_parts[parts_name].parts().UI_set(self.UI_auxiliary.SendUIData(self.window, self.all_data, self.all_UI_data, self.GUI_base_color, self.GUI_alpha_color))
        return new_parts_obj

    def display_size_get(self):
        self.display_size = [self.window.winfo_screenwidth(), self.window.winfo_screenheight()]
        return self.display_size

    def window_size_set(self, send):
        if not send is None:
            self.window_size = send
        self.window.resizable(width=True, height=True)
        self.window.geometry("{0}x{1}".format(self.window_size[0], self.window_size[1]))

    def window_title_set(self, send):
        if not send is None:
            self.window_name = send
        self.window.title(self.window_name)

    def menubar_set(self, send):
        if not send is None:
            self.menubar_list = send

        window_menubar = tk.Menu(self.window)

        for bar in self.menubar_list:

            main_bar = ""
            bar_name = []
            bar_prg = []
            # 奇数と偶数逆じゃん!とおもったら配列は0からはじまりました
            for i, content in enumerate(bar):
                if i == 0:
                    main_bar = content
                elif i % 2 == 0:
                    bar_prg.append(content)
                    #print("bar偶数情報", content, i)
                elif (i + 1) % 2 == 0:
                    bar_name.append(content)
                    #print("bar奇数情報", content, i)

            pull_down = tk.Menu(window_menubar, tearoff=0)

            window_menubar.add_cascade(label=main_bar, menu=pull_down)  # それぞれ

            for n, p in zip(bar_name, bar_prg):
                pull_down.add_command(label=n, command=p)
                self.operation["log"].write("メニューバー登録 {0} {1}".format(n, p))

        self.operation["log"].write("バー設定終了{0}".format(self.window))

        self.window.config(menu=window_menubar)
        self.window.update()

        # self.window.mainloop()