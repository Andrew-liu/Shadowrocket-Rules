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
DEFAULT_APPLE_DOMAIN_SOURCE_URL = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Apple/Apple_Domain.list"
GENERATED_RULE_FILES = (
    "Advertising.list",
    "Apple_Domain.list",
)
OWNED_RULE_FILES = (
    "AI.list",
    "Apple.list",
    "ApplePush.list",
    "Google.list",
    "HK_Broker.list",
)
COPY_FILES = OWNED_RULE_FILES + ("LICENSE",)
AUTO_STATS_START = "<!-- AUTO-STATS:START -->"
AUTO_STATS_END = "<!-- AUTO-STATS:END -->"
MIN_AD_RULE_COUNT = 10000
MIN_APPLE_DOMAIN_RULE_COUNT = 1000
ALLOWED_AD_RULE_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "DOMAIN-WILDCARD",
    "IP-CIDR",
    "IP-CIDR6",
}
ALLOWED_RULE_TYPES = ALLOWED_AD_RULE_TYPES | {
    "USER-AGENT",
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
    parser.add_argument(
        "--apple-domain-source",
        default=os.environ.get("APPLE_DOMAIN_SOURCE", DEFAULT_APPLE_DOMAIN_SOURCE_URL),
    )
    parser.add_argument("--validate", action="store_true", help="Validate generated release files before publishing.")
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


def convert_apple_domain_rules(source_text: str) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    for raw_line in source_text.splitlines():
        line = strip_inline_comment(raw_line)
        if not line or line.startswith("#") or "," in line:
            continue

        domain = line.lstrip(".").strip().lower()
        if not domain or "." not in domain or " " in domain:
            continue

        converted = f"DOMAIN-SUFFIX,{domain}"
        if converted not in seen:
            seen.add(converted)
            result.append(converted)

    if not result:
        raise RuntimeError("No Apple domain rules were converted from source")

    return result


def build_advertising_list(ad_rules: list[str], ad_source: str, build_time: dt.datetime) -> str:
    header = [
        "# Shadowrocket-Rules Advertising.list",
        "# Generated from Shadowrocket-ADBlock-Rules-Forever sr_ad_only.conf",
        f"# Source: {ad_source}",
        f"# Build time: {build_time.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"# Rule Count: {len(ad_rules)}",
        "# Policy is supplied by Shadowrocket.conf RULE-SET target group.",
        "",
    ]
    return "\n".join(header + ad_rules) + "\n"


def build_apple_domain_list(apple_domain_rules: list[str], apple_domain_source: str, build_time: dt.datetime) -> str:
    header = [
        "# Shadowrocket-Rules Apple_Domain.list",
        "# Generated from blackmatrix7 Apple_Domain.list bare domain set",
        f"# Source: {apple_domain_source}",
        f"# Build time: {build_time.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"# Rule Count: {len(apple_domain_rules)}",
        "# Policy is supplied by Shadowrocket.conf RULE-SET target group.",
        "",
    ]
    return "\n".join(header + apple_domain_rules) + "\n"


def build_shadowrocket_conf(repo_root: Path, build_time: dt.datetime) -> str:
    conf = (repo_root / "Shadowrocket.conf").read_text(encoding="utf-8")
    today = build_time.strftime("%Y-%m-%d")

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
    conf = conf.replace(
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/WeChat/WeChat.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/WeChat/WeChat.list",
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


def iter_rule_lines(text: str) -> list[str]:
    result: list[str] = []
    for raw_line in text.splitlines():
        line = strip_inline_comment(raw_line)
        if not line or line.startswith("#") or (line.startswith("[") and line.endswith("]")):
            continue
        result.append(line)
    return result


def count_rules(path: Path) -> int:
    return len(iter_rule_lines(path.read_text(encoding="utf-8", errors="ignore")))


def extract_rule_count_header(text: str, file_name: str) -> int:
    match = re.search(r"^# Rule Count:\s*(\d+)\s*$", text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"{file_name} is missing Rule Count header")
    return int(match.group(1))


def build_readme(
    repo_root: Path,
    output: Path,
    ad_source: str,
    apple_domain_source: str,
    build_time: dt.datetime,
) -> str:
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    rule_files = GENERATED_RULE_FILES + OWNED_RULE_FILES
    rows = []
    for file_name in rule_files:
        rule_path = output / file_name
        if rule_path.exists():
            rows.append(f"| `{file_name}` | {count_rules(rule_path)} |")

    stats_block = "\n".join(
        [
            AUTO_STATS_START,
            f"- 更新时间（UTC）：`{build_time.strftime('%Y-%m-%d %H:%M:%S')}`",
            f"- 广告规则源：`{ad_source}`",
            f"- Apple 域名源：`{apple_domain_source}`",
            "",
            "| 规则文件 | 规则数 |",
            "|----------|--------:|",
            *rows,
            AUTO_STATS_END,
        ]
    )

    pattern = re.compile(f"{re.escape(AUTO_STATS_START)}.*?{re.escape(AUTO_STATS_END)}", re.DOTALL)
    if pattern.search(readme):
        return pattern.sub(stats_block, readme)

    return readme.rstrip() + "\n\n## 自动统计\n\n" + stats_block + "\n"


def validate_rule_file(path: Path) -> list[str]:
    errors: list[str] = []
    for line_no, line in enumerate(iter_rule_lines(path.read_text(encoding="utf-8", errors="ignore")), start=1):
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 2:
            errors.append(f"{path.name}: invalid rule at parsed line {line_no}: {line}")
            continue
        if parts[0].upper() not in ALLOWED_RULE_TYPES:
            errors.append(f"{path.name}: unsupported rule type {parts[0]} at parsed line {line_no}")
        if not parts[1]:
            errors.append(f"{path.name}: empty rule value at parsed line {line_no}")
    return errors


def validate_release(output: Path) -> None:
    required_files = ("Shadowrocket.conf", "README.md") + GENERATED_RULE_FILES + OWNED_RULE_FILES
    missing = [file_name for file_name in required_files if not (output / file_name).exists()]
    errors = [f"Missing release file: {file_name}" for file_name in missing]

    conf_path = output / "Shadowrocket.conf"
    if conf_path.exists():
        conf = conf_path.read_text(encoding="utf-8", errors="ignore")
        if "refs/heads/main" in conf:
            errors.append("Shadowrocket.conf still contains refs/heads/main")
        if "rule/QuantumultX/WeChat/WeChat.list" in conf:
            errors.append("Shadowrocket.conf still references QuantumultX WeChat rules")
        if "rule/Shadowrocket/WeChat/WeChat.list" not in conf:
            errors.append("Shadowrocket.conf does not reference Shadowrocket WeChat rules")
        if f"{REPO_RAW_RELEASE}/Apple_Domain.list" not in conf:
            errors.append("Shadowrocket.conf does not reference generated Apple_Domain.list")

    ad_path = output / "Advertising.list"
    if ad_path.exists():
        ad_text = ad_path.read_text(encoding="utf-8", errors="ignore")
        header_count = extract_rule_count_header(ad_text, "Advertising.list")
        actual_count = count_rules(ad_path)
        if header_count != actual_count:
            errors.append(f"Advertising.list Rule Count mismatch: header={header_count}, actual={actual_count}")
        if actual_count < MIN_AD_RULE_COUNT:
            errors.append(f"Advertising.list rule count is too low: {actual_count}")

    apple_domain_path = output / "Apple_Domain.list"
    if apple_domain_path.exists():
        apple_domain_text = apple_domain_path.read_text(encoding="utf-8", errors="ignore")
        header_count = extract_rule_count_header(apple_domain_text, "Apple_Domain.list")
        actual_count = count_rules(apple_domain_path)
        if header_count != actual_count:
            errors.append(f"Apple_Domain.list Rule Count mismatch: header={header_count}, actual={actual_count}")
        if actual_count < MIN_APPLE_DOMAIN_RULE_COUNT:
            errors.append(f"Apple_Domain.list rule count is too low: {actual_count}")

    for rule_path in sorted(output.glob("*.list")):
        errors.extend(validate_rule_file(rule_path))

    if errors:
        raise RuntimeError("Release validation failed:\n" + "\n".join(f"- {error}" for error in errors))


def reset_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output = args.output.resolve()
    build_time = dt.datetime.now(dt.timezone.utc)

    reset_output(output)

    source_text = read_text_from_source(args.ad_source)
    ad_rules = convert_ad_rules(source_text)
    (output / "Advertising.list").write_text(
        build_advertising_list(ad_rules, args.ad_source, build_time), encoding="utf-8"
    )

    apple_domain_source_text = read_text_from_source(args.apple_domain_source)
    apple_domain_rules = convert_apple_domain_rules(apple_domain_source_text)
    (output / "Apple_Domain.list").write_text(
        build_apple_domain_list(apple_domain_rules, args.apple_domain_source, build_time), encoding="utf-8"
    )

    (output / "Shadowrocket.conf").write_text(build_shadowrocket_conf(repo_root, build_time), encoding="utf-8")

    for file_name in COPY_FILES:
        src = repo_root / file_name
        if src.exists():
            shutil.copy2(src, output / file_name)

    (output / "README.md").write_text(
        build_readme(repo_root, output, args.ad_source, args.apple_domain_source, build_time), encoding="utf-8"
    )

    if args.validate:
        validate_release(output)
        print("Release validation passed")

    print(f"Built release at {output}")
    print(f"Advertising rules: {len(ad_rules)}")
    print(f"Apple domain rules: {len(apple_domain_rules)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"build_release.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
