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

## 2. 컬리넥스트마일 연관성 파악 (매 실행 시 필수)

이 리포트는 컬리넥스트마일(유통·택배업, 새벽배송/콜드체인/3PL 물류 자회사)을 위해 발행된다. 검색으로 채택할 기사들이 우리 회사와 어떻게 연결되는지 판단할 수 있도록, 아래 핵심 리스크 축을 항상 기준으로 삼는다 (이미 알려진 배경 — 매번 새로 검색할 필요는 없지만, WebSearch 중 컬리/컬리넥스트마일 관련 신규 소식이 발견되면 우선 반영한다):

- **위탁(특수형태근로종사자) 배송기사의 근로자성/산재보험 적용** — 컬리넥스트마일 자체가 이 쟁점으로 소송을 겪은 바 있음(2023년 1심 근로기준법상 근로자 인정, 2025년 항소심은 특수형태근로종사자로서 산재보험 특례 대상으로 판단). 배달 라이더·택배기사 근로자성 관련 판결·입법은 모두 직접 관련.
- **3PL(제3자 물류대행) 확장에 따른 원청 사용자성 노출** — 노란봉투법(개정 노동조합법) 기반 원청 교섭의무·사용자성 판단 기준이 넓어지는 판결/사건은 직접 관련.
- **물류센터(대규모 시급제 인력) 운영** — 최저임금, 폭염 등 근로시간·휴게 규제, 산업안전 이슈는 직접 관련.
- 반대로 오프라인 대형마트·백화점의 폐점/구조조정처럼 사업 구조 자체가 다른 이슈는 특별한 연결고리가 없는 한 '관련 없음'으로 둔다.

각 후보 기사에 대해 위 기준으로 관련 여부를 판단하고, 관련이 있다면 왜 관련 있는지 한 줄로 적어둔다 (`kurly_reason`). 과도하게 모든 기사에 태그를 붙이지 말고, 실질적 연결고리가 있는 경우에만 표시한다 — 신뢰도가 태그 개수보다 중요하다.

## 3. 뉴스/자료 검색 (WebSearch)

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

각 그룹에서 HR 관점(정책 변화 / 주의 깊게 봐야 하는 사건 / 이슈)으로 중요한 항목을 선정한다. **개수를 그룹 간에 억지로 맞추지 않는다** — 그 주에 실제로 중요한 사안이 많으면 최대 8건까지, 적으면 최소 4건까지만 싣는다 (검색을 충분히 넓혀도 4건이 안 되면 STEP 3 세부 카테고리 중 안 훑은 것을 추가로 검색한다. 그래도 부족하면 임의로 채우지 말고 확보한 건수만큼만 발행하고 사유를 남긴다).

**정렬 우선순위**: 각 그룹 안에서 **정책/제도 변화(법 개정, 판결, 정부·위원회 발표 등)를 다루는 항목을 먼저 배치**하고, 그 다음에 개별 기업·업계 동향 항목을 배치한다. 정책 변화가 특정 업계 기사에 직접적인 계기가 된 경우(예: 판결 → 그 판결에 대한 업계 반응 기사) 그 둘을 붙여서 배치한다.

항목마다 다음을 기록:
- `headline`: 15자 내외 헤드라인
- `summary`: 1~2문장 자체 요약 (원문 인용 금지, 팩트만 자기 언어로 재서술)
- `source_name`: 매체명
- `source_url`: 원문 링크 (반드시 실제 검색 결과에 있는 URL)
- `published`: 보도일 (YYYY.MM.DD)
- `policy`: true/false — 정책·제도·판결 변화를 다루는 항목이면 true
- `kurly_related`: true/false — STEP 2 기준으로 컬리넥스트마일과 실질적 연관이 있으면 true
- `kurly_reason`: kurly_related가 true일 때만, 왜 관련 있는지 한 줄 설명 (내부 기록용, 카드에는 노출 안 함)

## 4. JSON 원본 데이터 저장

`reports/{SLUG}.json`에 아래 구조로 저장한다:

```json
{
  "week_start": "START",
  "week_end": "END",
  "summary": [ "이번 주 핵심 요약 1문장", "핵심 요약 2문장", "핵심 요약 3문장" ],
  "retail": [ { "headline": "...", "summary": "...", "source_name": "...", "source_url": "...", "published": "...", "policy": false, "kurly_related": false, "kurly_reason": "" } ],
  "other": [ { "headline": "...", "summary": "...", "source_name": "...", "source_url": "...", "published": "...", "policy": false, "kurly_related": false, "kurly_reason": "" } ]
}
```
정책 우선 정렬을 반영해 배열 순서 자체를 이미 정책 항목이 앞에 오도록 저장한다.

`summary`는 이번 주 전체(유통업계+타 산업군을 아울러)에서 HR 담당자가 반드시 알아야 할 핵심을 **정확히 3줄**로 압축한 것이다. 가장 중요한 정책 변화를 1번째 줄에, 그다음 중요한 흐름을 2·3번째 줄에 담는다. 각 줄은 카드에서 한 줄로 표시되므로 간결하게(60자 내외) 작성한다.

## 5. 카드뉴스 HTML 생성

