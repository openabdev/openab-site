"""Animated diagrams for the ui_action dev note (OpenAB Computer 0.10.0), four languages.

Same conventions as figures.py (data-show / data-hl, played by scripts/figs.js, complete static
state without JS or with prefers-reduced-motion). Every visible word comes from F[code].

fig_press: a made-up dialog pressed by ref, the cursor untouched. fig_cmp and perf_table: the
measured screenshot loop vs tree path comparison (numbers in RUN and C below).
"""
from figures import S, controls, esc

F = {
    "en": dict(
        title="Untitled", msg="Save changes?", cancel="Cancel", save="Save", delete="Delete",
        cursor="cursor",
        before="mouse before: (40, 160)", after="mouse after: (40, 160), same point",
        press_lines=['ui_snapshot → [e3] AXButton "{save}" (256,104 70×26)',
                     'ui_action {{ snapshot_id: "snap-…", ref: "e3", action: "press" }}',
                     "→ AXPress on e3: ok"],
        press_cap="Animation: a made-up dialog. The agent takes a snapshot and finds the Save button "
                  "as ref e3. It reads the mouse location, calls ui_action with the snapshot id, "
                  "ref e3 and press, and the button is pressed through the accessibility API. Then "
                  "it reads the mouse location again: the same point, because the cursor never "
                  "moved.",
    ),
    "zh": dict(
        title="未命名", msg="要儲存變更嗎？", cancel="取消", save="儲存", delete="刪除",
        cursor="游標",
        before="動手前的滑鼠位置：(40, 160)", after="動手後的滑鼠位置：(40, 160)，同一點",
        press_lines=['ui_snapshot → [e3] AXButton "{save}" (256,104 70×26)',
                     'ui_action {{ snapshot_id: "snap-…", ref: "e3", action: "press" }}',
                     "→ 對 e3 執行 AXPress：成功"],
        press_cap="動畫：一個示意用的對話框。agent 拍快照，找到「儲存」按鈕是 ref e3。它先讀一次"
                  "滑鼠位置，再帶著快照 id、ref e3 和 press 呼叫 ui_action，按鈕透過 accessibility "
                  "API 被按下。接著再讀一次滑鼠位置：同一個點，因為游標從頭到尾沒有動。",
    ),
    "ja": dict(
        title="名称未設定", msg="変更を保存しますか？", cancel="キャンセル", save="保存", delete="削除",
        cursor="カーソル",
        before="操作前のマウス位置：(40, 160)", after="操作後のマウス位置：(40, 160)、同じ点",
        press_lines=['ui_snapshot → [e3] AXButton "{save}" (256,104 70×26)',
                     'ui_action {{ snapshot_id: "snap-…", ref: "e3", action: "press" }}',
                     "→ e3 に AXPress：成功"],
        press_cap="アニメーション：説明用のダイアログ。エージェントはスナップショットを撮り、「保存」"
                  "ボタンが ref e3 だと見つけます。マウス位置を読み、スナップショット ID、ref e3、"
                  "press を渡して ui_action を呼ぶと、ボタンはアクセシビリティ API で押されます。"
                  "そのあともう一度マウス位置を読むと同じ点です。カーソルは一度も動いていません。",
    ),
    "ko": dict(
        title="제목 없음", msg="변경 사항을 저장할까요?", cancel="취소", save="저장", delete="삭제",
        cursor="커서",
        before="동작 전 마우스 위치: (40, 160)", after="동작 후 마우스 위치: (40, 160), 같은 점",
        press_lines=['ui_snapshot → [e3] AXButton "{save}" (256,104 70×26)',
                     'ui_action {{ snapshot_id: "snap-…", ref: "e3", action: "press" }}',
                     "→ e3에 AXPress: 성공"],
        press_cap="애니메이션: 설명용 대화상자. 에이전트가 스냅샷을 찍고 \"저장\" 버튼이 ref e3임을 "
                  "찾습니다. 마우스 위치를 읽고, 스냅샷 ID, ref e3, press를 넘겨 ui_action을 호출하면 "
                  "버튼이 접근성 API로 눌립니다. 그다음 마우스 위치를 다시 읽으면 같은 점입니다. "
                  "커서는 한 번도 움직이지 않았습니다.",
    ),
}

for _c in F:                      # Pause/Play labels shared with the first note
    F[_c]["ctl"] = S[_c]["ctl"]



