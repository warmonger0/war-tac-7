#!/usr/bin/env python3
"""
Analyze context usage from ADW workflow token database.

This tool examines the token usage database to understand:
1. Which agents/messages consume the most tokens
2. Context efficiency per message
3. Identify messages with low cache efficiency
4. Recommend optimizations

Based on the token monitoring in monitor_adw_tokens.py
"""

import json
import sqlite3
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import argparse


def get_adw_state_db() -> Path:
    """Get path to ADW state database."""
    return Path("adws/state/adw_state.db")


def get_latest_adw_id(db_path: Path) -> str:
    """Get the most recent ADW ID from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT adw_id
        FROM adw_tokens
        ORDER BY created_at DESC
        LIMIT 1
    """)

    result = cursor.fetchone()
    conn.close()

    if not result:
        raise ValueError("No ADW workflows found in database")

    return result[0]


def analyze_adw_context(adw_id: str, db_path: Path) -> Dict:
    """Analyze context usage for an ADW workflow."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all token records for this ADW
    cursor.execute("""
        SELECT
            agent_name,
            message_id,
            input_tokens,
            cache_creation_input_tokens,
            cache_read_input_tokens,
            output_tokens,
            created_at
        FROM adw_tokens
        WHERE adw_id = ?
        ORDER BY created_at ASC
    """, (adw_id,))

    records = cursor.fetchall()
    conn.close()

    if not records:
        return {"error": f"No token records found for ADW {adw_id}"}

    # Analyze by agent
    agent_stats = defaultdict(lambda: {
        "messages": 0,
        "total_input": 0,
        "total_cache_create": 0,
        "total_cache_read": 0,
        "total_output": 0,
        "avg_cache_efficiency": [],
        "low_efficiency_messages": []
    })

    # Track individual messages
    all_messages = []

    for record in records:
        agent_name, message_id, input_tokens, cache_create, cache_read, output_tokens, created_at = record

        # Calculate cache efficiency for this message
        total_input = input_tokens + cache_create + cache_read
        if total_input > 0:
            cache_efficiency = (cache_read / total_input) * 100
        else:
            cache_efficiency = 0

        # Update agent stats
        stats = agent_stats[agent_name]
        stats["messages"] += 1
        stats["total_input"] += input_tokens
        stats["total_cache_create"] += cache_create
        stats["total_cache_read"] += cache_read
        stats["total_output"] += output_tokens
        stats["avg_cache_efficiency"].append(cache_efficiency)

        # Track low efficiency messages (< 80%)
        if cache_efficiency < 80.0 and total_input > 10000:  # Only flag large contexts
            stats["low_efficiency_messages"].append({
                "message_id": message_id,
                "cache_efficiency": cache_efficiency,
                "total_input": total_input,
                "created_at": created_at
            })

        # Add to all messages
        all_messages.append({
            "agent_name": agent_name,
            "message_id": message_id,
            "input_tokens": input_tokens,
            "cache_create": cache_create,
            "cache_read": cache_read,
            "output_tokens": output_tokens,
            "total_input": total_input,
            "cache_efficiency": cache_efficiency,
            "created_at": created_at
        })

    # Calculate averages
    for agent_name, stats in agent_stats.items():
        if stats["avg_cache_efficiency"]:
            stats["avg_cache_efficiency"] = sum(stats["avg_cache_efficiency"]) / len(stats["avg_cache_efficiency"])
        else:
            stats["avg_cache_efficiency"] = 0

    # Sort agents by total input (most expensive first)
    sorted_agents = sorted(
        agent_stats.items(),
        key=lambda x: x[1]["total_cache_create"] + x[1]["total_cache_read"] + x[1]["total_input"],
        reverse=True
    )

    # Find bottleneck messages (largest context)
    bottleneck_messages = sorted(
        all_messages,
        key=lambda x: x["total_input"],
        reverse=True
    )[:10]

    # Find low efficiency messages
    low_efficiency_messages = [
        msg for msg in all_messages
        if msg["cache_efficiency"] < 80.0 and msg["total_input"] > 10000
    ]
    low_efficiency_messages.sort(key=lambda x: x["cache_efficiency"])

    return {
        "adw_id": adw_id,
        "total_messages": len(all_messages),
        "agents": dict(sorted_agents),
        "bottleneck_messages": bottleneck_messages,
        "low_efficiency_messages": low_efficiency_messages[:20],  # Top 20 worst
        "all_messages": all_messages
    }


def calculate_potential_savings(analysis: Dict) -> Dict:
    """Calculate potential token savings from optimizations."""

    recommendations = []

    # Check for agents with consistently low cache efficiency
    for agent_name, stats in analysis["agents"].items():
        if stats["avg_cache_efficiency"] < 85.0 and stats["messages"] > 5:
            # Estimate savings if we improved cache efficiency to 90%
            current_cache_read = stats["total_cache_read"]
            total_context = stats["total_input"] + stats["total_cache_create"] + stats["total_cache_read"]

            # If we had 90% efficiency, cache_read would be 0.9 * total_context
            potential_cache_read = total_context * 0.9
            potential_savings = potential_cache_read - current_cache_read

            # Convert to cost (cache read is $0.30 per 1M tokens for Sonnet 4.5)
            cost_per_million = 0.30
            potential_cost_savings = (potential_savings / 1_000_000) * cost_per_million

            recommendations.append({
                "agent": agent_name,
                "current_efficiency": stats["avg_cache_efficiency"],
                "messages": stats["messages"],
                "potential_token_savings": int(potential_savings),
                "potential_cost_savings": potential_cost_savings,
                "recommendation": f"Improve context reuse for {agent_name} - currently at {stats['avg_cache_efficiency']:.1f}% efficiency"
            })

    # Check for large context messages with low efficiency
    large_inefficient = [
        msg for msg in analysis["low_efficiency_messages"]
        if msg["total_input"] > 50000
    ]

    if large_inefficient:
        total_wasted = sum(
            msg["total_input"] * (1 - msg["cache_efficiency"]/100)
            for msg in large_inefficient
        )

        recommendations.append({
            "issue": "Large messages with low cache efficiency",
            "count": len(large_inefficient),
            "wasted_tokens": int(total_wasted),
            "recommendation": "These messages load >50k tokens with <80% cache efficiency. Consider breaking into smaller contexts or improving .claudeignore"
        })

    return {
        "recommendations": sorted(recommendations, key=lambda x: x.get("potential_cost_savings", 0), reverse=True)
    }


def print_analysis(analysis: Dict, show_messages: bool = False):
    """Print formatted analysis."""

    if "error" in analysis:
        print(f"Error: {analysis['error']}")
        return

    print("=" * 70)
    print(f"📊 ADW Context Analysis: {analysis['adw_id']}")
    print("=" * 70)
    print()

    print("📈 OVERVIEW")
    print(f"  Total messages: {analysis['total_messages']}")
    print(f"  Agents involved: {len(analysis['agents'])}")
    print()

    # Agent breakdown
    print("🤖 AGENT BREAKDOWN (by total context)")
    for i, (agent_name, stats) in enumerate(list(analysis["agents"].items())[:10], 1):
        total_context = stats["total_input"] + stats["total_cache_create"] + stats["total_cache_read"]
        avg_per_msg = total_context // stats["messages"] if stats["messages"] > 0 else 0

        efficiency_emoji = "✅" if stats["avg_cache_efficiency"] >= 85 else "⚠️" if stats["avg_cache_efficiency"] >= 75 else "🔴"

        print(f"  {i}. {agent_name}")
        print(f"     Messages: {stats['messages']}")
        print(f"     Total context: {total_context:,} tokens")
        print(f"     Avg per message: {avg_per_msg:,} tokens")
        print(f"     {efficiency_emoji} Avg cache efficiency: {stats['avg_cache_efficiency']:.1f}%")
        if stats["low_efficiency_messages"]:
            print(f"     ⚠️  {len(stats['low_efficiency_messages'])} messages with <80% efficiency")
        print()

    # Bottleneck messages
    if analysis["bottleneck_messages"]:
        print("🔥 TOP BOTTLENECK MESSAGES (largest context)")
        for i, msg in enumerate(analysis["bottleneck_messages"][:5], 1):
            efficiency_emoji = "✅" if msg["cache_efficiency"] >= 85 else "⚠️" if msg["cache_efficiency"] >= 75 else "🔴"
            print(f"  {i}. {msg['agent_name']} - Message {msg['message_id'][:8]}")
            print(f"     Total context: {msg['total_input']:,} tokens")
            print(f"     {efficiency_emoji} Cache efficiency: {msg['cache_efficiency']:.1f}%")
            print(f"     Breakdown: {msg['input_tokens']:,} input + {msg['cache_create']:,} cache create + {msg['cache_read']:,} cache read")
        print()

    # Low efficiency messages
    if analysis["low_efficiency_messages"]:
        print("⚠️  LOW EFFICIENCY MESSAGES (<80% cache efficiency)")
        print(f"  Found {len(analysis['low_efficiency_messages'])} messages with poor cache efficiency")
        print()
        for i, msg in enumerate(analysis["low_efficiency_messages"][:10], 1):
            print(f"  {i}. {msg['agent_name']} - {msg['cache_efficiency']:.1f}% efficient")
            print(f"     Context: {msg['total_input']:,} tokens")
            print(f"     This message loaded mostly fresh context, not reusing cache")
        print()

    # Recommendations
    savings = calculate_potential_savings(analysis)
    if savings["recommendations"]:
        print("💡 OPTIMIZATION RECOMMENDATIONS")
        print()
        for i, rec in enumerate(savings["recommendations"], 1):
            print(f"  {i}. {rec.get('agent', rec.get('issue', 'Unknown'))}")
            print(f"     {rec['recommendation']}")
            if "potential_cost_savings" in rec:
                print(f"     Potential savings: {rec['potential_token_savings']:,} tokens (${rec['potential_cost_savings']:.2f})")
            if "wasted_tokens" in rec:
                print(f"     Wasted tokens: {rec['wasted_tokens']:,}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Analyze ADW context usage from token database")
    parser.add_argument("adw_id", nargs="?", help="ADW ID to analyze (or 'latest')")
    parser.add_argument("--db", default="adws/state/adw_state.db", help="Path to state database")
    parser.add_argument("--show-messages", action="store_true", help="Show all messages")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {db_path}")
        sys.exit(1)

    # Get ADW ID
    adw_id = args.adw_id
    if not adw_id or adw_id == "latest":
        try:
            adw_id = get_latest_adw_id(db_path)
            print(f"📍 Analyzing latest ADW: {adw_id}\n")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Analyze
    analysis = analyze_adw_context(adw_id, db_path)

    if args.json:
        # Remove large fields for JSON output
        analysis_copy = analysis.copy()
        if not args.show_messages:
            analysis_copy.pop("all_messages", None)
        print(json.dumps(analysis_copy, indent=2))
    else:
        print_analysis(analysis, show_messages=args.show_messages)


if __name__ == "__main__":
    main()
