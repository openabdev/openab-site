"""Dev note 2: ui_action in OpenAB Computer 0.10.0, how we test it, and what it saves. Four languages.

Imported by notes.py, which puts it first in NOTES (newest first). The test facts come from PR #96
and its CI; the performance numbers come from a measured run (10 trials per approach on an M4 Mac
mini through the switchboard; raw CSV/JSON and the script are kept outside this repo). Figures and
the table come from figures_ui_action.py ({fig_press}, {fig_cmp}, {perf_table}).
"""

REL10 = "https://github.com/openabdev/openab-computer/releases/tag/v0.10.0"
PR96 = "https://github.com/openabdev/openab-computer/pull/96"
ISSUE102 = "https://github.com/openabdev/openab-computer/issues/102"
VISION = "https://platform.claude.com/docs/en/build-with-claude/vision"
NOTE1 = "../accessibility-tree/"   # same language, sibling note
SENTENCE = "<code>The quick brown fox jumps over the lazy dog.</code>"


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
            title="OpenAB Computer 0.10.0 now supports full accessibility-tree actions: 4.7× faster "
                  "and 55% fewer tokens in our test",
            dek="Results from one TextEdit task done two ways, 10 runs each, on an M4 Mac mini.",
            desc="Phase 1 could read the macOS accessibility tree; OpenAB Computer 0.10.0 adds "
                 "ui_action to act on it. How we test the whole operation, and what it saves "
                 "against a screenshot loop: on one TextEdit task it was 4.7× faster (0.36 s vs 1.70 s) "
                 "and used 55% fewer input tokens (1,435 vs 3,165).",
            og=(["OpenAB Computer 0.10.0 now supports", "full accessibility-tree actions:",
                 "4.7× faster, 55% fewer tokens"],
                "One TextEdit task, two ways, 10 runs each, on an M4 Mac mini"),
            og_alt="OpenAB dev note: OpenAB Computer 0.10.0 now supports full accessibility-tree actions, "
                   "4.7× faster and 55% fewer tokens in our test",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="lede">The {a(NOTE1, "previous dev note")} introduced <code>ui_snapshot</code>. That was
phase 1, in OpenAB Computer 0.9.0: an agent could read a Mac app's accessibility tree, but it could
not act on it. {a(REL10, "OpenAB Computer 0.10.0")} adds <code>ui_action</code>, which acts on the
tree. Given a <code>snapshot_id</code> and a <code>ref</code> from a snapshot, it can press,
set_value, focus, show_menu, confirm or cancel, and the cursor does not move.</p>
{{fig_press}}
<p class="hook">So how do we test the whole operation, from reading the tree to acting on it and
checking the result?</p>

<h2>How we test it</h2>

<h3>Unit tests with a fake accessibility provider</h3>
<p>CI machines have no screen, so the unit tests never touch a real app. They run against a fake
accessibility provider that stands in for windows, buttons and text fields, and they check each
rule of <code>ui_action</code>:</p>
<ul>
<li>A ref only works with the snapshot it came from. An expired snapshot, one pushed out of the
cache, or an unknown ref is refused.</li>
<li>If the element changed after the snapshot (it vanished, changed role, belongs to another
process or left its window), the ref is stale. The tool refuses it and asks for a new snapshot; it
never picks a lookalike.</li>
<li>An action the element does not support is refused before anything happens, with the list of
actions it does support.</li>
<li>A password field's value is never read back, logged or returned.</li>
<li>The app is not brought to the front unless the caller passes <code>activate: true</code>.</li>
<li>Only the <code>owner</code> profile can call <code>ui_action</code>.</li>
</ul>
<p>{a(PR96, "PR #96")} added 52 of these tests. On an M4 Mac mini the full <code>swift test</code>
run passed 256 tests with 0 failures, and every CI check on the PR passed.</p>

