"""ボタンを押して処理を動かす: add_button と callback"""
import dearpygui.dearpygui as dpg
from pathlib import Path

# 日本語フォント（app.py と同じ探し方）
FONTS = [r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]

dpg.create_context()
font_path = next((p for p in FONTS if Path(p).exists()), None)
if font_path:
    with dpg.font_registry():
        dpg.bind_font(dpg.add_font(font_path, 18))

count = 0


def on_click(sender, app_data, user_data):
    # sender: 押された部品の tag / app_data: ボタンでは None / user_data: 自分で渡した値
    global count
    count += 1
    dpg.set_value("result", f"{count}回押されました（sender={sender}, user_data={user_data}）")


with dpg.window(tag="main"):
    dpg.add_button(label="押してね", callback=on_click, tag="btn_a", user_data="Aボタン")
    dpg.add_button(label="大きいボタン", width=200, height=40,
                   callback=on_click, tag="btn_b", user_data="Bボタン")
    dpg.add_button(label="小さいボタン", small=True, callback=on_click,
                   tag="btn_c", user_data="Cボタン")
    dpg.add_text("まだ押されていません", tag="result")

dpg.create_viewport(title="02 Button", width=520, height=260)  # タイトルは半角英数字
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

