#!/usr/bin/env python3
"""openab.dev landing page, four languages, one template.

    python3 scripts/build.py          # writes index.html, zh/, ja/, ko/

Never hand-edit the generated HTML: four near-identical files drift. Every link and
asset path is relative, so the same files work at the GitHub Pages preview
(https://openabdev.github.io/openab-site/) and at https://openab.dev/. Only the tags
that must be absolute (canonical, hreflang, og:url, og:image) use SITE.
"""
import hashlib
import html
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = os.environ.get("SITE", "https://openab.dev").rstrip("/")
ORDER = ["en", "zh", "ja", "ko"]
SWITCH_ORDER = ["zh", "ja", "ko", "en"]
DISCORD = "https://openab.dev/discord"
GITHUB_ORG = "https://github.com/openabdev"

LANG = {
    "en": dict(dir="", htmllang="en", label="EN", og_locale="en_US"),
    "zh": dict(dir="zh", htmllang="zh-Hant", label="中文", og_locale="zh_TW"),
    "ja": dict(dir="ja", htmllang="ja", label="日本語", og_locale="ja_JP"),
    "ko": dict(dir="ko", htmllang="ko", label="한국어", og_locale="ko_KR"),
}

# Product order and the language-independent parts of each card. `link` is the only
# destination of the card. The Connect and Remote app source is not public, so those
# two cards point at connect.openab.dev instead of a repository.
PRODUCTS = [
    dict(key="classic", name="OpenAB Classic", icon=("art", "oab-classic"), accent="#5B3FA8",
         tags="Rust · Discord · Slack · Gateway", link="https://github.com/openabdev/openab",
         link_label="github.com/openabdev/openab"),
    dict(key="pty", name="OpenAB PTY", icon=("art", "oab-pty"), accent="#2F6E8F",
         tags="Rust · Kubernetes · ECS", link="https://github.com/openabdev/openab-pty",
         link_label="github.com/openabdev/openab-pty"),
    dict(key="connect", name="OpenAB Connect", icon=("art", "openab-connect"), accent="#304E68",
         tags="macOS · Mac App Store", link="https://connect.openab.dev/{lp}",
         link_label="connect.openab.dev"),
    dict(key="remote", name="OpenAB Remote", icon=("art", "openab-remote"), accent="#C96842",
         tags="iPhone · App Store", link="https://connect.openab.dev/{lp}",
         link_label="connect.openab.dev"),
    dict(key="computer", name="OpenAB Computer", icon=("art", "oab-computer"), accent="#3F7F5F",
         tags="Swift on macOS · Rust on Linux", link="https://github.com/openabdev/openab-computer",
         link_label="github.com/openabdev/openab-computer"),
    dict(key="sb", name="openab-sb", icon=("art", "oab-sb"), accent="#8A5A2B",
         tags="Rust · MCP · WebSocket", link="https://github.com/openabdev/openab-sb",
         link_label="github.com/openabdev/openab-sb"),
    dict(key="octobroker", name="octobroker", icon=("art", "octobroker"), accent="#7A3E6E",
         tags="Rust · Kubernetes · ECS", link="https://github.com/openabdev/octobroker",
         link_label="github.com/openabdev/octobroker"),
    # Private repo, to be renamed: no link and no icon until both exist.
    dict(key="nearpush", name="oab-nearpush", icon=("none", None), accent="#3E6A9E",
         tags="iPhone · macOS · Kiro hooks", link=None, link_label=None),
]

T = {}

