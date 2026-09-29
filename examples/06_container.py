"""部品をまとめる: 枠 / タブ / 折りたたみ"""
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
    with dpg.tab_bar():
        with dpg.tab(label="基本設定"):
            # child_window: 枠で囲んだ領域。高さを超えるとスクロールする
            with dpg.child_window(height=120, border=True):
                for i in range(10):
                    dpg.add_text(f"枠の中の{i + 1}行目")

            # collapsing_header: クリックで開閉できる見出し
            with dpg.collapsing_header(label="詳細設定（クリックで開閉）", default_open=True):
                dpg.add_checkbox(label="自動保存する")
                dpg.add_checkbox(label="起動時に更新を確認する")

        with dpg.tab(label="その他"):
            dpg.add_text("タブを切り替えると、別の画面を表示できます")

dpg.create_viewport(title="06 Container", width=560, height=420)  # タイトルは半角英数字
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

