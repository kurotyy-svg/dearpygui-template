"""
AIが書いたコードに、DearPyGui 1.x 以前の書き方や、
Windowsで強制終了する書き方（日本語のウィンドウタイトル）が混ざっていないか調べる。

使い方:
    python check_old_api.py            # カレントフォルダ以下の .py をすべて調べる
    python check_old_api.py app.py     # ファイルを指定
    python check_old_api.py examples   # フォルダを指定

dearpygui 2.3.1 のソースで確認した内容をもとにしています。
"""
import re
import sys
from pathlib import Path

# 旧API: (種類, 置き換え先)
#   削除   … 2.x に存在しない。AttributeError になる
#   no-op  … 呼べるが何もしない。エラーにならないので気づきにくい
#   非推奨 … 動くが DeprecationWarning が出る
OLD_API = {
    "mvKey_Control":       ("削除", "mvKey_ModCtrl"),
    "mvKey_Shift":         ("削除", "mvKey_ModShift"),
    "mvKey_Alt":           ("削除", "mvKey_ModAlt"),
    "enable_docking":      ("削除", "configure_app(docking=True)"),
    "mvPlotCol_XAxis":     ("削除", "mvPlotCol_AxisText などの Axis 系"),
    "mvPlotCol_YAxis":     ("削除", "mvPlotCol_AxisText などの Axis 系"),
    "mvPlotCol_XAxisGrid": ("削除", "mvPlotCol_AxisGrid"),
    "mvPlotCol_YAxisGrid": ("削除", "mvPlotCol_AxisGrid"),
    "add_font_range_hint": ("no-op", "不要（add_font + bind_font だけでよい）"),
    "add_font_range":      ("no-op", "不要（文字範囲は自動）"),
    "add_font_chars":      ("no-op", "不要（文字範囲は自動）"),
    "add_table_next_column": ("no-op", "不要（行の子要素が順に列へ入る）"),
    "set_staging_mode":    ("no-op", "stage を使う"),
    "add_same_line":       ("非推奨", "with dpg.group(horizontal=True):"),
    "setup_viewport":      ("非推奨", "create_viewport() → setup_dearpygui() → show_viewport()"),
    "cleanup_dearpygui":   ("非推奨", "destroy_context()"),
    "add_hline_series":    ("非推奨", "add_inf_line_series(horizontal=True)"),
    "add_vline_series":    ("非推奨", "add_inf_line_series()"),
    "set_item_theme":      ("非推奨", "bind_item_theme()"),
    "set_item_font":       ("非推奨", "bind_item_font()"),
    "add_spacing":         ("非推奨", "add_spacer()"),
    "add_dummy":           ("非推奨", "add_spacer()"),
    "is_viewport_created": ("非推奨", "is_viewport_ok()"),
    "set_start_callback":  ("非推奨", "set_frame_callback(3, ...)"),
}

# 旧APIではないが、書くと Windows で強制終了する書き方
TITLE_PATTERN = re.compile(r"""create_viewport\([^)]*title\s*=\s*(["'])(.*?)\1""")

PATTERN = re.compile(r"\b(" + "|".join(map(re.escape, OLD_API)) + r")\b")
SELF = Path(__file__).resolve()


def check(path: Path) -> int:
    found = 0
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        code = line.split("#", 1)[0]  # コメントは無視
        for m in PATTERN.finditer(code):
            kind, new = OLD_API[m.group(1)]
            print(f"{path}:{no}: [{kind}] {m.group(1)} → {new}")
            found += 1
        for m in TITLE_PATTERN.finditer(code):
            if not m.group(2).isascii():
                print(f"{path}:{no}: [強制終了] create_viewport のタイトルに日本語 → 半角英数字にする")
                found += 1
    return found


def main() -> None:
    targets = []
    for a in sys.argv[1:] or ["."]:
        p = Path(a)
        targets += sorted(p.rglob("*.py")) if p.is_dir() else [p]
    total = sum(check(p) for p in targets if p.resolve() != SELF)
    print(f"\n{total} 件見つかりました" if total else "旧APIは見つかりませんでした")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