<h3>A live end-to-end run on an M4 Mac mini</h3>
<p>Unit tests show the rules are right. The live run shows the whole thing works on a real app. An
agent drove an M4 Mac mini through the switchboard, over the same network path a remote agent
uses:</p>
<ol>
<li>Read the mouse position.</li>
<li>Open TextEdit with a new document.</li>
<li>Call <code>ui_snapshot</code> and find the text area (<code>AXTextArea</code>) and its ref.</li>
<li>Call <code>ui_action</code> with focus on that ref, then set_value with a sentence.</li>
<li>Call <code>ui_snapshot</code> again and check that the text area's value is that
sentence.</li>
<li>Read the mouse position again and compare.</li>
</ol>
<p>Both readings were the same point: the text went in, and the cursor did not move. The
performance run below repeated the tree steps 10 more times, and each time the text landed and the
pointer stayed put.</p>
<p>Every change is also reviewed by two independent AI reviewers running different models, and it
merges only when both approve the same commit.</p>

<h2>How much faster it is</h2>
<p>We timed one task done two ways, 10 times each: type {SENTENCE} (44 characters) into a new, empty
TextEdit document and confirm it.</p>
<ul>
<li><strong>A) Screenshot loop:</strong> <code>screenshot</code> → <code>mouse</code> click on the
text area → <code>key</code> type → <code>screenshot</code> to check.</li>
<li><strong>B) Tree path:</strong> <code>ui_snapshot</code> → <code>ui_action</code> focus →
<code>ui_action</code> set_value → <code>ui_snapshot</code> to check.</li>
</ul>
{{fig_cmp}}
{{perf_table}}
<p>On this task, B used about 55% fewer input tokens than A on a standard model (1,435 vs 3,165)
and about 74% fewer on a high-resolution model (1,435 vs 5,427). It finished in 0.36 s against
1.70 s, about 4.7× faster, and the pointer never moved.</p>
<p>Most of A's time goes to typing 44 keystrokes (877 ms) and to the two screenshots, about 500 KB
each, coming back through the switchboard. Each <code>ui_action</code> call took about 67 ms end to
end, mostly the network round trip.</p>
<p class="cmp-note">How tokens were counted: images with the formula in
{a(VISION, "Anthropic's vision guide")}. The image is shrunk to the model's limits, then costs
⌈width/28⌉ × ⌈height/28⌉ tokens. A standard model (1,568 px long edge) shrinks a 1920×1080
screenshot to 1456×819, about 1,560 tokens; a high-resolution model (2,576 px) keeps it at
1920×1080, about 2,691 tokens. Text at about 4 characters per token; no tokenizer was run. Only
what the model would see is counted, not tool definitions or the model's own output.</p>
<p class="cmp-note">Conditions: an M4 Mac mini (16 GB, macOS 15.7) with one 1920×1080 display,
running OpenAB Computer 0.10.0. The agent reached it over HTTPS on the tailnet through the
switchboard, so every call pays that round trip. 10 runs per approach, alternating A and B, after
one discarded warm-up pair. Only the four tool calls are timed. A clicked at a point taken from the
known window position; a real model would read it off the first screenshot. These numbers come
from one machine and one task, and they leave out the time a model spends reasoning about each
screenshot or snapshot.</p>

<h2>Next</h2>
<p>Linux (AT-SPI) support for <code>ui_snapshot</code> and <code>ui_action</code> is deferred as p3
in {a(ISSUE102, "issue #102")}. For custom-drawn UI with no accessibility node,
<code>screenshot</code> and <code>mouse</code> are still there.</p>

