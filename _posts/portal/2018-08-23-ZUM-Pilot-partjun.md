---
layout: post
title: "[포털개발팀-박효준] 파일럿 프로젝트"
description: 포털개발팀 신입사원 파일럿 프로젝트.
image: /images/portal/post/2018-08-23-ZUM-Pilot-partjun/vuejs-wallpaper-1_0.png

introduction: 파일럿 프로젝트를 진행하며.
subtitle: Vue.js를 이용한 모바일 줌 개발
category: portal/pilot
author: 포털개발팀
authorEmail: 
authorImage: /images/portal/author/zum.png
authorDescription: zum.com service <br/> Front-End & Back-End Developer.

nickname: partjun
tag: [spring,boot,vue.js,pilot]
---

# 소개
안녕하세요. 포털개발팀 신입사원 박효준입니다.  
이 글은 제가 진행한 파일럿 프로젝트에 대해 소개하고 느낀 점을 정리한 글입니다.
![GO](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/introduce.jpg)
  
## 파일럿 프로젝트
줌 인터넷에서는 모든 신입 사원이 파일럿 프로젝트를 진행합니다.  
주어진 주제와 기술 스펙을 통해 과제를 수행하면서 줌 인터넷의 문화와 분위기에 적응하면서 기술도 갈고 닦는
아주 귀중한 시간입니다.
  
## 1. 주제
제 파일럿 프로젝트의 주제는 *Vue.js로 만드는 모바일 줌* 이었습니다.  
Vue.js를 이용해 사이트의 각 기능을 **모듈화**한 모바일 줌 사이트를 만들어 보는 것이죠.
![JQuery에서 Vue.js로](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/jquery-to-vue.jpg)
  
## 2. 개발 스펙
개발 스펙은 대부분 제가 사용해온 기술 스택이었기 때문에 개발에 있어 큰 어려움을 느끼지는 않았습니다.

| Back-end | Front-end  |
|----------|------------|
|- Java8   |- Freemarker|
|- Gradle  |- Vue.js    |
|- Spring Boot|- Lodash|
|- Spring Data|- Webpack|
|- Ehcache||

이렇게 제시된 기술 스펙에 아래 라이브러리들을 추가로 사용했습니다.

| Back-end | Front-end  |
|----------|------------|
|- Lombok  |- Lory|
|- H2|- Axios|
||- Vue-lazyload|
||- Sass|

