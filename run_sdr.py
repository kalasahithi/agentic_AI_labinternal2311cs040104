"""
Multi-agent SDR (Sales Development Rep) system.

Three cooperating agents, each a separate LLM-driven step:
  1. LeadGenAgent      - finds prospects matching an Ideal Customer Profile
  2. QualificationAgent - scores/tiers them (BANT-style: Hot / Warm / Cold)
  3. EmailAgent        - drafts personalized outreach for qualified leads

Emails are DRAFTED ONLY (dry-run, saved under sdr_system/output/outbox/) -
this never sends real email.

Usage:
    python run_sdr.py
    python run_sdr.py "VP or Head of Sales at SaaS companies with 100-500 employees"
"""

import sys

from sdr_system.orchestrator import SDRPipeline

DEFAULT_ICP = (
    "Senior sales leaders (VP, Head of, Director level) with budget authority "
    "at mid-market B2B companies (50-1000 employees) who are likely to need "
    "a sales engagement / prospecting tool."
)


def main():
    icp_description = " ".join(sys.argv[1:]) or DEFAULT_ICP

    print("=" * 70)
    print("MULTI-AGENT SDR SYSTEM")
    print("=" * 70)
    print(f"ICP: {icp_description}")

    pipeline = SDRPipeline()
    result = pipeline.run(icp_description)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Leads generated : {len(result['leads'])}")
    hot = sum(1 for q in result["qualified"] if q.get("tier") == "Hot")
    warm = sum(1 for q in result["qualified"] if q.get("tier") == "Warm")
    cold = sum(1 for q in result["qualified"] if q.get("tier") == "Cold")
    print(f"Qualified        : {len(result['qualified'])} (Hot={hot}, Warm={warm}, Cold={cold})")
    print(f"Emails drafted   : {len(result['drafts'])} (saved to sdr_system/output/outbox/, not sent)")
    print("\nFull results in sdr_system/output/*.json")


if __name__ == "__main__":
    main()