def _cursor(x, y):
    return (f'<path class="cursor" d="M{x} {y} l0 16 l4.5 -4.5 l3.5 8 l2.7 -1.3 l-3.5 -8 '
            f'l6.3 0z"/>')


def _window(x, y, w, h, title, tx=None):
    tx = x + w / 2 if tx is None else tx
    return (f'<rect class="win" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
            f'<path class="winbar" d="M{x} {y + 10} a10 10 0 0 1 10 -10 h{w - 20} a10 10 0 0 1 10 10 '
            f'v14 h-{w}z"/>'
            f'<circle class="dot" cx="{x + 14}" cy="{y + 12}" r="4"/>'
            f'<circle class="dot" cx="{x + 26}" cy="{y + 12}" r="4"/>'
            f'<circle class="dot" cx="{x + 38}" cy="{y + 12}" r="4"/>'
            f'<text class="fs2" x="{tx}" y="{y + 17}" text-anchor="middle">{esc(title)}</text>')


def _btn(x, y, w, h, label, ok=False, hl=None, cls=""):
    g = f' data-hl="{hl}"' if hl is not None else ""
    if ok:
        return (f'<g class="okbtn{cls}"{g}><rect class="btnok" x="{x}" y="{y}" width="{w}" height="{h}" '
                f'rx="6"/><text class="fok fbtn" x="{x + w / 2}" y="{y + h / 2 + 4}" '
                f'text-anchor="middle">{esc(label)}</text></g>')
    return (f'<g class="okbtn plain{cls}"{g}><rect class="btn2" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'rx="6"/><text class="fbtn" x="{x + w / 2}" y="{y + h / 2 + 4}" '
            f'text-anchor="middle">{esc(label)}</text></g>')


def _steps(lines, cls="axtree axsteps"):
    """lines: (step, text, kind, level)."""
    out = []
    for step, text, kind, lvl in lines:
        k = f' class="{kind}"' if kind else ""
        out.append(f'<li{k} data-show="{step}" data-hl="{step}" style="--lvl:{lvl}">{esc(text)}</li>')
    return f'<ol class="{cls}">{"".join(out)}</ol>'


def _figure(cls, steps, ms, cap, inner, t, badge=""):
    return f"""<figure class="fig anim {cls}" data-steps="{steps}" data-ms="{ms}" aria-label="{esc(cap)}">
{badge}{inner}
{controls(t)}
<figcaption>{esc(cap)}</figcaption>
</figure>"""


def fig_press(code):
    """Press by ref; the cursor stays put and the mouse reads the same before and after."""
    t = F[code]
    svg = ['<svg viewBox="0 0 360 206" role="img" aria-label="' + esc(t["msg"]) + '">',
           '<rect class="screen" x="0" y="0" width="360" height="206"/>',
           _window(20, 12, 320, 130, t["title"]),
           f'<text class="fs2" x="40" y="80">{esc(t["msg"])}</text>',
           _btn(176, 104, 70, 26, t["cancel"]),
           _btn(256, 104, 70, 26, t["save"], ok=True, hl="2"),
           '<rect class="frx" data-show="0" x="252" y="100" width="78" height="34" rx="8"/>',
           '<circle class="ring" data-hl="2" cx="291" cy="117" r="22"/>',
           _cursor(40, 160),
           f'<text class="fs" x="30" y="190">{esc(t["cursor"])}</text>',
           f'<text class="fs2" data-show="1" data-hl="1" x="96" y="170">{esc(t["before"])}</text>',
           f'<text class="fs2 same" data-show="3" data-hl="3" x="96" y="190">{esc(t["after"])}</text>',
           "</svg>"]
    pl = t["press_lines"]
    save = t["save"]
    lines = [(0, pl[0].replace("{save}", save), "", 0),
             (2, pl[1].replace("{{", "{").replace("}}", "}"), "", 0),
             (2, pl[2], "okl", 0)]
    inner = f'<div class="pair">{"".join(svg)}<div class="treebox">{_steps(lines)}</div></div>'
    return _figure("press", 4, 1400, t["press_cap"], inner, t)