<p class="outro">Previous note:
{a(NOTE1, "OpenAB Computer can now read the macOS accessibility tree")}.</p>
""",
        ),
        "zh": dict(
            title="OpenAB Computer 0.10.0 開始支援完整的 accessibility tree 操作：實測快 4.7 倍，token 省 55%",
            dek="在一台 M4 Mac mini 上，用同一個 TextEdit 任務兩種做法各跑 10 次的結果。",
            desc="第一階段只能讀 macOS 的 accessibility tree，OpenAB Computer 0.10.0 的 ui_action "
                 "讓 agent 可以直接操作它。這篇說明我們怎麼測整個操作過程，以及它比截圖迴圈省多少："
                 "在一個 TextEdit 任務上，快了 4.7 倍（0.36 秒對 1.70 秒），輸入 token 省了 55%（1,435 對 3,165）。",
            og=(["OpenAB Computer 0.10.0 開始支援", "完整的 accessibility tree 操作：", "實測快 4.7 倍，token 省 55%"],
                "一台 M4 Mac mini、同一個 TextEdit 任務，兩種做法各跑 10 次"),
            og_alt="OpenAB 開發筆記：OpenAB Computer 0.10.0 開始支援完整的 accessibility tree 操作，實測快 4.7 倍，token 省 55%",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="lede">{a(NOTE1, "上一篇開發筆記")}介紹了 <code>ui_snapshot</code>。那是第一階段（OpenAB Computer 0.9.0）：agent 讀得到 Mac app 的 accessibility tree，但還不能操作。這篇搭配 {a(REL10, "OpenAB Computer 0.10.0")} 的發布，新增的 <code>ui_action</code> 讓 agent 可以直接操作這棵樹：帶著快照的 <code>snapshot_id</code> 和 <code>ref</code>，做 press、set_value、focus、show_menu、confirm 或 cancel，游標不會移動。</p>
{{fig_press}}
<p class="hook">那麼，從讀樹、動手到確認結果，整個操作過程要怎麼測？</p>

<h2>我們怎麼測</h2>

<h3>單元測試：用假的 accessibility 提供者</h3>
<p>CI 機器沒有螢幕，所以單元測試從不碰真的 app，而是跑在一個假的 accessibility 提供者上。它模擬出視窗、按鈕和文字欄位，讓測試逐條檢查 <code>ui_action</code> 的規則：</p>
<ul>
<li>ref 只在產生它的那次快照裡有效。快照過期、被擠出快取，或 ref 不存在，都會被拒絕。</li>
<li>快照之後元素變了（消失、角色改變、換了行程，或離開原本的視窗），這個 ref 就過期了。工具會拒絕，請 agent 重拍快照，不會挑一個長得像的元素代替。</li>
<li>元素不支援的動作，在動手前就拒絕，並列出它支援哪些動作。</li>
<li>密碼欄位的值不會被讀回，也不會寫進紀錄或出現在回應裡。</li>
<li>除非呼叫端傳 <code>activate: true</code>，否則不會把 app 叫到前景。</li>
<li>只有 <code>owner</code> profile 能呼叫 <code>ui_action</code>。</li>
</ul>
<p>{a(PR96, "PR #96")} 新增了 52 個這類測試。在一台 M4 Mac mini 上，整套 <code>swift test</code> 跑了 256 個測試，0 個失敗，PR 上的 CI 檢查也全部通過。</p>

<h3>實機端到端測試：一台 M4 Mac mini</h3>
<p>單元測試確認規則沒錯，實機測試則確認整件事在真的 app 上做得到。我們讓 agent 經過 switchboard 操作一台 M4 Mac mini，走的是遠端 agent 平常用的同一條網路路徑：</p>
<ol>
<li>讀一次滑鼠位置。</li>
<li>打開 TextEdit，開一份新文件。</li>
<li>呼叫 <code>ui_snapshot</code>，在樹裡找到文字區（<code>AXTextArea</code>）和它的 ref。</li>
<li>用 <code>ui_action</code> 對這個 ref 做 focus，再用 set_value 寫入一句話。</li>
<li>再呼叫一次 <code>ui_snapshot</code>，確認文字區的值就是那句話。</li>
<li>再讀一次滑鼠位置，和第一次比對。</li>
</ol>
<p>兩次讀到的是同一個點：文字寫進去了，游標沒有動。下面的效能測試又把 tree 路徑跑了 10 次，每次文字都寫進文件，游標也都沒動。</p>
<p>此外，每個變更都交給兩個使用不同模型的獨立 AI 審查者，兩邊都核准同一個 commit 才會合併。</p>

<h2>效能改進有多少</h2>
<p>我們拿同一件事，用兩種方式各做 10 次：在新的空白 TextEdit 文件裡輸入 {SENTENCE}（44 個字元），再確認它寫進去了。</p>
<ul>
<li><strong>A) 截圖迴圈：</strong><code>screenshot</code> → 用 <code>mouse</code> 點文字區 → 用 <code>key</code> 輸入 → 再 <code>screenshot</code> 確認。</li>
<li><strong>B) tree 路徑：</strong><code>ui_snapshot</code> → <code>ui_action</code> focus → <code>ui_action</code> set_value → 再 <code>ui_snapshot</code> 確認。</li>
</ul>
{{fig_cmp}}
{{perf_table}}
<p>在這個任務上，B 用掉的輸入 token 在一般模型上比 A 少約 55%（1,435 對 3,165），在高解析度模型上少約 74%（1,435 對 5,427）。B 花 0.36 秒做完，A 要 1.70 秒，B 約快 4.7 倍，而且游標從頭到尾沒動。</p>
<p>A 的時間主要花在用鍵盤送出 44 個按鍵（877 ms），以及兩張各約 500 KB 的截圖經過 switchboard 傳回來。B 的每次 <code>ui_action</code> 呼叫端到端約 67 ms，大部分是網路往返。</p>
<p class="cmp-note">token 怎麼算：圖片用 {a(VISION, "Anthropic vision 指南")}的公式，先把圖縮到模型的上限內，再算 ⌈寬/28⌉ × ⌈高/28⌉。一般模型（長邊上限 1,568 px）會把 1920×1080 的截圖縮成 1456×819，約 1,560 個 token；高解析度模型（長邊上限 2,576 px）不縮，約 2,691 個 token。文字以約 4 個字元算 1 個 token，沒有跑 tokenizer。只算模型實際會看到的內容，不含工具定義和模型自己的輸出。</p>
<p class="cmp-note">測試條件：一台 M4 Mac mini（16 GB、macOS 15.7），一個 1920×1080 的螢幕，裝的是 OpenAB Computer 0.10.0。agent 經 tailnet 用 HTTPS 連到 switchboard，再轉到這台 Mac mini，每次呼叫都要付這段往返。A、B 各跑 10 次，交錯進行，最前面一組暖身不計。只計四次工具呼叫的時間。A 點擊的座標取自已知的視窗位置，真的模型得先從第一張截圖裡找出來。這些數字來自一台機器、一個任務，也不包含模型看截圖或快照、思考下一步的時間。</p>

<h2>接下來</h2>
<p>Linux（AT-SPI）上的 <code>ui_snapshot</code> 和 <code>ui_action</code> 先延後，列為 p3，記在 {a(ISSUE102, "issue #102")}。沒有 accessibility 節點、自己繪製的介面，還是可以用 <code>screenshot</code> 加 <code>mouse</code>。</p>

<p class="outro">上一篇：{a(NOTE1, "OpenAB Computer 開始支援 macOS 的 accessibility tree")}。</p>
""",
        ),
        "ja": dict(
            title="OpenAB Computer 0.10.0 でアクセシビリティツリーの操作に完全対応：実測で 4.7 倍速く、トークンは 55% 削減",
            dek="M4 Mac mini 1 台で、同じ TextEdit の作業を二つのやり方で 10 回ずつ実行した結果です。",
            desc="第 1 段階は macOS のアクセシビリティツリーを読むだけでした。OpenAB Computer 0.10.0 の "
                 "ui_action でツリーを操作できます。一連の操作をどう試しているか、そしてスクリーンショットの"
                 "繰り返しと比べた差です。TextEdit の作業一つで 4.7 倍速く（0.36 秒対 1.70 秒）、入力トークンは "
                 "55% 少なくなりました（1,435 対 3,165）。",
            og=(["OpenAB Computer 0.10.0 で", "アクセシビリティツリーの", "操作に完全対応：", "実測で 4.7 倍速く、トークン 55% 削減"],
                "M4 Mac mini 1 台、同じ TextEdit の作業を二通りで 10 回ずつ"),
            og_alt="OpenAB 開発ノート：OpenAB Computer 0.10.0 でアクセシビリティツリーの操作に完全対応、実測で 4.7 倍速く、トークンは 55% 削減",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="lede">{a(NOTE1, "前回の開発ノート")}では <code>ui_snapshot</code> を紹介しました。これが第 1 段階（OpenAB Computer 0.9.0）で、エージェントは Mac アプリのアクセシビリティツリーを読めるようになりましたが、操作はまだできませんでした。{a(REL10, "OpenAB Computer 0.10.0")} で加わった <code>ui_action</code> は、このツリーを操作します。スナップショットの <code>snapshot_id</code> と <code>ref</code> を渡せば、press、set_value、focus、show_menu、confirm、cancel ができ、カーソルは動きません。</p>
{{fig_press}}
<p class="hook">では、ツリーを読み、操作し、結果を確かめるまでの一連の流れを、どうやって試すのでしょうか。</p>

<h2>どう試しているか</h2>

<h3>偽のアクセシビリティ提供元を使った単体テスト</h3>
<p>CI のマシンには画面がないので、単体テストは本物のアプリに触れません。ウィンドウやボタン、テキスト欄の代わりをする偽のアクセシビリティ提供元の上で動き、<code>ui_action</code> の規則を一つずつ確かめます。</p>
<ul>
<li>ref は、それが含まれていたスナップショットでだけ使えます。期限切れのスナップショット、キャッシュから押し出されたもの、存在しない ref は拒否されます。</li>
<li>スナップショットのあとで要素が変わった場合（消えた、ロールが変わった、別のプロセスのものになった、元のウィンドウを離れた）、その ref は古くなっています。ツールは拒否してスナップショットの撮り直しを求め、似た要素を代わりに選ぶことはしません。</li>
<li>要素が対応していない操作は、何かする前に拒否し、対応している操作の一覧を返します。</li>
<li>パスワード欄の値は読み戻さず、ログにも応答にも出しません。</li>
<li>呼び出し側が <code>activate: true</code> を渡さない限り、アプリを前面に出しません。</li>
<li><code>ui_action</code> を呼べるのは <code>owner</code> プロファイルだけです。</li>
</ul>
<p>{a(PR96, "PR #96")} でこうしたテストを 52 個加えました。M4 Mac mini での <code>swift test</code> は全 256 個が通って失敗は 0、PR の CI チェックもすべて通りました。</p>

<h3>M4 Mac mini での実機エンドツーエンドテスト</h3>
<p>単体テストは規則が正しいことを、実機テストは本物のアプリで全体が動くことを確かめます。エージェントからスイッチボード経由で M4 Mac mini を操作しました。リモートのエージェントが使うのと同じネットワーク経路です。</p>
<ol>
<li>マウス位置を読む。</li>
<li>TextEdit を開き、新しい書類を作る。</li>
<li><code>ui_snapshot</code> を呼び、ツリーからテキスト領域（<code>AXTextArea</code>）とその ref を見つける。</li>
<li>その ref に <code>ui_action</code> で focus し、続けて set_value で一文を入れる。</li>
<li>もう一度 <code>ui_snapshot</code> を呼び、テキスト領域の値がその一文であることを確かめる。</li>
<li>もう一度マウス位置を読み、最初と比べる。</li>
</ol>
<p>二回の読み取りは同じ点でした。文字は入り、カーソルは動いていません。下の性能測定でもツリーを使う手順をさらに 10 回繰り返し、毎回文字が書類に入り、ポインターは動きませんでした。</p>
<p>また、すべての変更は別々のモデルで動く二つの独立した AI レビュアーが見て、両方が同じコミットを承認したときだけマージします。</p>

<h2>どれだけ速くなったか</h2>
<p>同じ作業を二つのやり方で 10 回ずつ測りました。新しい空の TextEdit 書類に {SENTENCE}（44 文字）を入力し、入ったことを確かめる作業です。</p>
<ul>
<li><strong>A) スクリーンショットの繰り返し：</strong><code>screenshot</code> → <code>mouse</code> でテキスト領域をクリック → <code>key</code> で入力 → <code>screenshot</code> で確認。</li>
<li><strong>B) ツリーを使う：</strong><code>ui_snapshot</code> → <code>ui_action</code> focus → <code>ui_action</code> set_value → <code>ui_snapshot</code> で確認。</li>
</ul>
{{fig_cmp}}
{{perf_table}}
<p>この作業では、B が使った入力トークンは標準モデルで A より約 55% 少なく（1,435 対 3,165）、高解像度モデルでは約 74% 少なくなりました（1,435 対 5,427）。B は 0.36 秒、A は 1.70 秒で終わり、B のほうが約 4.7 倍速く、ポインターも一度も動きませんでした。</p>
<p>A の時間の多くは、44 回のキー入力（877 ms）と、スイッチボードを通って返ってくる約 500 KB のスクリーンショット 2 枚にかかっています。B の <code>ui_action</code> は一回あたり端から端まで約 67 ms で、その大半はネットワークの往復です。</p>
<p class="cmp-note">トークンの数え方：画像は {a(VISION, "Anthropic のビジョンのガイド")}の式を使いました。画像をモデルの上限まで縮めてから ⌈幅/28⌉ × ⌈高さ/28⌉ です。標準モデル（長辺 1,568 px まで）では 1920×1080 のスクリーンショットが 1456×819 に縮み、約 1,560 トークン。高解像度モデル（長辺 2,576 px まで）では縮まず、約 2,691 トークンです。テキストは約 4 文字で 1 トークンとし、トークナイザーは使っていません。数えたのはモデルが実際に見る内容だけで、ツールの定義やモデル自身の出力は含みません。</p>
<p class="cmp-note">条件：M4 Mac mini（16 GB、macOS 15.7）、1920×1080 のディスプレイ 1 枚、OpenAB Computer 0.10.0。エージェントは tailnet 上の HTTPS でスイッチボードにつなぎ、そこから Mac mini に届くので、毎回の呼び出しにこの往復がかかります。やり方ごとに 10 回、A と B を交互に実行し、最初のウォームアップ 1 組は捨てました。計ったのは四回のツール呼び出しだけです。A のクリック位置は既知のウィンドウ位置から決めました。実際のモデルなら最初のスクリーンショットから読み取ります。数字は 1 台のマシンと 1 つの作業から得たもので、モデルがスクリーンショットやスナップショットを見て考える時間は含みません。</p>

