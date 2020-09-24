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

***

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

***

## 2. 프로젝트 결과물 소개

👉👉👉 **[확장프로그램(Zum NewTab) 다운로드](https://chrome.google.com/webstore/detail/zum-newtab/bghgeookcfdmkoocalbclnhofnenmhlf?hl=ko&authuser=2)** 👈👈👈

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

***

최근에 사내테스트를 진행 했고, 위의 내용을 조금씩 더 개선중입니다. 더 멋진 모습으로 소개해드릴 날이 올 수 있습니다!

***

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

***

#### 3) 개발모드에 대한 핸들링

![13-localserver](/images/portal/post/2020-09-11-Zum-Chrome-Extension/13-localserver.jpg)

확장프로그램을 개발할 땐 **로컬서버에서 작업**했습니다.
크롬에 확장프로그램 개발모드가 따로 있어서 이를 이용해도 됐으나,
**퍼블리싱팀과의 협업**을 위해서 비교적 개발환경 자체는 **퍼블리싱팀이 최대한 신경쓰지 않도록 작업**하는게 필요했습니다.

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
 
***
 
사이트의 파비콘의 경우 확장프로그램에서는 `chrome://favicon/**` 형태의 `Favicon API`를 사용하면 됩니다.

- 예시) `chrome://favicon/size/24/https://zum.com/`

그런데 이건 **확장프로그램에서만 호출 가능한 API**입니다.
그래서 개발 환경에선 **실제 웹 서비스로 제공되는 `Favicon API`를 사용**해야 했습니다.

쭉 찾아본 결과, 구글에서 제공하는 API를 발견할 수 있었습니다.

