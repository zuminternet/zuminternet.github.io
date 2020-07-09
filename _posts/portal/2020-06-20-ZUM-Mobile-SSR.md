---

layout: post

title: 모바일 줌 SSR 적용과 그 성과 이야기

description: Vue.js 기반의 프로젝트를 Node.js 백엔드로 마이그레이션하고 SSR을 적용한 성과 이야기입니다

image: /images/portal/post/2020-06-20-ZUM-Mobile_SSR/title.png

introduction: 모바일 줌 프로젝트를 Node.js 및 SSR로 변경한 경험을 공유합니다

category: portal/tech

tag: [experience, Node.js, Frontend, Vue.js, SSR]

---
<br>
## 들어가며
정말 오래간만에 기술 블로그에 글을 작성하는 것 같습니다.  
이 글을 쓰기 약 3개월 전인 03월 26일 모바일 줌 프로젝트는 내부적으로 다시한번 큰 변화를 맞았습니다.  
EC2 인스턴스에 Spring Boot 백엔드에서 Docker 컨테이너, 백엔드는 Node.js. 그리고 SSR을 적용한 것입니다.

![아키텍쳐1](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/architecture.jpg)
*Spring Boot 어플리케이션에서 Node.js 어플리케이션으로 변경되었습니다*

이 글에 모든 내용을 다 담을 수는 없지만, 팀 내에 공유했던 자료와 완료 보고에 사용했던 자료들을 이용해
저희 팀이 어떤 선택을 했고 왜 그런 선택을 했는지, 또 어떤 성과를 보였는지 공유하고자 합니다.  

<br>
## Server Side Rendering?
모던 프론트엔드 프레임워크 이야기에서 빠질 수 없는 SSR은 Node.js 전환의 이유 중 하나이기도 합니다.  
실제로 SSR만을 위해 Node.js 어플리케이션으로 작성하는 경우도 있습니다. 
이번 작업은 단순히 SSR 때문에 Node.js 어플리케이션으로 변경한 것은 아니지만,
그만큼 비중이 있는 이야기이므로 SSR에 대해 조사하고 테스트했던 내용에 대해 먼저 풀어가고자 합니다.  
  
모바일 줌은 약 2년 전 Vue.js를 기반으로 한 SPA 프로젝트로 다시 개발되었습니다.  
많은 분들이 이미 알고 계시듯 SPA는 모듈화, 빠른 DOM 변경, 간편한 이벤트 핸들링 등 장점이 많은 반면, 
*JS 실행 후 DOM이 삽입된다는 점* 때문에 발생하는 제약사항과 단점도 있습니다. 
그리고 그 단점을 조금이나마 해소하고자 수행하는 것이 SSR입니다.

![SSR이란](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/what-is-ssr.png)
*SSR은 기존 템플리팅 방식(서버 템플리팅)과 크게 다르지 않습니다*

SSR을 수행할 수 있도록 만들어진 객체를 SSR Renderer라고 합니다.
SSR Renderer를 실행하여 페이지에 해당하는 HTML을 얻고, 그 HTML을 서버 템플릿에 삽입하는 것이죠.
이 일련의 과정을 SSR이라고 합니다. 

