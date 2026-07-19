# 노사동향 위클리

매주 노사동향(유통업계 / 유통업계 외)을 조사·요약해 한 장짜리 카드뉴스로 발행하는 저장소.

## 구조
- `index.html` — 발행된 리포트 아카이브 갤러리
- `reports/` — 주차별 `{start}_{end}.html` / `.png` / `_full.png` / `.pptx` / `.json`
- `reports/_template.html` — 카드뉴스 디자인 템플릿 (1080×1350 고정)
- `reports/assets/avatar.jpg` — 담당자 코멘트 박스에 쓰이는 아바타 사진 (모든 리포트 공유)
- `reports/assets/save-comment.js` — 담당자 코멘트 "💾 저장" 버튼 스크립트 (모든 리포트 공유, 아래 참고)
- `scripts/capture.py` — HTML → PNG 캡처 스크립트 (Playwright, 카드 전용/전체 페이지 두 모드)
- `scripts/make_pptx.py` — JSON → 편집 가능한 PPT(.pptx) 생성 스크립트 (python-pptx)
- `.claude/commands/weekly-report.md` — 검색부터 발행까지 전체 절차를 담은 슬래시 커맨드

## 로컬 환경
```bash
python3 -m venv .venv
./.venv/bin/pip install playwright python-pptx Pillow
./.venv/bin/playwright install chromium
```

## 담당자 코멘트 저장 (💾 저장 버튼)
이 사이트는 백엔드가 없는 정적 GitHub Pages라, 코멘트를 "저장"해서 모두에게 영구 반영하려면 브라우저에서 곧바로 GitHub API로 그 리포트 파일을 커밋하는 수밖에 없다. 그래서 각 리포트 페이지의 저장 버튼을 처음 누르면 이 저장소에 쓰기 권한이 있는 GitHub fine-grained PAT(Contents: Read and write, 이 저장소로 범위 한정)를 한 번 물어보고, 이후에는 그 브라우저의 localStorage에 저장되어 다시 묻지 않는다. 토큰은 서버로 전송되지 않고 오직 이 브라우저에서 api.github.com 호출에만 쓰인다.

## 수동 실행
Claude Code에서 이 저장소 루트를 열고 `/weekly-report` 실행.

## 자동 실행
매주 일요일 18:00(Asia/Seoul)에 `/weekly-report`를 실행하는 예약 작업으로 등록되어 있음. `.claude/settings.local.json`(gitignore됨)에 이 자동화가 쓰는 도구 권한을 미리 allow해둬서 사람 없이도 승인 프롬프트 없이 끝까지 진행된다.
