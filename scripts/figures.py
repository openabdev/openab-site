"""Animated diagrams for the ui_snapshot dev note, four languages.

Each figure is inline SVG plus HTML, with every visible word taken from S[code], so nothing
is baked into an image. scripts/figs.js plays them step by step, looping while they are on
screen. Without JS, or with prefers-reduced-motion, the figure shows its final, complete state:

  data-show="k"   hidden while playing until step k
  data-hl="k m"   highlighted at steps k and m
  data-node="eN"  links a tree line with its frame on hover, focus or tap

The dialog is a made-up example; its tree lines use ui_snapshot's real text format
(UITree.swift `line`): `[ref] Role/Subrole "title" = value desc="…" (x,y w×h) flags`.
"""
import html


def esc(s):
    return html.escape(s, quote=True)


S = {
    "en": dict(
        ctl=dict(play="Play", pause="Pause"),
        loop_l="Screenshot loop", loop_r="With ui_snapshot",
        loop_rows_l=[("Screenshot", "a full image, every step"),
                     ("Model guesses x, y", "small targets get missed"),
                     ("mouse moves and clicks", "the real cursor is taken over"),
                     ("Screenshot again to check", "another image")],
        loop_rows_r=[("ui_snapshot", "text and JSON, no image"),
                     ("Find the node by role and title", 'AXButton "{ok}" → ref e7 and its frame'),
                     ("Click the center of its frame", "today with mouse; phase 2: ui_action(ref)"),
                     ("ui_snapshot again to check", "a new snapshot with new refs")],
        meter_l="image tokens", meter_r="image tokens: none",
        loop_cap="Animation: the screenshot loop next to ui_snapshot. On the left, every step "
                 "sends a screenshot, the model guesses coordinates, mouse moves the real cursor "
                 "to click, and another screenshot checks the result, so image tokens add up. On "
                 "the right, ui_snapshot returns text; the agent finds the node by role and title, "
                 "clicks the center of its frame (today still with mouse; phase 2 plans ui_action "
                 "by ref), then takes a new snapshot. No image is sent.",
        dlg=dict(title="Export", name="File name", pw="Password", check="Open when done",
                 cancel="Cancel", ok="OK"),
        tree_head="ui_snapshot, text form",
        tree_cap="Animation: a made-up dialog and the tree ui_snapshot returns for it, built node "
                 "by node in the tool's text form. Each node has a role, a title or value, a ref "
                 "(e1 to e7) and a frame. Frames are in screen points, the same coordinates "
                 "screenshot and mouse use, so each highlighted line matches the outlined area of "
                 "the dialog. The password field shows ‹masked›: the tool never reads its value. "
                 "Hover over, focus or tap a line to see its frame.",
        act_badge="Next: ui_action · in progress, not shipped",
        act_lines=['ui_snapshot → [e7] AXButton "{ok}" (276,184 72×28)',
                   'ui_action {{ snapshot_id: "snap-…", ref: "e7", action: "press" }}',
                   "→ AXPress on e7; the cursor does not move",
                   "ui_snapshot again to check the result"],
        cursor="cursor stays here",
        act_cap="Animation of the planned phase 2, not shipped. After a snapshot, the agent calls "
                "ui_action with the snapshot id, ref e7 and the action press. OpenAB Computer "
                "presses the OK button through the accessibility API and the cursor stays where it "
                "was. The agent then takes a new snapshot to check. This follows the sketch in "
                "PR #93; the details may change.",
    ),
    "zh": dict(
        ctl=dict(play="播放", pause="暫停"),
        loop_l="截圖迴圈", loop_r="改用 ui_snapshot",
        loop_rows_l=[("截圖", "每一步都是一張完整的圖片"),
                     ("模型猜 x, y", "小目標容易點不到"),
                     ("mouse 移過去點擊", "真正的游標被搶走"),
                     ("再截一張圖確認", "又是一張圖片")],
        loop_rows_r=[("ui_snapshot", "文字和 JSON，沒有圖片"),
                     ("用角色和標題找到節點", 'AXButton "{ok}" → ref e7 和它的 frame'),
                     ("點 frame 的中心", "現在用 mouse；第二階段：ui_action(ref)"),
                     ("再拍一次快照確認", "新的快照，新的 ref")],
        meter_l="圖片 token", meter_r="圖片 token：0",
        loop_cap="動畫：截圖迴圈和 ui_snapshot 的對照。左邊每一步都要送一張截圖，模型猜座標，"
                 "mouse 移動真正的游標去點，再截一張圖確認，圖片 token 越疊越多。右邊 ui_snapshot "
                 "回傳文字，agent 用角色和標題找到節點，點它 frame 的中心（現在還是用 mouse，"
                 "第二階段規劃用 ref 呼叫 ui_action），再拍一次新的快照。全程不送圖片。",
        dlg=dict(title="匯出", name="檔案名稱", pw="密碼", check="完成後開啟",
                 cancel="取消", ok="好"),
        tree_head="ui_snapshot 的文字版",
        tree_cap="動畫：一個示意用的對話框，以及 ui_snapshot 為它回傳的樹，用工具的文字格式一個"
                 "節點一個節點長出來。每個節點都有角色、標題或值、ref（e1 到 e7）和 frame。frame "
                 "用的是螢幕點座標，和 screenshot、mouse 同一套，所以亮起來的那一行，會對上對話框裡"
                 "框起來的區域。密碼欄位顯示 ‹masked›：工具從不讀它的值。把游標移到某一行、用鍵盤"
                 "選取或點一下，就能看到它的 frame。",
        act_badge="下一步：ui_action · 開發中，尚未推出",
        act_lines=['ui_snapshot → [e7] AXButton "{ok}" (276,184 72×28)',
                   'ui_action {{ snapshot_id: "snap-…", ref: "e7", action: "press" }}',
                   "→ 對 e7 執行 AXPress，游標沒有移動",
                   "再拍一次 ui_snapshot 確認結果"],
        cursor="游標留在原地",
        act_cap="動畫：規劃中的第二階段，尚未推出。拍完快照後，agent 帶著快照 id、ref e7 和 press "
                "這個動作呼叫 ui_action。OpenAB Computer 透過 accessibility API 按下「好」，游標"
                "留在原地不動。接著 agent 再拍一次快照確認。內容依照 PR #93 裡的草案，細節還可能改變。",
    ),
    "ja": dict(
        ctl=dict(play="再生", pause="一時停止"),
        loop_l="スクリーンショットのループ", loop_r="ui_snapshot を使う",
        loop_rows_l=[("スクリーンショット", "毎回、画像を一枚まるごと"),
                     ("モデルが x, y を推測", "小さな対象は外れやすい"),
                     ("mouse が動いてクリック", "本物のカーソルを取られる"),
                     ("もう一度撮って確認", "また画像が一枚")],
        loop_rows_r=[("ui_snapshot", "テキストと JSON、画像なし"),
                     ("ロールとタイトルでノードを探す", 'AXButton "{ok}" → ref e7 と frame'),
                     ("frame の中心をクリック", "今は mouse、第 2 段階で ui_action(ref)"),
                     ("もう一度スナップショットで確認", "新しいスナップショット、新しい ref")],
        meter_l="画像のトークン", meter_r="画像のトークン：0",
        loop_cap="アニメーション：スクリーンショットのループと ui_snapshot の比較。左では一手ごとに"
                 "スクリーンショットを送り、モデルが座標を推測し、mouse が本物のカーソルを動かして"
                 "クリックし、もう一枚撮って確かめるので、画像のトークンが積み上がります。右では "
                 "ui_snapshot がテキストを返し、エージェントはロールとタイトルでノードを見つけ、その "
                 "frame の中心をクリックし（今はまだ mouse。第 2 段階では ref で ui_action を呼ぶ"
                 "予定）、新しいスナップショットを撮ります。画像は送りません。",
        dlg=dict(title="書き出し", name="ファイル名", pw="パスワード", check="完了後に開く",
                 cancel="キャンセル", ok="OK"),
        tree_head="ui_snapshot のテキスト形式",
        tree_cap="アニメーション：説明用のダイアログと、ui_snapshot がそれについて返すツリーを、"
                 "ツールのテキスト形式で一つずつ組み立てます。各ノードにはロール、タイトルか値、"
                 "ref（e1〜e7）、frame があります。frame は screenshot や mouse と同じ画面のポイント"
                 "座標なので、光った行はダイアログの枠で囲まれた部分と一致します。パスワード欄は "
                 "‹masked› と表示され、ツールは値を読みません。行にポインターを重ねるか、フォーカス"
                 "するか、タップすると、その frame が表示されます。",
        act_badge="次の段階：ui_action · 開発中、未リリース",
        act_lines=['ui_snapshot → [e7] AXButton "{ok}" (276,184 72×28)',
                   'ui_action {{ snapshot_id: "snap-…", ref: "e7", action: "press" }}',
                   "→ e7 に AXPress。カーソルは動かない",
                   "もう一度 ui_snapshot で結果を確認"],
        cursor="カーソルはそのまま",
        act_cap="アニメーション：計画中の第 2 段階で、まだリリースしていません。スナップショットの"
                "あと、エージェントはスナップショット ID、ref e7、press という操作を渡して "
                "ui_action を呼びます。OpenAB Computer はアクセシビリティ API で OK ボタンを押し、"
                "カーソルは元の位置のままです。そのあとエージェントは新しいスナップショットで確かめ"
                "ます。PR #93 の案に沿った内容で、細部は変わる可能性があります。",
    ),
    "ko": dict(
        ctl=dict(play="재생", pause="일시 정지"),
        loop_l="스크린샷 루프", loop_r="ui_snapshot으로",
        loop_rows_l=[("스크린샷", "단계마다 이미지 한 장"),
                     ("모델이 x, y를 짐작", "작은 대상은 빗나가기 쉬움"),
                     ("mouse가 움직여 클릭", "실제 커서를 빼앗김"),
                     ("다시 찍어서 확인", "또 이미지 한 장")],
        loop_rows_r=[("ui_snapshot", "텍스트와 JSON, 이미지 없음"),
                     ("역할과 제목으로 노드 찾기", 'AXButton "{ok}" → ref e7과 frame'),
                     ("frame 중심을 클릭", "지금은 mouse, 2단계는 ui_action(ref)"),
                     ("다시 스냅샷으로 확인", "새 스냅샷, 새 ref")],
        meter_l="이미지 토큰", meter_r="이미지 토큰: 0",
        loop_cap="애니메이션: 스크린샷 루프와 ui_snapshot 비교. 왼쪽은 단계마다 스크린샷을 보내고, "
                 "모델이 좌표를 짐작하고, mouse가 실제 커서를 움직여 클릭하고, 다시 스크린샷으로 "
                 "확인하므로 이미지 토큰이 쌓입니다. 오른쪽은 ui_snapshot이 텍스트를 돌려주고, "
                 "에이전트가 역할과 제목으로 노드를 찾아 그 frame의 중심을 클릭한 뒤(지금은 여전히 "
                 "mouse, 2단계에서는 ref로 ui_action을 호출할 계획) 새 스냅샷을 찍습니다. 이미지는 "
                 "보내지 않습니다.",
        dlg=dict(title="내보내기", name="파일 이름", pw="암호", check="완료 후 열기",
                 cancel="취소", ok="확인"),
        tree_head="ui_snapshot 텍스트 형식",
        tree_cap="애니메이션: 설명용 대화상자와 ui_snapshot이 그에 대해 돌려주는 트리를, 도구의 "
                 "텍스트 형식으로 노드 하나씩 쌓아 갑니다. 노드마다 역할, 제목이나 값, ref(e1~e7), "
                 "frame이 있습니다. frame은 screenshot, mouse와 같은 화면 포인트 좌표라서, 강조된 "
                 "줄은 대화상자에서 테두리로 표시된 영역과 맞습니다. 암호 입력란은 ‹masked›로 "
                 "표시되며 도구는 그 값을 읽지 않습니다. 줄에 포인터를 올리거나, 포커스하거나, "
                 "탭하면 그 frame이 보입니다.",
        act_badge="다음 단계: ui_action · 개발 중, 아직 출시 전",
        act_lines=['ui_snapshot → [e7] AXButton "{ok}" (276,184 72×28)',
                   'ui_action {{ snapshot_id: "snap-…", ref: "e7", action: "press" }}',
                   "→ e7에 AXPress, 커서는 움직이지 않음",
                   "다시 ui_snapshot으로 결과 확인"],
        cursor="커서는 그대로",
        act_cap="애니메이션: 계획 중인 2단계로, 아직 출시되지 않았습니다. 스냅샷을 찍은 뒤 "
                "에이전트는 스냅샷 ID, ref e7, press 동작을 넘겨 ui_action을 호출합니다. OpenAB "
                "Computer는 접근성 API로 확인 버튼을 누르고, 커서는 제자리에 있습니다. 그다음 "
                "에이전트는 새 스냅샷으로 확인합니다. PR #93의 초안을 따른 것이며 세부 사항은 바뀔 수 "
                "있습니다.",
    ),
}


