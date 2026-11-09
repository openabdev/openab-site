"""Dev notes for openab.dev: strings and bodies, four languages per note.

build.py renders each note to notes/<slug>/ (en), zh/notes/<slug>/, ja/notes/<slug>/ and
ko/notes/<slug>/, plus one index per language. og_cards.py draws one card per note and
language from the `og` entries (and from INDEX["og"] for the index pages).

Bodies are authored HTML. `{text}` and `{json}` in a body are replaced with the note's
escaped code samples, which are the same in every language. NOTES is newest first.
"""

INDEX = {
    "en": dict(
        nav="Dev notes",
        title="Dev notes — OpenAB",
        h1="Dev notes",
        desc="Notes from building OpenAB: what we changed, why, and what we learned on the way.",
        og=(["Dev notes", "from building OpenAB."], "What we changed, why, and what we learned"),
        og_alt="OpenAB dev notes",
        back="← OpenAB",
        read="Read the note",
    ),
    "zh": dict(
        nav="開發筆記",
        title="開發筆記 — OpenAB",
        h1="開發筆記",
        desc="打造 OpenAB 的過程紀錄：我們改了什麼、為什麼改，以及一路上學到的事。",
        og=(["OpenAB", "開發筆記。"], "我們改了什麼、為什麼改，以及學到的事"),
        og_alt="OpenAB 開發筆記",
        back="← OpenAB",
        read="閱讀筆記",
    ),
    "ja": dict(
        nav="開発ノート",
        title="開発ノート — OpenAB",
        h1="開発ノート",
        desc="OpenAB をつくる過程の記録です。何を変えたか、なぜ変えたか、そこで何を学んだか。",
        og=(["OpenAB の", "開発ノート。"], "何を変えたか、なぜ変えたか、何を学んだか"),
        og_alt="OpenAB 開発ノート",
        back="← OpenAB",
        read="ノートを読む",
    ),
    "ko": dict(
        nav="개발 노트",
        title="개발 노트 — OpenAB",
        h1="개발 노트",
        desc="OpenAB를 만들며 남기는 기록입니다. 무엇을 바꿨는지, 왜 바꿨는지, 그 과정에서 무엇을 배웠는지.",
        og=(["OpenAB", "개발 노트."], "무엇을 바꿨고, 왜 바꿨고, 무엇을 배웠는지"),
        og_alt="OpenAB 개발 노트",
        back="← OpenAB",
        read="노트 읽기",
    ),
}

# Links used by the first note.
REL = "https://github.com/openabdev/openab-computer/releases/tag/v0.9.0"
PR93 = "https://github.com/openabdev/openab-computer/pull/93"
ISSUE67 = "https://github.com/openabdev/openab-computer/issues/67"
TTMUSE = "https://github.com/openabdev/openab-computer/issues/67#issuecomment-6726398810"
AGENT_DESKTOP = "https://github.com/vercel-labs/agent-desktop"
MUSE = ("https://muse.ai/s/opencode-browse-vs-openab-computer-lxc6yxwxmxpk7iz/"
        "7lEkIj9rBZ_cbTI4KbMuF5EQQySq8Himvw-fgz8ELfg")
BROWSE = "https://github.com/anomalyco/browse"

# A real Finder snapshot taken on an M4 Mac mini with OpenAB Computer 0.9.0, called with
# app "Finder" and max_nodes 40. Changed from the tool's text output: the two drive names are
# replaced with "Data" and "Backup" and the pid is left out. Only the text output of that call
# was kept, so the JSON below is the same snapshot written with the tool's JSON field names
# (UITree.swift), as an excerpt: e4, limits, displays and fields the text form does not show
# are left out.
UI_TEXT = """ui_snapshot snap-10661573 · Finder (com.apple.finder) · 4 nodes · 104 ms
[e1] AXScrollArea desc="desktop" (0,0 1920×1080) focused
  [e2] AXGroup desc="desktop" (0,0 1920×1080) focused
    [e3] AXImage "Data" (1823,145 64×64)
    [e4] AXImage "Backup" (1823,33 64×64)"""

UI_JSON = """{
  "snapshot_id": "snap-10661573",
  "app": { "name": "Finder", "bundle_id": "com.apple.finder" },
  "node_count": 4,
  "truncated": false,
  "timed_out": false,
  "elapsed_ms": 104,
  "windows": [
    { "ref": "e1", "role": "AXScrollArea", "description": "desktop",
      "focused": true,
      "frame": { "x": 0, "y": 0, "width": 1920, "height": 1080 },
      "children": [
        { "ref": "e2", "role": "AXGroup", "description": "desktop",
          "focused": true,
          "frame": { "x": 0, "y": 0, "width": 1920, "height": 1080 },
          "children": [
            { "ref": "e3", "role": "AXImage", "title": "Data",
              "frame": { "x": 1823, "y": 145, "width": 64, "height": 64 } }
          ] }
      ] }
  ]
}"""


def a(href, label):
    return f'<a href="{href}">{label}</a>'


