#!/usr/bin/env python3
"""
domain_extractor.py -- Extract all domains contacted by Android device
Requires: tcpdump running on device
Usage: python3 domain_extractor.py [--output domains.txt] [--duration 300]
"""
import subprocess, re, argparse, time
from collections import defaultdict

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout

def start_tcpdump(device_ip="127.0.0.1", duration=300):
    """Start tcpdump on device and capture to PC"""
    print(f"Starting tcpdump for {duration}s...")
    # Capture DNS queries (port 53)
    proc = subprocess.Popen(
        f"adb shell 'tcpdump -i any -n -v port 53' | tee /tmp/dns_capture.txt",
        shell=True, stdout=subprocess.PIPE, text=True
    )
    time.sleep(duration)
    proc.terminate()
    return "/tmp/dns_capture.txt"

def extract_domains_from_tcpdump(logfile):
    """Parse tcpdump output to extract domains"""
    domains = defaultdict(int)
    
    with open(logfile) as f:
        for line in f:
            # Look for DNS queries: "A? example.com"
            match = re.search(r'A\?\s+([a-z0-9\-\.]+\.[a-z]{2,})', line, re.IGNORECASE)
            if match:
                domain = match.group(1).lower()
                domains[domain] += 1
    
    return domains

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60, help="Capture duration in seconds")
    parser.add_argument("--output", help="Save domains to file")
    args = parser.parse_args()

    print("\n🔍 Android Domain Extractor")
    print("=" * 45)
    print("This captures all DNS queries from your device.")
    print("Use this to see which servers your apps are contacting.\n")

    logfile = start_tcpdump(duration=args.duration)
    domains = extract_domains_from_tcpdump(logfile)

    sorted_domains = sorted(domains.items(), key=lambda x: -x[1])
    
    print(f"\nFound {len(sorted_domains)} unique domains:\n")
    for domain, count in sorted_domains[:50]:
        print(f"  {domain:<40} ({count} queries)")

    if args.output:
        with open(args.output, 'w') as f:
            for domain, count in sorted_domains:
                f.write(f"{domain} {count}\n")
        print(f"\n✓ Saved to {args.output}")

if __name__ == "__main__":
    main()