def controls(t):
    c = t["ctl"]
    return (f'<div class="figctl" hidden><button type="button" class="figbtn" '
            f'data-play="{esc(c["play"])}" data-pause="{esc(c["pause"])}">'
            f'{esc(c["pause"])}</button></div>')


def fig_loop(code):
    t = S[code]
    ok = t["dlg"]["ok"]

    def panel(title, rows, meter, side):
        out = [f'<svg viewBox="0 0 320 300" role="img" aria-label="{esc(title)}">',
               f'<text class="ft" x="16" y="22">{esc(title)}</text>']
        for i, (main, sub) in enumerate(rows):
            y = 36 + i * 56
            hl = f"{i} {i + 4}"
            out.append(f'<g data-hl="{hl}"><rect class="box" x="16" y="{y}" width="276" height="46" rx="10"/>'
                       f'<text class="fm" x="28" y="{y + 20}">{esc(main)}</text>'
                       f'<text class="fs" x="28" y="{y + 37}">{esc(sub.format(ok=ok))}</text></g>')
            if i < 3:
                out.append(f'<path class="arr" d="M154 {y + 47} v8"/>')
        # loop-back arrow on the right edge
        out.append('<path class="arr" d="M292 227 h12 V59 h-10"/><path class="arrh" d="M294 55 l7 4 l-7 4z"/>')
        out.append(f'<text class="fs" x="16" y="270">{esc(meter)}</text>')
        out.append('<rect class="meter" x="16" y="278" width="288" height="10" rx="5"/>')
        if side == "l":
            # one segment per screenshot: steps 0, 3, 4, 7
            for j, k in enumerate((0, 3, 4, 7)):
                out.append(f'<rect class="seg" data-show="{k}" x="{16 + j * 72}" y="278" '
                           f'width="70" height="10" rx="5"/>')
        out.append("</svg>")
        return "".join(out)

    return f"""<figure class="fig anim" data-steps="8" data-ms="1100" aria-label="{esc(t['loop_cap'])}">
<div class="panels">
{panel(t['loop_l'], t['loop_rows_l'], t['meter_l'], 'l')}
{panel(t['loop_r'], t['loop_rows_r'], t['meter_r'], 'r')}
</div>
{controls(t)}
<figcaption>{esc(t['loop_cap'])}</figcaption>
</figure>"""


