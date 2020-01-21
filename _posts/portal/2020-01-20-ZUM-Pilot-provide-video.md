---
layout: post
title: 주제별 영상 제공 웹 서비스
description: 크롤링과 Youtube Data API를 이용하여 영상 제공 웹 서비스를 구축하는 과정에 대해 소개합니다.
image: /images/portal/post/2020-01-20-ZUM-Pilot-provide-video/thumbnail.jpg
introduction: 크롤링과 Youtube Data API를 이용하여 영상 제공 웹 서비스를 구축하는 과정에 대해 소개합니다.
category: portal/tech
tag: [pilot,spring,vue.js,crawling,crawler,YoutubePlayerApi,YoutubeDataApi]
---

> ### 파일럿 프로젝트
> 줌인터넷 포털개발팀의 주니어 개발자가 수습 기간 동안 진행하는 파일럿 프로젝트입니다.

## 1. 프로젝트 개요

프로젝트의 목표, 개발 스펙, 그리고 기본적인 기능들에 대해 소개합니다.

### 목표 및 의의

- 모바일 웹 서비스 페이지 개발
- 외부 API를 이용한 데이터 획득 및 정제
- Vue.js로 front-end 구성

### front-end

- Vue-cli3(Webpack 4)
- Terser Webpack plugin
- SCSS, Lodash, Swiper

### back-end

- Java8 이상
- Spring Boot + Gradle
- Spring Data JPA (선택, DB는 H2사용)
- Ehcache
- Pebble Template Engine (선택)

### 기타

- UI 디자인/구성 자유
- SSR, Prerendering 적용 필요 없음
- 브라우저 스펙 관련 처리(ex. BF 캐시) 필요 없음
- UI 컴포넌트 라이브러리 사용 제한 없음
- JQuery 사용 지양
- 서버 사이드 템플릿 사용 제한 없음
- 태블릿 모드 고려 필요 없음
- 빌보드 모바일 홈페이지 참조

### 기본적인 요구사항

- 외부 페이지(뉴스, 음원) 크롤링 및 가공 처리
- 음원을 Youtube Data API에서 검색
- 비디오 플레이어 제작
- 음원 차트와 무관하게 페이지 내에서 많이 본 영상 순위 선정 및 노출
- Cache (Local) 처리
- 모듈화 및 아키텍처링
- 화면 스와이프(플리킹) 기능
- Dynamic Component 활용
- Bundle Analyze & Optimize
- SCSS 기능 활용

## 2. 프로젝트 결과물 소개

### (1) K-POP 뉴스

