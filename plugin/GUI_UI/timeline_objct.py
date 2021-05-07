import sys
import copy
import datetime


class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False

        data.new_diagram("bar")
        data.edit_diagram_size("bar", x=100, y=40)
        data.edit_diagram_position("bar", x=100, y=40)
        data.edit_diagram_color("bar", "#00ff00")
        data.territory_draw()

        #data.timeline_objct_ID = None

        data.pxf = data.plus_px_frame_data(direction=0, debug_name="obj")

        def draw(px_pos, px_size):
            data.edit_diagram_position("bar", x=px_pos)
            data.edit_diagram_size("bar", x=px_size)

            data.territory_draw()

        data.pxf.set_draw_func(draw)

        callback_ope = data.operation["plugin"]["other"]["callback"]
        callback_ope.CallBack(data)

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("bar")
            data.view_pos_sta = data.edit_diagram_position("bar")[0]
            data.view_size_sta = data.edit_diagram_size("bar")[0]

            data.event("sta", info=data.pxf.get_event_data())

        def click_position(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("bar")

            now_mov = copy.deepcopy(now_mouse[0] - data.mouse_sta[0])
            pos = data.view_pos_sta + now_mov

            if data.mouse_touch_sta[0][0]:  # 左側移動
                #print(now_mov, "A")
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta-now_mov)
                # #print("左側移動")

            elif data.mouse_touch_sta[0][1]:  # 右側移動
                data.pxf.set_px_ratio(position=data.view_pos_sta, size=data.view_size_sta+now_mov)
                #print(now_mov, "B")
                # #print("右側移動")

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta)

            data.event("mov", info=data.pxf.get_event_data())

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("bar", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("bar", del_mouse=True)

            data.event("end", info=data.pxf.get_event_data())

        data.add_diagram_event("bar", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_position)
        data.add_diagram_event("bar", "ButtonRelease-1", click_end)

        #data.edit_timeline_range = edit_timeline_range

        return data
