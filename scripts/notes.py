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
REL10 = "https://github.com/openabdev/openab-computer/releases/tag/v0.10.0"
PR93 = "https://github.com/openabdev/openab-computer/pull/93"
ISSUE67 = "https://github.com/openabdev/openab-computer/issues/67"
TTMUSE = "https://github.com/openabdev/openab-computer/issues/67#issuecomment-6726398810"
AGENT_DESKTOP = "https://github.com/vercel-labs/agent-desktop"
MUSE = ("https://muse.ai/s/opencode-browse-vs-openab-computer-lxc6yxwxmxpk7iz/"
        "7lEkIj9rBZ_cbTI4KbMuF5EQQySq8Himvw-fgz8ELfg")
BROWSE = "https://github.com/anomalyco/browse"

# Links for the "How does an agent click the right button?" section. Facts and the exact source
# lines are recorded outside this repo (facts-approaches.md in the task's run dir).
ANTHROPIC_CU = "https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool"
OPENAI_CU = "https://developers.openai.com/api/docs/guides/tools-computer-use"
OPENAI_CUA = "https://github.com/openai/openai-cua-sample-app"
SOM = "https://arxiv.org/abs/2310.11441"
OMNIPARSER = "https://github.com/microsoft/OmniParser"
APPLESCRIPT = ("https://developer.apple.com/library/archive/documentation/AppleScript/"
               "Conceptual/AppleScriptLangGuide/introduction/ASLR_intro.html")
AX_API = "https://developer.apple.com/documentation/applicationservices/axuielement_h"
UIA = "https://learn.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32"
ATSPI = "https://docs.gtk.org/atspi2/"
WEB_AX = "https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree"

# A real Finder snapshot taken on an Apple-silicon Mac with OpenAB Computer 0.9.0 (default limits),
# shown verbatim except: the two drive names are replaced with "Data" and "Backup", the pid is
# left out, and the JSON is an excerpt (e4, displays and coordinates are cut). The raw output is
# kept outside this repo as evidence.
UI_TEXT = """ui_snapshot snap-54785c06 · Finder (com.apple.finder) · 4 nodes · 46 ms
[e1] AXScrollArea desc="desktop" (0,0 1920×1080) disabled
  [e2] AXGroup desc="desktop" (0,0 1920×1080)
    [e3] AXImage "Data" (1823,145 64×64)
    [e4] AXImage "Backup" (1823,33 64×64)"""

