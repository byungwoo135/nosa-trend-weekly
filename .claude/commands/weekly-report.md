---
description: 지난 한 주(월~일)의 노사동향을 조사·요약해 카드뉴스 리포트를 발행한다
---

# 주간 노사동향 카드뉴스 발행

이 커맨드는 저장소 루트(`index.html`, `reports/`, `scripts/`가 있는 디렉터리)에서 실행한다고 가정한다. 먼저 `pwd`로 현재 위치를 확인하고, 저장소 루트가 아니면 이동한다.

## 1. 대상 주(週) 계산

아래를 실행해 이번에 다룰 월~일 날짜 범위를 구한다 (오늘이 일요일이면 오늘까지 포함, 아니면 가장 최근에 끝난 일요일까지).

```bash
python3 - << 'EOF'
import datetime
today = datetime.date.today()
days_since_sunday = (today.weekday() - 6) % 7
end = today - datetime.timedelta(days=days_since_sunday)
start = end - datetime.timedelta(days=6)
print("START", start.isoformat())
print("END", end.isoformat())
print("SLUG", f"{start.isoformat()}_{end.isoformat()}")
print("DATE_RANGE_LABEL", f"{start.strftime('%Y.%m.%d')} ~ {end.strftime('%Y.%m.%d')}")
EOF
```

이 값들(START, END, SLUG, DATE_RANGE_LABEL)을 이후 단계에서 그대로 사용한다.

## 2. 뉴스/자료 검색 (WebSearch)

아래 두 그룹으로 나누어 각각 여러 번 검색한다. 검색 결과는 STEP 1의 날짜 범위(START~END) 안에 게재된 것 위주로 채택하고, 범위를 다소 벗어나더라도 해당 주에 처음 보도된 중대한 사안이면 포함할 수 있다.

**그룹 A — 유통업계** (대형마트, 편의점, 백화점, 이커머스/물류, 프랜차이즈 등)
- "이마트 노조", "쿠팡 노동", "편의점 가맹점 노사", "백화점 노조 파업", "유통업계 임금협상", "물류센터 노동 이슈" 등

**그룹 B — 타 산업군** (전 산업 공통 정책/이슈)
- "최저임금 2026", "근로시간 개편", "노동법 개정", "대기업 노사협상 파업", "고용노동부 발표", "중대재해처벌법", "노란봉투법" 등

**우선 출처** (검색 시 아래를 명시적으로 함께 검색하거나 결과에서 발견되면 우선 채택)
- HR Insight (hrinsight.co.kr / hrinsight.com), 인사관리협회, 월간 인사관리 등 HR 전문 매체
- 고용노동부(moel.go.kr), 노동위원회 등 정부·공공기관 보도자료

각 그룹에서 HR 관점(정책 변화 / 주의 깊게 봐야 하는 사건 / 이슈)으로 가장 중요한 2~4건을 선정한다. 항목마다 다음을 기록:
- `headline`: 15자 내외 헤드라인
- `summary`: 1~2문장 자체 요약 (원문 인용 금지, 팩트만 자기 언어로 재서술)
- `source_name`: 매체명
- `source_url`: 원문 링크
- `published`: 보도일 (YYYY.MM.DD)

찾은 자료가 그룹당 2건 미만이면 검색어를 넓혀 최소 2건은 확보한다.

## 3. JSON 원본 데이터 저장

`reports/{SLUG}.json`에 아래 구조로 저장한다:

```json
{
  "week_start": "START",
  "week_end": "END",
  "retail": [ { "headline": "...", "summary": "...", "source_name": "...", "source_url": "...", "published": "..." } ],
  "other": [ { "headline": "...", "summary": "...", "source_name": "...", "source_url": "...", "published": "..." } ]
}
```

## 4. 카드뉴스 HTML 생성

`reports/_template.html`을 열어 구조/CSS를 그대로 유지한 채, 다음만 교체한다 (색상·서체는 Kurly Nextmile BI 가이드라인 고정값이므로 임의 변경 금지 — Main Color: Kurly Purple `#5f0080`, Sub Color: Nextmile Orange `#ff7b3c`, 국문서체 SD산돌고딕Neo1 / 영문서체 GT America):
- `{{DATE_RANGE}}` → DATE_RANGE_LABEL
- `{{PUBLISH_DATE}}` → 오늘 날짜 (YYYY.MM.DD)
- `유통업계` 섹션의 `.items` 안에 STEP 2 그룹 A 항목들을 `.item` 블록으로 반복 생성 (템플릿의 예시 `.item` 블록을 패턴으로 복제)
- `타 산업군` 섹션의 `.items` 안에 그룹 B 항목들을 동일하게 반복 생성
- 항목이 3~4개로 늘어나 세로 공간이 부족해 보이면 `.item-summary`를 1문장으로 줄이거나 `font-size`를 1~2px 낮춰서 **반드시 스크롤 없이 1080×1350 안에 다 들어가도록** 조정한다 (조건: 한 장에 모든 내용이 요약돼 들어가야 함)

완성된 HTML을 `reports/{SLUG}.html`로 저장한다.

## 5. PNG 캡처

```bash
.venv/bin/python scripts/capture.py reports/{SLUG}.html reports/{SLUG}.png
```

## 6. 결과 확인

Browser 도구로 `reports/{SLUG}.html`을 1080×1350 뷰포트에서 열어 스크린샷으로 스크롤 없이 한 화면에 다 들어가는지, 두 섹션이 명확히 구분되는지 육안 확인한다. 넘치면 STEP 4로 돌아가 내용을 줄인다.

## 7. index.html 갱신

`index.html`의 `<div class="grid" id="archive">` 안에서:
- 리포트가 처음이면 `<div class="empty">...</div>`를 제거
- 아래 카드를 **맨 앞**(최신순)에 추가:

```html
<a class="card-link" href="reports/{SLUG}.html">
  <img src="reports/{SLUG}.png" alt="{DATE_RANGE_LABEL} 노사동향 리포트" loading="lazy" />
  <div class="card-meta">
    <div class="week">WEEKLY REPORT</div>
    <div class="range">{DATE_RANGE_LABEL}</div>
  </div>
</a>
```

## 8. 배포

```bash
git add index.html reports/{SLUG}.html reports/{SLUG}.png reports/{SLUG}.json
git commit -m "Add weekly report {SLUG}"
git push origin main
```

푸시 실패 시(원격 미설정 등) 원인을 확인하고 사용자에게 보고한다. 자동화 과정에서 예상치 못한 상황(검색 결과 부족, 저장소 접근 불가 등)이 발생하면 임의로 넘어가지 말고 무엇이 문제였는지 명확히 기록해 다음 실행/사용자 확인 시 알 수 있게 한다.
