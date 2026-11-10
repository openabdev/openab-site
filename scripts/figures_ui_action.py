"""Animated diagrams for the ui_action dev note (OpenAB Computer 0.10.0), four languages.

Same conventions as figures.py (data-show / data-hl, played by scripts/figs.js, complete static
state without JS or with prefers-reduced-motion). Every visible word comes from F[code].

The dialogs are made-up examples. The sheet figure uses the refs and roles of the real TextEdit
repro from issue #98 (e1 AXWindow → e50 AXSheet → e63 AXButton "Delete"); the error strings are
the tool's own wording. The redaction figure's "••••••••" is illustrative (8 characters).
"""
from figures import S, controls, esc

# State of the 0.10.1 release when this note was built: False = the sheet fix is merged but
# 0.10.1 is not published yet. Flip it (and the note text in notes.py) once it is published.
REL101_PUBLISHED = False

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
        snap1="snap-1", changed="after the change", new_el="a new element",
        stale_lines=[('ui_snapshot → snap-1 · [e3] AXButton "{save}"', ""),
                     ("the dialog is closed and opened again", "aside"),
                     ('ui_action {{ snapshot_id: "snap-1", ref: "e3", action: "press" }}', ""),
                     ("✗ stale ref: e3 … take a new ui_snapshot", "err"),
                     ('ui_snapshot → snap-2 · [e4] AXButton "{save}"', ""),
                     ('ui_action {{ snapshot_id: "snap-2", ref: "e4", action: "press" }}', ""),
                     ("✓ AXPress on e4", "okl")],
        stale_cap="Animation: a stale ref is refused. The agent takes snapshot snap-1, in which "
                  "the Save button is e3. The dialog is then closed and opened again, so its "
                  "button is a new element. ui_action with the old ref is refused with “stale "
                  "ref … take a new ui_snapshot”, and nothing is pressed. The agent takes a new "
                  "snapshot, gets ref e4 for the new button, and the press succeeds.",
        sheet_head="ui_snapshot, text form",
        sheet_calls=['ui_action {{ ref: "e63", action: "press" }}',
                     "0.10.0 · AXWindow(e63) → nil → ✗ stale ref: e63 has left its window",
                     "0.10.1 · AXParent(e63) → [e50] AXSheet, in the snapshot → ✓ accepted"],
        refused="0.10.0: refused", accepted="0.10.1: accepted",
        badge_pending="0.10.1: fix merged in {pr}, release pending",
        badge_out="0.10.1: fix released in {rel}",
        sheet_cap="Animation: the sheet bug. A save sheet slides down from the window's title bar. "
                  "In the tree the sheet (e50) sits under the window (e1), and its Delete button is "
                  "e63. Pressing e63: the 0.10.0 check asks the button for its AXWindow, gets nil, "
                  "and refuses the ref as stale. The fix for 0.10.1 walks up AXParent from the "
                  "button, finds the sheet, sees that the sheet is in the snapshot, and accepts it.",
        agent="agent", sb="openab-sb", sb2="switchboard", mac="computer", audit="audit.jsonl",
        w1="1 log line", w2="2 forward",
        red_lines=[('ui_action {{ ref: "e4", action: "set_value", value: "••••••••" }}', ""),
                   ('before 0.2.2 · audit.jsonl: "value":"••••••••" (as typed)', "err"),
                   ('openab-sb 0.2.2 · audit.jsonl: "value":"<redacted:8 chars>"', "okl"),
                   ("→ the computer still gets the real value", ""),
                   ('canary · exec env API_TOKEN → "<redacted:31 chars>" · canary in the file: 0 times', "okl")],
        red_cap="Animation: audit redaction in openab-sb. A call carries a value through the "
                "switchboard. The switchboard writes the call to its audit log before it forwards "
                "it, so before 0.2.2 the value landed in audit.jsonl as typed. In 0.2.2 the log "
                "line holds “<redacted:8 chars>” instead, and the computer still receives the real "
                "value. The canary run sent a fake token in an exec call's env; its log line shows "
                "“<redacted:31 chars>”, and the token itself appears 0 times in the audit file.",
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
        snap1="snap-1", changed="改變之後", new_el="新的元素",
        stale_lines=[('ui_snapshot → snap-1 · [e3] AXButton "{save}"', ""),
                     ("對話框被關掉，又重新打開", "aside"),
                     ('ui_action {{ snapshot_id: "snap-1", ref: "e3", action: "press" }}', ""),
                     ("✗ stale ref: e3 … take a new ui_snapshot", "err"),
                     ('ui_snapshot → snap-2 · [e4] AXButton "{save}"', ""),
                     ('ui_action {{ snapshot_id: "snap-2", ref: "e4", action: "press" }}', ""),
                     ("✓ 對 e4 執行 AXPress", "okl")],
        stale_cap="動畫：過期的 ref 會被拒絕。agent 拍了快照 snap-1，裡面「儲存」按鈕是 e3。之後對話框"
                  "被關掉又重新打開，按鈕已經是新的元素。拿舊的 ref 呼叫 ui_action，得到「stale ref … "
                  "take a new ui_snapshot」，什麼都沒按。agent 重拍快照，新的按鈕是 e4，這次按下成功。",
        sheet_head="ui_snapshot 的文字版",
        sheet_calls=['ui_action {{ ref: "e63", action: "press" }}',
                     "0.10.0 · AXWindow(e63) → nil → ✗ stale ref: e63 has left its window",
                     "0.10.1 · AXParent(e63) → [e50] AXSheet，在快照裡 → ✓ 接受"],
        refused="0.10.0：拒絕", accepted="0.10.1：接受",
        badge_pending="0.10.1：修正已在 {pr} 合併，尚未發布",
        badge_out="0.10.1：修正已在 {rel} 發布",
        sheet_cap="動畫：sheet 的 bug。儲存用的 sheet 從視窗標題列滑下來。在樹裡，sheet（e50）位在視窗"
                  "（e1）底下，「刪除」按鈕是 e63。按 e63 時，0.10.0 的檢查去問按鈕的 AXWindow，得到 "
                  "nil，就把 ref 當成過期而拒絕。0.10.1 的修正改成從按鈕沿著 AXParent 往上找，找到 "
                  "sheet，確認 sheet 在快照裡，於是接受。",
        agent="agent", sb="openab-sb", sb2="switchboard", mac="電腦", audit="audit.jsonl",
        w1="1 寫紀錄", w2="2 轉送",
        red_lines=[('ui_action {{ ref: "e4", action: "set_value", value: "••••••••" }}', ""),
                   ('0.2.2 之前 · audit.jsonl："value":"••••••••"（原封不動）', "err"),
                   ('openab-sb 0.2.2 · audit.jsonl："value":"<redacted:8 chars>"', "okl"),
                   ("→ 電腦收到的仍是真正的值", ""),
                   ('canary · exec env API_TOKEN → "<redacted:31 chars>" · 檔案裡的 canary：0 次', "okl")],
        red_cap="動畫：openab-sb 稽核紀錄的遮蔽。一次呼叫帶著一個值經過 switchboard。switchboard 會先把"
                "呼叫寫進稽核紀錄，再轉送出去，所以 0.2.2 之前，這個值會原封不動寫進 audit.jsonl。"
                "0.2.2 起，那一行改成「<redacted:8 chars>」，電腦收到的仍是真正的值。canary 測試在一次 "
                "exec 呼叫的 env 裡放了假的 token，紀錄裡那一行顯示「<redacted:31 chars>」，那個 token 本身在稽核檔案裡出現 0 次。",
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
        snap1="snap-1", changed="変化のあと", new_el="新しい要素",
        stale_lines=[('ui_snapshot → snap-1 · [e3] AXButton "{save}"', ""),
                     ("ダイアログを閉じて、もう一度開く", "aside"),
                     ('ui_action {{ snapshot_id: "snap-1", ref: "e3", action: "press" }}', ""),
                     ("✗ stale ref: e3 … take a new ui_snapshot", "err"),
                     ('ui_snapshot → snap-2 · [e4] AXButton "{save}"', ""),
                     ('ui_action {{ snapshot_id: "snap-2", ref: "e4", action: "press" }}', ""),
                     ("✓ e4 に AXPress", "okl")],
        stale_cap="アニメーション：古い ref は拒否されます。エージェントはスナップショット snap-1 を撮り、"
                  "そこでは「保存」ボタンが e3 です。そのあとダイアログが閉じてまた開き、ボタンは新しい"
                  "要素になります。古い ref で ui_action を呼ぶと「stale ref … take a new ui_snapshot」"
                  "で拒否され、何も押されません。撮り直したスナップショットで新しいボタンは e4 になり、"
                  "今度は押せます。",
        sheet_head="ui_snapshot のテキスト形式",
        sheet_calls=['ui_action {{ ref: "e63", action: "press" }}',
                     "0.10.0 · AXWindow(e63) → nil → ✗ stale ref: e63 has left its window",
                     "0.10.1 · AXParent(e63) → [e50] AXSheet、スナップショットにある → ✓ 受け付ける"],
        refused="0.10.0：拒否", accepted="0.10.1：受け付ける",
        badge_pending="0.10.1：修正は {pr} でマージ済み、リリース待ち",
        badge_out="0.10.1：修正は {rel} でリリース",
        sheet_cap="アニメーション：シートのバグ。保存用のシートがウィンドウのタイトルバーから下りてきます。"
                  "ツリーではシート（e50）がウィンドウ（e1）の下にあり、「削除」ボタンは e63 です。e63 を"
                  "押すと、0.10.0 のチェックはボタンに AXWindow を尋ね、nil が返るので、ref を古いものと"
                  "して拒否します。0.10.1 の修正では、ボタンから AXParent をたどってシートを見つけ、"
                  "シートがスナップショットにあることを確かめて受け付けます。",
        agent="エージェント", sb="openab-sb", sb2="スイッチボード", mac="コンピューター",
        audit="audit.jsonl", w1="1 ログを書く", w2="2 転送",
        red_lines=[('ui_action {{ ref: "e4", action: "set_value", value: "••••••••" }}', ""),
                   ('0.2.2 より前 · audit.jsonl："value":"••••••••"（そのまま）', "err"),
                   ('openab-sb 0.2.2 · audit.jsonl："value":"<redacted:8 chars>"', "okl"),
                   ("→ コンピューターには本当の値が届く", ""),
                   ('canary · exec env API_TOKEN → "<redacted:31 chars>" · ファイル内の canary：0 回', "okl")],
        red_cap="アニメーション：openab-sb の監査ログの伏せ字。値を持った呼び出しがスイッチボードを"
                "通ります。スイッチボードは転送する前に呼び出しを監査ログに書くので、0.2.2 より前は値が"
                "そのまま audit.jsonl に残りました。0.2.2 ではその行が「<redacted:8 chars>」になり、"
                "コンピューターには本当の値が届きます。canary のテストでは exec 呼び出しの env に偽の"
                "トークンを入れ、ログの行は「<redacted:31 chars>」で、監査ファイルにトークンそのものは 0 回でした。",
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
        snap1="snap-1", changed="바뀐 뒤", new_el="새 요소",
        stale_lines=[('ui_snapshot → snap-1 · [e3] AXButton "{save}"', ""),
                     ("대화상자가 닫혔다가 다시 열림", "aside"),
                     ('ui_action {{ snapshot_id: "snap-1", ref: "e3", action: "press" }}', ""),
                     ("✗ stale ref: e3 … take a new ui_snapshot", "err"),
                     ('ui_snapshot → snap-2 · [e4] AXButton "{save}"', ""),
                     ('ui_action {{ snapshot_id: "snap-2", ref: "e4", action: "press" }}', ""),
                     ("✓ e4에 AXPress", "okl")],
        stale_cap="애니메이션: 오래된 ref는 거부됩니다. 에이전트가 스냅샷 snap-1을 찍었고, 거기서 \"저장\" "
                  "버튼은 e3입니다. 그 뒤 대화상자가 닫혔다가 다시 열려 버튼은 새 요소가 됩니다. 옛 ref로 "
                  "ui_action을 호출하면 \"stale ref … take a new ui_snapshot\"으로 거부되고 아무것도 "
                  "눌리지 않습니다. 새로 찍은 스냅샷에서 새 버튼은 e4이고, 이번에는 눌립니다.",
        sheet_head="ui_snapshot 텍스트 형식",
        sheet_calls=['ui_action {{ ref: "e63", action: "press" }}',
                     "0.10.0 · AXWindow(e63) → nil → ✗ stale ref: e63 has left its window",
                     "0.10.1 · AXParent(e63) → [e50] AXSheet, 스냅샷에 있음 → ✓ 수락"],
        refused="0.10.0: 거부", accepted="0.10.1: 수락",
        badge_pending="0.10.1: 수정은 {pr}에서 병합됨, 릴리스 대기",
        badge_out="0.10.1: 수정은 {rel}에서 릴리스",
        sheet_cap="애니메이션: 시트 버그. 저장용 시트가 창의 제목 막대에서 내려옵니다. 트리에서 시트(e50)는 "
                  "창(e1) 아래에 있고 \"삭제\" 버튼은 e63입니다. e63을 누르면 0.10.0의 검사는 버튼에 "
                  "AXWindow를 묻고 nil을 받아 ref를 오래된 것으로 거부합니다. 0.10.1의 수정은 버튼에서 "
                  "AXParent를 따라 올라가 시트를 찾고, 시트가 스냅샷에 있음을 확인한 뒤 수락합니다.",
        agent="에이전트", sb="openab-sb", sb2="스위치보드", mac="컴퓨터", audit="audit.jsonl",
        w1="1 로그 기록", w2="2 전달",
        red_lines=[('ui_action {{ ref: "e4", action: "set_value", value: "••••••••" }}', ""),
                   ('0.2.2 이전 · audit.jsonl: "value":"••••••••" (입력 그대로)', "err"),
                   ('openab-sb 0.2.2 · audit.jsonl: "value":"<redacted:8 chars>"', "okl"),
                   ("→ 컴퓨터는 여전히 진짜 값을 받음", ""),
                   ('canary · exec env API_TOKEN → "<redacted:31 chars>" · 파일 속 canary: 0번', "okl")],
        red_cap="애니메이션: openab-sb 감사 로그의 가림 처리. 값을 담은 호출이 스위치보드를 지나갑니다. "
                "스위치보드는 전달하기 전에 호출을 감사 로그에 쓰기 때문에, 0.2.2 이전에는 값이 입력 그대로 "
                "audit.jsonl에 남았습니다. 0.2.2에서는 그 줄에 \"<redacted:8 chars>\"가 남고, 컴퓨터는 "
                "여전히 진짜 값을 받습니다. canary 시험에서는 exec 호출의 env에 가짜 토큰을 넣었고, 로그 "
                "줄에는 \"<redacted:31 chars>\"가 찍혔으며 감사 파일에 토큰 자체는 0번 나왔습니다.",
    ),
}

