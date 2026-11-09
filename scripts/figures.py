"""Animated diagrams for the ui_snapshot dev note, four languages.

Each figure is inline SVG plus HTML, with every visible word taken from S[code], so nothing
is baked into an image. scripts/figs.js plays them step by step. Without JS, or with
prefers-reduced-motion, the figure shows its final, complete state:

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
        ctl=dict(play="Play", pause="Pause", resume="Resume", replay="Replay"),
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
        ctl=dict(play="播放", pause="暫停", resume="繼續", replay="重播"),
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
        ctl=dict(play="再生", pause="一時停止", resume="再開", replay="もう一度"),
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
        ctl=dict(play="재생", pause="일시 정지", resume="계속", replay="다시 보기"),
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
            f'data-play="{esc(c["play"])}" data-pause="{esc(c["pause"])}" '
            f'data-resume="{esc(c["resume"])}" data-replay="{esc(c["replay"])}">'
            f'{esc(c["replay"])}</button></div>')


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


FIGS = {"fig_loop": fig_loop, "fig_tree": fig_tree, "fig_action": fig_action}