[빌보드 코리아](http://billboard.co.kr/main/news/list)와 [SBS K-POP](http://sbsfune.sbs.co.kr/news/ssports_list.jsp?code_category=SS04)의 뉴스 컨텐츠를 `크롤링`하여 가져옵니다.

#### 빌보드 코리아 크롤링

![빌보드 코리아 뉴스 크롤링](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/001.gif){:width="300" style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
![빌보드 코리아 뉴스](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/005.jpg){:width="400" style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}

빌보드 코리아의 뉴스는 `Headline Swipe` 형태로 만들었습니다.

#### SBS K-POP 크롤링

![SBS 연예뉴스 크롤링](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/002.gif){:width="300" style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
![SBS 연예뉴스](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/004.jpg){:width="400" style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}

- SBS K-POP 뉴스는 `infinite scroll` 기법을 이용하여 만들었습니다. 최대 `5 페이지` 를 가져옵니다.
- 크롤링한 데이터는 `캐시에 저장`되며, `1분 간격으로 크롤링`을 합니다.

#### 뉴스 상세 조회

![뉴스 상세조회](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/003.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

뉴스 상세조회는 `Native App` 에서 사용되는 `Bottom-top slide` 형태로 만들었으며, 결과물을 크롤링하여 가져오도록 했습니다.


### (2) 음원차트

음원차트는 [멜론 차트](https://www.melon.com/chart/index.htm)의 컨텐츠를 크롤링하여 메타 데이터로 사용했습니다.

![멜론 음원차트](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/007-3.jpg){:width="600"}
- 멜론에서 음원차트를 크롤링하여 가져옵니다.

![음원차트 01](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/006-1.gif){:style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
![음원차트 02](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/006-2.gif){:style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}

- **100개의 음원**을 `Infinite Scroll` 기법을 이용하여 가져옵니다.
- `실시간` `일간` `발라드` `댄스` `힙합` `R&B/Soul` 등 6개의 카테고리가 존재합니다.

### (3) 음원차트에 대한 유튜브 동영상

`Youtube Search API`를 이용하여 `음원 제목을 기반`으로 동영상을 가져옵니다.

![음원 유튜브 동영상 01](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/007.gif){:style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
![음원 유튜브 동영상 02](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/008.gif){:style="display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}

- 음원은 클릭하면 **음원에 대한 유튜브 동영상**을 재생합니다.
- 플레이어에서 **Swipe 모션**을 사용하면 `이전/다음 음원에 대한 동영상`을 재생합니다.

![플레이어 컨트롤러](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/009.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- `직접 제작한 컨트롤러`를 통해서 동영상을 컨트롤할 수 있습니다.
  - 정지/재생 토글
  - 음소거 토글
  - 재생 시간 컨트롤
  - 최대화/최소화

### (4) 회원가입/로그인

서비스에 회원가입 및 로그인을 할 수 있으며, `로그인 상태의 사용자는 즐겨찾기/좋아요 기능을 사용`할 수 있습니다.

#### 비회원의 제한

![비회원 제한](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/010.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- 비회원은 좋아요와 즐겨찾기 기능을 이용할 수 없습니다.

#### 회원가입

![회원가입](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/013.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- 회원가입 페이지에서 `아이디` `비밀번호` `이름` 등을 입력받습니다.
- 중복된 아이디가 있으면 `경고창(Modal Popup)`을 통해 알립니다.
- 회원가입이 완료되면 `로그인 페이지로 이동`합니다.

#### 로그인

![로그인](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/014.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- 사용자가 입력한 정보가 잘못되었다면 `경고창(Modal Popup)`을 통해 알립니다.
- 로그인에 성공하면 `메인 페이지(뉴스)로 이동`합니다.

#### 즐겨찾기와 좋아요

![즐겨찾기와 좋아요](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/011.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- 로그인 상태의 사용자는 즐겨찾기와 좋아요 기능을 이용할 수 있습니다.

### (5) 인기영상

동영상의 **조회수**와 **좋아요**를 기반으로 순위를 측정하여 인기영상 목록을 만듭니다.

`인기도 = 조회수 + (좋아요 * 2)`

#### 좋아요 토글

![좋아요 토글](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/012-1.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- 로그인 상태의 사용자는 `좋아요 토글` 기능을 사용할 수 있습니다.
- 좋아요를 누르면 `인기도가 2 증가`합니다.

#### 조회수 처리

![동영상 조회수 증가](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/result/012-2.gif){:style="box-shadow:0 0 10px #ddd;padding:0"}

- 동영상 재상이 끝나면 조회수가 증가합니다.
- 조회수가 증가하면 `인기도가 1 증가`합니다.

## 3. 일정 관리 방법 소개

`Github Issue` 와 `Github Project`를 이용하여 프로젝트의 진행 사항과 일정을 어떤 식으로 관리했는지 소개합니다.

### (1) GitHub Issue 활용

각각의 `Issue`에 `Labeling`을 하여 어떤 기능들을 구현해야 되는지 쭉 작성했습니다.

#### Labeling

![일정관리01](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/0102.jpg)

먼저 위와 같이 적절한 `Label`을 만들습니다.

#### Milestone

GitHub Issue에는 `Milestone` 이라는 기능이 있습니다.

![일정관리02](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/03.jpg)

먼저 Milestone 목록을 만든 후

![일정관리03](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/04.jpg)

이렇게 `Milestone`와 `Issue`를 연동하면 `부분 일정`을 관리할 수 있습니다.

#### Issue List

![일정관리0401](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/0101.jpg)

Label과 Milestone 작성 후, Issue에다가 만들어야 하는 기능을 쭉 작성했습니다.

![일정관리0402](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/02.jpg)

Issue를 작성할 때, 관련 `Project`와 `Milestone`을 지정할 수 있으며 이렇게 했을 때 진행 현황을 눈으로 확인할 수 있기 때문에 매우 편리합니다.

#### Commit Message로 Issue에 Commit Reference

Commit Message에 `IssueID (#Number)`를 입력하면, 해당 Issue와 Commit이 연동됩니다.

![일정관리0403](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/0203.jpg)

이렇게 Commit Message에 `#26`을 포함할 경우

![일정관리0403](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/0202.jpg)

**관련 Issue(실시간 랭킹#26)** 에 Commit이 Reference 된 것을 확인할 수 있습니다.


### (2) Github Project 활용

![일정관리05](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/05.jpg)

`GitHub Project Tab`에서 `Project Unit`을 작성 및 관리할 수 있습니다.

![일정관리06](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/timeline/06.jpg)

`Automated`로 Project 생성 후 **Issue와 연동**하면 저절로 `To do`(해야 됨), `In Progress`(진행 중), `Done`(완료 됨) 등의 항목을 만들어줍니다.

**그리고 Issue에서 State를 변경하면 자동으로 반영됩니다**

### 사용 후기

작은 규모의 프로젝트는 이렇게 GitHub만 사용해도 충분히 효율적인 일정관리가 가능합니다.


## 4. 프로젝트 아키텍쳐 및 설계

User, Client, Server 그리고 Open API 각각의 구조와 서로간의 관계를 표현합니다.

### (1) Simple Service Structure

해당 프로젝트는 `Single Page Appliction` + `REST API` 형태로 서비스됩니다.

![Simple Service Structure](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/architecture/01.jpg)

### (2) Client Structure

Front-end는 `Vue.js`를 이용하여 `Single Page Application`으로 만들었습니다.

![Client Structure](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/architecture/02.jpg)

### (3) Server Structure

Back-end는 `SpringBoot`로 `웹 서버를 구축`하고 `REST API`를 만들었습니다.

DB 구축은 `H2`와 `JPA`를 사용하였습니다.

![Server Structure](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/architecture/03.jpg)

### (4) Detail Service Structure

앞서 보여드린 Structure들을 종합하면 다음과 같습니다.

![Detail Service Structure](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/architecture/04.jpg)

### (5) DB 설계

news와 관련된 데이터는 영구적으로 저장할 필요가 없기 때문에 테이블을 만들지 않았습니다.

대신 **캐시에 저장하여 일시적으로 데이터를 유지**합니다.

![Detail Service Structure](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/architecture/05.jpg)

## 6. 클라이언트 사이드

### (1) Vue Components

#### Hierarchy

- SiteHeader, SiteFooter, Modal 등의 Component는 항상 존재하는 component입니다.
- news, music, popular, bookmark, login, join 등은 vue-router를 통해 handling됩니다.

```
VueApp
├─ SiteHeader.vue
├─ VueRouter
│  ├─ /news: News.vue
│  │  ├─ NewsWrapper.vue
│  │  │   ├─ Headline.vue
│  │  │   └─ Article.vue
│  │  └─ NewsDetail.vue
│  ├─ /music: Chart.vue
│  │  ├─ ChartCategory.vue
│  │  ├─ VideoPlayer.vue
│  │  └─ ChartArticle.vue
│  ├─ /popular: Popular.vue
│  │  ├─ VideoPlayer.vue
│  │  └─ VideoArticle.vue
│  ├─ /bookmark: Bookmark.vue
│  │  ├─ VideoPlayer.vue
│  │  └─ VideoArticle.vue
│  ├─ /sign-in: Login.vue
│  └─ /sign-up: Join.vue
├─ SiteFooter.vue
└─ Modal.vue
```


#### App.vue

![app structure](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/components/app.jpg)

App에는 `SiteHeader` `VueRouter` `SiteFooter` `Modal` 등의 compnent가 있으며, `VueRouter`는 path를 통해 `component를 handling`합니다.

#### VueRouter

![vue-router](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/components/vue-router.jpg)

VueRouter는 browser의 주소와 compnent를 매칭시킵니다.


#### News

![news](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/components/news.jpg)

#### Chart, Popular, Bookmark

![etc](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/components/etc.jpg)

- Chart, Popular, Bookmark에서 `VideoPlayer`가 사용됩니다.
- `VideoArticle`에는 `viewCount` `likeCount` `popularPoint` 등의 parameter를 추가로 넘길 수 있습니다.

#### Login, Join

![login](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/components/login.jpg){:style="display:inline-block"}
![join](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/components/join.jpg){:style="display:inline-block"}

login과 join에는 다른 컴포넌트가 포함되지 않았습니다.

#### Summary

앞서 보여드린 구조를 조합하면 다음과 같은 구조가 됩니다.

![summary](https://www.plantuml.com/plantuml/svg/fLHDQzj04BtlhnX43wr13N5l8eUaBgMKjfWMSebps4Y3lNWz8-HLGoZvxzqlQLUM3eM2aMRUUxCpivhnxTd8plGdBJgiZQIzHYZksdP71VmH03MVMYOa0x-KmIye6-pWmHAmMYLajRB8uqH-t-DFxarIZy22s9tqcTbCpmx8WlmxDr8FIk-C8ljx-wPpUTwtqXpUWJo3CoRnnHNXyxc27_PPE8KpVBi0wHeSwDhJYj1JDMjjMSKK8kuwesgD5s6Vq4YbFPYV0EN3GJKDqkCiDlCprNZEwqNjzS5-iGesxkMhzzQiV8zkfC4zToyNtBrgaBTQljWBTnVahUjPa_w8LEbb8IstlPPT1TjW-6AYFIjdCULwbhBmkfXpHsLPxcZdLKOPXqJdq9-UoDxF0FnM-BpXdim0Q7N42H2htRAYS6qo9BbUwEo9-NYItR62Zz7o4OFpRyrz-E_cyZBNipA_yLvHs0Ax1bTdjQTIKHNmXQtvoZDvtrOUZkfNaIrvciHnSqLQwiIcJHNP6YVUxsSMUNDJbc4bXNk2zTm234uPfcxauZmbUlW8eyBtctZNZn2JwS-g6KOzlZDcCkp352SwfGsJcr7Z8CNlFgVMGjmYDVPlzYy0)

### (2) Vuex(VueStore)

vuex는 vue.js에서 제공하는 중앙집중식 상태 관리 라이브러리입니다. vuex를 이용하여 어떤 식으로 상태관리를 하였는지 소개합니다.

#### Structure

module화 하여 사용하였습니다.

```
./middleware/store
  ├─ index.js
  ├─ mutations-type.js
  └─ modal|music|news|user|video
       ├─ index.js
       ├─ actions.js
       ├─ mutations.js
       └─ state.js
```

![structure2](https://www.plantuml.com/plantuml/svg/bP8x3i8m38Rtd28gMoNV027kWCH26Qp6GAMIeZn0275t4lT1KbWwrVtZ_xDZPsiT6kUlhJ1KEzJdbcInzxHpdQ52leIKDHebhzwXQpfjHm7hx3TW74t9dV8jMRawuMdKYea0xdaBQBGo1Z49Gr9IlYm30Dkoh3G0LBeAnyolzBUF40yjC8eTFnXlcteP9Zhc64qFkuWI3NE8jsGMGQ9X3hatYhf557Q8j-0y2OTBenJfOxBFAKfEn-KEtzJNhrQCArwl0ORXvn8FCfDuAfd2LyoKlbr-5-1liDdyKVfgcSB5KeLhfGANsf9MuQb_0000)

이렇게 사용하면 `state`만 `namespace`로 분리됩니다.

그래서 `mutations` `actions` 에 사용될 method name은 **mutations-type.js**을 통하여 관리합니다.

``` js
// mutations-type.js : mutations 혹은 actions 에 사용될 상수를 정의합니다
export const VIDEO_FETCH = 'video/fetch'; // 비디오 가져오기
export const VIDEO_SELECT = 'video/select'; // 비디오 선택
export const VIDEO_VIEW = 'video/view'; // 비디오 조회수 증가
export const VIDEO_LIKE = 'video/like'; // 비디오 좋아요 토글
export const VIDEO_POPULAR_FETCH = 'video/popularFetch'; // 인기영상 가져오기
export const VIDEO_BOOKMARK = 'video/bookmark'; // 즐겨찾기 가져오기
export const VIDEO_LOADING = 'video/loading'; // 비디오 로딩 완료 여부
// ... 생략
```

그 다음 `component`에 필요한 `state` `mutations` `actions` 만 `mapping` 하여 사용합니다.

![example1](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/stores/example.jpg)

#### Logic

Vuex의 로직은 다음과 같습니다.

![logic](https://www.plantuml.com/plantuml/svg/RP7FIWCn4CRlUOgX9mta1QIK5XNq84WhdlOIag6xa7ya4nN4TtTsksQtu34pltpVDpFxGZfJzKwOw1mQ6c8ei7clU1zzYW43bIuefRhGYHDfGl0w0KMGqZ1H2QsKO_Cm_zN1majbSders2FrqHOfDw0Bc2OkRewFfpSul3xVZes2-GEpo9n4XxD3u2HVy2q0bjBiT5LhZbVLAR3u4OiTg3oSUrAxLSOxu5dzGFzYVsCnzJ2KfCdqQswhRFmCwkB4p163vVoB-5RLf9fAirg0Yy1kfP2SDjZs6USeSTuD8qz4QTIfOJ2JYjYpBH_n5m00)

- Component는 Actions와 Mutations을 사용할 수 있습니다.
- Actions는 Server(혹은 API)와 통신할 수 있습니다.
- State는 오직 Mutations을 통해서만 수정할 수 있습니다.
- Actions이 받아온 데이터를 Mutations에 넘깁니다.
- State가 수정되면 Component에 반영되어 렌더링됩니다.

### (3) 분석 및 최적화

vue-cli에 포함된 vue-loader는 `*.vue`를 포함해 webpack을 기반으로 프로젝트를 구성할 수 있도록 해주는 도구입니다. 그리고 webpack으로 구성된 프로젝트를 build할 때 다양한 이슈가 발생할 수 있습니다.

그러한 이슈들을 해결할 때 사용한 분석 및 최적화 도구와 방법에 대해 소개합니다.

#### 1) analyzer

analyzer는 `webpack-bundle-analyzer`를 사용했습니다.

##### install

``` sh
yarn add -D webpack-bundle-analyzer
```

##### 적용

`vue-cli`로 만든 프로젝트는 `vue.config.js`를 통해서 `webpack` 설정을 `override`할 수 있습니다.

**vue.cofig.js**

``` js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
module.exports = {
  // 앞 내용 생략
  configureWebpack: config => {
    // NODE_ENV의 값이 analyze일 때 Analyzer를 작동시킵니다.
    if (process.env.NODE_ENV === 'analyze') {
      config.plugins = [new BundleAnalyzerPlugin()];
    }
  },
}
```

그리고 `package.json`에 analyze 시작을 위한 `npm script`를 작성해야 합니다.

``` json
{
  /* 앞 내용 생략 */
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint",
    "analyze": "cross-env NODE_ENV=analyze vue-cli-service serve"
  },
  /* 뒷 내용 생략 */
}
```

그리고 실행해주면 프로젝트에서 작동중인 코드들의 용량을 확인할 수 있습니다.

![analize1](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/optimization/analize01.jpg)

box의 size가 클 수록 용량이 `상대적으로 큰 것`입니다.

그리고 여기서 문제를 확인할 수 있습니다. icon 사용을 위해 fontawsome package를 설치했는데, 생각보다 용량이 너무 컸습니다.

![icon](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/optimization/fontawsome.jpg)

그래서 babel의 기능을 이용하여 fontasome pacakge 중 필요한 것만 포함 시키도록 하였습니다.

**.babelrc**

``` json
{
  "plugins": [
    ["transform-imports", {
      "@fortawesome/free-solid-svg-icons": {
        "transform": "@fortawesome/free-solid-svg-icons/${member}",
        "skipDefaultConversion": true
      },
      "@fortawesome/free-regular-svg-icons": {
        "transform": "@fortawesome/free-regular-svg-icons/${member}",
        "skipDefaultConversion": true
      }
    }]
  ]
}
```

이렇게 하면 지정한 것들만 가져오게 됩니다.

다시 analyzer를 실행하여 확인해본 결과

![analize1](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/optimization/analize02.jpg)

`860kb에서 100kb` 정도로 줄어든 것을 확인할 수 있었습니다.

#### 2) Code Splitting

Vue.js는 SPA(Single Page Application)을 만드는 도구이며
Code Splitting은 SPA의 성능을 향상시키는 방법입니다.
SPA는 초기 실행시 모든 자원(css, js, ...)을 한 번에 불러옵니다.

![build01](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/optimization/build02.jpg)

이럴 경우 **사이트 로딩이 매우 느려질 수 있습니다.**

그런데 `Code Splitting`을 활용하게 되면 **필요한 시점에 자원을 불러와 사용**합니다.

> ##### Lazy Loading
> `Dynamic Import` + `webpackChunkName`을 사용하면 Lazy Loading이 가능합니다.
> - Dynamic Import는 `const moduleName = () => import('path')` 형태로 사용할 수 있습니다.
> - path 앞에 할 때 prefix로 `/*webpackChunkName: name*/`을 붙이면 리소스를 분리하고 묶을 수 있습니다.
> - `index.js`를 이용하면 쉽게 관리할 수 있습니다.


실제 사용 예는 다음과 같습니다.

##### 폴더 구조

```
client/src
├─ components
│   ├─ video
│   │   ├─ index.js
│   │   ├─ Article.vue
│   │   ├─ List.vue
│   │   ├─ Meta.vue
│   │   ├─ Player.vue
│   │   └─ Controls.vue
│   └─ ...
├─ views
│   ├─ index.js
│   ├─ Popular.vue
│   └─ ...
├─ middleware/router/index.js
└─ ...
```

`**/index.js`를 이용하여 import/export를 관리합니다.


##### index.js를 사용하면 좋은 점

다음과 같이 `index.js를 생략하여 import` 할 수 있습니다.

``` js
import { VideoPlayer, VideoControls } from 'components/video/index.js'
import { NewsArticle, NewsDetail } from 'components/news/index.js'
import { SiteHeader, SiteFooter } from 'components/common/index.js'
import { Alert } from 'components/modal/index.js'

// index.js를 생략할 수 있습니다.
import { VideoPlayer, VideoControls } from 'components/video'
import { NewsArticle, NewsDetail } from 'components/news'
import { SiteHeader, SiteFooter } from 'components/common'
import { Alert } from 'components/modal'
```

##### Code Splitting 적용

``` js
/* client/src/views/index.js */
export const News = () => import(/* webpackChunkName: "views" */'./News.vue');
export const Chart = () => import(/* webpackChunkName: "views" */'./Chart.vue');
export const Login = () => import(/* webpackChunkName: "views" */'./Login.vue');
export const Join = () => import(/* webpackChunkName: "views" */'./Join.vue');
export const Popular = () => import(/* webpackChunkName: "views" */'./Popular.vue');
export const Bookmark = () => import(/* webpackChunkName: "views" */'./Bookmark.vue');

/* client/src/components/video/index.js */
export const VideoList = () => import(/* webpackChunkName: "chart" */'./List.vue');
export const VideoPlayer = () => import(/* webpackChunkName: "chart" */'./Player.vue');
export const VideoControls = () => import(/* webpackChunkName: "chart" */'./Controls.vue');
export const VideoMeta = () => import(/* webpackChunkName: "chart" */'./Meta.vue');
export const VideoArticle = () => import(/* webpackChunkName: "chart" */'./Article.vue');

/* 나머지 생략 */
```

**client/src/middleware/router/index.js**

``` js
/* 앞 내용 생략 */
import { News, Chart, Login, Join, Popular, Bookmark } from '@/views';
const routes = [
  { path: '/', component: News, alias: '/news' },
  { path: '/chart', component: Chart },
  { path: '/sign-in', component: Login },
  { path: '/sign-up', component: Join },
  { path: '/popular', component: Popular },
  { path: '/bookmark', component: Bookmark },
];
/* 뒷 내용 생략 */
```

**client/src/views/Chart.vue**

``` html
<template><!-- 생략 --></template>
<script>
// 앞 생략
import { Flicking } from '@egjs/vue-flicking';
import { ChartArticle } from '@/components/chart';
import { VideoPlayer } from '@/components/video';
import { Spinner } from '@/components/common';
const components = { ChartArticle, VideoPlayer, Flicking, Spinner };
// 뒤 생략
</script>
```

이렇게 작성 후 `build` 하면 다음과 같이 분리됩니다.

![build01](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/client/optimization/build01.jpg)

`app` `chart` `modal` `news` `template` `views` 등으로 쪼개진 것을 확인할 수 있습니다.

## 7. 서버 사이드

### (1) Crawling

`SBS K-POP 뉴스` `빌보드코리아 뉴스` `멜론 차트` 등의 사이트를 크롤링 하는 과정에 대해 소개합니다.

#### Jsoup

Crawling은 Jsoup을 활용했습니다. `Jsoup`은 **java로 만들어지는 HTML Parser**입니다.

``` java
Document doc = Jsoup.connect(url).userAgent(agent).get();
```

이렇게 URL에 해당하는 DOM을 Parsing할 수 있으며, **interface가 jQuery와 매우 유사합니다.**

#### Flow Chart

![flowchart1](https://www.plantuml.com/plantuml/svg/ZPBFIiD04CRlUOevBmJlHQHGJu8exS6BbqqwD85qj-vkgju4lOYN21Qh1F4WU54eRK_Y4pNRTt12yySeYAU5RtxxVJEpszQ6AnCF8yUNKOI-2QNGq4LjEb8ObMkgKUgX6eS-DhIEugSvr-U6UrmZ7A7N2mqwJjC8t9toFhJ0Fa-onHBiuvsTlpkbJaXXLoEh-OMzl7PAdP0YW90kdiGK0juvCBQdPJnYh2AttGQfHzGj4cVmp6m5PXWHAoHLvPZeEjU5tODzEEHAXs9mB5pgOBPQV4Bs-hAUt5QzadrzPrFBahI2PzFrm_IRVprwX_i1ESFF_P3Xh_qKDl_O96FswMsppd8k5Gu2qmAVyX3ov_apaGm-4dkJqdcVsAkqp6wZwDCN-G80)

Crawling한 Data는 `Caching` 하여 재사용하여 `1분 동안 저장`합니다.

Caching 후 1분 동안 요청이 오면 Cache에 저장된 data를 반환하고, 그 이후에는 다시 Jsoup을 통하여 크롤링을 수행합니다.

### (2) Youtube Search

크롤링 해온 **음원**에 대해 **Youtube에 검색해서 동영상을 가져오는 과정**에 대해 소개합니다.

#### API Request Cost

`Youtube Data API`를 통하여 Youtube에 있는 `동영상` `채널` `리소스` 등에 접근할 수 있습니다.

그런데 Youtube Data API는 Youtube Service의 자원을 사용하기 때문에, 요청에 대한 제한이 있습니다.

**하루에 `10000`의 할당량을 사용할 수 있으며, Request 종류별로 할당량에 대한 cost가 다릅니다.**

공식 문서에서 요청에 대한 cost를 확인해볼 수 있는데, 정확한 수치가 아니라 `근삿값`입니다.

![cost](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/server/cost.jpg)

이렇듯 `Search` 요청은 기본적으로 `100` 이상의 Cost를 지불해야합니다.

![cost2](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/server/cost2.jpg)

`한 개의 Search 요청`을 보낸 후 API 관리자에서 확인해본 결과, 실제로 `102`의 Cost를 지불합니다. 한도가 10000 이므로, `하루에 98회의 Search 요청`을 보낼 수 있습니다.

#### Youtube API Client Package

Youtube는 API를 Client에서 사용하기 쉽게 Client Package를 제공합니다.

``` java
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestInitializer;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.youtube.YouTube;
import com.google.api.services.youtube.model.SearchResultSnippet;

// { NetHttpTransprot, JacksonFactory } --> 구글에서 제공하는 Client API
// NetHttpTransport: java.net 패키지 기반의 Thread-safe http low-level Transport
// JacksonFactory: Jackson2 기반의 low-level JSON library
private HttpTransport HTTP_TRANSPORT = new NetHttpTransport();
private JsonFactory JSON_FACTORY = new JacksonFactory();

// API 사용에 필요한 Instance 생성
YouTube youtube = new YouTube.Builder(HTTP_TRANSPORT, JSON_FACTORY, new HttpRequestInitializer() {
  public void initialize(HttpRequest request) throws IOException { }
}).setApplicationName("youtube-cmdline-search-sample").build();
```

그리고 Snippet에서 필요한 것들만 선택하여 가져오면 됩니다.

``` java
search
  .setKey(API_KEY) // 검색에 사용할 API KEY
  .setQ(searchQuery) // 검색어. 제목+가수 형태의 문자열을 넘김
  .setType("video") // 기본값: chnnel,playlist,video. 현재 필요한 것은 video
  .setMaxResults(1) // 검색된 목록에서 가져올 데이터의 수
  .setFields("items(id/videoId,snippet(title,thumbnails/default/url))") // 결과로 가져올 필드
  .execute() // Search 실행 후 결과를 Video List에 Mapping
  .getItems()
  .forEach(v -> {
    SearchResultSnippet snippet = v.getSnippet();
    result.add(
      Video.builder()
        .title(snippet.getTitle())
        .videoId(v.getId().getVideoId())
        .thumbnail(snippet.getThumbnails().getDefault().getUrl())
        .searchTitle(searchQuery)
        .build()
    );
  });
```

#### Search Result Save

`VideoService`의 일부 코드입니다.

``` java
/*
 * 검색어(제목+가수) 기반으로 Video 정보를 가져옴
 * @param q : 검색어(제목+가수)
 * @return : Video Entity
 * @throws VideoNotFoundException : 동영상을 가져오는 과정에 오류가 발생했을 때 예외 처리
 */
@Cacheable(cacheNames = "VideoCache", key="#q")
public Video getBySearch (String q) throws VideoNotFoundException {
  // 일단 DB에 video가 있는지 탐색
  Video video = Optional.ofNullable(videoRepository.findBySearchTitle(q)).orElseGet(() -> {
    // DB에 없다면 Youtube Search
    Video v = Optional.ofNullable(youtubeSearch.execute(q))
                      .orElseThrow(VideoNotFoundException::new);
    videoRepository.save(v);
    return v;
  });
  // 탐색해온 Video 정보 반환
  return video;
}
```

앞서 언급했듯이 **API 요청에는 cost가 필요**합니다.
그래서 중복 요청을 방지하기위해 이미 **결과로 가져온 데이터는 DB에 저장하고, Caching 처리** 합니다.
따라서 API 요청을 하기 위해선 일단 cache와 db를 거쳐야 합니다.

#### Flow Chart

Youtube Search를 위한 과정은 다음과 같습니다.

![FlowChart2](https://www.plantuml.com/plantuml/svg/bLBDQeD04BxlKynPy0LAAI796mGAXLuskaJ1QZ1hpWdnKdAeWQQQ8f93IoyfsAIdaYVIoJjqhLMh0Q6dWTbllf-PxKmujRbpPv2ngBgYZwd9uLfNcTMpJ6vRXi7isjk0sLDTORNUZULmPyW6ZDgAHbJAwP1EMD4cG1g485yLF701wSC6Wpakve3RTNhu17n-nFqxAH02N1CG8yb-XejxV1BOhPikTyIqE0DhAgYRKBde0FfniezlJVbNe9IBLkX-aFfW9LhADH2NyXb2b3Wv726DWzCcQ37LWB-zdDOhA0DNpEL03aczi3Jzanl-Q5GBbQ7VHTyJc1b6hrdW7bKqtHoT7q98jHmYpm7_lPyaORJBTon9kKDR7saySwO89ooprE-scn4aNnukGr5z3zsmM6g7cQhuhzy0)

음원의 제목을 통해서 Youtube에 검색합니다. 검색 후 DB에 결과를 저장하고, 캐싱까지 합니다.

그래서 동영상 정보를 재요청시 Cache나 DB에서 가져오게 됩니다.

### (3) Authorization

회원가입 후 로그인을 하면 다음과같은 과정으로 `JWT(Json Web Token)`을 발행합니다.

``` java
/**
* 토큰 생성
* @param userId : user의 id
* @param roles : user의 역할. 현재는 ROLE_USER 만 존재
* @return 토큰 값 반환
*/
public String createToken(String userId, List<String> roles) {
  Claims claims = Jwts.claims().setSubject(userId); // claim 생성
  claims.put("roles", roles); // role 지정
  Date now = new Date();
  return Jwts.builder()
          .setClaims(claims) // claim 지정
          .setIssuedAt(now) // 토큰 발행 일자 지정
          .setExpiration(new Date(now.getTime() + tokenValidMS)) // 유효 시간 지정
          .signWith(SignatureAlgorithm.HS256, secretKey) // 암호화 알고리즘, secret 값 지정
          .compact(); // 위의 내용을 압축 후 반환
}

```

![flowchart3](https://www.plantuml.com/plantuml/svg/SoWkIImgAStDuN8goYylJYrIqBLJ20NIplbv9KNvEJb04Ik5ejJ2qjJY4WNzn89C_UBCz3pTp3mkD5LGVS6fHMMPoQb0JPuk-W7XN7dv9QaA-ML01LXa5LvjQdYpR2vEHMzdzRoPFK7XpOAfhpTlKKXBBKdEGBVMHXUldZSBMbvthy7YLg_ma82Y_BBC5B07FLsGt80g1UGfl6cU-wPb8nQhiIY5M0WBJQZpq4Apk20_hpXLGHVgMAXRjK46S3cavgK0umC0)

### (4) Authentication

Authentication은 Spring Security의 Filter와 JWT를 이용합니다.

먼저 spring security에서 **filter를 정의**합니다.

``` java
/**
* http 요청에 대해 처리하는 내용을 정의함
* @param http
* @throws Exception
*/
@Override
protected void configure (HttpSecurity http) throws Exception {
http
  .httpBasic().disable() // spring-security에서 제공하는 /login 과 같은 페이지 비활성
  .csrf().disable() // Cross site request forgery 비활성
  .sessionManagement()
    .sessionCreationPolicy(SessionCreationPolicy.STATELESS) // session을 stateless 형태로 관리
  .and()
     // jwt를 이용하는 filter 추가
    .addFilterBefore(
      new JwtAuthenticationFilter(jwtTokenProvider),
      UsernamePasswordAuthenticationFilter.class
    );
}
```

이렇게 모든 요청에 대해 `jwtAuthenticationFilter`를 통해 사전 검증을 합니다.

``` java
@Override
public void doFilter(
  ServletRequest request,
  ServletResponse response,
  FilterChain chain
) throws IOException, ServletException {
  // request의 header에 포함된 Token 정보를 가져온다.
  String token = jwtTokenProvider.resolveToken((HttpServletRequest) request);

  // token 정보가 존재할 때만 token을 검증
  if (token != null && jwtTokenProvider.validateToken(token)) {
    // token에서 값을 추출하여
    Authentication auth = jwtTokenProvider.getAuthentication(token);
    // context에 저장한다.
    SecurityContextHolder.getContext().setAuthentication(auth);
  }

  chain.doFilter(request, response);
}
```

이렇게 Request Header에 Token 정보가 있을 때만 Token 검증 후 Token에 담긴 Authentication을 Security Context에 저장합니다. 그리고 다음과 같이 사용됩니다.

``` java
/**
 * AuthenticationCheck
 * @return
 * @throws AuthException
 */
public String AuthenticationCheck () throws AuthException {
  // Security Context 에 저장한 authentication 정보 가져오기
  Authentication auth = SecurityContextHolder.getContext().getAuthentication();
  // Token 에서 가져온 User Id가 익명의 사용자일 경우 예외처리
  String userId = auth.getName();
  if (userId.equals("anonymousUser")) {
     throw new AuthException();
  }
  return userId;
}
```

즉, Security의 Authentication 정보는 기본 값이 항상 `anoymousUser`입니다. 이런식으로 User 권한이 필요할 때 Token 정보를 통해서 검증이 가능합니다.

![flowchart4](https://www.plantuml.com/plantuml/svg/SoWkIImgAStDuN8goYylJYrIqBLJ20NIplbv9KNvEJb04Ik5ejJ2qjJY4WNzn89C_UBCz3pTp3mkD5LGVS6fHMMPoQb0JPuk-W7XN7dv9QaA-ML01LXa5LvjQdYpR2vEHMzdzRoPFK7XpOAfhpTlKKXBBKdEGBVMHXUldZSBMbvthy7YLg_ma82Y_BBC5B07FLsGt80g1UGfl6cU-wPb8nQhiIY5M0WBJQZpq4Apk20_hpXLGHVgMAXRjK46S3cavgK0umC0)

### (5) Exception

`Optional`과 Spring의 `RestControllerAdvice`을 이용하여 예외에 대한 Response를 만들었습니다.

`ExceptionAdvice.java`의 일부입니다.

``` java
@Slf4j
@RequiredArgsConstructor
@RestControllerAdvice
public class ExceptionAdvice {
  private final ResponseService responseService;

  /**
   * User select 에 대한 response 예외 처리
   * @param request
   * @param e
   * @return USER_FAIL
   */
  @ExceptionHandler(UserIdNotFoundException.class)
  @ResponseStatus(HttpStatus.OK)
  protected CommonResult userIdNotFoundException(HttpServletRequest request, Exception e) {
    return responseService.failResult(CommonResponse.USER_FAIL);
  }
  // 나머지 생략
}
```

아래의 코드에서 예외가 발생하면 `ExceptionAdvice`에서 처리됩니다.

``` java
/**
 * 유저 정보가 Null 이면 Exception 처리, 아니면 유저 정보 반환
 * @param userId : User의 login ID
 * @return
 * @throws UserIdNotFoundException : 유저 정보 탐색에 대한 실패 처리
 */
@Override
public User loadUserByUsername(String userId) throws UserIdNotFoundException {
  return Optional.ofNullable(get(userId)).orElseThrow(UserIdNotFoundException::new);
}
```

즉, ExceptionAdvice.java에 정의된 Exception 이 발생하면 ExceptionAdvice가 바로 관련 Response 데이터를 만들고 바로 브라우저에 return 합니다.

![flowchart5](https://www.plantuml.com/plantuml/svg/VL6zIWD14ExlAUO1p0k8I52miCofQT8iTuCkd3Fdx5pKtYuMWe8H4cn4B2mK4Mny8M_p3juQpiGxIRdx_JDTfqQqECwYBU5JXmATJOXpiNGOOrA8rNDOXnwU5EWq8bO47bQi5cN7PehXRnLfjxy7kH4NQ0smYZsmAV8samfdMIMlJJ45QHLea_yQ1WZFT42cq2CajObHo_GxSwFpZuMVVlZ7AVZHm-pooOycQmFojrVb_RF_l2cl9r2-Z6TtuwWfhBl7A4ERu9BHnUlNs_lSQ3-afaPDSyH25L38XHDqhXLI5rxGVvvpovMhUkXo9eTH5ocjJlqD)

`POST /api/video-like` 요청에 대한 예시입니다.

![response01](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/server/response01.jpg)

이런 응답을 반환합니다. 여기에 `request-body`를 추가하면 다음과 같습니다.

![response02](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/server/response02.jpg)

header에 JWT가 생략되었기 때문에 로그인이 필요하다는 응답을 반환합니다. 다시 header에 access token 정보를 담아서 요청하면

![response03](/images/portal/post/2020-01-20-ZUM-Pilot-provide-video/server/response03.jpg)

이렇게 정상적인 내용을 반환합니다.

## 8. Reference

> - JPA
>   - [개발자의 기록 습관](https://ict-nroo.tistory.com/category/ICT%20Eng/JPA)
>   - [Heee's Development Blog](https://gmlwjd9405.github.io/tags.html#jpa)
>
> - Spring Security
>   - [카페 형식 게시판 구현 - 파일럿 프로젝트](https://zuminternet.github.io/ZUM-Pilot-dynamic-board/)
>
> - Spring Ehcache
>   - [SpringBoot + Ehcache 기본 예제 및 소개](https://jojoldu.tistory.com/57)
>
> - Swipe
>   - [Vuejs로 모바일 웹 구축하기](https://zuminternet.github.io/ZUM-Pilot-vuejs/)

## 9. 마치며

고등학교를 거쳐 대학교 시절까지 꾸준히 개발을 공부하고 무언가를 만들어왔지만, 이렇게 꼼꼼하게 신경쓰면서 프로젝트를 진행해본 적은 처음이었습니다. 그래서 짧은 시간이었지만 이런 프로젝트를 진행할 수 있어서 즐거웠고 이런 기회를 제공해준 회사와 팀장님께 감사했습니다.

무엇보다 팀원들이 공부하고 기록한 자료를 참고하고 조언을 구하면서 이런 팀원들과 함께할 수 있다는 것 자체가 너무나 큰 축복임을 느꼈습니다.

긴 글 읽어주셔서 감사합니다!