UI_JSON = """{
  "snapshot_id": "snap-54785c06",
  "app": { "name": "Finder", "bundle_id": "com.apple.finder" },
  "node_count": 4,
  "truncated": false,
  "timed_out": false,
  "elapsed_ms": 46,
  "limits": { "max_depth": 20, "max_nodes": 300, "timeout_ms": 3000 },
  "windows": [
    { "ref": "e1", "role": "AXScrollArea", "description": "desktop",
      "enabled": false,
      "frame": { "x": 0, "y": 0, "width": 1920, "height": 1080 },
      "children": [
        { "ref": "e2", "role": "AXGroup", "description": "desktop",
          "children": [
            { "ref": "e3", "role": "AXImage", "role_description": "image",
              "title": "Data", "description": "Data", "display": 0,
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
        og_art="ax-tree",   # og_cards.ARTS: a topic illustration, never the mascot
        text=UI_TEXT,
        json=UI_JSON,
        langs={
            "en": dict(
                title="OpenAB Computer can now read the macOS accessibility tree",
                desc="How does an agent click exactly the right button on a remote desktop? "
                     "OpenAB Computer 0.9.0 adds ui_snapshot, an MCP tool that returns a Mac app's "
                     "accessibility tree as JSON.",
                og=(["OpenAB Computer can now read", "the macOS accessibility tree."],
                    "ui_snapshot in 0.9.0: a Mac app's UI as JSON, not pixels"),
                og_alt="OpenAB dev note: OpenAB Computer can now read the macOS accessibility tree",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="hook">Have you ever wondered how an agent actually manages to click exactly the right
button in an app on a remote computer's desktop when you ask it to?</p>

<p class="lede">OpenAB Computer 0.9.0 adds <code>ui_snapshot</code>, an MCP tool that reads the
accessibility tree of a Mac app and returns it as JSON. An agent can now see the buttons, fields
and labels in a window as text, with their positions on screen, instead of working them out from
a screenshot.</p>

<h2>How does an agent click the right button?</h2>
<p>Computer use means letting an agent operate a computer: look at the screen, move the mouse,
click and type. Clicking is easy. Clicking the right thing is hard: for a Save button on the
screen, the agent has to know where it is, whether it really is a button, and whether it can be
pressed right now.</p>
<p>There are roughly four common ways to do it.</p>
<ol class="ways">
<li>
<p><strong>1. Look at a screenshot and guess coordinates.</strong> At every step the agent takes a
screenshot, the model works out where the button is and returns x and y, the mouse moves there and
clicks, and another screenshot checks the result.</p>
<p><em>Pros:</em> it is the most general. Any app whose screen you can see can be operated,
including games and custom-drawn interfaces.</p>
<p><em>Cons:</em> every step sends an image, which costs tokens and time. The coordinates are a
guess, so clicks often land off target when a button is small or the resolution or scaling
differs. The model sees pixels: it cannot tell a button from a picture that looks like one, and it
does not know whether a button is greyed out. Clicking moves the real cursor, so you cannot use
that computer while the agent works.</p>
<p><em>Examples:</em> Anthropic's {a(ANTHROPIC_CU, "computer use tool")} works this way. Claude
receives screenshots and returns actions such as <code>left_click</code> with an [x, y] in
screenshot pixels, which your code carries out. Its docs list clicks that land in the right area
but miss a very small target, and suggest the zoom action for a closer look. OpenAI's
{a(OPENAI_CU, "computer use tool")}, built on its Computer-Using Agent model
({a(OPENAI_CUA, "CUA")}), also looks at screenshots and returns mouse and keyboard actions with x
and y; screenshots count as image input. OpenAI also offers a second mode in which the model writes
code (Playwright or PyAutoGUI) to drive the interface.</p>
</li>
<li>
<p><strong>2. Number the screenshot first, then ask the model to pick (often called
set-of-mark).</strong> Another vision model first detects the elements on screen, draws a box
around each and numbers them. The agent then answers "press 7".</p>
<p><em>Pros:</em> the model does not have to work out coordinates, so it misses far less
often.</p>
<p><em>Cons:</em> every step still sends an image, and there is now a second model. If the detector
misses an element or boxes the wrong thing, the agent goes wrong with it. It still does not know
an element's state, such as whether it can be pressed or what its value is.</p>
<p><em>Examples:</em> the idea comes from the {a(SOM, "Set-of-Mark")} prompting paper, which
splits an image into regions with an off-the-shelf segmentation model, overlays numbers or boxes,
and has the model answer from the marked image. Microsoft's {a(OMNIPARSER, "OmniParser")} applies
it to screenshots: a detection model finds the interactable regions, a caption model describes
what each element does, and the screenshot becomes a structured list of elements.</p>
</li>
<li>
<p><strong>3. Use the app's own API or scripts.</strong> For example, an AppleScript that tells
Finder to open a folder, or a command-line tool.</p>
<p><em>Pros:</em> the most precise, and no screen is needed.</p>
<p><em>Cons:</em> every app is different, many apps have no such interface, and the agent has to
learn each app first.</p>
<p><em>Example:</em> Apple's {a(APPLESCRIPT, "AppleScript")} controls scriptable Mac apps and parts
of macOS directly. Apps that are not scriptable are out of its reach.</p>
</li>
<li>
<p><strong>4. Read the accessibility tree.</strong> Operating systems already have an interface
built for screen readers: the macOS {a(AX_API, "Accessibility API")}, Windows
{a(UIA, "UI Automation")} and Linux {a(ATSPI, "AT-SPI")}. Web pages have the browser's
{a(WEB_AX, "accessibility tree")}. It describes buttons, fields and menus as a tree: the role,
the label, the current value, whether the element can be used, and its exact position on
screen.</p>
<p><em>Pros:</em> the result is text, which is cheap and fast. The system gives the kind of
element, its name and its state directly. Positions are exact. Each element can get a ref, and
the agent can later say "press this ref", without even moving the cursor.</p>
<p><em>Cons:</em> it depends on how well the app supports it. Custom-drawn interfaces, canvases and
games are often empty in the tree. It needs the Accessibility permission. A complex interface makes
a large tree, so depth and node count need limits. When the screen changes, old refs stop working
and the tree has to be read again.</p>
<p><em>Example:</em> Vercel's {a(AGENT_DESKTOP, "Agent Desktop")} takes this route. It reads a
desktop app's accessibility tree and returns it as JSON with a ref for every element an agent can
act on; ref actions do not move the pointer or take focus. It covers macOS, Windows and Linux.</p>
</li>
</ol>
{{cmp_table}}
{{fig_aim}}

<h3>Why we chose the accessibility tree</h3>
<p>In OpenAB Computer the agent is somewhere else, so the most expensive part is sending screenshots
back and forth. The accessibility tree turns each step from "send an image, guess a coordinate" into
"read some text, pick a ref". It also fixes the missed clicks, because positions are not guessed.
For most standard Mac apps that is enough. It does not cover everything, so we kept screenshots
and use all three together: <code>ui_snapshot</code> reads the accessibility tree of native apps,
<code>browser_snapshot</code> reads the browser's accessibility tree for web pages, and whatever
the tree cannot see (canvases, custom-drawn interfaces) goes back to <code>screenshot</code> and
<code>mouse</code>.</p>

<div class="callout">
<h2>The research behind this</h2>
<p>This work started with a {a(MUSE, "research report")} we published for the community on Muse.
It compares three projects. {a(BROWSE, "OpenCode Browse")} lets an agent drive your own logged-in
browser on your machine. {a(AGENT_DESKTOP, "Vercel Agent Desktop")} lets an agent drive desktop apps
through the accessibility tree: it returns structured JSON with a ref for each element, and acts on
those refs without moving the pointer or taking focus. OpenAB Computer lends a whole machine to an
agent somewhere else. For that remote agent, the report found, the screenshot loop is the main
cost.</p>
<p>We took what Agent Desktop does well, reading the accessibility tree as structured data with
refs instead of guessing from pixels, and made it an OpenAB Computer MCP tool,
<code>ui_snapshot</code>. The remote agent can now read native apps as structured text, not only
the browser.</p>
</div>

<h2>Why the screenshot loop was not enough</h2>
<p>Until now, an agent using OpenAB Computer on a Mac worked in a loop: take a screenshot, guess
where a button is, click it with <code>mouse</code>, then take another screenshot to check.</p>
<p>A community user, {a(TTMUSE, "ttmuse")}, described the cost of that loop on
{a(ISSUE67, "issue #67")}. They use OpenAB Computer every day as the hands of a cloud agent that
drives a home Mac. Every step costs image tokens, small targets get missed, and the real cursor is
taken over while the agent works.</p>
<p>The issue had been waiting for a real user. The comment showed there was one, so we raised its
priority and started with macOS.</p>
{{fig_loop}}

<h2>What we learned from Agent Desktop</h2>
<p>Before writing code we read Vercel Labs' {a(AGENT_DESKTOP, "Agent Desktop")} closely: its
README, its concept docs and its macOS code. Agent Desktop reads the accessibility tree of a
desktop app and returns it as JSON, with a ref for every element an agent can act on. Three of its
ideas shaped our plan: the first two are in <code>ui_snapshot</code>, and the third shipped in
0.10.0 as <code>ui_action</code>.</p>
<ul>
<li><strong>Structured text instead of images.</strong> The model reads roles, names and values.
It does not have to find a button in pixels.</li>
<li><strong>A ref per element, from one snapshot.</strong> Agent Desktop's refs belong to the
snapshot that produced them. When the UI changes, a stale or ambiguous ref is rejected instead of
guessed, and the agent takes a new snapshot.</li>
<li><strong>Acting without the pointer (phase 2, shipped in 0.10.0).</strong> Agent Desktop's ref actions go through the
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
{{fig_tree}}
<p>Here is a real snapshot of Finder on an Apple-silicon Mac, taken with no Finder window open. The
window is the desktop itself, and the two images in it are the icons of two mounted drives. The
tool returns a text form for the model:</p>
<pre><code>{{text}}</code></pre>
<p>and the same tree as JSON (an excerpt; some fields are left out):</p>
<pre><code>{{json}}</code></pre>
<p>In this one run it read four nodes in 46 ms. The drive names are replaced with generic ones here. To open the
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
<li><strong>Acting by ref is new in 0.10.0.</strong> Until then OpenAB Computer only read the tree.
Agent Desktop could already click, type, set values and move focus by ref without moving the
pointer. Since 0.10.0, <code>ui_action</code> presses, sets values and moves focus by ref without
moving the cursor too. Drags, gestures and custom-drawn content still go through
<code>mouse</code>, and there the real cursor still moves.</li>
<li><strong>Refs.</strong> Since 0.10.0 the tool keeps the last four snapshots for five minutes.
Before acting it checks that the element is still there, with the same role and in the same
window, and refuses a stale ref instead of guessing a replacement. Agent Desktop stores a map from
each ref to evidence of the element's identity, and checks it is the same element before
acting.</li>
<li><strong>Platforms.</strong> OpenAB Computer reads the tree on macOS only. Agent Desktop covers
macOS, Windows and Linux.</li>
<li><strong>Shape.</strong> <code>ui_snapshot</code> is one tool in a remote MCP server, used by an
agent on another machine. Agent Desktop runs locally as a CLI, a C library or a stdio MCP
server.</li>
</ul>

<h2>Phase 2 shipped: ui_action in 0.10.0</h2>
<p>Phase 2 is <code>ui_action</code>, released in {a(REL10, "OpenAB Computer 0.10.0")}. With a
<code>snapshot_id</code> and a <code>ref</code> it presses a button, sets a field's value, moves
focus, opens a menu, confirms, cancels, or steps a value up or down, through the accessibility API
and without moving the cursor. That is the part that ends the cursor takeover. Pass
<code>include_menu_bar</code> to <code>ui_snapshot</code> and menu bar items get refs too. Through
a switchboard, setting a value on a password field is refused unless the owner opts in.</p>
{{fig_action}}
<p>Next is a Linux version based on AT-SPI. It has no date yet. Issue #67 stays open to track
it.</p>

<p class="outro">To try it, update to {a(REL10, "OpenAB Computer 0.10.0")}, give it the
Accessibility permission, and call <code>ui_snapshot</code> and then <code>ui_action</code> from an
agent with the <code>owner</code> profile.</p>
""",
            ),
            "zh": dict(
                title="OpenAB Computer 開始支援 macOS 的 accessibility tree",
                desc="Agent 是怎麼在遠端電腦上精準點到那顆按鈕的？"
                     "OpenAB Computer 0.9.0 新增 ui_snapshot，一個把 Mac app 的 accessibility tree "
                     "以 JSON 回傳的 MCP 工具。它回傳什麼、我們從 Vercel 的 Agent Desktop 學到什麼，"
                     "以及還缺什麼。",
                og=(["OpenAB Computer 開始支援", "macOS 的 accessibility tree。"],
                    "0.9.0 的 ui_snapshot：用 JSON 讀 Mac app 的畫面，不用看圖"),
                og_alt="OpenAB 開發筆記：OpenAB Computer 開始支援 macOS 的 accessibility tree",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="hook">你有沒有想過：當你請 Agent 幫你用滑鼠點擊遠端電腦桌面上某個 app 裡的一顆按鈕時，Agent 到底是怎麼做到精準點擊的？</p>

<p class="lede">OpenAB Computer 0.9.0 新增了 <code>ui_snapshot</code> 這個 MCP 工具：讀取 Mac app
的 accessibility tree，以 JSON 回傳。agent 現在可以直接用文字看到視窗裡的按鈕、欄位和標籤，
連同它們在螢幕上的位置，不必再從截圖裡猜。</p>

<h2>Agent 要怎麼點到對的按鈕？</h2>
<p>所謂 computer use，就是讓 agent 操作一台電腦：看畫面、移動滑鼠、點擊、打字。點下去不難，
難的是點到對的東西。畫面上有一顆「儲存」按鈕，agent 得知道它在哪裡、是不是真的是按鈕、
現在能不能按。</p>
<p>常見的做法大致有四種。</p>
<ol class="ways">
<li>
<p><strong>1. 看截圖，猜座標。</strong>agent 每一步截一張圖，模型從圖裡判斷按鈕位置、回傳 x、y，
再移動滑鼠點下去，再截圖確認。</p>
<p><em>優點：</em>最通用，只要畫面看得到，什麼 app 都能操作，包括遊戲和自己畫的介面。</p>
<p><em>缺點：</em>每一步都要傳一張圖，token 成本高、速度慢；座標是猜的，按鈕小、解析度或縮放比例
不同時常點偏；模型看到的是像素，分不清按鈕和長得像按鈕的圖片，也不知道按鈕是不是灰掉了；
點擊要真的移動游標，agent 工作時你就不能用那台電腦。</p>
<p><em>例子：</em>Anthropic 的 {a(ANTHROPIC_CU, "computer use 工具")}就是這樣運作：Claude 拿到截圖，
回傳 <code>left_click</code> 這類動作和以截圖像素為單位的 [x, y]，由你的程式去執行。它的文件也列出
目標很小時，點擊落在對的區域卻沒點中的情況，建議用 zoom 動作放大檢查。OpenAI 的
{a(OPENAI_CU, "computer use 工具")}建立在它的 Computer-Using Agent 模型（{a(OPENAI_CUA, "CUA")}）上，
同樣看截圖，回傳帶 x、y 的滑鼠和鍵盤動作，截圖算作圖片輸入。OpenAI 另外也提供一種做法，讓模型寫程式
（Playwright 或 PyAutoGUI）來操作介面。</p>
</li>
<li>
<p><strong>2. 先在截圖上標號，再請模型選（常被稱為 set-of-mark）。</strong>先用另一個視覺模型偵測
元件、框起來編號，再請 agent 回答「按 7 號」。</p>
<p><em>優點：</em>模型不用自己算座標，點偏少很多。</p>
<p><em>缺點：</em>還是每步要傳圖，又多一個偵測模型，漏掉或框錯，agent 就跟著錯，也不知道元件狀態
（能不能按、目前的值）。</p>
<p><em>例子：</em>這個做法出自 {a(SOM, "Set-of-Mark")} 這篇論文：用現成的分割模型把圖切成區塊，
疊上數字或框，模型看著標好的圖回答。Microsoft 的 {a(OMNIPARSER, "OmniParser")} 把它用在螢幕截圖上：
一個偵測模型找出可以互動的區域，一個描述模型說明每個元素的用途，把截圖轉成一份結構化的元素清單。</p>
</li>
<li>
<p><strong>3. 用 app 自己的 API 或腳本。</strong>例如用 AppleScript 叫 Finder 開資料夾，或用指令列工具。</p>
<p><em>優點：</em>最精準，不需要畫面。</p>
<p><em>缺點：</em>每個 app 都不一樣，很多 app 沒有這種介面，agent 要先知道每個 app 怎麼用。</p>
<p><em>例子：</em>Apple 的 {a(APPLESCRIPT, "AppleScript")} 可以直接控制「可腳本化」的 Mac app 和部分
macOS 功能；不支援腳本的 app 就用不上。</p>
</li>
<li>
<p><strong>4. 讀 accessibility tree。</strong>作業系統本來就為螢幕閱讀器準備了一套介面
（macOS {a(AX_API, "Accessibility API")}、Windows {a(UIA, "UI Automation")}、Linux {a(ATSPI, "AT-SPI")}；
網頁也有瀏覽器的 {a(WEB_AX, "accessibility tree")}），把按鈕、欄位、選單描述成一棵樹：角色、標籤、
目前的值、能不能操作，以及在螢幕上的確切位置。</p>
<p><em>優點：</em>回傳的是文字，便宜又快；種類、名稱、狀態由系統直接給；位置是確切的；每個元件可以有
ref，之後可以「對這個 ref 按下去」，連游標都不用移動。</p>
<p><em>缺點：</em>要看 app 有沒有好好支援，自己畫的介面、canvas、遊戲在樹裡常是空的；需要開「輔助使用」
權限；介面很複雜時樹很大，要限制深度和節點數；畫面一變，舊的 ref 就失效，要重新讀。</p>
<p><em>例子：</em>Vercel 的 {a(AGENT_DESKTOP, "Agent Desktop")} 走的就是這條路：讀桌面 app 的
accessibility tree，以 JSON 回傳，每個 agent 能操作的元素都有 ref；用 ref 執行動作時不移動游標，
也不搶走焦點。它支援 macOS、Windows 和 Linux。</p>
</li>
</ol>
{{cmp_table}}
{{fig_aim}}

<h3>為什麼我們選 accessibility tree</h3>
<p>對 OpenAB Computer 這種「agent 在遠端」的情境，成本最高的就是一直來回傳截圖。accessibility tree
把每一步從「傳一張圖、猜一次座標」變成「讀一段文字、選一個 ref」，也解決了點不準，因為位置不是猜的。
對大多數標準的 Mac app 來說已經夠用。但它不是萬能的，所以我們保留截圖，三種一起用：原生 app 用
<code>ui_snapshot</code> 讀 accessibility tree；網頁用 <code>browser_snapshot</code> 讀瀏覽器的
accessibility tree；樹裡看不到的（canvas、自己畫的介面）回到截圖加 <code>mouse</code>。</p>

<div class="callout">
<h2>這項工作背後的研究</h2>
<p>這次的工作，起點是我們在 Muse 上為社群發表的一份{a(MUSE, "研究報告")}。報告比較了三個專案。{a(BROWSE, "OpenCode Browse")} 讓 agent 在你自己的電腦上，操作你已經登入的瀏覽器。{a(AGENT_DESKTOP, "Vercel Agent Desktop")} 讓 agent 透過 accessibility tree 操作桌面 app：它回傳
結構化的 JSON，每個元素都有一個 ref，用 ref 執行動作時不移動游標，也不搶走焦點。OpenAB Computer
則是把一整台機器借給在別處的 agent。報告也指出，對這個遠端 agent 來說，主要的成本花在截圖迴圈上。</p>
<p>我們把 Agent Desktop 的長處帶了過來：把 accessibility tree 當成帶有 ref 的結構化資料來讀，
不再從像素裡猜，並做成 OpenAB Computer 的 MCP 工具 <code>ui_snapshot</code>。現在遠端 agent
除了瀏覽器，也能用結構化的文字讀原生 app。</p>
</div>

<h2>為什麼截圖迴圈不夠用</h2>
<p>在這之前，agent 透過 OpenAB Computer 操作 Mac，走的是這樣的迴圈：截圖、猜按鈕在哪裡、用
<code>mouse</code> 點下去，再截一張圖確認。</p>
<p>社群使用者 {a(TTMUSE, "ttmuse")} 在 {a(ISSUE67, "issue #67")} 寫下了這個迴圈的代價。
這位使用者每天把 OpenAB Computer 當成雲端 agent 的手，遠端操作家裡的 Mac。每一步都要花圖片
token，小目標常常點不到，agent 工作時，真正的游標也被搶走了。</p>
<p>這個 issue 原本在等一個真正需要它的人。這則留言說明了有人真的需要，於是我們調高了優先順序，
先從 macOS 開始做。</p>
{{fig_loop}}

<h2>從 Agent Desktop 學到的事</h2>
<p>動手之前，我們仔細讀了 Vercel Labs 的 {a(AGENT_DESKTOP, "Agent Desktop")}：README、概念文件，
還有 macOS 的程式碼。Agent Desktop 讀取桌面 app 的 accessibility tree，以 JSON 回傳，每個 agent
能操作的元素都配有一個 ref。其中三個想法影響了我們的規劃：前兩個做進了 <code>ui_snapshot</code>，
第三個在 0.10.0 以 <code>ui_action</code> 推出。</p>
<ul>
<li><strong>用結構化的文字取代圖片。</strong>模型讀的是角色、名稱和值，不用在像素裡找按鈕。</li>
<li><strong>每個元素一個 ref，來自某一次快照。</strong>Agent Desktop 的 ref 只屬於產生它的那次快照。
畫面一變，過期或對不上的 ref 會直接被拒絕，不會用猜的，agent 重新拍一次快照就好。</li>
<li><strong>操作不靠游標（第二階段，已在 0.10.0 推出）。</strong>Agent Desktop 用 ref 執行的動作走 accessibility API，
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
{{fig_tree}}
<p>下面是在一台 Apple 晶片的 Mac 上對 Finder 拍的真實快照，當時沒有開任何 Finder 視窗，所以這個「視窗」
就是桌面本身，裡面兩張圖是兩顆已掛載磁碟的圖示。工具會回傳一份給模型讀的文字版：</p>
<pre><code>{{text}}</code></pre>
<p>以及同一棵樹的 JSON（節錄，省略了部分欄位）：</p>
<pre><code>{{json}}</code></pre>
<p>這一次讀到四個節點，花了 46 ms。磁碟名稱在這裡換成了通用名稱。agent 想打開「Data」這顆磁碟，只要對 e3 的
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
<li><strong>用 ref 操作是 0.10.0 才有的。</strong>在那之前 OpenAB Computer 只能讀。Agent Desktop
早就能用 ref 點擊、輸入、設定值、移動焦點，而且不動游標；從 0.10.0 起，<code>ui_action</code>
也能用 ref 按下、設定值、移動焦點，游標不動。拖曳、手勢和自己繪製的內容還是得用 <code>mouse</code>，
這時真正的游標還是會動。</li>
<li><strong>ref。</strong>從 0.10.0 起，工具會保留最近四次快照五分鐘。動作之前先確認元素還在、角色
沒變、還在同一個視窗裡；ref 過期就拒絕，不會猜一個替代的。Agent Desktop 會把每個 ref 對應到辨識
元素用的資訊並存下來，動作之前先確認還是同一個元素。</li>
<li><strong>平台。</strong>OpenAB Computer 目前只在 macOS 上讀得到這棵樹，Agent Desktop 支援
macOS、Windows 和 Linux。</li>
<li><strong>形式。</strong><code>ui_snapshot</code> 是遠端 MCP server 裡的一個工具，給另一台
機器上的 agent 使用。Agent Desktop 則在本機以 CLI、C 函式庫或 stdio MCP server 的形式執行。</li>
</ul>

<h2>第二階段已推出：0.10.0 的 ui_action</h2>
<p>第二階段是 <code>ui_action</code>，已在 {a(REL10, "OpenAB Computer 0.10.0")} 推出。帶著
<code>snapshot_id</code> 和 <code>ref</code>，它透過 accessibility API 按按鈕、設定欄位的值、移動焦點、
打開選單、確認、取消，或把數值調高調低，而且不移動游標。真正解決游標被搶走的，是這一段。對
<code>ui_snapshot</code> 加上 <code>include_menu_bar</code>，選單列的項目也會有 ref。透過 switchboard
時，對密碼欄位設定值預設會被拒絕，除非擁有者自己開啟。</p>
{{fig_action}}
<p>接下來是以 AT-SPI 為基礎的 Linux 版本，還沒有時程，issue #67 會繼續開著追蹤。</p>

<p class="outro">想試試看的話：更新到 {a(REL10, "OpenAB Computer 0.10.0")}，給它「輔助使用」權限，
再從使用 <code>owner</code> profile 的 agent 先呼叫 <code>ui_snapshot</code>，再呼叫
<code>ui_action</code>。</p>
""",
            ),
            "ja": dict(
                title="OpenAB Computer が macOS のアクセシビリティツリーを読めるようになりました",
                desc="リモートのデスクトップで、エージェントはどうやって狙ったボタンを正確に押すのか。"
                     "OpenAB Computer 0.9.0 で、Mac アプリのアクセシビリティツリーを JSON で返す MCP "
                     "ツール ui_snapshot が加わりました。返す内容、Vercel の Agent Desktop から学んだこと、"
                     "まだ足りないこと。",
                og=(["OpenAB Computer が", "アクセシビリティツリーを読む。"],
                    "0.9.0 の ui_snapshot：Mac アプリの画面を画像ではなく JSON で"),
                og_alt="OpenAB 開発ノート：OpenAB Computer が macOS のアクセシビリティツリーを読めるようになりました",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="hook">エージェントに「リモートのコンピューターのデスクトップで、あるアプリのこのボタンを
クリックして」と頼んだとき、エージェントがどうやって狙いどおりに正確にクリックしているのか、
考えたことはありますか。</p>

<p class="lede">OpenAB Computer 0.9.0 で、MCP ツール <code>ui_snapshot</code> が加わりました。Mac
アプリのアクセシビリティツリーを読み、JSON で返します。エージェントは、ウィンドウの中のボタンや
入力欄やラベルを、画面上の位置とあわせてテキストで受け取れます。スクリーンショットから読み解く
必要はもうありません。</p>

<h2>エージェントはどうやって正しいボタンを押すのか</h2>
<p>computer use とは、エージェントにコンピューターを操作させることです。画面を見て、マウスを動かし、
クリックし、文字を入力します。クリックすること自体は簡単です。難しいのは、正しいものをクリックする
ことです。画面に「保存」ボタンがあるなら、エージェントはそれがどこにあり、本当にボタンなのか、今
押せる状態なのかを知る必要があります。</p>
<p>よく使われる方法は、おおまかに四つあります。</p>
<ol class="ways">
<li>
<p><strong>1. スクリーンショットを見て、座標を推測する。</strong>エージェントは一手ごとに
スクリーンショットを撮り、モデルが画像からボタンの位置を判断して x と y を返します。マウスをそこへ
動かしてクリックし、もう一度スクリーンショットで確かめます。</p>
<p><em>長所：</em>最も汎用的です。画面に映っていれば、ゲームや独自に描画された UI も含めて、どんな
アプリでも操作できます。</p>
<p><em>短所：</em>一手ごとに画像を一枚送るので、トークンのコストが高く、時間もかかります。座標は推測
なので、ボタンが小さいときや解像度、拡大率が違うときによく外れます。モデルが見ているのはピクセル
なので、ボタンとボタンに似た画像の区別がつかず、ボタンがグレーアウトしているかどうかもわかりません。
クリックには本物のカーソルを動かす必要があり、エージェントが動いている間、そのコンピューターは
使えません。</p>
<p><em>例：</em>Anthropic の {a(ANTHROPIC_CU, "computer use ツール")}はこの方式です。Claude は
スクリーンショットを受け取り、<code>left_click</code> などの操作を、スクリーンショットのピクセル単位の
[x, y] とともに返し、それを実行するのは利用者側のコードです。ドキュメントには、対象がとても小さいと
クリックが近くに落ちても外れることがあると書かれ、zoom で拡大して確かめる方法が勧められています。
OpenAI の {a(OPENAI_CU, "computer use ツール")}は Computer-Using Agent というモデル
（{a(OPENAI_CUA, "CUA")}）にもとづき、同じくスクリーンショットを見て、x と y 付きのマウスとキーボードの
操作を返します。スクリーンショットは画像入力として数えられます。OpenAI は、モデルがコード
（Playwright や PyAutoGUI）を書いて UI を操作する方式も用意しています。</p>
</li>
<li>
<p><strong>2. スクリーンショットに番号を付けてから、モデルに選ばせる（set-of-mark とも呼ばれます）。</strong>
まず別の視覚モデルで画面上の要素を検出し、枠で囲んで番号を振ります。エージェントは「7 番を押す」と
答えます。</p>
<p><em>長所：</em>モデルが自分で座標を計算しなくてよいので、外れることがずっと少なくなります。</p>
<p><em>短所：</em>やはり一手ごとに画像を送り、さらに検出モデルが一つ増えます。検出が漏れたり枠を
間違えたりすれば、エージェントもそのまま間違えます。押せるか、今の値は何か、といった要素の状態も
わかりません。</p>
<p><em>例：</em>この考え方は {a(SOM, "Set-of-Mark")} の論文から来ています。既存のセグメンテーション
モデルで画像を領域に分け、番号や枠を重ね、印の付いた画像を見てモデルに答えさせるものです。
Microsoft の {a(OMNIPARSER, "OmniParser")} はこれをスクリーンショットに使います。検出モデルが操作
できる領域を見つけ、説明モデルが各要素の役割を書き、スクリーンショットを構造化された要素の一覧に
変えます。</p>
</li>
<li>
<p><strong>3. アプリ自身の API やスクリプトを使う。</strong>たとえば AppleScript で Finder にフォルダを
開かせたり、コマンドラインツールを使ったりします。</p>
<p><em>長所：</em>最も正確で、画面がいりません。</p>
<p><em>短所：</em>アプリごとにやり方が違い、こうした仕組みを持たないアプリも多く、エージェントは
アプリごとに使い方を先に知っておく必要があります。</p>
<p><em>例：</em>Apple の {a(APPLESCRIPT, "AppleScript")} は、スクリプトに対応した Mac アプリと macOS の
一部を直接操作できます。スクリプトに対応していないアプリには使えません。</p>
</li>
<li>
<p><strong>4. アクセシビリティツリーを読む。</strong>OS には、もともとスクリーンリーダーのための仕組みが
あります。macOS の {a(AX_API, "Accessibility API")}、Windows の {a(UIA, "UI Automation")}、Linux の
{a(ATSPI, "AT-SPI")} で、Web ページにもブラウザーの{a(WEB_AX, "アクセシビリティツリー")}があります。
ボタン、入力欄、メニューを、ロール、ラベル、今の値、操作できるかどうか、画面上の正確な位置とともに、
一本のツリーとして表します。</p>
<p><em>長所：</em>返ってくるのはテキストなので、安くて速いです。種類、名前、状態はシステムが直接
教えてくれます。位置は正確です。要素ごとに ref を付けられ、あとで「この ref を押す」と指示でき、
カーソルを動かす必要すらありません。</p>
<p><em>短所：</em>アプリがきちんと対応しているかどうかに左右されます。独自に描画された UI、canvas、
ゲームは、ツリーが空のことがよくあります。「アクセシビリティ」の権限が必要です。UI が複雑だとツリーが
大きくなるので、深さとノード数に上限が要ります。画面が変われば古い ref は使えなくなり、読み直す必要が
あります。</p>
<p><em>例：</em>Vercel の {a(AGENT_DESKTOP, "Agent Desktop")} はこの方法をとっています。
デスクトップアプリのアクセシビリティツリーを読んで JSON で返し、エージェントが操作できる要素ごとに
ref を付けます。ref による操作ではポインターを動かさず、フォーカスも奪いません。macOS、Windows、
Linux に対応しています。</p>
</li>
</ol>
{{cmp_table}}
{{fig_aim}}

<h3>アクセシビリティツリーを選んだ理由</h3>
<p>OpenAB Computer のようにエージェントが遠くにいる場合、いちばんコストがかかるのは、
スクリーンショットを何度も行き来させることです。アクセシビリティツリーを使うと、一手が「画像を一枚
送って座標を一回推測する」から「テキストを読んで ref を一つ選ぶ」に変わります。位置を推測しないので、
クリックが外れる問題も解消します。標準的な Mac アプリの多くは、これで十分です。ただ、どんな画面にも
使えるわけではないので、スクリーンショットは残し、三つを組み合わせています。ネイティブアプリは
<code>ui_snapshot</code> でアクセシビリティツリーを読み、Web ページは <code>browser_snapshot</code> で
ブラウザーのアクセシビリティツリーを読み、ツリーに現れないもの（canvas や独自に描画された UI）は
<code>screenshot</code> と <code>mouse</code> に戻ります。</p>

<div class="callout">
<h2>この取り組みのもとになった調査</h2>
<p>今回の取り組みは、私たちがコミュニティ向けに Muse で公開した{a(MUSE, "調査レポート")}から
始まりました。レポートは三つのプロジェクトを比べています。{a(BROWSE, "OpenCode Browse")} は、
自分のマシンにあるログイン済みのブラウザーをエージェントに操作させます。{a(AGENT_DESKTOP, "Vercel Agent Desktop")} は、アクセシビリティツリーを通してエージェントに
デスクトップアプリを操作させます。構造化された JSON を返して要素ごとに ref を付け、ref による
操作ではポインターを動かさず、フォーカスも奪いません。OpenAB Computer は、マシン一台を丸ごと別の
場所のエージェントに貸します。そのリモートのエージェントにとって、コストの大部分はスクリーンショットの
ループから生じている、というのがレポートの指摘です。</p>
<p>私たちは Agent Desktop の長所を取り入れました。ピクセルから推測するのではなく、アクセシビリティ
ツリーを ref 付きの構造化データとして読むことです。これを OpenAB Computer の MCP ツール
<code>ui_snapshot</code> にしました。リモートのエージェントは、ブラウザーだけでなくネイティブアプリも
構造化されたテキストとして読めるようになりました。</p>
</div>

<h2>スクリーンショットのループでは足りなかった理由</h2>
<p>これまで、OpenAB Computer で Mac を操作するエージェントはこう動いていました。スクリーンショットを
撮り、ボタンの位置を推測し、<code>mouse</code> でクリックし、もう一度スクリーンショットで確かめる。</p>
<p>コミュニティのユーザー {a(TTMUSE, "ttmuse")} さんが、{a(ISSUE67, "issue #67")} でこのループの
コストを書いてくれました。この方は OpenAB Computer を毎日、自宅の Mac を動かすクラウドの
エージェントの手として使っています。一手ごとに画像のトークンがかかり、小さな対象は外れ、
エージェントが動いている間は本物のカーソルを取られてしまう、というものです。</p>
<p>この issue は、本当に必要とする人を待っていました。このコメントで実際に必要な人がいると
わかったので、優先度を上げ、macOS から取りかかりました。</p>
{{fig_loop}}

<h2>Agent Desktop から学んだこと</h2>
<p>コードを書く前に、Vercel Labs の {a(AGENT_DESKTOP, "Agent Desktop")} をじっくり読みました。
README、コンセプトの文書、そして macOS のコードです。Agent Desktop はデスクトップアプリの
アクセシビリティツリーを読んで JSON で返し、エージェントが操作できる要素ごとに ref を付けます。
そのうち三つの考え方が私たちの計画を形づくりました。最初の二つは <code>ui_snapshot</code> に
入り、三つ目は 0.10.0 で <code>ui_action</code> としてリリースしました。</p>
<ul>
<li><strong>画像ではなく構造化されたテキスト。</strong>モデルが読むのはロール、名前、値です。
ピクセルの中からボタンを探す必要はありません。</li>
<li><strong>要素ごとの ref は、一回のスナップショットのもの。</strong>Agent Desktop の ref は、
それを作ったスナップショットに属します。UI が変われば、古い ref や曖昧な ref は推測せずに
拒否され、エージェントは新しいスナップショットを撮ります。</li>
<li><strong>ポインターを使わない操作（第 2 段階、0.10.0 でリリース）。</strong>Agent Desktop の ref による操作はアクセシビリティ
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
{{fig_tree}}
<p>以下は、Apple シリコンの Mac で Finder のウィンドウを一つも開いていないときに撮った、実際の
スナップショットです。この場合のウィンドウはデスクトップそのもので、中の二つの画像は
マウントされた二台のドライブのアイコンです。ツールはモデル向けのテキスト版を返します。</p>
<pre><code>{{text}}</code></pre>
<p>同じツリーの JSON（抜粋。一部のフィールドは省いています）：</p>
<pre><code>{{json}}</code></pre>
<p>この一回の実行では、四つのノードを 46 ms で読みました。ドライブ名はここでは一般的な名前に置き換えています。
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
<li><strong>ref による操作は 0.10.0 からです。</strong>それまで OpenAB Computer は読むだけでした。
Agent Desktop は以前から、ref でクリック、入力、値の設定、フォーカスの移動ができ、ポインターも
動かしません。0.10.0 からは <code>ui_action</code> も、ref で押す、値を設定する、フォーカスを移す
操作をカーソルを動かさずに行います。ドラッグ、ジェスチャー、独自に描画された内容は今も
<code>mouse</code> を使うので、その場合は本物のカーソルが動きます。</li>
<li><strong>ref。</strong>0.10.0 から、ツールは直近四回のスナップショットを五分間保持します。
操作の前に、要素がまだあり、ロールが同じで、同じウィンドウの中にあることを確かめ、古い ref は
代わりを推測せずに拒否します。Agent Desktop は ref ごとに要素を特定するための情報を保存し、
操作の前に同じ要素であることを確かめます。</li>
<li><strong>プラットフォーム。</strong>OpenAB Computer がツリーを読めるのは今のところ macOS だけです。
Agent Desktop は macOS、Windows、Linux に対応しています。</li>
<li><strong>形。</strong><code>ui_snapshot</code> はリモートの MCP サーバーにあるツールの一つで、
別のマシンのエージェントが使います。Agent Desktop はローカルで、CLI、C ライブラリー、または
stdio の MCP サーバーとして動きます。</li>
</ul>

<h2>第 2 段階をリリース：0.10.0 の ui_action</h2>
<p>第 2 段階は <code>ui_action</code> で、{a(REL10, "OpenAB Computer 0.10.0")} でリリースしました。
<code>snapshot_id</code> と <code>ref</code> を渡すと、アクセシビリティ API を通して、ボタンを押す、
入力欄に値を設定する、フォーカスを移す、メニューを開く、確定する、キャンセルする、値を上げ下げする、
といった操作をカーソルを動かさずに行います。カーソルを取られる問題を解消するのはこの部分です。
<code>ui_snapshot</code> に <code>include_menu_bar</code> を付ければ、メニューバーの項目にも ref が
付きます。スイッチボード経由では、パスワード欄への値の設定は、所有者が有効にしない限り拒否されます。</p>
{{fig_action}}
<p>次は AT-SPI を使った Linux 版です。日程はまだ決まっていません。issue #67 は開いたままにして
追いかけます。</p>

<p class="outro">試すには、{a(REL10, "OpenAB Computer 0.10.0")} に更新してアクセシビリティ権限を与え、
<code>owner</code> プロファイルのエージェントから <code>ui_snapshot</code>、続けて
<code>ui_action</code> を呼んでください。</p>
""",
            ),
            "ko": dict(
                title="OpenAB Computer가 이제 macOS 접근성 트리를 읽습니다",
                desc="원격 데스크톱에서 에이전트는 어떻게 정확히 그 버튼을 누를까요? "
                     "OpenAB Computer 0.9.0에 Mac 앱의 접근성 트리를 JSON으로 돌려주는 MCP 도구 "
                     "ui_snapshot이 추가됐습니다. 무엇을 돌려주는지, Vercel의 Agent Desktop에서 무엇을 "
                     "배웠는지, 아직 무엇이 빠져 있는지.",
                og=(["OpenAB Computer가 이제", "macOS 접근성 트리를 읽습니다."],
                    "0.9.0의 ui_snapshot: Mac 앱 화면을 이미지 대신 JSON으로"),
                og_alt="OpenAB 개발 노트: OpenAB Computer가 이제 macOS 접근성 트리를 읽습니다",
                byline="2026-11-09 · OpenAB Computer 0.9.0",
                body=f"""
<p class="hook">에이전트에게 원격 컴퓨터 데스크톱의 어떤 앱에 있는 버튼 하나를 마우스로 눌러 달라고 할 때,
에이전트가 실제로 어떻게 정확히 그 버튼을 누르는지 궁금했던 적이 있나요?</p>

<p class="lede">OpenAB Computer 0.9.0에 MCP 도구 <code>ui_snapshot</code>이 추가됐습니다. Mac 앱의
접근성 트리를 읽어 JSON으로 돌려줍니다. 이제 에이전트는 창 안의 버튼, 입력란, 레이블을 화면 위
위치와 함께 텍스트로 받습니다. 스크린샷을 보고 짐작할 필요가 없습니다.</p>

<h2>에이전트는 어떻게 맞는 버튼을 누를까요?</h2>
<p>computer use는 에이전트가 컴퓨터를 다루게 하는 것입니다. 화면을 보고, 마우스를 움직이고, 클릭하고,
타이핑합니다. 클릭 자체는 쉽습니다. 어려운 것은 맞는 대상을 클릭하는 일입니다. 화면에 "저장" 버튼이
있다면, 에이전트는 그것이 어디 있는지, 정말 버튼인지, 지금 누를 수 있는지를 알아야 합니다.</p>
<p>흔히 쓰는 방법은 크게 네 가지입니다.</p>
<ol class="ways">
<li>
<p><strong>1. 스크린샷을 보고 좌표를 짐작하기.</strong> 에이전트는 단계마다 스크린샷을 찍고, 모델이
이미지에서 버튼 위치를 판단해 x, y를 돌려줍니다. 마우스를 그 위치로 옮겨 클릭한 뒤, 다시 스크린샷을
찍어 확인합니다.</p>
<p><em>장점:</em> 가장 범용적입니다. 화면에 보이기만 하면 게임이나 직접 그린 UI를 포함해 어떤 앱이든
다룰 수 있습니다.</p>
<p><em>단점:</em> 단계마다 이미지를 한 장씩 보내므로 토큰 비용이 크고 느립니다. 좌표는 짐작이라서
버튼이 작거나 해상도, 배율이 다르면 자주 빗나갑니다. 모델이 보는 것은 픽셀이라 버튼과 버튼처럼 생긴
그림을 구분하지 못하고, 버튼이 비활성화되어 있는지도 모릅니다. 클릭하려면 실제 커서를 움직여야 하므로
에이전트가 일하는 동안 그 컴퓨터를 쓸 수 없습니다.</p>
<p><em>예:</em> Anthropic의 {a(ANTHROPIC_CU, "computer use 도구")}가 이렇게 동작합니다. Claude는
스크린샷을 받고 <code>left_click</code> 같은 동작을 스크린샷 픽셀 단위의 [x, y]와 함께 돌려주며, 그
동작은 사용자 쪽 코드가 실행합니다. 문서에는 대상이 아주 작으면 클릭이 맞는 영역에 떨어져도 대상을
놓칠 수 있다고 적혀 있고, zoom 동작으로 확대해 확인하라고 권합니다. OpenAI의
{a(OPENAI_CU, "computer use 도구")}는 Computer-Using Agent 모델({a(OPENAI_CUA, "CUA")})을 바탕으로
하며, 마찬가지로 스크린샷을 보고 x, y가 담긴 마우스와 키보드 동작을 돌려줍니다. 스크린샷은 이미지
입력으로 계산됩니다. OpenAI는 모델이 코드(Playwright나 PyAutoGUI)를 써서 UI를 다루는 방식도
제공합니다.</p>
</li>
<li>
<p><strong>2. 스크린샷에 먼저 번호를 붙이고 모델에게 고르게 하기(흔히 set-of-mark라고
부릅니다).</strong> 먼저 다른 비전 모델로 화면의 요소를 탐지해 테두리를 두르고 번호를 매깁니다.
그러면 에이전트는 "7번을 눌러"라고 답합니다.</p>
<p><em>장점:</em> 모델이 좌표를 직접 계산하지 않아도 되므로 빗나가는 일이 훨씬 줄어듭니다.</p>
<p><em>단점:</em> 여전히 단계마다 이미지를 보내고, 탐지 모델이 하나 더 붙습니다. 탐지가 요소를 놓치거나
테두리를 잘못 그리면 에이전트도 그대로 틀립니다. 누를 수 있는지, 현재 값이 무엇인지 같은 요소의
상태도 모릅니다.</p>
<p><em>예:</em> 이 방식은 {a(SOM, "Set-of-Mark")} 논문에서 나왔습니다. 기존 분할(segmentation)
모델로 이미지를 영역으로 나누고 숫자나 테두리를 겹친 뒤, 모델이 표시된 이미지를 보고 답하게 합니다.
Microsoft의 {a(OMNIPARSER, "OmniParser")}는 이를 스크린샷에 적용합니다. 탐지 모델이 조작할 수 있는
영역을 찾고, 설명 모델이 각 요소의 역할을 적어, 스크린샷을 구조화된 요소 목록으로 바꿉니다.</p>
</li>
<li>
<p><strong>3. 앱 자체의 API나 스크립트 쓰기.</strong> 예를 들어 AppleScript로 Finder에게 폴더를
열게 하거나, 명령줄 도구를 씁니다.</p>
<p><em>장점:</em> 가장 정확하고 화면이 필요 없습니다.</p>
<p><em>단점:</em> 앱마다 방식이 다르고, 이런 인터페이스가 없는 앱도 많으며, 에이전트가 앱마다 쓰는 법을
먼저 알아야 합니다.</p>
<p><em>예:</em> Apple의 {a(APPLESCRIPT, "AppleScript")}는 스크립트를 지원하는 Mac 앱과 macOS 일부를
직접 제어합니다. 스크립트를 지원하지 않는 앱에는 쓸 수 없습니다.</p>
</li>
<li>
<p><strong>4. 접근성 트리 읽기.</strong> 운영체제에는 원래 화면 낭독기를 위한 인터페이스가 있습니다.
macOS의 {a(AX_API, "Accessibility API")}, Windows의 {a(UIA, "UI Automation")}, Linux의
{a(ATSPI, "AT-SPI")}이고, 웹 페이지에는 브라우저의 {a(WEB_AX, "접근성 트리")}가 있습니다. 버튼,
입력란, 메뉴를 역할, 레이블, 현재 값, 조작할 수 있는지, 화면 위 정확한 위치와 함께 하나의 트리로
나타냅니다.</p>
<p><em>장점:</em> 돌려받는 것이 텍스트라 저렴하고 빠릅니다. 종류, 이름, 상태를 시스템이 직접
알려 줍니다. 위치가 정확합니다. 요소마다 ref를 붙일 수 있어서 나중에 "이 ref를 눌러"라고 할 수 있고,
커서를 움직일 필요도 없습니다.</p>
<p><em>단점:</em> 앱이 얼마나 잘 지원하느냐에 달려 있습니다. 직접 그린 UI, canvas, 게임은 트리가 비어
있는 경우가 많습니다. 손쉬운 사용 권한이 필요합니다. UI가 복잡하면 트리가 커지므로 깊이와 노드 수를
제한해야 합니다. 화면이 바뀌면 이전 ref는 쓸 수 없게 되어 다시 읽어야 합니다.</p>
<p><em>예:</em> Vercel의 {a(AGENT_DESKTOP, "Agent Desktop")}이 이 방식을 씁니다. 데스크톱 앱의
접근성 트리를 읽어 JSON으로 돌려주고, 에이전트가 조작할 수 있는 요소마다 ref를 붙입니다. ref로
동작할 때는 포인터를 움직이지 않고 포커스도 가져가지 않습니다. macOS, Windows, Linux를 지원합니다.</p>
</li>
</ol>
{{cmp_table}}
{{fig_aim}}

<h3>접근성 트리를 고른 이유</h3>
<p>OpenAB Computer처럼 에이전트가 멀리 있는 경우, 가장 비싼 부분은 스크린샷을 계속 주고받는
일입니다. 접근성 트리를 쓰면 한 단계가 "이미지 한 장 보내고 좌표 한 번 짐작하기"에서 "텍스트를 읽고
ref 하나 고르기"로 바뀝니다. 위치를 짐작하지 않으니 클릭이 빗나가는 문제도 해결됩니다. 대부분의 표준
Mac 앱에는 이것으로 충분합니다. 다만 모든 화면을 다룰 수는 없어서 스크린샷은 그대로 두고 세 가지를
함께 씁니다. 네이티브 앱은 <code>ui_snapshot</code>으로 접근성 트리를 읽고, 웹 페이지는
<code>browser_snapshot</code>으로 브라우저의 접근성 트리를 읽고, 트리에 보이지 않는 것(canvas, 직접 그린
UI)은 <code>screenshot</code>과 <code>mouse</code>로 돌아갑니다.</p>

<div class="callout">
<h2>이 작업의 바탕이 된 리서치</h2>
<p>이번 작업은 우리가 커뮤니티를 위해 Muse에 공개한 {a(MUSE, "리서치 보고서")}에서
시작했습니다. 보고서는 세 프로젝트를 비교합니다. {a(BROWSE, "OpenCode Browse")}는 에이전트가 내
기기에서 로그인된 브라우저를 다루게 합니다. {a(AGENT_DESKTOP, "Vercel Agent Desktop")}은
에이전트가 접근성 트리를 통해 데스크톱 앱을 다루게 합니다. 구조화된 JSON을 돌려주고 요소마다 ref를
붙이며, ref로 동작할 때는 포인터를 움직이지 않고 포커스도 가져가지 않습니다. OpenAB Computer는
기기 한 대를 통째로 다른 곳의 에이전트에게 빌려줍니다. 보고서는 그 원격 에이전트에게 주된 비용이
스크린샷 루프라고 짚었습니다.</p>
<p>우리는 Agent Desktop의 장점을 가져왔습니다. 픽셀로 짐작하는 대신 접근성 트리를 ref가 붙은
구조화된 데이터로 읽는 방식입니다. 이것을 OpenAB Computer의 MCP 도구 <code>ui_snapshot</code>으로
만들었습니다. 이제 원격 에이전트는 브라우저뿐 아니라 네이티브 앱도 구조화된 텍스트로 읽을 수
있습니다.</p>
</div>

<h2>스크린샷 루프로는 부족했던 이유</h2>
<p>지금까지 OpenAB Computer로 Mac을 다루는 에이전트는 이렇게 움직였습니다. 스크린샷을 찍고,
버튼 위치를 짐작하고, <code>mouse</code>로 클릭하고, 다시 스크린샷을 찍어 확인합니다.</p>
<p>커뮤니티 사용자 {a(TTMUSE, "ttmuse")} 님이 {a(ISSUE67, "issue #67")}에 이 루프의 비용을
적어 주었습니다. 이 사용자는 OpenAB Computer를 매일, 집에 있는 Mac을 움직이는 클라우드 에이전트의
손으로 씁니다. 단계마다 이미지 토큰이 들고, 작은 대상은 빗나가고, 에이전트가 일하는 동안 실제
커서를 빼앗긴다는 내용이었습니다.</p>
<p>이 issue는 정말 필요로 하는 사람을 기다리고 있었습니다. 그 댓글로 실제로 필요한 사람이 있다는
것을 알게 되어 우선순위를 올리고 macOS부터 시작했습니다.</p>
{{fig_loop}}

<h2>Agent Desktop에서 배운 것</h2>
<p>코드를 쓰기 전에 Vercel Labs의 {a(AGENT_DESKTOP, "Agent Desktop")}을 꼼꼼히 읽었습니다.
README, 개념 문서, 그리고 macOS 코드입니다. Agent Desktop은 데스크톱 앱의 접근성 트리를 읽어
JSON으로 돌려주고, 에이전트가 조작할 수 있는 요소마다 ref를 붙입니다. 그중 세 가지 생각이
우리 계획의 모양을 정했습니다. 앞의 두 가지는 <code>ui_snapshot</code>에 들어갔고, 세 번째는
0.10.0에서 <code>ui_action</code>으로 출시했습니다.</p>
<ul>
<li><strong>이미지 대신 구조화된 텍스트.</strong> 모델은 역할, 이름, 값을 읽습니다. 픽셀 속에서
버튼을 찾지 않아도 됩니다.</li>
<li><strong>요소마다 하나의 ref, 한 번의 스냅샷에서.</strong> Agent Desktop의 ref는 그것을 만든
스냅샷에 속합니다. UI가 바뀌면 오래되었거나 모호한 ref는 짐작하지 않고 거부되고, 에이전트는 새
스냅샷을 찍습니다.</li>
<li><strong>포인터 없이 조작하기(2단계, 0.10.0에서 출시).</strong> Agent Desktop의 ref 동작은 접근성 API를 거치며
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
{{fig_tree}}
<p>아래는 Apple 실리콘 Mac에서 Finder 창을 하나도 열지 않은 상태로 찍은 실제 스냅샷입니다. 이때 창은
데스크톱 자체이고, 그 안의 두 이미지는 마운트된 드라이브 두 개의 아이콘입니다. 도구는 모델이
읽을 텍스트 형식을 돌려줍니다.</p>
<pre><code>{{text}}</code></pre>
<p>같은 트리의 JSON(발췌, 일부 필드는 생략):</p>
<pre><code>{{json}}</code></pre>
<p>이번 한 번의 실행에서는 노드 네 개를 46 ms에 읽었습니다. 드라이브 이름은 여기서 일반적인 이름으로 바꿨습니다.
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
<li><strong>ref로 조작하기는 0.10.0부터입니다.</strong> 그전까지 OpenAB Computer는 읽기만 했습니다.
Agent Desktop은 이미 ref로 클릭, 입력, 값 설정, 포커스 이동을 하고 포인터도 움직이지 않습니다.
0.10.0부터는 <code>ui_action</code>도 ref로 누르기, 값 설정, 포커스 이동을 커서를 움직이지 않고
합니다. 드래그, 제스처, 직접 그린 내용은 여전히 <code>mouse</code>를 쓰고, 이때는 실제 커서가
움직입니다.</li>
<li><strong>ref.</strong> 0.10.0부터 도구는 최근 스냅샷 네 개를 5분 동안 보관합니다. 동작하기 전에
요소가 아직 있는지, 역할이 같은지, 같은 창 안에 있는지 확인하고, 오래된 ref는 대신할 요소를 짐작하지
않고 거부합니다. Agent Desktop은 ref마다 요소를 식별할 정보를 저장해 두고, 동작하기 전에 같은
요소인지 확인합니다.</li>
<li><strong>플랫폼.</strong> OpenAB Computer가 트리를 읽는 곳은 아직 macOS뿐입니다. Agent
Desktop은 macOS, Windows, Linux를 지원합니다.</li>
<li><strong>형태.</strong> <code>ui_snapshot</code>은 원격 MCP 서버의 도구 하나로, 다른 기기의
에이전트가 씁니다. Agent Desktop은 로컬에서 CLI, C 라이브러리, 또는 stdio MCP 서버로
실행됩니다.</li>
</ul>

<h2>2단계 출시: 0.10.0의 ui_action</h2>
<p>2단계는 <code>ui_action</code>이며 {a(REL10, "OpenAB Computer 0.10.0")}에서 출시했습니다.
<code>snapshot_id</code>와 <code>ref</code>를 넘기면 접근성 API를 통해 버튼 누르기, 입력란 값 설정,
포커스 이동, 메뉴 열기, 확인, 취소, 값 올리기와 내리기를 커서를 움직이지 않고 합니다. 커서를 빼앗기는
문제를 끝내는 것이 이 부분입니다. <code>ui_snapshot</code>에 <code>include_menu_bar</code>를 주면
메뉴 막대 항목에도 ref가 붙습니다. 스위치보드를 거칠 때는 소유자가 직접 켜지 않는 한 비밀번호
입력란에 값을 설정하는 것이 거부됩니다.</p>
{{fig_action}}
<p>다음은 AT-SPI 기반의 Linux 버전입니다. 아직 일정은 정해지지 않았고, issue #67을 열어 둔 채
추적합니다.</p>

<p class="outro">써 보려면 {a(REL10, "OpenAB Computer 0.10.0")}으로 업데이트하고 손쉬운 사용 권한을 준 뒤,
<code>owner</code> 프로필의 에이전트에서 <code>ui_snapshot</code>을 호출하고 이어서
<code>ui_action</code>을 호출하세요.</p>
""",
            ),
        },
    ),
]
