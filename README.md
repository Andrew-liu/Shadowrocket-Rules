# Shadowrocket 配置文件

一份开箱即用的 Shadowrocket 规则配置，导入后添加自己的节点或订阅即可使用。

## 快速开始

1. 复制配置文件的 Raw 链接：
   `https://raw.githubusercontent.com/Andrew-liu/Shadowrocket-Rules/refs/heads/release/Shadowrocket.conf`
2. 打开 Shadowrocket → 配置 → 右上角 `+` → 粘贴链接 → 下载
3. 点击已下载的配置，设为使用中
4. 首页添加你自己的节点或订阅
5. 连通性测试，选择可用节点连接

## 发布说明

- `main` 分支维护源配置、规则列表、构建脚本和 GitHub Actions。
- `release` 分支由 GitHub Actions 每日北京时间 09:00 自动生成，是 Shadowrocket 的导入和更新地址。
- `Advertising.list` 不在 `main` 手工维护，发布时从 `Shadowrocket-ADBlock-Rules-Forever` 的 `sr_ad_only.conf` 转换生成。

## 当前重点

- 广告过滤规则已迁移为本仓库 `release/Advertising.list`，由 `🛑 广告拦截` 策略组统一执行。
- 保留 blackmatrix7 `BlockHttpDNS`，优先拦截 App 内置 HTTPDNS，减少广告和分流规则被绕过。
- 本仓库维护 `AI.list`、`Google.list`、`Apple.list`、`ApplePush.list`、`HK_Broker.list`。
- `Google.list` 包含 Google / Gemini 相关规则，`🔍 谷歌服务` 默认走日本节点，并提供香港节点作为手动可选分区。
- 新增新加坡、韩国自动测速节点组，方便按地区手动切换。
- 新增 PayPal、Twitter、Facebook、Amazon 独立分流策略组。
- 国内常用 App 增加前置直连规则，覆盖 BiliBili、网易云音乐、百度、豆瓣、微信、新浪、知乎、小红书、抖音。
- `Apple.list` 基于 blackmatrix7 Apple 规则，补充 iCloud Photos、CloudKit、Apple CDN 相关域名。
- `ApplePush.list` 将 Apple Push Notification service 相关域名优先归入 `🍎 苹果推送`。
- `HK_Broker.list` 补充富途 / moomoo / 长桥 / 老虎 / TradeUP / Schwab 证券域名及交易 IP 段。

## 默认策略

| 服务 | 默认策略 | 可选策略 |
|------|----------|----------|
| 🧱 DNS 防泄露 | REJECT | 节点选择、DIRECT |
| 🛑 广告拦截 | REJECT | DIRECT、节点选择 |
| 🤖 AI 服务 | 🇺🇸 美国节点 | 节点选择、PROXY、DIRECT |
| 📹 油管视频 | 节点选择 | PROXY、DIRECT |
| 🔍 谷歌服务 | 🇯🇵 日本节点 | 🇭🇰 香港节点、节点选择、PROXY、DIRECT |
| Ⓜ️ 微软服务 | 节点选择 | PROXY、DIRECT |
| 💳 PayPal | 节点选择 | PROXY、DIRECT |
| 🐦 Twitter | 节点选择 | PROXY、DIRECT |
| 📘 Facebook | 节点选择 | PROXY、DIRECT |
| 🛒 Amazon | 节点选择 | PROXY、DIRECT |
| 🍎 苹果推送 | 节点选择 | PROXY、DIRECT |
| 🍏 苹果服务 | DIRECT | 节点选择、PROXY |
| 📈 券商服务 | 🇭🇰 香港节点 | DIRECT、节点选择、PROXY |
| 🏠 私有网络 | DIRECT | 节点选择、REJECT |
| 🔒 国内服务 | DIRECT | 节点选择、REJECT |
| 🌍 非中国 | PROXY | 节点选择、DIRECT、日本节点 |
| 🐟 漏网之鱼 | PROXY | 节点选择、DIRECT、日本节点 |

## 策略组说明

| 策略组 | 类型 | 说明 |
|--------|------|------|
| 🚀 节点选择 | 手动选择 | 主策略，可选内置代理、地区分组或直连 |
| 🇭🇰 香港节点 | 自动测速 | 按节点名关键词匹配香港节点 |
| 🇹🇼 台湾节点 | 自动测速 | 按节点名关键词匹配台湾节点 |
| 🇯🇵 日本节点 | 自动测速 | 按节点名关键词匹配日本节点 |
| 🇸🇬 新加坡节点 | 自动测速 | 按节点名关键词匹配新加坡节点 |
| 🇰🇷 韩国节点 | 自动测速 | 按节点名关键词匹配韩国节点 |
| 🇺🇸 美国节点 | 自动测速 | 按节点名关键词匹配美国节点 |
| 🌐 其他节点 | 自动测速 | 匹配不属于以上地区的节点 |
| 💳 PayPal / 🐦 Twitter / 📘 Facebook / 🛒 Amazon | 手动选择 | 海外服务独立分流，可切节点选择、PROXY、DIRECT 或 REJECT |

