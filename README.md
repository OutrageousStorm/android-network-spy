# 🕵️ Android Network Spy

Rust CLI to analyze Android network traffic dumps. Parse pcap files, find suspicious domains, aggregate by app.

## Usage

```bash
# Capture on device
adb shell tcpdump -i any -w /sdcard/capture.pcap

# Pull and analyze
adb pull /sdcard/capture.pcap
cargo run -- capture.pcap

# Find domains
cargo run -- capture.pcap --domains

# Top talkers
cargo run -- capture.pcap --top 10
```

## Requirements
```bash
cargo install pcap
rustc 1.70+
```
