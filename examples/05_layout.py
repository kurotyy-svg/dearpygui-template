"""部品を並べる: 縦並び / 横並び / 余白 / 字下げ / ラベルの位置"""
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

with dpg.window(tag="main"):
    # 何も指定しなければ、上から順に縦に並ぶ
    dpg.add_button(label="縦1")
    dpg.add_button(label="縦2")

    # group(horizontal=True) の中は横に並ぶ
    with dpg.group(horizontal=True):
        dpg.add_button(label="横1")
        dpg.add_button(label="横2")
        dpg.add_button(label="横3")

    dpg.add_spacer(height=15)                      # 縦の余白
    dpg.add_text("indent で字下げ", indent=30)

    dpg.add_separator(label="ラベルの位置")
    # label を付けると、部品の「右側」に表示される
    dpg.add_input_text(label="名前", width=200)

    # 左側に項目名を出したいときは、add_text と横並びにする
    with dpg.group(horizontal=True):
        dpg.add_text("名前")
        dpg.add_input_text(width=200)

    # 項目名の長さがバラバラでも入力欄の位置をそろえたいときは、
    # 枠線なしのテーブルを使う（1列目の幅を固定する）
    with dpg.table(header_row=False):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=130)
        dpg.add_table_column()
        for item in ["氏名", "メールアドレス"]:
            with dpg.table_row():
                dpg.add_text(item)
                dpg.add_input_text(width=200)

dpg.create_viewport(title="05 Layout", width=560, height=420)  # タイトルは半角英数字
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