T["en"] = dict(
    title="OpenAB — open agent broker ecosystem",
    desc="OpenAB is a family of open-source runtimes and native apps for coding agents: "
         "instruct them from chat, take over their terminal, lend them a computer, and broker "
         "their GitHub access, all on infrastructure you own.",
    og_alt="OpenAB — coding agents on infrastructure you own",
    nav=("Products", "Community"),
    kicker="Open Agent Broker",
    h1='Coding agents,<br>on <span class="mark">infrastructure you own</span>.',
    tag="Open-source runtimes and native apps for coding agents. Instruct them from chat, "
        "take over their terminal, lend them a computer, and broker their GitHub access.",
    cta_products="See the products", cta_discord="Join us on Discord",
    products_h2="The ecosystem",
    products_intro="Each piece works on its own. Together they make one loop: "
                   "an agent in a sandbox, your hands in its terminal, its hands on your computer.",
    for_label="For",
    community_h2="Come say hi",
    community_p="Questions, bug reports and show-and-tell happen in the OpenAB Discord.",
    community_cta="Join the OpenAB Discord",
    foot=("GitHub", "Discord"),
    cards=dict(
        classic=("ACP broker",
                 "The original Open Agent Broker. Mention a bot in Discord or Slack (or Telegram, "
                 "LINE, Feishu/Lark, Google Chat, WeCom and Teams through gateway adapters) and it "
                 "drives an ACP coding CLI such as Kiro, Claude Code, Codex, Gemini or Copilot "
                 "over stdio JSON-RPC.",
                 "instructing coding agents from team chat, one thread per task."),
        pty=("Sandboxed remote terminal",
             "A small runtime that hands out a shell inside a locked-down container: uid 1000, "
             "no sudo, a read-only root filesystem and no host credentials. It is reached over a "
             "WireGuard tailnet with per-session tokens.",
             "attaching to the same image and workspace your agent works in, and looking at "
             "what it left behind."),
        connect=("Mac app",
                 "The native Mac client for OpenAB PTY. Agents from every major vendor, each in "
                 "its own sandbox on your own infrastructure, with split panes, voice input and "
                 "sessions that keep running after you quit the app.",
                 "running and watching many coding agents from one Mac."),
        remote=("iPhone app",
                "Your iPhone becomes a private push-to-talk remote for OpenAB Connect. Speech is "
                "transcribed on the device, and only terminal-safe text is sent to the selected "
                "Mac session.",
                "talking to your agents from across the room instead of typing."),
        computer=("Your computer as MCP tools",
                  "A thin daemon on a Mac or Linux box you own that exposes it to an agent "
                  "elsewhere as MCP servers: shell, screenshots, mouse, keyboard, AppleScript "
                  "and a browser. Every call needs both a Tailscale identity and a bearer token.",
                  "letting a sandboxed agent build in Xcode, drive the Simulator and check the "
                  "screen on a machine you own."),
        sb=("Switchboard",
            "Lets agents use tools on computers that can only dial out. Each computer dials the "
            "switchboard over one WebSocket, and the switchboard relays MCP calls to it under a "
            "deny-by-default allowlist per caller. It runs no tools and stores nothing.",
            "lending the browser on a machine in your own network to cloud agents without "
            "opening an inbound port."),
        octobroker=("GitHub credential broker",
                    "Agents get GitHub's MCP tools, REST and GraphQL reads, and even git push "
                    "without holding a GitHub credential. octobroker checks each agent's revocable "
                    "key against a default-deny tool and repo policy, then mints short-lived, "
                    "repo-scoped GitHub App tokens.",
                    "giving a fleet of agents GitHub access you can scope, audit and revoke."),
        nearpush=("Desk display for agent status",
                  "Turns an iPhone into a dedicated desk display for your coding agent, one large "
                  "card at a time: \u201callow.\u201d when it needs permission, \u201cyour turn.\u201d when it is "
                  "waiting for your answer, \u201call set.\u201d when the task is done. A small Mac app and "
                  "daemon feed it from agent hooks on your private network: Kiro today, adapters "
                  "for other CLIs planned.",
                  "knowing at a glance whether your agent needs you, without watching the terminal."),
    ),
)

