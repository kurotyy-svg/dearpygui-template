"""文字を表示する: add_text / add_separator"""
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
    dpg.add_text("ふつうの文字")
    dpg.add_text("色付きの文字", color=(255, 180, 80))         # (R, G, B)
    dpg.add_text("箇条書きの文字", bullet=True)
    dpg.add_text("wrap を指定すると、指定した幅（ピクセル）で自動的に折り返します。"
                 "長い説明文を表示するときに使います。", wrap=300)
    dpg.add_separator()                                          # 区切り線
    dpg.add_separator(label="見出し付きの区切り線")
    dpg.add_text("tag を付けておくと、あとから中身を書き換えられます", tag="msg")
    dpg.set_value("msg", "set_value で書き換えました")

dpg.create_viewport(title="01 Text", width=520, height=330)  # タイトルは半角英数字
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

