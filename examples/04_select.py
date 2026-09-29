"""選択する部品: チェックボックス / ラジオボタン / コンボボックス / スライダー"""
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

def on_change(sender, app_data, user_data):
    # 選択系の部品は、変更後の値が app_data に入ってくる
    dpg.set_value("result", f"{sender} → {app_data!r}（{type(app_data).__name__}）")


with dpg.window(tag="main"):
    dpg.add_checkbox(label="通知を受け取る", tag="notify", callback=on_change)
    dpg.add_radio_button(items=["小", "中", "大"], default_value="中", horizontal=True,
                         tag="size", callback=on_change)
    dpg.add_combo(items=["りんご", "みかん", "ぶどう"], default_value="りんご", width=200,
                  tag="fruit", callback=on_change)
    dpg.add_slider_int(default_value=50, min_value=0, max_value=100, width=200,
                       tag="volume", callback=on_change)
    dpg.add_listbox(items=["東京", "大阪", "名古屋", "福岡"], num_items=4, width=200,
                    tag="city", callback=on_change)
    dpg.add_text("部品を操作すると、ここに値が出ます", tag="result")

dpg.create_viewport(title="04 Select", width=560, height=380)  # タイトルは半角英数字
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