T["zh"] = dict(
    title="OpenAB — 開源 Agent Broker 生態系",
    desc="OpenAB 是一組給 coding agent 用的開源執行環境與原生 App：在聊天室下指令、接手它的終端機、"
         "借它一台電腦、代管它的 GitHub 權限，全部跑在你自己的基礎架構。",
    og_alt="OpenAB — coding agent 跑在你自己的基礎架構",
    nav=("產品", "社群"),
    kicker="Open Agent Broker",
    h1='你的 Coding Agent，<br>跑在<span class="mark">你自己的基礎架構</span>。',
    tag="給 coding agent 用的開源執行環境與原生 App。在聊天室下指令、接手它的終端機、"
        "借它一台電腦，再幫它代管 GitHub 權限。",
    cta_products="看看產品", cta_discord="加入 Discord",
    products_h2="生態系",
    products_intro="每一塊都能單獨使用。放在一起就是一個完整迴圈：agent 在沙箱裡，"
                   "你的手在它的終端機，它的手在你的電腦上。",
    for_label="用途",
    community_h2="來打個招呼",
    community_p="問題、bug 回報和作品分享，都在 OpenAB 的 Discord。",
    community_cta="加入 OpenAB Discord",
    foot=("GitHub", "Discord"),
    cards=dict(
        classic=("ACP broker",
                 "最初的 Open Agent Broker。在 Discord 或 Slack 提及 bot（Telegram、LINE、"
                 "飛書/Lark、Google Chat、企業微信與 Teams 走 gateway adapter），"
                 "它就透過 stdio JSON-RPC 驅動 Kiro、Claude Code、Codex、Gemini、Copilot 等 ACP coding CLI。",
                 "在團隊聊天室指揮 coding agent，一個任務一個討論串。"),
        pty=("沙箱遠端終端機",
             "一個小型 runtime，在鎖死的容器裡交給你一個 shell：uid 1000、沒有 sudo、"
             "唯讀的根檔案系統、沒有主機憑證。透過 WireGuard tailnet 連線，每個 session 各自一組 token。",
             "進到 agent 工作的同一個 image 和 workspace，直接看它留下了什麼。"),
        connect=("Mac App",
                 "OpenAB PTY 的原生 Mac 客戶端。所有頂尖廠商的 Agent，各自沙箱，"
                 "執行在你的私有基礎架構；分割窗格、語音輸入，關掉 app 後 session 繼續執行。",
                 "在一台 Mac 上同時執行、觀看多個 coding agent。"),
        remote=("iPhone App",
                "把 iPhone 變成 OpenAB Connect 的私人按住說話遙控器。語音只在手機上轉成文字，"
                "只有可以安全送進終端機的文字會送到選定的 Mac session。",
                "不用打字，在房間另一頭就能跟 agent 說話。"),
        computer=("把你的電腦變成 MCP 工具",
                  "一個跑在你自己的 Mac 或 Linux 機器上的輕量常駐程式，把這台機器以 MCP server 的形式"
                  "提供給別處的 agent：shell、截圖、滑鼠、鍵盤、AppleScript 和瀏覽器。"
                  "每次呼叫都要同時通過 Tailscale 身分與 bearer token。",
                  "讓沙箱裡的 agent 在你自己的機器上用 Xcode 編譯、操作 Simulator、檢查畫面。"),
        sb=("交換機（Switchboard）",
            "讓 agent 使用只能主動往外連的電腦上的工具。每台電腦用一條 WebSocket 連上交換機，"
            "交換機再依每個呼叫者「預設拒絕」的允許清單轉送 MCP 呼叫。它不執行工具，也不儲存任何東西。",
            "不開任何對內 port，就把你自家網路裡那台機器的瀏覽器借給雲端 agent。"),
        octobroker=("GitHub 憑證代管",
                    "agent 不用持有任何 GitHub 憑證，也能使用 GitHub 的 MCP 工具、REST 與 GraphQL 讀取，"
                    "甚至 git push。octobroker 以可撤銷的金鑰比對每個 agent「預設拒絕」的工具與 repo 政策，"
                    "再發放短效、限定 repo 的 GitHub App token。",
                    "給一整批 agent 可限縮、可稽核、可撤銷的 GitHub 權限。"),
        nearpush=("Agent 狀態桌面顯示器",
                  "把 iPhone 變成桌上專門顯示 coding agent 狀態的螢幕，一次只顯示一張大卡片："
                  "需要權限時是「allow.」，等你回答時是「your turn.」，任務完成時是「all set.」。"
                  "由一個小型 Mac App 與常駐程式在你的私有網路上從 agent hooks 推送狀態："
                  "目前支援 Kiro，其他 CLI 的 adapter 規劃中。",
                  "不用盯著終端機，瞄一眼就知道 agent 是不是在等你。"),
    ),
)