- `https://www.google.com/s2/favicons?sz=24&domain=https://zum.com/`
- 출력: ![구글 파비콘](https://www.google.com/s2/favicons?sz=24&domain=https://zum.com/){:style="display:inline-block;width:24px;height:24px;border:1px solid #000;padding:0;margin:0;vertical-align:middle;"}

프로덕션 모드에서 해당 API를 사용해도 무방하지만 **도메인이 존재하는 API에 요청을 한다는 것 자체가 검수 과정에서 문제**가될 수 있습니다.
그래서 배포할 땐 `chrome://favicon`을 사용했고, 개발환경에선 `https://www.google.com/s2/favicons`을 사용했습니다.

***

사실 이러한 과정이 필요했던 이유는 **퍼블리싱 팀과의 협업 때문**입니다.
오직 개발에만 집중할 수 있는 환경이 필요하다면
[Webpack Chrome Extension Reloader](https://www.npmjs.com/package/webpack-chrome-extension-reloader) 패키지를 이용하면 좋습니다.

이 패키지는 크롬 확장프로그램을 웹팩 환경에서 개발할 수 있도록 도와줍니다.

***

#### 4) 확장프로그램을 크롬 개발자 모드에서 확인하기

앞서 언급한 것들은 `Webpack Dev-Server`에서 작업할 때 필요한 과정이었습니다.
이번에는 확장프로그램을 크롬 개발자 모드에서 확인하는 방법에 대해 소개하겠습니다.

- 크롬 브라우저에서 주소창에 `chrome://extensions/`을 치고 접근하면 설치된 `확장프로그램 목록`을 확인할 수 있습니다.
![15-devmode_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/15-devmode_01.jpg){:style="border:1px solid #666;padding:0;margin:0"}

- `개발자 모드`를 활성화하면 `압축해제된 확장 프로그램을 로드합니다.` 버튼이 생기고, 각각의 확장프로그램에 대한 `meta` 정보도 볼 수 있습니다.
![15-devmode_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/15-devmode_02.jpg){:style="border:1px solid #666;padding:0;margin:0"}
`압축해제된 확장 프로그램을 로드합니다.`를 클릭한 후에 확장프로그램을 업로드하면 됩니다!

- 이 때 `manifest.json`이 포함된 폴더를 업로드 해야합니다.
![15-devmode_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/15-devmode_01.gif){:style="border:1px solid #666;padding:0;margin:0"}

- 혹은 `드래그 앤 드롭`으로 추가할 수 있습니다. 이 때 `manifest.json`이 폴더나 압축파일에 포함되어 있어야 합니다.
![15-devmode_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/15-devmode_02.gif){:style="border:1px solid #666;padding:0;margin:0"}

위의 과정을 거쳐서 개발된 확장프로그램의 기능이 정상적으로 작동하는지 확인해볼 수 있습니다.

## 4. 시스템 아키텍쳐

![12-architecture_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/12-architecture_01.png)

시스템의 전체적인 흐름을 설명하자면

1. 사용자가 뉴탭을 통해 확장프로그램에 진입합니다.
2. 브라우저에서 **외부에 개방되어 있는 API에 접근**합니다.
  - 개인운세 API
  - 줌앱 API
  - 검색어 제안 API
3. 줌앱 API는 다시 **내부적으로만 사용하는 Internal API에 접근**합니다.
  - Internal API는 **줌프런트와 모바일줌에서 사용**하는 API입니다.
4. Internal API에서 다시 필요한 API를 호출하고, 호출결과를 잘 조합하여 줌앱 API에게 response로 내보냅니다.
5. 결과적으로 줌앱 API는 **일종의 Proxy 역할**을 수행합니다.

***

### (1) 외부에 개방되어 있는 API

![12-architecture_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/12-architecture_02.png)

크롬 확장프로그램에선 이렇게 3개의 API만 호출합니다. 

1. Personal Fortune API
  - Input: 성별, 생년월일
  - Output: 오늘의 운세 
2. Search Suggest API
  - Input: 검색어
  - Output: 추천검색어
3. Zum App API
  - 본래 사용 용도는 **줌앱에서 필요한 데이터를 가져오기위해** 만들어졌습니다.
  - 즉, 외부에서의 접근이 가능한 API입니다.
  - 팀원과 팀장님과 논의한 결과로 확장프로그램에서 필요한 데이터도 줌앱 API에서 만들기로 하였습니다.
  - 줌앱API는 **주기적으로 Intenral API를 호출하고 캐싱**합니다.
  - 따라서 **사용자는 항상 캐싱된 데이터를 이용**하게 됩니다.
  
***

### (2) Internal API

![12-architecture_03](/images/portal/post/2020-09-11-Zum-Chrome-Extension/12-architecture_03.png)

앞서 언급했지만, Internal API는 [줌프런트](http://zum.com)와 [모바일줌](http://m.zum.com)에서 호출하는 API입니다.
그렇기 때문에 컨텐츠를 제공하기에 적합한 API였고, 모바일줌의 컨텐츠와 겹치는 것들이 있었습니다.
덕분에 확장프로그램과 관련된 API는 큰 어려움 없이 만들 수 있었습니다.

Internal API에서 내려주는 컨텐츠는 다음과 같습니다.

- 별자리 운세, 띠별 운세
- 날씨 및 대기 정보
- 주제별 컨텐츠
- 실시간 이슈 키워드

***

### (3) Target API

![12-architecture_04](/images/portal/post/2020-09-11-Zum-Chrome-Extension/12-architecture_04.png)

`Target API`는 사용자(클라이언트)의 **IP주소를 넘겨주면, 현재 위치(주소)를 알려주는 API**입니다.
`Target API`를 사용할 경우 **IP 주소를 기준으로 캐싱** 처리가 필요합니다.
그래서 **App API에서 넘겨주는 형태**로 만들었습니다.
 
만약에 `Internal API`에 구현한다고 치면 `Internal API`에서 캐싱을 하고,
`App API`에서도 캐싱을 해야하기 때문에 **자원을 두 배로 소모**합니다.

***

### (4) Front-End

![12-architecture_05](/images/portal/post/2020-09-11-Zum-Chrome-Extension/12-architecture_05.png)

Front-End는 위와 같은 모습으로 설계하였습니다. 일반적인 `Single Page Application` 프로젝트의 구조입니다.

- Vue CLI를 이용하여 Vue Project를 구성할 경우 webpack 기반의 개발환경이 만들어집니다.
- 개발이 완료되면 다시 Webpack Build를 이용하여 HTML, CSS, JS 등으로 번들링합니다.

이에대해 조금 더 구체적으로 설명하기 위해선 프로젝트의 `package.json`이 필요합니다.

```js
{
  "name": "zum-chrome-extension",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "publish": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "build-zip": "node scripts/build-zip.js",
    "build-and-zip": "vue-cli-service build && node scripts/build-zip.js"
  },
  "dependencies": {
    "@babel/plugin-proposal-optional-chaining": "^7.8.3",
    "core-js": "^3.6.5",
    "fetch-jsonp": "^1.1.3",
    "reset-css": "^5.0.1",
    "vue": "^2.6.11",
    "vue-loader": "^15.8.3",
    "vuex": "^3.1.1"
  },
  "devDependencies": {
    "@vue/cli-plugin-babel": "^4.4.1",
    "@vue/cli-plugin-vuex": "^4.4.1",
    "@vue/cli-service": "^4.4.1",
    "archiver": "^4.0.1",
    "node-sass": "^4.14.1",
    "sass-loader": "^8.0.2",
    "vue-template-compiler": "^2.6.11"
  }
}
```

사실 Vue-cli를 통해서 설치된 것 이외에는 거의 외부 패키지를 설치하지 않았습니다.
여기서 `scripts` 부분만 조금 더 살펴보겠습니다.

```js
{
  /* ... 생략 ... */
  "scripts": {
    // 개발 서버를 실행합니다.
    "publish": "vue-cli-service serve",

    // webpack으로 src폴더를 패키징하여 public폴더에 합친 후 dist폴더에 저장합니다.
    "build": "vue-cli-service build",

    // dist폴더를 압축하여 dist-zip에 저장합니다.
    "build-zip": "node scripts/build-zip.js",

    // build와 build-zip를 동시에 실행합니다.
    "build-and-zip": "vue-cli-service build && node scripts/build-zip.js"
  },
  /* ... 생략 ... */
}
```

터미널에서는 다음과 같이 사용할 수 있습니다.

```shell
# 개발 서버를 실행합니다. 
> npm run publish
> yarn publish

# webpack으로 src폴더를 패키징하여 public폴더에 합친 후 dist폴더에 저장합니다.
> npm run build
> yarn build

# dist폴더를 압축하여 dist-zip에 저장합니다.
> npm run build-zip
> yarn build-zip

# build와 build-zip를 동시에 실행합니다.
> npm run build-and-zip
> yarn build-and-zip
```

다른 `SPA` 프로젝트와 구분되는 부분이 보이지 않나요?
확장프로그램의 경우 앱 소스를 zip 파일로 만들어야 하기 때문에 build만 하는게 아니라 build된 폴더를 zip으로 구성하는 스크립트를 만들어야 했습니다.

코드로 확인해봅시다!

```js
// scripts/build-zip.js
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');
const DEST_DIR = path.join(__dirname, '../dist');
const DEST_ZIP_DIR = path.join(__dirname, '../dist-zip');

function extractExtensionData () {
  const manifest = require('../public/manifest.json');
  const name = manifest.name.toLowerCase().replace(/\s/g, '-');
  const version = manifest.version.replace(/\./g, '_');
  return { name, version };
};

function buildZip (src, dist, zipFilename) {
  console.info(`Building ${zipFilename}...`);
  const zipFilePath = path.join(dist, zipFilename);

  if (fs.existsSync(zipFilePath)) {
    fs.unlinkSync(zipFilePath);
  }

  const archive = archiver('zip', { zlib: { level: 9 }});
  const stream = fs.createWriteStream(zipFilePath);
  
  return new Promise((resolve, reject) => {
    archive.directory(src, false)
           .on('error', reject)
           .pipe(stream);

    stream.on('close', resolve);
    archive.finalize();
  });
}

const {name, version} = extractExtensionData();
const zipFilename = `${name}-v${version}.zip`;

if(!fs.existsSync(DEST_ZIP_DIR)) fs.mkdirSync(DEST_ZIP_DIR);

buildZip(DEST_DIR, DEST_ZIP_DIR, zipFilename)
  .then(() => console.info('SUCCESS'))
  .catch(console.err);
``` 

- zip은 [archiver](https://www.npmjs.com/package/archiver) 패키지를 사용해서 만들 수 있습니다.
- 코드는 [Kocal/vue-web-extension Repository](https://github.com/Kocal/vue-web-extension/blob/v1/template/scripts/build-zip.js)에서 참고하였습니다.
- 전체적인 흐름은 다음과 같습니다.
  - build 폴더를 압축한다.
  - 이 때 `public/manifest.json`에 있는 `name` `version` 정보를 읽어온다.
  - 압축 파일의 이름은 `${name}-v${version}.zip` 형태로 만든다.
  - 압축 파일은 `build-zip` 폴더에 저장한다.

따라서 `build-and-zip`을 실행할 경우, **build를 하자마자 바로 build-zip 폴더에 압축하여 저장**하게 됩니다.

***

### 🚩 정리

여기까지 프로젝트 구조를 살펴봤습니다. 다시 정리하자면 다음과 같습니다.

- `back-end`
  - 크롬 확장프로그램은 웹서비스가 아니기 때문에 확장프로그램 전용 서버가 존재하지 않습니다.
    - 따라서 확장프로그램에서 API를 사용할 땐 외부에서 접근 가능한 API를 사용해야 합니다.
    - 그리고 API에 대한 Permission 설정이 필요합니다.
  - `Zum NewTab`은 `Zum App API` `Zum Search Suggest API` `Personal Fortune API` 등 세 개의 API와 직접적으로 통신합니다.
  - `Zum App API`는 다시 `Internal API` `Target API`와 통신합니다.
    - `Internal API`에서 대부분의 데이터를 정제하여 내보내줍니다.
    - `Target API`는 `IP Address` 기반으로 캐싱하여 사용합니다.
    - `Internal API`를 주기적으로 호출하고, 이 때 전체 데이터를 캐싱합니다.
  - 결과적으로 사용자는 항상 캐싱된 데이터를 조회하게 됩니다.
- `front-end`
  - `Vue-cli`를 이용하여 `Single Page Application` 형태로 구성하였습니다.

사용하는 API가 많기 때문에 **확장프로그램치곤 조금 복잡한 형태**를 띄고 있습니다.

***

## 5. 배포 과정 소개

이제 앱스토어에 배포하는 과정에 대해 간단하게 소개하겠습니다.

- [크롬 웹 스토어](https://chrome.google.com/webstore/category/extensions?hl=ko&authuser=2)에 접속 후 `설정 아이콘`을 클릭하면 `개발자 대시보드` 메뉴가 보입니다. 
![14-01_webstore](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-01_webstore.jpg){:style="border:1px solid #666;padding:0;margin:0"}

- 대시보드에 접근하고, 확장프로그램을 등록하기 위해선 `등록수수료(5$)`를 결제해야합니다. 
![14-02_dashboard](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-02_dashboard.jpg){:style="border:1px solid #666;padding:0;margin:0"}

- 다음과 같은 정보들을 입력하고 결제를 진행하면 됩니다.
![14-03_cash](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-03_cash.jpg){:style="border:1px solid #666;padding:0;margin:0"}

- 등록 수수로 결제가 완료되면 [대시보드](https://chrome.google.com/u/2/webstore/devconsole/a5efa500-a9c0-4385-b070-b1873b2d8212?hl=ko) 페이지에 접근할 수 있습니다.
![14-04_new_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-04_new_01.jpg){:style="border:1px solid #666;padding:0;margin:0"}

- `새 항목` 버튼을 클릭하면 항목을 추가하는 팝업이 열립니다. `파일 탐색` 버튼을 클릭하여 `확장프로그램 zip 파일`을 업로드하면 됩니다.
![14-04_new_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-04_new_02.jpg){:style="border:1px solid #666;padding:0;margin:0"}

- 업로드가 완료되면 확장프로그램의 정보를 입력하는 페이지로 넘어갑니다. 먼저 `스토어 등록정보`에서 `설명`란을 입력해야합니다. 나머지는 `manifest.json`의 내용으로 채워집니다.
![14-05_detail_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-05_detail_01.jpg){:style="border:1px solid #666;padding:0;margin:0;"}

- `그래픽 저작물`은 확장프로그램 설치 페이지에 접근했을 때 보여지는 이미지입니다. 규격에 맞게 이미지를 만들어서 업로드하면 됩니다
![14-05_detail_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-05_detail_02.jpg){:style="border:1px solid #666;padding:0;margin:0;"}

- `추가 입력란`에는 확장프로그램에 대한 문의를 받을 수 있는 정보들을 입력합니다.
![14-05_detail_03](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-05_detail_03.jpg){:style="border:1px solid #666;padding:0;margin:0;"}

- `개인정보 보호 탭`에서 `manifest.json`에 정의한 `permission`에 대한 설명을 작성해야합니다.
![14-05_detail_04](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-05_detail_04.jpg){:style="border:1px solid #666;padding:0;margin:0;"}

- 앞서 언급한 항목들을 모두 입력한 뒤에 제출하면 `검수`후에 `거부` 및 `게시` 여부를 이메일로 알려주고, 대시보드에서 확인할 수 있습니다.
![14-05_detail_05](/images/portal/post/2020-09-11-Zum-Chrome-Extension/14-05_detail_05.jpg){:style="border:1px solid #666;padding:0;margin:0;"}

이렇게 배포하는 과정은 어렵지 않습니다.

아직 최종 관문인 `지옥의 검수과정`이 남았습니다. ~~검수 과정 때문에 정말 힘들었습니다..~~

***

## 6. 지옥의 검수 과정

이제 검수과정에 대해 ~~하소연~~**소개**합니다.

***

### (1) 첫 번째 게시 요청

- 5월 29일에 개발이 완료되어서 6월 1일에 첫 번째 게시 요청을 올렸습니다.
- **그리고, 정말 다양한 사유로 반려되었습니다.**
![16-validate_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_01.jpg){:style="border:1px solid #666;padding:0;margin:0;"}
- 사실 예상했던 일이었습니다.
- ~~그러나 검수 과정이 한 달 넘게 지속 될 것은 예상하지 못했죠..~~

***

### (2) 문제점 분석 및 대처

먼저 문제가 될 만한 것들을 생각해봤습니다.

1. API 호출에 대한 이슈
  - `JSONP`를 사용해도 되는가
    - 일부 API를 `JSONP`로 사용하고 있습니다.
  - 꼭 호출하는 API의 도메인이 **개발자의 소유**여야만 하는가
    - 그렇다면 `Open API`는 어떻게 이용해야 하는가?
2. Manifest.json에서 `permission 설정`에 대한 이슈
  - **정말로 필요한 권한**인가?
3. `Content Security Policy` 설정 이슈
4. `Chrome API`에 대한 이슈
5. **컨텐츠 자체**의 이슈
  - 사용해도 무방한 컨텐츠인가?
  - **컨텐츠가 포함되어도 상관 없는가?**
6. Zum Front End Core에 대한 이슈
  - **대부분의 Front-End 프로젝트에 Zum Front Core Pacakge를 사용**하고 있었습니다.
  - 따라서 확장프로그램에도 자연스럽게 Core를 적용했습니다.
  - 뒤에 서술하겠지만, 결론만 말하자면 **결정적으로 Core에 문제가 있었습니다.**

이렇게 정리한 다음에 다음과 같은 조치를 취하였습니다.

- 빈 화면 부터 시작하여 각각의 컴포넌트를 쪼개어서 한 번에 검수 요청을 보냈습니다.
  - 일단 `외부 API 요청`이 필요하지 않은 모듈부터 검수요청을 보냈습니다.
  - `검색 모듈`
    ![16-validate_03](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_03.png){:style="border:1px solid #666;padding:0;margin:0;"}
  - `시계 모듈`
    ![16-validate_02](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_02.png){:style="border:1px solid #666;padding:0;margin:0;"}
  - `메모 모듈`
    ![16-validate_04](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_04.png){:style="border:1px solid #666;padding:0;margin:0;"}
  - `사이트 모듈`
    ![16-validate_05](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_05.png){:style="border:1px solid #666;padding:0;margin:0;"}
- **모든 API를 제외하고 MockUp 데이터만 사용**하여 올렸습니다.
- **확장프로그램의 제목, 설명, 스크린샷 등을 수정**하여 올렸습니다.

그 결과..

![16-validate_06](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_06.png){:style="border:1px solid #666;padding:0;margin:0;"}

**전부 반려되었습니다....**

![emoticon_01](/images/portal/post/2020-09-11-Zum-Chrome-Extension/emoticon_01.png)

이 결과를 확인했을 때 많이 들어본 말이 떠올랐습니다.

> 눈을 감아보세요. 아무것도 안 보이죠? 네 그게 당신의 미래입니다.

말 그대로 눈 앞이 깜깜했습니다..

***

### (3) 다시 문제점 분석

팀장님, 팀원들과 머리를 맞대고 다시 고민을 시작했습니다.

- **Zum Front Core Package에 권한과 관련된 코드**가 있었습니다.
- 즉, **Core Pacakge를 포함하면 반려될 가능성이 매우 높다**는 것을 알았습니다.
  - 사실 거의 확정하고 있었습니다.
- 그래서 Core를 제거하고, **앞선 과정(처음부터 다시만들기)을 반복**했습니다.

![16-validate_07](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_07.png){:style="border:1px solid #666;padding:0;margin:0;"}

***

### (4) 첫 검수 통과

Core 패키지를 제외한 후에 검수 요청한 것들은 대부분 통과했습니다.

![16-validate_08](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_08.png){:style="border:1px solid #666;padding:0;margin:0;"}

![emoticon_03](/images/portal/post/2020-09-11-Zum-Chrome-Extension/emoticon_03.png){:style="padding:0;margin:0;display:inline-block"}
![emoticon_04](/images/portal/post/2020-09-11-Zum-Chrome-Extension/emoticon_04.png){:style="padding:0;margin:0;display:inline-block"}

**이 때 알 수 있던 사실은 다음과 같습니다.**

1. `컨텐츠 자체`에는 문제가 없다.
2. `JSONP`를 사용해도 된다.

일단 검수가 성공했기 때문에 **여태까지 정리해놓은 이슈들을 하나씩 테스트**할 수 있었습니다.

***

### (5) 이어진 분석 - 검수 과정에서 알 수 있었던 것들

1. **API 호출은 소유자가 아니여도 상관 없었습니다.**
  - 단, **모든 요청은 https**로 보내야합니다. 👈👈👈 매우중요합니다!
  
2. 확장프로그램 전용으로 사용할 수 있는 `Chrome API`는 **Manifest.json에 명시한게 아닐 경우,**
  API가 호출 가능한지만 체크하는 코드 또한 반려사유가 될 수 있습니다.
  - ex) `if (chrome.store) { /*...*/ }` 이런 코드 또한 반려사유가 됩니다.
  
3. 반대로 **Manifest.json에 명시했으나 사용하지 않는 기능**이 있을 경우에도 반려 사유가 됩니다.

4. **개인정보 처리방침**이 필요합니다.

5. 리소스를 `base64`로 사용하면 안 됩니다.
  - **webpack을 사용하면 기본적으로 작은 용량의 파일을 base64로 만듭니다.**
  - 그래서 vue.config.js 혹은 webpack.config.js에 다음과 같은 코드를 삽입해줘야합니다.

```js
// vue.config.js
module.exports = {
  /* 생략 */
  chainWebpack: config => config.module
                                   .rule('images')
                                   .use('url-loader')
                                   .loader('url-loader')
                                   .tap(options => ({ ...options, limit: -1 }));
  },
  /* 생략 */
};
```

위의 과정들을 거치면서 이제 정말 검수는 문제 없겠구나 생각했습니다.
실제로 3번 정도는 큰 문제없이 통과했습니다.

**그런데 약 한 달을 더 검수에 더 시달려야했습니다... 😂😂**

![16-validate_09](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_09.png){:style="border:1px solid #666;padding:0;margin:0;"}

이렇게 반려된 이유는 `검색 모듈` 때문이었는데

![16-validate_03](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_03.png){:style="border:1px solid #666;padding:0;margin:0;"}

사용자에게 무언가를 입력받은 후 특정 페이지에 넘겨줄 경우, 마찬가지로 `https`로 처리해야 했습니다.
즉, 입력정보를 암호화해야 하는 것입니다.

`search.zum.com`은 타 팀에서 관리하는 프로젝트이기 때문에 `https`전환을 요청했고, 약 한 달 정도 기다려야 했습니다.
일단 손놓고 기다리기만 할 순 없는 노릇이고, 또 다른 원인에 대한 가능성도 있기 때문에 다방면의 시도를 해보았습니다.

**결과는 앞서 올린 사진처럼 모두 반려되었습니다.**

![16-validate_10](/images/portal/post/2020-09-11-Zum-Chrome-Extension/16-validate_09.png){:style="border:1px solid #666;padding:0;margin:0;"}

어쨌든 많은 우여곡절 끝에 마지막 베타버전을 배포할 수 있었습니다.

***

### 🚩 정리

앞서 언급한 검수과정의 핵심내용에 대한 요약입니다.

1. **API는 `SSL` 인증이 된 것(`https`)만 사용 가능합니다.**
  - 가능하면 확장프로그램 내에 연결된 모든 사이트가 `SSL`인증을 받은 상태면 더 좋습니다.
2. **`jsonp`를 사용해도 됩니다.**
  - 단, `Content Security Policy`를 명확하게 작성해야 합니다.
3. **다른 사이트의 파비콘이 필요한 경우 `chrome://favicon`을 사용하면 됩니다.**
4. **`manifest.json`에 명시한 `Chrome API`는 무조건 사용해야 합니다.**
  - 명시해놓고 사용하지 않으면 반려
  - 명시하지 않았는데 사용해도 반려
    - `if` 조건으로 언급하는 것도 반려
5. **대시보드에 `개인정보 처리방침` 링크를 올려야합니다.**
  - 정말 대충 작성해도 상관 없으니까 올려놓기만 하면 됩니다!
  - 예시: https://www.better-image-description.com/chromeprivacy.html
  - 간단한 확장프로그램의 경우는 필요없습니다.
6. **리소스를 `base64`로 사용하면 반려됩니다.**
7. **쿠키 사용은 자제할 수록 좋습니다.**
  - 사용하더라도 권한에 명시하면 됩니다. (확실하진 않습니다.)
  - 그래도 사용하지 않는게 제일 좋습니다. (안전하게!)
8. **사용자에게 무언가 입력을 받은 후 다른 사이트에 넘기는 경우(검색, 로그인 등) 무조건 해당 사이트는 무조건 SSL(https) 인증을 받아야합니다.**
  - 즉, **사용자 정보(입력정보)에 대한 암호화**가 되어있어야 합니다.
  - `https`로 인증하기 힘들다면 `proxy` 혹은 `redirect`를 통해서 우회해도 상관없습니다.
9. **`manifest.json`에 명시한 권한이 많을 수록 검수가 오래 걸립니다.**
10. 검수는 **빠르면 1일, 길면 4일** 정도 소요됩니다.
11. **검수 요청을 올릴 때 `manifest.json`에 명시한 `version`은 항상 달라야 합니다.**
  - 똑같은 `version`에 대한 검수가 진행되었을 경우 바로 반려될 수 있습니다.

***

## 7. 앞으로의 계획

최근에 사내테스트를 진행했습니다.

![17-test](/images/portal/post/2020-09-11-Zum-Chrome-Extension/17-test.png){:style="border:1px solid #666;padding:0;margin:0;"}

일단 내부적으로 긍정적인 반응이 많은 상태입니다.
그래서 조금 더 다듬고 완성도를 높여서 고객에게 선보일 예정입니다.

개인적으로 서비스를 만들 때 마음속, 머릿속에 새겨두는 말이 있습니다.

> “서비스는 런칭 이후가 진짜 시작이다.”

서비스를 운영하는 기업의 입장에서 서비스를 만들기까지보단,
**만든 후에 운영하는 것부터가 진짜 시작**이라고 생각합니다.

그래서 이렇게 확장프로그램을 만들긴 했으나, **아직 시작도 못한 것이라고 생각합니다.**

앞으로를 더 기대해주세요!

긴 글 읽어주셔서 정말 감사합니다!

***

![emoticon_05](/images/portal/post/2020-09-11-Zum-Chrome-Extension/emoticon_05.png)