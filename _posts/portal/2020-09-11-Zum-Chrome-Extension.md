---
layout: post
title: 크롬 확장프로그램 개발⛏️ 회고
description: Vue.js를 이용하여 줌 확장프로그램을 개발하는 과정에 대한 회고입니다.
image: /images/portal/post/2020-09-11-Zum-Chrome-Extension/0-thumbnail.png
introduction: Vue.js로 줌 확장프로그램을 개발하는 과정을 공유합니다.
category: portal/tech
tag: [experience, Vue.js, Frontend, 크롬 확장프로그램, 웹스토어 배포, 웹스토어 검수]
---


안녕하세요! 최근에 포털개발팀에서 [Zum NewTab](https://chrome.google.com/webstore/detail/zum-newtab/bghgeookcfdmkoocalbclnhofnenmhlf?hl=ko&authuser=2)
이라는 크롬 확장프로그램을 만들었습니다. 아직 고쳐야할 점도 많고, 사내 테스트를 통해서 조금 더 의견을 모으고 있는 중입니다.
어쨌든 4월부터 6월까지의 확장프로그램을 개발, 배포, 검수하는 과정에서의 **~~삽질한~~** 경험을 공유하고자 이렇게 글을 올립니다.

## 1. 프로젝트 개요

### 크롬 확장프로그램

확장프로그램은 사용자의 브라우징 경험을 긍정적으로 확장시킬 수 있는 작은 **소프트웨어**입니다.
이를 통해 사용자는 브라우저의 기능과 동작을 **개인의 필요 또는 선호도에 맞게 조정**할 수 있습니다.

확장프로그램 개발은 HTML, JavaScript 및 CSS와 같은 **웹 기술을 기반**으로 이루어지며,
**Chrome 개발자 대시 보드**를 통해 배포할 수 있습니다. **이에 대한 내용은 뒤에서 자세하게 다루도록 하겠습니다.**

배포가 완료되면 [Chrome 웹 스토어](https://chrome.google.com/webstore/category/extensions?hl=ko&)에서 다운로드할 수 있습니다.
**앱 개발과 많은 부분에서 유사**합니다.

\* 참고: [https://developer.chrome.com/extensions](https://developer.chrome.com/extensions)

### 확장프로그램 조사

굉장히 다양한 성격의 확장프로그램이 많았고, 먼저 **어떤 형태의 확장프로그램을 만들어야 좋을지** 리서치를 했습니다.

![리서치](/images/portal/post/2020-09-11-Zum-Chrome-Extension/1-research.png)

여러가지 논의가 나왔고 바로가기 링크, 위젯, 웰페이퍼, 검생 등의 기능을 **골고루 포함한** 확장프로그램을 만들기로 결정되었습니다.


## 2. 프로젝트 결과물 소개

먼저 결과물부터 간단하게 소개해드리겠습니다.

![전체화면](/images/portal/post/2020-09-11-Zum-Chrome-Extension/0-thumbnail.png)

결과물은 생각보다 이쁘게 만들어졌습니다 👏👏👏

1. 날씨<br>
![2-weather_1](/images/portal/post/2020-09-11-Zum-Chrome-Extension/2-weather_1.png){:style="height:75px;display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
![2-weather_2](/images/portal/post/2020-09-11-Zum-Chrome-Extension/2-weather_2.png){:style="height:75px;display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
  - 현재 위치에 대한 **기온, 대기상태, 미세먼지 농도** 등을 보여줍니다.
  - 지역별 날씨를 한 눈에 볼 순 없지만 **특정 위치에 대한 날씨**는 조회할 수 있습니다.

2. 시계<br>
![3-clock](/images/portal/post/2020-09-11-Zum-Chrome-Extension/3-clock.png){:style="height:75px;display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
- 현재 시각을 보여줍니다.

3. 운세<br>
![4-fortune](/images/portal/post/2020-09-11-Zum-Chrome-Extension/4-fortune.png){:style="height:200px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}
- 띠별운세, 별자리운세, 개인운세 등을 조회할 수 있습니다.
- 더보기는 검색줌과 연결되어 있습니다.

4. 검색<br>
![5-search](/images/portal/post/2020-09-11-Zum-Chrome-Extension/5-search.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}
- 줌, 네이버, 다음, 구글, 유튜브 등의 검색엔진으로 검색 가능합니다.
- 기획에는 없지만 개인적으로 네이버처럼 키보드 입력시 바로 검색엔진에 커서가 가도록 하고 싶은데 생각만 하는 중입니다.


5. 추천사이트, 자주방문한 사이트<br>
![6-sites](/images/portal/post/2020-09-11-Zum-Chrome-Extension/6-sites.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}
- 추천 사이트를 커스텀하여 관리할 수 있습니다.
- 자주 방문하는 사이트가 자동으로 표시됩니다.
- 개인적으로 제일 많이 사용하는 영역입니다.

6. 주제별 컨텐츠<br>
![7-contents](/images/portal/post/2020-09-11-Zum-Chrome-Extension/7-contents.png)
- 주요뉴스, TV연예, 스포츠, 라이프, 여행/푸드 등의 컨텐츠를 조회할 수 있습니다.
- 개인적으로 라이프, 여행/푸드에 올라오는 컨텐츠가 재미있어서 많이 보는 편입니다.

7. 이슈검색어<br>
![8-issueword](/images/portal/post/2020-09-11-Zum-Chrome-Extension/8-issueword.png){:style="height:400px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}
- 실시간 이슈를 확인할 수 있습니다.
- 사실 눈에 잘 띄지 않아서 UI 개선이 필요한 영역입니다.

8. 설정
- ![9-setting_0](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-setting_0.png){:style="height:200px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}
- 설정 영역의 경우 사이트 좌측 하단에 존재합니다. 잘 보이시나요? ![9-setting_1](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-setting_1.png){:style="height:50px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}
  이렇게 생겼답니다. 이 영역도 어느정도 눈에 띄도록 개편이 필요할 것같습니다.
- 배경화면, 위치설정, 추천사이트 등에 대해 설정할 수 있습니다.
![9-setting_2](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-setting_2.png){:style="height:350px;box-shadow:0 0 10px #ddd;padding:0;margin:0;display:inline-block;"}
![9-setting_3](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-setting_3.png){:style="height:350px;box-shadow:0 0 10px #ddd;padding:0;margin:0;display:inline-block;"}
![9-setting_4](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-setting_4.png){:style="height:350px;box-shadow:0 0 10px #ddd;padding:0;margin:0;display:inline-block;"}  

아직 부족한 부분이 많기 때문에 사내 테스트를 진행중입니다. 조만간 더 멋진 모습으로 거듭나길 기대하고 있답니다!

## 3. 개발 과정 소개

### (1) 프로젝트 구조

```sh
Zum-Chrome-Extension
├─ dist                  # webpack으로 vue project를 패키징한 결과물이 들어있습니다. 
├─ dist-zip              # 확장프로그램의 버전별 압축파일 모음입니다.
├─ public                # 기본적으로 사용될 html,css,js,img 파일들을 모아놓습니다.
├─ scripts               # node.js 스크립트
└─ src                   # webpack의 entry point 입니다.
   ├─ assets             # 컴포넌트에 필요한 resource를 모아놓은 폴더입니다.
   ├─ components         # 컴포넌트들을 모아놓습니다.
   ├─ constant           # 앱 내에서 사용 되는 상수를 모아놓습니다.
   ├─ filters            # Vue Component에서 사용되는 filters를 정의합니다.
   ├─ services           # 각종 서비스 로직을 모아놓습니다.
   ├─ storage            # Local Storage API, Chrome Storage API 등을 추상화하여 관리합니다.  
   ├─ store              # Vuex로 만든 store를 관리합니다.    
   ├─ stub               # 개발모드에서 사용되는 목업 데이터입니다.
   └─ styles             # 스타일시트를 모아놓는 폴더입니다.
```

전체적인 프로젝트 구조입니다. 여기에서 핵심이 되는 부분만 간략하게 설명하겠습니다.

***

**Vue App**

![프로젝트 구조(4)](https://user-images.githubusercontent.com/18749057/93161642-ebdea180-f74d-11ea-9dc1-94372e9a8f00.png)

사내에서 Vue를 사용하고 있기 때문에 **Vue-cli를 이용하여 프로젝트를 구성**하였습니다.

***  

**Manifest.json**

![프로젝트 구조(2)](https://user-images.githubusercontent.com/18749057/93161456-8f7b8200-f74d-11ea-9116-38b03980c0e8.png)

크롬 확장프로그램을 만들 때 제일 중요한 것이 바로 `manifest.json`입니다.
manifest.json은 Vue App을 빌드했을 때 root에 위치해야 하기 때문에 public 폴더에 위치시켰습니다.

이에 대한 설명은 뒤에 상세하게 다루도록 하겠습니다.

***

**Build Script**

![프로젝트 구조(3)](https://user-images.githubusercontent.com/18749057/93161634-e6815700-f74d-11ea-9845-26948ec1f136.png)

확장프로그램을 스토어에 등록하거나 혹은 개발자모드에서 확인 하기 위해선 일단 압축을 해야합니다. <br>
`build-zip.js`를 실행하면 `manifest.json`에 명시된 버전을 파싱하고 `dist` 폴더를 압축하여 <br>
`zum-newtab-v{$version}.zip` 형식의 이름으로 `dist-zip`에 만들어줍니다.

***

여기까지가 크롬 확장프로그램을 만드는데 필요한 최소한의 프로젝트 구성입니다. 이제 본격적으로 어떤식으로 개발했는지 소개하겠습니다.

***

### (2) manifest.json

확장프로그램에서 제일 중요한 게 바로 `manifest.json`입니다.

`manifest.json`은 json 포맷 파일로서, 모든 웹 익스텐션이 포함하고 있어야 하는 파일이며
`manifest.json`에 확장프로그램의 이름, 버젼과 같은 기본 정보를 명시해야 합니다.
뿐만아니라 반드시 확장프로그램이 사용하는 기능을 명시해야합니다.<br>
(ex: `background scripts` `content scripts` `browser actions`)

그리고 **실행할 HTML, Javascript 등을 지정**할 수 있습니다.

- [Getting Started Extension Tutorial](https://developer.chrome.com/extensions/getstarted)
- [manifest.json이란?](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json)

그래서 `manifest.json`만 보면 확장프로그램이 어떤 일을 하는지 대강 확인해볼 수 있습니다.

```js
{
  "manifest_version": 2, // Manifest 버전 명시. 공식문서 가이드에 따라 `2`로 고정
  "name": "Zum NewTab", // 확장 프로그램 이름
  "description": "New Tab 활용하여 사용자의 웹 서핑 생산성을 높여주는 줌 시작페이지 제공",
  "version": "1.1.7.0", // 확장 프로그램 버전

  "browser_action": {
    "default_icon": "icon.png" // 확장 프로그램의 아이콘
  },

  "permissions": [
    "bookmarks",             // 북마크에 접근할 수 있는 API 사용 권한
    "topSites",              // 자주방문한 사이트 목록을 조회할 수 있는 API 사용 권한
    "https://*.zum.com/*"    // 모든 zum.com host에 접근할 수 있는 권한
    // "<all_urls>"          // 모든 호스트(사이트)에 접근할 수 있는 권한
    // "activeTab",          // 현재 활성중인 탭에 대해 다룰 수 있는 API 사용 권한
    // "tabs",               // 열려 있는 탭에 대해 다룰 수 있는 API 사용 권한
    // "storage",            // 일종의 브라우저 데이터베이스 API 사용 권한
    // "history",            // 방문기록에 접근할 수 있는 API 사용 권한
  ], 

  // 리소스에 대한 보안정책을 설정. 줄여서 CSP라고 불린다.
  "content_security_policy":  "script-src 'self' 'unsafe-eval'; script-src-elem 'self' 'unsafe-eval' https://ssug.api.search.zum.com https://contentsgt.cafe24.com; object-src 'self'; img-src chrome://favicon/ https://*.zumst.com/;",

  "chrome_url_overrides": {
    "newtab": "index.html" // 새 탭을 열었을 때 보여지는 페이지를 설정할 수 있습니다.
  }
}
```

#### 1) Content Security Policy (CSP)

HTTP Response Header에 [Content Security Policy](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Content-Security-Policy)라는 것을 명시하여 보내줄 수 있습니다. 

- HTTP Content-Security-Policy 응답 헤더를 사용하면 **사용자 에이전트가 주어진 페이지에 대해로드 할 수있는 리소스를 제어** 할 수 있습니다.
- 몇 가지 예외를 제외하고 정책에는 대부분 **서버 원본 및 스크립트 end-point 지정이 포함**됩니다.
- 이는 크로스 사이트 **스크립팅 공격 (XSS)으로부터 보호하는 데 도움**됩니다.

요약하자면 요청한 리소스가 어떤 권한을 사용할 것인지 정확히 명시하는 과정이라고 보면 좋을 것 같습니다.

`manifest.json`에 명시한 내용을 조금 더 살펴봅시다.

```sh
# JavaScript의 유효한 소스(source, src)를 지정합니다.
script-src 'self' 'unsafe-eval';

# <script> 요소의 유효한 소스(source, src)를 지정합니다.
script-src-elem 'self' 'unsafe-eval' https://ssug.api.search.zum.com https://contentsgt.cafe24.com;

# <object>, <embed> 및 <applet> 태그에 대한 유효한 소스(source, src)를 지정합니다.
object-src 'self';

# 이미지 및 파비콘의 유효한 소스(source, src)를 지정합니다.
img-src chrome://favicon/ https://*.zumst.com/;
```

이렇게 명시했기 때문에 확장프로그램 내에서 외부 리소스를 요청하면 다음과 같이 CSP가 포함된 응답을 건내줍니다.

![10-CSP](/images/portal/post/2020-09-11-Zum-Chrome-Extension/10-CSP.png)

그리고 [이 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)를 살펴보면
`<meta>` 태그를 이용하여 다음과 같이 명시하는 것도 가능합니다.

`<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src https://*; child-src 'none';">`

필자는 확장프로그램을 개발할 때 말곤 아직 `CSP`를 사용해본적이 없습니다. 

***

#### 2) Chrome API

다음에 소개할 것은 [Chrome API](https://developer.chrome.com/apps/api_index)입니다.

`manifest.json`에 다음과 같이 어떤 Chrome API를 사용할지 명시할 수 있습니다.

```js
{
  ...
  "permissions": [
    "bookmarks", // 북마크를 조회할 수 있는 API
    "topSites",  // 자주 방문한 사이트를 조회할 수 있는 API
  ],
  ...
}
```

위에 명시한 API들은 다음과 같이 사용할 수 있습니다.

``` js

chrome.topSites.get(console.log); // 자주 방문한 사이트를 조회할 수 있습니다.
chrome.bookmarks.getTree(console.log); // 북마크를 트리 형태로 조회할 수 있습니다.

```

![11-chrome-api_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/11-chrome-api_1.png)
![11-chrome-api_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/11-chrome-api_2.png)

API 호출 결과는 `callback`에게 반환하기 때문에 조금 더 유연하게 사용하기 위해선 `Promise`로 감싸서 사용해야합니다.

```js
const BookmarkService = Object.freeze({

  /** 북마크 트리를 가져옵니다. **/
  getTree () {
    return new Promise(resolve => {
      chrome.bookmarks.getTree(([ tree ]) => resolve(tree));
    })
  },

  /** 북마크의 트리를 목록으로 변환하여 가져옵니다. **/
  async getListAboutTree () {
    const tree = await this.getTree()
    let bookmarks = tree.children.flatMap(v => v.children);
    while (bookmarks.find(v => v.children)) {
      bookmarks = bookmarks.flatMap(v => v.children || [ v ])
    }
    return bookmarks.map(({ id, title, url }) => ({ id, title, url }));
  },
});

// 다음과 같이 사용할 수 있습니다.
BookmarkService.getTree().then(console.log);
BookmarkService.getListAboutTree().then(console.log);
```

#### 3) Development Mode

확장프로그램을 개발할 땐 **로컬서버에서 작업**했습니다.
크롬에 확장프로그램 개발모드가 따로 있어서 이를 이용해도 됐으나,
**퍼블리싱팀과의 협업**을 위해서 비교적 개발환경 자체는 **퍼블리싱팀이 최대한 신경쓰지 않도록 작업**하는게 필요했습니다.

논외로 [Webpack Chrome Extension Reloader](https://www.npmjs.com/package/webpack-chrome-extension-reloader)를 이용하면 웹팩을 이용하여 개발할때 확장프로그램을 계속 리로드할 수 있습니다.

```js
// BookmarkService.js

export default Object.freeze({
  fetchBookmarks () {
    // 개발 환경에서는 stub data를 반환합니다.
    if (process.env.NODE_ENV === 'development') {
      return resolve(require('../stub/bookmarks'));
    }
    return new Promise(resolve => {    
      chrome.bookmarks.getTree(([ tree ]) => {
          let temp = tree.children.flatMap(v => v.children);
          while (temp.find(v => v.children)) {
            temp = temp.flatMap(v => v.children || [ v ]);
          }
          // BookmarkTreeNode에서 title과 url만 뽑아온다.
          resolve(temp.map(({ title, url }) => ({ title, url: url || '' })))
        }
      )
    });
  }
});
```

위의 코드는 사용자의 북마크를 가져오는 역할을 수행하고 있습니다.
그런데 개발 모드에서는 Webpack dev-server에서 결과물을 확인하기 때문에 Chrome API를 사용할 수 없습니다.
그래서 **현재 환경이 development 일 땐 stub data를 가져오도록** 만들었습니다.

```js
if (process.env.NODE_ENV === 'development') {
  return resolve(require('../stub/bookmarks'));
}
```

여기서 핵심은 다음과 같습니다.

- 조건문에 직접적으로 `process.env.NODE_ENV`를 언급 해야합니다.
- `process.env.NODE_ENV`를 변수에 담아서 사용하면 안 됩니다.
- `import`를 통해서 데이터를 미리 가져오는 것이 아니라 **if 내부**에서 `require`로 stub data를 가져와야 합니다. 

**이는 build 시점에 stub data가 bundle에 포함되지 않게 하기 위함입니다.**
이처럼 webpack에서 `process.env`와 `require`를 이용하여 bundle 시점에 포함되는 데이터의 여부를 간단하게 표현할 수 있습니다.
 

## 4. 시스템 아키텍쳐

## 5. 배포 과정 소개

## 6. 지옥의 검수 과정

## 7. 앞으로의 계획