T["ja"] = dict(
    title="OpenAB — オープンな Agent Broker エコシステム",
    desc="OpenAB は、コーディングエージェントのためのオープンソースのランタイムとネイティブアプリの集まりです。"
         "チャットで指示し、ターミナルを引き継ぎ、コンピューターを貸し、GitHub へのアクセスを仲介します。すべて自分のインフラで。",
    og_alt="OpenAB — コーディングエージェントを自分のインフラで",
    nav=("プロダクト", "コミュニティ"),
    kicker="Open Agent Broker",
    h1='コーディングエージェントを、<br><span class="mark">自分のインフラ</span>で。',
    tag="コーディングエージェントのためのオープンソースのランタイムとネイティブアプリ。"
        "チャットで指示し、ターミナルを引き継ぎ、コンピューターを貸し、GitHub へのアクセスを仲介します。",
    cta_products="プロダクトを見る", cta_discord="Discord に参加",
    products_h2="エコシステム",
    products_intro="どれも単体で使えます。組み合わせると一つのループになります。"
                   "エージェントはサンドボックスに、あなたの手はそのターミナルに、エージェントの手はあなたのコンピューターに。",
    for_label="用途",
    community_h2="気軽にどうぞ",
    community_p="質問、バグ報告、作ったものの紹介は OpenAB の Discord で。",
    community_cta="OpenAB Discord に参加",
    foot=("GitHub", "Discord"),
    cards=dict(
        classic=("ACP ブローカー",
                 "最初の Open Agent Broker。Discord や Slack で bot をメンションすると"
                 "（Telegram、LINE、Feishu/Lark、Google Chat、WeCom、Teams は gateway アダプター経由）、"
                 "stdio JSON-RPC で Kiro、Claude Code、Codex、Gemini、Copilot などの ACP コーディング CLI を動かします。",
                 "チームのチャットからコーディングエージェントに指示する。タスクごとに一スレッド。"),
        pty=("サンドボックスのリモートターミナル",
             "ロックダウンされたコンテナ内のシェルを渡す小さなランタイム。uid 1000、sudo なし、"
             "読み取り専用のルートファイルシステム、ホストの認証情報なし。"
             "WireGuard の tailnet 越しに、セッションごとのトークンで接続します。",
             "エージェントが作業しているのと同じイメージとワークスペースに入り、残したものをその場で見る。"),
        connect=("Mac アプリ",
                 "OpenAB PTY のネイティブ Mac クライアント。主要ベンダーのエージェントを、"
                 "それぞれ自分のインフラ上のサンドボックスで。分割ペイン、音声入力、"
                 "アプリを終了しても動き続けるセッション。",
                 "一台の Mac で多くのコーディングエージェントを動かし、見守る。"),
        remote=("iPhone アプリ",
                "iPhone を OpenAB Connect 用のプライベートなプッシュ・トゥ・トークのリモコンにします。"
                "音声は端末上で文字になり、ターミナルに安全なテキストだけが選んだ Mac のセッションに送られます。",
                "キーボードを打たずに、部屋の向こうからエージェントに話しかける。"),
        computer=("自分のコンピューターを MCP ツールに",
                  "自分の Mac や Linux マシンで動く薄いデーモン。そのマシンを、別の場所にいるエージェントに"
                  " MCP サーバーとして公開します。シェル、スクリーンショット、マウス、キーボード、AppleScript、ブラウザー。"
                  "呼び出しには Tailscale の ID と bearer トークンの両方が必要です。",
                  "サンドボックスのエージェントに、自分のマシンで Xcode のビルド、シミュレーター操作、画面確認をさせる。"),
        sb=("スイッチボード",
            "外向きにしか接続できないコンピューター上のツールを、エージェントが使えるようにします。"
            "各コンピューターが WebSocket 一本でスイッチボードに接続し、スイッチボードは呼び出し元ごとの"
            "デフォルト拒否の許可リストに従って MCP 呼び出しを中継します。ツールは実行せず、何も保存しません。",
            "受信ポートを開けずに、自分のネットワーク内のマシンのブラウザーをクラウドのエージェントに貸す。"),
        octobroker=("GitHub 認証情報ブローカー",
                    "エージェントは GitHub の認証情報を一切持たずに、GitHub の MCP ツール、REST と GraphQL の読み取り、"
                    "さらに git push まで使えます。octobroker は失効可能なキーでエージェントを確認し、"
                    "デフォルト拒否のツール・リポジトリポリシーを適用したうえで、短命でリポジトリ限定の GitHub App トークンを発行します。",
                    "多数のエージェントに、範囲を絞れて、監査でき、取り消せる GitHub アクセスを与える。"),
        nearpush=("エージェント状態のデスクディスプレイ",
                  "iPhone を、コーディングエージェントの状態を映す専用のデスクディスプレイにします。"
                  "表示は一度に大きなカード一枚。許可が必要なら「allow.」、あなたの返事を待っているなら"
                  "「your turn.」、タスクが終わったら「all set.」。小さな Mac アプリとデーモンが、"
                  "プライベートネットワーク上でエージェントのフックから状態を送ります。"
                  "現在は Kiro に対応し、ほかの CLI 向けアダプターも予定しています。",
                  "ターミナルを見張らなくても、エージェントが自分を待っているかを一目で知る。"),
    ),
)

