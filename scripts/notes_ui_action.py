"""Dev note 2: ui_action in OpenAB Computer 0.10.0, and how we tested it. Four languages.

Imported by notes.py, which puts it first in NOTES (newest first). Every fact here is recorded
with its source outside this repo (facts-devnote-2.md in the task's run dir). Figures come from
figures_ui_action.py ({fig_press}, {fig_stale}, {fig_sheet}, {fig_redact}).
"""

REL10 = "https://github.com/openabdev/openab-computer/releases/tag/v0.10.0"
PR96 = "https://github.com/openabdev/openab-computer/pull/96"
ISSUE98 = "https://github.com/openabdev/openab-computer/issues/98"
PR99 = "https://github.com/openabdev/openab-computer/pull/99"
ISSUE67 = "https://github.com/openabdev/openab-computer/issues/67"
ISSUE102 = "https://github.com/openabdev/openab-computer/issues/102"
SB022 = "https://github.com/openabdev/openab-sb/releases/tag/v0.2.2"
SB16 = "https://github.com/openabdev/openab-sb/pull/16"
SB14 = "https://github.com/openabdev/openab-sb/issues/14"
NOTE1 = "../accessibility-tree/"   # same language, sibling note


def a(href, label):
    return f'<a href="{href}">{label}</a>'


