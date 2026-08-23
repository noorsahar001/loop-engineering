#!/usr/bin/env python3
"""TODO Audit Script - The MAKER
Scans all Python files for TODO, FIXME, HACK, XXX comments.
Summarizes by priority and file location.
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

TODO_PATTERNS = {
    'TODO': re.compile(r'#\s*TODO[:\s]*(.*)', re.IGNORECASE),
    'FIXME': re.compile(r'#\s*FIXME[:\s]*(.*)', re.IGNORECASE),
    'HACK': re.compile(r'#\s*HACK[:\s]*(.*)', re.IGNORECASE),
    'XXX': re.compile(r'#\s*XXX[:\s]*(.*)', re.IGNORECASE),
}

PRIORITY_MAP = {
    'FIXME': 'HIGH',
    'HACK': 'HIGH',
    'XXX': 'MEDIUM',
    'TODO': 'LOW',
}

def scan_file(filepath):
    """Scan a single file for TODO-type comments"""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for todo_type, pattern in TODO_PATTERNS.items():
                    match = pattern.search(line)
                    if match:
                        description = match.group(1).strip() or "(no description)"
                        findings.append({
                            'type': todo_type,
                            'priority': PRIORITY_MAP[todo_type],
                            'line': line_num,
                            'description': description,
                            'file': str(filepath),
                        })
    except Exception as e:
        print(f"ERROR: Could not read {filepath}: {e}")
    return findings

def scan_directory(root_dir):
    """Recursively scan directory for TODO comments"""
    all_findings = []
    scanned_files = 0
    
    for path in Path(root_dir).rglob('*.py'):
        if '__pycache__' in str(path) or '.git' in str(path):
            continue
        if 'wt-' in str(path):
            continue
        findings = scan_file(path)
        all_findings.extend(findings)
        scanned_files += 1
    
    return all_findings, scanned_files

def generate_report(findings, scanned_files):
    """Generate the audit report"""
    report = []
    report.append("=" * 60)
    report.append("TODO AUDIT REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    report.append("")
    report.append(f"Files scanned: {scanned_files}")
    report.append(f"Total findings: {len(findings)}")
    report.append("")
    
    # Group by priority
    by_priority = {}
    for f in findings:
        p = f['priority']
        if p not in by_priority:
            by_priority[p] = []
        by_priority[p].append(f)
    
    for priority in ['HIGH', 'MEDIUM', 'LOW']:
        items = by_priority.get(priority, [])
        report.append(f"--- {priority} PRIORITY ({len(items)} items) ---")
        for item in items:
            rel_path = item['file']
            report.append(f"  {item['type']} in {rel_path}:{item['line']}")
            report.append(f"    {item['description']}")
        report.append("")
    
    # Group by file
    by_file = {}
    for f in findings:
        fn = f['file']
        if fn not in by_file:
            by_file[fn] = []
        by_file[fn].append(f)
    
    report.append("--- FINDINGS BY FILE ---")
    for filepath, items in sorted(by_file.items()):
        report.append(f"\n  {filepath} ({len(items)} items):")
        for item in items:
            report.append(f"    L{item['line']}: [{item['type']}] {item['description']}")
    
    # Summary
    report.append("")
    report.append("=" * 60)
    report.append("SUMMARY")
    report.append(f"  HIGH priority:   {len(by_priority.get('HIGH', []))}")
    report.append(f"  MEDIUM priority: {len(by_priority.get('MEDIUM', []))}")
    report.append(f"  LOW priority:    {len(by_priority.get('LOW', []))}")
    report.append(f"  Total:           {len(findings)}")
    report.append("=" * 60)
    
    return "\n".join(report)

def main():
    """Main entry point"""
    print(f"Starting TODO audit at {datetime.now()}")
    print(f"Scanning directory: {os.getcwd()}")
    print()
    
    findings, scanned_files = scan_directory(os.getcwd())
    report = generate_report(findings, scanned_files)
    print(report)
    
    # Save findings to JSON for programmatic access
    with open('audit_findings.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'files_scanned': scanned_files,
            'total_findings': len(findings),
            'findings': findings,
        }, f, indent=2)
    
    print(f"\nFindings saved to audit_findings.json")
    return 0

if __name__ == '__main__':
    exit(main())