T["ko"] = dict(
    title="OpenAB — 오픈 Agent Broker 생태계",
    desc="OpenAB는 코딩 에이전트를 위한 오픈소스 런타임과 네이티브 앱 모음입니다. 채팅으로 지시하고, "
         "터미널을 이어받고, 컴퓨터를 빌려주고, GitHub 접근을 중개합니다. 모두 내 인프라에서.",
    og_alt="OpenAB — 코딩 에이전트를 내 인프라에서",
    nav=("제품", "커뮤니티"),
    kicker="Open Agent Broker",
    h1='코딩 에이전트를,<br><span class="mark">내 인프라</span>에서.',
    tag="코딩 에이전트를 위한 오픈소스 런타임과 네이티브 앱. 채팅으로 지시하고, 터미널을 이어받고, "
        "컴퓨터를 빌려주고, GitHub 접근을 중개합니다.",
    cta_products="제품 보기", cta_discord="Discord 참여",
    products_h2="생태계",
    products_intro="각각 따로 쓸 수 있습니다. 함께 쓰면 하나의 루프가 됩니다. "
                   "에이전트는 샌드박스에, 내 손은 그 터미널에, 에이전트의 손은 내 컴퓨터에.",
    for_label="용도",
    community_h2="인사 나눠요",
    community_p="질문, 버그 제보, 만든 것 자랑은 OpenAB Discord에서.",
    community_cta="OpenAB Discord 참여",
    foot=("GitHub", "Discord"),
    cards=dict(
        classic=("ACP 브로커",
                 "최초의 Open Agent Broker. Discord나 Slack에서 bot을 멘션하면"
                 "(Telegram, LINE, Feishu/Lark, Google Chat, WeCom, Teams는 gateway 어댑터로) "
                 "stdio JSON-RPC로 Kiro, Claude Code, Codex, Gemini, Copilot 같은 ACP 코딩 CLI를 구동합니다.",
                 "팀 채팅에서 코딩 에이전트에게 지시하기. 작업마다 스레드 하나."),
        pty=("샌드박스 원격 터미널",
             "잠긴 컨테이너 안의 셸을 내주는 작은 런타임. uid 1000, sudo 없음, 읽기 전용 루트 파일시스템, "
             "호스트 자격 증명 없음. WireGuard tailnet을 통해 세션별 토큰으로 접속합니다.",
             "에이전트가 일하는 바로 그 이미지와 워크스페이스에 들어가, 남긴 것을 그 자리에서 보기."),
        connect=("Mac 앱",
                 "OpenAB PTY의 네이티브 Mac 클라이언트. 주요 벤더의 모든 에이전트를 각자의 샌드박스에서, "
                 "내 인프라 위에서. 분할 창, 음성 입력, 앱을 종료해도 계속 실행되는 세션.",
                 "Mac 한 대에서 여러 코딩 에이전트를 실행하고 지켜보기."),
        remote=("iPhone 앱",
                "iPhone을 OpenAB Connect용 개인 푸시 투 토크 리모컨으로 바꿉니다. 음성은 기기에서 텍스트로 바뀌고, "
                "터미널에 안전한 텍스트만 선택한 Mac 세션으로 전송됩니다.",
                "타이핑 대신 방 건너편에서 에이전트에게 말하기."),
        computer=("내 컴퓨터를 MCP 도구로",
                  "내가 소유한 Mac이나 Linux 기기에서 도는 얇은 데몬. 그 기기를 다른 곳의 에이전트에게 "
                  "MCP 서버로 제공합니다. 셸, 스크린샷, 마우스, 키보드, AppleScript, 브라우저. "
                  "모든 호출에 Tailscale 신원과 bearer 토큰이 둘 다 필요합니다.",
                  "샌드박스의 에이전트가 내 기기에서 Xcode 빌드, 시뮬레이터 조작, 화면 확인을 하게 하기."),
        sb=("스위치보드",
            "바깥으로만 연결할 수 있는 컴퓨터의 도구를 에이전트가 쓸 수 있게 합니다. 각 컴퓨터가 WebSocket "
            "하나로 스위치보드에 접속하고, 스위치보드는 호출자별 기본 거부 허용 목록에 따라 MCP 호출을 중계합니다. "
            "도구를 실행하지 않고 아무것도 저장하지 않습니다.",
            "인바운드 포트를 열지 않고 내 네트워크 안 기기의 브라우저를 클라우드 에이전트에게 빌려주기."),
        octobroker=("GitHub 자격 증명 브로커",
                    "에이전트는 GitHub 자격 증명을 전혀 갖지 않고도 GitHub의 MCP 도구, REST와 GraphQL 읽기, "
                    "git push까지 씁니다. octobroker는 취소 가능한 키로 에이전트를 확인하고 기본 거부 도구·저장소 정책을 "
                    "적용한 뒤, 수명이 짧고 저장소로 범위가 제한된 GitHub App 토큰을 발급합니다.",
                    "여러 에이전트에게 범위를 좁히고, 감사하고, 취소할 수 있는 GitHub 접근 주기."),
        nearpush=("에이전트 상태 데스크 디스플레이",
                  "iPhone을 코딩 에이전트 상태 전용 데스크 디스플레이로 바꿉니다. 한 번에 큰 카드 한 장: "
                  "권한이 필요하면 \u201callow.\u201d, 내 답을 기다리면 \u201cyour turn.\u201d, 작업이 끝나면 "
                  "\u201call set.\u201d. 작은 Mac 앱과 데몬이 내 사설 네트워크에서 에이전트 hook으로 상태를 보냅니다. "
                  "지금은 Kiro를 지원하고, 다른 CLI용 어댑터를 계획하고 있습니다.",
                  "터미널을 지켜보지 않아도 에이전트가 나를 기다리는지 한눈에 알기."),
    ),
)