# ---- Screenshot loop (A) vs tree path (B): measured on one TextEdit task -------------------
# Source: the perf run for this note (bench.py, calls.csv, trials.csv, summary.json, kept outside
# this repo). 10 trials per approach on an M4 Mac mini through the switchboard. The running
# counters use the per-step medians; the last value of each counter is the measured per-task
# total (median). Tokens: images by Anthropic's vision guide (standard tier, 1,560 per 1920×1080
# screenshot), text at about 4 characters per token.
VISION = "https://platform.claude.com/docs/en/build-with-claude/vision"
TOK_MAX = 3165
RUN = {
    "A": dict(calls=["1", "2", "3", "4"],
              time=["0.33 s", "0.44 s", "1.32 s", "1.70 s"],
              bytes=["500 KB", "500 KB", "500 KB", "1.0 MB"],
              tokens=[1578, 1582, 1588, 3165],
              moved=[False, True, True, True]),
    "B": dict(calls=["1", "2", "3", "4"],
              time=["0.10 s", "0.17 s", "0.24 s", "0.36 s"],
              bytes=["2.8 KB", "2.9 KB", "3.0 KB", "5.8 KB"],
              tokens=[685, 709, 738, 1435],
              moved=[False, False, False, False]),
}
SENT = "The quick brown fox…"