## 分流规则

规则从上到下依次匹配。`🔍 谷歌服务` 优先级高于 `🤖 AI 服务`，因此 Gemini 会走谷歌服务策略组。

| 优先级 | 服务 | 默认策略 |
|--------|------|----------|
| 1 | 🧱 DNS 防泄露（HTTPDNS） | REJECT |
| 2 | 🛑 广告拦截 | REJECT |
| 3 | 🔍 谷歌服务（含 Gemini） | 日本节点，可手动切香港节点 |
| 4 | 🤖 AI 服务（ChatGPT、Claude 等） | 美国节点 |
| 5 | 📹 油管视频 | 节点选择 |
| 6 | 🔒 哔哩哔哩 / 国内常用 App | DIRECT |
| 7 | 🏠 私有网络 / 局域网 | DIRECT |
| 8 | 📲 电报消息 | 节点选择 |
| 9 | 💳 PayPal / 🐦 Twitter / 📘 Facebook / 🛒 Amazon | 节点选择 |
| 10 | 🐱 代码托管（GitHub、GitLab、Atlassian） | 节点选择 |
| 11 | Ⓜ️ 微软服务 | 节点选择 |
| 12 | 📈 券商服务（富途 / moomoo / 长桥 / 老虎） | 香港节点 |
| 13 | 🍎 苹果推送 | 节点选择 |
| 14 | 🍏 苹果服务 | DIRECT |
| 15 | 🔒 国内服务 | DIRECT |
| 16 | 🌍 非中国（境外流量） | PROXY |
| 17 | GEOIP CN | DIRECT |
| 18 | 🐟 漏网之鱼（兜底） | PROXY |

## 规则集来源

- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) — 主要分流规则集
- [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) — 广告过滤规则来源，每日转换为本仓库 `release/Advertising.list`
- [iab0x00/ProxyRules](https://github.com/iab0x00/ProxyRules) — AI 服务补充规则
- `Apple.list` 基于 blackmatrix7 Apple 规则，并补充 iCloud Photos / Apple CDN 直连域名
- `HK_Broker.list` 补充富途 / moomoo / 长桥 / 老虎 / TradeUP / Schwab 证券域名及交易 IP 段

## 其他特性

- DNS：默认使用 AliDNS DoH + 腾讯 DNS / AliDNS 普通 DNS，备用 DNS 不回退系统 DNS
- DNS 劫持：拦截常见硬编码 53 端口 DNS，防止应用绕过规则
- HTTPDNS 拦截：引用 blackmatrix7 `BlockHttpDNS`，阻止 App 通过内置 HTTPDNS 绕过系统解析
- 广告过滤：每日从 `Shadowrocket-ADBlock-Rules-Forever` 的 `sr_ad_only.conf` 转换生成 `release/Advertising.list`，由 `🛑 广告拦截` 策略组统一执行
- QUIC 屏蔽：对代理连接屏蔽 UDP/443，强制回退 HTTP/2
- 本地服务保护：`localhost.weixin.qq.com` 固定解析到 `127.0.0.1` 并强制直连，避免 fake-IP 影响微信本地回调
- 腾讯云 IM：`shortconn.im.qcloud.com` 前置归入国内服务，避免被券商分流规则误挂到香港节点
- TUN 直连优化：iCloud Photos / CloudKit / Apple CDN 域名使用系统 DNS 并跳过代理，保留 Apple Push 走代理
- DNS 上游：移除 `doh.pub`，默认使用 AliDNS DoH + 腾讯 DNS / AliDNS 普通 DNS，减少 DoH 长尾超时
- 局域网解析保护：`*.in-addr.arpa`、`*.ip6.arpa`、`*.local`、`*.lan`、`*.internal` 前置直连并交给系统解析，补充常见 DNS-SD 反查模式，避免 Bonjour / PTR 反查打到公共 DoH
- TUN 边界：保留 `198.18.0.0/15` 给 fake-IP / TUN 内部使用，不加入排除路由，私网桥接网段仍通过 `10.0.0.0/8`、`192.168.0.0/16` 等排除
- Apple 推送：默认走 `🚀 节点选择`，通常随主策略走代理
   - `push.apple.com`
   - `gateway.push.apple.com`
   - `api.push.apple.com`
   - `sandbox.push.apple.com` 
- Google 防跳转：`google.cn` / `g.cn` 自动 302 到 `google.com`
- MITM：仅解密 `*.google.cn`

## 注意事项

- 地区分组通过节点名称关键词自动匹配，请确保你的节点名称包含地区标识（如 🇭🇰、HK、香港、SG、新加坡、KR、韩国等）
- Google、AI、PayPal、Twitter、Facebook、Amazon、非中国和漏网之鱼的默认出口可在 App 内手动切换
- 如需 HTTPS 解密功能，请在 Shadowrocket 中生成并安装 CA 证书

## License

MIT
