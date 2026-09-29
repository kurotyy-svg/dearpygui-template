# DearPyGui コード生成ルール（AIに渡す用）

このファイルを `app.py` と一緒にAIへ渡し、「このルールと app.py の書き方に従って書いて」と指示してください。

---

あなたは DearPyGui **2.3.1** 向けのコードを書きます。学習データには 1.x 以前の書き方が多く含まれていますが、それらは使わないでください。

## 必ず守ること

1. 処理の順番は `create_context()` → フォント登録と `bind_font()` → ウィンドウ作成 → ハンドラ登録 → `create_viewport()` → `setup_dearpygui()` → `show_viewport()` → `set_primary_window()` → `start_dearpygui()` → `destroy_context()`。
2. 日本語フォントは `dpg.add_font(パス, サイズ)` で登録して `dpg.bind_font()` するだけ。`add_font_range_hint` / `add_font_range` / `add_font_chars` は書かない（2.3以降は何もしない関数）。
3. 横並びは `with dpg.group(horizontal=True):`。`add_same_line` は使わない。
4. Ctrl / Shift / Alt の判定は `dpg.mvKey_ModCtrl` / `dpg.mvKey_ModShift` / `dpg.mvKey_ModAlt`。`mvKey_Control` などは存在しない。
5. コールバックには app.py の `@safe_callback` を必ず付ける。DearPyGui はコールバック内の例外でアプリが止まらないため、付けないとエラーに気づけない。
6. ドッキングは `dpg.configure_app(docking=True, docking_space=True)`。`enable_docking` は存在しない。
7. 無限直線は `add_inf_line_series()`（横線は `horizontal=True`）。`add_hline_series` / `add_vline_series` は使わない。
8. テーマのプロット軸色は `mvPlotCol_AxisText` / `mvPlotCol_AxisGrid` などを使う。`mvPlotCol_XAxis` / `mvPlotCol_YAxis` 系は存在しない。
9. `create_viewport(title=...)` のタイトルは**半角英数字だけ**にする。日本語を入れると Windows 版では何のエラーも出さずに強制終了する。画面内の文字（`add_text` やボタンのラベル）は日本語でよい。
10. ウィジェットには文字列の `tag` を付け、`dpg.get_value("tag")` のように参照する。

## 書いたあとに

`python check_old_api.py` を実行し、旧APIが0件であることを確認すること。