# The made-up dialog, in screen points. (ref, depth, role, title, value, desc, frame, flags)
def nodes(t):
    d = t["dlg"]
    return [
        ("e1", 0, "AXWindow", d["title"], None, None, (40, 20, 320, 210), ""),
        ("e2", 1, "AXGroup", None, None, None, (56, 56, 288, 112), ""),
        ("e3", 2, "AXTextField", None, '"report"', d["name"], (150, 62, 180, 24), " focused"),
        ("e4", 2, "AXTextField/AXSecureTextField", None, "‹masked›", d["pw"], (150, 94, 180, 24), ""),
        ("e5", 2, "AXCheckBox", d["check"], "1", None, (150, 128, 150, 20), ""),
        ("e6", 1, "AXButton", d["cancel"], None, None, (196, 184, 72, 28), ""),
        ("e7", 1, "AXButton", d["ok"], None, None, (276, 184, 72, 28), ""),
    ]


def tree_line(n):
    ref, _, role, title, value, desc, (x, y, w, h), flags = n
    s = f"[{ref}] {role}"
    if title:
        s += f' "{title}"'
    if value:
        s += f" = {value}"
    if desc:
        s += f' desc="{desc}"'
    return s + f" ({x},{y} {w}×{h}){flags}"


def dialog_svg(t, view, label, pressed_step=None, cursor=False):
    d = t["dlg"]
    ns = nodes(t)
    p = [f'<svg viewBox="{view}" role="img" aria-label="{esc(label)}">',
         '<rect class="screen" x="0" y="0" width="400" height="260"/>',
         '<text class="fs" x="4" y="12">(0,0)</text>',
         '<rect class="win" x="40" y="20" width="320" height="210" rx="10"/>',
         '<path class="winbar" d="M40 30 a10 10 0 0 1 10 -10 h300 a10 10 0 0 1 10 10 v14 h-320z"/>',
         '<circle class="dot" cx="54" cy="32" r="4"/><circle class="dot" cx="66" cy="32" r="4"/>'
         '<circle class="dot" cx="78" cy="32" r="4"/>',
         f'<text class="fm" x="200" y="37" text-anchor="middle">{esc(d["title"])}</text>',
         f'<text class="fs2" x="64" y="78">{esc(d["name"])}</text>',
         '<rect class="field focus" x="150" y="62" width="180" height="24" rx="5"/>',
         '<text class="fs2" x="158" y="78">report</text>',
         f'<text class="fs2" x="64" y="110">{esc(d["pw"])}</text>',
         '<rect class="field" x="150" y="94" width="180" height="24" rx="5"/>',
         '<text class="fs2" x="158" y="111">••••••</text>',
         '<rect class="field" x="150" y="131" width="14" height="14" rx="3"/>',
         '<path class="tick" d="M153 138 l3 3 l6 -7"/>',
         f'<text class="fs2" x="170" y="143">{esc(d["check"])}</text>',
         '<rect class="btn2" x="196" y="184" width="72" height="28" rx="7"/>',
         f'<text class="fs2" x="232" y="203" text-anchor="middle">{esc(d["cancel"])}</text>']
    okg = f' data-hl="{pressed_step}"' if pressed_step is not None else ""
    p.append(f'<g class="okbtn"{okg}><rect class="btnok" x="276" y="184" width="72" height="28" rx="7"/>'
             f'<text class="fok" x="312" y="203" text-anchor="middle">{esc(d["ok"])}</text></g>')
    if cursor:
        p.append('<path class="cursor" d="M92 140 l0 18 l5 -5 l4 9 l3 -1.5 l-4 -9 l7 0z"/>')
        p.append(f'<text class="fs" data-hl="2 3" x="104" y="176">{esc(t["cursor"])}</text>')
    else:
        for i, n in enumerate(ns):
            x, y, w, h = n[6]
            p.append(f'<rect class="fr" data-node="{n[0]}" data-hl="{i}" x="{x - 2}" y="{y - 2}" '
                     f'width="{w + 4}" height="{h + 4}" rx="6"/>')
    p.append("</svg>")
    return "".join(p)


