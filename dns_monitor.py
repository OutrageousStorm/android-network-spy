#!/usr/bin/env python3
"""
dns_monitor.py -- Monitor Android DNS queries in real time
Shows every domain lookup with timestamp and app
Usage: python3 dns_monitor.py [--filter keyword]
"""
import subprocess, re, argparse

def stream_dns(filter_kw=None):
    print("\n🕵️  DNS Monitor — Ctrl+C to stop\n")
    print(f"{'Time':<10} {'App':<30} {'Domain':<40}")
    print("─"*80)

    proc = subprocess.Popen(
        "adb logcat -v time *:V | grep -E 'getaddrinfo|DNS|resolve'",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )

    try:
        for line in proc.stdout:
            # Parse domain from logcat
            domain_m = re.search(r'([\w\-]+\.[\w\-\.]+\.[\w]{2,})', line)
            if not domain_m:
                continue
            domain = domain_m.group(1)

            if filter_kw and filter_kw.lower() not in domain.lower():
                continue

            time_m = re.search(r'(\d{2}:\d{2}:\d{2})', line)
            time_str = time_m.group(1) if time_m else "??:??:??"

            # Extract app from logcat tag
            app = re.search(r'(\S+):', line)
            app_str = app.group(1) if app else "unknown"

            print(f"{time_str:<10} {app_str:<30} {domain:<40}")
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        proc.terminate()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", help="Filter domains by keyword")
    args = parser.parse_args()
    stream_dns(args.filter)

if __name__ == "__main__":
    main()
