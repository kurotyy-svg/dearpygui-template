"""
DearPyGui 2.x テンプレート（ニンジン🥕 / py-vbalab.com）

動作確認: dearpygui 2.3.1
AIにコードを書かせるときは、このファイルと AI_RULES.md を一緒に渡して
「このテンプレートの書き方に合わせて」と指示してください。

構成（この順番を崩さないこと）:
  1. create_context()
  2. フォント登録 → bind_font()
  3. ウィンドウ・ウィジェットを作る
  4. キー操作などのハンドラを登録
  5. create_viewport() → setup_dearpygui() → show_viewport()
  6. set_primary_window() → start_dearpygui()
  7. destroy_context()
"""
import functools
import sys
import traceback
from datetime import datetime
from pathlib import Path

import dearpygui
import dearpygui.dearpygui as dpg

# ウィンドウ（ビューポート）のタイトルは半角英数字だけにすること。
# dearpygui 2.3.1 の Windows 版では、日本語タイトルにすると
# エラー表示なしで強制終了する（終了コード 0xC0000005。
# PowerShell の $LASTEXITCODE では -1073741819 と表示される）。
APP_TITLE = "DearPyGui Template"
FONT_SIZE = 18
REQUIRED_VERSION = (2, 3)

# 日本語フォントの候補（上から順に探す）。独自フォントを使うなら先頭に足す。
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\YuGothM.ttc",   # 游ゴシック Medium（Windows 10/11）
    r"C:\Windows\Fonts\meiryo.ttc",    # メイリオ
    r"C:\Windows\Fonts\msgothic.ttc",  # MS ゴシック
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",            # macOS
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux
]


# ------------------------------------------------------------
# 0. バージョン確認
#    古いバージョン向けの記事やAIのコードと混ざるのを防ぐ
# ------------------------------------------------------------
def check_version() -> None:
    ver = tuple(int(x) for x in dearpygui.__version__.split(".")[:2])
    if ver < REQUIRED_VERSION:
        sys.exit(
            f"dearpygui {dearpygui.__version__} が入っています。"
            f"このテンプレートは {'.'.join(map(str, REQUIRED_VERSION))} 以上が前提です。\n"
            "  pip install -U dearpygui"
        )


# ------------------------------------------------------------
# コールバック用の安全装置
#    DearPyGuiはコールバック内で例外が起きてもアプリが落ちない。
#    コンソールにTracebackが出るだけなので、気づかないまま
#    「ボタンを押しても何も起きない」状態になる。
#    → すべてのコールバックにこれを付けて、画面にもエラーを出す。
# ------------------------------------------------------------
def safe_callback(func):
    @functools.wraps(func)
    def wrapper(sender=None, app_data=None, user_data=None):
        try:
            return func(sender, app_data, user_data)
        except Exception as e:
            traceback.print_exc()
            set_status(f"エラー: {type(e).__name__}: {e}", error=True)
    return wrapper


def set_status(message: str, error: bool = False) -> None:
    if dpg.does_item_exist("status"):
        dpg.set_value("status", message)
        dpg.configure_item("status", color=(255, 110, 110) if error else (170, 220, 170))


# ------------------------------------------------------------
# 2. 日本語フォント
#    2.3以降は文字範囲が自動。add_font_range_hint() は不要（呼んでも何もしない）。
#    フォントを登録して bind_font() するだけで日本語が出る。
# ------------------------------------------------------------
def setup_japanese_font() -> None:
    font_path = next((p for p in FONT_CANDIDATES if Path(p).exists()), None)
    if font_path is None:
        # 見つからないと日本語が「????」になる。黙って進めずに必ず知らせる。
        print("警告: 日本語フォントが見つかりません。FONT_CANDIDATES にパスを追加してください。")
        return
    with dpg.font_registry():
        font = dpg.add_font(font_path, FONT_SIZE)
    dpg.bind_font(font)


# ------------------------------------------------------------
# アプリの処理（ここを書き換えて使う）
# ------------------------------------------------------------
@safe_callback
def on_add(sender, app_data, user_data):
    text = dpg.get_value("memo_input").strip()
    if not text:
        set_status("メモが空です", error=True)
        return
    with dpg.table_row(parent="memo_table"):
        dpg.add_text(datetime.now().strftime("%H:%M:%S"))
        dpg.add_text(text)
    dpg.set_value("memo_input", "")
    set_status(f"追加しました: {text}")


@safe_callback
def on_save(sender, app_data, user_data):
    rows = dpg.get_item_children("memo_table", 1)  # slot 1 = 行
    lines = []
    for row in rows:
        cells = dpg.get_item_children(row, 1)
        lines.append("\t".join(dpg.get_value(c) for c in cells))
    # 保存先は app.py と同じフォルダ。Path("memo.txt") だけだと
    # 「実行したときのカレントフォルダ」に保存され、VS Codeの▶実行では迷子になる。
    out = Path(__file__).resolve().parent / "memo.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    # フルパスを出すとユーザー名が画面に映るので、ファイル名だけ表示する
    set_status(f"{len(lines)}件を {out.name}（app.py と同じフォルダ）に保存しました")


@safe_callback
def on_key_s(sender, app_data, user_data):
    # Ctrl判定は mvKey_ModCtrl（左右どちらのCtrlでも反応）
    # ※ 1.x の mvKey_Control は 2.x で削除済み
    if dpg.is_key_down(dpg.mvKey_ModCtrl):
        on_save(None, None, None)


# ------------------------------------------------------------
# 3. 画面を作る
# ------------------------------------------------------------
def build_ui() -> None:
    with dpg.window(tag="main"):
        dpg.add_text("メモを入力して「追加」。Ctrl+S で memo.txt に保存します。")

        # 横並びは group(horizontal=True)（add_same_line は使わない）
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="memo_input", hint="メモを入力", width=300,
                               on_enter=True, callback=on_add)
            dpg.add_button(label="追加", callback=on_add)
            dpg.add_button(label="保存", callback=on_save)

        dpg.add_separator()
        with dpg.table(tag="memo_table", header_row=True, resizable=True,
                       borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True,
                       scrollY=True, height=-40):
            dpg.add_table_column(label="時刻", width_fixed=True, init_width_or_weight=80)
            dpg.add_table_column(label="メモ")

        dpg.add_text("", tag="status")


# ------------------------------------------------------------
# 4. キー操作
# ------------------------------------------------------------
def register_handlers() -> None:
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_S, callback=on_key_s)


def check_title() -> None:
    # 日本語タイトルは Windows で無言のまま落ちるので、起動前に止めて理由を出す
    if not APP_TITLE.isascii():
        sys.exit(
            f"APP_TITLE に半角英数字以外が含まれています: {APP_TITLE!r}\n"
            "Windows版の dearpygui 2.3.1 では、日本語タイトルにすると強制終了します。"
        )


def main() -> None:
    check_version()
    check_title()
    print(f"dearpygui {dearpygui.__version__} で起動します", flush=True)
    dpg.create_context()                       # 1
    setup_japanese_font()                      # 2
    build_ui()                                 # 3
    register_handlers()                        # 4
    dpg.create_viewport(title=APP_TITLE, width=640, height=420)  # 5
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main", True)       # 6
    dpg.start_dearpygui()
    dpg.destroy_context()                      # 7
    print("終了しました", flush=True)


if __name__ == "__main__":
    main()