NOTE = dict(
    slug="ui-action",
    date="2026-11-10",
    og_art="ui-action",   # og_cards.ARTS
    text="",
    json="",
    langs={
        "en": dict(
            title="How we tested ui_action in OpenAB Computer 0.10.0",
            desc="Once an agent can read a window's accessibility tree, how does it press a button "
                 "without taking your mouse, and how do you prove it didn't? OpenAB Computer 0.10.0 "
                 "adds ui_action. Here is what it does and how we tested it.",
            og=(["ui_action in 0.10.0:", "press by ref, cursor stays."],
                "How we tested it, and what the tests caught"),
            og_alt="OpenAB dev note: how we tested ui_action in OpenAB Computer 0.10.0",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="hook">Once an agent can read a window's accessibility tree, how does it press a button
in that window without taking over your mouse? And after it presses, how do you prove it never
touched the mouse?</p>

<p class="lede">{a(REL10, "OpenAB Computer 0.10.0")} adds <code>ui_action</code>. The
<code>ui_snapshot</code> tool from the {a(NOTE1, "previous dev note")} reads a window;
<code>ui_action</code> acts on it. It takes a ref from a snapshot and presses a button or fills a
field through the accessibility API, and the cursor stays where it is. This note covers what it
does and how we tested it.</p>

<h2>What ui_action does</h2>
<p>The call is <code>ui_action {{snapshot_id, ref, action}}</code> ({a(PR96, "PR #96")}). The
actions are press, set_value, focus, show_menu, confirm and cancel, plus increment and decrement.
Each one maps to an accessibility action: press is AXPress on the element, set_value sets its
AXValue and replaces the whole value. If the element does not support the action, the tool refuses
before doing anything and lists the actions it does support.</p>
<p>The intended loop has three steps: <code>ui_snapshot</code>, then <code>ui_action</code> on one
of its refs, then another <code>ui_snapshot</code> to check the result.</p>
{{fig_press}}
<p>The tool never synthesizes input events and never moves the pointer; a test scans the source to
keep it that way. By default it does not bring the app to the front or raise a window either. When
that is needed, for example to open a menu in a background app, the caller passes
<code>activate: true</code>.</p>

<h3>A ref is only good in its own snapshot</h3>
<p>The tool keeps the last four snapshots, for five minutes each. Before acting it checks the ref
again: same process, same role and subrole, still under the window it was found in. For a menu
item, the menu bar must still answer. If any check fails, the answer is <code>stale ref: … take a
new ui_snapshot</code>. The tool never picks a lookalike element to stand in for the old one.</p>
{{fig_stale}}

<h3>Who can use it, and password fields</h3>
<p><code>ui_action</code> is available only to the <code>owner</code> profile, in the same class as
<code>mouse</code> and <code>key</code>, and it needs the macOS Accessibility permission. When it
sets a password field, the value is never read back, logged or returned. For every field, the input
value stays out of errors, log lines and response text. Through a switchboard, set_value on a
password field is refused by default, unless the operator of that computer turns it on.</p>

<h2>How we tested it</h2>

<h3>1. Unit tests with a fake accessibility provider</h3>
<p>CI machines have no GUI, so the tests do not touch real apps. <code>ui_snapshot</code> already
had a fake accessibility provider, and the <code>ui_action</code> tests run on it too. PR #96 added
52 tests in three suites: <code>UIActionToolTests</code> (40), <code>UISnapshotCacheTests</code>
(5) and <code>UIActivateTests</code> (7).</p>
<p>They cover: a snapshot that expired or was pushed out; an unknown ref; an element that vanished,
changed role, belongs to another process or left its window; an unsupported action, with the list
of supported ones; which accessibility call sits behind each action; a password value absent from
the response and from every log line; password fields refused by default through a switchboard;
<code>activate</code> false by default; and the profile rules.</p>
<p>On an M4 Mac mini, <code>swift test</code> ran 256 tests with 0 failures, and every CI check on
the PR passed.</p>
<p>We also tried a live run before merging, but that test build had no Accessibility permission, so
<code>ui_action</code> only returned the permission error and the TextEdit run did not happen. It
waited for the released build, which has the permission.</p>

<h3>2. A live run on an M4 Mac mini, through the switchboard</h3>
<p>After 0.10.0 was released, a remote agent drove an M4 Mac mini through the switchboard. Each
step was one MCP tool call, and the switchboard's audit log recorded the times:</p>
<ol>
<li>Read the mouse location (a short JXA script through <code>osascript</code>, reading
<code>NSEvent.mouseLocation</code>).</li>
<li>Open TextEdit with a new document.</li>
<li><code>ui_snapshot</code> of TextEdit, 96 ms. The text area is <code>[e3] AXTextArea</code>.</li>
<li><code>ui_action</code> focus on e3 (8 ms), then set_value with "hello from ui_action 0.10.0"
(15 ms).</li>
<li>Another snapshot to check: e3's value is "hello from ui_action 0.10.0".</li>
<li>Read the mouse location again.</li>
</ol>
<p>Both readings gave the same point, (284, 88). The text went in and the cursor did not move.</p>

<h3>3. What the live run caught: buttons inside a sheet</h3>
<p>Next we quit TextEdit. The unsaved document brought up a save sheet, the kind of dialog that
slides down from a window's title bar. <code>ui_action</code> press on the sheet's Delete button
failed:</p>
<pre><code>stale ref: e63 has left its window; take a new ui_snapshot and use its refs</code></pre>
<p>It failed the same way three times, with a fresh snapshot each time. A read-only Swift probe
showed why. Asked for its AXWindow, a control inside a sheet returns nil, not some other window.
The 0.10.0 check treated "no AXWindow" as something only menu items do, so it refused the ref. The
button's AXParent is the sheet, and it is the sheet whose AXWindow is the window.</p>
{{fig_sheet}}
<p>This became {a(ISSUE98, "issue #98")} (labels bug and p2), fixed by {a(PR99, "PR #99")}. When an
element has no AXWindow, or one that is not on the snapshot's recorded path, the check walks up
AXParent to the nearest window, sheet, drawer or popover, and accepts the ref only if that container
is on the recorded path. The walk stops after 50 steps, checks for cycles and runs under the same
time budget. A change of process or role is still refused first, and no replacement is guessed.</p>
<p>PR #99 added 8 tests, for 264 in total with 0 failures, and CI passed. Its live check was
read-only: applied to TextEdit's real save sheet, the new rule accepted all 15 controls in the
sheet, Delete included; the 0.10.0 rule accepted none of them. The fix is merged and ships in
0.10.1. Pressing a button inside a sheet is covered by the unit tests; we have not yet re-run that
press live through <code>ui_action</code>.</p>

<h3>4. Two reviewers, and a leak in the audit log</h3>
<p>Every change goes to two independent AI reviewers running different models. They review in
parallel, and the change merges only when both approve the same commit. PR #96 went through five
rounds and a confirming review.</p>
<p>The first round found a real problem. Through a switchboard, a password value sent with
set_value ended up in the switchboard's audit log. The switchboard (openab-sb) writes each tool
call's arguments to audit.jsonl before it forwards the call. So even when the Mac refused the call,
the log line was already written. Only openab-sb could fix that, so PR #96 waited until the fix was
merged and deployed.</p>
<p>The fix is {a(SB022, "openab-sb 0.2.2")} ({a(SB16, "PR #16")}, {a(SB14, "issue #14")}). It
redacts secret-bearing arguments in the audit line, at any depth in objects and arrays: the value
of <code>ui_action</code>, typed text, keys whose names contain words such as password, secret,
token or credential, and every value in env and headers. A string becomes
<code>&lt;redacted:N chars&gt;</code>; any other type becomes <code>&lt;redacted&gt;</code>. Only the
audit copy is redacted, and the computer still receives the real arguments. Free-form strings,
such as a shell command, a script or a URL's query string, are not inspected.</p>
{{fig_redact}}
<p>We checked it with a canary. Through the deployed switchboard we sent one <code>exec</code> call
with a fake token in its env, as API_TOKEN. In the audit file the canary appeared 0 times, and the
line for that call held <code>&lt;redacted:31 chars&gt;</code> where the token had been. The live
TextEdit set_value was logged as <code>"value":"&lt;redacted:27 chars&gt;"</code> too, and 27 is
the length of "hello from ui_action 0.10.0".</p>
<p>The 0.10.0 release notes also ask switchboard operators to upgrade to openab-sb 0.2.2 before
sending anything sensitive through <code>ui_action</code>, and to consider rotating audit files
written by older versions.</p>

<h2>Limits and next</h2>
<ul>
<li>set_value replaces the whole value. Some apps only commit it on confirm or when focus
moves.</li>
<li>A press that opens a sheet or a menu may get a late answer from the app. The result is then
reported as unconfirmed: it may have happened, so take a new snapshot instead of pressing
again.</li>
<li>Drags and multi-step gestures stay on <code>mouse</code>. Custom-drawn content with no
accessibility node stays on <code>screenshot</code> and <code>mouse</code>.</li>
<li>Linux: {a(ISSUE67, "issue #67")} is closed, because the macOS part is done. AT-SPI support for
<code>ui_snapshot</code> and <code>ui_action</code> on Linux is deferred as p3 in
{a(ISSUE102, "issue #102")}, to be picked up when a Linux machine needs it. Until then, use
<code>screenshot</code>, <code>mouse</code> and <code>key</code> on Linux.</li>
</ul>

<p class="outro">To try it, update to {a(REL10, "OpenAB Computer 0.10.0")}, give it the
Accessibility permission, and from an agent with the <code>owner</code> profile call
<code>ui_snapshot</code>, then <code>ui_action</code>, then <code>ui_snapshot</code> again. If you
use a switchboard, upgrade it to openab-sb 0.2.2 first. Previous note:
{a(NOTE1, "OpenAB Computer can now read the macOS accessibility tree")}.</p>
""",
        ),
        "zh": dict(
            title="我們怎麼測試 OpenAB Computer 0.10.0 的 ui_action",
            desc="Agent 讀得到視窗的 accessibility tree 之後，要怎麼不搶你的滑鼠就按下按鈕？又要怎麼"
                 "證明它沒碰滑鼠？OpenAB Computer 0.10.0 新增 ui_action，這篇記錄它做什麼，以及我們"
                 "怎麼測。",
            og=(["0.10.0 的 ui_action：", "用 ref 按下，游標不動。"],
                "我們怎麼測，以及測出了什麼"),
            og_alt="OpenAB 開發筆記：我們怎麼測試 OpenAB Computer 0.10.0 的 ui_action",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="hook">Agent 讀得到一個視窗的 accessibility tree 之後，要怎麼在不搶走你滑鼠的情況下，
按下視窗裡的按鈕？按完之後，又要怎麼證明它真的沒碰到滑鼠？</p>

<p class="lede">{a(REL10, "OpenAB Computer 0.10.0")} 新增了 <code>ui_action</code>。
{a(NOTE1, "上一篇開發筆記")}介紹的 <code>ui_snapshot</code> 負責讀畫面，<code>ui_action</code>
負責動手：拿快照裡的 ref，透過 accessibility API 按按鈕、填欄位，游標留在原地。這篇記錄它做了什麼，
以及我們怎麼測它。</p>

<h2>ui_action 做什麼</h2>
<p>呼叫方式是 <code>ui_action {{snapshot_id, ref, action}}</code>（{a(PR96, "PR #96")}）。動作有
press、set_value、focus、show_menu、confirm、cancel，以及 increment、decrement，每個動作都對應一個
accessibility 動作：press 是對元素執行 AXPress，set_value 是設定它的 AXValue，整個值換掉。元素不支援
這個動作時，工具在動手之前就拒絕，並列出它支援哪些動作。</p>
<p>建議的用法分三步：先 <code>ui_snapshot</code>，再對其中一個 ref 呼叫 <code>ui_action</code>，
最後再拍一次 <code>ui_snapshot</code> 確認結果。</p>
{{fig_press}}
<p>它從不合成輸入事件，也從不移動游標，原始碼裡有一個掃描測試盯著這一點。預設也不會把 app 叫到前景、
不會拉起視窗。真的需要時，例如要打開背景 app 的選單，呼叫端要明確傳 <code>activate: true</code>。</p>

<h3>ref 只在自己的快照裡有效</h3>
<p>工具會保留最近四次快照，每次五分鐘。動手之前，它會重新檢查這個 ref：還是同一個行程、角色和子角色
沒變、還在當初找到它的那個視窗底下；如果是選單項目，選單列要還在回應。任何一項不符，就回傳
<code>stale ref: … take a new ui_snapshot</code>。工具不會挑一個長得像的元素來頂替。</p>
{{fig_stale}}

<h3>誰能用，以及密碼欄位</h3>
<p><code>ui_action</code> 只開放給 <code>owner</code> profile，和 <code>mouse</code>、<code>key</code>
同一級，也需要 macOS 的「輔助使用」權限。對密碼欄位 set_value 時，值不會被讀回、不會寫進紀錄，也不會
出現在回應裡。對任何欄位，輸入的值都不會出現在錯誤訊息、紀錄或回應文字中。透過 switchboard 呼叫時，
對密碼欄位 set_value 預設會被拒絕，除非那台電腦的管理者自己開啟。</p>

<h2>我們怎麼測</h2>

<h3>1. 單元測試：用假的 accessibility 提供者</h3>
<p>CI 機器沒有圖形介面，所以測試不碰真的 app。<code>ui_snapshot</code> 原本就有一個假的
accessibility 提供者，<code>ui_action</code> 的測試也跑在它上面。PR #96 新增三組共 52 個測試：
<code>UIActionToolTests</code> 40 個、<code>UISnapshotCacheTests</code> 5 個、
<code>UIActivateTests</code> 7 個。</p>
<p>涵蓋的情況有：快照過期或被擠掉；ref 不存在；元素消失、角色改變、屬於別的行程，或離開了原本的視窗；
不支援的動作，要列出支援的動作；每個動作背後呼叫的是哪個 accessibility 動作；密碼的值不出現在回應和
任何一行紀錄裡；透過 switchboard 時密碼欄位預設拒絕；<code>activate</code> 預設是 false；以及 profile
的權限劃分。</p>
<p>在一台 M4 Mac mini 上，<code>swift test</code> 跑了 256 個測試，0 個失敗；PR 上的 CI 檢查全部
通過。</p>
<p>合併之前我們也試過實機測試，但那個測試版程式沒有「輔助使用」權限，<code>ui_action</code> 只回了沒有
權限的錯誤，TextEdit 那段沒跑成。這段留到發布後，用已經授權的版本來做。</p>

<h3>2. 實機測試：一台 M4 Mac mini，經過 switchboard</h3>
<p>0.10.0 發布之後，我們讓遠端的 agent 經過 switchboard 操作一台 M4 Mac mini。每一步都是一次 MCP
工具呼叫，switchboard 的稽核紀錄記下了時間：</p>
<ol>
<li>讀一次滑鼠位置（透過 <code>osascript</code> 跑一小段 JXA，讀 <code>NSEvent.mouseLocation</code>）。</li>
<li>打開 TextEdit，開一份新文件。</li>
<li>對 TextEdit 拍 <code>ui_snapshot</code>，花了 96 ms。文字區是 <code>[e3] AXTextArea</code>。</li>
<li>用 <code>ui_action</code> 對 e3 做 focus（8 ms），再 set_value 寫入 "hello from ui_action 0.10.0"
（15 ms）。</li>
<li>再拍一次快照確認：e3 的值是 "hello from ui_action 0.10.0"。</li>
<li>再讀一次滑鼠位置。</li>
</ol>
<p>兩次讀到的是同一個點：(284, 88)。文字寫進去了，游標沒有動。</p>

<h3>3. 實機測試抓到的問題：sheet 裡的按鈕</h3>
<p>接著我們結束 TextEdit。還沒儲存的文件跳出了儲存用的 sheet，也就是從視窗標題列往下滑出來的那種
對話框。對 sheet 上的「刪除」按鈕呼叫 <code>ui_action</code> press，失敗了：</p>
<pre><code>stale ref: e63 has left its window; take a new ui_snapshot and use its refs</code></pre>
<p>每次都重拍快照，連試三次都一樣。我們用一段唯讀的 Swift 探測程式查原因：sheet 裡的控制項被問到
AXWindow 時，回的是 nil，而不是別的視窗。0.10.0 的檢查以為只有選單項目才會沒有 AXWindow，所以拒絕了
這個 ref。按鈕的 AXParent 是 sheet，sheet 的 AXWindow 才是那個視窗。</p>
{{fig_sheet}}
<p>這件事開成了 {a(ISSUE98, "issue #98")}（標籤 bug、p2），由 {a(PR99, "PR #99")} 修正：元素沒有
AXWindow，或它的 AXWindow 不在快照記錄的路徑上時，檢查改成沿著 AXParent 往上找最近的視窗、sheet、
drawer 或 popover，而且只有這個容器在記錄的路徑上才接受。往上最多找 50 步，會檢查有沒有繞圈，也受同一個
時間預算限制。行程或角色改變還是會先被拒絕，也不會猜替代的元素。</p>
<p>PR #99 新增 8 個測試，總數 264 個，0 個失敗，CI 通過。它的實機檢查是唯讀的：把新規則套到 TextEdit
真的儲存 sheet 上，sheet 裡 15 個控制項全部通過，包括「刪除」；用 0.10.0 的規則則一個也不通過。修正
已經合併，會在 0.10.1 推出。在 sheet 裡真的按下按鈕這件事，目前由單元測試涵蓋，還沒有用
<code>ui_action</code> 在實機上重跑。</p>

<h3>4. 兩個審查者，以及稽核紀錄的外洩</h3>
<p>每一個變更都交給兩個獨立的 AI 審查者，用的是不同的模型。它們平行審查，兩邊都核准同一個 commit 才會
合併。PR #96 審了五輪，最後再加一次確認。</p>
<p>第一輪就抓到一個真的問題：透過 switchboard 對密碼欄位 set_value 時，那個值會寫進 switchboard 的
稽核紀錄。switchboard（openab-sb）在把工具呼叫轉給電腦之前，就先把參數寫進 audit.jsonl。所以就算
Mac 那端拒絕了這次呼叫，那一行紀錄也已經寫下去了。這只能在 openab-sb 修，PR #96 因此一直等到修正合併
並部署之後才合併。</p>
<p>修正是 {a(SB022, "openab-sb 0.2.2")}（{a(SB16, "PR #16")}、{a(SB14, "issue #14")}）。它在稽核
紀錄裡遮掉帶有祕密的參數，不管藏在多深的物件或陣列裡：<code>ui_action</code> 的 value、輸入的文字、
名稱裡有 password、secret、token、credential 這類字眼的鍵，以及 env 和 headers 裡的每一個值。字串
變成 <code>&lt;redacted:N chars&gt;</code>，其他型別變成 <code>&lt;redacted&gt;</code>。只有稽核
紀錄裡那一份被遮，電腦收到的仍是原本的參數。自由格式的字串，例如 shell 指令、腳本內容或網址的查詢
字串，不會被檢查。</p>
{{fig_redact}}
<p>我們用一個 canary 驗證：經過部署好的 switchboard 送出一次 <code>exec</code> 呼叫，在 env 的
API_TOKEN 放一個假的 token。這個 canary 在稽核檔案裡出現 0 次，那次呼叫的紀錄在 token 原本的位置寫的是
<code>&lt;redacted:31 chars&gt;</code>。後來實機測試 TextEdit 的 set_value，在紀錄裡也是
<code>"value":"&lt;redacted:27 chars&gt;"</code>，27 正好是 "hello from ui_action 0.10.0" 的長度。</p>
<p>0.10.0 的發布說明也提醒使用 switchboard 的人：透過 <code>ui_action</code> 傳任何敏感內容之前，先
升級到 openab-sb 0.2.2，並考慮輪替舊版本寫下的稽核檔案。</p>

<h2>限制與接下來</h2>
<ul>
<li>set_value 會把整個值換掉。有些 app 要等確認或焦點移開，才會真正套用。</li>
<li>會打開 sheet 或選單的 press，app 可能比較晚才回應。這時結果會標成 unconfirmed：動作可能已經發生，
請重拍快照確認，不要直接再按一次。</li>
<li>拖曳和多步驟手勢還是用 <code>mouse</code>。沒有 accessibility 節點、自己繪製的內容，還是用
<code>screenshot</code> 加 <code>mouse</code>。</li>
<li>Linux：{a(ISSUE67, "issue #67")} 已經關閉，因為 macOS 的部分做完了。Linux 上用 AT-SPI 實作
<code>ui_snapshot</code> 和 <code>ui_action</code> 先延後，列為 p3，記在 {a(ISSUE102, "issue #102")}，
等有 Linux 機器真的需要時再做。在那之前，Linux 上請用 <code>screenshot</code>、<code>mouse</code> 和
<code>key</code>。</li>
</ul>

<p class="outro">想試試看：更新到 {a(REL10, "OpenAB Computer 0.10.0")}，給它「輔助使用」權限，再從使用
<code>owner</code> profile 的 agent 依序呼叫 <code>ui_snapshot</code>、<code>ui_action</code>，最後再
<code>ui_snapshot</code> 一次。有用 switchboard 的話，先把它升級到 openab-sb 0.2.2。上一篇：
{a(NOTE1, "OpenAB Computer 開始支援 macOS 的 accessibility tree")}。</p>
""",
        ),
        "ja": dict(
            title="OpenAB Computer 0.10.0 の ui_action をどう試したか",
            desc="ウィンドウのアクセシビリティツリーを読めるようになったエージェントは、マウスを奪わずに"
                 "どうボタンを押すのか。そして触っていないことをどう証明するのか。OpenAB Computer 0.10.0 "
                 "で加わった ui_action と、その試し方の記録です。",
            og=(["0.10.0 の ui_action：", "ref で押し、カーソルはそのまま。"],
                "どう試したか、そこで何が見つかったか"),
            og_alt="OpenAB 開発ノート：OpenAB Computer 0.10.0 の ui_action をどう試したか",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="hook">ウィンドウのアクセシビリティツリーを読めるようになったエージェントは、あなたのマウスを
奪わずに、どうやってそのウィンドウのボタンを押すのでしょうか。押したあと、マウスに触れていないことを
どう証明すればいいのでしょうか。</p>

<p class="lede">{a(REL10, "OpenAB Computer 0.10.0")} で <code>ui_action</code> が加わりました。
{a(NOTE1, "前回の開発ノート")}で紹介した <code>ui_snapshot</code> は画面を読む道具で、
<code>ui_action</code> は操作する道具です。スナップショットの ref を受け取り、アクセシビリティ API で
ボタンを押したり入力欄を埋めたりし、カーソルはその場に残ります。このノートでは、何ができるのかと、
どう試したのかをまとめます。</p>

<h2>ui_action でできること</h2>
<p>呼び出しは <code>ui_action {{snapshot_id, ref, action}}</code> です（{a(PR96, "PR #96")}）。操作は
press、set_value、focus、show_menu、confirm、cancel と、increment、decrement です。どれもアクセシビリティの
アクションに対応していて、press は要素への AXPress、set_value は AXValue の設定で、値全体を置き換えます。
要素がその操作に対応していなければ、ツールは何もする前に拒否し、対応している操作の一覧を返します。</p>
<p>想定している流れは三段階です。<code>ui_snapshot</code>、その ref の一つに <code>ui_action</code>、
最後にもう一度 <code>ui_snapshot</code> で結果を確かめます。</p>
{{fig_press}}
<p>ツールは入力イベントを合成せず、ポインターも動かしません。ソースを走査するテストがこれを見張って
います。既定ではアプリを前面に出さず、ウィンドウも手前に出しません。バックグラウンドのアプリでメニューを
開くときなど、必要な場合は呼び出し側が <code>activate: true</code> を明示します。</p>

<h3>ref は自分のスナップショットの中でだけ有効</h3>
<p>ツールは直近四回のスナップショットを、それぞれ五分間保持します。操作の前に ref をもう一度確かめます。
同じプロセスか、ロールとサブロールが変わっていないか、見つけたときのウィンドウの下にまだあるか。
メニュー項目なら、メニューバーがまだ応答するか。どれか一つでも外れれば、答えは <code>stale ref: …
take a new ui_snapshot</code> です。似た要素を選んで代わりにすることはしません。</p>
{{fig_stale}}

<h3>使える人と、パスワード欄</h3>
<p><code>ui_action</code> を使えるのは <code>owner</code> プロファイルだけで、<code>mouse</code> や
<code>key</code> と同じ扱いです。macOS のアクセシビリティ権限も必要です。パスワード欄に set_value
するとき、値は読み戻されず、ログにも応答にも出ません。どの欄でも、入力した値はエラー、ログの行、応答の
テキストに出ません。スイッチボード経由では、パスワード欄への set_value は既定で拒否され、そのコンピューターの
管理者が有効にした場合だけ通ります。</p>

<h2>どう試したか</h2>

<h3>1. 偽のアクセシビリティ提供元を使った単体テスト</h3>
<p>CI のマシンには GUI がないので、テストは本物のアプリに触れません。<code>ui_snapshot</code> には
もともと偽のアクセシビリティ提供元があり、<code>ui_action</code> のテストもその上で動きます。PR #96 では
三つのスイートで 52 個のテストを加えました。<code>UIActionToolTests</code> が 40、
<code>UISnapshotCacheTests</code> が 5、<code>UIActivateTests</code> が 7 です。</p>
<p>扱っているのは次のようなケースです。期限切れや押し出されたスナップショット。存在しない ref。消えた
要素、ロールが変わった要素、別のプロセスの要素、元のウィンドウを離れた要素。対応していない操作と、
対応している操作の一覧。各操作の裏で呼ばれるアクセシビリティのアクション。応答にもログのどの行にも
パスワードの値が出ないこと。スイッチボード経由ではパスワード欄が既定で拒否されること。
<code>activate</code> の既定が false であること。プロファイルの権限の区分。</p>
<p>M4 Mac mini で <code>swift test</code> は 256 個のテストを実行し、失敗は 0 でした。PR の CI チェックも
すべて通りました。</p>
<p>マージの前に実機でも試しましたが、そのテスト用のビルドにはアクセシビリティ権限がなく、
<code>ui_action</code> は権限がないというエラーを返すだけで、TextEdit の手順は動きませんでした。この部分は
権限のあるリリース版を待ちました。</p>

<h3>2. M4 Mac mini での実機テスト（スイッチボード経由）</h3>
<p>0.10.0 のリリース後、リモートのエージェントからスイッチボード経由で M4 Mac mini を操作しました。
一手ごとに MCP ツールを一回呼び、スイッチボードの監査ログに時刻が残っています。</p>
<ol>
<li>マウス位置を読む（<code>osascript</code> で短い JXA を動かし、<code>NSEvent.mouseLocation</code>
を読む）。</li>
<li>TextEdit を開き、新しい書類を作る。</li>
<li>TextEdit の <code>ui_snapshot</code>、96 ms。テキスト領域は <code>[e3] AXTextArea</code>。</li>
<li><code>ui_action</code> で e3 に focus（8 ms）、続けて set_value で "hello from ui_action 0.10.0" を
入れる（15 ms）。</li>
<li>もう一度スナップショットを撮って確かめる。e3 の値は "hello from ui_action 0.10.0"。</li>
<li>もう一度マウス位置を読む。</li>
</ol>
<p>二回の読み取りは同じ点、(284, 88) でした。文字は入り、カーソルは動いていません。</p>

<h3>3. 実機テストで見つかったこと：シートの中のボタン</h3>
<p>続けて TextEdit を終了すると、保存していない書類のために保存用のシートが出ました。ウィンドウの
タイトルバーから下りてくる種類のダイアログです。シートの「削除」ボタンに <code>ui_action</code> の
press を送ると、失敗しました。</p>
<pre><code>stale ref: e63 has left its window; take a new ui_snapshot and use its refs</code></pre>
<p>毎回スナップショットを撮り直して三回試し、三回とも同じでした。読み取り専用の Swift のプローブで原因を
調べました。シートの中のコントロールに AXWindow を尋ねると、別のウィンドウではなく nil が返ります。
0.10.0 のチェックは「AXWindow がない」のはメニュー項目だけだと考えていたので、この ref を拒否しました。
ボタンの AXParent はシートで、AXWindow がそのウィンドウなのはシートのほうです。</p>
{{fig_sheet}}
<p>これは {a(ISSUE98, "issue #98")}（ラベルは bug と p2）になり、{a(PR99, "PR #99")} で直しました。
要素に AXWindow がない場合や、それがスナップショットに記録された経路にない場合、チェックは AXParent を
たどって最も近いウィンドウ、シート、ドロワー、ポップオーバーを探し、その入れ物が記録された経路にある
ときだけ受け付けます。たどるのは最大 50 段で、循環を確かめ、同じ時間の予算の中で動きます。プロセスや
ロールの変化は今までどおり先に拒否され、代わりの要素を推測することもありません。</p>
<p>PR #99 ではテストを 8 個加えて合計 264 個、失敗は 0 で、CI も通りました。実機での確認は読み取り専用
でした。TextEdit の本物の保存シートに新しい規則を当てると、「削除」を含むシート内の 15 個のコントロールが
すべて通り、0.10.0 の規則では一つも通りませんでした。修正はマージ済みで、0.10.1 で出ます。シートの中で
実際にボタンを押す動作は単体テストで確かめていて、<code>ui_action</code> による実機での押し直しはまだ
していません。</p>

<h3>4. 二人のレビュアーと、監査ログからの漏れ</h3>
<p>すべての変更は、別々のモデルで動く二つの独立した AI レビュアーに渡します。二つは並行してレビューし、
両方が同じコミットを承認したときだけマージします。PR #96 は五回のレビューと、最後の確認を経ました。</p>
<p>最初の回で本当の問題が見つかりました。スイッチボード経由でパスワード欄に set_value すると、その値が
スイッチボードの監査ログに残っていたのです。スイッチボード（openab-sb）は、ツールの呼び出しを
コンピューターへ転送する前に、引数を audit.jsonl に書きます。そのため Mac 側が呼び出しを拒否しても、
ログの行はもう書かれていました。直せるのは openab-sb だけなので、PR #96 は修正がマージされ、
デプロイされるまでマージを待ちました。</p>
<p>修正は {a(SB022, "openab-sb 0.2.2")}（{a(SB16, "PR #16")}、{a(SB14, "issue #14")}）です。監査ログの
行で、秘密を含む引数を、オブジェクトや配列のどの深さにあっても伏せます。対象は <code>ui_action</code> の
value、入力したテキスト、password、secret、token、credential のような語を名前に含むキー、そして env と
headers のすべての値です。文字列は <code>&lt;redacted:N chars&gt;</code> に、それ以外の型は
<code>&lt;redacted&gt;</code> になります。伏せるのは監査用の写しだけで、コンピューターには本当の引数が
届きます。シェルのコマンド、スクリプト、URL のクエリ文字列のような自由形式の文字列は調べません。</p>
{{fig_redact}}
<p>canary で確かめました。デプロイ済みのスイッチボードを通して <code>exec</code> を一回呼び、env の
API_TOKEN に偽のトークンを入れました。監査ファイルに canary は一度も出ず（0 回）、その呼び出しの行ではトークンの
位置に <code>&lt;redacted:31 chars&gt;</code> がありました。実機テストでの TextEdit の set_value も
<code>"value":"&lt;redacted:27 chars&gt;"</code> と記録され、27 は "hello from ui_action 0.10.0" の
長さと同じです。</p>
<p>0.10.0 のリリースノートでも、スイッチボードを運用する人に、<code>ui_action</code> で機密を送る前に
openab-sb 0.2.2 へ上げること、古い版が書いた監査ファイルの入れ替えを検討することを勧めています。</p>

<h2>制限と、これから</h2>
<ul>
<li>set_value は値全体を置き換えます。確定するかフォーカスが移るまで反映しないアプリもあります。</li>
<li>シートやメニューを開く press には、アプリの返事が遅れることがあります。そのときの結果は unconfirmed
と報告されます。操作は起きたかもしれないので、もう一度押さず、スナップショットを撮り直してください。</li>
<li>ドラッグや複数段のジェスチャーは今も <code>mouse</code> を使います。アクセシビリティのノードがない
独自描画の内容は、今も <code>screenshot</code> と <code>mouse</code> です。</li>
<li>Linux：macOS の部分が終わったので {a(ISSUE67, "issue #67")} は閉じました。Linux で AT-SPI を使って
<code>ui_snapshot</code> と <code>ui_action</code> を動かす作業は、p3 として {a(ISSUE102, "issue #102")}
で後回しにしていて、Linux のマシンで必要になったら取りかかります。それまで Linux では
<code>screenshot</code>、<code>mouse</code>、<code>key</code> を使ってください。</li>
</ul>

<p class="outro">試すには、{a(REL10, "OpenAB Computer 0.10.0")} に更新してアクセシビリティ権限を与え、
<code>owner</code> プロファイルのエージェントから <code>ui_snapshot</code>、<code>ui_action</code>、
もう一度 <code>ui_snapshot</code> の順に呼んでください。スイッチボードを使っているなら、先に
openab-sb 0.2.2 に上げてください。前回のノート：
{a(NOTE1, "OpenAB Computer が macOS のアクセシビリティツリーを読めるようになりました")}。</p>
""",
        ),
        "ko": dict(
            title="OpenAB Computer 0.10.0의 ui_action을 어떻게 시험했나",
            desc="창의 접근성 트리를 읽을 수 있게 된 에이전트는 마우스를 빼앗지 않고 어떻게 버튼을 "
                 "누를까요? 그리고 마우스를 건드리지 않았다는 것은 어떻게 증명할까요? OpenAB Computer "
                 "0.10.0에 추가된 ui_action과 그 시험 과정을 정리했습니다.",
            og=(["0.10.0의 ui_action:", "ref로 누르고 커서는 그대로."],
                "어떻게 시험했고, 무엇을 찾았는지"),
            og_alt="OpenAB 개발 노트: OpenAB Computer 0.10.0의 ui_action을 어떻게 시험했나",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="hook">창의 접근성 트리를 읽을 수 있게 된 에이전트는 여러분의 마우스를 빼앗지 않고 그 창의
버튼을 어떻게 누를까요? 누른 뒤에는 마우스를 건드리지 않았다는 것을 어떻게 증명할까요?</p>

<p class="lede">{a(REL10, "OpenAB Computer 0.10.0")}에 <code>ui_action</code>이 추가됐습니다.
{a(NOTE1, "지난 개발 노트")}에서 소개한 <code>ui_snapshot</code>이 화면을 읽는다면,
<code>ui_action</code>은 조작합니다. 스냅샷의 ref를 받아 접근성 API로 버튼을 누르거나 입력란을 채우고,
커서는 제자리에 둡니다. 이 노트에서는 무엇을 하는지, 그리고 어떻게 시험했는지를 다룹니다.</p>

<h2>ui_action이 하는 일</h2>
<p>호출 형태는 <code>ui_action {{snapshot_id, ref, action}}</code>입니다({a(PR96, "PR #96")}). 동작은
press, set_value, focus, show_menu, confirm, cancel과 increment, decrement입니다. 각 동작은 접근성
액션 하나에 대응합니다. press는 요소에 AXPress를, set_value는 AXValue 설정이며 값 전체를 바꿉니다.
요소가 그 동작을 지원하지 않으면 도구는 아무것도 하기 전에 거부하고, 지원하는 동작 목록을 알려 줍니다.</p>
<p>권장하는 흐름은 세 단계입니다. <code>ui_snapshot</code>, 그 ref 중 하나에 <code>ui_action</code>,
마지막으로 다시 <code>ui_snapshot</code>을 찍어 결과를 확인합니다.</p>
{{fig_press}}
<p>도구는 입력 이벤트를 합성하지 않고 포인터도 움직이지 않습니다. 소스 코드를 훑는 테스트가 이를 지킵니다.
기본적으로 앱을 앞으로 가져오지도, 창을 올리지도 않습니다. 백그라운드 앱의 메뉴를 열 때처럼 꼭 필요하면
호출하는 쪽이 <code>activate: true</code>를 명시합니다.</p>

<h3>ref는 자기 스냅샷 안에서만 유효합니다</h3>
<p>도구는 최근 스냅샷 네 개를 각각 5분 동안 보관합니다. 동작하기 전에 ref를 다시 확인합니다. 같은
프로세스인지, 역할과 하위 역할이 그대로인지, 처음 찾은 창 아래에 아직 있는지. 메뉴 항목이라면 메뉴 막대가
아직 응답하는지. 하나라도 어긋나면 답은 <code>stale ref: … take a new ui_snapshot</code>입니다. 비슷해
보이는 요소를 골라 대신 누르지 않습니다.</p>
{{fig_stale}}

<h3>누가 쓸 수 있는지, 그리고 비밀번호 입력란</h3>
<p><code>ui_action</code>은 <code>owner</code> 프로필에서만 쓸 수 있고, <code>mouse</code>,
<code>key</code>와 같은 등급입니다. macOS 손쉬운 사용 권한도 필요합니다. 비밀번호 입력란에 set_value를
할 때 값은 다시 읽히지 않고, 로그에도 응답에도 남지 않습니다. 어떤 입력란이든 입력한 값은 오류, 로그 줄,
응답 텍스트에 나오지 않습니다. 스위치보드를 거칠 때는 비밀번호 입력란에 대한 set_value가 기본적으로
거부되며, 그 컴퓨터의 관리자가 직접 켠 경우에만 허용됩니다.</p>

<h2>어떻게 시험했나</h2>

<h3>1. 가짜 접근성 공급자를 쓴 단위 테스트</h3>
<p>CI 기기에는 GUI가 없으므로 테스트는 실제 앱을 건드리지 않습니다. <code>ui_snapshot</code>에는 원래
가짜 접근성 공급자가 있었고, <code>ui_action</code>의 테스트도 그 위에서 돕니다. PR #96은 세 묶음에
테스트 52개를 추가했습니다. <code>UIActionToolTests</code> 40개, <code>UISnapshotCacheTests</code>
5개, <code>UIActivateTests</code> 7개입니다.</p>
<p>다루는 경우는 다음과 같습니다. 만료됐거나 밀려난 스냅샷. 없는 ref. 사라졌거나, 역할이 바뀌었거나,
다른 프로세스에 속하거나, 원래 창을 떠난 요소. 지원하지 않는 동작과 지원하는 동작 목록. 동작마다 뒤에서
호출되는 접근성 액션. 비밀번호 값이 응답과 모든 로그 줄에 없을 것. 스위치보드를 거치면 비밀번호 입력란이
기본적으로 거부될 것. <code>activate</code>의 기본값이 false일 것. 프로필 권한 구분.</p>
<p>M4 Mac mini에서 <code>swift test</code>는 테스트 256개를 실행했고 실패는 0개였습니다. PR의 CI 검사도
모두 통과했습니다.</p>
<p>병합 전에 실기기에서도 시도했지만, 그 테스트용 빌드에는 손쉬운 사용 권한이 없어서 <code>ui_action</code>은
권한 오류만 돌려줬고 TextEdit 단계는 돌지 못했습니다. 이 부분은 권한이 있는 릴리스 빌드를 기다렸습니다.</p>

<h3>2. M4 Mac mini 실기기 시험, 스위치보드 경유</h3>
<p>0.10.0 릴리스 뒤, 원격 에이전트가 스위치보드를 거쳐 M4 Mac mini를 조작했습니다. 한 단계가 MCP 도구
호출 한 번이고, 스위치보드의 감사 로그에 시각이 남았습니다.</p>
<ol>
<li>마우스 위치 읽기(<code>osascript</code>로 짧은 JXA를 실행해 <code>NSEvent.mouseLocation</code>을
읽음).</li>
<li>TextEdit을 열고 새 문서 만들기.</li>
<li>TextEdit의 <code>ui_snapshot</code>, 96 ms. 텍스트 영역은 <code>[e3] AXTextArea</code>.</li>
<li><code>ui_action</code>으로 e3에 focus(8 ms), 이어서 set_value로 "hello from ui_action 0.10.0" 입력
(15 ms).</li>
<li>스냅샷을 다시 찍어 확인: e3의 값은 "hello from ui_action 0.10.0".</li>
<li>마우스 위치 다시 읽기.</li>
</ol>
<p>두 번 읽은 값은 같은 점, (284, 88)이었습니다. 글자는 들어갔고 커서는 움직이지 않았습니다.</p>

<h3>3. 실기기 시험이 잡아낸 것: 시트 안의 버튼</h3>
<p>이어서 TextEdit을 종료하자, 저장하지 않은 문서 때문에 저장 시트가 떴습니다. 창의 제목 막대에서 아래로
내려오는 종류의 대화상자입니다. 시트의 "삭제" 버튼에 <code>ui_action</code> press를 보내자 실패했습니다.</p>
<pre><code>stale ref: e63 has left its window; take a new ui_snapshot and use its refs</code></pre>
<p>매번 스냅샷을 새로 찍어 세 번 시도했고 세 번 모두 같았습니다. 읽기 전용 Swift 프로브로 원인을
찾았습니다. 시트 안의 컨트롤에 AXWindow를 물으면 다른 창이 아니라 nil이 돌아옵니다. 0.10.0의 검사는
AXWindow가 없는 것은 메뉴 항목뿐이라고 보고 이 ref를 거부했습니다. 버튼의 AXParent는 시트이고, AXWindow가
그 창인 쪽은 시트입니다.</p>
{{fig_sheet}}
<p>이것은 {a(ISSUE98, "issue #98")}(라벨 bug, p2)이 됐고 {a(PR99, "PR #99")}에서 고쳤습니다. 요소에
AXWindow가 없거나 그것이 스냅샷에 기록된 경로에 없으면, 검사는 AXParent를 따라 가장 가까운 창, 시트,
드로어, 팝오버를 찾고, 그 컨테이너가 기록된 경로에 있을 때만 받아들입니다. 최대 50단계까지 올라가고, 순환을
검사하며, 같은 시간 예산 안에서 돕니다. 프로세스나 역할이 바뀐 경우는 여전히 먼저 거부되고, 대신할 요소를
짐작하지도 않습니다.</p>
<p>PR #99는 테스트 8개를 추가해 모두 264개, 실패 0개였고 CI도 통과했습니다. 실기기 확인은 읽기 전용이었습니다.
TextEdit의 실제 저장 시트에 새 규칙을 적용하자 "삭제"를 포함한 시트 안 컨트롤 15개가 모두 통과했고,
0.10.0의 규칙으로는 하나도 통과하지 못했습니다. 수정은 병합됐고 0.10.1에 실립니다. 시트 안에서 실제로
버튼을 누르는 동작은 단위 테스트로 확인했으며, <code>ui_action</code>으로 실기기에서 다시 눌러 보는 일은
아직 하지 않았습니다.</p>

<h3>4. 두 리뷰어, 그리고 감사 로그로 샌 값</h3>
<p>모든 변경은 서로 다른 모델로 도는 독립적인 AI 리뷰어 두 명에게 갑니다. 둘은 동시에 리뷰하고, 둘 다 같은
커밋을 승인해야 병합합니다. PR #96은 다섯 차례 리뷰와 마지막 확인을 거쳤습니다.</p>
<p>첫 차례에서 실제 문제가 나왔습니다. 스위치보드를 거쳐 비밀번호 입력란에 set_value를 하면 그 값이
스위치보드의 감사 로그에 남았습니다. 스위치보드(openab-sb)는 도구 호출을 컴퓨터로 전달하기 전에 인자를
audit.jsonl에 씁니다. 그래서 Mac 쪽이 호출을 거부해도 로그 줄은 이미 쓰인 뒤였습니다. 고칠 수 있는 곳은
openab-sb뿐이라, PR #96은 수정이 병합되고 배포될 때까지 병합을 미뤘습니다.</p>
<p>수정은 {a(SB022, "openab-sb 0.2.2")}({a(SB16, "PR #16")}, {a(SB14, "issue #14")})입니다. 감사 로그 줄에서
비밀을 담은 인자를 객체나 배열의 어느 깊이에 있든 가립니다. 대상은 <code>ui_action</code>의 value, 입력한
텍스트, password, secret, token, credential 같은 말이 이름에 들어간 키, 그리고 env와 headers의 모든
값입니다. 문자열은 <code>&lt;redacted:N chars&gt;</code>로, 다른 타입은 <code>&lt;redacted&gt;</code>로
바뀝니다. 가리는 것은 감사용 사본뿐이고 컴퓨터는 진짜 인자를 받습니다. 셸 명령, 스크립트, URL의 쿼리
문자열 같은 자유 형식 문자열은 검사하지 않습니다.</p>
{{fig_redact}}
<p>canary로 확인했습니다. 배포된 스위치보드를 거쳐 <code>exec</code>를 한 번 호출하면서 env의 API_TOKEN에
가짜 토큰을 넣었습니다. 감사 파일에 canary는 0번 나왔고, 그 호출의 줄에는 토큰 자리에
<code>&lt;redacted:31 chars&gt;</code>가 있었습니다. 실기기 시험의 TextEdit set_value도
<code>"value":"&lt;redacted:27 chars&gt;"</code>로 기록됐는데, 27은 "hello from ui_action 0.10.0"의
길이입니다.</p>
<p>0.10.0 릴리스 노트도 스위치보드 운영자에게, <code>ui_action</code>으로 민감한 내용을 보내기 전에
openab-sb 0.2.2로 올리고 이전 버전이 쓴 감사 파일의 교체를 검토하라고 권합니다.</p>

<h2>한계와 다음 단계</h2>
<ul>
<li>set_value는 값 전체를 바꿉니다. 확인하거나 포커스가 옮겨 가야 반영하는 앱도 있습니다.</li>
<li>시트나 메뉴를 여는 press는 앱의 응답이 늦을 수 있습니다. 그러면 결과는 unconfirmed로 보고됩니다.
동작이 이미 일어났을 수 있으니 다시 누르지 말고 스냅샷을 새로 찍어 확인하세요.</li>
<li>드래그와 여러 단계의 제스처는 여전히 <code>mouse</code>를 씁니다. 접근성 노드가 없는 직접 그린
내용은 여전히 <code>screenshot</code>과 <code>mouse</code>입니다.</li>
<li>Linux: macOS 부분이 끝나서 {a(ISSUE67, "issue #67")}은 닫혔습니다. Linux에서 AT-SPI로
<code>ui_snapshot</code>과 <code>ui_action</code>을 지원하는 일은 p3로 {a(ISSUE102, "issue #102")}에
미뤄 두었고, Linux 기기에서 필요해지면 시작합니다. 그때까지 Linux에서는 <code>screenshot</code>,
<code>mouse</code>, <code>key</code>를 쓰세요.</li>
</ul>

<p class="outro">써 보려면 {a(REL10, "OpenAB Computer 0.10.0")}으로 업데이트하고 손쉬운 사용 권한을 준 뒤,
<code>owner</code> 프로필의 에이전트에서 <code>ui_snapshot</code>, <code>ui_action</code>, 다시
<code>ui_snapshot</code> 순서로 호출하세요. 스위치보드를 쓴다면 먼저 openab-sb 0.2.2로 올리세요. 지난
노트: {a(NOTE1, "OpenAB Computer가 이제 macOS 접근성 트리를 읽습니다")}.</p>
""",
        ),
    },
)