### Vue.js?
![Vue.js 로고](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/vue-logo.png)
[Vue.js](https://kr.vuejs.org/v2/guide/index.html)는 프론트엔드 프레임워크입니다. 
2018년 8월 23일 기준으로 111k의 Star를 확보했고, 15k의 Fork 프로젝트가 존재합니다.
그리고 셀 수 없을 정도의 써드파티 라이브러리가 만들어지고 있죠. 명실상부한 '대세' 프레임워크입니다.  
  
많은 프론트엔드 프레임워크가 그렇듯 Vue.js 역시 [SPA](https://ko.wikipedia.org/wiki/%EC%8B%B1%EA%B8%80_%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98)(Single Page Application)
을 지향하고, 컴포넌트 기반으로 설계됩니다. 또, [NPM](https://www.npmjs.com/)으로 디펜전시를 관리하고 
[Webpack](https://webpack.js.org/)을 기반으로 Vue/SASS를 비롯한 각종 로더, [Babel](https://babeljs.io/) 폴리필등을 사용합니다.
최근 업데이트에서는 [TypeScript](https://www.typescriptlang.org/)을 이용한 개발 편의성을 강화하고 있습니다.
![??](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/what.jpg) 
*프론트엔드 개발을 접하지 않으셨다면 이게 뭔가 싶으실 수 있습니다...*
> 개인적으로 *[Angular](https://angular.io/)와 비교하자면 아쉬운 점*도 있었습니다.  
> 아쉬운 점은 아래 후기에서 말씀드리도록 하죠.
  
## 3. 개발 내용
![개발 내용](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/development.jpg)
*프론트엔드 개발 후 백엔드를 개발*
  
저는 Stub 데이터를 이용하여 Vue.js 기반의 SPA 프론트엔드 프로젝트를 개발하고 번들링 한 후,  
Spring Boot 백엔드 서버를 개발해 합치는 방법을 택했습니다.  
그리고 최종적으로 프론트엔드, 백엔드 프로젝트 파일을 통합하여 [Gradle을 통해 한번에 빌드](https://github.com/srs/gradle-node-plugin)할 수 있도록 구성했습니다.

### Front-end: Vue.js Project
모바일 줌 CMS의 컴포넌트와 라이브러리가 포함된 *build.cms_main.js* 파일과  
CMS 기능이 없는, 일반 사용자를 위한 모바일 줌 컴포넌트만이 포함된 *build.main.js*
두 개의 파일로 번들링했습니다.
![프론트엔드 번들링](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/front-bundling.jpg)
*두 개의 Entry point를 가지는 웹 앱으로 번들링*
  
결과적으로 두 개의 웹앱이 만들어진 셈입니다.

#### 개발 포인트
![프론트엔드 개발 포인트](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/front-project-point.jpg)
*프론트엔드 개발 포인트*

1. 컴포넌트 단위 개발
- Side Effect를 최소화하는 **컴포넌트 단위**의 개발
> 제가 가장 중요하게 여긴 부분입니다.  
Side Effect 문제는 함수형 언어를 배워보아야 할 언어로 만들 정도로 아주 중요해졌습니다.
특히 동적 언어이자 Event-Driven 언어인 JS에서는 더욱 조심스럽게 접근해야 한다고 생각합니다.
- 데이터, 이벤트 플로우의 단순화
> 컴포넌트 간의 데이터 처리와 이벤트 플로우를 간단하고 명료하게 구현하기 위해 노력했습니다.  
  
2. SASS(SCSS): 구조적 스타일 및 믹스인 활용 
- 상하위 구조를 가지는 스타일 시트 작성
- 믹스인 및 함수로 작성 코드 최소화
> 스타일 시트에 개발 시간을 뺏기지 않도록 flex box와 믹스인, 함수등을 활용했습니다.
  
3. Webpack: 핫 리로드 및 번들링
- 로더 및 플러그인의 적용(babel, sass, minify)
- 변경 사항을 즉각적으로 확인
> Webpack Dev Server를 이용해 변경 사항을 즉시 확인하고 테스트함으로서 더 빠른 개발을 할 수 있었습니다.

### Back-end: Spring Boot Project
#### 개발 포인트

1. 템플릿과 관련된 코드 최소화: 주요 로직 집중
> 아래에서 말씀드릴 **첫 페이지**를 위한 코드 외에는
> 템플릿 엔진을 이용해 백엔드 데이터를 프론트엔드에 전달하는 보일러 플레이트 코드를 작성할 필요가 없었습니다.

2. Spring Data, Spring Security: 빠르고 강력한 기능들
> 스프링 데이터를 이용하여 ORM 기반으로 데이터베이스와 모델을 구성했고, 
> CMS에서 사용되는 로그인 기능은 스프링 시큐리티를 이용해 구현했습니다.

3. Ehcache를 이용한 캐싱
> 자주 호출되지만 **갱신이 잦지 않은 서비스**에 대해 캐시를 적용하여 DB 쿼리를 줄였습니다.
  
  
### 프로젝트 URL 및 테이블

![프로젝트 URL 구성](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/project-url-control.jpg)
*프로젝트 URL 구성*

프로젝트의 URL은 위 그림과 같이 심플하게 구성했습니다.  
스프링 시큐리티를 이용해 CMS 관련 페이지의 접근을 제한한 것 외에 특별한 사항은 없었습니다.
  
![프로젝트 ERD 구성](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/project-erd.jpg)
*프로젝트 ERD 구성*

제가 추가한 테이블은 위와 같습니다.  
유저당 하나의 네비게이션을 가지고, 네비게이션은 다수의 부모 네비게이션, 부모 네비게이션은 다수의 자식 네비게이션을 가지게 구성했습니다.
* 로그인하지 않은 유저는 관리자가 컨트롤할 수 있는 기본 네비게이션을 사용합니다.
* 네비게이션 스케줄은 부모/자식 네비게이션의 ID를 통해 ON/OFF를 컨트롤합니다.

  
### 모바일 줌
![구현된 모바일 줌 테스트](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-zum-test.gif){:width="300px"}
*Vue.js로 구현한 모바일 줌 테스트*

#### 개요
현재 서비스되고 있는 모바일 줌 페이지를 Vue.js를 이용하여 구현해 보았습니다.  
상단 검색바 및 검색어 추천(stub data), 핫이슈, 메인 페이지와 스와이프, 인피니티 스크롤을 통한 랭킹 뉴스 등을 구현했고, 
실제 서비스에서 제공되는 사용자 경험 통계, 사용자별 기능 등은 포함하지 않았습니다.  
  
#### 컴포넌트 구성
![모바일 줌 컴포넌트 구성](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-zum-components.jpg)
*모바일 줌 컴포넌트 구성*

* 모든 컴포넌트는 Side-effect를 발생시키지 않는 독립적인 컴포넌트로 구성했습니다.
* Navigation 컴포넌트
  * Vue의 라우터를 이용하는 일종의 라우팅 컴포넌트입니다.
* ZumMain 컴포넌트
  * 스와이프 기능을 포함하고 있습니다.
  * 현재 보이는 페이지의 좌/우 페이지를 미리 로드합니다.
  * **페이지 본문**이 5초간 캐싱됩니다. 따라서 5초 내에 페이지를 다시 열면 서버에 요청하지 않습니다. 
* 페이지 컴포넌트
  * 공통 기능은 PageMixin이라는 *믹스인 컴포넌트*로 추상화해 구현했습니다.
  * ZumNewsPage
    * 페이지 최하단에서 내려갈 때 보여지는 *랭킹 뉴스* 관련 기능을 포함합니다.
  * ZumHubPage 컴포넌트
    * 이미지-타이틀로 구성된 허브줌 페이지와 관련된 기능들을 포함합니다.
  
  
#### 서버 구성
![모바일 줌 서버 구성](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-zum-server.jpg)
*모바일 줌 서버 구성*

* 일반적인 Controller-Service-Repository 레이어링을 사용했습니다.
* 템플릿 엔진: 일부 정보는 DOM으로 구성되어 템플릿에 전달됩니다. 이 정보들을 이용해 아래 컴포넌트를 구성합니다.
  * Vue.js 라우터
  * 유저별 네비게이션(상단 메뉴)
  * **접속 URL에 해당하는 첫 페이지**
* 임의의 캐시 시간: 카테고리별로 임의의 캐시 타임아웃을 정해 두었습니다.
  * 네비게이션: 직접 변경 혹은 스케줄링에 따라 네비게이션이 변할 때 캐시를 Eviction하도록 구현했습니다.
  
#### 개발 포인트  
##### 믹스인(mixin) 컴포넌트
뉴스줌 페이지와 허브줌 페이지는 스와이프에 따라 보여지거나 감추고, AJAX를 이용해 페이지를 로드하는 등 기능이 중복됩니다. 
그래서 저는 그런 부분들을 추상화하고 믹스인 컴포넌트로 뽑아내 구현했습니다.
{% highlight javascript %}
/**
 * 메인 페이지의 기본 기능을 위한 믹스인 컴포넌트
 * **/
export default {

  data: function () {
    return {
      isLoading: false, // 현재 페이지가 로딩 중인지 여부
      contentData: [],  // 페이지에서 보여줄 컨텐츠의 raw 데이터 
      isHide: true      // 현재 페이지 노출 여부
    }
  },
  
  // 실제 구현 생략

}
{% endhighlight %}
덕분에 중복 코드를 줄이고 해당 컴포넌트에 필요한 객체만을 선언, 구현 할 수 있었습니다. 

##### SEO(Search Engine Optimize)
자바스크립트 실행을 기반으로 하는 SPA는 그 특성상 크롤러에 노출되기가 쉽지 않습니다. 
대부분의 크롤러는 자바스크립트를 무시하기 때문이죠.  
> 하지만 최근 구글 크롤러는 SPA 사이트를 거의 완벽하게 수집하고 있습니다. 앞으로는 신경 쓰지 않아도 될 수 있겠네요.

웹 사이트의 성향에 따라 **robot.txt** 를 작성하여 
의도적으로 크롤러에 노출되지 않게도 하지만, 대부분의 사이트에 있어 페이지 노출은 아주 중요합니다. 
수익과도 직결되는 문제니까요.

![광고=돈](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/google-adsense.jpg)
*광고=돈의 대표 구글 애드센스*

이 문제를 해결하기 위한 방법이 몇 가지 있습니다.  

###### 1. SSR
말 그대로 Server Side Rendering을 수행하는 방법입니다.  
서버에서 HTML 파일을 전해주기 전에 스크립트를 실행하는 방법인데,  
자바 서버에서는 [Nashorn](http://openjdk.java.net/projects/nashorn/)이나 [셀레니움](https://www.seleniumhq.org/)(혹은 PhantomJS)등을 활용할 수 있습니다.  
하지만 어떤 방법을 선택해도 스크립트를 실행하는 과정 자체가 오버헤드를 발생시킨다는 점은 피할 수 없습니다.  
  
###### 2. Pre-rendering
서버에서 HTML을 클라이언트로 전해줄테니, 그 파일 안에 스크립트를 실행한 결과(DOM)를 미리 만들어 넣어두는 방법입니다.  
꽤 멋진 방법입니다. 간편하게 적용할 수 있고, 별다른 로직 구현이 필요하지 않습니다.  
> Vue.js는 [Nuxt.js](https://ko.nuxtjs.org/), [pre-renderer-spa-plugin](https://github.com/chrisvfritz/prerender-spa-plugin) 등을 이용해 프리렌더링 할 수 있습니다.
  
하지만 페이지가 동적으로 자주 변한다면 어떨까요?  
번들링을 수행할 때 작성된 파일이니 변화가 없을 것이고, 크롤러가 새로운 정보를 가져가지 못합니다.
  
###### 3. 그럼...?
제가 선택한 방법은 앞서 소개해드린 두 가지 방법의 절충안입니다.  
**템플릿 엔진**을 이용하여 HTML 파일에 *페이지에 사용할 데이터*를 DOM으로 만들고, 
클라이언트에서 스크립트를 실행할 때 DOM에 구성되어 있는 **정보**를 파싱하여 페이지에 활용하는 것입니다.  
{% highlight javascript %}
// 모바일 줌 페이지 진입점
new Vue({
  el: '#app',
  router: router,
  components: {ZumApp},
  render: function (h) {
    const $el = this.$el;
    return h(ZumApp, {
      props: {
        navigation: filteredRoute(route),
        $topIssue: $el.querySelector('#top-issue'), // 템플릿에 있는 핫이슈
        $zumMain: $el.querySelector('#zum-main') // 템플릿에 있는 뉴스/허브 등 '메인 페이지'
        // 물론 템플릿에 아무 데이터도 없다면 서버에 요청합니다.
      }
    });
  }
});
{% endhighlight %}

클라이언트로 전달되는 DOM이 Vue.js가 실행되어 만들어지는 *사용자가 보게 될 DOM*과는 다르지만,
노출시키고자 하는 **정보** 자체는 크롤러에 노출됩니다.

![SEO 처리된 페이지](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/seo.jpg)
*Postman으로 확인한 페이지의 모습<br>페이지에서 보여줄 기사가 포함되어 있습니다.*
> 좋은 방법인지는 의문이 남습니다. 파싱-데이터 처리 과정이 추가되기 때문이죠.
  
  
##### 라이브러리 커스터마이즈
모바일 줌 페이지 본문 스와이프 기능은 사용자를 위한 중요한 기능입니다.  
저는 이 기능 구현을 위해 [Lory](http://meandmax.github.io/lory/)라는 라이브러리를 사용했는데, 
JQuery 기반의 다른 라이브러리들과 다르게 Vanilla JS로 구성되었기 때문입니다. 하지만 **복제된 DOM의 동적인 변화**를 지원하지 않는다는 문제가 있었습니다.  
  
좌-우로 끊임없이 스와이프 할 수 있는 *인피니티 스와이프* 기능은 첫 페이지와 마지막 페이지에 **복제된 페이지**를 만들어야 합니다. 
첫 페이지에서 좌측으로(마지막 페이지는 우측으로) 스와이프 할 때 마지막 페이지를 보여주어야 하기 때문입니다.  

![인피니티 스와이프 로직](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/infinity-swipe.jpg)
*infinity swipe 로직*

라이브러리 내에서 페이지를 복제하고 삽입하는데, 삽입된 이후 원본 페이지를 변화시켜도 복제된 페이지가 변하지 않는 문제가 발생합니다.
저는 이 문제를 해결하기 위해 **[MutationObserver](https://developer.mozilla.org/ko/docs/Web/API/MutationObserver)** 객체를 추가했습니다.  
![커스터마이즈된 Lory 라이브러리](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/lory-customize.jpg)

이 객체를 통해 DOM 수정을 감지할 수 있는데, 
*원본* 페이지가 변할 때마다 *복제* 페이지도 갱신하도록 추가 구현하였습니다.

![본문 스와이프](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/swipe-example.gif){:width="300px"}
*구현된 본문 스와이프*

> 사용하는데 문제는 없지만 커스터마이즈된 라이브러리를 프로젝트에 포함했기 때문에
라이브러리를 최신 버전으로 업데이트하기 까다로워진다는 문제가 생겼습니다.
  
  
##### Virtual DOM 활용
JQuery의 문제점 중 하나로 지목되는 것은 전체 Context를 대상으로 하는 JQuery Selector의 성능 문제입니다.
물론 이 문제는 Query Context를 제한함으로서 해결할 수 있습니다.  

하지만 모바일 줌 페이지에서는 페이지 전체 Context를 대상으로 쿼리하는 JQuery Selector가 자주 사용되고 있었습니다.
*그 뿐 아니라* 스와이프 할 때 **삽입된 페이지의 DOM 엘리먼트가 브라우저 성능**에 심각한 영향을 미치고 있습니다.
  
![m.zum.com-devtool](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-zum-devtool.png){:width="600px"}
*스와이프할 때마다 증가하는 노드와 리스너*
> 모바일 페이지 전체를 한바퀴 둘러보면 3500개가 넘는 DOM 엘리먼트가 포함된 **무거운** 웹 페이지가 되어버립니다.
  
저는 Vue.js의 Virtual DOM 기능을 활용하여 **현재 보이는 페이지와 좌,우(스와이프 시 보여질 페이지) 페이지**의 DOM만을 렌더링하고,
당장 보여줄 필요가 없는 나머지 페이지의 DOM은 렌더링하지 않도록 했습니다.
이렇게 구현함으로서 DOM Query 및 렌더링 성능을 크게 향상시킬 수 있었습니다.
  
![Virtual DOM을 통한 성능 향상](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/virtual-dom.jpg)
*렌더링되는 DOM 엘리먼트의 수 자체를 줄임으로써 큰 성능 향상을 노릴 수 있습니다.*

> 제 파일럿 프로젝트에서 만든 페이지와 실 서비스 페이지의 구성 요소는 다르고,
Virtual DOM을 이용해도 메모리에 있는 DOM 노드의 수 자체가 줄어드는 것은 아닙니다.<br>
하지만 서비스되고 있는 페이지는 카테고리의 DOM 수가 800개 이상이고 
더 복잡한 DOM 구조를 가지므로 렌더링 및 DOM Query에서 큰 성능 향상을 기대할 수 있습니다. 
  
## 모바일 줌 CMS
![구현된 모바일 CMS 테스트](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-test.gif)
*구현된 CMS 테스트 화면*

### 개요
모바일 줌 페이지의 네비게이션을 감추거나 보이게 스케줄링하고, 
순서를 바꾸는 기능을 포함하는 CMS를 구현하는 프로젝트였습니다.
저는 앞서 만든 모바일 줌 컴포넌트를 그대로 활용, **미리보기** 기능을 구현하여 아래와 같은 화면을 구성하게 되었습니다.
  
![모바일 CMS](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms.jpg){:width="600px"}
*크게 좌측의 CMS 네비게이션, CMS 본문 그리고 오른쪽에 CMS 미리보기 화면이 있습니다.*  
  
### 컴포넌트 구성
![모바일 CMS 컴포넌트 구성](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-component.jpg)
CMS는 모바일 줌 화면보다 간단하게 구성했습니다.

* CMS 네비게이션
  * CMS 본문 화면을 전환합니다.
* CMS 본문 컴포넌트
  * 조작할 내용에 해당하는 CMS 본문 컴포넌트입니다.
  * 모바일 줌의 페이지 컴포넌트와 마찬가지로 공통 기능을 추상화했습니다.
* CMS 적용 결과 미리보기
  * 모바일 줌 컴포넌트를 그대로 사용하여 미리보기 화면을 구현했습니다.
  
### 서버 구성
![모바일 CMS 서버](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-server.jpg)
모바일 줌 페이지와 마찬가지로 CMS도 Controller-Service-Repository 레이어링을 사용했습니다.  
* 스프링 시큐리티
  * 로그인 페이지에서 인증된 사용자만이 CMS 페이지와 API 등을 사용할 수 있도록 구성했습니다.
* 스프링 스케줄
  * 등록된 스케줄을 실행하기 위한 기능을 구현했습니다(아래에서 자세한 설명)
> CMS에서 지원하는 기능이 많아진다면 기능별, 모듈별 레이어링을 하는 것이 더 좋을 것 같다는 생각이 들었습니다.

### 개발 포인트  
#### 페이지 라우팅
Vue.js는 같은 레벨에서 분리된 두 개의 라우터, 다시말해 보조 라우터(Auxiliary Route)를 지원하지 않습니다.  
따라서 미리보기 용도로 사용하는 *모바일 줌 컴포넌트*가 라우터를 사용하고 있기 때문에 CMS는 최상위 라우터를 사용할 수 없었습니다.   
그래서 저는 메뉴에 따라 다른 **Query parameter를 사용**하여 라우터의 역할을 하도록 구현했습니다.
![모바일 CMS 라우팅](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-routing.jpg)
  
이를 위해 두 가지 작업이 필요했습니다.  
첫 번째는 미리보기가 라우팅될 때 Query Parameter를 그대로 다음 페이지에 가져가는 것이었습니다.
{% highlight javascript %}
router.beforeEach((to, from, next) => {
  const hasQueryParams = (route) => !!Object.keys(route.query).length;
  
  if (hasQueryParams(from) && !hasQueryParams(to)){ // 쿼리 파라미터가 있을 때 파라미터 유지
    next({name: to.name, query: from.query});
  } else {
    next();
  }
});
{% endhighlight %}
두 번째는 라우터 변화를 감시하는 watch 설정입니다.  
CMS 네비게이션을 클릭했을 때 더미 라우터(named router지만 이름이 없는)를 변경하기 때문입니다. 
더미 라우터의 값이 변할 때에도 아래 함수는 실행됩니다.
{% highlight javascript %}
watch: {
      '$route': function (to, from) { // 라우터가 변할 때
        this.getNavigation();         // 쿼리 파라미터를 파싱, 해당하는 본문 컴포넌트 로드
      }
    }
{% endhighlight %}

> Vue.js는 라우팅과 관련된 추가 설정이 아주 간편합니다.    
기능이 너무 강력해 오히려 익히기 힘든 Angular의 Guard보다 더 쉽게, 입맛에 맞게 설정할 수 있을 것 같습니다.
  
#### 네비게이션 순서 변경 및 ON/OFF
CMS의 기본 기능은 네비게이션 컨트롤입니다.  
네비게이션의 상태를 **보이게 혹은 보이지 않게 설정**하거나 네비게이션의 **순서를 변경**하는 기능입니다.  
  
드래그 앤 드랍을 이용해 순서를 바꾸거나 버튼을 이용해 숨김 여부를 설정할 수 있게 구현했습니다.
또, 어떻게 보이는지 우측 미리보기를 이용해 바로 확인할 수 있습니다. 
  
![모바일 CMS 네비게이션 컨트롤](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-navi-control.gif) 

#### 네비게이션 스케줄링
CMS에서 가장 주요했던 기능은 화면에서 입력한 시간에 맞춰 네비게이션을 보이거나 보이지 않게 하는 네비게이션 스케줄링 기능입니다.
![모바일 CMS 네비게이션 스케줄링](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-navi-schedule.jpg) 
  
저는 Spring Schedule을 이용하여 **1분마다 스케줄 메소드를 실행**시키는 방법으로 구현했습니다.

{% highlight java %}
@Scheduled(cron = "1 0/1 * * * *")
  public void navScheduleExecute() {
    this.navScheduleService.executeNavigationSchedule(); // 스케줄 처리 로직 실행
  }
{% endhighlight %}

구체적인 과정은 아래와 같습니다.  
![모바일 CMS 스케줄링](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/mobile-cms-schedule.jpg)

* 이 과정들은 Transaction 처리됩니다.
1. 실행 시간을 초과했고 실행되지 않은 스케줄 쿼리
2. 쿼리된 스케줄에 따라 네비게이션 상세 정보 변경, 스케줄 실행 완료 처리
3. 네비게이션 캐시 eviction

CMS 서버를 재시작했을 때에도 등록된 스케줄을 처리해야 한다는 점을 신경썼고, 
스케줄이 실행되어 네비게이션이 변경되었을 때 네비게이션 캐시를 eviction 하도록 구현했습니다.  
{% highlight java %}
/**
 * 매 분 1초마다 실행되는 스케줄 업데이트 메소드
 * @see com.zum.pilotproject.bean.NavigationScheduler
 */
@CacheEvict(value = "navigation", allEntries = true)
public void executeNavigationSchedule() {

  val time = (new Date()).getTime();

  // 실행되지 않은 스케줄 쿼리
  val changed = this.navScheduleRepository
                    .findAllByIsExecutedAndTimeIsLessThanEqualOrderByTimeAsc(false, time);

  // 변경 작업
  changed.forEach(this::scheduleApply);

}
{% endhighlight %}
  
이번 프로젝트에서는 네비게이션 ON/OFF 스케줄만 구현했지만 스케줄 객체를 구체화하는 것만으로
순서 바꾸기, 이름 바꾸기 등의 기능을 추가할 수 있을 것이라고 생각합니다.

> 하지만 등록된 스케줄이 없을 때에도 메소드가 실행된다는 점이 아쉽습니다. 
기회가 된다면 Reactive X(RxJAVA)를 이용해 Call-back 스타일의 스케줄링도 구현해보고 싶네요.


# 후기

## 개발하며 느꼈던 Vue.js의 장단점
### 장점: Happy Coding!
#### 1. Webpack based
Scala 기반의 서버 프레임워크인 *Play framework가 Spring보다 나은 점*이라는 글을 보며 공감했던 내용이 있습니다. 
Spring은 핫 리로드 지원이 약해 개발자의 개발-테스트 리듬을 망친다는 내용이었죠.  
그런 점에서 Webpack Dev Server를 지원하는 Vue.js를 통한 프론트엔드 개발은 정말 즐겁습니다.  
CTRL + S만으로 띄워놓은 창이 변하니까요!  
게다가 크로스 브라우징을 위한 Babel을 비롯해 수많은, 빠르게 변해가는 모듈과 플러그인 적용이 쉽다는 점도 매력적입니다. 
> 최근 LESS나 SASS같은 css preprocessor를 넘어 JS까지 이용해 CSS에 변화를 주는 PostCSS가 관심을 받고 있습니다.
차후 PostCSS의 플러그인을 적용해야 할 때에도 프로젝트에 큰 변화를 줄 필요가 없다는 점이 아주 매력적입니다. 


#### 2. Easy and Fast, smooth Learning curve
저는 Angular를 공부해왔지만 아직도 하나도 모르는 것 같습니다.  
너무 많은 기능과 선택 사항, 그리고 라이프사이클을 가지니까요.  
하지만 Vue.js는 벌써 할만한데? 라는 느낌입니다. 
훨씬 완만한 러닝 커브에 개발자를 배려한 쉽고 명확한 코드는 아주 매력적입니다.
  
  
> 하지만...

### 단점: There is no sliver bullet
제가 가장 좋아하는 소프트웨어 엔지니어링 명언입니다.  
어디에나 쓸 수 있는 완벽한 것은 없다고 하죠. 
제가 파일럿 프로젝트를 진행하며 느낀 Vue.js의 단점은 학습 성취도가 떨어져서 느끼는 문제일 수도 있고, 
다른 프레임워크(저의 경우는 Angular)와 비슷하게 사용하려다 보니 생긴 문제일 수도 있습니다.
하지만 저와 같은 개발자도 많을 것이라 생각하여 경험을 공유하고자 아래와 같이 정리해 보았습니다. 
  
#### 1. 라우팅
앞서 설명드린대로 Vue.js는 보조 라우터(Auxiliary Route)를 사용하지 못합니다. 미리 정해놓은 라우터 하이라키로 작동할 뿐이죠. 
Vue router 프로젝트의 이슈란을 보면 주기적으로 언급되고 있지만 필요한 use case가 있는지 논의하고 있다는 답변만 있습니다.
  
그들의 주장대로 보조 라우터를 *반드시* 사용해야만 하는 use case는 없을지도 모릅니다.  
하지만 점점 복잡해지고 다양해지는 웹 어플리케이션에서 사용하지 **못하는** 것과 사용하지 **않는** 것은 너무나도 다르다고 생각합니다.

  
#### 2. 데이터 변화 감지
Angular는 데이터의 변화에 따라 컴포넌트를 언제, 어떻게 다시 그릴지를 정하는 ChangeDetectionStrategy라는 옵션과
OnChanges 메소드 등이 있습니다. 하지만 Vue.js에서는 그런 상세한 컨트롤을 할 수 없죠.  
데이터가 변할 때마다 다시 그립니다. 그 변하는 과정을 컨트롤하고 싶다면 데이터 변화 자체를 컨트롤해야 합니다.  

> 조금 더 자세하게 적자면...

Vue.js에서 변화를 감지하는 데이터는 Object.defineProperty를 이용해 set/get 프로퍼티를 선언하고,  
get과 set 프로퍼티를 통해 데이터가 변할 때, Watcher 객체가 DOM 렌더링 작업을 다음 'tick'에 수행하도록 예약합니다.    
그리고 DOM이 렌더링 되는 'tick'에 예약된 작업을 수행합니다. 하지만 'tick'을 컨트롤할 수는 없습니다.  
결국 데이터가 변했을 때 의도적으로 **다시 그리지 않게** 하지는 못 한다는 것입니다.  

  
#### 3. 이벤트
Angular는 Spring과 유사한 형태의 DI를 이용합니다.  
서비스나 컴포넌트의 객체를 만들고, Decorator(Spring의 Autowired 어노테이션과 비슷한)를 이용해 객체를 주입받아서 사용할 수 있습니다. 
Vue.js는 ECMA6의 Import를 이용해 다른 곳에 선언된 객체나 메소드를 사용할 수 있습니다만, 컴포넌트 '객체'의 '이벤트'를
발생시키는데는 무리가 있습니다. 기본적으로 컴포넌트 객체를 참조할 수는 없으니까요. (객체 Holder를 이용할 수는 있겠네요).  
  
아래와 같이 컴포넌트가 중첩되어 있는 구성에서 이벤트를 전달할 방법을 생각해 봅시다.

![Event Dispatch](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/event-dispatch.jpg)
*D 컴포넌트에서 발생한 클릭 이벤트를 어떻게 ⓐ 컴포넌트로 전달해야 할까요?*  
  
  
이벤트가 발생한 D 컴포넌트부터 **순서대로 D -> C -> B -> A -> ⓐ 순으로 전달**하는 것이 일반적이지만  
단순히 이벤트를 *전달*하기 위해 모든 컴포넌트에 이벤트 핸들링 하는 것은 너무 지루하고 복잡한 작업입니다.  
  
이 문제 해결을 위해 몇 가지 방법이 제시되고 있습니다.

* [전역 이벤트 버스 객체](https://kr.vuejs.org/v2/guide/components.html#%EB%B9%84-%EB%B6%80%EB%AA%A8-%EC%9E%90%EC%8B%9D%EA%B0%84-%ED%86%B5%EC%8B%A0)를 만들어 이벤트를 발생시키고 구독하는 방법이 있습니다.
일반적인 문제를 간단하게 해결할 수 있지만 복잡한 이벤트 처리에는 좋지 않습니다. 또, 컴포넌트가 global scope의 이벤트를 참조해야하니 잠재적인 문제가 생길 수도 있습니다.

* [Vuex](https://vuex.vuejs.org/kr/)라는 라이브러리를 사용할 수 있습니다.  
Vuex Store를 통해 데이터의 변화를 커밋하고 데이터의 변화를 **구독하고 있는 컴포넌트에서 처리**하는 방법입니다. 
전역 이벤트 버스와 비슷하지만 더 다양한 기능들을 제공합니다.
  
* Vue.js 2.2버전에서 추가된 provide / inject를 이용하는 방법도 있습니다.  
상위 컴포넌트에 **하위 컴포넌트에서 조작할 데이터**를 가지는 객체를 만들어 놓고, 하위 컴포넌트에서 그 **객체를 주입받는 방법**입니다.
데이터 변화를 감지하기 위해서 직접 Object.defineProperty를 이용해 선언하고 데이터 변경을 핸들링해야 하는 어려움이 있습니다. 
  
프로젝트에 따라 어떤 방법을 선택할지, 어떤 과정으로 처리할지 등 컴포넌트간 이벤트 전달에 대해 생각해 볼 필요가 있습니다. 
컴포넌트가 많고 종속 관계가 복잡하다면 생각하는 시간이 더 길어질 겁니다.
 
### 그럼에도...
Vue.js는 훌륭한 프론트엔드 프레임워크입니다. Github의 Star가 그걸 증명합니다...라고는 말할 수 없지만  
프론트엔드 프레임워크, 라이브러리의 홍수 속에서 *배우기 쉽고 사용하기 쉬운 프레임워크*라는 점 하나만으로도 굉장합니다. 
더 쉽고 빠르게, 현대적인 프론트엔드 개발을 **협업**해야 한다면 저는 자신있게 Vue.js를 추천하겠습니다. 


## 파일럿 프로젝트를 진행하며...
약 한 달간 진행한 파일럿 프로젝트는 사용해보지 않았던 Vue.js를 비롯해 다양한 라이브러리를 
이용해 실제 서비스되고 있는 사이트와 유사한 형태로 개발하는 재미있는 과제였습니다.
  
줌 인터넷의 서비스는 어떤 식으로 되어 있고, 어떤 정보를 제공하는지 파악하고
실제 서비스와 유사하게 직접 구현해 보니 어려운 점도 있었고, 난해한 부분도 있었습니다. 
하지만 그런 난관을 헤쳐나가며 프로젝트와 파이널 리뷰를 진행하니 개발자로서 조금 더 성장한 느낌이 듭니다.  
  
앞으로 줌 인터넷에서 진행하게 될 업무들도 즐겁게, 값지게 보낼 수 있었으면 좋겠습니다.  

![BYE](/images/portal/post/2018-08-23-ZUM-Pilot-partjun/bye.png)
<div style="text-align: center;">
  <span style="background: linear-gradient(to right, red, orange, yellow, green, cyan, blue, violet); 
              -webkit-text-fill-color: transparent; 
              -webkit-background-clip: text; 
              font-size: 24px;
              width: 400px;
              height: 40px;
              line-height: 40px;
              text-align: center;
              display: inline-block;">
  Happy Coding with ZUM internet!
  </span>
</div>