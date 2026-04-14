# Deployment Requirements

## Network Environment

> [!IMPORTANT]
> **[PRE-DEPLOYMENT WARNING] IGNORE THIS, AND YOUR DIGITAL HUMAN WILL 100% GO ON STRIKE!**
>
> Your network environment determines the MANDATORY setup:
>
> * **Localhost-Only Access**
>   > Simplest setup, usually requiring no extra configuration.
>
> * **LAN Access (e.g., from your phone to your PC)**
>   > An **SSL certificate becomes ESSENTIAL**! Most browsers require `https://` for camera/microphone permissions.
>
> * **Public / Internet Access**
>   > Both **SSL certificate and TURN service are NON-NEGOTIABLE**!

## Prepare SSL Certificates

Since this project uses RTC for audio/video transmission, an SSL certificate is needed for non-localhost access. The default config reads `localhost.crt` and `localhost.key` from the `ssl_certs` directory.

Generate a self-signed certificate:

```bash
scripts/create_ssl_certs.sh
```

## TURN Server

If clicking "Start Conversation" results in a perpetual waiting state, it may be due to NAT traversal issues.

### Local Installation

1. Run the installation script:
```bash
chmod 777 scripts/setup_coturn.sh
scripts/setup_coturn.sh
```

2. Add TURN configuration:
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

3. Ensure firewall allows coturn ports.

### Docker Installation

Use the Dockerized coturn service. See [Docker Deployment](/en/getting-started/docker).