for _c in F:                      # Pause/Play labels shared with the first note
    F[_c]["ctl"] = S[_c]["ctl"]

PR99 = "https://github.com/openabdev/openab-computer/pull/99"
REL101 = "https://github.com/openabdev/openab-computer/releases/tag/v0.10.1"


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


def _mini(x, title, save, cancel, cls_btn=""):
    return (_window(x, 8, 160, 96, title) +
            f'<rect class="bar" x="{x + 14}" y="48" width="96" height="8" rx="4"/>'
            f'<rect class="bar" x="{x + 14}" y="62" width="64" height="8" rx="4"/>' +
            _btn(x + 30, 74, 56, 22, cancel) +
            _btn(x + 94, 74, 56, 22, save, ok=True))


def fig_stale(code):
    """A stale ref is refused; a new snapshot gives a new ref that works."""
    t = F[code]
    save, cancel = t["save"], t["cancel"]
    svg = ['<svg viewBox="0 0 360 132" role="img" aria-label="' + esc(t["stale_cap"][:60]) + '">',
           _mini(4, t["snap1"], save, cancel),
           '<rect class="frx" x="94" y="70" width="64" height="30" rx="7"/>',
           f'<text class="mono" x="100" y="120">e3</text>',
           f'<g data-show="2"><path class="xmark" d="M118 78 l16 16 M134 78 l-16 16"/></g>',
           f'<g data-show="1"><path class="arr" d="M168 56 h18"/><path class="arrh" d="M188 52 l7 4 l-7 4z"/>',
           _mini(196, t["changed"], save, cancel),
           f'<text class="fs" x="196" y="120">{esc(t["new_el"])}</text></g>',
           '<rect class="frx" data-show="3" x="286" y="70" width="64" height="30" rx="7"/>',
           '<text class="mono" data-show="3" x="292" y="120">e4</text>',
           '<circle class="ring" data-hl="4" cx="318" cy="85" r="20"/>',
           "</svg>"]
    sl = t["stale_lines"]
    steps = [0, 1, 2, 2, 3, 4, 4]
    lines = [(s, txt.replace("{save}", save).replace("{{", "{").replace("}}", "}"), kind, 0)
             for s, (txt, kind) in zip(steps, sl)]
    inner = f'<div class="pair">{"".join(svg)}<div class="treebox">{_steps(lines)}</div></div>'
    return _figure("stale", 5, 1300, t["stale_cap"], inner, t)