<h2>これから</h2>
<p>Linux（AT-SPI）での <code>ui_snapshot</code> と <code>ui_action</code> は、p3 として {a(ISSUE102, "issue #102")} で後回しにしています。アクセシビリティのノードがない独自描画の UI には、今も <code>screenshot</code> と <code>mouse</code> が使えます。</p>

<p class="outro">前回のノート：{a(NOTE1, "OpenAB Computer が macOS のアクセシビリティツリーを読めるようになりました")}。</p>
""",
        ),
        "ko": dict(
            title="OpenAB Computer 0.10.0, 접근성 트리 조작 완전 지원: 실측 4.7배 빠르고 토큰 55% 절약",
            dek="M4 Mac mini 한 대에서 같은 TextEdit 작업을 두 가지 방식으로 10번씩 돌린 결과입니다.",
            desc="1단계는 macOS 접근성 트리를 읽기만 했습니다. OpenAB Computer 0.10.0의 ui_action으로 "
                 "트리를 조작할 수 있습니다. 전체 과정을 어떻게 시험하는지, 그리고 스크린샷 반복과 비교한 "
                 "차이를 정리했습니다. TextEdit 작업 하나에서 4.7배 빨랐고(0.36초 대 1.70초), 입력 토큰은 "
                 "55% 적었습니다(1,435 대 3,165).",
            og=(["OpenAB Computer 0.10.0,", "접근성 트리 조작 완전 지원:", "실측 4.7배 빠르고 토큰 55% 절약"],
                "M4 Mac mini 한 대, 같은 TextEdit 작업을 두 방식으로 10번씩"),
            og_alt="OpenAB 개발 노트: OpenAB Computer 0.10.0, 접근성 트리 조작 완전 지원, 실측 4.7배 빠르고 토큰 55% 절약",
            byline="2026-11-10 · OpenAB Computer 0.10.0",
            body=f"""
