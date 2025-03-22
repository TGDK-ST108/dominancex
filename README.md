
# DominanceX Firewall

DominanceX is an advanced, modular, encrypted firewall designed to provide secure socket-level protection, real-time control, encrypted logging, AI-driven threat profiling, and seamless integration with OliviaAI and TGDK.

## Quick Download via QR Code
Scan the QR code below to instantly download DominanceX:

![DominanceX Download](dominancex_qr.png)

## Features:
- **AES-256 Encrypted Logging**: Securely log connection attempts.
- **Real-time Firewall Control**: Dynamically manage IP/domain blocking.
- **IPv4/IPv6, DNS-level Protection**: Complete network control.
- **Adaptive AI Integration**: Automatic learning and proactive defense.
- **OliviaAI Support**: Integrates seamlessly for voice alerts and real-time monitoring.

## Installation

Run the provided installer script:
```bash
./deploy_dominancex.sh

Basic Usage:

Launch applications securely:

~/.dominancex/bin/launch_protected.sh curl http://example.com

Manage firewall rules:

Block a domain:

domctl block example.org
domctl reload

Whitelist an IP address:

domctl whitelist 192.168.1.100
domctl reload

Decrypt firewall logs:

decrypt_logs ~/.dominancex/logs/blocked.log

Generate Security Reports:

~/.dominancex/bin/generate_report.sh
cat ~/.dominancex/logs/dominancex_report.txt

Sync Logs Securely:

dominancex.sync

Integration and Customization:

DominanceX is highly customizable and can integrate with various services, including OliviaAI, Elaris nodes, TGDK infrastructure, webhooks, and more. Modify the configuration file located at:

~/.dominancex/config/config.cfg


---

© 2025 Sean Tichenor | TGDK - All Rights Reserved.