def fig_sheet(code):
    """The sheet bug: AXWindow is nil inside an AXSheet; 0.10.1 walks AXParent instead."""
    t = F[code]
    svg = ['<svg viewBox="0 0 360 214" role="img" aria-label="' + esc(t["title"]) + '">',
           '<rect class="screen" x="0" y="0" width="360" height="214"/>',
           _window(20, 8, 320, 198, t["title"]),
           '<rect class="bar" x="40" y="48" width="230" height="8" rx="4"/>',
           '<rect class="bar" x="40" y="64" width="190" height="8" rx="4"/>',
           '<rect class="bar" x="40" y="80" width="210" height="8" rx="4"/>',
           '<g class="sheet" data-show="1">',
           '<rect class="sheetbox" x="60" y="32" width="240" height="112" rx="10"/>',
           '<rect class="bar" x="80" y="50" width="160" height="9" rx="4"/>',
           '<rect class="bar" x="80" y="66" width="120" height="7" rx="3"/>',
           _btn(72, 108, 66, 24, t["delete"], hl="2"),
           _btn(152, 108, 66, 24, t["cancel"]),
           _btn(226, 108, 66, 24, t["save"], ok=True),
           '<circle class="ring" data-hl="2" cx="105" cy="120" r="22"/>',
           "</g>",
           f'<g data-show="3"><path class="xmark" d="M62 158 l12 12 M74 158 l-12 12"/>'
           f'<text class="fmiss" x="82" y="169">{esc(t["refused"])}</text></g>',
           f'<g data-show="4"><path class="vmark" d="M62 184 l5 6 l10 -12"/>'
           f'<text class="fhit" x="82" y="191">{esc(t["accepted"])}</text></g>',
           "</svg>"]
    title, delete = t["title"], t["delete"]
    tree = [(0, f'[e1] AXWindow "{title}"', "", 0),
            (1, '[e50] AXSheet desc="save"', "", 1),
            (2, f'[e63] AXButton "{delete}"', "", 2)]
    sc = [c.replace("{{", "{").replace("}}", "}") for c in t["sheet_calls"]]
    calls = [(2, sc[0], "", 0), (3, sc[1], "err", 0), (4, sc[2], "okl", 0)]
    if REL101_PUBLISHED:
        badge = t["badge_out"].format(rel=f'<a href="{REL101}">OpenAB Computer 0.10.1</a>')
    else:
        badge = t["badge_pending"].format(pr=f'<a href="{PR99}">PR #99</a>')
    badge_html = f'<p class="badge">{badge}</p>\n'
    inner = (f'<div class="pair">{"".join(svg)}<div class="treebox">'
             f'<p class="treehead">{esc(t["sheet_head"])}</p>{_steps(tree)}'
             f'{_steps(calls, "axtree axsteps calls")}</div></div>')
    return _figure("sheetfig", 5, 1400, t["sheet_cap"], inner, t, badge_html)