def fig_tree(code):
    t = S[code]
    ns = nodes(t)
    lines = "".join(
        f'<li tabindex="0" data-node="{n[0]}" data-show="{i}" data-hl="{i}" style="--lvl:{n[1]}">'
        f'{esc(tree_line(n))}</li>' for i, n in enumerate(ns))
    return f"""<figure class="fig anim" data-steps="7" data-ms="1000" aria-label="{esc(t['tree_cap'])}">
<div class="pair">
{dialog_svg(t, "0 0 400 260", t['dlg']['title'])}
<div class="treebox"><p class="treehead">{esc(t['tree_head'])}</p><ol class="axtree">{lines}</ol></div>
</div>
{controls(t)}
<figcaption>{esc(t['tree_cap'])}</figcaption>
</figure>"""


def fig_action(code):
    t = S[code]
    ok = t["dlg"]["ok"]
    lines = "".join(
        f'<li data-show="{i}" data-hl="{i}">{esc(s.format(ok=ok))}</li>'
        for i, s in enumerate(t["act_lines"]))
    return f"""<figure class="fig anim next" data-steps="4" data-ms="1400" aria-label="{esc(t['act_cap'])}">
<p class="badge">{esc(t['act_badge'])}</p>
<div class="pair">
{dialog_svg(t, "0 122 400 128", t['dlg']['title'], pressed_step=2, cursor=True)}
<div class="treebox"><ol class="axtree axsteps">{lines}</ol></div>
</div>
{controls(t)}
<figcaption>{esc(t['act_cap'])}</figcaption>
</figure>"""


