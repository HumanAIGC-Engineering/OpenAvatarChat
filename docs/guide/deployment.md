# 部署要求

## 网络环境说明

> [!IMPORTANT]
> **【部署前置警告】不看这里，数字人 100% 罢工！**
>
> 在你兴冲冲地开始部署前，请务必停下脚步！否则，你将大概率遇到：**界面无法访问**、**数字人永远在加载中** 这两大"天坑"。
>
> **你的网络环境决定了【必做配置】：**
>
> * **① 仅本机访问 (`localhost`)**
>   > 最简单，通常无需额外配置。但也只能在部署的电脑上自己访问。
>
> * **② 局域网访问 (如：用手机访问电脑)**
>   > **SSL 证书开始变得【必要】**！多数浏览器需要 `https://` 安全连接才能授权摄像头/麦克风。
>
> * **③ 公网访问 (让任何人都能用)**
>   > **SSL 和 TURN 服务【缺一不可】**！
>   > - **没有合法的 SSL 证书**，浏览器会直接拒绝连接。
>   > - **没有 TURN 服务**，处在不同网络下的用户无法建立视频流连接。

## 准备SSL证书

由于本项目使用 RTC 作为视音频传输的通道，用户如果需要从 localhost 以外的地方连接服务的话，需要准备 SSL 证书以开启 HTTPS。默认配置会读取 `ssl_certs` 目录下的 `localhost.crt` 和 `localhost.key`，用户可以相应修改配置来使用自己的证书。

我们也在 `scripts` 目录下提供了生成自签名证书的脚本：

```bash
scripts/create_ssl_certs.sh
```

## TURN Server

如果点击开始对话后，出现一直等待中的情况，可能你的部署环境存在 NAT 穿透方面的问题（如部署在云上机器等），需要进行数据中继。

### 本地安装

可参考以下操作在同一机器上安装、启动并配置使用 coturn：

1. 运行安装脚本：
```bash
chmod 777 scripts/setup_coturn.sh
scripts/setup_coturn.sh
```

2. 修改 config 配置文件，添加以下配置后启动服务：
```yaml
default:
  chat_engine:
    handler_configs:
      RtcClient:
        turn_config:
          turn_provider: "turn_server"
          urls: ["turn:your-turn-server.com:3478", "turns:your-turn-server.com:5349"]
          username: "your-username"
          credential: "your-credential"
```

3. 确保防火墙（包括云上机器安全组等策略）开放 coturn 所需端口。

### Docker 安装

可以使用 coturn 的 Docker 服务，具体请参考 [Docker Compose 部署](/getting-started/docker) 章节，统一拉起服务。
