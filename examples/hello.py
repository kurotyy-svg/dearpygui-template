import dearpygui.dearpygui as dpg

dpg.create_context()                          # 1. 準備

with dpg.window(tag="main"):                  # 2. 画面の中身を作る
    dpg.add_text("Hello, DearPyGui!")
    dpg.add_text("こんにちは")

dpg.create_viewport(title="Hello", width=400, height=200)  # 3. OSのウィンドウを作る
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)          # 4. main をウィンドウいっぱいに広げる
dpg.start_dearpygui()                         # 5. 閉じるまでここで動き続ける
dpg.destroy_context()                         # 6. 後片付け