# ── Approach 1 next to approach 4 (the "How does an agent click the right button?" section) ──
# Same made-up dialog on both sides, in screen points. The Save button is small (56×22); on the
# left the guessed point (266,153) lands 5 points below it, on the right the press lands on the
# center of e3's frame. Acting by ref is ui_action (openab-computer PR #96, not released).
AIM = {
    "en": dict(
        l="Screenshot, guess coordinates", r="Read the accessibility tree",
        title="Untitled", msg="Save changes?", save="Save",
        guess="guess: (266, 153)", miss="just missed", hit="center of e3",
        stay="cursor did not move", sent="screenshots sent",
        rows_l=["1  Screenshot", "2  Model guesses x, y", "3  Click: just off the button",
                "4  Screenshot again to check"],
        rows_r=["1  Read the tree: text, no image", '2  Pick ref e3: AXButton "{save}"',
                "3  Act on e3: lands exactly, cursor stays", "4  Read the tree again to check"],
        badge="Acting on a ref without moving the cursor is ui_action: in progress (PR #96), "
              "not released yet.",
        cap="Animation: approach 1 next to approach 4. On the left, the agent takes a screenshot, "
            "the model guesses coordinates, and the click lands just below the small Save button, "
            "so it takes another screenshot; each screenshot adds image tokens. On the right, the "
            "agent reads the accessibility tree as text, picks ref e3 (AXButton \"Save\") and acts "
            "on it: the press lands on the button and the cursor does not move. Acting by ref is "
            "ui_action, in progress in PR #96 and not released yet; today OpenAB Computer still "
            "clicks the center of e3's frame with mouse.",
    ),
    "zh": dict(
        l="看截圖，猜座標", r="讀 accessibility tree",
        title="未命名", msg="要儲存變更嗎？", save="儲存",
        guess="猜：(266, 153)", miss="差一點，沒點中", hit="正中 e3",
        stay="游標沒動", sent="送出的截圖",
        rows_l=["1  截圖", "2  模型猜 x、y", "3  點下去：差一點沒點中", "4  再截一張圖確認"],
        rows_r=["1  讀 tree：文字，沒有圖片", '2  選 ref e3：AXButton "{save}"',
                "3  對 e3 按下：正中，游標不動", "4  再讀一次確認"],
        badge="用 ref 操作、不移動游標的是 ui_action：開發中（PR #96），尚未推出。",
        cap="動畫：第 1 種和第 4 種做法並排。左邊 agent 截圖，模型猜座標，點擊落在小小的「儲存」"
            "按鈕下方一點點，沒點中，只好再截一張圖；每張截圖都會增加圖片 token。右邊 agent 讀 "
            "accessibility tree 的文字，選出 ref e3（AXButton「儲存」）並對它按下：正好按在按鈕上，"
            "游標也沒有移動。用 ref 操作的是 ui_action，還在 PR #96 開發中，尚未推出；目前 OpenAB "
            "Computer 仍用 mouse 點 e3 的 frame 中心。",
    ),
    "ja": dict(
        l="スクリーンショットで推測", r="アクセシビリティツリーを読む",
        title="名称未設定", msg="変更を保存しますか？", save="保存",
        guess="推測：(266, 153)", miss="わずかに外れた", hit="e3 の中心",
        stay="カーソルは動かない", sent="送ったスクリーンショット",
        rows_l=["1  スクリーンショット", "2  モデルが x, y を推測", "3  クリック：ボタンから少し外れる",
                "4  もう一度撮って確認"],
        rows_r=["1  ツリーを読む：テキスト、画像なし", '2  ref e3 を選ぶ：AXButton "{save}"',
                "3  e3 を押す：正確に当たり、カーソルはそのまま", "4  もう一度読んで確認"],
        badge="ref で操作し、カーソルを動かさないのは ui_action です。開発中（PR #96）で、"
              "まだリリースしていません。",
        cap="アニメーション：方法 1 と方法 4 の比較。左では、エージェントがスクリーンショットを撮り、"
            "モデルが座標を推測し、クリックは小さな「保存」ボタンのすぐ下に外れるので、もう一枚撮り"
            "ます。スクリーンショットのたびに画像のトークンが増えます。右では、エージェントが"
            "アクセシビリティツリーをテキストで読み、ref e3（AXButton「保存」）を選んで操作します。"
            "押す位置はボタンに正確に当たり、カーソルは動きません。ref による操作は ui_action で、"
            "PR #96 で開発中、まだリリースしていません。今の OpenAB Computer は mouse で e3 の "
            "frame の中心をクリックします。",
    ),
    "ko": dict(
        l="스크린샷 보고 좌표 짐작", r="접근성 트리 읽기",
        title="제목 없음", msg="변경 사항을 저장할까요?", save="저장",
        guess="짐작: (266, 153)", miss="살짝 빗나감", hit="e3 정중앙",
        stay="커서는 그대로", sent="보낸 스크린샷",
        rows_l=["1  스크린샷", "2  모델이 x, y를 짐작", "3  클릭: 버튼에서 살짝 빗나감",
                "4  다시 찍어서 확인"],
        rows_r=["1  트리 읽기: 텍스트, 이미지 없음", '2  ref e3 고르기: AXButton "{save}"',
                "3  e3 누르기: 정확히 맞고 커서는 그대로", "4  다시 읽어서 확인"],
        badge="ref로 조작하고 커서를 움직이지 않는 것은 ui_action입니다. 개발 중(PR #96)이며 "
              "아직 출시되지 않았습니다.",
        cap="애니메이션: 방법 1과 방법 4 비교. 왼쪽에서는 에이전트가 스크린샷을 찍고, 모델이 좌표를 "
            "짐작하고, 클릭이 작은 \"저장\" 버튼 바로 아래로 빗나가서 스크린샷을 한 장 더 찍습니다. "
            "스크린샷마다 이미지 토큰이 늘어납니다. 오른쪽에서는 에이전트가 접근성 트리를 텍스트로 "
            "읽고 ref e3(AXButton \"저장\")을 골라 누릅니다. 누른 위치가 버튼에 정확히 맞고 커서는 "
            "움직이지 않습니다. ref로 조작하는 것은 ui_action이며 PR #96에서 개발 중이고 아직 "
            "출시되지 않았습니다. 지금의 OpenAB Computer는 mouse로 e3 frame의 중심을 클릭합니다.",
    ),
}


