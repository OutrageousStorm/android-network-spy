# 🔍 Android Network Spy

Monitor and analyze all network traffic from your Android device — see what data apps are sending.

## Tools

| Tool | What it does |
|------|-------------|
| `traffic_monitor.py` | Real-time network traffic sniffer |
| `data_analyzer.py` | Analyze saved traffic captures |
| `domain_extractor.py` | Extract all domains contacted by device |

## Setup

```bash
# Requires: adb, tcpdump installed on device
adb shell "which tcpdump" || echo "Install: apt install tcpdump"

# Monitor all traffic from device
python3 traffic_monitor.py

# Analyze a saved PCAP
python3 data_analyzer.py capture.pcap
```