`reports/_template.html`을 열어 구조/CSS를 그대로 유지한 채, 다음만 교체한다 (색상·서체는 Kurly Nextmile BI 가이드라인 고정값이므로 임의 변경 금지 — Main Color: Kurly Purple `#5f0080`, Sub Color: Nextmile Orange `#ff7b3c`, 국문서체 SD산돌고딕Neo1 / 영문서체 GT America):
- `{{DATE_RANGE}}` → DATE_RANGE_LABEL
- `{{PUBLISH_DATE}}` → 오늘 날짜 (YYYY.MM.DD)
- `{{SUMMARY_LINE_1}}` / `{{SUMMARY_LINE_2}}` / `{{SUMMARY_LINE_3}}` → JSON의 `summary` 배열 3줄 (헤더 바로 아래 "📌 이번 주 한눈에 보기" 박스에 표시됨 — 두 섹션보다 위에 위치)
- `유통업계` 섹션의 `.items` 안에 그룹 A 항목들을(JSON에 저장한 순서 그대로, 정책 항목 먼저) `.item` 블록으로 반복 생성 (템플릿의 예시 `.item` 블록을 패턴으로 복제)
- `타 산업군` 섹션의 `.items` 안에 그룹 B 항목들을 동일하게 반복 생성
- **각 `.item`은 `<div>`가 아니라 `<a class="item" href="{source_url}" target="_blank" rel="noopener">`로 작성한다** — 카드에서 헤드라인/요약을 클릭하면 원문 기사로 바로 이동해야 한다
- `kurly_related`가 true인 항목만 `item-headline`을 `item-headline-row`로 감싸고 그 안에 `<span class="kn-badge">CHECK</span>`을 헤드라인 옆에 추가한다 (템플릿에 두 패턴 모두 예시로 들어있음 — 배지 있는 것/없는 것). false인 항목은 배지 없이 기존 `item-headline` 구조 그대로 둔다. 배지 문구는 항상 정확히 "CHECK"로 쓴다 (다른 문구로 바꾸지 않는다).
- **항목 수에 따라 밀도를 조정한다** (한 섹션에 담기는 개수 기준):
  - 4~5개: 기본 스타일 그대로 사용
  - 6~7개: 그 섹션의 `.items`에 `tier-b` 클래스 추가 (`<div class="items tier-b">`)
  - 8개: `.items`에 `tier-c` 클래스 추가하고 `item-summary`를 반드시 1문장으로 압축
- 그래도 넘칠 것 같으면 `.item-summary` 문장을 더 줄이거나 헤더 padding을 살짝 줄여서 **`.card`(1080×1350) 안에는 다 들어가도록** 조정한다 (조건: 카드 한 장에 모든 내용이 요약돼 들어가야 함). `.card` 바깥(아래에 새로 붙는 `.opinion-section`)까지 넘치는 건 정상이며 문제가 아니다 — 카드 자체만 1350px를 넘지 않으면 된다.
- **`html, body`에 `overflow: hidden`이나 고정 `height: 1350px`를 절대 다시 추가하지 않는다.** 이 페이지는 PNG 캡처(카드 부분만) 용도와 사람이 브라우저로 직접 열어보는 용도를 겸하는데, `overflow: hidden`을 넣으면 브라우저 창이 1350px보다 작을 때 카드 아래(타 산업군 뒷부분, 담당자 코멘트 칸)를 스크롤해서 볼 수 없게 된다. 캡처는 `.card`가 정확히 1080×1350이고 Playwright 뷰포트도 1080×1350이라 `overflow: hidden` 없이도 카드 부분만 정확히 잘려서 찍힌다.
- `</div>`로 `.card`가 끝난 바로 다음, `</body>` 앞에 담당자가 수기로 의견을 남길 수 있는 영역을 항상 그대로 추가한다 (문구를 바꾸지 않는다):
  ```html
  <div class="opinion-section">
    <div class="opinion-box">
      <div class="opinion-title">📝 담당자 코멘트</div>
      <div class="opinion-hint">이번 주 리포트를 보고 느낀 의견이나 챙겨야 할 액션을 자유롭게 적어주세요.</div>
      <div class="opinion-content" contenteditable="true" data-placeholder="여기를 클릭해서 의견을 작성하세요."></div>
    </div>
  </div>
  ```
  이 영역은 매주 항상 빈 상태로 발행한다 (내용을 임의로 채우지 않는다) — 사용자가 직접 브라우저에서 클릭해 손으로 작성하는 칸이다. `.card` 밖에 있으므로 PNG 캡처에는 포함되지 않는다.

완성된 HTML을 `reports/{SLUG}.html`로 저장한다.

## 6. PNG 캡처

```bash
.venv/bin/python scripts/capture.py reports/{SLUG}.html reports/{SLUG}.png
```

## 7. 결과 확인

Browser 도구로 `reports/{SLUG}.html`을 1080×1350 뷰포트에서 열어 스크린샷으로 `.card` 영역이 스크롤 없이 한 화면에 다 들어가는지, 상단 3줄 요약 박스가 큼직하게 채워져 있는지, 두 섹션이 명확히 구분되는지, 정책 항목이 각 섹션 상단에 오는지, CHECK 배지가 실질적 연관이 있는 항목에만 붙어있는지, 맨 아래 담당자 코멘트 칸이 비어 있는 채로 존재하는지 육안 확인한다. `.card`가 넘치면 STEP 5로 돌아가 내용을 줄인다.

## 8. index.html 갱신

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

## 9. 배포

```bash
git add index.html reports/{SLUG}.html reports/{SLUG}.png reports/{SLUG}.json
git commit -m "Add weekly report {SLUG}"
git push origin main
```

푸시 실패 시(원격 미설정 등) 원인을 확인하고 사용자에게 보고한다. 자동화 과정에서 예상치 못한 상황(검색 결과 부족, 저장소 접근 불가 등)이 발생하면 임의로 넘어가지 말고 무엇이 문제였는지 명확히 기록해 다음 실행/사용자 확인 시 알 수 있게 한다.