def _cursor(x, y):
    return (f'<path class="cursor" d="M{x} {y} l0 16 l4.5 -4.5 l3.5 8 l2.7 -1.3 l-3.5 -8 '
            f'l6.3 0z"/>')


def _aim_window(t, a, ok_hl=None):
    okg = f' data-hl="{ok_hl}"' if ok_hl is not None else ""
    return ('<rect class="win" x="16" y="34" width="288" height="128" rx="10"/>'
            '<path class="winbar" d="M16 44 a10 10 0 0 1 10 -10 h268 a10 10 0 0 1 10 10 v14 h-288z"/>'
            '<circle class="dot" cx="30" cy="46" r="4"/><circle class="dot" cx="42" cy="46" r="4"/>'
            '<circle class="dot" cx="54" cy="46" r="4"/>'
            f'<text class="fs2" x="160" y="50" text-anchor="middle">{esc(a["title"])}</text>'
            f'<text class="fs2" x="32" y="118">{esc(a["msg"])}</text>'
            '<rect class="btn2" x="168" y="126" width="56" height="22" rx="6"/>'
            f'<text class="fbtn" x="196" y="141" text-anchor="middle">{esc(t["dlg"]["cancel"])}</text>'
            f'<g class="okbtn"{okg}><rect class="btnok" x="232" y="126" width="56" height="22" rx="6"/>'
            f'<text class="fok fbtn" x="260" y="141" text-anchor="middle">{esc(a["save"])}</text></g>')


def _rows(rows, save):
    return "".join(f'<text class="fs2" data-hl="{i}" x="16" y="{254 + i * 18}">'
                   f'{esc(r.format(save=save))}</text>' for i, r in enumerate(rows))