<p class="lede">{a(NOTE1, "지난 개발 노트")}에서는 <code>ui_snapshot</code>을 소개했습니다. 그것이
1단계(OpenAB Computer 0.9.0)로, 에이전트가 Mac 앱의 접근성 트리를 읽을 수는 있었지만 조작은 아직
못 했습니다. {a(REL10, "OpenAB Computer 0.10.0")} 릴리스와 함께 나온 <code>ui_action</code>은 이
트리를 직접 조작합니다. 스냅샷의 <code>snapshot_id</code>와 <code>ref</code>를 넘기면 press,
set_value, focus, show_menu, confirm, cancel을 할 수 있고, 커서는 움직이지 않습니다.</p>
{{fig_press}}
<p class="hook">그렇다면 트리를 읽고, 조작하고, 결과를 확인하는 전체 과정을 어떻게 시험할까요?</p>

<h2>어떻게 시험하나</h2>

<h3>가짜 접근성 공급자를 쓴 단위 테스트</h3>
<p>CI 기기에는 화면이 없어서 단위 테스트는 실제 앱을 건드리지 않습니다. 창, 버튼, 텍스트 입력란을
흉내 내는 가짜 접근성 공급자 위에서 돌며 <code>ui_action</code>의 규칙을 하나씩 확인합니다.</p>
<ul>
<li>ref는 자기가 나온 스냅샷에서만 쓸 수 있습니다. 만료된 스냅샷, 캐시에서 밀려난 스냅샷, 없는 ref는
거부됩니다.</li>
<li>스냅샷 뒤에 요소가 바뀌면(사라졌거나, 역할이 바뀌었거나, 다른 프로세스에 속하거나, 원래 창을
떠났으면) 그 ref는 오래된 것입니다. 도구는 거부하고 스냅샷을 새로 찍으라고 하며, 비슷한 요소를 대신
고르지 않습니다.</li>
<li>요소가 지원하지 않는 동작은 아무것도 하기 전에 거부하고, 지원하는 동작 목록을 알려 줍니다.</li>
<li>비밀번호 입력란의 값은 다시 읽지 않고, 로그에도 응답에도 남기지 않습니다.</li>
<li>호출하는 쪽이 <code>activate: true</code>를 넘기지 않으면 앱을 앞으로 가져오지 않습니다.</li>
<li><code>ui_action</code>은 <code>owner</code> 프로필만 호출할 수 있습니다.</li>
</ul>
<p>{a(PR96, "PR #96")}에서 이런 테스트 52개를 추가했습니다. M4 Mac mini에서 전체 <code>swift test</code>는
테스트 256개를 실패 0개로 통과했고, PR의 CI 검사도 모두 통과했습니다.</p>

