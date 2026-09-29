"""文字や数値を入力する: add_input_text / add_input_int と get_value"""
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

def show_values(sender, app_data, user_data):
    # 入力された値は get_value(tag) で読み出す
    name = dpg.get_value("name")
    age = dpg.get_value("age")
    memo = dpg.get_value("memo")
    dpg.set_value("result", f"名前: {name} / 年齢: {age}（{type(age).__name__}） / メモ: {len(memo)}文字")


with dpg.window(tag="main"):
    # label は入力欄の右側に表示される（左側に出す方法は 05_layout.py）
    dpg.add_input_text(tag="name", label="名前", hint="名前を入力", width=250)
    dpg.add_input_text(tag="password", label="パスワード", hint="パスワード",
                       password=True, width=250)
    dpg.add_input_int(tag="age", label="年齢（0〜120）", default_value=20,
                      min_value=0, max_value=120,
                      min_clamped=True, max_clamped=True, width=250)
    dpg.add_input_text(tag="memo", label="メモ", multiline=True, width=400, height=80,
                       default_value="複数行の入力欄です")
    dpg.add_button(label="入力内容を表示", callback=show_values)
    dpg.add_text("", tag="result")

dpg.create_viewport(title="03 Input", width=560, height=380)  # タイトルは半角英数字
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