def fig_aim(code):
    t, a = S[code], AIM[code]
    thumb = ('<rect class="thumb" x="{x}" y="184" width="64" height="40" rx="4"/>'
             '<rect class="thumbbar" x="{x}" y="184" width="64" height="7" rx="3"/>'
             '<rect class="thumbbtn" x="{bx}" y="211" width="12" height="6" rx="2"/>')
    left = [f'<svg viewBox="0 0 320 350" role="img" aria-label="{esc(a["l"])}">',
            f'<text class="ft" x="16" y="22">{esc(a["l"])}</text>',
            _aim_window(t, a),
            '<rect class="flash" data-hl="0 3" x="16" y="34" width="288" height="128" rx="10"/>',
            f'<g data-show="1"><circle class="aim" cx="266" cy="153" r="6"/>'
            '<path class="aim" d="M256 153 h20 M266 143 v20"/>'
            f'<text class="fs" x="24" y="140">{esc(a["guess"])}</text></g>',
            f'<g data-show="2"><circle class="miss" cx="266" cy="153" r="10"/>'
            f'<text class="fmiss" x="254" y="176" text-anchor="end">{esc(a["miss"])}</text></g>',
            f'<g class="cur" data-hl="0 1">{_cursor(266, 153)}</g>',
            f'<g data-show="0">{thumb.format(x=16, bx=60)}</g>',
            f'<g data-show="3">{thumb.format(x=88, bx=132)}</g>',
            f'<text class="fs" x="164" y="208">{esc(a["sent"])}</text>',
            _rows(a["rows_l"], a["save"]),
            f'<text class="fs" x="16" y="328">{esc(t["meter_l"])}</text>',
            '<rect class="meter" x="16" y="334" width="288" height="10" rx="5"/>',
            '<rect class="seg" data-show="0" x="16" y="334" width="70" height="10" rx="5"/>',
            '<rect class="seg" data-show="3" x="88" y="334" width="70" height="10" rx="5"/>',
            "</svg>"]
    save, cancel = a["save"], t["dlg"]["cancel"]
    tree = [(0, f'[e1] AXWindow "{a["title"]}"', ""),
            (1, f'[e2] AXButton "{cancel}" (168,126 56×22)', ""),
            (1, f'[e3] AXButton "{save}" (232,126 56×22)', ' data-hl="1 2"')]
    lines = "".join(f'<text class="mono"{hl} x="{24 + lvl * 12}" y="{198 + i * 14}">{esc(s)}</text>'
                    for i, (lvl, s, hl) in enumerate(tree))
    right = [f'<svg viewBox="0 0 320 350" role="img" aria-label="{esc(a["r"])}">',
             f'<text class="ft" x="16" y="22">{esc(a["r"])}</text>',
             _aim_window(t, a, ok_hl=2),
             '<rect class="frx" data-show="1" x="229" y="123" width="62" height="28" rx="8"/>',
             f'<g data-show="2"><circle class="hit" cx="260" cy="137" r="10"/>'
             f'<text class="fhit" x="304" y="176" text-anchor="end">{esc(a["hit"])}</text>'
             f'<text class="fs" x="130" y="94">{esc(a["stay"])}</text></g>',
             _cursor(116, 78),
             '<rect class="treebg" x="16" y="184" width="288" height="50" rx="6"/>',
             f'<g data-show="0">{lines}</g>',
             _rows(a["rows_r"], save),
             f'<text class="fs" x="16" y="328">{esc(t["meter_r"])}</text>',
             '<rect class="meter" x="16" y="334" width="288" height="10" rx="5"/>',
             "</svg>"]
    return f"""<figure class="fig anim aim" data-steps="4" data-ms="1300" aria-label="{esc(a['cap'])}">
<div class="panels">
<div class="panel">{"".join(left)}</div>
<div class="panel">{"".join(right)}<p class="badge">{esc(a['badge'])}</p></div>
</div>
{controls(t)}
<figcaption>{esc(a['cap'])}</figcaption>
</figure>"""


