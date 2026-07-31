<div align="center">

<h1>Shadowrocket Rules</h1>

<p>一份开箱即用的 Shadowrocket 规则配置，导入后添加自己的节点或订阅即可使用。</p>

<p>
  <a href="https://github.com/Andrew-liu/Shadowrocket-Rules/actions/workflows/release.yml"><img src="https://img.shields.io/github/actions/workflow/status/Andrew-liu/Shadowrocket-Rules/release.yml?branch=main&style=for-the-badge&logo=githubactions&label=Release" alt="Release Workflow"></a>
  <a href="https://raw.githubusercontent.com/Andrew-liu/Shadowrocket-Rules/refs/heads/release/Shadowrocket.conf"><img src="https://img.shields.io/badge/Shadowrocket-Config-7B61FF?style=for-the-badge" alt="Shadowrocket Config"></a>
  <img src="https://img.shields.io/badge/AdBlock-Daily%20Build-brightgreen?style=for-the-badge" alt="Daily AdBlock Build">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License MIT"></a>
</p>

<p>
  参考 <a href="https://github.com/LingJingMaster/Shadowrocket-Rules">LingJingMaster/Shadowrocket-Rules</a> 与
  <a href="https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever">Johnshall/Shadowrocket-ADBlock-Rules-Forever</a>。
</p>

</div>

## 快速开始

1. 复制配置文件的 Raw 链接：
   `https://raw.githubusercontent.com/Andrew-liu/Shadowrocket-Rules/refs/heads/release/Shadowrocket.conf`
2. 打开 Shadowrocket → 配置 → 右上角 `+` → 粘贴链接 → 下载
3. 点击已下载的配置，设为使用中
4. 首页添加你自己的节点或订阅
5. 连通性测试，确认 `🛟 自动节点` 已选择可用节点
6. 首页 → 全局路由 → 开启“启用回退”，让实际连接连续失败时自动换节点

## 发布说明

- `main` 分支维护源配置、规则列表、构建脚本和 GitHub Actions。
- `release` 分支由 GitHub Actions 每日北京时间 09:00 自动生成，是 Shadowrocket 的导入和更新地址。
- `Advertising.list` 不在 `main` 手工维护，发布时从 `Shadowrocket-ADBlock-Rules-Forever` 的 `sr_ad_only.conf` 转换生成。
- 发布前会校验生成配置、规则数量、规则类型和 WeChat 规则源，校验通过后才发布 `release` 分支。

## 自动统计

<!-- AUTO-STATS:START -->
- 更新时间（UTC）：`发布构建时自动写入`
- 广告规则源：`发布构建时自动写入`
- Apple 域名源：`发布构建时自动写入`

| 规则文件 | 规则数 |
|----------|--------:|
| `Advertising.list` | 发布构建时自动写入 |
| `Apple_Domain.list` | 发布构建时自动写入 |
| `AI.list` | 发布构建时自动写入 |
| `Apple.list` | 发布构建时自动写入 |
| `ApplePush.list` | 发布构建时自动写入 |
| `Google.list` | 发布构建时自动写入 |
| `HK_Broker.list` | 发布构建时自动写入 |
<!-- AUTO-STATS:END -->

## 当前重点

- 广告过滤规则已迁移为本仓库 `release/Advertising.list`，由 `🛑 广告拦截` 策略组统一执行。
- 保留 blackmatrix7 `BlockHttpDNS`，优先拦截 App 内置 HTTPDNS，减少广告和分流规则被绕过。
- 本仓库维护 `AI.list`、`Google.list`、`Apple.list`、`ApplePush.list`、`HK_Broker.list`，并在发布时生成 `Apple_Domain.list`。
- `Google.list` 包含 Google / Gemini 相关规则，`🔍 谷歌服务` 默认走日本节点，并提供香港节点作为手动可选分区。
- `🤖 AI 服务` 默认走日本节点，覆盖 ChatGPT、Claude、Copilot、Grok、OpenRouter 与 Perplexity；美国节点和自动节点作为备用。
- ChatGPT 规则仅保留核心主站、静态资源、上传、功能配置和必要验证域名，避免第三方客服、支付与遥测服务被过度分流。
- 新增 `🛟 自动节点` 全局测速组，境外与兜底流量默认使用经过健康检查的节点，不再默认裸走 `PROXY`。
- 全部自动测速组改用 YouTube HTTPS 204 探测，每 120 秒检查一次，并设置 100ms 切换容差。
- GitHub / GitHub Raw 更新域名使用内联前置规则，避免远程规则尚未下载时形成启动闭环。
- `𝕏 X 服务` 默认走日本节点，并内联 `x.com`、`twitter.com`、`t.co`、`twimg.com` 等核心域名；美国节点和自动节点作为备用。
- Google、ChatGPT/AI 与 X 三类高频服务统一日本优先，减少跨地区出口变化。
- 新增新加坡、韩国自动测速节点组，方便按地区手动切换。
- 新增 PayPal、X、Facebook、Amazon 独立分流策略组。
- 国内常用 App 增加前置直连规则，覆盖 BiliBili、网易云音乐、百度、豆瓣、微信、新浪、知乎、小红书、抖音。
- `Apple_Domain.list` 发布时从 blackmatrix7 Apple bare domain set 同步转换，提供完整 Apple 域名覆盖。
- `Apple.list` 是本仓维护的 Apple overlay / 精简补充规则，补充 iCloud Photos、CloudKit、Apple CDN，并保留少量 blackmatrix7 Apple 规则。
- `ApplePush.list` 将 Apple Push Notification service 相关域名优先归入 `🍎 苹果推送`。
- `HK_Broker.list` 补充富途 / moomoo / 长桥 / 老虎 / TradeUP / Schwab 证券域名及交易 IP 段。