def fig_redact(code):
    """openab-sb writes the audit line before forwarding; 0.2.2 redacts the value in it."""
    t = F[code]
    svg = ['<svg viewBox="0 0 360 150" role="img" aria-label="' + esc(t["sb2"]) + '">',
           '<g data-hl="0"><rect class="box" x="6" y="14" width="80" height="40" rx="9"/>'
           f'<text class="fm" x="46" y="39" text-anchor="middle">{esc(t["agent"])}</text></g>',
           '<path class="arr" d="M86 34 h40"/><path class="arrh" d="M128 30 l7 4 l-7 4z"/>',
           '<g data-hl="1 2"><rect class="box" x="136" y="8" width="96" height="52" rx="9"/>'
           f'<text class="fm" x="184" y="30" text-anchor="middle">{esc(t["sb"])}</text>'
           f'<text class="fs" x="184" y="47" text-anchor="middle">{esc(t["sb2"])}</text></g>',
           '<g data-show="3"><path class="arr" d="M232 34 h34"/><path class="arrh" d="M268 30 l7 4 l-7 4z"/>'
           f'<text class="fs" x="236" y="26">{esc(t["w2"])}</text></g>',
           '<g data-hl="3"><rect class="box" x="276" y="14" width="78" height="40" rx="9"/>'
           f'<text class="fm" x="315" y="39" text-anchor="middle">{esc(t["mac"])}</text></g>',
           '<g data-show="1"><path class="arr" d="M184 60 v30"/><path class="arrh" d="M180 92 l4 7 l4 -7z"/>'
           f'<text class="fs" x="192" y="80">{esc(t["w1"])}</text></g>',
           '<g data-hl="1 2 4"><path class="filebox" d="M146 102 h64 l12 12 v30 h-76z"/>'
           f'<text class="fs2" x="184" y="130" text-anchor="middle">{esc(t["audit"])}</text></g>',
           "</svg>"]
    rl = t["red_lines"]
    lines = [(i, txt.replace("{{", "{").replace("}}", "}"), kind, 0) for i, (txt, kind) in enumerate(rl)]
    inner = f'<div class="pair">{"".join(svg)}<div class="treebox">{_steps(lines)}</div></div>'
    return _figure("redact", 5, 1400, t["red_cap"], inner, t)


FIGS = {"fig_press": fig_press, "fig_stale": fig_stale, "fig_sheet": fig_sheet,
        "fig_redact": fig_redact}
