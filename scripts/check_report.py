#!/usr/bin/env python3
"""리포트 JSON을 발행 전에 검증한다: 중복 출처 링크, 빈/잘못된 URL 등.

발견되면 문제를 출력하고 exit code 1로 종료한다 (문제 없으면 0).

Usage: .venv/bin/python scripts/check_report.py reports/{SLUG}.json
"""
import json
import sys


def check(json_path: str) -> list[str]:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    problems = []
    seen_urls: dict[str, str] = {}

    for section in ("retail", "other"):
        for item in data.get(section, []):
            headline = item.get("headline", "(제목 없음)")
            url = item.get("source_url", "")

            if not url or not url.startswith("http"):
                problems.append(f"잘못된/빈 source_url: '{headline}' -> '{url}'")
                continue

            if url in seen_urls:
                problems.append(
                    f"중복 링크: '{headline}' 와 '{seen_urls[url]}' 가 같은 URL을 가리킴 -> {url}"
                )
            else:
                seen_urls[url] = headline

    for section in ("retail", "other"):
        items = data.get(section, [])
        if len(items) < 4:
            problems.append(f"{section} 섹션 항목이 {len(items)}개뿐 (최소 4개 필요)")

    return problems


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_report.py <report.json>", file=sys.stderr)
        sys.exit(1)

    issues = check(sys.argv[1])
    if issues:
        print(f"❌ {len(issues)}개 문제 발견:")
        for p in issues:
            print(" -", p)
        sys.exit(1)
    else:
        print("✅ 문제 없음 (중복 링크 없음, 항목 수 충족)")
        sys.exit(0)