# ── Comparison table for the four approaches. On narrow screens style.css turns each row
# into a card and shows the column name from data-label next to each value.
CMP = {
    "en": dict(
        cap="The four approaches side by side",
        cols=["Approach", "Cost per step", "Accuracy", "Coverage", "Knows state (enabled, value)",
              "Takes over the cursor", "Needs permission"],
        rows=[["1. Screenshot, guess coordinates", "High: an image every step", "Low: coordinates are guessed",
               "Widest: anything visible", "✗ No", "✓ Yes", "Yes: screen capture and input"],
              ["2. Numbered marks (set-of-mark)", "High: image plus a detection model",
               "Medium: depends on detection", "Wide: what the detector finds", "✗ No", "✓ Yes",
               "Yes: screen capture and input"],
              ["3. App API or script", "Low: one command", "High", "Narrow: only apps that support it",
               "Depends on the app", "✗ No", "Depends (macOS: Automation)"],
              ["4. Accessibility tree", "Low: a block of text", "High: exact positions",
               "Medium: standard UI; canvas and games often empty", "✓ Yes, from the system",
               "✗ No, when acting by ref*", "Yes: Accessibility"]],
        note="* Acting by ref without moving the cursor is <code>ui_action</code>, in progress in "
             "{pr96} and not released yet. Today an agent on OpenAB Computer still clicks with "
             "<code>mouse</code>, which moves the cursor.",
    ),
    "zh": dict(
        cap="四種做法對照",
        cols=["做法", "每步成本", "準確度", "涵蓋範圍", "知道狀態（能不能按、目前的值）", "搶走游標", "需要權限"],
        rows=[["1. 看截圖，猜座標", "高：每步一張圖", "低：座標用猜的", "最廣：看得到就行", "✗ 不知道",
               "✓ 會", "要：截圖和操控輸入"],
              ["2. 標號再選（set-of-mark）", "高：圖片加偵測模型", "中：看偵測準不準", "廣：偵測得到就行",
               "✗ 不知道", "✓ 會", "要：截圖和操控輸入"],
              ["3. app 的 API 或腳本", "低：一個指令", "高", "窄：要 app 有支援", "看 app", "✗ 不會",
               "看情況（macOS：自動化）"],
              ["4. accessibility tree", "低：一段文字", "高：位置是確切的", "中：標準介面；canvas、遊戲常是空的",
               "✓ 系統直接給", "✗ 用 ref 操作時不會*", "要：輔助使用"]],
        note="* 用 ref 操作、不移動游標的是 <code>ui_action</code>，還在 {pr96} 開發中，尚未推出。"
             "目前 agent 透過 OpenAB Computer 還是用 <code>mouse</code> 點擊，游標會動。",
    ),
    "ja": dict(
        cap="四つの方法の比較",
        cols=["方法", "一手ごとのコスト", "正確さ", "対応範囲", "状態がわかるか（押せるか、今の値）",
              "カーソルを取られるか", "必要な権限"],
        rows=[["1. スクリーンショットで座標を推測", "高い：毎回画像一枚", "低い：座標は推測",
               "最も広い：見えれば操作できる", "✗ わからない", "✓ 取られる", "必要：画面収録と入力の操作"],
              ["2. 番号を付けて選ぶ（set-of-mark）", "高い：画像と検出モデル", "中：検出の精度しだい",
               "広い：検出できれば操作できる", "✗ わからない", "✓ 取られる", "必要：画面収録と入力の操作"],
              ["3. アプリの API やスクリプト", "低い：コマンド一つ", "高い", "狭い：対応アプリだけ",
               "アプリしだい", "✗ 取られない", "場合による（macOS：オートメーション）"],
              ["4. アクセシビリティツリー", "低い：テキストだけ", "高い：位置が正確",
               "中：標準的な UI。canvas やゲームは空のことが多い", "✓ システムが返す",
               "✗ ref で操作すれば取られない*", "必要：アクセシビリティ"]],
        note="* ref で操作し、カーソルを動かさないのは <code>ui_action</code> で、{pr96} で開発中、"
             "まだリリースしていません。今のところ OpenAB Computer のエージェントは "
             "<code>mouse</code> でクリックするので、カーソルは動きます。",
    ),
    "ko": dict(
        cap="네 가지 방법 비교",
        cols=["방법", "단계당 비용", "정확도", "적용 범위", "상태 파악(누를 수 있는지, 현재 값)",
              "커서를 빼앗는지", "필요한 권한"],
        rows=[["1. 스크린샷 보고 좌표 짐작", "높음: 단계마다 이미지 한 장", "낮음: 좌표를 짐작",
               "가장 넓음: 보이면 됨", "✗ 모름", "✓ 빼앗음", "필요: 화면 기록과 입력 제어"],
              ["2. 번호 붙여 고르기(set-of-mark)", "높음: 이미지와 탐지 모델", "중간: 탐지 정확도에 달림",
               "넓음: 탐지되면 됨", "✗ 모름", "✓ 빼앗음", "필요: 화면 기록과 입력 제어"],
              ["3. 앱의 API나 스크립트", "낮음: 명령 하나", "높음", "좁음: 지원하는 앱만", "앱에 따라 다름",
               "✗ 빼앗지 않음", "경우에 따라(macOS: 자동화)"],
              ["4. 접근성 트리", "낮음: 텍스트 한 덩어리", "높음: 위치가 정확",
               "중간: 표준 UI. canvas나 게임은 비어 있을 때가 많음", "✓ 시스템이 알려 줌",
               "✗ ref로 조작하면 빼앗지 않음*", "필요: 손쉬운 사용"]],
        note="* ref로 조작하고 커서를 움직이지 않는 것은 <code>ui_action</code>이며, {pr96}에서 개발 "
             "중이고 아직 출시되지 않았습니다. 지금은 OpenAB Computer의 에이전트가 여전히 "
             "<code>mouse</code>로 클릭하므로 커서가 움직입니다.",
    ),
}
PR96 = "https://github.com/openabdev/openab-computer/pull/96"


def cmp_table(code):
    c = CMP[code]
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in c["cols"])
    body = []
    for row in c["rows"]:
        cells = "".join(f'<td data-label="{esc(h)}">{esc(v)}</td>'
                        for h, v in zip(c["cols"][1:], row[1:]))
        body.append(f'<tr><th scope="row">{esc(row[0])}</th>{cells}</tr>')
    note = c["note"].format(pr96=f'<a href="{PR96}">PR #96</a>')
    return (f'<div class="cmp-wrap"><table class="cmp"><caption>{esc(c["cap"])}</caption>'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
            f'<p class="cmp-note">{note}</p>')


FIGS = {"fig_loop": fig_loop, "fig_tree": fig_tree, "fig_action": fig_action,
        "fig_aim": fig_aim, "cmp_table": cmp_table}