## 默认策略

| 服务 | 默认策略 | 可选策略 |
|------|----------|----------|
| 🧱 DNS 防泄露 | REJECT | 节点选择、DIRECT |
| 🛑 广告拦截 | REJECT | DIRECT、节点选择 |
| 🤖 AI 服务 | 🇯🇵 日本节点 | 🇺🇸 美国节点、自动节点、节点选择、PROXY、DIRECT |
| 📹 油管视频 | 节点选择 | PROXY、DIRECT |
| 🔍 谷歌服务 | 🇯🇵 日本节点 | 🇭🇰 香港节点、节点选择、PROXY、DIRECT |
| Ⓜ️ 微软服务 | 节点选择 | PROXY、DIRECT |
| 💳 PayPal | 节点选择 | PROXY、DIRECT |
| 𝕏 X 服务 | 🇯🇵 日本节点 | 🇺🇸 美国节点、自动节点、节点选择、PROXY、DIRECT |
| 📘 Facebook | 节点选择 | PROXY、DIRECT |
| 🛒 Amazon | 节点选择 | PROXY、DIRECT |
| 🍎 苹果推送 | 节点选择 | PROXY、DIRECT |
| 🍏 苹果服务 | DIRECT | 节点选择、PROXY |
| 📈 券商服务 | 🇭🇰 香港节点 | DIRECT、节点选择、PROXY |
| 🏠 私有网络 | DIRECT | 节点选择、REJECT |
| 🔒 国内服务 | DIRECT | 节点选择、REJECT |
| 🌍 非中国 | 自动节点 | 节点选择、PROXY、DIRECT、日本节点 |
| 🐟 漏网之鱼 | 自动节点 | 节点选择、PROXY、DIRECT、日本节点 |

## 策略组说明

| 策略组 | 类型 | 说明 |
|--------|------|------|
| 🚀 节点选择 | 手动选择 | 主策略，默认选择自动节点，也可切内置代理、地区分组或直连 |
| 🛟 自动节点 | 自动测速 | 匹配全部有效节点，排除流量/套餐信息，默认承载境外与兜底流量 |
| 🇭🇰 香港节点 | 自动测速 | 按节点名关键词匹配香港节点 |
| 🇹🇼 台湾节点 | 自动测速 | 按节点名关键词匹配台湾节点 |
| 🇯🇵 日本节点 | 自动测速 | 按节点名关键词匹配日本节点 |
| 🇸🇬 新加坡节点 | 自动测速 | 按节点名关键词匹配新加坡节点 |
| 🇰🇷 韩国节点 | 自动测速 | 按节点名关键词匹配韩国节点 |
| 🇺🇸 美国节点 | 自动测速 | 按节点名关键词匹配美国节点 |
| 🌐 其他节点 | 自动测速 | 匹配不属于以上地区的节点 |
| 𝕏 X 服务 | 手动选择 | 默认日本节点，覆盖 X 主站、短链、图片视频和直播域名，可切美国或自动节点 |
| 💳 PayPal / 📘 Facebook / 🛒 Amazon | 手动选择 | 海外服务独立分流，可切节点选择、PROXY、DIRECT 或 REJECT |

## 分流规则

规则从上到下依次匹配。`🔍 谷歌服务` 优先级高于 `🤖 AI 服务`，因此 Gemini 会走谷歌服务策略组。

