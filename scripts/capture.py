#!/usr/bin/env python3
"""HTML 카드뉴스를 PNG로 캡처한다.

Usage:
  카드(1080x1350)만 캡처:  .venv/bin/python scripts/capture.py <input.html> <output.png>
  전체 페이지 캡처(공유용): .venv/bin/python scripts/capture.py <input.html> <output.png> full
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

CARD_WIDTH = 1080
CARD_HEIGHT = 1350


def capture(html_path: str, png_path: str, width: int = CARD_WIDTH, height: int = CARD_HEIGHT) -> None:
    """뷰포트를 정확히 width x height로 잡고 그 영역만 캡처한다 (카드 전용, 아래 opinion-section 등은 잘려서 안 보임)."""
    html_file = Path(html_path).resolve()
    if not html_file.exists():
        raise FileNotFoundError(html_file)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.goto(html_file.as_uri())
        page.wait_for_timeout(200)
        page.screenshot(path=png_path)
        browser.close()


def capture_full_page(html_path: str, png_path: str, width: int = CARD_WIDTH) -> None:
    """페이지 전체(카드 + PPT/이미지 링크 + 담당자 코멘트 칸까지)를 스크롤 없이 한 장으로 캡처한다."""
    html_file = Path(html_path).resolve()
    if not html_file.exists():
        raise FileNotFoundError(html_file)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 1000}, device_scale_factor=2)
        page.goto(html_file.as_uri())
        page.wait_for_timeout(200)
        page.screenshot(path=png_path, full_page=True)
        browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: capture.py <input.html> <output.png> [width height | full]", file=sys.stderr)
        sys.exit(1)
    in_path, out_path = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == "full":
        capture_full_page(in_path, out_path)
    else:
        w = int(sys.argv[3]) if len(sys.argv) > 3 else CARD_WIDTH
        h = int(sys.argv[4]) if len(sys.argv) > 4 else CARD_HEIGHT
        capture(in_path, out_path, w, h)
    print(f"Saved {out_path}")
