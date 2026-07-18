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

**깊고 넓게, 그러나 정확하게** 검색한다. 그룹당 최소 8회 이상 서로 다른 키워드로 검색하고, 아래 카테고리를 최대한 골고루 훑어 후보를 넉넉히 모은 다음, 그중 날짜·출처가 명확히 확인된 것만 채택한다. 검색 결과는 STEP 1의 날짜 범위(START~END) 안에 게재된 것 위주로 채택하고, 범위를 다소 벗어나더라도 해당 주에 처음 보도된 중대한 사안이면 포함할 수 있다.

**그룹 A — 유통업계** (아래 세부 카테고리를 나눠서 각각 검색)
- 대형마트/SSM: 이마트, 홈플러스, 롯데마트 노사 이슈
- 편의점: CU, GS25, 세븐일레븐 가맹·노조·최저임금 이슈
- 백화점·면세점: 신세계, 롯데, 현대 및 입점업체 노동 이슈
- 이커머스/물류/배송: 쿠팡, 마켓컬리, 배달 라이더, 택배기사(CJ대한통운 등) 관련 판결·교섭·근로환경
- 프랜차이즈/외식유통: 가맹점 노동 이슈

**그룹 B — 타 산업군** (아래 세부 카테고리를 나눠서 각각 검색)
- 제조/완성차: 현대차, 기아, 삼성전자 등 임단협·파업
- 금융: 은행권/금융노조 임단협, 주4.5일제 등 근로시간 이슈
- 공공/공무원: 공무원노조, 공공기관 노사 이슈
- 노동정책/입법: 최저임금, 근로시간 개편, 노동법 개정, 노란봉투법, 중대재해처벌법
- 노동위원회·법원 판결: 대법원/고법/중노위의 노동 관련 주요 판결·결정
- 총연맹 동향: 민주노총, 한국노총 등 상급단체의 성명·투쟁 일정

**우선 출처** (검색 시 아래를 명시적으로 함께 검색하거나 결과에서 발견되면 우선 채택)
- HR Insight (hrinsight.co.kr / hrinsight.com), 매일노동뉴스, 참여와혁신 등 HR·노동 전문 매체
- 고용노동부(moel.go.kr), 대법원(scourt.go.kr), 중앙노동위원회 등 정부·공공기관 발표·판결

**정확성 원칙** (안전하게 검색하기 위한 규칙):
- 날짜가 START~END 범위 안인지 검색 스니펫에서 직접 확인한 것만 채택한다. 발행일이 불명확하거나 추정에 의존해야 하는 항목은 버린다.
- 같은 사안이라도 서로 다른 매체 기사가 있으면 날짜가 가장 명확한 쪽을 source로 쓴다.
- 헤드라인·요약에 검색 결과에 없는 숫자·인용을 지어내지 않는다 (환각 금지). 애매하면 보수적으로 표현한다.
- source_url은 검색 결과에 실제로 등장한 URL만 사용한다.

각 그룹에서 HR 관점(정책 변화 / 주의 깊게 봐야 하는 사건 / 이슈)으로 가장 중요한 항목을 선정한다. **그룹당 기본 4~5건을 목표로 하고, 검색을 넓혀도 도저히 못 채우는 경우에도 최소 3건은 확보한다.** 항목마다 다음을 기록:
- `headline`: 15자 내외 헤드라인
- `summary`: 1~2문장 자체 요약 (원문 인용 금지, 팩트만 자기 언어로 재서술)
- `source_name`: 매체명
- `source_url`: 원문 링크 (반드시 실제 검색 결과에 있는 URL)
- `published`: 보도일 (YYYY.MM.DD)

그룹당 3건 미만이면 STEP 2 세부 카테고리 중 아직 검색하지 않은 것들을 추가로 검색해 최소 3건을 확보한다. 그래도 부족하면 임의로 채우지 말고 실제 확보한 건수만큼만 발행하고 사유를 남긴다.

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
- **각 `.item`은 `<div>`가 아니라 `<a class="item" href="{source_url}" target="_blank" rel="noopener">`로 작성한다** — 카드에서 헤드라인/요약을 클릭하면 원문 기사로 바로 이동해야 한다 (템플릿 예시에 이미 이 패턴이 적용돼 있음)
- 기본 4~5개 항목 기준으로 이미 여백이 맞춰진 템플릿이므로 보통은 그대로 채우면 된다. 그래도 항목이 많거나 요약이 길어 넘칠 것 같으면 `.item-summary`를 1문장으로 더 줄이거나 `font-size`를 1px 정도 낮춰서 **반드시 스크롤 없이 1080×1350 안에 다 들어가도록** 조정한다 (조건: 한 장에 모든 내용이 요약돼 들어가야 함)

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
