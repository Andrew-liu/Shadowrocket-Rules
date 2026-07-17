#!/usr/bin/env python3
"""Build release artifacts for Shadowrocket-Rules."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path

REPO_RAW_RELEASE = "https://raw.githubusercontent.com/Andrew-liu/Shadowrocket-Rules/refs/heads/release"
DEFAULT_AD_SOURCE_URL = "https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/release/sr_ad_only.conf"
OWNED_RULE_FILES = (
    "AI.list",
    "Apple.list",
    "ApplePush.list",
    "Google.list",
    "HK_Broker.list",
)
COPY_FILES = OWNED_RULE_FILES + ("README.md", "LICENSE")
ALLOWED_AD_RULE_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "DOMAIN-WILDCARD",
    "IP-CIDR",
    "IP-CIDR6",
}
REJECT_POLICIES = {
    "REJECT",
    "REJECT-DICT",
    "REJECT-ARRAY",
    "REJECT-200",
    "REJECT-IMG",
    "REJECT-TINYGIF",
    "REJECT-DROP",
    "REJECT-NO-DROP",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Shadowrocket-Rules release files.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "dist")
    parser.add_argument("--ad-source", default=os.environ.get("AD_RULE_SOURCE", DEFAULT_AD_SOURCE_URL))
    return parser.parse_args()


def read_text_from_source(source: str) -> str:
    source_path = Path(source).expanduser()
    if source_path.exists():
        return source_path.read_text(encoding="utf-8", errors="ignore")

    with urllib.request.urlopen(source, timeout=120) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="ignore")


def strip_inline_comment(line: str) -> str:
    if " #" in line:
        return line.split(" #", 1)[0].strip()
    return line.strip()


def convert_ad_rules(source_text: str) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    in_rule_section = False

    for raw_line in source_text.splitlines():
        line = strip_inline_comment(raw_line)
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_rule_section = line.lower() == "[rule]"
            continue
        if not in_rule_section:
            continue

        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 3:
            continue

        rule_type = parts[0].upper()
        if rule_type not in ALLOWED_AD_RULE_TYPES:
            continue

        reject_index = next((i for i, part in enumerate(parts[2:], start=2) if part.upper() in REJECT_POLICIES), -1)
        if reject_index == -1:
            continue

        converted_parts = [rule_type] + parts[1:reject_index] + parts[reject_index + 1 :]
        if len(converted_parts) < 2 or not converted_parts[1]:
            continue

        converted = ",".join(converted_parts)
        if converted not in seen:
            seen.add(converted)
            result.append(converted)

    if not result:
        raise RuntimeError("No ad rules were converted from source")

    return result


def build_advertising_list(ad_rules: list[str], ad_source: str) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    header = [
        "# Shadowrocket-Rules Advertising.list",
        "# Generated from Shadowrocket-ADBlock-Rules-Forever sr_ad_only.conf",
        f"# Source: {ad_source}",
        f"# Build time: {now}",
        f"# Rule Count: {len(ad_rules)}",
        "# Policy is supplied by Shadowrocket.conf RULE-SET target group.",
        "",
    ]
    return "\n".join(header + ad_rules) + "\n"


def build_shadowrocket_conf(repo_root: Path) -> str:
    conf = (repo_root / "Shadowrocket.conf").read_text(encoding="utf-8")
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    conf = re.sub(r"^# 更新时间: .*$", f"# 更新时间: {today}", conf, flags=re.MULTILINE)
    conf = re.sub(
        r"^update-url\s*=\s*.*$",
        f"update-url = {REPO_RAW_RELEASE}/Shadowrocket.conf",
        conf,
        flags=re.MULTILINE,
    )
    conf = conf.replace(
        "https://raw.githubusercontent.com/Andrew-liu/Shadowrocket-Rules/refs/heads/main/",
        f"{REPO_RAW_RELEASE}/",
    )
    conf = re.sub(
        r"RULE-SET,https://raw\.githubusercontent\.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Advertising/Advertising\.list,🛑 广告拦截",
        f"RULE-SET,{REPO_RAW_RELEASE}/Advertising.list,🛑 广告拦截",
        conf,
    )
    conf = re.sub(
        r"RULE-SET,https://raw\.githubusercontent\.com/Andrew-liu/Shadowrocket-Rules/refs/heads/(?:main|release)/Advertising\.list,🛑 广告拦截",
        f"RULE-SET,{REPO_RAW_RELEASE}/Advertising.list,🛑 广告拦截",
        conf,
    )
    return conf


def reset_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output = args.output.resolve()

    reset_output(output)

    source_text = read_text_from_source(args.ad_source)
    ad_rules = convert_ad_rules(source_text)
    (output / "Advertising.list").write_text(build_advertising_list(ad_rules, args.ad_source), encoding="utf-8")
    (output / "Shadowrocket.conf").write_text(build_shadowrocket_conf(repo_root), encoding="utf-8")

    for file_name in COPY_FILES:
        src = repo_root / file_name
        if src.exists():
            shutil.copy2(src, output / file_name)

    print(f"Built release at {output}")
    print(f"Advertising rules: {len(ad_rules)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"build_release.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