NOTES = [
    dict(
        slug="accessibility-tree",
        date="2026-11-09",
        text=UI_TEXT,
        json=UI_JSON,
        langs={
            "en": dict(
                title="OpenAB Computer can now read the macOS accessibility tree",
                desc="OpenAB Computer 0.9.0 adds ui_snapshot, an MCP tool that returns a Mac app's "
                     "accessibility tree as JSON. What it returns, what we learned from Vercel's "
                     "Agent Desktop, and what is still missing.",
                og=(["OpenAB Computer can now read", "the macOS accessibility tree."],
                    "ui_snapshot in 0.9.0: a Mac app's UI as JSON, not pixels"),
                og_alt="OpenAB dev note: OpenAB Computer can now read the macOS accessibility tree",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="lede">OpenAB Computer 0.9.0 adds <code>ui_snapshot</code>, an MCP tool that reads the
accessibility tree of a Mac app and returns it as JSON. An agent can now see the buttons, fields
and labels in a window as text, with their positions on screen, instead of working them out from
a screenshot.</p>

<h2>Why the screenshot loop was not enough</h2>
<p>Until now, an agent using OpenAB Computer on a Mac worked in a loop: take a screenshot, guess
where a button is, click it with <code>mouse</code>, then take another screenshot to check.</p>
<p>A community user, {a(TTMUSE, "ttmuse")}, described the cost of that loop on
{a(ISSUE67, "issue #67")}. They use OpenAB Computer every day as the hands of a cloud agent that
drives a home Mac. Every step costs image tokens, small targets get missed, and the real cursor is
taken over while the agent works.</p>
<p>The issue had been waiting for a real user. The comment showed there was one, so we raised its
priority and started with macOS.</p>

<h2>What we learned from Agent Desktop</h2>
<p>Before writing code we read Vercel Labs' {a(AGENT_DESKTOP, "Agent Desktop")} closely: its
README, its concept docs and its macOS code. Agent Desktop reads the accessibility tree of a
desktop app and returns it as JSON, with a ref for every element an agent can act on. Three of its
ideas shaped our plan: the first two are in <code>ui_snapshot</code> today, and the third waits for
phase 2.</p>
<ul>
<li><strong>Structured text instead of images.</strong> The model reads roles, names and values.
It does not have to find a button in pixels.</li>
<li><strong>A ref per element, from one snapshot.</strong> Agent Desktop's refs belong to the
snapshot that produced them. When the UI changes, a stale or ambiguous ref is rejected instead of
guessed, and the agent takes a new snapshot.</li>
<li><strong>Acting without the pointer (phase 2).</strong> Agent Desktop's ref actions go through the
accessibility API without moving the pointer or taking focus.</li>
</ul>
<p>Issue #67 listed calling Agent Desktop from OpenAB Computer as one option, and weighed less code
to own against an external dependency and its release cadence. We decided to make the
accessibility tree one of OpenAB Computer's own MCP tools, in the Swift daemon that already serves
<code>screenshot</code>, <code>mouse</code> and <code>key</code> ({a(PR93, "PR #93")}).</p>

<h2>What ui_snapshot returns</h2>
<p>By default it reads the focused window of the frontmost app. <code>app</code> (a bundle id or
name), <code>pid</code>, <code>window</code> and <code>all_windows</code> pick another target.</p>
<p>Each node carries its role, title, value and description, whether it is enabled or focused, and
a frame. The frame uses the same display points as <code>screenshot</code> and <code>mouse</code>,
so an agent can aim a click at a node without looking at the screen first. Every node also gets a
ref (<code>e1</code>, <code>e2</code>, …) that is unique within that snapshot's id.</p>
<p>Here is a real snapshot of Finder on an M4 Mac mini, taken with no Finder window open. The
window is the desktop itself, and the two images in it are the icons of two mounted drives. The
tool returns a text form for the model:</p>
<pre><code>{{text}}</code></pre>
<p>and the same tree as JSON (an excerpt; some fields are left out):</p>
<pre><code>{{json}}</code></pre>
<p>Four nodes, read in 104 ms. The drive names are replaced with generic ones here. To open the
“Data” drive, an agent can double-click the center of e3's frame, (1855, 177), without taking a
screenshot to find it.</p>

<h2>Limits, timeouts and privacy</h2>
<p>A snapshot is bounded. By default it stops at 20 levels deep or 300 nodes, and the whole call
gets 3 seconds; a caller can raise these to 50 levels, 2,000 nodes and 10 seconds. Before every
accessibility call the tool sets a messaging timeout of at most half a second, so an app that has
stopped responding cannot block it.</p>
<p>When a limit or the time budget runs out, the agent gets what was read so far, flagged with
<code>truncated</code> or <code>timed_out</code>, and no error. Long text is read as a
200-character prefix, so a large document is not copied whole.</p>
<p>Password fields are always masked. For a secure text field the tool never asks for the value
and does not look inside it. Other fields are not masked.</p>
<p>That matters because the tree holds text a screenshot does not show: rows scrolled out of view,
collapsed content, other windows. So <code>ui_snapshot</code> is available only to the
<code>owner</code> profile, and it needs the macOS Accessibility permission, the same one
<code>mouse</code> and <code>key</code> already use.</p>

<h2>Which tool for which screen</h2>
<ul>
<li>Native Mac apps: <code>ui_snapshot</code>.</li>
<li>Web pages: <code>browser_snapshot</code>, which reads the page structure from the browser.</li>
<li>Custom-drawn content such as canvases, which has no accessibility tree:
<code>screenshot</code> and <code>mouse</code>, as before.</li>
</ul>

<h2>Where we match Agent Desktop, and where we don't yet</h2>
<p>The same: both read the macOS accessibility API and return JSON, not images. Both give elements
refs that are valid only within one snapshot. Ours label every node; Agent Desktop's label the
elements an agent can act on. Both return a partial tree instead of failing.
Neither has a model inside; the calling agent runs the loop.</p>
<p>Different, today:</p>
<ul>
<li><strong>OpenAB Computer only reads.</strong> Agent Desktop can already click, type, set values
and move focus by ref without moving the pointer. An agent on OpenAB Computer still clicks with
<code>mouse</code> at coordinates, and the real cursor still moves.</li>
<li><strong>Refs.</strong> Our refs only label one snapshot; the tool keeps no state. Agent Desktop
stores a map from each ref to evidence of the element's identity, and checks it is the same
element before acting.</li>
<li><strong>Platforms.</strong> OpenAB Computer reads the tree on macOS only. Agent Desktop covers
macOS, Windows and Linux.</li>
<li><strong>Shape.</strong> <code>ui_snapshot</code> is one tool in a remote MCP server, used by an
agent on another machine. Agent Desktop runs locally as a CLI, a C library or a stdio MCP
server.</li>
</ul>

<h2>A comparison worth reading</h2>
<p>A {a(MUSE, "research write-up on Muse")} compares {a(BROWSE, "OpenCode Browse")} with OpenAB
Computer. Its main point: Browse lets an agent drive your real, logged-in browser on your own
machine, while OpenAB Computer lends a whole machine to an agent somewhere else. With
<code>ui_snapshot</code>, that remote agent can now read native apps as structured text, not only the
browser.</p>

<h2>What's next (not shipped)</h2>
<p>Phase 2 is <code>ui_action(ref)</code>: press a button, set a field's value, move focus or open
a menu by ref, without moving the cursor. That is the part that ends the cursor takeover. It will
also add the menu bar, which today's tree leaves out. Setting a value on a password field will be
refused.</p>
<p>After macOS, a Linux version based on AT-SPI is planned. Neither has a date. Issue #67 stays
open to track both.</p>

<p class="outro">To try it, update to {a(REL, "OpenAB Computer 0.9.0")}, give it the Accessibility
permission, and call <code>ui_snapshot</code> from an agent with the <code>owner</code>
profile.</p>
""",
            ),
            "zh": dict(
                title="OpenAB Computer 開始支援 macOS 的 accessibility tree",
                desc="OpenAB Computer 0.9.0 新增 ui_snapshot，一個把 Mac app 的 accessibility tree "
                     "以 JSON 回傳的 MCP 工具。它回傳什麼、我們從 Vercel 的 Agent Desktop 學到什麼，"
                     "以及還缺什麼。",
                og=(["OpenAB Computer 開始支援", "macOS 的 accessibility tree。"],
                    "0.9.0 的 ui_snapshot：用 JSON 讀 Mac app 的畫面，不用看圖"),
                og_alt="OpenAB 開發筆記：OpenAB Computer 開始支援 macOS 的 accessibility tree",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="lede">OpenAB Computer 0.9.0 新增了 <code>ui_snapshot</code> 這個 MCP 工具：讀取 Mac app
的 accessibility tree，以 JSON 回傳。agent 現在可以直接用文字看到視窗裡的按鈕、欄位和標籤，
連同它們在螢幕上的位置，不必再從截圖裡猜。</p>

<h2>為什麼截圖迴圈不夠用</h2>
<p>在這之前，agent 透過 OpenAB Computer 操作 Mac，走的是這樣的迴圈：截圖、猜按鈕在哪裡、用
<code>mouse</code> 點下去，再截一張圖確認。</p>
<p>社群使用者 {a(TTMUSE, "ttmuse")} 在 {a(ISSUE67, "issue #67")} 寫下了這個迴圈的代價。
這位使用者每天把 OpenAB Computer 當成雲端 agent 的手，遠端操作家裡的 Mac。每一步都要花圖片
token，小目標常常點不到，agent 工作時，真正的游標也被搶走了。</p>
<p>這個 issue 原本在等一個真正需要它的人。這則留言說明了有人真的需要，於是我們調高了優先順序，
先從 macOS 開始做。</p>

<h2>從 Agent Desktop 學到的事</h2>
<p>動手之前，我們仔細讀了 Vercel Labs 的 {a(AGENT_DESKTOP, "Agent Desktop")}：README、概念文件，
還有 macOS 的程式碼。Agent Desktop 讀取桌面 app 的 accessibility tree，以 JSON 回傳，每個 agent
能操作的元素都配有一個 ref。其中三個想法影響了我們的規劃：前兩個已經做進 <code>ui_snapshot</code>，
第三個要等第二階段。</p>
<ul>
<li><strong>用結構化的文字取代圖片。</strong>模型讀的是角色、名稱和值，不用在像素裡找按鈕。</li>
<li><strong>每個元素一個 ref，來自某一次快照。</strong>Agent Desktop 的 ref 只屬於產生它的那次快照。
畫面一變，過期或對不上的 ref 會直接被拒絕，不會用猜的，agent 重新拍一次快照就好。</li>
<li><strong>操作不靠游標（第二階段）。</strong>Agent Desktop 用 ref 執行的動作走 accessibility API，
不移動游標，也不搶走焦點。</li>
</ul>
<p>issue #67 當初也列過另一個做法：讓 OpenAB Computer 直接呼叫 Agent Desktop，好處是自己要維護的
程式碼比較少，代價是多一個外部依賴，也得跟著它的更新節奏走。最後我們決定把 accessibility tree
做成 OpenAB Computer 自己的 MCP 工具之一，放進原本就提供 <code>screenshot</code>、<code>mouse</code>、
<code>key</code> 的那支 Swift 常駐程式（{a(PR93, "PR #93")}）。</p>

<h2>ui_snapshot 回傳什麼</h2>
<p>預設讀取最前面那個 app 目前的焦點視窗。用 <code>app</code>（bundle id 或 app 名稱）、
<code>pid</code>、<code>window</code> 和 <code>all_windows</code> 可以換成別的目標。</p>
<p>每個節點都帶有角色、標題、值、說明、是否啟用或取得焦點，以及一個 frame。frame 用的是和
<code>screenshot</code>、<code>mouse</code> 相同的顯示點座標，所以 agent 不用先看螢幕，就能對準
節點點下去。每個節點也有一個 ref（<code>e1</code>、<code>e2</code>⋯⋯），在同一個快照 id 之內不會重複。</p>
<p>下面是在一台 M4 Mac mini 上對 Finder 拍的真實快照，當時沒有開任何 Finder 視窗，所以這個「視窗」
就是桌面本身，裡面兩張圖是兩顆已掛載磁碟的圖示。工具會回傳一份給模型讀的文字版：</p>
<pre><code>{{text}}</code></pre>
<p>以及同一棵樹的 JSON（節錄，省略了部分欄位）：</p>
<pre><code>{{json}}</code></pre>
<p>四個節點，花了 104 ms。磁碟名稱在這裡換成了通用名稱。agent 想打開「Data」這顆磁碟，只要對 e3 的
frame 中心 (1855, 177) 按兩下，不必先截圖找它在哪裡。</p>

<h2>上限、逾時與隱私</h2>
<p>一次快照有上限。預設最多往下 20 層或 300 個節點，整個呼叫給 3 秒；呼叫端可以調高到 50 層、
2,000 個節點和 10 秒。每次呼叫 accessibility API 之前，工具都會設定最多半秒的訊息逾時，
所以一個已經沒有回應的 app 拖不住它。</p>
<p>碰到上限或時間用完時，agent 拿到的是目前已經讀到的部分，標上 <code>truncated</code> 或
<code>timed_out</code>，不會變成錯誤。很長的文字只讀前 200 個字元，大份文件不會被整份複製出來。</p>
<p>密碼欄位一律遮蔽。遇到安全文字欄位，工具根本不會去要它的值，也不會往裡面讀。其他欄位則不遮蔽。</p>
<p>這點很重要，因為這棵樹裡有截圖看不到的文字：捲到畫面外的列、收合起來的內容、其他視窗。所以
<code>ui_snapshot</code> 只開放給 <code>owner</code> profile，而且需要 macOS 的「輔助使用」權限，
也就是 <code>mouse</code> 和 <code>key</code> 本來就在用的那一個。</p>

<h2>哪種畫面用哪個工具</h2>
<ul>
<li>原生 Mac app：<code>ui_snapshot</code>。</li>
<li>網頁：<code>browser_snapshot</code>，從瀏覽器讀取頁面結構。</li>
<li>自己繪製的內容，例如 canvas，沒有 accessibility tree：照舊用 <code>screenshot</code> 加
<code>mouse</code>。</li>
</ul>

<h2>和 Agent Desktop 一樣的地方，以及還不一樣的地方</h2>
<p>一樣的：兩者都讀 macOS 的 accessibility API，回傳 JSON 而不是圖片；都替元素配上只在單次快照內有效的
ref，差別是我們替每個節點都配，Agent Desktop 只替 agent 能操作的元素配；讀不完時都回傳部分的樹，而不是直接失敗；兩者裡面都沒有模型，迴圈由呼叫它的
agent 自己跑。</p>
<p>目前不一樣的：</p>
<ul>
<li><strong>OpenAB Computer 只能讀。</strong>Agent Desktop 已經能用 ref 點擊、輸入、設定值、
移動焦點，而且不動游標。用 OpenAB Computer 的 agent 還是得用 <code>mouse</code> 點座標，
真正的游標還是會動。</li>
<li><strong>ref。</strong>我們的 ref 只是單次快照裡的標籤，工具本身不保留狀態。Agent Desktop
會把每個 ref 對應到辨識元素用的資訊並存下來，動作之前先確認還是同一個元素。</li>
<li><strong>平台。</strong>OpenAB Computer 目前只在 macOS 上讀得到這棵樹，Agent Desktop 支援
macOS、Windows 和 Linux。</li>
<li><strong>形式。</strong><code>ui_snapshot</code> 是遠端 MCP server 裡的一個工具，給另一台
機器上的 agent 使用。Agent Desktop 則在本機以 CLI、C 函式庫或 stdio MCP server 的形式執行。</li>
</ul>

<h2>一篇值得一讀的比較</h2>
<p>Muse 上有一篇{a(MUSE, "研究文章")}比較了 {a(BROWSE, "OpenCode Browse")} 和 OpenAB Computer。
重點是：Browse 讓 agent 在你自己的電腦上操作你已經登入的那個瀏覽器，OpenAB Computer 則是把一整台
機器借給在別處的 agent。有了 <code>ui_snapshot</code>，這個遠端 agent 除了瀏覽器，也能用結構化的文字
讀原生 app 了。</p>

<h2>接下來（尚未推出）</h2>
<p>第二階段是 <code>ui_action(ref)</code>：用 ref 按按鈕、設定欄位的值、移動焦點或打開選單，
不移動游標。真正解決游標被搶走的，是這一段。它也會把目前樹裡沒有的選單列加進來。對密碼欄位設定值
則會被拒絕。</p>
<p>macOS 之後，規劃中的是以 AT-SPI 為基礎的 Linux 版本。兩者都還沒有時程，issue #67 會繼續開著追蹤。</p>

<p class="outro">想試試看的話：更新到 {a(REL, "OpenAB Computer 0.9.0")}，給它「輔助使用」權限，
再從使用 <code>owner</code> profile 的 agent 呼叫 <code>ui_snapshot</code>。</p>
""",
            ),
            "ja": dict(
                title="OpenAB Computer が macOS のアクセシビリティツリーを読めるようになりました",
                desc="OpenAB Computer 0.9.0 で、Mac アプリのアクセシビリティツリーを JSON で返す MCP "
                     "ツール ui_snapshot が加わりました。返す内容、Vercel の Agent Desktop から学んだこと、"
                     "まだ足りないこと。",
                og=(["OpenAB Computer が", "アクセシビリティツリーを読む。"],
                    "0.9.0 の ui_snapshot：Mac アプリの画面を画像ではなく JSON で"),
                og_alt="OpenAB 開発ノート：OpenAB Computer が macOS のアクセシビリティツリーを読めるようになりました",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="lede">OpenAB Computer 0.9.0 で、MCP ツール <code>ui_snapshot</code> が加わりました。Mac
アプリのアクセシビリティツリーを読み、JSON で返します。エージェントは、ウィンドウの中のボタンや
入力欄やラベルを、画面上の位置とあわせてテキストで受け取れます。スクリーンショットから読み解く
必要はもうありません。</p>

<h2>スクリーンショットのループでは足りなかった理由</h2>
<p>これまで、OpenAB Computer で Mac を操作するエージェントはこう動いていました。スクリーンショットを
撮り、ボタンの位置を推測し、<code>mouse</code> でクリックし、もう一度スクリーンショットで確かめる。</p>
<p>コミュニティのユーザー {a(TTMUSE, "ttmuse")} さんが、{a(ISSUE67, "issue #67")} でこのループの
コストを書いてくれました。この方は OpenAB Computer を毎日、自宅の Mac を動かすクラウドの
エージェントの手として使っています。一手ごとに画像のトークンがかかり、小さな対象は外れ、
エージェントが動いている間は本物のカーソルを取られてしまう、というものです。</p>
<p>この issue は、本当に必要とする人を待っていました。このコメントで実際に必要な人がいると
わかったので、優先度を上げ、macOS から取りかかりました。</p>

<h2>Agent Desktop から学んだこと</h2>
<p>コードを書く前に、Vercel Labs の {a(AGENT_DESKTOP, "Agent Desktop")} をじっくり読みました。
README、コンセプトの文書、そして macOS のコードです。Agent Desktop はデスクトップアプリの
アクセシビリティツリーを読んで JSON で返し、エージェントが操作できる要素ごとに ref を付けます。
そのうち三つの考え方が私たちの計画を形づくりました。最初の二つは今の <code>ui_snapshot</code> に
入っていて、三つ目は第 2 段階で取り組みます。</p>
<ul>
<li><strong>画像ではなく構造化されたテキスト。</strong>モデルが読むのはロール、名前、値です。
ピクセルの中からボタンを探す必要はありません。</li>
<li><strong>要素ごとの ref は、一回のスナップショットのもの。</strong>Agent Desktop の ref は、
それを作ったスナップショットに属します。UI が変われば、古い ref や曖昧な ref は推測せずに
拒否され、エージェントは新しいスナップショットを撮ります。</li>
<li><strong>ポインターを使わない操作（第 2 段階）。</strong>Agent Desktop の ref による操作はアクセシビリティ
API を通り、ポインターを動かさず、フォーカスも奪いません。</li>
</ul>
<p>issue #67 では、OpenAB Computer から Agent Desktop を呼び出す案も挙げていました。自分で持つコードが
減る一方で、外部への依存とその更新のペースを抱えることになる、という比較です。最終的に、
アクセシビリティツリーを OpenAB Computer 自身の MCP ツールの一つにすることにし、
<code>screenshot</code>、<code>mouse</code>、<code>key</code> をすでに提供している Swift の
デーモンに入れました（{a(PR93, "PR #93")}）。</p>

<h2>ui_snapshot が返すもの</h2>
<p>既定では、最前面のアプリのフォーカスされたウィンドウを読みます。<code>app</code>（bundle id か
アプリ名）、<code>pid</code>、<code>window</code>、<code>all_windows</code> で別の対象を選べます。</p>
<p>各ノードには、ロール、タイトル、値、説明、有効かどうかとフォーカスの有無、そして frame が
入ります。frame は <code>screenshot</code> や <code>mouse</code> と同じディスプレイのポイント座標
なので、エージェントは画面を見なくてもノードを狙ってクリックできます。各ノードには ref
（<code>e1</code>、<code>e2</code>…）も付き、同じスナップショット ID の中では重複しません。</p>
<p>以下は、M4 Mac mini で Finder のウィンドウを一つも開いていないときに撮った、実際の
スナップショットです。この場合のウィンドウはデスクトップそのもので、中の二つの画像は
マウントされた二台のドライブのアイコンです。ツールはモデル向けのテキスト版を返します。</p>
<pre><code>{{text}}</code></pre>
<p>同じツリーの JSON（抜粋。一部のフィールドは省いています）：</p>
<pre><code>{{json}}</code></pre>
<p>四つのノードを 104 ms で読みました。ドライブ名はここでは一般的な名前に置き換えています。
「Data」ドライブを開きたければ、エージェントは e3 の frame の中心 (1855, 177) をダブルクリック
すればよく、場所を探すためのスクリーンショットはいりません。</p>

<h2>上限、タイムアウト、プライバシー</h2>
<p>スナップショットには上限があります。既定では深さ 20 階層か 300 ノードで止まり、呼び出し全体に
3 秒を割り当てます。呼び出し側は 50 階層、2,000 ノード、10 秒まで引き上げられます。
アクセシビリティの呼び出しの前には毎回、最大 0.5 秒のメッセージタイムアウトを設定するので、
応答しなくなったアプリに止められることはありません。</p>
<p>上限や時間に達したときは、それまでに読めた分を <code>truncated</code> か <code>timed_out</code>
の印付きで返し、エラーにはしません。長いテキストは先頭 200 文字だけを読むので、大きな文書が
丸ごとコピーされることはありません。</p>
<p>パスワード欄は必ずマスクします。セキュアテキストフィールドについては、ツールは値を一切
問い合わせず、中も読みません。それ以外の入力欄はマスクしません。</p>
<p>これが大事なのは、ツリーにはスクリーンショットに写らないテキストも入っているからです。
スクロールで隠れた行、折りたたまれた内容、ほかのウィンドウ。そのため <code>ui_snapshot</code> は
<code>owner</code> プロファイルでしか使えず、macOS のアクセシビリティ権限が必要です。
<code>mouse</code> と <code>key</code> がすでに使っているのと同じ権限です。</p>

<h2>どの画面にどのツールを使うか</h2>
<ul>
<li>ネイティブの Mac アプリ：<code>ui_snapshot</code>。</li>
<li>Web ページ：<code>browser_snapshot</code>。ブラウザーからページの構造を読みます。</li>
<li>canvas のように独自に描画された、アクセシビリティツリーのない内容：これまでどおり
<code>screenshot</code> と <code>mouse</code>。</li>
</ul>

<h2>Agent Desktop と同じところ、まだ違うところ</h2>
<p>同じところ：どちらも macOS のアクセシビリティ API を読み、画像ではなく JSON を返します。どちらも
要素に、一回のスナップショットの中でだけ有効な ref を付けます。こちらはすべてのノードに、Agent Desktop
はエージェントが操作できる要素に付けます。どちらも、読み切れないときは
失敗せずに部分的なツリーを返します。どちらも中にモデルを持たず、ループは呼び出すエージェントが
回します。</p>
<p>今のところ違うところ：</p>
<ul>
<li><strong>OpenAB Computer は読むだけです。</strong>Agent Desktop はすでに、ref でクリック、入力、
値の設定、フォーカスの移動ができ、ポインターも動かしません。OpenAB Computer のエージェントは今も
<code>mouse</code> で座標をクリックするので、本物のカーソルは動きます。</li>
<li><strong>ref。</strong>こちらの ref は一回のスナップショットのラベルにすぎず、ツールは状態を
持ちません。Agent Desktop は ref ごとに要素を特定するための情報を保存し、操作の前に同じ要素で
あることを確かめます。</li>
<li><strong>プラットフォーム。</strong>OpenAB Computer がツリーを読めるのは今のところ macOS だけです。
Agent Desktop は macOS、Windows、Linux に対応しています。</li>
<li><strong>形。</strong><code>ui_snapshot</code> はリモートの MCP サーバーにあるツールの一つで、
別のマシンのエージェントが使います。Agent Desktop はローカルで、CLI、C ライブラリー、または
stdio の MCP サーバーとして動きます。</li>
</ul>

<h2>読む価値のある比較記事</h2>
<p>Muse の{a(MUSE, "リサーチ記事")}が、{a(BROWSE, "OpenCode Browse")} と OpenAB Computer を比べて
います。要点は、Browse はエージェントに自分のマシンにある、ログイン済みの本物のブラウザーを操作させ、
OpenAB Computer はマシン一台を丸ごと別の場所のエージェントに貸す、ということです。
<code>ui_snapshot</code> によって、そのリモートのエージェントはブラウザーだけでなく、
ネイティブアプリも構造化されたテキストとして読めるようになりました。</p>

<h2>次にやること（まだリリースしていません）</h2>
<p>第 2 段階は <code>ui_action(ref)</code> です。ref を使って、ボタンを押す、入力欄に値を設定する、
フォーカスを移す、メニューを開く、といった操作をカーソルを動かさずに行います。カーソルを取られる
問題を解消するのはこの部分です。今のツリーには入っていないメニューバーもここで加えます。
パスワード欄への値の設定は拒否します。</p>
<p>macOS の次は、AT-SPI を使った Linux 版を予定しています。どちらも日程は決まっていません。
issue #67 は開いたままにして、両方を追いかけます。</p>

<p class="outro">試すには、{a(REL, "OpenAB Computer 0.9.0")} に更新してアクセシビリティ権限を与え、
<code>owner</code> プロファイルのエージェントから <code>ui_snapshot</code> を呼んでください。</p>
""",
            ),
            "ko": dict(
                title="OpenAB Computer가 이제 macOS 접근성 트리를 읽습니다",
                desc="OpenAB Computer 0.9.0에 Mac 앱의 접근성 트리를 JSON으로 돌려주는 MCP 도구 "
                     "ui_snapshot이 추가됐습니다. 무엇을 돌려주는지, Vercel의 Agent Desktop에서 무엇을 "
                     "배웠는지, 아직 무엇이 빠져 있는지.",
                og=(["OpenAB Computer가 이제", "macOS 접근성 트리를 읽습니다."],
                    "0.9.0의 ui_snapshot: Mac 앱 화면을 이미지 대신 JSON으로"),
                og_alt="OpenAB 개발 노트: OpenAB Computer가 이제 macOS 접근성 트리를 읽습니다",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="lede">OpenAB Computer 0.9.0에 MCP 도구 <code>ui_snapshot</code>이 추가됐습니다. Mac 앱의
접근성 트리를 읽어 JSON으로 돌려줍니다. 이제 에이전트는 창 안의 버튼, 입력란, 레이블을 화면 위
위치와 함께 텍스트로 받습니다. 스크린샷을 보고 짐작할 필요가 없습니다.</p>

<h2>스크린샷 루프로는 부족했던 이유</h2>
<p>지금까지 OpenAB Computer로 Mac을 다루는 에이전트는 이렇게 움직였습니다. 스크린샷을 찍고,
버튼 위치를 짐작하고, <code>mouse</code>로 클릭하고, 다시 스크린샷을 찍어 확인합니다.</p>
<p>커뮤니티 사용자 {a(TTMUSE, "ttmuse")} 님이 {a(ISSUE67, "issue #67")}에 이 루프의 비용을
적어 주었습니다. 이 사용자는 OpenAB Computer를 매일, 집에 있는 Mac을 움직이는 클라우드 에이전트의
손으로 씁니다. 단계마다 이미지 토큰이 들고, 작은 대상은 빗나가고, 에이전트가 일하는 동안 실제
커서를 빼앗긴다는 내용이었습니다.</p>
<p>이 issue는 정말 필요로 하는 사람을 기다리고 있었습니다. 그 댓글로 실제로 필요한 사람이 있다는
것을 알게 되어 우선순위를 올리고 macOS부터 시작했습니다.</p>

<h2>Agent Desktop에서 배운 것</h2>
<p>코드를 쓰기 전에 Vercel Labs의 {a(AGENT_DESKTOP, "Agent Desktop")}을 꼼꼼히 읽었습니다.
README, 개념 문서, 그리고 macOS 코드입니다. Agent Desktop은 데스크톱 앱의 접근성 트리를 읽어
JSON으로 돌려주고, 에이전트가 조작할 수 있는 요소마다 ref를 붙입니다. 그중 세 가지 생각이
우리 계획의 모양을 정했습니다. 앞의 두 가지는 지금의 <code>ui_snapshot</code>에 들어 있고, 세 번째는
2단계에서 다룹니다.</p>
<ul>
<li><strong>이미지 대신 구조화된 텍스트.</strong> 모델은 역할, 이름, 값을 읽습니다. 픽셀 속에서
버튼을 찾지 않아도 됩니다.</li>
<li><strong>요소마다 하나의 ref, 한 번의 스냅샷에서.</strong> Agent Desktop의 ref는 그것을 만든
스냅샷에 속합니다. UI가 바뀌면 오래되었거나 모호한 ref는 짐작하지 않고 거부되고, 에이전트는 새
스냅샷을 찍습니다.</li>
<li><strong>포인터 없이 조작하기(2단계).</strong> Agent Desktop의 ref 동작은 접근성 API를 거치며
포인터를 움직이지 않고 포커스도 가져가지 않습니다.</li>
</ul>
<p>issue #67에는 OpenAB Computer에서 Agent Desktop을 호출하는 방안도 있었습니다. 직접 관리할
코드는 줄지만 외부 의존성과 그 업데이트 주기를 떠안게 된다는 비교였습니다. 결국 접근성 트리를
OpenAB Computer 자체 MCP 도구 중 하나로 만들기로 했고, <code>screenshot</code>, <code>mouse</code>,
<code>key</code>를 이미 제공하는 Swift 데몬에 넣었습니다({a(PR93, "PR #93")}).</p>

<h2>ui_snapshot이 돌려주는 것</h2>
<p>기본으로는 맨 앞에 있는 앱의 포커스된 창을 읽습니다. <code>app</code>(bundle id나 앱 이름),
<code>pid</code>, <code>window</code>, <code>all_windows</code>로 다른 대상을 고를 수 있습니다.</p>
<p>각 노드에는 역할, 제목, 값, 설명, 활성 여부와 포커스 여부, 그리고 frame이 들어 있습니다. frame은
<code>screenshot</code>, <code>mouse</code>와 같은 디스플레이 포인트 좌표를 쓰므로, 에이전트는
화면을 먼저 보지 않고도 노드를 겨냥해 클릭할 수 있습니다. 노드마다 ref(<code>e1</code>,
<code>e2</code>, …)도 붙는데, 같은 스냅샷 ID 안에서는 겹치지 않습니다.</p>
<p>아래는 M4 Mac mini에서 Finder 창을 하나도 열지 않은 상태로 찍은 실제 스냅샷입니다. 이때 창은
데스크톱 자체이고, 그 안의 두 이미지는 마운트된 드라이브 두 개의 아이콘입니다. 도구는 모델이
읽을 텍스트 형식을 돌려줍니다.</p>
<pre><code>{{text}}</code></pre>
<p>같은 트리의 JSON(발췌, 일부 필드는 생략):</p>
<pre><code>{{json}}</code></pre>
<p>노드 네 개를 104 ms에 읽었습니다. 드라이브 이름은 여기서 일반적인 이름으로 바꿨습니다.
“Data” 드라이브를 열려면 에이전트는 e3 frame의 중심 (1855, 177)을 더블클릭하면 되고, 위치를
찾으려고 스크린샷을 찍을 필요가 없습니다.</p>

<h2>한도, 타임아웃, 프라이버시</h2>
<p>스냅샷에는 한도가 있습니다. 기본으로 깊이 20단계나 노드 300개에서 멈추고, 호출 전체에 3초를
줍니다. 호출하는 쪽은 50단계, 노드 2,000개, 10초까지 올릴 수 있습니다. 접근성 호출 전마다
최대 0.5초의 메시지 타임아웃을 걸기 때문에, 응답을 멈춘 앱이 도구를 붙잡아 둘 수 없습니다.</p>
<p>한도나 시간이 다 되면 에이전트는 그때까지 읽은 부분을 <code>truncated</code>나
<code>timed_out</code> 표시와 함께 받고, 오류는 나지 않습니다. 긴 텍스트는 앞의 200자만 읽으므로
큰 문서가 통째로 복사되지 않습니다.</p>
<p>비밀번호 입력란은 항상 가립니다. 보안 텍스트 필드에 대해서는 도구가 값을 아예 요청하지 않고
안쪽도 읽지 않습니다. 다른 입력란은 가리지 않습니다.</p>
<p>이 점이 중요한 이유는 트리에 스크린샷에 보이지 않는 텍스트도 들어 있기 때문입니다. 스크롤로
가려진 행, 접힌 내용, 다른 창. 그래서 <code>ui_snapshot</code>은 <code>owner</code> 프로필에서만
쓸 수 있고, macOS 손쉬운 사용(Accessibility) 권한이 필요합니다. <code>mouse</code>와
<code>key</code>가 이미 쓰는 바로 그 권한입니다.</p>

<h2>어떤 화면에 어떤 도구를</h2>
<ul>
<li>네이티브 Mac 앱: <code>ui_snapshot</code>.</li>
<li>웹 페이지: <code>browser_snapshot</code>. 브라우저에서 페이지 구조를 읽습니다.</li>
<li>canvas처럼 직접 그린, 접근성 트리가 없는 내용: 예전처럼 <code>screenshot</code>과
<code>mouse</code>.</li>
</ul>

<h2>Agent Desktop과 같은 점, 아직 다른 점</h2>
<p>같은 점: 둘 다 macOS 접근성 API를 읽고 이미지 대신 JSON을 돌려줍니다. 둘 다 요소에 한 번의
스냅샷 안에서만 유효한 ref를 붙입니다. 우리는 모든 노드에, Agent Desktop은 에이전트가 조작할 수 있는
요소에 붙입니다. 둘 다 다 읽지 못하면 실패하는 대신 일부 트리를 돌려줍니다.
둘 다 안에 모델이 없고, 루프는 호출하는 에이전트가 돌립니다.</p>
<p>지금 다른 점:</p>
<ul>
<li><strong>OpenAB Computer는 읽기만 합니다.</strong> Agent Desktop은 이미 ref로 클릭, 입력, 값
설정, 포커스 이동을 하고 포인터도 움직이지 않습니다. OpenAB Computer의 에이전트는 여전히
<code>mouse</code>로 좌표를 클릭하고, 실제 커서는 여전히 움직입니다.</li>
<li><strong>ref.</strong> 우리 ref는 한 스냅샷의 레이블일 뿐이고 도구는 상태를 두지 않습니다.
Agent Desktop은 ref마다 요소를 식별할 정보를 저장해 두고, 동작하기 전에 같은 요소인지
확인합니다.</li>
<li><strong>플랫폼.</strong> OpenAB Computer가 트리를 읽는 곳은 아직 macOS뿐입니다. Agent
Desktop은 macOS, Windows, Linux를 지원합니다.</li>
<li><strong>형태.</strong> <code>ui_snapshot</code>은 원격 MCP 서버의 도구 하나로, 다른 기기의
에이전트가 씁니다. Agent Desktop은 로컬에서 CLI, C 라이브러리, 또는 stdio MCP 서버로
실행됩니다.</li>
</ul>

<h2>읽어 볼 만한 비교 글</h2>
<p>Muse의 {a(MUSE, "리서치 글")}이 {a(BROWSE, "OpenCode Browse")}와 OpenAB Computer를 비교합니다.
요점은 이렇습니다. Browse는 에이전트가 내 기기에서 로그인된 실제 브라우저를 다루게 하고, OpenAB
Computer는 기기 한 대를 통째로 다른 곳의 에이전트에게 빌려줍니다. <code>ui_snapshot</code> 덕분에
그 원격 에이전트는 이제 브라우저뿐 아니라 네이티브 앱도 구조화된 텍스트로 읽을 수 있습니다.</p>

<h2>다음 단계(아직 출시 전)</h2>
<p>2단계는 <code>ui_action(ref)</code>입니다. ref로 버튼 누르기, 입력란 값 설정, 포커스 이동,
메뉴 열기를 커서를 움직이지 않고 합니다. 커서를 빼앗기는 문제를 끝내는 것이 이 부분입니다. 지금
트리에 빠져 있는 메뉴 막대도 이때 추가합니다. 비밀번호 입력란에 값을 설정하는 것은 거부합니다.</p>
<p>macOS 다음으로는 AT-SPI 기반의 Linux 버전을 계획하고 있습니다. 둘 다 일정은 정해지지 않았고,
issue #67을 열어 둔 채 둘 다 추적합니다.</p>

<p class="outro">써 보려면 {a(REL, "OpenAB Computer 0.9.0")}으로 업데이트하고 손쉬운 사용 권한을 준 뒤,
<code>owner</code> 프로필의 에이전트에서 <code>ui_snapshot</code>을 호출하세요.</p>
""",
            ),
        },
    ),
]
