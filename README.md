# 노사동향 위클리

매주 노사동향(유통업계 / 유통업계 외)을 조사·요약해 한 장짜리 카드뉴스로 발행하는 저장소.

## 구조
- `index.html` — 발행된 리포트 아카이브 갤러리
- `reports/` — 주차별 `{start}_{end}.html` / `.png` / `.pptx` / `.json`
- `reports/_template.html` — 카드뉴스 디자인 템플릿 (1080×1350 고정)
- `scripts/capture.py` — HTML → PNG 캡처 스크립트 (Playwright)
- `scripts/make_pptx.py` — JSON → 편집 가능한 PPT(.pptx) 생성 스크립트 (python-pptx)
- `.claude/commands/weekly-report.md` — 검색부터 발행까지 전체 절차를 담은 슬래시 커맨드

## 로컬 환경
```bash
python3 -m venv .venv
./.venv/bin/pip install playwright python-pptx
./.venv/bin/playwright install chromium
```

## 수동 실행
Claude Code에서 이 저장소 루트를 열고 `/weekly-report` 실행.

## 자동 실행
매주 일요일 18:00(Asia/Seoul)에 `/weekly-report`를 실행하는 예약 작업으로 등록되어 있음.
