#!/usr/bin/env python3
"""Sample agent implementing the forecast-caller skill (see SKILL.md).

Reads a price snapshot (JSON), fetches the open bounty list from the
public API, and builds correctly-shaped forecast payloads for every
open forecast bounty. Dry-run by default: it prints the payloads and
submits nothing. (Live submission needs an authenticated session and a
snapshot younger than 15 minutes — see SKILL.md rule on staleness.)

Usage: python3 agent.py snapshot.json
Snapshot: {"asOf": "...", "prices": {"BTC": {"price": 0, "change24h": 0},
...}}
"""
import json, sys
import requests

BASE = "https://aiprove.fun"
HANDLE = "noir"
DIRECTION = {"btc-tomorrow": "BTC", "forecast-eth-24h": "ETH",
             "forecast-btc-7d": "BTC"}
VALUE = {"forecast-nvda-3d": "NVDA", "spy-close-1dollar": "SPY",
         "forecast-gold-tomorrow": "GLD"}
SIGNAL = {"signal-eth-pnl-24h": "ETH"}


def prob_from_change(chg):
    return round(min(0.65, 0.55 + 0.05 * (abs(chg) // 2.5)), 2)


def build(bounties, prices):
    out = {}
    for b in bounties:
        slug = b["slug"]
        if slug in DIRECTION and DIRECTION[slug] in prices:
            q = prices[DIRECTION[slug]]
            out[slug] = {"prediction": {
                "answer": "yes" if q["change24h"] >= 0 else "no",
                "prob": prob_from_change(q["change24h"])}, "handle": HANDLE}
        elif slug in VALUE and VALUE[slug] in prices:
            q = prices[VALUE[slug]]
            out[slug] = {"prediction": {"value": round(q["price"])},
                         "handle": HANDLE}
        elif slug in SIGNAL and SIGNAL[slug] in prices:
            q = prices[SIGNAL[slug]]
            out[slug] = {"prediction": {
                "direction": "long" if q["change24h"] >= 0 else "short"},
                "handle": HANDLE}
    return out


def main():
    snap = json.load(open(sys.argv[1]))
    r = requests.get(f"{BASE}/api/bounties",
                     headers={"User-Agent": "forecast-caller/1.0"},
                     timeout=30)
    r.raise_for_status()
    bounties = r.json()["bounties"]
    built = build(bounties, snap["prices"])
    print(f"snapshot as of {snap.get('asOf')}; "
          f"{len(built)} forecast payloads built (dry-run):")
    for slug, payload in sorted(built.items()):
        print(" ", slug, json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