<h3>M4 Mac mini 실기기 종단 간 시험</h3>
<p>단위 테스트는 규칙이 맞는지를, 실기기 시험은 실제 앱에서 전체가 동작하는지를 확인합니다. 에이전트가
스위치보드를 거쳐 M4 Mac mini를 조작했습니다. 원격 에이전트가 쓰는 것과 같은 네트워크 경로입니다.</p>
<ol>
<li>마우스 위치를 읽습니다.</li>
<li>TextEdit을 열고 새 문서를 만듭니다.</li>
<li><code>ui_snapshot</code>을 호출해 트리에서 텍스트 영역(<code>AXTextArea</code>)과 그 ref를
찾습니다.</li>
<li>그 ref에 <code>ui_action</code>으로 focus하고, 이어서 set_value로 문장 하나를 넣습니다.</li>
<li><code>ui_snapshot</code>을 다시 호출해 텍스트 영역의 값이 그 문장인지 확인합니다.</li>
<li>마우스 위치를 다시 읽어 처음과 비교합니다.</li>
</ol>
<p>두 번 읽은 위치는 같은 점이었습니다. 글자는 들어갔고 커서는 움직이지 않았습니다. 아래 성능
측정에서도 트리 경로를 10번 더 돌렸고, 매번 글자가 문서에 들어갔으며 포인터는 그대로였습니다.</p>
<p>또한 모든 변경은 서로 다른 모델로 도는 독립적인 AI 리뷰어 두 명이 보고, 둘 다 같은 커밋을 승인해야
병합합니다.</p>

