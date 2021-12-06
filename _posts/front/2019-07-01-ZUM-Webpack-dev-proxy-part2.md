---

layout: post

title: Webpack dev server를 이용한 개발 환경 구성 Part2

description: 백엔드 프록시 개발 모드 구현과 그 설명

image: /images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/webpack-spring.png

introduction: 모바일 줌 개편을 진행하며 구성했던 개발 모드에 관한 경험을 공유합니다

category: portal/tech

tag: [experience, Frontend, Vue.js, Webpack4]

---

> Part1에서는 JS파일을 이용한 프론트엔드 단독 개발 모드 publish 모드에 대해 설명드렸고, 
> Part2에서는 [리버스 프록시](https://ko.wikipedia.org/wiki/%EB%A6%AC%EB%B2%84%EC%8A%A4_%ED%94%84%EB%A1%9D%EC%8B%9C)를 활용하여 백엔드와 연동하는 dev 모드에 대해 설명드립니다.  
> 이번 예제도 Webpack4, Vue-CLI2, Axios를 이용합니다.


## 다시 들어가며...
Part1에서 설명드린 publish 모드는 개발 편의성을 위한 설정에 가까웠습니다.
이미 많은 개발자들이 하고 있었던 방식일 것이구요.  
Part2에서는 조금 색다른 내용을 소개합니다. 
일반적인 백엔드 개발 환경과 마찬가지로 페이지를 이동하고 API를 호출할 수 있지만,
Webpack Hot Reload 또는 [Hot Module Replacement](https://webpack.js.org/concepts/hot-module-replacement/)를 적용하여 수정 사항이 바로 적용하는 개발 모드입니다.


## 'dev 모드'가 필요한 이유
이제 많은 사이트가 SPA로 만들어지고 있습니다. 한 도메인당 하나의 웹앱이라고 볼 수 있을 정도입니다.
하지만 아직 사이트 전체를 SPA로 만들기는 어려움이 따릅니다. 
Netflix의 [SPA를 사용하지 않아](https://medium.com/dev-channel/a-netflix-web-performance-case-study-c0bcde26a9d9)
퍼포먼스를 향상시켰다는 글은 프론트엔드 진영에 큰 파장을 불러일으켰지만 확실히 일리있는 말이었습니다.

![음..](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/burn.jpg)
*음...*

Vue.js가 장점으로 내세우기도 하는 SPA의 좋은 활용법 중 하나는 페이지의 일부 영역만, 혹은 일부 페이지만
SPA로 구성하는 방법입니다. 로그인 페이지나 이용 약관 페이지 같은 완전히 *정적인 페이지*는 고전적인 서버 템플릿 방식을 채용하고
*동적인 조작이 많은* 페이지만 SPA로 구성하면 장점을 모두 흡수할 수 있습니다.  
이 아이디어 자체는 꽤 괜찮아 보입니다. 하지만 개발 환경에서 문제가 생깁니다.
Vue-CLI를 이용해(혹은 다른 프레임워크의 project init) 프로젝트를 만들게 되면 
SPA를 위한, SPA에 의한 프로젝트가 되어버린다는 것입니다.
다시 말해 전통적인 멀티 페이지 형식 개발이 아니라 `<div id="app"></div>` 이 포함된 *index.html*만 사용하는 싱글 페이지 형식이라는 것이죠.

> 물론 다른 html 파일을 사용하지 못하는 것은 아닙니다.
[HtmlWebpackPlugin을 이용하여 html 파일을 등록](https://www.youtube.com/watch?v=y_RFOaSDL8I)하면 `/파일명.html`으로 접속할 수 있습니다.
하지만 서버 사이드 템플릿 엔진을 사용하는 것이 아닌 단순 html 파일이고, 
세부적인 컨트롤러 설정이나 세션 설정등이 불가능하여 로그인 테스트나 form 테스트를 할 수 없습니다.

아래에서 설명드릴 몇 가지 설정을 적용하면 모든 요청을 백엔드 서버로 bypass하되 
지정해놓은 URL에만 웹팩이 번들링한 JS를 삽입하여 SPA와 서버 템플릿이 혼합된 웹 어플리케이션 개발 환경을 구축할 수 있습니다.
또한 배포된 서비스 환경과 유사한 형태를 가지기 때문에 CORS 설정이 필요없게 됩니다.

## 4-2. 'dev 모드' 구성
dev모드는 Webpack Dev Server의 [proxy 설정](https://webpack.js.org/configuration/dev-server/#devserverproxy)을 활용합니다.   
요청이 들어오면 요청 그대로 백엔드에 전달하고, *요청한 URL이 스크립트를 삽입할 URL이라면* 스크립트 삽입 태그를 붙이는 방식입니다.

> **스크립트 삽입 태그를 템플릿에 직접 작성하지 않는 이유는 다음과 같습니다.**  
> 1. Webpack entry point를 변경하는 경우 템플릿에 미리 작성한 JS 삽입 코드를 변경해야 합니다.
> 2. 실제 서비스 환경으로 배포시 번들링된 JS파일을 Chunk로 나누거나 Chunk Hash 값이 추가된 경우
> 사용할 템플릿 파일을 수정해야 합니다.
>  
> 물론 상황에 따라 직접 삽입하는 것이 더 나을 수도 있습니다.

### 목표
dev 모드는 크게 세 가지 기능 지원을 목표로 합니다.

- 모든 요청을 백엔드로 bypass
- 백엔드에서 설정한 컨트롤러 매핑 및 리소스를 그대로 응답
- 특정 URL은 Webpack이 동적으로 번들링하는 JS 삽입 및 Hot Reload 지원

그림으로 보면 아래와 같습니다.

![dev-spa](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/dev_spa.png)
*SPA를 지원하는 URL로 요청한 경우.  템플릿 엔진에서 만들어진 HTML에 스크립트 태그를 삽입한다.*

![dev-other](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/dev_other.png)
*그 외 요청.  백엔드에서 온 응답 그대로 반환한다.*


#### 1. proxy.js
먼저 Webpack Dev Server에서 사용할 proxy 처리 함수를 작성합니다.  
이 함수는 프로젝트 특성에 따라 크게 달라지므로 이러한 흐름이다라는 식으로 이해해 주시면 감사하겠습니다.
또, Webpack Dev Server 설정이 있는 **webpack.dev.conf** 파일에 작성해도 상관없습니다.

{% highlight javascript %}
/* proxy.js */
// 백엔드와 연결을 위한 리버스 프록시 설정

const config = require('../env'); // 환경설정 파일

module.exports = function (entry) {
  return { 
    '/**': { // 모든 요청을 백엔드로 bypass 
      target: {
        host: config.dev.proxyHost,           // 백엔드 호스트 'localhost'
        protocol: config.dev.proxyProtocol, // 백엔드 프로토콜 'http'
        port: config.dev.proxyPort,          // 백엔드 포트 '8080'
      },
      onProxyRes: proxyProcessing(config.dev.assetsPublicPath, entry) // HTML 구분 및 스크립트 처리 로직. 후술
    },
    ignorePath: false,
    changeOrigin: true,
    secure: false
  }
};
{% endhighlight %}
Webpack Dev Server [옵션 중 Proxy](https://webpack.js.org/configuration/dev-server/#devserverproxy)에 설정할 내용을 리턴하는 함수를 작성합니다.  
이 함수는 모든 요청`/**`을 백엔드로 bypass하게 설정하는 함수입니다. 
  
onProxyRes 프로퍼티는 리버스 프록시 서버가 요청하고 **받은 응답을 처리**하는 구문입니다.
특히 proxyProcessing 함수에 전달하는 **assetsPublicPath**를 주의하셔야 합니다. 
Webpack Dev Server가 생성하여 메모리에 올려두는 JS 파일도 public path에 따라 URL이 변하기 때문입니다. 

위 코드에서 사용한 proxyProcessing 함수의 세부 구현은 아래와 같습니다.

{% highlight javascript %}
/* proxy.js 계속 */

/**
 * 백엔드로부터 받은 응답이 HTML이면 스크립트를 삽입하는 함수.
 *
 * @param publicPath Webpack config의 publicPath. 이 주소가 static 요소의 baseURL로 사용된다 
 * @param entry Webpack config의 entry 객체
 * @returns {Function} 프록시 처리 함수
 */
function proxyProcessing(publicPath, entry) {
  // 파라미터로 입력받은 publicPath와 entry 정보로 js script 삽입 코드를 생성하는 함수. 후술
  const script = entryToScript(publicPath, entry); 

  return function (proxyRes, request, response) {
    if (request.originalUrl === '/'   // <== 스크립트를 삽입할 페이지의 URL. 
                                        // 이 구문을 생략하면 모든 페이지에 스크립트 삽입됨
        && proxyRes.headers
        && proxyRes.headers['content-type']
        && proxyRes.headers['content-type'].match('text/html')) { // content type이 HTML인지 체크

      const _write = response.write;

      response.write = function (data) {
        if (data && data.toString) {
          // HTML 문자열 마지막에 스크립트 태그를 끼워넣는 함수. 후술
          return _write.apply(response, [appendScriptToHtml(data.toString(), script)]);  
          
        } else {
          return _write.apply(response, arguments);
          
        }
      };

    }
  }
}
{% endhighlight %}
proxyProcessing 함수는 백엔드 서버로 요청된 응답을 처리하는 함수입니다. 
요청 URL이 스크립트를 삽입할 URL인지 확인한 후, 응답이 HTML이면 스크립트 태그`<script src="...">`를 끼워넣습니다.

위 코드에서 사용된 entryToScript 함수와 appendScriptToHtml 함수는 간단합니다.
{% highlight javascript %}
/* proxy.js 계속 */

/**
 * Webpack Entry Point를 스크립트 태그로 리턴하는 함수
 * 
 * @param publicPath Webpack Config의 public path인 js파일 폴더 경로
 * @param entry {Array|Object|String} js파일이 될 엔트리 포인트 설정
 * @returns {string} 스크립트 삽입 태그
 */
function entryToScript(publicPath, entry) {
  let files;
  
  // Webpack Entry Point는 배열, 객체, 문자를 지원하므로 분기 처리
  if (entry instanceof Array) { 
    files = entry.map(str => str.split('/'))
                 .map(arr => arr[arr.length - 1]);
        
  } else if (entry instanceof Object) {
    files = Object.keys(entry).map(key => key + '.js');
    
  } else {
    files = [entry];
    
  }

  // public path와 파일명을 합쳐 스크립트 삽입 태그로 변경
  return files.map(name => `<script src="${publicPath}${name}"></script>`)
              .join('');
}
{% endhighlight %}
입력받은 Webpack Entry Point 목록을 스크립트 삽입 태그로 변경하는 함수입니다.
단순 문자열 치환 로직입니다.
 

{% highlight javascript %}
/* proxy.js 계속 */

/**
 * HTML 파일 마지막 라인에 스크립트 태그를 추가하는 함수
 * 
 * 만약 템플릿에서 직접 스크립트 태그를 삽입한다면 이 부분은 생략할 것.
 *
 * @param html 스크립트 삽입 코드를 끼워넣을 HTML 문자열
 * @param script 끼워넣을 스크립트 태그 (<script src="...">)
 * @returns {string} 스크립트 태그가 끼워넣어진 HTML 문자열
 */
function appendScriptToHtml(html, script) {
  if (html.includes('</html>')) {
    html = html.replace('</html>', script + '</html>');
  }
  return html;
}
{% endhighlight %}
이 함수 역시 단순 문자열 치환 로직으로, `</html>` 태그가 있으면 그 앞에 스크립트 삽입 태그를 넣는 함수입니다.

> 사실 이 함수는 [HtmlWebpackPlugin에서 하는 일 중 하나](https://github.com/jantimon/html-webpack-plugin/blob/master/index.js#L846)입니다.  
HtmlWebpackPlugin 플러그인에서는 정규식을 통해 분류하고 삽입하지만, 이 코드는 플러그인과 달리 사용하는 상황을 한정했기 때문에
위와 같이 간단한 로직으로도 비슷한 효과를 볼 수 있습니다.

프록시 설정이 끝났습니다.  
다시 정리해보자면 모든 요청`/**`을 백엔드 서버로 bypass한 후,
응답에 따라 스크립트를 삽입하거나 응답 그대로 반환하는 로직이었습니다.


### 2. Webpack Config
이제 마지막으로 Webpack Config 파일을 수정해야 합니다.

{% highlight javascript %}
/* webpack.dev.conf.js */
// 웹팩 dev모드 설정

const baseWebpackConfig = require('./webpack.base.conf');
const proxy = require('./proxy'); // 위에서 작성한 proxy.js 파일의 함수

devServer: {
    // 생략
    proxy: proxy(baseWebpackConfig.entry), // 작성한 프록시 함수 적용. 
                                             // 파라미터로 Webpack 번들링시 사용할 엔트리 포인트 리스트를 전달.
  },
  
optimization: {
  splitCHunks: false // proxy.js에서 청크 삽입을 고려하지 않기 때문에 false
}
  
plugins: [
    // 생략
    // new MiniCssExtractPlugin({ ... }) <= js 파일에 스타일 포함시키기 위해 플러그인 제거
    // new HtmlWebpackPlugin({ ... }) <= html 파일을 사용하지 않기 때문에 제거 
],  
{% endhighlight %}
[HtmlWebpackPlugin](https://webpack.js.org/plugins/html-webpack-plugin/)을 꼭 제거하셔야 합니다. 
앞서 *dev모드가 필요한 이유*에서 말씀드린대로 이 플러그인에 html 파일을 추가하면
Webpack Dev Server에 `/index.html`과 같은 URL로 접속할 수 있게 됩니다.
특히 index.html이라면 `/`로 접속되는데, dev 모드에서는 모든 응답을 백엔드 서버로 bypass할 것이므로
HTML 파일을 응답하지 않게 플러그인을 제거해야 합니다.

백엔드와 연동되는 개발 환경인 dev 모드를 위한 모든 설정이 끝났습니다.  
이제 dev 스크립트를 실행하면 모든 요청은 위에서 설정한 백엔드, 
http://localhost:8080로 bypass됩니다. 그리고 요청 URL이 `/`인 경우 </html> 태그 전에 스크립트 삽입 태그를 끼워넣습니다.  
결과적으로 번들링된 js 파일에서 소켓을 열어 웹팩 HMR 기능을 활용하면서 
백엔드 테스트까지 가능한 상태가 되었습니다.


### 3. 테스트

![프록시 응답](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/reverse-proxy.png)
*http://localhost:3000 요청 결과*

Webpack Dev Server인 3000포트로 요청한 응답입니다.  
`</html>` 태그 이전 스크립트 삽입 태그가 포함된 것을 볼 수 있습니다.
또, 템플릿 엔진으로 만들어진 문자열인 'hello'도 확인할 수 있습니다.

![백엔드 직접 요청](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/no-proxy.png)
*http://localhost:8080 요청 결과*

백엔드 서버인 8080포트로 직접 요청한 응답입니다.  
프록시 로직이 없으므로 템플릿 엔진에서 작성한 그대로 응답합니다.

![굿2](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/good2.jpg)
*물론 페이지 이동이나 form 관련 리다이렉트도 잘 작동합니다*




### 4. 번외: 템플릿 파일과 build
웹팩의 장점 중 하나는 [코드 스플릿(Chunk)](https://webpack.js.org/guides/code-splitting/)과 
[Chunk Hash](https://webpack.js.org/configuration/output/#outputhashfunction)가 아주 간단하게 지원된다는 것입니다.
하지만 이 설정은 Webpack이 기본적으로 지원하는 형태인 *index.html*에 css/js를 삽입하고, 배포 시에는 /dist 폴더 내에 생성된 *index.html*을 사용할 때
간단한 것 뿐입니다. 이 글에서 설명드린 dev 모드에서는 난감합니다. 
특유의 문법을 사용하는 템플릿 파일은 정적인 HTML 파일이 아니기 때문이죠.

하지만 생각보다 간단하게 해결할 수 있습니다.  
Webpack 프로젝트 기본 룰과 마찬가지로 css/js 태그가 없는 템플릿 파일*(ex: _index.peb)*을 만들어 놓고, 
번들링할 때 그 템플릿 파일을 로드, 웹팩이 생성한 css/js를 삽입한 템플릿 파일*(ex: index.peb)*을 생성하게 하는 것입니다.  

![생성되는 템플릿](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/generate_template.png)
*위 그림과 같은 순서를 따릅니다*

이 방법을 적용하려면 HtmlWebpackPlugin이 지원하는 String interpolation과 관련된 문제가 조금 있지만 꽤나 훌륭하게 작동합니다.
> 플러그인 작동 방식과 관련되어
> <...>처럼 HTML과 유사한 문법, Webpack Plugin 관련 문법 사용시 번들링 에러가 발생합니다.

{% highlight javascript %}
/* webpack.prod.conf.js */
// 번들링 스크립트인 `build` 사용시 사용되는 웹팩 설정.
// 
// pebble 템플릿 파일을 이용하는 예제

plugins: [
    // 번들링된 스크립트/스타일이 삽입된 HTML 파일을 생성
    new HtmlWebpackPlugin({
      template: '../../../resources/templates/_index.peb', // css/js 태그가 없는 원본 템플릿 파일
      filename: '../../../resources/templates/index.peb',  // 태그가 삽입된 배포용 템플릿 파일
      inject: true // 태그 inejct
    })
    
  /* 그 외 플러그인 생략 */
]
{% endhighlight %}

위 코드와 같이 플러그인 옵션의 **template** 에는 css/js 삽입 태그가 없는 원본 템플릿의 주소를 넣고,
**filename**에는 배포 시 사용할 템플릿 파일의 주소를 넣으면 됩니다.  
백엔드 컨트롤러 부분에 profile에 따라 dev모드로 개발할 때와 배포 후 사용할 템플릿을 구분하는 로직이 포함되어야 하지만
직접 스크립트 삽입 태그를 넣는 것에 비하면 훨씬 간편해집니다. 프론트엔드 빌드만으로 백엔드에서는 더 이상 **보여지는** 것에 신경 쓸 필요가 없으니까요. 


## 마치며
Part1에서 말씀드렸듯 저는 **보여지는** 것은 프론트엔드로, **보여질 데이터에 관한** 것은 백엔드로 구분해 작업하고자 했고,
그 첫걸음으로 위와 같이 개발 모드를 구분하여 개발했습니다.  
  
개발 중에는 작업의 분류나 모드별 관리가 귀찮았지만(특히 publish 모드) 개발이 끝난 후 유지보수 중에 더 큰 힘을 발휘하고 있습니다. 
하려는 작업에 따라 명확하게 개발 모드를 분리하여 실행하고 개발을 진행할 수 있기 때문입니다.
또, 프론트엔드 개발과 백엔드 개발이 서로에게 영향을 주지 않기 때문에 동시에 개발할 수 있다는 점도
굉장한 장점입니다. 
  
많은 내용과 코드를 담게 되었지만 이게 끝은 아닙니다. 
더 많고 세세한 빌드 설정과 서버 템플릿 데이터를 프론트엔드에서 사용하기 위해 몇가지 룰도 정해야 하는 등 남은 작업이 많습니다. 
특히 publish 모드는 정해진 JS 파일만을 사용하게 구성했으니 주기적으로 JS 파일 갱신을 위한 작업이 필요합니다.

하지만
![끝](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part2/end.jpeg)