C = {
    "en": dict(
        head_a="A) Screenshot loop", head_b="B) Tree path",
        steps_a=["screenshot → JPEG 1920×1080, ~500 KB", "mouse click on the text area",
                 f'key type "{SENT}" (44 keys)', "screenshot → check the text"],
        steps_b=['ui_snapshot {app: "TextEdit"} → ~2.8 KB text', "ui_action focus → text area",
                 f'ui_action set_value "{SENT}"', "ui_snapshot → value confirmed"],
        calls="tool calls", time="time", bytes="returned to the agent", tokens="est. input tokens",
        pointer="pointer", moved="moved", still="not moved",
        cap="Animation: the same task done two ways, typing a sentence into a new TextEdit document "
            "and checking it. Both sides make four tool calls; the counters add up each call. "
            "A, the screenshot loop, ends at 1.70 s, 1.0 MB of images and about 3,165 input "
            "tokens (5,427 on a high-resolution model), and the pointer moves. B, the tree path, "
            "ends at 0.36 s, 5.8 KB of text and about 1,435 tokens, and the pointer stays put. "
            "Medians of 10 runs each on an M4 Mac mini through the switchboard.",
        tcap="Measured: 10 runs per approach, one TextEdit task",
        cols=["", "A) Screenshot loop", "B) Tree path"],
        rows=[["Tool calls per task", "4", "4"],
              ["Time per task, median / p90", "1.70 s / 1.83 s", "0.36 s / 0.42 s"],
              ["Time per call, median", "333 ms", "101 ms"],
              ["Images returned", "1,001,879 B (2 JPEGs, 1920×1080)", "0"],
              ["Text returned", "188 B", "5,846 B (2 snapshots, ~2.8 KB each)"],
              ["Est. input tokens, standard model", "3,165", "1,435"],
              ["Est. input tokens, high-res model", "5,427", "1,435"],
              ["Pointer moved", "10 of 10 runs", "0 of 10 runs"],
              ["Text landed in the document", "10 of 10", "10 of 10"]],
    ),
    "zh": dict(
        head_a="A) 截圖迴圈", head_b="B) tree 路徑",
        steps_a=["screenshot → JPEG 1920×1080，約 500 KB", "mouse 點一下文字區",
                 f'key 輸入 "{SENT}"（44 個按鍵）', "screenshot → 確認文字"],
        steps_b=['ui_snapshot {app: "TextEdit"} → 約 2.8 KB 文字', "ui_action focus → 文字區",
                 f'ui_action set_value "{SENT}"', "ui_snapshot → 確認值"],
        calls="工具呼叫", time="時間", bytes="回傳給 agent", tokens="估計輸入 token",
        pointer="游標", moved="移動了", still="沒動",
        cap="動畫：同一件事用兩種方式做，在新的 TextEdit 文件裡輸入一句話並確認。兩邊都是四次工具呼叫，"
            "計數器隨每次呼叫累加。A 截圖迴圈最後是 1.70 秒、1.0 MB 的圖片、約 3,165 個輸入 token"
            "（高解析度模型約 5,427），游標移動了。B tree 路徑最後是 0.36 秒、5.8 KB 的文字、約 1,435 "
            "個 token，游標沒動。數字是一台 M4 Mac mini 經過 switchboard、各跑 10 次的中位數。",
        tcap="實測：每種方式 10 次，同一個 TextEdit 任務",
        cols=["", "A) 截圖迴圈", "B) tree 路徑"],
        rows=[["每個任務的工具呼叫", "4", "4"],
              ["每個任務的時間（中位數 / p90）", "1.70 s / 1.83 s", "0.36 s / 0.42 s"],
              ["每次呼叫的時間（中位數）", "333 ms", "101 ms"],
              ["回傳的圖片", "1,001,879 B（2 張 1920×1080 JPEG）", "0"],
              ["回傳的文字", "188 B", "5,846 B（2 次快照，各約 2.8 KB）"],
              ["估計輸入 token（一般模型）", "3,165", "1,435"],
              ["估計輸入 token（高解析度模型）", "5,427", "1,435"],
              ["游標移動", "10 次中 10 次", "10 次中 0 次"],
              ["文字寫進文件", "10 次中 10 次", "10 次中 10 次"]],
    ),
    "ja": dict(
        head_a="A) スクリーンショットの繰り返し", head_b="B) ツリーを使う",
        steps_a=["screenshot → JPEG 1920×1080、約 500 KB", "mouse でテキスト領域をクリック",
                 f'key で "{SENT}" を入力（44 キー）', "screenshot → 文字を確かめる"],
        steps_b=['ui_snapshot {app: "TextEdit"} → 約 2.8 KB のテキスト', "ui_action focus → テキスト領域",
                 f'ui_action set_value "{SENT}"', "ui_snapshot → 値を確かめる"],
        calls="ツール呼び出し", time="時間", bytes="エージェントに返る量", tokens="推定入力トークン",
        pointer="ポインター", moved="動いた", still="動かない",
        cap="アニメーション：同じ作業を二つのやり方で行います。新しい TextEdit の書類に一文を入力して"
            "確かめる作業です。どちらもツール呼び出しは四回で、カウンターは呼び出しごとに増えます。"
            "A のスクリーンショットの繰り返しは 1.70 秒、画像 1.0 MB、入力トークン約 3,165"
            "（高解像度モデルでは約 5,427）で終わり、ポインターが動きます。B のツリーを使うやり方は "
            "0.36 秒、テキスト 5.8 KB、約 1,435 トークンで終わり、ポインターは動きません。M4 Mac mini "
            "でスイッチボード経由、各 10 回の中央値です。",
        tcap="実測：やり方ごとに 10 回、同じ TextEdit の作業",
        cols=["", "A) スクリーンショットの繰り返し", "B) ツリーを使う"],
        rows=[["作業あたりのツール呼び出し", "4", "4"],
              ["作業あたりの時間（中央値 / p90）", "1.70 s / 1.83 s", "0.36 s / 0.42 s"],
              ["呼び出しあたりの時間（中央値）", "333 ms", "101 ms"],
              ["返ってきた画像", "1,001,879 B（1920×1080 の JPEG 2 枚）", "0"],
              ["返ってきたテキスト", "188 B", "5,846 B（スナップショット 2 回、各約 2.8 KB）"],
              ["推定入力トークン（標準モデル）", "3,165", "1,435"],
              ["推定入力トークン（高解像度モデル）", "5,427", "1,435"],
              ["ポインターが動いた", "10 回中 10 回", "10 回中 0 回"],
              ["文字が書類に入った", "10 回中 10 回", "10 回中 10 回"]],
    ),
    "ko": dict(
        head_a="A) 스크린샷 반복", head_b="B) 트리 경로",
        steps_a=["screenshot → JPEG 1920×1080, 약 500 KB", "mouse로 텍스트 영역 클릭",
                 f'key로 "{SENT}" 입력(키 44개)', "screenshot → 글자 확인"],
        steps_b=['ui_snapshot {app: "TextEdit"} → 약 2.8 KB 텍스트', "ui_action focus → 텍스트 영역",
                 f'ui_action set_value "{SENT}"', "ui_snapshot → 값 확인"],
        calls="도구 호출", time="시간", bytes="에이전트가 받은 양", tokens="추정 입력 토큰",
        pointer="포인터", moved="움직임", still="그대로",
        cap="애니메이션: 같은 작업을 두 가지 방식으로 합니다. 새 TextEdit 문서에 문장 하나를 입력하고 "
            "확인하는 작업입니다. 양쪽 모두 도구 호출은 네 번이고, 카운터는 호출마다 늘어납니다. "
            "A 스크린샷 반복은 1.70초, 이미지 1.0 MB, 입력 토큰 약 3,165개(고해상도 모델은 약 5,427개)로 "
            "끝나고 포인터가 움직입니다. B 트리 경로는 0.36초, 텍스트 5.8 KB, 약 1,435개 토큰으로 끝나고 "
            "포인터는 그대로입니다. M4 Mac mini에서 스위치보드를 거쳐 각각 10번 돌린 중앙값입니다.",
        tcap="실측: 방식마다 10번, 같은 TextEdit 작업",
        cols=["", "A) 스크린샷 반복", "B) 트리 경로"],
        rows=[["작업당 도구 호출", "4", "4"],
              ["작업당 시간(중앙값 / p90)", "1.70 s / 1.83 s", "0.36 s / 0.42 s"],
              ["호출당 시간(중앙값)", "333 ms", "101 ms"],
              ["돌아온 이미지", "1,001,879 B(1920×1080 JPEG 2장)", "0"],
              ["돌아온 텍스트", "188 B", "5,846 B(스냅샷 2번, 각 약 2.8 KB)"],
              ["추정 입력 토큰(표준 모델)", "3,165", "1,435"],
              ["추정 입력 토큰(고해상도 모델)", "5,427", "1,435"],
              ["포인터가 움직임", "10번 중 10번", "10번 중 0번"],
              ["문서에 글자가 들어감", "10번 중 10번", "10번 중 10번"]],
    ),
}