def rev(name):
    """Content hash for cache busting: GitHub Pages serves max-age=600."""
    f = ROOT / name
    return hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"


def up(code):
    """Relative prefix from a language page back to the site root."""
    return "../" if LANG[code]["dir"] else ""


def page_url(code):
    d = LANG[code]["dir"]
    return f"{SITE}/{d}/" if d else f"{SITE}/"


def esc(s):
    return html.escape(s, quote=True)


# Root page only: a first-time visitor is sent to their browser language. zh-Hant/TW/HK/MO
# go to zh, ja and ko to their pages, everything else (including zh-Hans) stays English.
# A click on the switcher stores the choice and is never overridden. The redirect target
# is relative, so it works under /openab-site/ as well as at the domain root.
ROOT_REDIRECT = """<script>
(function () {
  var KEY = "oab-lang";
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function pick(tag) {
    var p = String(tag).toLowerCase().split("-");
    if (p[0] === "en" || p[0] === "ja" || p[0] === "ko") return p[0];
    if (p[0] !== "zh" || p.indexOf("hans") >= 0) return null;
    return p.some(function (s) { return s === "hant" || s === "tw" || s === "hk" || s === "mo"; }) ? "zh" : null;
  }
  if (stored()) return;
  var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
  var lang = null;
  for (var i = 0; i < langs.length && !lang; i++) lang = pick(langs[i]);
  if (lang && lang !== "en") location.replace(lang + "/" + location.search + location.hash);
})();
</script>"""