> Vue.js 는 [Vue SSR 렌더링 가이드](https://ssr.vuejs.org/#what-is-server-side-rendering-ssr)를 제공하고 있습니다.  
> 사이트에서 SSR에 대한 기본 개념과 하는 이유 등을 자세하게 확인하실 수 있습니다. 

### SSR은 왜?
모바일 줌닷컴에 SSR을 적용하려고 했던 이유는 크게 두가지입니다.

- 검색엔진 최적화(SEO)  
컨텐츠가 HTML에 삽입되어 있으면 검색엔진 노출에 더 유리합니다.
> SPA 사이트는 JavaScript가 실행되어야 DOM이 구성됩니다.
> 아직까지 일부 크롤러가 사용하는 headless 브라우저는 JS를 실행하지 않습니다.
> 그렇기 때문에 사이트의 데이터를 가져가지 못하고, 이는 검색엔진에 정상적으로 노출되지 못한다는 것을 뜻합니다.

- 성능이 좋지 않은 유저를 위한 최적화(혹은 [수화(Hydration)](https://ssr.vuejs.org/guide/hydration.html))  
HTML에 DOM이 작성되어 있으면 JS가 실행되고 DOM이 삽입되는 SPA에 비해 더 빠르게 보입니다.
> 사실 JS로 생성된 DOM을 그대로 이용하는 Hydration 기능의 효과는 미미합니다.  
> 이 글을 쓰는 2020년 6월은 이미 5G 통신을 하고 있고, 스마트폰은 2.5Ghz x 8 core가 보급형으로 판매되고 있는 시대니까요.  
> 다만 아주 오래된 스마트폰 혹은 브라우저를 사용하는 사용자에게는 크게 느껴질 수 있습니다.
> 간단하게 테스트를 해 본 결과 갤럭시 노트2(2012년 모델)에서 약 3초정도 빠르게 화면을 볼 수 있었습니다.
 

### SSR의 문제?
Vue.js 비롯해 대부분의 모던 SPA 프레임워크는 SSR을 지원합니다. 다만 지원만 합니다.  
예제 프로젝트는 많지만 *리얼 월드*에 적용할만한 예제가 없습니다. 
작업하며 겪었던 큰 문제와 제가 선택한 해결법은 아래와 같습니다.

- **브라우저 표준 객체/클래스(window, document 등)를 사용할 수 없음**  
    잘 작동하는 것처럼 보이는 예시 프로젝트의 함정은 **외부 라이브러리를 사용하지 않는다는 점**에 있습니다.  
    가이드에 따라 브라우저 표준 객체/클래스 사용 구문을 모두 if-else 구문으로 감싸는 것도 비현실적일뿐더러, 
    프로젝트에 사용하게 될 외부 라이브러리(ex. [Swiper.js](https://github.com/nolimits4web/swiper)) 는 브라우저 표준 객체를 참조하고 있습니다. 
    그렇기 때문에 극도로 정제된 코드가 아니라면 결국 브라우저 객체 참조 문제가 발생합니다.   
      
    지금 코드에서 문제가 없다고 하더라도, 유지보수하고 운영하면서 같은 문제에 맞딱뜨리지 않을 것이라고 장담할 수도 없습니다.
    담당자가 바뀌게 될 지도 모르고, 라이브러리를 추가할 수도 있기 때문이죠.  
    이는 현실적으로 ‘유지보수하는 서비스’에 사용이 어렵다는 것을 뜻합니다.  
    
    ![음...](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/aa.jpg)
    *음...*
    
    이 문제를 해결하기 위해 제가 선택한 해결 방법은 *테스트를 위해 만들어진* 가상 DOM 라이브러리 [JSDOM](https://github.com/jsdom/jsdom)을 사용하는 것입니다. 
    JSDOM은 자바스크립트만으로 만들어진 브라우저 객체를 제공합니다. 
    window, document, location 등 다양한 객체를 가지고 있고, 이벤트 핸들링이나 DOM 추가 삭제와 같은 기본적인 작업도 가능합니다.  
    
    ![JSDOM](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/jsdom.jpg)
    *정말 바보같지만 꽤나 괜찮은 해결 방법입니다*
        
    아래 코드는 JSDOM 8.5버전을 이용하여 Vue SSR Renderering를 수행하는 예제입니다. 
    
```ts
  declare const global; // Node.js global 객체

  // JSDOM 8.5 버전을 이용하여 브라우저 객체 생성 후 global 객체에 바인딩
  global.document = jsdom(``, {
    url: RenderingOption.projectDomain,
    userAgent: RenderingOption?.userAgent,
    cookieJar: RenderingOption.cookieJar
  });

  global.window = document.defaultView;
  global.location = window.location;
  global.navigator = window.navigator;

  // Vue SSR Renderer의 renderToString 메소드 실행
  // 렌더링 중에 global의 window 객체 사용함  
  const resultHtml = await renderer.renderToString(RenderingOption.rendererContext || {});

  // JSDOM close 이후 SSR 결과 반환
  global.window.close();

  return resultHtml;
```

*JSDOM 객체를 global에 바인딩하면 SSR Renderer는 브라우저 객체를 사용할 수 있게 됩니다.*

 
JSDOM을 적용하기 위해서도 우여곡절이 있었지만, 어쨌든 가장 큰 걸림돌이었던 **브라우저 객체 사용 문제**는 이렇게 해결이 되었습니다.

<br><br>

- **Vue SSR Renderer를 실행할 백엔드 및 운영 환경**  
    앞서 말씀드린대로 이번 작업 이전, 모바일 줌 프로젝트는 Spring Boot, 곧 JAVA 백엔드를 사용하고 있었습니다. 
    하지만 Vue.js의 SSR 렌더러는 [Node.js 환경을 대상으로](https://ssr.vuejs.org/guide/non-node.html) 지원하고 있습니다. 
    
    > 다른 환경에서 실행이 가능하기는 합니다만 직접 시도해 보시면 정말 수많은 문제를 만나게 됩니다.
    > 그리고 그 문제에 대해 리서치하면 *Node.js 외의 환경*은 우선 순위가 한참 떨어진다는 것을 알게 됩니다.  
                                                                                                                                                                                                                        
    그래서 이번 기회에 모두가 알고만 있는(서비스에 사용할 필요도 없는) 몇가지를 이용하여 JAVA 백엔드에서 해결해보자는 생각이 들었습니다.

    1. **첫번째 시도 : J2V8을 이용한 Java ↔ Node.js 중계**  
        ![j2v8](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/j2v8.png)
          
        첫번째 끔찍한 아이디어는 JAVA에서 Node.js 코드를 실행할 수 있게 해주는 라이브러리인 [J2V8](https://github.com/eclipsesource/J2V8)을 이용하는 것입니다. 
        J2V8을 이용하여 Node 코드를 수행하고 결과를 가져오는 방법이죠. 이건 꽤 괜찮아 보였습니다.  
        검증된 라이브러리기도 하고, [JNI](https://ko.wikipedia.org/wiki/%EC%9E%90%EB%B0%94_%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C_%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4)를 통해 Node.js를 실행하는 것이니 퍼포먼스도 좋아 보였죠.
        
        > 재미있는 점은 Node의 코어인 [V8](https://github.com/v8/v8) 자체도 JS코드를 C++로 실행하는 엔진이라는 점입니다.  
        > JAVA (기계어로 변환) → NODE → C++ (기계어로 변환) 순서로 실행하게 되는 것이죠. (언어 대통합?)  

        하지만 여기서 전혀 생각치도 못한 메모리 누수 문제가 발생했습니다.  
          
        ![메모리 누수?](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/dd.jpg)
        *메모리 누수...?*
        
        SSR을 수행할때마다 쓰레기 객체가 생기기 시작했습니다.  
        하지만 그렇게 어려운 문제는 아니었습니다. Vue SSR Renderer를 이용하여 HTML을 만들어 내는 작업 역시 *Node.js 어플리케이션을 실행하는 일련의 과정*을 따르기 때문에 
        Node.js 어플리케이션 메모리 스냅샷으로 어플리케이션의 메모리 할당 및 GC 상태 등을 확인할 수 있습니다. 
        메모리에 어떤 객체가 쓰레기로 남아있는지 알 수 있으면 그 부분부터 차근차근 수정해 나가면 되는 것이죠.
          
        메모리 누수 체크 과정을 간단하게 설명드리자면
            
        ![노드-크롬 연결](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/node-chrome-inspect.jpg) *Node.js 기동시 --inspect 플래그를 추가해 포트를 열고 크롬 개발자도구를 이용해 연결합니다*
        <br><br>  
        ![크롬 개발자도구 메모리 스냅샷](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/node-chrome-inspect2.jpg) *개발자 도구에서 메모리 스냅샷을 찍고 비교하여 GC이후에<br>메모리에 어떤 객체가, 어떤 값이 남아있는지 확인합니다*
        > 자세한 설명은 [구글 공식 가이드](https://developers.google.com/web/tools/chrome-devtools/memory-problems/heap-snapshots?hl=ko) 등을 참조하시기 바랍니다.
     
       메모리 누수는 이렇게 메모리 스냅샷 툴(간단하게는 크롬)을 이용해 잡아낼 수 있는 문제입니다. 
       하지만 고려해야 할 정말 치명적인 문제는 JNI에서 메모리 오버플로가 발생하면 JAVA 어플리케이션이 **멈추어** 버린다는 것이었습니다.   
       어플리케이션이 강제 종료되는 것도, 예외가 발생하는 것도 아니라 말 그대로 멈춰 버리면서 
       어플리케이션 레벨, 혹은 OS 레벨에서도 체크가 불가능했습니다.  
       
       > JNI를 이용한 경우 발생하는 메모리 누수와 그 문제에 관한 많은 글을 구글에서 만나보실 수 있습니다...  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
       어플리케이션이 **'멈출 수 있다'는 가능성**은 아주 심각한 장애 요소라고 판단되었기에 이 방법은 각하되었습니다.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    1. **두번째 시도: Nashorn**  
    
        ![Nashorn](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/nashorn.jpeg)
        *Rhino보다 낫다고 자랑하던 그 Nashorn입니다*
        
        두번째 끔찍한 아이디어는 자바8에서 공식으로 지원하고 자바11에서 공식으로 [Deprecated된](https://docs.oracle.com/en/java/javase/11/docs/api/jdk.scripting.nashorn/module-summary.html) Nashorn을 이용하는 것이었습니다.
        테스트만 해보고 글을 작성한 수많은 블로그들이 원망스러워질 정도로 사용할 수 없는 끔찍한 방법이었습니다.   
          
        직면했던 문제들을 나열해 보자면...
        
        1. **CommonJS 모듈 사용 불가**  
        Vue SSR 렌더러로 만들어진 코드는 commonjs 형식의 [require 구문](https://nodejs.org/api/modules.html#modules_require_id)을 이용합니다.  
        하지만 Nashorn은 지원하지 않습니다. 그렇기 때문에 폴리필을 사용하거나 다른 모듈 형식으로 빌드해야 합니다. 
        앞서 말씀드렸듯 Vue.js SSR Renderer는 Node.js를 우선으로 개발되고 있기 때문에 다른 모듈 형식으로 빌드했을 때 정상적인 작동을 기대할 수 없습니다. 
        
        1. **폴리필 사용**  
        Nashorn은 몇몇 객체를 지원하지 않기 때문에 대부분 [폴리필](https://github.com/shendepu/nashorn-polyfill)을 적용해야 합니다.  
        더군다나 성능이 심각하게 좋지 않기 때문에 폴리필을 적용하는데에만 꽤나 긴 시간이 소요됩니다. 
        게다가 이 폴리필 코드를 관리하는 것 또한 꽤나 힘든 일입니다. 어쩌면 배보다 배꼽이 더 큰 일이 될지도 모릅니다.
        
        1. **심각한 퍼포먼스**  
        정말 심하게 느립니다. 엄청나게 느려서 언급할 가치조차 없습니다. 폴리필을 적용한 후에 V8(Node.js)보다 10배정도 더 느리게 작동합니다.
        
        결국 Nashorn을 서비스에 사용하는 것은 불가능하다는 결론을 내렸습니다.  
        특히 더 이상 자바에서 지원하지 않겠다고 했으니까요.
        
        > Javascript를 사용하게 해 주겠다는 Java의 꿈은 결국... 
    
    1. **세번째 시도: Puppeteer**  
        ![puppeteer](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/puppeteer.png) *Puppeteer는 Chromium 기반으로 다양한 곳에 사용되고 있는 헤드리스 브라우저입니다*
          
        세번째 방법은 헤드리스 브라우저 [Puppeteer](https://github.com/puppeteer/puppeteer)를 이용해 사이트에 접속하고 스크립트가 실행된 결과 페이지를 가져오는 방법이었습니다.    
        이 방법으로 진행하려면 헤드리스 브라우저를 사용할 서버를 구성하고, 어플리케이션도 구성한 후 HTML을 캐시하고, 
        캐시 시간은 몇초로 하지? 이건 어느 팀에서 관리해야하는 프로젝트지? 잠깐… SSR이 아닌데?
  
  
결국 JAVA 백엔드에서는 **정상적이고 유지가능한** 방법이 없다고 판단하게 되었습니다.  
정확히는 *‘SSR을 수행해서 얻는 이득’*과 *‘SSR을 수행하는데 드는 리소스’*를 비교했을 때 **SSR은 수행할 가치가 없다**는 결론을 내리게 된 것이죠.  

![우선순위](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/ff.jpg)
*이렇게 사용자에게 보이지 않고 영향이 작은 작업은 나중에 하는게 맞겠죠?*


<br>
         
여기까지가 2019년 하반기에 수행했던 최적화 방안 및 기술 리서치입니다.  
팀 내에 관련 정보를 공유하고 한동안 다른 프로젝트와 서스테이닝 작업을 진행했죠.
  
<br>

---

<br>
  
## 그리고 2020년이 되었습니다.
2020년 상반기 모바일 줌은 다시 한번 변화를 맞게 됩니다. 바로 운영 환경 변경입니다.  
줌 인터넷도 다양한 서비스를 도커 기반으로 옮기고 비용 감소 및 오토 스케일링 최적화를 하기로 했습니다.     
  
이쯤 해서 저희 포털 개발팀은 한가지 큰 고민을 하고 있었습니다.  
*‘과연 Spring Boot가 효율적인가?’* 라는 고민이죠.  
당연히 장단점이 있고, 유지보수를 위해 Spring을 이용하는 것은 아주 유효합니다. 
     
하지만 저희 팀이 맡고 있는 *프론트 서비스 프로젝트*는 대부분 ‘API Aggregation & Frontend Serving’를 주력으로 하는 프로젝트이기 때문에, 
대부분의 **비즈니스 로직은 API 서버에서 수행**하고 프론트 서비스는 사용자에게 **보여주어야 하는 정보를 처리**하는 역할을 합니다.

![아키텍쳐2](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/architecture2.jpg)
*위 아키텍처에서 유추하실 수 있듯 프론트 서비스는 아주 가볍게 운영할 수 있습니다*
  
저희 팀은 그런 프로젝트에 Spring Boot는 *너무 무겁고 과하다*는 결론을 내리게 됩니다.  
그래서 바꿉니다. Node.js로. Express.js로.  

![컨테이너 변경](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/change-container.jpg)
*Spring Boot 어플리케이션을 Node.js 어플리케이션으로 변경합니다*
  
  > 이것은 [Netflix에서 택한 방법](https://thenewstack.io/netflix-uses-node-js-power-user-interface/)이기도 합니다.  
  > 서비스의 일부를 Node.js 기반으로 변경하여 개발 생산성과 유지보수 편의성을 높이는 방법이죠.
  
<br>
  
### 표준화 라이브러리 
이제 다른 문제가 발생합니다. Node.js 기반 웹 프레임워크인 [Express.js](https://expressjs.com/ko/)는 너무 자유로워 지옥같은 코드가 만들어질 확률이 너무 높습니다.  
저는 이런 문제를 막기 위해 표준화 라이브러리 개발을 택했습니다. 백엔드 코드는 [Typescript](https://www.typescriptlang.org/)를 사용하도록 권장하고, 
자주 사용하는 기능을 데코레이터로 개발해두어 코딩 스타일을 어느정도 강제화하는 방법이죠.  

  > 자주 사용되는 기능은 대표적으로 캐시가 있습니다.  
  > 프론트 서비스 서버에서 API 서버로 요청을 보내고 응답을 캐시해두는 패턴은 대부분의 서비스에서 사용하고 있지만
  > 각 서비스마다 다르게 구현되어 유지보수에 어려움이 있었습니다.
   
표준화 라이브러리에는 백엔드에서 사용될 [데코레이터](https://www.typescriptlang.org/docs/handbook/decorators.html)와 프론트엔드에서 사용될 [Webpack](https://webpack.js.org/) 설정 등 다양한 코드와 기능을 작성했고, 
사내 [넥서스](https://help.sonatype.com/repomanager3)에 배포하여 npm install로 손쉽게 설치할 수 있도록 했습니다.  
아래 코드는 사내 표준화 라이브러리를 사용한 예제 코드입니다  
  
```ts
/**
 * HomeController.ts 
 * 표준화 예시 코드
 */
@Controller({path: '/'})
export class HomeController {

  constructor(@Inject(CalculateService) private calculateService: CalculateService) {
  }

  @GetMapping({path: '/hello'})
  public hello(req: Request, res: Response) {
    res.json({
      hello: 'world',
      add: this.calculateService.add(100, 200)
    });
  }
}


/**
 * CaculateService.ts 
 */
@Service()
export class CalculateService {
  constructor(@Yml('application') private application?: any) {
    console.log('constructor')
  }

 /**
  * 이 클래스의 객체 생성 후 실행
  */
  @PostConstructor()
  public async postConstructor() {
    console.log('post constructor')
  }

  /**
   * 이 메소드 결과를 캐시함. 
   * 10초마다 이 메소드를 실행하여 result.completed가 false일 때에만 캐시
   */
  @Caching({key: 'test', refreshCron: '10 * * * * *', unless: (result) => result.completed === true})
  public async test() {
    const result = await Axios.get('https://jsonplaceholder.typicode.com/todos/1');
    return result.data;
  }


  public add(x, y) {
    return x + y;
  }
}
```
스프링 계열과 비슷하게 구현하였는데, 데코레이터를 이용하여 Express.js의 기능을 사용하고 
더불어 설정 값이 저장된 Yml 파일을 로드하거나 메소드의 응답 값을 캐시하는 등 유용한 기능을 구현해 두었습니다. 
이 라이브러리는 다른 서브도메인 개발에도 큰 도움을 줄 수 있습니다. 같은 방식으로, 같은 코드로 서비스 개발이 가능하기 때문입니다.  

<br>

### 다시 SSR
Node.js 기반 백엔드로 변경하며 SSR을 적용하지 않을 이유가 없어졌습니다.  
앞서 말씀드렸듯 여러가지 테스트를 했었고, 준비를 해 두었기 때문에 손쉽게 적용할 수 있었습니다.  
하지만 표준화 라이브러리에 JSDOM이 포함된 SSR 수행 코드를 녹여내기 위해 옵션을 추가하거나 공통화된 개발을 진행했습니다.

![SSR_OPTION](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/ssr-option.png)
*다른 프로젝트에서도 사용하기 위해 이런 옵션들을 추가했습니다.*

  
특히 SSR을 적용하면서 생각보다 PV가 많이 늘어나게 되었는데, 
referer 값을 확인해본 결과 검색 엔진 노출 빈도가 크게 증가했음을 알 수 있었습니다.

<br>
  
### 도커 컨테이너 생성  
Node.js를 기반으로 하는 프로젝트는 본래 파일을 모두 전송하고 *npm run ...* 명령어로 어플리케이션을 실행합니다.
어플리케이션을 관리하기 위해 [PM2](https://pm2.keymetrics.io/)나 간단하게는 [nodemon](https://github.com/remy/nodemon)과 같은 NPM 어플리케이션을 추가로 사용하죠.  
하지만 이번 작업의 목표 중 하나는 도커 컨테이너 기반 운영 환경이었습니다. 
그렇기 때문에 Node.js 어플리케이션 [도커라이징](https://nodejs.org/ko/docs/guides/nodejs-docker-webapp/)을 위해 도커 파일 생성과 [젠킨스](https://www.jenkins.io/) 설정이 필요했습니다.
이 작업은 수많은 가이드가 있으니 어려운 점은 없습니다. 단지 timezone 설정을 추가해야 했을 뿐이죠.

![도커 타임존 설정](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/docker-timezone.png){:width="600px"}
*도커 컨테이너의 타임존 설정*

추가로 표준화 라이브러리에 적용해 두었던 [winston logger](https://github.com/winstonjs/winston)에도 타임존 설정이 필요했습니다.
![winston timezone](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/winston-logger.png){:width="700px"}
*타임존 오프셋을 계산한 후 toISOString 메소드를 이용하여 출력*

간단하게 toISOString 메소드를 이용하여 로그 시간을 출력하기 위해 타임존 오프셋을 계산하고 date 값을 조정했습니다.
좋은 방법은 아니지만 단순 로그 출력에는 효과적입니다.  
  
이런 설정이 적용된 winston 로그는
![winston log](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/winston-logger2.png){:width="300px"}
위와 같이 출력되어 도커 로그로 쌓이게 됩니다.

<br>



## 성과
위의 고민들과 추가적인 작업들을 통해 모바일 줌 프로젝트는  
도커 컨테이너 운영 환경에 Node.js Express 백엔드에 Typescript 기반으로 Vue.js 프론트엔드를 구성했고 SSR이 적용된 프로젝트가 되었습니다.  
설명하니 거창해 보이네요. 성과를 정리하면 아래와 같습니다.
  
1. **SSR 적용으로 타 검색엔진에서의 유입 증가**  
    기획팀의 도움을 받아 PV 증감을 비교해 보았는데 *생각보다 큰 PV 변화*를 확인할 수 있었습니다.  
    
    ![SSR_PV](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/ssr_pv.jpg)
    *가볍게 생각할 수 없는 수준의 PV 증가를 확인했습니다*
    
    이 결과를 통해 네이버와 다음의 사이트 크롤러는 헤드리스 브라우저를 사용하지 않는다는 것을 알 수 있었습니다. 
    의외인 것은 JS를 실행하는 크롤러를 통해 웹 사이트를 수집하는 구글에서 유입된 pv도 증가했다는 것입니다. 
    이는 검색엔진 노출 친화도가 높아져 검색 결과 순위가 상승한 것으로 예측됩니다.  


2. **사양 대비 성능(TPS) 증가**  
    ![TPS CHECK](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/tps-check.png)
    *[Jmeter](https://jmeter.apache.org/)를 이용한 테스트 결과*
    
    많은 테스트 결과들이 보여주든 싱글 쓰레드에 가까운 Node.js 특성상 코어가 작은 시스템일 때 상대적으로 더 좋은 성능을 보여줍니다. 
    실제로 같은 사양 대비 [TPS](https://ko.wikipedia.org/wiki/%EC%B4%88%EB%8B%B9_%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98_%EC%88%98)가 약 40%증가하는 결과를 얻었습니다.  
    TPS뿐만 아니라 메모리 사용량도 절반 이상 줄어들어 같은 컨테이너에 다른 어플리케이션을 추가로 더 기동할 수 있을 정도로 긍정적인 결과를 볼 수 있었습니다.


3. **코드 다이어트**   
    Express 백엔드로 전환함으로서 전체 코드를 크게 줄여낼 수 있었습니다. 
    
    ![Code Lines](/images/portal/post/2020-06-20-ZUM-Mobile_SSR/code-lines.png)
    *1608 라인에서 472 라인으로 약 1/4로 줄어들었습니다*
    
    같은 기능을 구현했음에도 백엔드 코드의 라인 수가 이렇게 줄어든 것은 언어적 특성뿐 아니라, 
    표준화 라이브러리에 Scheduling, Adapter 등 기능이 포함되어 직접 구현할 필요가 없어졌기 때문입니다.
    이런 변화는 프로젝트의 주요 기능인 프론트엔드 개발에 더 집중할 수 있게 해줍니다.
    
    또한, 제가 가장 중요하게 생각하고 있는 유지보수 편의성에도 아주 큰 강점이 됩니다.    
    코딩 스타일을 어느정도 강제화함으로서 담당자가 변경되고 인수인계 받더라도 비슷한 코딩 스타일로 작성되어 있어 적응하기 쉽기 때문이죠.  



## 마치며
이 글에서는 자세하게 설명하지 않았지만 표준화 라이브러리를 유지보수 하는 것 자체도 꽤나 큰 작업입니다.  
새로운 기능 (혹은 데코레이터)가 필요하게 될 수도 있고 버그가 발견될 수도 있겠죠.   
하지만 앞으로 줌 인터넷에서 진행하게 될 많은 서브 도메인 사이트를 개발할 때에는 분명 큰 힘이 될 것이고,
그 장점이 단점을 상쇄할 것이라고 생각합니다.  
  
어쨌든 이렇게 모바일 줌은 최신 스펙을 겸비한 꽤나 재미있는 프로젝트로 완전히 탈바꿈했습니다.  
사실 모바일 줌에서 가장 재미있는 부분은 Dynamic Component를 활용한 프론트엔드와 API 부분입니다만, 
어째선지 글을 작성하지 않았었네요. 어디선가 다시 이야기할 기회가 올 거라 생각합니다. 
어쩌면 서브도메인에서, 어쩌면 줌닷컴 메인을 개편하고 다시 이야기 할 수 있겠죠.  
  
2019년 하반기와 2020년 상반기를 아우른 이 글은 여기서 마무리 짓겠습니다.  
  
지금까지 읽어주셔서 감사합니다.  








