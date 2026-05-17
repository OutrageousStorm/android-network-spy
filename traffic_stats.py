#!/usr/bin/env python3
"""
traffic_stats.py -- Per-app network traffic analysis
Shows bandwidth usage by app — sent/received bytes
Usage: python3 traffic_stats.py [--top 10] [--watch]
"""
import subprocess, re, time, argparse
from collections import defaultdict

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def parse_traffic():
    stats = adb("cat /proc/net/dev | tail -n +3")
    traffic = defaultdict(lambda: {"recv": 0, "sent": 0})

    for line in stats.splitlines():
        parts = line.split()
        if len(parts) < 10:
            continue
        iface = parts[0].rstrip(':')
        recv = int(parts[1])
        sent = int(parts[9])

        if recv > 0 or sent > 0:
            traffic[iface] = {"recv": recv, "sent": sent}

    return traffic

def bytes_to_human(b):
    if b < 1024: return f"{b}B"
    if b < 1024**2: return f"{b/1024:.1f}KB"
    return f"{b/1024**2:.1f}MB"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--watch", action="store_true", help="Monitor continuously")
    args = parser.parse_args()

    print("\n🕵️  Network Traffic Stats\n")
    print(f"{'Interface':<20} {'Received':<15} {'Sent':<15} {'Total'}")
    print("─"*60)

    traffic = parse_traffic()
    items = sorted(traffic.items(), key=lambda x: x[1]["recv"] + x[1]["sent"], reverse=True)

    for iface, stats in items[:args.top]:
        total = stats["recv"] + stats["sent"]
        print(f"{iface:<20} {bytes_to_human(stats['recv']):<15} {bytes_to_human(stats['sent']):<15} {bytes_to_human(total)}")

    if args.watch:
        print("\nWatching (Ctrl+C to stop)...\n")
        time.sleep(2)
        try:
            while True:
                print("\n[Update]")
                traffic = parse_traffic()
                items = sorted(traffic.items(), key=lambda x: x[1]["recv"] + x[1]["sent"], reverse=True)
                for iface, stats in items[:args.top]:
                    total = stats["recv"] + stats["sent"]
                    print(f"{iface:<20} {bytes_to_human(stats['recv']):<15} {bytes_to_human(stats['sent']):<15}")
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    main()
