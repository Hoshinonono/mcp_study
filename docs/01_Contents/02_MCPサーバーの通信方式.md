# MCPサーバーの通信方式

主にClaude向けの内容になります。<br>

## MCPの接続方式

MCPの仕様で決まっている接続方法は3種類あります。<br>
Claude CodeでMCPサーバーを追加するときも、この中から選びます。

| 方式 | 概要 |
| -- | -- |
| 標準入出力(stdio) | 自分のPC上でMCPサーバーを起動して、直接やりとりする |
| HTTP(Streamable HTTP)| URLを指定して、ネットワーク越しにつなぐ |
| SSE(Server-Sent Events) | 古い方式。現在は非推奨なので、今回は省略 | 

## MCPサーバーの到達範囲

2種類の方式のMCPサーバーの動く場所は下記のようになっています。

- 標準入出力(stdio) : MCPサーバーは自分のPCの中で動く
- HTTP : MCPサーバーは別の場所（社内サーバーなど）で動く。自分のPCでも可。

それらの影響により、MCPサーバーが届く範囲は下記のようにClaudeの媒体によって異なっています。

| 媒体 | インターネット上のHTTP | stdio | 社内HTTP |
| -- | -- | -- | -- |
| Claude.ai<br>(Web) | 〇 | × | × |
| Claude Desktop<br>(Chatタブ) | 〇 | 〇 | × |
| Claude Code<br>(CLI・VS Code・<br>Desktop Codeタブ) | 〇 | 〇 | 〇 |

## Claude Desktopの挙動について


