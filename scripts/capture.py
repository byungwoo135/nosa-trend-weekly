#!/usr/bin/env python3
"""HTML 카드뉴스를 고정 크기 PNG로 캡처한다.

Usage: .venv/bin/python scripts/capture.py <input.html> <output.png> [width] [height]
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

CARD_WIDTH = 1080
CARD_HEIGHT = 1350


def capture(html_path: str, png_path: str, width: int = CARD_WIDTH, height: int = CARD_HEIGHT) -> None:
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


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: capture.py <input.html> <output.png> [width] [height]", file=sys.stderr)
        sys.exit(1)
    in_path, out_path = sys.argv[1], sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else CARD_WIDTH
    h = int(sys.argv[4]) if len(sys.argv) > 4 else CARD_HEIGHT
    capture(in_path, out_path, w, h)
    print(f"Saved {out_path}")
