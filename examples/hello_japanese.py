import dearpygui.dearpygui as dpg

dpg.create_context()

# ここを追加：日本語フォントを登録して、アプリ全体に使う
with dpg.font_registry():
    font = dpg.add_font(r"C:\Windows\Fonts\YuGothM.ttc", 18)   # 游ゴシック、18px
dpg.bind_font(font)

with dpg.window(tag="main"):
    dpg.add_text("Hello, DearPyGui!")
    dpg.add_text("こんにちは")

dpg.create_viewport(title="Hello", width=400, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