REMEMBER = """<script>
document.addEventListener("click", function (e) {
  var a = e.target.closest && e.target.closest(".lang a");
  if (!a) return;
  try { localStorage.setItem("oab-lang", a.getAttribute("data-lang")); } catch (err) { /* no storage */ }
});
</script>"""


def head(code):
    t = T[code]
    d = LANG[code]
    u = up(code)
    og = f"{SITE}/og-{code}.png?v={rev(f'og-{code}.png')}"
    alts = [f'<link rel="alternate" hreflang="{LANG[c]["htmllang"]}" href="{page_url(c)}">' for c in ORDER]
    alts.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/">')
    tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
    ]
    if code == "en":
        tags.append(ROOT_REDIRECT)
    tags += [
        f"<title>{esc(t['title'])}</title>",
        f'<meta name="description" content="{esc(t["desc"])}">',
        f'<link rel="canonical" href="{page_url(code)}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="OpenAB">',
        f'<meta property="og:locale" content="{d["og_locale"]}">',
        f'<meta property="og:title" content="{esc(t["title"])}">',
        f'<meta property="og:description" content="{esc(t["desc"])}">',
        f'<meta property="og:url" content="{page_url(code)}">',
        f'<meta property="og:image" content="{og}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(t["og_alt"])}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(t["title"])}">',
        f'<meta name="twitter:description" content="{esc(t["desc"])}">',
        f'<meta name="twitter:image" content="{og}">',
        '<meta name="theme-color" content="#F7F4FC">',
        *[f'<link rel="icon" type="image/png" sizes="{s}x{s}" href="{u}assets/favicon-{s}.png?v={rev(f"assets/favicon-{s}.png")}">'
          for s in (16, 32, 64)],
        f'<link rel="apple-touch-icon" href="{u}assets/apple-touch-icon.png?v={rev("assets/apple-touch-icon.png")}">',
        f'<link rel="stylesheet" href="{u}style.css?v={rev("style.css")}">',
        *alts,
    ]
    return "\n".join(tags)


def switcher(code):
    u = up(code)
    out = []
    # Same order and "|" separators as connect.openab.dev: 中文|日本語|한국어|EN.
    for c in SWITCH_ORDER:
        href = u + (f"{LANG[c]['dir']}/" if LANG[c]["dir"] else "")
        href = href or "./"
        cls = ' class="active" aria-current="page"' if c == code else ""
        out.append(f'<a{cls} href="{href}" data-lang="{c}" hreflang="{LANG[c]["htmllang"]}">{LANG[c]["label"]}</a>')
    return "|".join(out)


def icon(code, p):
    kind, val = p["icon"]
    # Every card: transparent art with its own shape (sticker outline or app-icon
    # squircle), 56px with a 2x source; no tile, radius or box shadow added.
    if kind == "none":      # neutral slot until the art exists; keeps the head aligned
        return '<span class="card-icon placeholder" aria-hidden="true"></span>'
    assert kind == "art", kind
    a = f"{up(code)}assets/{val}"
    return (f'<img class="card-icon" src="{a}-56.png?v={rev(f"assets/{val}-56.png")}" '
            f'srcset="{a}-112.png?v={rev(f"assets/{val}-112.png")} 2x" alt="" width="56" height="56">')


