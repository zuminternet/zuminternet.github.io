---

layout: post

title: Webpack Dev Server를 이용한 개발 환경 구성 Part1

description: 프론트엔드 단독 개발 모드 구현과 그 설명

image: /images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/webpack-js.png

introduction: 모바일 줌 개편을 진행하며 구성했던 개발 모드 구성에 관한 경험을 공유합니다

category: portal/tech

tag: [experience, Frontend, Vue.js, Webpack4]

---

> Part1에서는 프론트엔드 단독 개발 모드를 구성하는 방법을,  
> Part2에서는 백엔드 연동 개발 모드를 구성한 방법에 대해 공유합니다.    
> - 설명드릴 예제 코드는 [Webpack4](https://webpack.js.org/), [Axios](https://github.com/axios/axios)를 이용합니다.


## 목차
1. 들어가기 전에
2. 도입 배경
3. NPM 스크립트 소개
4. 각 모드별 구성 방법  
4-1. publish 모드  
4-2. dev 모드
5. 정리
6. 마치며

1~4까지는 Part 1, 5~7은 Part2로 나누어 설명을 진행하겠습니다.
  
  
## 1. 들어가기 전에
최근 [Github 트렌드 Javascript](https://github.com/trending/javascript?since=monthly)를 보면 번들링 툴은 [Webpack](https://github.com/webpack/webpack)이 압도적인 자리를 차지합니다.
많은 프레임워크와 라이브러리가 이미 Webpack을 기반으로 하고 있고, 계속된 업데이트로 기능을 더해나가고 있기 때문일 것입니다.

![Webpack](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/webpack.png)
*웹팩은 언제까지 갈런지?*

줌인터넷에서도 Webpack을 기반으로 프론트엔드 개발을 진행합니다.
특히 2018년 하반기에 [Vue.js](https://vuejs.org/)를 기반으로 진행한 모바일 줌 개편에는 Webpack의 많은 기능들을 활용하였는데
그 중 [Webpack Dev Server](https://webpack.js.org/configuration/dev-server/)를 활용하여 프론트엔드 개발 모드를 분리 구성함으로써
효과적으로, 더 빠르고 편리하게 개발한 경험을 공유하고자 합니다.
  
  
## 2. 도입 배경
당시 모바일 줌 개발에 들어가기 전 몇가지 고려할 사항이 있었습니다.

1. **JS 파일 및 자바 백엔드는 하나의 웹 어플리케이션 서버로 배포**  
  프론트엔드 프레임워크가 자리잡은 이후, HTML,CSS,JS 등 static 요소와 비즈니스 로직을 포함하는
  API 서버를 분리하여 배포하고 운영하는 사이트들이 생겼습니다. 하지만 이번 프로젝트는
  기존 방식대로 하나의 웹 어플리케이션으로 배포하기로 결정되었습니다.
2. **빠른 개발 및 협업을 위해 프론트엔드와 백엔드 분리 개발**  
  릴리즈 날짜는 정해져 있었지만 기획 및 디자인이 수정되면서 개발 기간은 점점 짧아지기 시작했습니다.
  이전 개발 프로세스 그대로 기획-디자인-퍼블리싱-개발 순으로 진행하기에는 부담되는 개발 일정이었습니다.
3. **템플릿 엔진 사용**  
   앞서 말씀드린대로 하나의 웹 어플리케이션으로 배포하게 된 이유 중 하나는 템플릿 엔진 사용을 위해서였습니다.
   모든 정보를 AJAX로 가져오는 것도 좋지만 몇 가지 개선을 위해 템플릿 엔진을 활용하게 되었습니다. 
   문제는 프론트엔드 개발 환경에서 백엔드 템플릿 엔진으로 만들어 낸 템플릿 파일을 사용할 수 없다는 점이었습니다.
4. **stub 데이터는 제공받을 수 있지만 API 개발까지는 시간이 필요**  
   기획 및 개발 일정이 계속 변경되면서 각 서브 도메인의 API 개발이 언제 마무리될지 알 수 없게 되었습니다.
   일단 데이터 규격을 맞추는 것으로 급한 불은 껐지만, API로 직접 개발이 가능해질때까지 기다릴 수는 없었습니다.
   
![time](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/what.jpg)
*갈 길이 멀다...*

이렇게 한정된 리소스와 개발 기간을 해결하기 위해 **stub 데이터만을 이용하는 프론트엔드 개발** 모드와 
**백엔드 데이터를 연동하는 프론트엔드 개발** 모드로 분리할 필요가 있었습니다.  
말 그대로 **눈에 보이는 부분**의 개발과 **데이터를 다루는 부분**의 개발을 분리하여 동시에 진행하고자 한 것입니다.


![목표 개발 프로세스](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/goal.png)
*결과적으로 위 그림과 같은 프로세스로 개발을 진행할 수 있었습니다*  
  
  
  
## 3. NPM 스크립트 소개

먼저 package.json 파일에 정의한 스크립트를 소개합니다.

{% highlight javascript %}
{
  /* package.json */
  // config 폴더 안에 있는 webpack.[dev-pub].conf.js 파일에 각 모드에 관한 상세 설정을 작성했다
  
  "scripts": {
      "publish": "cross-env webpack-dev-server --inline --progress --config config/webpack.pub.conf.js",
      "dev": "cross-env webpack-dev-server --inline --progress --config config/webpack.dev.conf.js",
      // ... 이하 생략
    }
}
{% endhighlight %}

|NPM 스크립트|설명|
|---|---|
|publish|백엔드 프로젝트가 불필요한 단독 실행 모드. stub 데이터를 사용|
|dev|백엔드 서버에 리버스 프록시로 접속하는 실행 모드|

package.json 파일은 Vue-CLI2가 만들어 주는 형태와 크게 다르지 않습니다. 
다만 실행가능한 스크립트를 한 줄 추가했습니다.

앞서 말씀드린 대로 *stub 데이터를 활용한 프론트엔드 단독 실행 모드*는 publish 라고 정했고,
리버스 프록시를 이용하여 *백엔드 서버를 이용하는 모드*는 dev 모드라 정하고 구성했습니다.  
이제부터는 두가지 스크립트를 publish / dev 모드라고 설명하겠습니다.

각 모드의 특징은 아래와 같습니다.
1. **publish**    
![publish 모드](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/publish.png)
  - 프론트엔드 단독 실행 모드. 백엔드 불필요.
  - `/api/...` 경로로 AJAX 호출시 `/stub` 폴더 내의 JS 파일(JSON 데이터)을 응답
  - API 추가시 경로에 해당하는 폴더에 JS 파일을 추가하여 적용
  - JS 파일 수정으로 글자 수 변경, 이미지 링크 깨짐, 데이터 형식 등 다양한 UI 테스트/개발 진행
  
2. **dev**  
![dev 모드](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/dev.png)
  - 프론트엔드와 백엔드 연동 모드.  
  하나의 웹앱으로 빌드하고 배포한 상태와 유사함. 
  - 모든 요청이 백엔드로 bypass
  - 페이지 접속시 백엔드에서 템플릿 엔진으로 생성한 HTML 반환
  - Webpack Hot Reload: Chunk 및 Hash와 상관 없이 항상 [Webpack Hot Reload](https://webpack.js.org/concepts/hot-module-replacement/) 지원
  - CORS 설정 없이 `/api/...` URL로 백엔드 API를 호출 가능

publish 모드는 **AJAX 요청시 JS 파일이 응답**되니 파일 수정으로 데이터의 구조를 바꾸거나
예외 상황을 만들어 테스트할 수 있고, 새로운 API가 필요할 때에도 파일 추가만으로 동작합니다.  
dev 모드는 **모든 요청이 백엔드로 bypass** 되므로 
외부 API와 연동, 비즈니스 로직 개발 등 백엔드 API 개발과 프론트엔드에서의 AJAX 요청 개발에 집중할 수 있는 환경으로 구성되었습니다. 
  
  
## 4. 각 모드별 구성
개발 모드를 분리 구성하기 위해 webpack 설정 파일을 추가했습니다.  
먼저 publish, dev, build 공통적으로 사용되는 옵션을 정의한 **webpack.base.conf.js** 파일과  
각 개발 모드별로 **webpack.[dev/publish].conf.js**, 빌드 시 사용하는
**webpack.prod.conf.js** 파일입니다.  
이 파일들 역시 [Vue-CLI2](https://cli.vuejs.org/)가 생성한 파일과 크게 다르지 않으므로 주요 코드만 설명합니다.

>Vue CLI3로도 가능하지만 설정할 것이 조금 더 많아집니다.  
  
  
## 4-1. publish 모드 구성

### 목표
publish 모드는 크게 세 가지 기능 구현을 목표로 합니다.

- 백엔드 API 서버와 전혀 무관하게 프론트 어플리케이션 실행 가능
- Axios를 이용해 AJAX 호출시 stub 폴더 내에 있는 JS 파일(JSON 데이터)을 읽어오도록 구성
- GET / POST와 같은 요청 메소드 구분 작동 가능

구현을 위해 아래와 같은 순서로 작업합니다.

#### 1. 환경 변수 선언 (webpack.DefinePlugin)

먼저 모드별 분기 처리를 위해 webpack.DefinePlugin을 이용하여 환경 변수를 설정합니다.   
아래 구문을 통해 현재 실행 모드를 전역 변수로 등록하여 코드 내에서 구분할 수 있게 됩니다.

{% highlight javascript %}
  /* webpack.pub.conf.js */
  // publish 모드에서 사용할 변수와 플러그인 설정

  plugins: [
    new webpack.DefinePlugin({ // 현재 실행 환경을 글로벌 변수로 선언
      'process.env': JSON.stringify('publish')
    }),
    
    // 그 외 생략
  ]
{% endhighlight %}

여기서 선언한 process.env 를 통해 현재 실행 스크립트를 구분함으로써 특정 로직을 수행할 수 있습니다.  
>위 구문에 대한 자세한 설명은 [Webpack DefinePlugin 플러그인 페이지](https://webpack.js.org/plugins/define-plugin/)를 참조하시기 바랍니다.

#### 2. Axios 인스턴스 baseURL 설정 또는 요청 URL 몽키패칭

publish 모드에서는 Axios를 이용한 AJAX 호출시 URL 앞에 /stub를 붙이도록 설정합니다.  
**ex) /api/example -> /stub/api/example**  
`html` `image`와 같은 요소는 webpack dev server의 기본 옵션 그대로 응답하면서 백엔드 API 호출만
따로 관리하기 위해서입니다.  

Axios 인스턴스를 생성하여 사용하는 경우에는 생성자의 [baseURL 옵션](https://github.com/axios/axios#creating-an-instance) 등으로 지정할 수 있고, 
인스턴스를 생성하지 않는다면 Axios를 몽키패칭하거나 [defaults.*](https://github.com/axios/axios#config-defaults) 값을 설정하는 방법이 있습니다. 

>이 글에서는 예시 코드를 줄이기 위해 몽키패칭하는 방법만 소개하겠습니다. 

##### Axios 객체 몽키패칭

위험성이 있지만 개발 환경에만 적용할 예정이고, 모든 요청을 마음대로 컨트롤할 수 있어 선호합니다.  

{% highlight javascript %}
/* _core/axios.js */

if (process.env.NODE_ENV === 'publish') { // publish 모드에서만 패칭

  ['request', 'get',
    'delete', 'head', 'options',
    'post', 'put', 'patch'].forEach(method => {

    const _method = Axios[method];
    Axios[method] = function (url, ...args) {
      let parsedUrl = url + '.js'; 
      if (parsedUrl.charAt(0) !== '/') {
        parsedUrl = '/' + parsedUrl; 
      }

      return _method(`/stub${parsedUrl}`, ...args);
    };

  });
}
{% endhighlight %}
요청 URL 앞에는 **/stub**, 뒤에는 **.js**를 붙이는 로직입니다.  
만약 다른 도메인으로 요청하는 경우도 있다면 추가 로직이 필요합니다.  
위 파일을 적당한 곳에 import하면 Axios의 request method들이 작성한 로직을 수행하게 됩니다.


#### 3. stub 폴더 및 파일 생성

이제 프론트엔드 개발중 사용하게 될 stub 데이터를 작성합니다.
루트 폴더 내에 stub 폴더를 만들고 stub 데이터를 export하는 JS 파일을 추가합니다.


{% highlight javascript %}
/* /stub/api/example.js */

const userList = []; // 데이터를 저장할 배열

module.exports = {
  get(req) { // get 요청
    return userList;
  },
  
  post(req) { // post 요청
    const {id, name} = req.body; // id와 name 획득
                                 // 이 구문은 아래에서 선언할 express의 json 파싱 미들 웨어가 필요

    const user = {id: id, name: name}; // 유저 정보 추가
    userList.push(user);
    
    return userList;
  }
};
{% endhighlight %}

export할 객체에는 Http 요청 Method에 해당하는 함수를 구현합니다. 
눈치채셨겠지만 Webpack Dev Server로 요청이 왔을 때 
요청 URL과 일치하는 JS 파일을 찾아 import하고, 객체의 메소드를 실행하여 결과를 반환합니다. 
간단하지만 아주 강력한 코드죠. 

![파일 로드 방식](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/file-load.png)

이제 Webpack Dev Server에서 사용할 응답 데이터 파일이 준비되었습니다.



#### 4. Webpack Dev Server의 before 훅 로직 추가
    
{% highlight javascript %}
/* webpack.pub.conf.js */
// publish 모드에서 사용하는 Webpack Dev Server에 stub 데이터 파일을 연결합니다

devServer: {
    // 생략
    before: function (app) {
          app.use(require('express').json()); // POST 요청 body 파싱 미들웨어 등록
          const root = path.join(__dirname, '..');
    
          /**
           * /stub으로 요청된 데이터 처리
           */
          app.all('/stub/**', (req, res) => {
            const data = require(`${root}${req.path}`);
            res.send(data[method](req));
          });
    
        }
  }
{% endhighlight %}

Webpack Dev Server에서 지원하는 hook 중 [before 훅](https://webpack.js.org/configuration/dev-server/#devserverbefore)에서 요청 처리를 진행합니다.  
post 요청 처리를 위해 미들웨어를 등록하고 
Axios 패칭 구문에서 설정한대로 `/stub/**` URL로 온 요청의 path를 파일 위치로 변경한 후
JS 파일을 import 하고 실행하는 로직을 수행합니다.

![before hook 로직](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/req-res.png)
*post 요청이라면 b.post(request)가 호출됩니다*

이제 public 모드 설정이 끝났습니다.  
새로운 API가 추가될 때마다 */stub* 폴더 아래 경로에 JS 파일을 추가하면 되고,
API에서 query parameter 처리와 같이 request와 관련된 로직이 필요하면 
Node Express 문법 그대로 [request 객체에서 데이터를 획득](https://expressjs.com/ko/api.html)할 수 있습니다.  
결과적으로 **백엔드 프로젝트와 관계 없이 단독 실행**이 가능하며, **JS 파일을 변경하는 것**으로 다양한
데이터를 테스트 해볼 수 있는 환경을 구성한 것입니다.


#### 5. 테스트

post 요청을 통해 데이터를 삽입하고 get 요청으로 데이터를 조회하는 테스트입니다.

{% highlight javascript %}
/*** Step 1 ***/
await axios.get('/api/example')
           .then(response => {
             console.log('get');
             console.log(response.data);
           })
// get
// []


/*** Step 2 ***/
await axios.post('/api/example', {id: 100, name: 'jack'})
           .then(response => {
             console.log('post');
             console.log(response.data);
           });
// post
// [ {id: 100, name: 'jack'} ]


/*** Step 3 ***/
await axios.get('/api/example')
           .then(response => {
             console.log('get2');
             console.log(response.data);
           });
// get
// [ {id: 100, name: 'jack'} ]
{% endhighlight %}

의도대로 작동하는 것을 확인할 수 있습니다.



### 더해서...
JS 파일로 응답하는 publish 모드에 대해 설명드렸습니다.  
그리 특별한 내용은 아니니 전체적으로 정리한다는 느낌으로 읽어 주셨으면 좋을 것 같습니다.  

사실 publish 모드의 구성은 [grunt](https://gruntjs.com/)나 [rollup](https://github.com/rollup/rollup)과 같은 번들링 도구를 사용하면서 Node Express를 함께 실행하는 방식과
근본적으로 다르지 않습니다. 하지만 직접 Node 서버를 구성한다면 개발 환경에 어울리지 않는 의미없고 귀찮은 설정이 필요합니다. 
대표적으로 [CORS](https://developer.mozilla.org/ko/docs/Web/HTTP/Access_control_CORS) 설정과 [Nodemon](https://www.npmjs.com/package/nodemon) 설정이 있겠네요.

![굿](/images/front/post/2019-07-08-ZUM-Webpack-dev-proxy-part1/good.jpg)
*귀찮은건 질색*
  
이어질 Part2에서는 리버스 프록시 설정을 이용하여 모든 요청을 백엔드 서버로 bypass하면서도
Webpack의 Hot Reload 기능을 사용할 수 있는 **dev 모드 구성 방법**과 **배포를 위한 추가 설정**에 대해 설명하겠습니다.