def _vals(values, cls="val"):
    """One element per step; CSS shows the current step's, or the last one when not playing."""
    n = len(values)
    return "".join(f'<span class="{cls}{" fin" if i == n - 1 else ""}" data-hl="{i}">{v}</span>'
                   for i, v in enumerate(values))


def _panel(side, t):
    r = RUN[side]
    steps = t["steps_a"] if side == "A" else t["steps_b"]
    lis = "".join(f'<li data-show="{i}" data-hl="{i}">{esc(x)}</li>' for i, x in enumerate(steps))
    mv = [f'<b class="{"moved" if m else "still"}">{esc(t["moved"] if m else t["still"])}</b>'
          for m in r["moved"]]
    toks = [f"{v:,}" for v in r["tokens"]]
    bars = "".join(f'<i class="{"fin" if i == 3 else ""}" data-hl="{i}" '
                   f'style="width:{v / TOK_MAX * 100:.1f}%"></i>' for i, v in enumerate(r["tokens"]))
    rows = [(t["calls"], r["calls"]), (t["time"], r["time"]), (t["bytes"], r["bytes"]),
            (t["tokens"], toks), (t["pointer"], mv)]
    meters = "".join(f'<div><dt>{esc(k)}</dt><dd>{_vals(v)}</dd></div>' for k, v in rows)
    head = t["head_a"] if side == "A" else t["head_b"]
    return (f'<div class="panel side{side.lower()}"><p class="treehead">{esc(head)}</p>'
            f'<ol class="axtree axsteps">{lis}</ol><dl class="meters">{meters}</dl>'
            f'<div class="tbar" aria-hidden="true">{bars}</div></div>')


def fig_cmp(code):
    """Screenshot loop vs tree path: calls, time, bytes and tokens add up to the measured totals."""
    t = {**C[code], "ctl": S[code]["ctl"]}
    inner = f'<div class="panels">{_panel("A", t)}{_panel("B", t)}</div>'
    return _figure("cmpfig", 4, 1500, t["cap"], inner, t)


def perf_table(code):
    c = C[code]
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in c["cols"])
    body = []
    for row in c["rows"]:
        cells = "".join(f'<td data-label="{esc(h)}">{esc(v)}</td>'
                        for h, v in zip(c["cols"][1:], row[1:]))
        body.append(f'<tr><th scope="row">{esc(row[0])}</th>{cells}</tr>')
    return (f'<div class="cmp-wrap"><table class="cmp perf"><caption>{esc(c["tcap"])}</caption>'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


FIGS = {"fig_press": fig_press, "fig_cmp": fig_cmp, "perf_table": perf_table}