def cards(code):
    t = T[code]
    lp = f"{LANG[code]['dir']}/" if LANG[code]["dir"] else ""
    out = []
    for p in PRODUCTS:
        role, desc, use = t["cards"][p["key"]]
        if p["link"]:
            tag = f'a class="card" href="{p["link"].format(lp=lp)}"'
            link = f'\n    <span class="card-link">{p["link_label"]}</span>'
        else:               # no public destination yet: a plain card, no link
            tag, link = 'div class="card static"', ""
        out.append(f"""  <{tag} style="--accent:{p['accent']}">
    <div class="card-head">
      {icon(code, p)}
      <div>
        <h3 class="card-name">{p['name']}</h3>
        <span class="card-role">{esc(role)}</span>
      </div>
    </div>
    <p class="card-desc">{esc(desc)}</p>
    <p class="card-for"><strong>{t['for_label']}</strong> {esc(use)}</p>
    <p class="card-tags">{p['tags']}</p>
{link}
  </{tag.split()[0]}>""")
    return "\n".join(out)


def page(code):
    t = T[code]
    u = up(code)
    home = "./"  # brand stays in the current language, like connect.openab.dev
    brand = (f'src="{u}assets/brand-64.png?v={rev("assets/brand-64.png")}" '
             f'srcset="{u}assets/brand-128.png?v={rev("assets/brand-128.png")} 2x"')
    hero = (f'src="{u}assets/hero-224.webp?v={rev("assets/hero-224.webp")}" '
            f'srcset="{u}assets/hero-448.webp?v={rev("assets/hero-448.webp")} 2x"')
    # The hero mascot is un-blended against white, so on the dark theme it would read
    # as faint; there the sticker (own outline) takes its place.
    hero_dark = (f'{u}assets/hero-dark-224.webp?v={rev("assets/hero-dark-224.webp")}, '
                 f'{u}assets/hero-dark-448.webp?v={rev("assets/hero-dark-448.webp")} 2x')
    return f"""<!DOCTYPE html>
<html lang="{LANG[code]['htmllang']}" data-lang="{code}">
<head>
{head(code)}
</head>
<body>
<nav class="top">
  <a class="brand" href="{home}"><img {brand} alt="" width="28" height="28">OpenAB</a>
  <div class="links">
    <a href="#products">{t['nav'][0]}</a>
    <a href="#community">{t['nav'][1]}</a>
    <a href="{GITHUB_ORG}">GitHub</a>
    <span class="lang" aria-label="Language">
    {switcher(code)}
    </span>
  </div>
</nav>
{REMEMBER}

<header class="hero">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{hero_dark}">
    <img class="logo" {hero} alt="OpenAB jellyfish mascot" width="224" height="224">
  </picture>
  <p class="kicker">{t['kicker']}</p>
  <h1>{t['h1']}</h1>
  <p class="tag">{esc(t['tag'])}</p>
  <div class="cta">
    <a class="btn primary" href="#products">{t['cta_products']}</a>
    <a class="btn" href="{DISCORD}">{t['cta_discord']}</a>
  </div>
</header>

<section class="products" id="products">
  <h2>{t['products_h2']}</h2>
  <p class="intro">{esc(t['products_intro'])}</p>
  <div class="grid">
{cards(code)}
  </div>
</section>

<section class="community" id="community">
  <h2>{t['community_h2']}</h2>
  <p>{esc(t['community_p'])}</p>
  <a class="btn primary" href="{DISCORD}">{t['community_cta']}</a>
</section>

<footer>
  <a href="{GITHUB_ORG}">{t['foot'][0]}</a>
  <a href="{DISCORD}">{t['foot'][1]}</a>
  <span class="dim">© 2026 openabdev</span>
</footer>
</body>
</html>
"""


def main():
    for code in ORDER:
        d = LANG[code]["dir"]
        dest = ROOT / d / "index.html" if d else ROOT / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(code), encoding="utf-8")
        print(f"  wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