<h2>얼마나 빨라졌나</h2>
<p>같은 작업을 두 가지 방식으로 10번씩 측정했습니다. 비어 있는 새 TextEdit 문서에 {SENTENCE}(44자)를
입력하고, 들어갔는지 확인하는 작업입니다.</p>
<ul>
<li><strong>A) 스크린샷 반복:</strong> <code>screenshot</code> → <code>mouse</code>로 텍스트 영역 클릭 →
<code>key</code>로 입력 → <code>screenshot</code>으로 확인.</li>
<li><strong>B) 트리 경로:</strong> <code>ui_snapshot</code> → <code>ui_action</code> focus →
<code>ui_action</code> set_value → <code>ui_snapshot</code>으로 확인.</li>
</ul>
{{fig_cmp}}
{{perf_table}}
<p>이 작업에서 B가 쓴 입력 토큰은 표준 모델에서 A보다 약 55% 적었고(1,435 대 3,165), 고해상도 모델에서는 약
74% 적었습니다(1,435 대 5,427). B는 0.36초, A는 1.70초 만에 끝나 B가 약 4.7배 빨랐고, 포인터도 한 번도
움직이지 않았습니다.</p>
<p>A의 시간은 대부분 키 44개 입력(877 ms)과, 스위치보드를 거쳐 돌아오는 약 500 KB짜리 스크린샷 두 장에
들어갑니다. B의 <code>ui_action</code>은 호출마다 처음부터 끝까지 약 67 ms였고, 대부분은 네트워크
왕복입니다.</p>
<p class="cmp-note">토큰 계산 방법: 이미지는 {a(VISION, "Anthropic 비전 가이드")}의 공식을 썼습니다.
이미지를 모델 한도에 맞게 줄인 뒤 ⌈너비/28⌉ × ⌈높이/28⌉입니다. 표준 모델(긴 변 1,568 px까지)은
1920×1080 스크린샷을 1456×819로 줄여 약 1,560 토큰, 고해상도 모델(긴 변 2,576 px까지)은 줄이지 않아 약
2,691 토큰입니다. 텍스트는 약 4자를 1토큰으로 셌고, 토크나이저는 돌리지 않았습니다. 모델이 실제로 보는
내용만 셌고, 도구 정의와 모델 자신의 출력은 넣지 않았습니다.</p>
<p class="cmp-note">조건: M4 Mac mini(16 GB, macOS 15.7), 1920×1080 디스플레이 한 대, OpenAB Computer
0.10.0. 에이전트는 tailnet 위의 HTTPS로 스위치보드에 연결하고 거기서 Mac mini로 이어지므로, 호출마다 이
왕복 비용이 듭니다. 방식마다 10번, A와 B를 번갈아 돌렸고 처음 워밍업 한 쌍은 버렸습니다. 네 번의 도구
호출 시간만 쟀습니다. A의 클릭 좌표는 알고 있는 창 위치에서 정했고, 실제 모델이라면 첫 스크린샷에서 읽어
내야 합니다. 이 수치는 기기 한 대, 작업 하나에서 나왔고, 모델이 스크린샷이나 스냅샷을 보고 생각하는
시간은 들어 있지 않습니다.</p>

<h2>다음 단계</h2>
<p>Linux(AT-SPI)의 <code>ui_snapshot</code>과 <code>ui_action</code>은 p3로 {a(ISSUE102, "issue #102")}에
미뤄 두었습니다. 접근성 노드가 없는 직접 그린 UI에는 여전히 <code>screenshot</code>과 <code>mouse</code>를
쓸 수 있습니다.</p>

<p class="outro">지난 노트: {a(NOTE1, "OpenAB Computer가 이제 macOS 접근성 트리를 읽습니다")}.</p>
""",
        ),
    },
)
