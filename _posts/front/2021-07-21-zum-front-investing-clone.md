---
layout: post
title: INVESTING.COM 클론 코딩(feat. Vue JS SSR, CANVAS API)
description: 신입 프론트엔드 개발자들이 파일럿 프로젝트로 진행한 INVESTING.COM 클론 코딩 경험을 공유합니다.
image: /images/front/post/2021-07-21-zum-front-investing-clone/0-thumbnail.png
introduction: 신입 프론트엔드 개발자들이 파일럿 프로젝트로 진행한 INVESTING.COM 클론 코딩 경험을 공유합니다.
category: portal/tech
tag: [Frontend, pilot, 회고, javascript, Vue.js, CANVAS API, SSR, Typescript]
author: karl
---

> **파일럿 프로젝트** <br>줌인터넷 서비스개발팀 프론트엔드 파트 주니어 개발자들이 수습 기간 동안진행했던 파일럿 프로젝트 입니다. 진행된 프로젝트는 [GitHub 레포지토리](https://github.com/zuminternet/investing-app-clone)에서 확인하실 수 있습니다.

<br>

<p style="text-align: right">
  <img style="margin: 0; display: inline-block;" src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=http%3A%2F%2Flocalhost%3A4000%2Fzum-front-investing-clone%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false" alt="조회수" />
</p>

# 1. 프로젝트 개요

## 1.1. 프로젝트 주제

파일럿 프로젝트의 의의는 미리 실무를 위한 웹 서비스 기반 지식, 기술을 습득하여 신규 입사자들이 보다 빨리 실무에 적응할 수 있도록 하는 데 있습니다.

그리고 파일럿 프로젝트가 끝나면 바로 줌닷컴 신규 서비스 개발 프로젝트에 투입될 예정이었습니다. 미리 도메인에 대해 학습케하여 더욱 실무 적응을 돕고 프로젝트를 성공적으로 수행할 수 있게끔 하고자 했습니다.

두 마리 토끼를 잡을 수 있도록 주제를 선정해야 했습니다.

그래서 ..

### [INVESTING.COM](http://investing.COM) 클론코딩

![1](/images/front/post/2021-07-21-zum-front-investing-clone/1.jpg)

앞으로 진행될 프로젝트에선 주식, 원자재, 가상화폐 등의 자산들을 폭넓게 다룰 예정입니다. 많은 투자 지표들을 상세히 다루고 캔들 차트, 라인 차트 등 풍부한 그래픽 자료를 제공해야 합니다.

그러한 컨텐츠를 이미 제공하고 있는 [INVESTING.COM](http://investing.COM) 이 있었습니다. [INVESTING.COM](http://investing.COM) 은 전세계 거래소 250곳의 실시간 데이터, 관련 뉴스 및 분석을 44개의 언어로 제공하는 금융시장 플랫폼입니다. 월간 2,100만 명의 이용자를 자랑합니다. 투자자들이 한 번에 필요한 정보를 모두 확인할 수 있는 장소를 제공하는 것을 목표로 하고 있습니다.

이러한 서비스를 클론 코딩하면서 기술적, 도메인적 이슈를 해결하는 경험, 실무에 필요한 지식 및 기술을 얻을 수 있으리라 생각했습니다.

이러한 이유로 [INVESTING.COM](http://investing.COM) 을 클론 코딩 하기로 했습니다.

개발은 5. 10 ~ 6. 24 까지 약 7주간 이루어졌습니다.

## 1.2. 요구사항

### 1.2.1 기술적 요구사항

- 필수
  - 공통
    - `zum-portal-core-js` (사내 라이브러리) 완벽 이해 및 사용
  - Front-end
    - `Vue.js 2`
    - `Webpack`
    - 차트
      - `Canvas API`, `SVG API`를 이용해서 직접 만들어보기
      - 그 후 `ChartIQ`, `Highcharts` 등 응용해보기
      - 성능 최적화

    - 초기 렌더링 `SSR`, 이후 `CSR` 사용
    - 번들 용량 최적화
    - 비즈니스 로직에 `TypeScript` 사용
    - `SASS` 사용
    - 비동기 프로그래밍 최적화 (로딩 전/후 처리)
  - Back-end
    - `Node.js` + `Express.js` + `Typescript` 사용
    - `Cache` + `Scheduling` 적극 사용
    - 주식 관련 외부 API는 자유롭게 선택 사용
    - 회원 시스템
      - `OAuth 2.0` (구글 로그인)
      - `JWT` 인증
      - 이메일/ 비밀번호/ 닉네임을 통한 일반 로그인
      - 마이페이지 (닉네임/ 비밀번호 수정)

    - `DB`는 자유롭게 선택
- 선택
  - Front-end
    - 동적 컴포넌트 (`Dynamic Component`, `Composition API` 사용)
    - `Vue Component`에 `TypeScript` 적용
  - Back-end
    - `TypeORM` 사용

### 1.2.2 기능적 요구 사항

- 필수
  - 기본 테마/ 다크 테마 지원
  - 로그인
    - Google 로그인
    - 일반 로그인
    - 자동 로그인
  - 뉴스 및 분석
    - 피드 (카테고리 별 뉴스)
    - 상세 페이지
      - 타이틀, 컨텐츠, 매체사, 작성일을 렌더링
    - 스와이프 기능으로 카테고리 이동
  - 실시간 시세
    - 자산(주식, 가상화폐, 지수)의 실시간 가격
  - 종목별 상세페이지
    - 차트
      - 확대, 축소
      - 구간 변경
      - 형태 변경
    - 종목 상세 정보
    - 뉴스탭
    - 종목 의견(댓글)

- 선택
  - 뉴스 및 분석
    - 무한스크롤, 댓글, 검색
  - 실시간 시세
    - 정렬(가격, 등락률)
  - 즐겨찾기 및 검색

## 1.3. 프로젝트 기능 소개

![2](/images/front/post/2021-07-21-zum-front-investing-clone/2.png)

우선 간단하게 태스크들을 정의하고 분배하였습니다. 무엇을 해야 할지 인지한 상태에서 개발을 시작할 수 있었습니다.

~~검색, 관심목록은 저렇게 나눌 땐 몰랐는데 양이 만만치 않았습니다...~~

크게 공통 개발 기능, 개별 개발 기능 두 가지로 나누어 개발하였습니다.

공통 개발 기능은 모두가 한번씩 구현해보기로 했습니다. 전체 UI 구성과 로그인은 실무 내내 다룰 것입니다. 앞으로 많은 실무 프로젝트를 수행하기 위해선 차트에 대한 이해가 필수적입니다. 그래서 이 세 부분을 공통 개발 기능에 추가했습니다.

개별 개발 기능은 각자가 전담하여 자신의 코딩 스타일, 역량을 잘 드러내도록 개발하였습니다. 신규 입사자들을 더 파악하여 팀에 잘 녹아들 수 있도록 도움을 주기 위해서입니다.

### 1.3.1 공통 개발 기능

### Google 및 자동 로그인

![3](/images/front/post/2021-07-21-zum-front-investing-clone/3.gif)

재민 님 프로젝트

- `OAuth 2.0`을 활용해 Google 로그인을 구현했습니다.
- 로그인 시도 서버에서 회원 여부를 검토합니다.
- 미가입 사용자라면 가입 후 로그인합니다.
- 로그인과 동시에 `JWT(JSON Web Tokens)`이 발행되고 이후 자동 로그인에 사용합니다

### 이메일 회원가입 및 로그인

![4](/images/front/post/2021-07-21-zum-front-investing-clone/4.gif)

재민 님 프로젝트

- 이메일을 통해 회원가입 및 로그인할 수 있습니다
- 마찬가지로 회원 여부를 검토, 미가입 사용라면 계정을 생성합니다.
- 로그인과 동시에 `JWT`를 발행합니다.

### 마켓 페이지

![5](/images/front/post/2021-07-21-zum-front-investing-clone/5.gif)

도경 님 프로젝트

![6](/images/front/post/2021-07-21-zum-front-investing-clone/6.png)

정훈 님 프로젝트

- 주식, 지수, 가상화폐 전체 종목을 나열 합니다.
- 현재가, 전일 대비 가격 변동이 실시간으로 반영되며 보기 쉽게 강조해줍니다. (상승 시 빨간색, 하락 시 파란색)
- 정렬 기능을 제공합니다. (등락률, 가격, 종목에 대한 내림차 순/ 오름차 순)

### 다크모드 지원 & 스와이프

![7](/images/front/post/2021-07-21-zum-front-investing-clone/7.gif)

재민 님 프로젝트

- 홈페이지에서 버튼 토글링을 통해 기본/다크 모드를 설정할 수 있습니다.
- 스와이프를 통해 탭 간 이동을 할 수 있습니다.

### 비동기 처리 UI(Loading, Error 등)

![8](/images/front/post/2021-07-21-zum-front-investing-clone/8.gif)

정훈 님 프로젝트

![9](/images/front/post/2021-07-21-zum-front-investing-clone/9.gif)

재민 님 프로젝트

![10](/images/front/post/2021-07-21-zum-front-investing-clone/10.gif)

재민 님 프로젝트

- 서버에 요청하는 즉시 데이터가 오는 것은 아니기 때문에 비동기 대응이 필요했습니다.
- 정훈 님은 [Webull](https://www.webull.com/)의 로딩 UI를 참고하셨고, 도경 님과 저는 Spinner Loading을 구현하여 적용하였습니다.
- 이 외 에러 상황, 컨텐츠가 없는 상황도 처리하였습니다.

### 차트

![11](/images/front/post/2021-07-21-zum-front-investing-clone/11.gif)

도경 님 프로젝트

![12](/images/front/post/2021-07-21-zum-front-investing-clone/12.gif)

재민 님 프로젝트

![13](/images/front/post/2021-07-21-zum-front-investing-clone/13.png)

정훈 님 프로젝트

- 모두 `CANVAS API`를 활용하여 라이브러리 없이 제작하였습니다.
- 캔들 차트, 라인 차트를 제공합니다. (형태 변경)
- 1일, 1주, 1달, 1년 등 다양한 기간의 데이터를 제공합니다. (구간 변경)
- 마우스, 손가락 상호작용을 통한 확대, 축소, 드래그를 제공합니다. (확대, 축소)
- 이동평균선, 가격구분선, 일자구분선, 거래량 차트를 제공합니다.

### 1.3.2 개별 개발 기능

### 자산종목 상세 페이지

![14](/images/front/post/2021-07-21-zum-front-investing-clone/14.gif)

재민 님 프로젝트

![15](/images/front/post/2021-07-21-zum-front-investing-clone/15.gif)

재민 님 프로젝트

- 마켓 페이지에서 종목 선택 시 해당 종목의 상세페이지로 이동합니다.
- 가격 정보 박스에서 실시간 가격 변동을 반영합니다.
- 개요 탭에선 종목 차트, 개괄적 정보 및 뉴스, 분석, 의견 일부를 노출합니다.
- 뉴스, 분석, 의견 탭에선 탭에 해당하는 컨텐츠 전부를 노출합니다.
- 상세페이지에서 종목 즐겨찾기 추가/삭제를 할 수 있습니다.

### 관심목록 페이지

![16](/images/front/post/2021-07-21-zum-front-investing-clone/16.gif)

재민 님 프로젝트

- 관심 목록에 등록하면 해당 종목을 빠르게 찾아볼 수 있습니다.
- 종목 상세페이지, 검색페이지에서 북마크 버튼을 통해 관심 종목을 추가/삭제할 수 있습니다.

### 종목검색 페이지

![17](/images/front/post/2021-07-21-zum-front-investing-clone/17.gif)

재민 님 프로젝트

### 댓글 기능

- 검색어(티커 및 이름)에 해당하는 종목, 뉴스 및 분석을 나열합니다.
- 검색어를 입력할 때마다 자동완성을 지원합니다.
- 종목, 뉴스 및 분석을 클릭하면 해당 아이템의 상세페이지로 이동할 수 있습니다.
- 북마크 버튼을 통해 관심 종목을 추가/삭제할 수 있습니다.

![18](/images/front/post/2021-07-21-zum-front-investing-clone/18.gif)

정훈 님 프로젝트

- 종목, 뉴스 및 분석에 관련된 댓글을 달 수 있습니다.
- 로그인 여부를 확인하고, 비 로그인 상태면 로그인 화면으로 리다이렉트 합니다.

![19](/images/front/post/2021-07-21-zum-front-investing-clone/19.gif)

정훈 님 프로젝트

- 댓글에 토글링을 통해 좋아요/ 좋아요 취소를 할 수 있습니다.

### 뉴스, 분석 리스트 및 상세 페이지

![20](/images/front/post/2021-07-21-zum-front-investing-clone/20.gif)

도경 님 프로젝트

- 최신순, 인기순(댓글순)으로 뉴스 리스트를 제공합니다.
- 더 불러오기 기능을 제공합니다.

![21](/images/front/post/2021-07-21-zum-front-investing-clone/21.gif)

도경 님 프로젝트

- 상세 페이지에선 제목, 매체사, 썸네일, 내용, 관련 댓글들을 제공합니다.
- 새로운 댓글을 추가하는 등 댓글 기능을 활용할 수 있습니다.

### 더보기 페이지

![22](/images/front/post/2021-07-21-zum-front-investing-clone/22.gif)

도경 님 프로젝트

- 로그인/ 로그아웃 기능을 제공합니다.
- 닉네임, 비밀번호 변경 기능을 제공합니다.
- 다크모드 ON/OFF 기능을 제공합니다.

# 2. 협업 방법

이번 파일럿 프로젝트는 3명이 같이 진행했기 때문에 협업을 하는 방법도 중요했습니다. 어떤 방식과 도구를 사용해서 협업을 진행했는지 소개하고자 합니다.

### 스크럼

매일 업무를 시작하기 전에 짧은 스크럼을 하여 자신이 했던 업무와 어려운 점, 문제점 등을 공유하고 의견을 나누는 시간을 가졌습니다. 계속해서 서로 하는 일들을 체크하고 조율할 수 있어서 프로젝트를 더욱 원활하게 진행할 수 있었습니다.

### 문서 공유

프로젝트 진행 중 서로 공유할 사항이 생기면 문서로 기록해두었습니다. 문서를 작성하면서 작성하는 사람도 한 번 더 내용을 정리할 수 있었고, 타입을 나눠서 보는 사람들도 나중에 편하게 볼 수 있었습니다.

![23](/images/front/post/2021-07-21-zum-front-investing-clone/23.png)

작성한 스터디, 참고자료 문서들

### 모노레포

서로 비슷하지만, 개별적인 서비스를 개발하므로 마이크로서비스 아키텍처를 적용하기로 했습니다. 마이크로서비스 아키텍처에서는 각각의 서비스들이 독립적이므로 따로 사용하는 패키지를 관리하기 쉬웠고, 개발과정에서 충돌도 더 적었습니다.

그리고 마이크로서비스 아키텍처를 구성하면서 여러 서비스들을 하나의 레포지토리에서 관리할 수 있는 모노레포를 같이 적용했습니다. [yarn workspaces](https://classic.yarnpkg.com/en/docs/workspaces/)로 쉽게 설정할 수 있었는데요, 여러 레포지토리로 구성을 하면 서비스 간의 공통코드를 사용하기가 불편한데 모노레포에서는 이런 점을 쉽게 할 수 있었습니다.

![24](/images/front/post/2021-07-21-zum-front-investing-clone/24.png)

모노레포의 구조

### 코드리뷰

이번 프로젝트를 하면서 새로운 기술 스택을 사용하고 서로 기술에 대한 숙련도의 정도도 달랐기 때문에 코드 품질을 비슷하게 맞추기 위해 코드 리뷰를 활발하게 진행했습니다. 다양한 관점에서 피드백을 주고받으면서 혼자 했을 때보다 더 빠르게 성장할 수 있었습니다.

# 3. 프로젝트 구조

![25](/images/front/post/2021-07-21-zum-front-investing-clone/25.png)

## 3.1. 프로젝트 전체 구조

앞서 협업 관련해서 모노레포에 대해 설명 드렸는데요,

프로젝트 루트에는 패키지들이 저장된 `node_modules` 와 각자가 구현한 패키지들이 있는`packages` , 그리고 각종 설정 파일들로 구성되어 있습니다.

코드 컨벤션을 최대한 편하게 맞출 수 있도록 `eslint`, `prettier`를 설정했고, VSCode extension인 `vetur`에 대한 설정도 추가했습니다.

---

## 3.2 패키지별 구조

본격적인 구현물은 `packages` 안에 있는데요, 각자의 이름을 걸고(...?) 구현한 패키지들과 공용으로 사용할 `common` 패키지로 구성되어 있습니다.

### 3.2.1 개별 서비스 패키지

팀 프로젝트이기 때문에 큰 틀은 유사하게 가져가지만, 신입사원 파일럿 프로젝트인 만큼 **각자의 코드에는 각자의 개성이 드러났으면 좋겠다는 요구사항**이 있었습니다. 이러한 개성은 파일 구조를 구성하는 데에서도 볼 수 있었습니다.

### 도경

![26](/images/front/post/2021-07-21-zum-front-investing-clone/26.png)

### 재민

![27](/images/front/post/2021-07-21-zum-front-investing-clone/27.png)

### 정훈

![28](/images/front/post/2021-07-21-zum-front-investing-clone/28.png)

크게 `backend` - `frontend` 로 나누어 서버단에서 필요한 작업은 `backend`에서, 클라이언트에서 필요한 작업은 `frontend`에서 담당하도록 했습니다. domain 으로 된 부분은 `axios` 응답 데이터처럼 backend-frontend에서 공통으로 사용될 수 있는 인터페이스를 모아 두었습니다.

![29](/images/front/post/2021-07-21-zum-front-investing-clone/29.png)

![30](/images/front/post/2021-07-21-zum-front-investing-clone/30.png)

도경 님과 정훈 님은 DB 사용을 위해 docker를 사용했는데요, 도경 님은 docker 관련 설정을 별도로 분리하고 나머지 프로젝트 로직에 대한 부분은 `src` 폴더로 모은 반면, 정훈 님은 그냥 `wiii` package 루트에 `docker-compose.yml` 만 넣었습니다. ~~_정훈 님 패키지에는 `__tests__` 폴더도 보이긴 하는데요, `흔적기관` 같은 거라 보시면 될 것 같아요..._~~

---

## 3.3 Backend 구조

`backend` 에는 여느 백엔드 프로젝트처럼 `controller` - `service` - db(`repository` - `model`) 로 기능을 분리했습니다. API Key 등 설정 관련 상수는 `config`에 모았습니다. 도경 님은 특별히 `middlewares`를 추가해서, 사용자 인증 관련 미들웨어를 구현했네요.

![31](/images/front/post/2021-07-21-zum-front-investing-clone/31.png)

![32](/images/front/post/2021-07-21-zum-front-investing-clone/32.png)

DB는 저희 모두 `MongoDB`를 사용했는데, ORM으로 도경, 재민 님은 `Mongoose`를, 정훈 님은 `TypeORM`을 사용했습니다. 두 분은 `model`에서 필요한 `schema`만 작성하고 해당 `schema`를 이용하는 로직은 각 Service에서 `mongoose` 기본 API를 활용하는 방식으로 구현했습니다.

`TypeORM`에서도 당연히 `find`, `create` 등 기본적인 CRUD API는 제공하는데요, custom repository를 만들어서 추가적인 로직을 구현할 수 있더라구요. 그래서 `TypeORM` 개념을 따라서 `entity` - `repository`를 구분해 DB 관련한 로직을 구현했습니다. (끝나고 보니 `entity`는 주로 RDBMS 테이블에서 사용하는 개념이라 `MongoDB`에서 사용하는 게 맞는지 잘 모르겠네요.. ~~_디알못이라..)_~~

---

## 3.4 Frontend 구조

저희가 프론트엔드 개발자들이고, 프로젝트 또한 프론트엔드 작업이 중요한 프로젝트이기 때문에 프론트엔드 구조에 대해서는 좀 더 자세히 설명해 드리는 것이 좋을 것 같습니다.

![33](/images/front/post/2021-07-21-zum-front-investing-clone/33.png)

![34](/images/front/post/2021-07-21-zum-front-investing-clone/34.png)

![35](/images/front/post/2021-07-21-zum-front-investing-clone/35.png)

프론트엔드 역시 큰 구조는 유사합니다. Vue 컴포넌트가 들어가는 `components`, 각 페이지를 구성하는 `views`, Vuex 사용을 위한 `stores`, Vue-router 사용을 위한 `router`, 전역에서 사용할 SCSS 변수, 클래스를 위한 `styles`, Axios 등 서버와의 통신 기능을 담당하는 `service`/`api` 등 프로젝트에 필수적인 부분들은 유사하게 구조를 잡았습니다.

`components` 디렉토리는 공통으로 사용하고 있지만, 내부 구성은 조금씩 다르게 구현했습니다. 도경 님과 재민 님은 기능별로 컴포넌트 단위를 나누어 구현했습니다. 도경 님은 Vue의 `Mixin` 컴포넌트도 적절히 사용하셨네요. 정훈 님은 아토믹 디자인 패턴을 적용했는데요, 초반엔 컴포넌트들을 잘게 쪼개는 과정이 필요해서 구현 시간이 좀 더 필요했습니다. 하지만 뒤로 갈수록 높은 재사용성 덕분에 필요한 컴포넌트들을 불러와서 갖다 붙이기만 하면 페이지 하나가 뚝딱뚝딱 만들어지는, 재미있는 경험을 할 수 있었습니다. 여기에 `props`를 좀더 잘 활용하고, `Mixin`도 함께 쓴다면 재사용성이 훨씬 더 높아질 것 같아요.

![36](/images/front/post/2021-07-21-zum-front-investing-clone/36.png)

![37](/images/front/post/2021-07-21-zum-front-investing-clone/37.png)

캔버스 차트를 그리는 로직도 서로 다른데요, 도경 님은 `chart` 디렉토리를 별도로 만들고 내부 로직을 클래스로 구현했습니다. 반면 재민 님과 정훈 님은 함수를 활용해 구현했습니다. 재민 님은 `Chart.vue` 컴포넌트 내부 메서드로 구현했고, 정훈 님은 `utils/chart` 에서 함수로 구현했습니다.

---

![38](/images/front/post/2021-07-21-zum-front-investing-clone/38.png)

## 3.5 `common`

`common` 패키지는 개별 서비스 패키지 구조와 유사하지만, 모두가 공통으로 사용할 컴포넌트와 서비스 로직을 모아둔 패키지입니다. 업무 분배를 통해 담당자가 뉴스, 댓글 등 기능과 컴포넌트를 구현하고, 각자의 서비스에서 마치 `node_modules`의 패키지를 불러와서 사용하는 것처럼 담당 기능을 사용할 수 있도록 했습니다.

별도의 서비스가 아니기 때문에 `resource` 등 불필요한 부분과 `controller` 처럼 각자 구현할 수밖에 없는 부분은 제외했습니다. backend - frontend를 동시에 활용해야 하는 기능을 공용으로 구현하다 보니 코드가 조금 지저분해지는 것은 아쉽긴 하지만 어쩔 수 없었던 것 같아요.

---

프로젝트 전반에 대한 소개는 이 정도로 마무리하고, 각자가 구현하면서 고민했던 내용들에 대해 말씀드리겠습니다.

# 4. 기술적 고민

## 4.1 재민 님의 고민

### 4.1.1 실시간성 보장을 위한 기술 선택 고민

사용자 편의를 위해 마켓 페이지와 종목 상세페이지 내의 가격 정보 변화를 실시간으로 제공해야 했습니다.

이렇게 외부 정보를 받아 동적으로 반영하기 위한 최선의 방법이 무엇일지 고민했습니다.

### 4.1.2 여러 선택지

### WebSocket

- 양방향 통신을 위한 새로운 프로토콜입니다.
- 업그레이드만 하면 하나의 `HTTP` 커넥션으로 자유롭게 양방향 통신이 가능합니다. (`HTTP`는 통신은 본질적으로 일회성, 단방향입니다.)
- 그러나 소켓 연결을 유지하는데 높은 코스트, 항상 연결을 유지하는 것을 전제로 하기에 비정상적으로 연결이 끊겼을 시 복잡한 예외 처리가 필요하므로 코드 복잡도를 올립니다.
- 또한 완벽한 양방향 통신이 필요할 정도로 본 프로젝트는 클라이언트에서 복잡한 루틴을 수행하진 않습니다. 단지 가격 정보를 매번 갱신하는 것이 전부입니다.
- 결국, 리소스 소모 및 구현 부담으로 본 프로젝트엔 과하다 판단했습니다.

### Regular Polling

- 일정하고 짧은 Time(N Time) 간격으로 주기적으로 서버에 `HTTP` 요청하는 방법입니다.
- 구현이 쉽습니다.
- 그러나 실시간성을 보장하기 위해선 N Time을 매우 작게 잡아 짧은 간격으로 계속 요청을 보내야 합니다.
- 서버의 응답이 N Time 보다 느려질 경우, 즉 할당된 시간에 리턴 값이 오지 않는 경우를 처리, 또한 자칫하면 요청의 병목현상이 일어날 수 있습니다.

### SSE(Server-Sent-Event)

- `SSE`에 관련해선 정훈 님이 잘 설명해주셨죠.
- 사실 한번 커넥션을 열어두면 서버는 계속 가격 정보를 보내주면 되기 때문에, 가장 로직이 깔끔할 것이라는 생각이 들었습니다.
- `IE` 미지원, `HTTP` 연결 횟수 제한 등으로 결국 실무에선 쓰기 어려울 것으로 생각해 제외하였습니다.

### 4.1.3 결국 Long Polling

- `WebSocket`은 강력하나 본 프로젝트엔 과한 감이 있었습니다. 그리고 `Regular Polling`은 단순하나 자칫하면 실시간성을 보장하기 어려울 수 있었습니다.
- 결국 절충하여 `Long Polling` 기법을 사용하도록 결정했고, 비교적 간단하게 실시간성을 확보할 수 있었습니다.

### Long Polling 이란?

![39](/images/front/post/2021-07-21-zum-front-investing-clone/39.png)

출처 : [Modern Javascript Tutorials](https://ko.javascript.info/long-polling)

- 본래 `HTTP` 인프라에선 양방향 통신을 지원하지 않습니다.
- 그러므로 클라이언트 측에서 서버와 커넥션이 끊기자마자 바로 재요청하여 커넥션을 엶으로써 양방향 통신을 모사합니다.
- 구현이 간단합니다.
- 이를 통해 최소한의 부담으로 클라이언트가 서버 내 필요한 데이터를 지속해서 추적할 수 있습니다.

### 코드

![40](/images/front/post/2021-07-21-zum-front-investing-clone/40.png)

클라이언트에서 계속 재귀적으로 서버로 주식 관련 데이터를 요청하는 코드

- `subscribeStocks` 메소드는 응답을 기다린 후 커넥션이 끊기자마자 자신을 재귀적으로 호출함으로써 실시간성을 모사하려고 합니다.
- 일단 에러(timeout 등 일반 에러, 커스텀 에러)가 발생하더라도 1초 정도의 유예를 갖고 다시 재귀적 호출합니다.

![41](/images/front/post/2021-07-21-zum-front-investing-clone/41.png)

주식 관련 데이터를 가져오는 `store` 내 `action`

- `action` 내에서 `trycatch`를 통해 에러처리를 맡아서 합니다.
- 에러가 발생하면 `setStocksIsError` 플래그를 활성화해 에러 관련 비동기 컴포넌트를 사용자에게 보여줍니다.

## 4.2 도경 님의 고민

협업을 위해 코드리뷰를 진행하면서 몇 가지 고민들이 생겼습니다.

### 중요한 리뷰에 집중하기

코딩 컨벤션, 린트, 포맷팅, 오타 등 비교적 가벼운 부분들에서 코드 리뷰를 하느라 시간을 많이 쓰는 경향이 있었습니다. 그렇게 되면 중요한 부분에서 리뷰를 놓칠 수 있는 문제가 있습니다. 이를 최소화하기 위해 [husky](https://typicode.github.io/husky/#/)와 같은 도구를 이용해서 커밋, 푸시 훅에서 체크할 수 있는 부분들을 먼저 체크하는 방법이 있습니다. 코드 리뷰 시에는 더 중요한 부분에 집중할 수 있기 때문에 다음 프로젝트부터 적용할 계획입니다.

### 작은 PR 만들기

PR의 코드가 적으면 코드 내의 이슈를 찾기가 쉽습니다. 하지만 PR이 커지게 되면 이슈를 찾기가 어렵고 코드가 괜찮아 보이는 문제가 생기는데요, 그렇기 때문에 PR은 최대한 작게 나누는 것이 좋습니다. 이를 위해 도움이 될만한 것들이 있습니다.

1. 할 일을 명확하게 정하고 측정하기

   작업을 하기 전에 하는 일에 대한 명세를 미리 작성해두면 작업량에 대한 예상과 측정이 쉬워져 미리 PR을 어떻게 나눌지 생각할 수 있습니다. 깃허브의 이슈 또는 자라의 티켓이 많이 사용됩니다.

2. 브랜치를 잘 나누기

   기능 브랜치를 여러 개의 서브 브랜치로 나눠서 작업한 다음 기존 기능 브랜치로 PR를 만들게 되면 작은 PR을 만드는 데 도움이 됩니다.

## 4.3 정훈 님의 고민

### Server Sent Events 적용과 실패 그 사이..

종목별 상세페이지에 있는 차트 컴포넌트를 동적으로 만들어보고자 Server Sent Events(이하 `SSE`)를 적용해보았습니다.

### SSE는 무엇인가

`SSE`는 아래 도표를 보고 설명을 보시면 좀 더 이해하기 쉬우실 것 같아요

![42](/images/front/post/2021-07-21-zum-front-investing-clone/42.png)

(이미지 출처: [https://subscription.packtpub.com/book/web_development/9781782166320/6/ch06lvl1sec43/listening-for-server-sent-events](https://subscription.packtpub.com/book/web_development/9781785888960/6/ch06lvl1sec48/listening-for-server-sent-events))

간단히 설명해 드리면,

일반적인 요청-응답과 동일하게 HTTP/HTTPS 프로토콜을 사용하지만, 클라이언트에서 한번 요청한 이후 `keep-alive`로 연결을 유지하면서 서버에서 계속해서 데이터를 보내는 기술입니다.

양방향 통신으로 지속적인 연결을 하는 `Socket` 과는 달리 단방향 통신을 위해 사용되기 때문에, ~~_(공식적인 확인은 할 수 없었지만)_~~ 트위터, 페이스북의 알림 기능에서도 사용되고, 저희 프로젝트처럼 주식 시세 정보를 실시간으로 보내는 데도 사용될 수 있습니다.

`Socket`에 비해 자주 사용되는 기술은 아니지만, 웹 표준 API([https://html.spec.whatwg.org/multipage/server-sent-events.html](https://html.spec.whatwg.org/multipage/server-sent-events.html))기 때문에 `모던` 브라우저에서는 모두 사용할 수 있어요.

### Socket이 아닌 SSE를 적용한 이유

참고로 했던 타 서비스들 상당수는 시세 관련 데이터를 실시간으로 전송하기 위해 `Socket`을 사용하고 있습니다. 저도 처음엔 `Socket` 쓰는 게 당연하다 생각했죠.

그런데 서버 단에서는 클라이언트에서 연결을 종료할 때까지 지속적으로 응답을 보내기만 하면 되기 때문에, `Socket`에 비해 상대적으로 구현하기 쉬웠고, 단방향 통신만 필요한 상황이어서 `SSE`를 적용하는 것이 괜찮을 것 같다고 판단을 했습니다.

### SSE 적용 결과

SSE는 기존 로직과 크게 다르지 않게 구성할 수 있습니다.

먼저 서버 단에서는 `controller`에서 `response.write` 를 통해 데이터를 추가로 보내는 로직과 `response.end` 를 통해 클라이언트와의 통신이 끊어질 때 로직만 추가해서 구현하면 됩니다. 데이터 객체를 만드는 서비스 로직은 기존에 사용하던 로직 그대로 사용하면 됩니다.

SSE 관련된 서버 단 코드 전부를 아래와 같이 가져왔는데요, `SSE 클래스` 를 만드는 부분 때문에 생소해 보일 순 있지만, 응답 헤더를 지정하고 `response.write`를 조금 더 추상화한 것에 불과합니다.

또 `setInterval`을 사용하는 부분이 있는데, 완전한 실시간 시세 데이터가 아니라 일정 시간 간격으로 캐싱 된 데이터를 보내주는 방식으로 구현했기 때문입니다. 만약 파일럿 프로젝트가 아니라 실 서비스라면 interval이 아니라 현재가가 변동될 때마다 해당 데이터를 보내주는 방식으로 조금 바꾸면 될 것 같아요.

```tsx

/**
 * @see https://github.com/zuminternet/investing-app-clone/blob/main/packages/wiii/backend/controller/SSE.ts
 */
export default class SSE {
  res: Response<any, Record<string, any>>;
  options: any;
  service: MarketService;

  constructor(res: Response, options) {
    this.res = res;
    this.options = options;
    this.setHeader();
  }

  private setHeader() {
    this.res.writeHead(200, {
      /** EventSource 활용 위한 연결 지속 */
      Connection: 'keep-alive',
      /** EventSource 활용 위한 text타입 전송 */
      'Content-Type': 'text/event-stream',
      /** 지정 초(15s)까지 public caching 허용 */
      'Cache-Control': `public, max-age=${times.sse}`,
      /** CORS 허용 */
      'Access-Control-Allow-Origin': 'http://localhost:3000',
    });
  }

  public write(data) {
    this.res.write(`data: ${JSON.stringify(data)}\n\n`);
  }
}

/**
 * @see https://github.com/zuminternet/investing-app-clone/blob/main/packages/wiii/backend/controller/Market.controller.ts
 */
@GetMapping({ path: [marketSubpaths.historical] })
  public async sendHistoricalData(req: Request, res: Response) {
    try {
      const options = parseQueryToOptions(marketName.historical, req.query);

      if (!isOptionsValidate(options)) return res.sendStatus(404);

      /** SSE Response Instance 생성 */
      new SSE(res, options);

      const data = await this.marketService.getCachedHistorical(options);
      this.writeData(data, res);

      const intervalTime = times.sse * 3000;
      const eventSourceInterval = setInterval(async () => {
         const data = await this.marketService.getHistorical(options);
         this.writeData(data, res);
       }, /** 15s */ intervalTime);

      /** 연결 끊어지는 경우 */
      res.end(() => {
        clearInterval(eventSourceInterval);
        console.log(`SSE Ended`);
      });
    } catch (e) {
      console.error(e);
      res.sendStatus(500);
    }
  }

  private async writeData(data, res) {
    res.write(`id: ${new Date()}\n`);
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  }
```

브라우저에서는 `EventSource`라는 웹 API를 사용합니다. `open`, `message`, `error`, `close` 이벤트 각각에 대한 로직만 `addEventListener`로 등록해주면 됩니다.

클래스로 서비스 로직을 구현하다 보니, Vue 컴포넌트 내부 데이터를 변경하기 위해 `dataCarrier`로 `Proxy` 객체를 사용하는 부분 정도 말고는 생소하지 않은 코드죠

```tsx
/**
 * @see [https://github.com/zuminternet/investing-app-clone/blob/main/packages/wiii/frontend/services/chart/eventSource.ts](https://github.com/zuminternet/investing-app-clone/blob/main/packages/wiii/frontend/services/chart/eventSource.ts)
 */

export default class EsService {
  url: string;
  private observer: object;
  private es: EventSource;
  private location: string;

  constructor(query: GetHistoricalOptions, dataCarrier: ProxyConstructor) {
    this.url = this.setUrl(query);
    this.observer = dataCarrier;
    this.location = location.href;

    this.es = new EventSource(this.url);

    this.addEventListers();
  }

  /**
   * sourceUrl
   * undefined로 들어온 쿼리만 제거하고 나머지 예외처리는 서버에서 담당
   */
  private setUrl(query: GetHistoricalOptions) {
    ...
  }

  private addEventListers() {
    this.es.addEventListener(`error`, this.onError.bind(this));
    this.es.addEventListener(`open`, this.onOpen.bind(this));
    this.es.addEventListener(`message`, this.onMessage.bind(this));
  }

  /** 서버 연결 시 로직 */
  private onOpen() {
    console.info(`[SSR:Client] Connection Opened`);
  }

  /** 서버 데이터 받을 때 로직 */
  private onMessage({ data }) {
    /** 페이지 이동시 종료 */
    if (this.location !== location.href) this.onClose();
    try {
      this.observer['data'] = Object.freeze(JSON.parse(data));
    } catch (e) {
      console.error(e);
    }
  }

  /** 에러 발생 시 로직 */
  private onError(e) {
    const {
      target: { readyState },
    } = e;
    readyState === 0
      ? console.log(`[SSE:Client] EventSource on Waiting for Server..`)
      : console.error(`[SSE:Client] EventSource on Error`);
  }

  /** 서버와의 연결 끊어질 때 로직 */
  private onClose() {
    this.es.close();
    console.warn(`[SSR:Client] Connection Closed`);
  }
}
```

![43](/images/front/post/2021-07-21-zum-front-investing-clone/43.png)

위 코드를 devServer로 실행시키면 위와 같이 일정 간격으로 계속해서 차트를 그리게 됩니다. 약 200개 캔들과 이동평균선, 거래량을 캔버스로 그리는 게 했는데, API 요청부터 차트 생성 완료까지 짧게는 20ms 정도밖에 걸리지 않더라구요.

### SSE를 적용했을 때의 문제점

다해서 200줄가량의 간단한 코드인데요, 사실 여기까지 하는데 약간의 시행착오가 있었습니다. 무엇보다 기술 난이도가 어렵다기보다는 제대로 된 레퍼런스를 구하기 어려웠기 때문이죠..

일례로 백엔드 `SSE.ts`의 `writeData` 메서드 코드를 보시면,

```tsx
  private async writeData(data, res) {
    res.write(`id: ${new Date()}\n`);
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  }
```

이렇게 `id`와 `data`를 명시해서 해당 데이터가 어떤 데이터인지 내용은 뭔지 알려줘야 합니다. 이런 간단한 내용에 대해서도 정확히 명세가 적힌 곳이 없어서 블로그, StackOverflow 등등 여기저기를 검색해보고 이것저것 시도해봐야 하더라구요. 결국 구현하고 나서도 이렇게 하는 게 맞나 하는 확신이 잘 들지 않다보니, 다른 프로젝트에서도 사용할 수 있을지에 대해 회의를 가질 수밖에 없었습니다.

![44](/images/front/post/2021-07-21-zum-front-investing-clone/44.png)

또 앞서 SSE는 `모던 브라우저에서 사용가능`하다고 말씀드렸는데요, IE에선 SSE-EventSource를 지원하지 않아서 polyfill을 사용해야 합니다. polyfill을 사용하더라도, IE 9~10 버전에선 HTTP 동시 연결 가능한 수가 6개여서 SSE가 연결 하나를 계속 잡고 있게 되면 다른 API들, 특히 광고나 로그 관련 API를 사용하지 못하게 될 수도 있죠.

저희 서비스 사용자 상당수가 여전히 IE를 사용 중이다 보니, 현실적으로 이 기술을 계속 사용하기는 조금 무리지 않을까 하는 생각이 들었습니다.

앞으로 다른 프로젝트에서 적용하기는 어려울 것 같아 아쉽긴 하지만, SSE라는 신박한 기술을 적용해보기 위해 JS의 Proxy도 써보고, HTTP에 대한 고민도 해봤던 재밌는 경험이었습니다.

# 5. 회고

## 5.1 재민 님의 회고

### 실무를 앞두고 필요한 기술 스택 및 도메인 압축적 습득

입사 전엔 `바닐라 JS`, `React`로 프로젝트를 해왔습니다. `Vue.js`는 입사가 결정된 이후로 간단한 프로젝트를 통해 맛만 보았습니다. 그리고 `TypeScript`, 사내 `Core.js`, `CANVAS API` 등 새롭게 챙겨야 할 기술들도 많았습니다.

기술을 적용해가며 배우는 것이 최고의 학습법이었습니다. 그저 문서만 읽어가며 공부하는 것보다 프로젝트를 진행하며 짧은 시간 내에 필요한 기술을 압축적으로 습득할 수 있었습니다.

`Vue` 라이프사이클과 `Directive`에 대한 깊은 이해를 통해 `Vue.js`를 능숙하게 사용할 수 있게 되었습니다. 그리고 클라이언트 - 서버 간 잘 정의된 인터페이스들을 공유하여 데이터 흐름을 통제하고 버그를 줄이는 노하우도 얻을 수 있었습니다.

`CANVAS API`로 차트를 만들고 고도화하면서 마우스, 손가락 상호작용 이벤트 핸들링, 데이터 기반 드로잉을 진행함으로써 이벤트 핸들링에 깊은 이해를 얻을 수 있었습니다. 그리고 주식 등 자산에 깜깜이였던 제가 금융에 관심도 생기고 어느 정도 이해하게 되었습니다.

실무 전 파일럿 프로젝트를 진행하지 않았다면 적응하는 데 오랜 시간이 필요했을 것으로 생각합니다.

### 나름 피드백 루프가 빨랐던 협업 경험

협업 관련해서 도경 님이 이미 설명해주셨지만, 제가 느낀 바도 적어보겠습니다!

![45](/images/front/post/2021-07-21-zum-front-investing-clone/45.png)

매일 10시 데일리 스크럼 내용 정리

데일리 스크럼을 통해 서로의 진척도, 나아가 전체 프로젝트의 진척도를 추적, 가늠해볼 수 있었습니다. '프로젝트가 진행되고 있다' 라는 확신을 갖고 일할 수 있었습니다. 이슈 공유하여 같이 고민해보면서 해결책을 찾는 창조적 논의의 경험도 해볼 수 있었습니다. 혼자 고민하는 것보다 같이 고민하는 것이 낫다는 당연한 진리를 재확인할 수 있었습니다.

![46](/images/front/post/2021-07-21-zum-front-investing-clone/46.png)

코드리뷰를 받은 후 MERGE된 PR들

하루 동안 작업한 내용을 `PR`로 올리면 다음 날 코드리뷰를 진행하고 머지하였습니다. 매일 꾸준히 하면서 리뷰안된 `PR`이 남지 않도록 노력했습니다.

코드를 피드백하면서 서로의 발전을 도모하고 리뷰를 거친 검증된 코드들로 프로젝트가 진행된다는 점이 무척 좋았습니다. 그리고 각자 코드들을 다 보게 되기 때문에 코드의 히스토리도 공유할 수 있었습니다.

무엇보다 피드백루프를 데일리로 짧게 가져감으로써 좀 더 프로젝트를 가볍고 민첩하게 수행할 수 있다는 점이 매력적이었습니다!

## 5.2 도경 님의 회고

업무에 필요한 기술 셋을 공부하고 다른 사람들과 협업하면서 내가 지금 부족한게 무엇이고 앞으로 어떤 것을 공부해야 하는지 알게 되었던 좋은 시간이었습니다. 부족한 점들이 느껴질 때마다 아직 갈 길이 멀었구나를 일깨워주면서 더욱 빠르게 성장하고 싶은 욕심을 불어넣어 주었던 시간이기도 했습니다.

이제 파일럿 프로젝트를 마치고 실무에 참여하게 되는데요, 좋은 기회를 만들어주신 팀원분들께 감사드리고 앞으로 좋은 모습 보여드릴 수 있도록 하겠습니다.

## 5.3 정훈 님의 회고

입사 전에는 `React`로 프로젝트 경험을 했기 때문에 `Vue` 생태계에 익숙해지는 것이, 이 프로젝트에서 가장 중요한 목표 중 하나였습니다. 프론트엔드만 구현하는 프로젝트였다면 데이터 흐름을 완전히 파악하지 못했을 수도 있는데, (거의) 풀스택으로 진행한 프로젝트였기 때문에 오히려 `Vue` 라이프사이클과 `Vuex` 같은 상태관리 라이브러리를 통한 데이터 흐름을 좀 더 잘 이해할 수 있었던 것 같습니다. 어떤 데이터를 가공하고 정제할 때 이걸 브라우저에서 하는 게 좋을지, 서버에서 하는 게 좋을지, 컴포넌트 안에서 하는 게 좋을지 `Vuex`에서 하는 게 좋을지 고민하는 과정도 재미있었어요.

다만 초반에 `TDD`를 해보고 싶었는데, `유닛 테스트`와 `E2E 테스트` 개념도 잘 모르고 무작정 이것저것 시도해보다가 시간을 소비했던 게 제일 아쉬운 것 같습니다. 거의 1주일을 날리다 보니 차트에 기능 추가도 제대로 못 하고 다른 기능들도 급하게 구현하게 됐고, 결국 그 테스트 코드들은 아주 극 초반에 테스트를 시도했던 흔적만 남게 되었거든요. 개인 프로젝트로 좀 더 공부하면서 나중에 실무에도 적용할 수 있으면 좋을 것 같아요.

또 다른 한 가지는 앞서 `SSE` 적용기에서도 아쉬웠다고 말씀드린 부분인데요, `MongoDB`에 `TypeORM` 적용했던 부분, `Vuex`에 `Vuex-Module-Decorators` 적용했던 부분들도 레퍼런스가 충분치 않아서 많이 헤맸던 부분들입니다. 물론 제가 검색을 잘 못 했을 수도 있겠지만, `RDBMS`에서 사용할 수 있는 많은 `TypeORM API`들이 `MongoDB`에서는 지원되지 않는 것들이 많다든지, `Vuex-Module-Decorators`를 제대로 사용하려면 `class-validator` 같은 추가적인 패키지 설치가 필요하다든지 이런 내용들이 공식 문서에는 명확하게 나타나지 않더라고요. 그래서 좋아 보이는 신기술을 사용해보는 것도 좋지만, 일단 모두가 익숙한 기술을 잘 써보고 나서 조금씩 바꿔보는 것이 좋겠다는 생각을 많이 하게 되었습니다.

# 6. 마치며

저희 신입 개발자 3인방은 실무에서 고군분투하고 있습니다. 그렇다고 다들 버겁다고 느끼기보단 재미나게 일하고 있습니다.

물론 입사 전부터 쌓아온 실력이 뒷받침되어 행복 개발을 하고 있겠죠. 그러나 앞서 진행한 파일럿 프로젝트가 좋은 자양분이 되었다고 생각합니다. 바로 실무에 투입되 학습과 동시에 일을 처리했다면, 할 수야 있었겠지만, 개발자 개인도 힘들고 회사에 좋은 소프트웨어를 딜리버리할 수 없었을 것입니다.

파일럿 프로젝트를 통해 앞서 필요한 스킬, 도메인을 학습한 것이 **소프트하게 온보딩하고, 실무를 위한 발판을 마련하는 데** 도움이 되었습니다.

이런 훌륭한 문화, 우수한 팀원을 가진 개발 조직에서 일할 수 있다는 점이 저희에겐 큰 축복입니다. 늘 감사하며 더욱 발전시켜 앞으로 합류할 개발자들과 나눌 수 있도록 노력하겠습니다.

긴 글 읽어주셔서 감사합니다!