| 优先级 | 服务 | 默认策略 |
|--------|------|----------|
| 1 | GitHub / GitHub Raw 更新引导 | 自动节点 |
| 2 | 🧱 DNS 防泄露（HTTPDNS） | REJECT |
| 3 | 🛑 广告拦截 | REJECT |
| 4 | 🔍 谷歌服务（含 Gemini） | 日本节点，可手动切香港节点 |
| 5 | 🤖 AI 服务（ChatGPT、Claude 等） | 日本节点，美国与自动节点备用 |
| 6 | 📹 油管视频 | 节点选择 |
| 7 | 🔒 哔哩哔哩 / 国内常用 App | DIRECT |
| 8 | 🏠 私有网络 / 局域网 | DIRECT |
| 9 | 📲 电报消息 | 节点选择 |
| 10 | 𝕏 X 服务 | 日本节点，美国与自动节点备用 |
| 11 | 💳 PayPal / 📘 Facebook / 🛒 Amazon | 节点选择 |
| 12 | 🐱 代码托管（GitHub、GitLab、Atlassian） | 节点选择 |
| 13 | Ⓜ️ 微软服务 | 节点选择 |
| 14 | 📈 券商服务（富途 / moomoo / 长桥 / 老虎） | 香港节点 |
| 15 | 🍎 苹果推送 | 节点选择 |
| 16 | 🍏 苹果服务 | DIRECT |
| 17 | 🔒 国内服务 | DIRECT |
| 18 | 🌍 非中国（境外流量） | 自动节点 |
| 19 | GEOIP CN | DIRECT |
| 20 | 🐟 漏网之鱼（兜底） | 自动节点 |

## 规则集来源

- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) — 主要分流规则集
- [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) — 广告过滤规则来源，每日转换为本仓库 `release/Advertising.list`
- [iab0x00/ProxyRules](https://github.com/iab0x00/ProxyRules) — AI 服务补充规则
- `Apple_Domain.list` 发布时从 blackmatrix7 Apple bare domain set 转换生成，作为完整 Apple 域名规则
- `Apple.list` 是本仓维护的 Apple overlay / 精简补充规则，用于补充 iCloud Photos / CloudKit / Apple CDN 直连域名
- `HK_Broker.list` 补充富途 / moomoo / 长桥 / 老虎 / TradeUP / Schwab 证券域名及交易 IP 段

## 其他特性

- DNS：主 DNS 使用 AliDNS DoH / AliDNS，备用 DNS 使用腾讯 DoH / 腾讯 DNS / 系统 DNS，隔离单一上游故障
- DNS 劫持：拦截常见硬编码 53 端口 DNS，防止应用绕过规则
- HTTPDNS 拦截：引用 blackmatrix7 `BlockHttpDNS`，阻止 App 通过内置 HTTPDNS 绕过系统解析
- 自动节点：使用 `https://www.youtube.com/generate_204` 验证 HTTPS 出口，每 120 秒检测，100ms 容差减少频繁抖动
- 更新引导：GitHub、GitHub Raw 和静态资源域名在远程规则之前直接进入自动节点，避免首次加载依赖闭环
- 广告过滤：每日从 `Shadowrocket-ADBlock-Rules-Forever` 的 `sr_ad_only.conf` 转换生成 `release/Advertising.list`，由 `🛑 广告拦截` 策略组统一执行
- QUIC 屏蔽：对代理连接屏蔽 UDP/443，强制回退 HTTP/2
- 本地服务保护：`localhost.weixin.qq.com` 固定解析到 `127.0.0.1` 并强制直连，避免 fake-IP 影响微信本地回调
- 腾讯云 IM：`shortconn.im.qcloud.com` 前置归入国内服务，避免被券商分流规则误挂到香港节点
- TUN 直连优化：iCloud Photos / CloudKit / Apple CDN 域名使用系统 DNS 并跳过代理，保留 Apple Push 走代理
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
- 自动节点会排除名称包含“剩余、流量、套餐、到期、官网、客服、邀请”的订阅信息条目
- Google、AI 与 X 默认走日本节点，也可在 App 内切换备用出口；PayPal、Facebook、Amazon、非中国和漏网之鱼同样支持手动切换
- 建议在首页 → 全局路由中开启“启用回退”，用实际连接失败触发节点切换，弥补单 URL 健康检查的局限
- 若订阅域名在当前网络不可直连，请将域名（不要包含订阅 Token）作为前置 `DOMAIN` 规则指向 `🛟 自动节点`
- 如需 HTTPS 解密功能，请在 Shadowrocket 中生成并安装 CA 证书

## License

MIT
