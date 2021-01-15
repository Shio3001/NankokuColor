# coding:utf-8
import sys
import numpy as np
import os
import copy
import tkinter as tk

GUI_main_name = "GUI_main"
GUI_base_color = "#1a1a1a"
GUI_alpha_color = "#000000"


class CentralRole:
    def __init__(self):
        pass

    def main(self, all_elements, elements, internal_operation, app_name):
        expansion_keys = internal_operation["plugin"]["expansion"].keys()
        expansion_list = {}

        GUI_UI = internal_operation["plugin"]["GUI_UI"]

        base_data = [internal_operation, all_elements, elements, GUI_UI]
        send_main = SendWindowData(None, base_data)
        expansion_list["main"] = internal_operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = SendWindowData(expansion_list["main"].window, base_data)
                expansion_list[key] = internal_operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        print(expansion_list)

        expansion_list["main"].window.mainloop()

        print("GUI終了")

        return


class SendWindowData:  # window生成のためのデータ
    def __init__(self, main_window, base_data):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window
        self.operation = base_data[0]
        self.all_elements = base_data[1]
        self.elements = base_data[2]
        print(base_data[3].keys())

        # self.GUI_UI = {key: base_data[3][key].parts(send_UI_data(self.main_window, self.operation)) for key in list(base_data[3].keys())}

        if not self.main_window is None:
            self.window = tk.Toplevel(self.main_window)
        else:
            self.window = tk.Tk()

        self.GUI_UI_parts = base_data[3]
        # self.UI_operation =

        self.window.configure(bg=GUI_base_color)

    def new_parts(self, parts_name=None):
        new_parts_obj = self.GUI_UI_parts[parts_name].parts().UI_set(SendUIData(self.window))
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
        self.window.config(menu=window_menubar)
        for bar in self.menubar_list:
            window_menubar_bar = tk.Menu(window_menubar, tearoff=0)
            window_menubar.add_cascade(label=bar[0], menu=window_menubar_bar)
            for tab in bar[1]:
                window_menubar_bar.add_command(label=tab[0], command=tab[1])

    def main(self):
        def window_exit():
            self.window.destroy()
            print("終了")

        self.window.mainloop()


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window):
        # canvas系：文字入力なし 表示だけ
        # textbox系：文字入力あり 入力あり
        self.window = window
        self.tk = tk

        self.canvas = None

        self.canvas_size = [10, 10]
        self.canvas_position = [0, 0]

        #self.canvas_color = GUI_alpha_color

        self.text = ""
        self.text_position = [0, 0]

        self.event_key = []
        self.event_processing = []

        self.processing = self.template
        self.user_event = "Button-1"

        self.mouse_position = [0, 0]

        self.view_data = {}

        self.motion_history = []

        self.mouse_motion = {"catch": False}
        self.mouse_touch = {"cursor": None}

        self.cursor_default = "arrow"
        self.cursor_event = ""
        self.cursor_design = MouseCursorDesign()

        print("パーツ初期設定")

    def template(self, event):
        # print("関数が指定されていません")
        pass

    # canvasのため

    def canvas_update(self):
        if not self.canvas is None:
            self.canvas.destroy()
            # print("パーツ更新のため削除")

        this_cursor = None

        if not True in self.mouse_touch.values():
            # print("もどす")
            this_cursor = self.cursor_default

        else:
            this_cursor = self.mouse_touch["cursor"]

        self.canvas = tk.Canvas(self.window, highlightthickness=0, width=self.canvas_size[0], height=self.canvas_size[1], cursor=this_cursor)
        self.canvas.place(x=self.canvas_position[0], y=self.canvas_position[1])

        self.paint()

        # if not self.event_key is None and not self.event_processing is None:  # canvasのボタン化

        for k, p in zip(self.event_key, self.event_processing):
            self.canvas.bind('<{0}>'.format(k), p)

        # if self.mouse_motion["catch"] == True:
        #    self.canvas.bind("<Motion>", self.__mouse_position_get)

        # if True in self.mouse_touch.values():

    def paint(self):
        self.canvas.delete("all")

        for data in list(self.view_data.values()):
            if data.fill == True:
                self.canvas.create_rectangle(0, 0, self.canvas_size[0], self.canvas_size[1], fill=data.color, outline="")  # 塗りつぶし
            else:
                self.canvas.create_rectangle(data.position[0], data.position[1], data.size[0], data.size[1], fill=data.color, outline="")  # 塗りつぶし

        if not self.text is None:
            canvas_center = [s / 2 for s in self.canvas_size]
            self.canvas.create_text(canvas_center[0], canvas_center[1], text=self.text)

    def canvas_change_size(self):
        self.canvas.config(width=self.canvas_size[0])
        self.canvas.config(height=self.canvas_size[1])

        self.paint()

    def canvas_change_position(self):
        self.canvas.place(x=self.canvas_position[0], y=self.canvas_position[1])
        self.paint()

    def canvas_for_event(self, processing=None, user_event=None):
        # if processing is None:
        #    self.event_processing.self.template
        #    return

        if not user_event is None:
            self.event_key.append(user_event)
            self.event_processing.append(processing)
        self.canvas_update()

    def edit_canvas_position(self, width_position=None, height_position=None):
        if not width_position is None:
            self.canvas_position[0] = width_position
        if not height_position is None:
            self.canvas_position[1] = height_position
        self.canvas_change_position()

    def edit_canvas_size(self, width_size=None, height_size=None):
        if not width_size is None:
            self.canvas_size[0] = width_size
        if not height_size is None:
            self.canvas_size[1] = height_size
        self.canvas_change_size()

    def edit_canvas_text(self, text=None, width_text_position=None, height_text_position=None):
        self.text = text
        self.text_position = [width_text_position, height_text_position]
        self.canvas_update()

    def set_mouse_motion(self, select, cursor=None):
        #self.canvas.bind("<Motion>", motion)
        self.mouse_motion["catch"] = select

        if self.mouse_motion["catch"] is True:
            self.window.bind("<Motion>", self.__mouse_position_get)

        self.mouse_motion["cursor"] = cursor
        print("追加 ", self.mouse_motion["catch"])
        self.canvas_update()

    """
    def edit_canvas_color(self, color=None):
        if not color is None:
            self.canvas_color = color
        self.canvas_update()
    """

    # canvas内描画のため

    def edit_view_new(self, name):
        self.view_data[name] = PartsViewData()
        self.disclosure()

    def edit_view_color(self, name, color=None):
        if not color is None:
            self.view_data[name].color = color
        self.canvas_update()

    def edit_view_position(self, name, width_position=None, height_position=None):
        if not width_position is None:
            self.view_data[name].position[0] = width_position
        if not height_position is None:
            self.view_data[name].position[1] = height_position
        self.canvas_update()

    def edit_view_size(self, name, width_size=None, height_size=None):
        if not width_size is None:
            self.view_data[name].size[0] = width_size
        if not height_size is None:
            self.view_data[name].size[1] = height_size
        self.canvas_update()

    def set_view_fill(self, name, fill_select):
        self.view_data[name].fill = fill_select
        self.canvas_update()

    def disclosure(self):  # canvasに書かれている描画keyを開示
        print(list(self.view_data.keys()))

    # テキストボックスのため

    def textbox_update(self):
        if not self.canvas is None:
            _ = self.textbox_text_get()
            self.canvas.destroy()
            # print("パーツ更新のため削除")
            # print(self.text)

        self.canvas = tk.Entry()
        self.canvas = self.tk.Entry(width=self.canvas_size[0], highlightthickness=0, relief="flat")
        self.canvas.place(x=self.canvas_position[0], y=self.canvas_position[1])

        self.canvas.insert(0, self.text)

        # if self.mouse_motion["catch"] == True:
        #    self.canvas.bind("<Motion>", self.__mouse_position_get)
        # self.text_box.bind("<Key>", self.textbox_text_event)

    def textbox_text_get(self):
        self.text = self.canvas.get()
        return self.text

    def edit_textbox_position(self, width_position=None, height_position=None):
        if not width_position is None:
            self.canvas_position[0] = width_position
        if not height_position is None:
            self.canvas_position[1] = height_position
        self.textbox_update()

    # 共通処理

    def __canvas_authenticity(self):  # キャンバスかどうかを確認
        if str(type(self.canvas)) == "<class 'tkinter.Canvas'>":
            return True
        else:
            print("canvasが設定されていません")
            return False

    def set_cursor(self, name):  # マウスのcursorをnameに入ってるものに変更する
        self.mouse_touch["cursor"] = name

    def notion_andkey(self, name):  # マウスが動いたときのeventを設定
        self.notion_key = name

    def get_mouse_position(self):
        return copy.deepcopy(self.mouse_motion), copy.deepcopy(self.mouse_touch)

    def __mouse_position_get(self, event):
        #self.mouse_position = [event.x, event.y, event.x + self.position[0], event.y + self.position[1]]
        # print(self.mouse_position)

        # winfo_pointer は 画面左上からの絶対的なマウスの位置
        # winfo_root は画面左上からの絶対的なwindowの位置

        #print("winfo_pointerx :{0} ".format(self.window.winfo_pointerx()))
        #print("winfo_rootx    :{0} ".format(self.window.winfo_rootx()))

        self.mouse_motion["x"] = self.window.winfo_pointerx() - self.window.winfo_rootx()
        self.mouse_motion["y"] = self.window.winfo_pointery() - self.window.winfo_rooty()

        self.mouse_touch["left"] = False  # 左
        self.mouse_touch["right"] = False  # 右
        self.mouse_touch["top"] = False
        self.mouse_touch["under"] = False

        left = self.canvas_position[0]
        right = self.canvas_size[0] + self.canvas_position[0]
        top = self.canvas_position[1]
        under = self.canvas_size[1] + self.canvas_position[1]

        tolerance = 3

        if left - tolerance <= self.mouse_motion["x"] <= left + tolerance:
            self.mouse_touch["left"] = True

        if right - tolerance <= self.mouse_motion["x"] <= right + tolerance:
            self.mouse_touch["right"] = True

        if top - tolerance <= self.mouse_motion["y"] <= top + tolerance:
            self.mouse_touch["top"] = True

        if under - tolerance <= self.mouse_motion["y"] <= under + tolerance:
            self.mouse_touch["under"] = True

        # self.canvas_update()

    # def mouse_position_decision(self):
    #


class PartsViewData:
    def __init__(self):
        self.color = GUI_alpha_color
        self.position = [0, 0]
        self.size = [0, 0]
        self.fill = False

# classひとつひとつに描画するデータを差し込み、classの数forかなにかでまわして描画していく作戦s


class MouseCursorDesign:
    def __init__(self):
        self.round_trip_arrow = None
