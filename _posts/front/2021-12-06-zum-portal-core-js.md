---
layout: post
title: Zum Portal Core JS 소개
description: 줌인터넷 프론트엔드 파트에서 사용되고 있는 core package에 대해 소개합니다.
image: /images/front/post/2021-12-06-zum-portal-core-js/thumbnail.png
introduction: 줌인터넷 프론트엔드 파트에서 사용되고 있는 core package를 만들게된 과정과 기능에 대해 소개합니다.
category: portal/tech
tag: [프론트엔드, Front-end, FE, zum, zum-fe, core, yarn, mono-repo, nodejs, nestjs, expressjs]
author: junilhwang
---

> 본 포스트는 줌인터넷 포털개발팀 프론트엔드 파트에서 사용되고 있는 표준화 core package 에 대해 다루고 있습니다.
>

안녕하세요! 다시 한 달 만에 블로그 포스트를 작성하게 되었습니다.
이번에는 저희 프론트엔드 파트에서 사용하고 있는 `zum-portal-core-js`에 대해 다뤄볼 생각입니다.
`zum-portal-core-js` 는 서비스를 만들 때 필요한 Frontend config와 uilts, 그리고 backend config 및 utils를 추출하여 관리하고 있는 패키지입니다.
줌인터넷 프론트엔드 파트가 하는 업무도 홍보할겸, 그리고 파트에서 사용중인 기술스택에 대해 상세히 다뤄본적이 없어서 이렇게 포스트를 작성하게 되었습니다.

`zum-portal-core-js`는 현재

- [줌프론트](https://zum.com/)
- [모바일줌](http://m.zum.com)
- [금융줌](http://finance.zum.com)
- [스타트줌](http://start.zum.com)
- [쇼핑줌](http://shopping.zum.com)

등의 서비스에서 사용되고 있습니다. 그리고 다음과 같은 서비스에 **적용할 예정**입니다.

- [뉴스줌](http://news.zum.com)
- [모바일 뉴스줌](http://m.news.zum.com)
- [허브줌](http://hub.zum.com)
- [모바일 허브줌](http://m.hub.zum.com)
- 모바일 금융줌(신규)

## 0. 불편함을 감지하기

일단 패키지를 다루기 이전에, 줌인터넷 포털개발팀의 히스토리에 대해 먼저 설명할 필요가 있을 것 같습니다.
원래 저희 포털개발팀은 **구성원 모두가 풀스택으로 서비스를 운영**하고 있었습니다.
사실 풀스택이라고 해도 팀 내에서는 React나 Vue 같은 프레임워크를 사용하지 않고,
순수하게 `Spring MVC(Template Engine)`로만 구성된 형태로 웹 서비스를 운영했습니다.
그러다 팀 내의 기술스택의 변화를 가져온 계기가 있었는데, 바로 **[모바일줌](http://m.zum.com) 개편 프로젝트**였습니다.

### (1) SpringBoot + MVC(Template Engine) → SpringBoot + SPA(Vue)

일단 SpringBoot의 Template Engine으로만 사용자의 UI를 관리하기는 무척 번거롭습니다.
여러가지 단점이 있겠지만 핵심적인 것들 몇 가지만 추려보자면 다음과 같습니다.

- 일단 Template Engine을 사용할 경우 코드를 수정하고 반영되기 까지가 매우 느렸습니다. (아무리 빠르다고 해도 한계가 있어요.. 🥲)
- 중복되는 코드가 무척 많고, 특히 **모바일 서비스 특성상 비슷한 형태의 UI (즉, 컴포넌트)가 반복되는 경우가 많은데,** 이를 모듈화 하기가 무척 번거로웠습니다.
- 프레임워크를 사용하지 않고 직접 HTML/JS/CSS 로만 자동화 코드를 만들기까지 학습해야 하는 내용도 많고, 렌더링 최적화를 하기가 무척 힘듭니다.
- **불필요하게 Ajax 요청을 남발하는 경우**가 많습니다.
  - 특히 API를 호출하다기보단, Ajax로 변경될 템플릿 자체를 가져오는 경우가 많이 있습니다.
  - 즉, 호출도 빈번한데 호출하는게 API가 아니라 HTML Template 이라서 네트워크 통신량이 무척 많은 것이죠
  - 이럴 경우 서버에 부하가 불필요하게 생기기 때문에 instance를 추가적으로 붙여야 하는 경우가 생깁니다.

이러한 이유들 때문에 팀 내에 진지하게 Modern Frontend Framework 도입을 고민하고 있었고,
**Javascript를 깊게 해본 신입 개발자에게 파일럿 프로젝트로 모바일줌을 Vue.js로 만들어 보도록 제안**하였습니다. (지금은 퇴사하신 저의 사수님..🥲)

\* 관령링크: [Vuejs로 모바일 웹 구축하기](https://zuminternet.github.io/ZUM-Pilot-vuejs/)

파일럿 프로젝트가 생각보다 퀄리티가 좋았으며 바로 서비스로 전환해도 무방할 정도라고 생각되어 해당 파일럿 프로젝트를 고도화하여 기획도 덧붙이고 모바일줌을 다시 만들었습니다.
일단 **Server는 SpringBoot를 사용했고, Front는 Vue.js로 SPA를 구성**하여 런칭했습니다.

![1](/images/front/post/2021-12-06-zum-portal-core-js/1.png)

덕분에 불필요한 Ajax 요청도 줄일 수 있게 되었으며, 무엇보다 컴포넌트 단위의 개발이 가능해져서 UI 수정에 대한 이슈가 대폭 감소했습니다.

![2](/images/front/post/2021-12-06-zum-portal-core-js/2.png)

개편된 모바일줌 API에서는 위와 같이 **어떤 Component로 렌더링을 하고, 어떤 데이터를 삽입할지 정의**되어 있습니다.

![3](/images/front/post/2021-12-06-zum-portal-core-js/3.png)

그리고 프론트에서는 `Dynamic Component`를 이용하여 API에서 내려주는 Component와 Data에 대해 렌더링을 진행합니다.

결과적으로 프론트엔드에서는 무엇이 그려지는지에 대한 정보는 없고, **어떻게 그려지는지에 대해서만 개발**할 수 있게 되었습니다.

대부분의 로직이 백엔드의 API에 종속되기 때문에, 유지보수(운영) 자체에 대한 이슈가 거의 생기지 않게 되었습니다.
**극단적으로 UI가 변경되는게 아니라면 프론트엔드 코드는 수정될 일이 거의 없었습니다.**

### (2) SpringBoot + SPA → NodeJS + SPA + SSR

그렇게 개편을 진행한 다음에 문제가 되는 부분은 바로 SSR 이였습니다. SSR을 하기 위해선 거의 필수적으로 Node.js 환경이 필요했는데, 자세한 내용은 **[모바일 줌 SpringBoot → NodeJS 전환기 (feat. VueJS SSR)](https://zuminternet.github.io/ZUM-Mobile-NodeJS/)** 포스트에서 확인할 수 있습니다.

![4](/images/front/post/2021-12-06-zum-portal-core-js/4.png)

결론만 이야기 하자면

- SSR(Server Side Rendering)이 가능해졌으며
- 똑같은 자원으로 더 많은 일을 할 수 있게 되었고,

![5](/images/front/post/2021-12-06-zum-portal-core-js/5.png)

- 실제로 같은 사양 대비 [TPS](https://ko.wikipedia.org/wiki/%EC%B4%88%EB%8B%B9_%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98_%EC%88%98)가 약 40% 증가하는 결과를 얻었습니다.
- TPS뿐만 아니라 메모리 사용량도 절반 이상 줄어들어 같은 컨테이너에 다른 어플리케이션을 추가로 더 기동할 수 있을 정도로 긍정적인 결과를 볼 수 있었습니다.

> 올해 초에 [줌프론트](https://zum.com)도 Node.js로 개편했는데, **Spring을 사용할 땐 30개의 instance였으나, Node로 개편하고 나서 5개의 instance로 축소하는 등** 굉장히 많은 리소스를 절약할 수 있었습니다.

다만 Node.js + Express.js의 경우 Java + SpringBoot 보다 기능도 많이 부족했고,
무엇보다 코드 스타일이 작성하는 사람에 따라 극단적으로 달라지기 때문에 어느 정도 강제성을 가질 수 있는 코드를 제공하는 과정이 필요했습니다.

**이러한 과정에서 `zum-portal-core-js`를 만들게 되었습니다.**

## 1. zum-portal-core-js@1.x.x ( 패키지 제작 )

### (0) 목표

#### 1) Express.js를 커스텀하여 spring 처럼 사용하기

일단 Node.js + Express.js 를 사용하더라도 spring을 사용하는 다른 사람들에게도 친화적인 형태의 코드를 만들어야 했습니다.
왜냐면 zum-portal-core-js를 만들 당시에는 줌인터넷에 프론트엔드를 전문으로 하는 팀(혹은 파트)이 없었습니다.
누구라도(spring을 사용하던 사람이라도) zum-portal-core-js를 사용할 때 불편함이 없어야 한다고 생각했습니다.
무엇보다 **우리는 모두 언제 퇴사할지 모르기 때문에** Spring을 하던 사람이 Node로 된 프로젝트를 인수인계 받았을 때 위화감이 없어야 하는 것을 첫 번째 목표로 했습니다.

그래서 백엔드에서는 `typescript`를 강제했으며, Spring의 `annotation`과 비슷한 역할을 하는 `decorator`를 최대한 적극적으로 이용했습니다.

덕분에 팀 내에 `zum-portal-core-js`와 관련된 내용을 전파할 때 `이거 Node 맞나요?`라는 반응이 많이 있었습니다.

#### 2) 최소한의 기능만 만들기

직접 core package를 만드는 이유는 다른 오픈소스에서 제공하는 수많은 기능들이 불필요하기 때문입니다.
우리에게 필요한건 Singleton Container, SSR, Cache, Schedule 같은 소수의 핵심 기능이었습니다.
**최소한의 기능으로 최대한의 효과를 보는 것!**

#### 3) frontend + backend 를 한 개의 repository로 관리하기

![6](/images/front/post/2021-12-06-zum-portal-core-js/6.png)

먼저 코어 패키지만 설치했을 때 정말 꼭 필요한 패키지가 아니면 사용하지 않는 것을 목표로 했습니다.

```jsx
"dependencies": {
  // cli 는 npm script 실행을 위해서 필요함
  "@vue/cli-plugin-babel": "3.12.1",
  "@vue/cli-plugin-typescript": "3.12.1",
  "@vue/cli-service": "3.12.1",

  // express, vue, vue-cli, vuex, vue-router 등 대부분의 패키지를 포함하고 있음
  "zum-portal-core": "1.1.2",
}
```

그리고 npm script도 frontend와 backend를 같이 관리하도록 구성했습니다.

```jsx
"scripts": {
  "dev": "concurrently -c yellow,cyan \"npm:frontend:dev\" \"npm:backend:dev\"",
  "start": "cross-env ZUM_BACK_MODE=deploy SSR_MODE=prod ENABLE_WHATAP=true NODE_ENV=production ts-node ./backend/Server.ts",
  "start:qa": "cross-env ZUM_BACK_MODE=deploy SSR_MODE=qa NODE_ENV=production ts-node ./backend/Server.ts",
  "build": "rimraf ./node_modules/.cache && npm run frontend:build",
  "frontend:dev": "cross-env ZUM_FRONT_MODE=dev vue-cli-service serve",
  "frontend:publish": "cross-env ZUM_FRONT_MODE=publish vue-cli-service serve",
  "frontend:build": "vue-cli-service build --no-clean --report && cross-env ZUM_FRONT_MODE=ssr vue-cli-service build --no-clean",
  "frontend:build-report": "vue-cli-service build --no-clean --report",
  "backend:dev": "cross-env NODE_ENV=development nodemon --exec ts-node --transpile-only backend/Server.ts",
  "backend:dev-stub": "cross-env ZUM_BACK_MODE=stub NODE_ENV=development nodemon --exec ts-node --transpile-only backend/Server.ts"
},
```

- `frontend:build`를 실행하면 resource 폴더에 bundling된 `css` `js` `img` `client-manifest` `ssr-bundler` 등이 위치됩니다.
![7](/images/front/post/2021-12-06-zum-portal-core-js/7.png){:style="display:block;margin:0;"}

- `frontend` FE 관련 리소스를 관리합니다.
![8](/images/front/post/2021-12-06-zum-portal-core-js/8.png){:style="display:block;margin:0;"}

- `backend` BE관련 리소스를 관리합니다.
![9](/images/front/post/2021-12-06-zum-portal-core-js/9.png){:style="display:block;margin:0;"}


#### 4) SSR(Server-Side Rendering) 관련 유틸리티 제공

SSR의 경우 무척 손이 많이 가는 작업입니다.
그래서 SSR을 할 때 기본적으로 필요한 설정들을 core에서 제공하는 방식으로 만들었습니다.

SSR에 대한 자세한 내용은 **[Vue SSR 제대로 적용하기 (feat. Vanilla SSR)](https://zuminternet.github.io/vue-ssr/)** 로 대체하겠습니다.

### (1) Backend (Server-side)

먼저 다음과 같은 `decorator`를 정의했습니다.

- `@Controller`: Request Mapping을 위해 사용하는 Controller 클래스에 사용합니다.
  - `@GetMapping` `@PostMapping` `@PutMapping` `@DeleteMapping`
    - 아마 Spring을 사용하는 사람이라면 바로 이해할 수 있을 것 같습니다.
    - 데코레이팅한 메소드를 http 요청에 대해 핸들링 합니다.
  - `@Middleware`
    - 핸들러에 미들웨어를 삽입할 수 있습니다.

```ts
@Controller({path: '/'})
export class HomeController {
  
  /**
   * 템플릿을 반환
   * @param req
   * @param res
   */
  @GetMapping({path: '/'})
  public async getHome(req: Request, res: Response) {
    console.error({
    res.send("메인페이지");
  }
  
  @Middleware([
    (req, res, next) => {
      console.log('hello middleware');
      next()
    },
  ])
  @GetMapping({path: '/hello'})
  public hello(req: Request, res: Response) {
    res.json({
      message: "/hello 페이지"
    });
  }
}
```

- Singleton Container 관련 데코레이터
  - `@Component`
    - Spring의 `@Component annotation` 과 똑같은 역할을을 수행합니다.
    - `@Component`는 `@Service` `@Scheduler` `@Singleton` `@Injectable` `@Facade` 등을 alias로 사용할 수 있도록 하였습니다.
    - 사용하는 로직에 따라 적절한 Decorator를 붙입니다.
  - `@Inject`
    - Component의 constructor에서 사용 가능한 데코레이터로 **파라미터에 해당하는 객체를 주입**받아서 사용할 수 있습니다.

```ts
@Service()
export class CatService {

  private readonly cats: Cat[] = [];

  create(cat: Cat) {
    this.cats.push(cat);
  }

  findAll(): Cat[] {
    return this.cats;
  }

}

@Service()
export class HouseService {
  constructor (
    // 상단에 정의한 CatService의 singleton 객체를 주입받아서 사용합니다.
    @Inject(CatService) private readonly catService: CatService,
  ) {}

  homecoming () {
    const cats = this.catService.findAll();
    cats.forEach(cat => cat.meow("밥달라옹"));
  }
}
```

- 유틸성 데코레이터
  - `@Scheduled`: 해당 메소드를 일정 시간마다 실행합니다.

```ts
@Service()
export class MeowService {

  // 10초마다 이 메소드를 실행합니다.
  @Scheduled({ cron: "*/10 * * * * *", runOnStart: true })
  meow() {
    console.log("야옹");
  }

}
```

  - `@Caching`: 메소드의 결과값을 캐싱하여 사용합니다.

```ts
@Service()
export class WeatherService {

  // 60초마다 이 메소드를 실행합니다.
  @Caching({ cron: "*/60 * * * * *" })
  getWeathers() {
    return 날씨정보를_가져오는_메소드();
  }

}

@Service()
export class PostService {

  // 결과값을 10초동안 캐싱합니다.
  @Caching({ ttl: 10 })
  getPost(id: number) {
    return 데이터베이스에서_게시물을_ID에_대한_게시물을_가져오는_메소드(id);
  }

}
```

> 특히 `Caching`의 경우 포털 서비스에 꼭 필요한 로직입니다.
> 실시간으로 API를 호출하는게 아니라 일정 주기마다 API를 호출하여 캐싱하고,
> 실제로 위의 서비스로직을 Controller에서 호출하면 항상 캐싱된 값에 대해서 반환합니다.
> 즉, 불필요한 io가 발생하지 않도록 하는 것입니다.

- spring의 application.yml 대체제
  - `@Yml`
    - Component의 constructor에서 사용 가능한 데코레이터로 파일명에 해당하는 yml 객체를 주입받아서 사용할 수 있습니다.

`application.yml`

```yaml
# 공통 설정 
default:
  service-name: "zum-portal-core-js-local"
  api: "http://localhost:8080" # 기본적으로 localhost 호출

# NODE_ENV가 development일 때
development:
  service-name: "zum-portal-core-js-dev"
  api: "http://dev-api.zum.com" # 개발용 api 호출

# NODE_ENV가 production-local일 때
production-local:
  service-name: "zum-portal-core-js-stage"
  api: "http://stage-api.zum.com" # stage api 사용

# 서비스할 때
production:
  service-name: "zum-portal-core-js"
  api: "http://api.zum.com" # 실제 API 사용
```

`application.yml`은 다음과 같이 주입하여 사용할 수 있습니다.

```ts
export class AppService {
  constructor (
    @Yml("application") private readonly property: any,
  ) {
    // NODE_ENV에 따라서 출력되는 결과값이 달라짐
    console.log(
      property['service-name'],
      property['api'],
    );
  }

}
```


이러한 Decorator를 통해서 Spring을 사용하던 사람도 Node를 사용할 때 위화감이 없도록 만들었습니다.

그리고 표준화 패키지를 만드는 목적 중 하나가 SSR(Server Side Rendering)입니다.
SSR 개념이 난해하기도 하고, 손이 많이 가는 작업이 많으며 예상하지 못한 구간에서 오류가 발생하기도 하는 등의 문제가 있어서 이를 해결하기 위한 작업을 진행했습니다.
<u>이 포스트에서 SSR에 대한 자세한 내용은 다루지 않을 예정입니다.</u>

- `bundleRendering` 정의하기
  - SSR을 할 때 window와 document 객체를 사용할 수 있도록 작업합니다.
  - SSR 시점에 아무리 서비스 내에서 window와 document 사용을 하지 않도록 하여도, 다양한 라이브러리를 사용하다보면 의도하지 않은 window, document 접근이 발생하기 때문입니다.
  - 그래서 window와 document 객체를 생성한 다음에 `bundler` 에게 이를 넘겨줍니다.

```ts
export async function bundleRendering(
  renderer: BundleRenderer,
  option: RenderingOption
): Promise<string> {

  // Document 관련 정의부
  global.document = jsdom(``, {
    url: option.projectDomain,
    userAgent: option?.userAgent.toLowerCase(),
    cookieJar: option.cookieJar
  });

  // Window 관련 정의부
  global.window = document.defaultView;
  global.location = window.location;
  global.navigator = window.navigator;
  global.localStorage = {
    getItem(key) { return this[key] || null; },
    setItem(key, value) { this[key] = value; }
  };
  global.window.resizeTo(
    option?.windowSize?.width || 375,
    option?.windowSize?.height || 812
  );

  // Window 객체에 바인드
  Object.assign(global.window, option?.windowObjects || {});

  // Vue SSR 실행 및 JSDOM close 이후 SSR된 결과 반환
  try {
    // SSR을 할 때 window, document를 사용하는 부분이 있더라도 오류가 발생하지 않고 진행되도록 한다.
    const result = await renderer.renderToString(option.rendererContext || {});
    global.window.close();
    return result;
  } catch (e) {
    throw new Error(`There is an error when SSR bundleRendering ${e}`)
  }
  
}
```

- `bundleRendering` 사용하기

```ts
@Facade()
export default class SsrService {

  // SSR은 CPU 사용이 큰 작업이므로 캐싱을 고려할 것
  public async getRenderedHtml(): Promise<string> {

    // SSR 렌더러 생성
    const bundle = require("vue-ssr-server-bundle.json"); // 실제 경로는 더 복잡함
    this.renderer = createBundleRenderer(bundle, {
      runInNewContext: false,
      clientManifest: "...",
      template: "...",
    });

    // Vue.js SSR 수행 후 만들어진 HTML 반환
    const html = await bundleRendering(this.renderer, {
      projectDomain: "https://zum.com",
      userAgent: renderingUserAgent.desktop.windowChrome,
      cookieJar: createCookieJar(domain, {}), // cookie 전달
      windowObjects: {},
      rendererContext: {path: '/'}, // ssr context 전달
    });
    return html;
  }

}
```


다음은 실제 [줌프론트](http://zum.com)에서 사용되는 일부 Controller 코드입니다.

```ts
/**
 * 줌 닷컴 메인 페이지 컨트롤러
 */
@Controller({path: '/'})
export default class HomeController {

  constructor(
    // Facade 주입
    @Inject(HomeFacade) private homeFacade: HomeFacade
  ) {}

  // 메인페이지로 접근시 SSR된 html string 반환
  @GetMapping({path: ['/:id?', '/*/home']})
  public async getHome(req: Request, res: Response, next: NextFunction) {
    // SSR이 실행된 결과물 반환
    return res.send(await this.homeFacade.getRenderedHtml());
  }

}
```

### (2) Frontend(Client-Side)

frontend에서는 특별한 기능을 제공하진 않고, 대신 공용으로 사용하는 설정파일을 작성하여 사용했습니다.

설정파일에 대한 자세한 내용은 다음 포스트에서 확인할 수 있습니다.

- **[Webpack Dev Server를 이용한 개발 환경 구성 Part1](https://zuminternet.github.io/ZUM-Webpack-dev-proxy-part1/)**
- **[Webpack Dev Server를 이용한 개발 환경 구성 Part2](https://zuminternet.github.io/ZUM-Webpack-dev-proxy-part2/)**

이 포스트에서는 필수적인 내용만 간략하게 소개해보겠습니다.

```ts
// 기본 설정 획득
const getDefaultCliOption = require('./default/_getDefaultCliOption');

module.exports = {

  /**
   * 글로벌 환경변수와 모드별 환경변수를 합치는 함수
   *
   * @param projectConfigurer 프로젝트에서 고유하게 사용되는 설정
   * @returns Vue Cli3 옵션
   */
  modeConfigurer: function (projectConfigurer) {

    /**
     * 설정을 적용하는 함수
     *
     * @param func 적용할 WebpackChain 함수
     * @param config 적용할 옵션
     */
    const applyChain = (func, config) => func ? func(config) : null;

    // 기본 설정 획득
    const defaultOption = getDefaultCliOption();

    // Build를 하지 않는 경우에는 개발에 필요한 환경을 정의합니다.
    // 필수설정 > 각종 개발환경에 대한 설정 > 프로젝트 설정 순서로 덮어씁니다.
    if (
      process.env.NODE_ENV === 'development' ||
      process.env.NODE_ENV === undefined
    ) {
      // ZUM_FRONT_MODE는 'publish' 혹은 'dev' 둘 중 한개가 할당됩니다.
      const requiredConfig = require(`./default/${process.env.ZUM_FRONT_MODE}.config.js`);
  
      // 여기가 핵심코드입니다.
      // 기본 설정 + 필수 설정 + 프로젝트 설정을 차례대로 불러와서 덮어씁니다.
      return merge.all([defaultOption, requiredConfig, projectConfigurer, {
        chainWebpack: config => {
          // webpack chain 함수를 차례대로 적용합니다.
          applyChain(defaultOption.chainWebpack, config);
          applyChain(requiredConfig.chainWebpack, config);
          applyChain(projectConfigurer.chainWebpack, config);
        }
      }]);

    }

    // build를 할 때는 CSR인 경우와 SSR인 경우를 구분하여 작업합니다.
    // 개발환경에 필요한 설정은 제외하고 오직 build에 필요한 설정만 작업합니다.
    return merge.all([defaultOption, projectConfigurer, {

      chainWebpack: config => {
        // 함수 머지가 불가능하므로 직접 webpack chain 함수 실행.
        applyChain(defaultOption.chainWebpack, config);
        applyChain(projectConfigurer.chainWebpack, config);

        // SSR 빌드 모드가 아닐 때 static 폴더 삭제.
        if (process.env.ZUM_FRONT_MODE !== 'ssr') {
          const staticPath = path.join(resourcePath, './static');

          rimraf.sync(`${staticPath}/{css,img,js}`);
          for (let key in page) { // 생성될 파일들 제거
            if (!page.hasOwnProperty(key)) continue;
            rimraf.sync(path.join(resourcePath, `./${page[key].filename}`));
          }
        }

      },

      assetsDir: './static/',
      outputDir: outputPath,
    }]);
  }

};
```

처음에 core를 만들었을 때는 복잡한 설정이 많아서 최대한 불필요한 내용은 생략했습니다. 중요한건 다음과 같습니다.

- `개발`을 위한 설정
- `CSR`을 위한 설정
- `SSR`을 위한 설정

**이렇게 3가지로 분리해서 관리한다는 점입니다.**

### (2) 배포

배포는 사내에서 관리하는 [nexus](https://www.sonatype.com/products/repository-oss)에 하기로 결정했습니다. **지금은 코드를 최대한 다듬어서 Github에 올려놓는 것을 목표로 하고 있습니다.**

> Nexus는 Maven, Docker, PyPI, npm 등의 패키지를 관리할 수 있는 설치형 Repository 입니다. local nexus를 사용할 경우 빠르게 라이브러리를 끌어올 수 있고, 팀내에서 사용하는 공용 라이브러리를 local nexus에 배포하여 관리할 수 있습니다.
>

먼저 nexus에 repository를 만들고 배포하기 위해선 다음과 같은 과정이 필요합니다.

- nexus에 npm repository 생성
  - npm group 생성
  - npm repository 생성
  - npm repository에 group 지정
  - role 생성
  - role에 대한 privilege 지정
  - user에 role 지정
- package.json에 `publishConfig` 지정
  - `.npmrc` 작성
  - nexus 로그인
  - npm publish
- nexus에 배포된 package 설치하기
  - `.npmrc` 작성

#### 1) 일단 nexus에 관리자 계정으로 로그인 한 다음 Repository를 생성해야 합니다.

![10](/images/front/post/2021-12-06-zum-portal-core-js/10.png)

#### 2) 설정 → Repository → Repositories → Create Repository

![11](/images/front/post/2021-12-06-zum-portal-core-js/11.png)

#### 3) npm (group) 선택

![12](/images/front/post/2021-12-06-zum-portal-core-js/12.png)

- group name 을 작성합니다.
- blog Store는 npm으로 지정합니다.
  - 만약 npm이 없다면 좌측의 blob store 메뉴로 들어가서 직접 npm을 만들어서 저장합니다.

![13](/images/front/post/2021-12-06-zum-portal-core-js/13.png)

- 마지막으로 상위 그룹을 지정하는 항목이 있는데, 저희 파트의 경우 `zum-portal-npm` 을 지정하였습니다. 굳이 상위 그룹을 지정하지 않아도 무방합니다. 필요할 때 지정하여 사용하면 됩니다.

#### 4) npm hosted repository 생성

![14](/images/front/post/2021-12-06-zum-portal-core-js/14.png)

![15](/images/front/post/2021-12-06-zum-portal-core-js/15.png)

#### 5) Role 지정

![16](/images/front/post/2021-12-06-zum-portal-core-js/16.png)

- Roles → 신규 Roles을 생성하거나 기존에 있는 Roles를 선택 → `zum-portal-core-js-*` 로 되어있는 Available 추가 후 저장합니다.

#### 6) package.json에 `publishConfig`지정

![17](/images/front/post/2021-12-06-zum-portal-core-js/17.png)

![18](/images/front/post/2021-12-06-zum-portal-core-js/18.png)


#### 7) core project에 .npmrc 추가
- npm repository와 관련된 정보를 작성하는 파일입니다.
- nexus 관련 정보를 기입해야 하기 때문에 필수로 추가해줘야합니다.

```bash
email=<NEXUS_계정_이메일>
always-auth=true
_auth=<Authorizatio Token 입력>
```

`_auth`의 경우 다음과 같은 명령어를 통해서 생성할 수 있습니다.

```bash
> echo -n 'username:password' | openssl base64

# 가령, id가 junil, pw가 1234 일 경우 다음과 같이 실행
> echo -n 'junil:1234' | openssl base64
```

![19](/images/front/post/2021-12-06-zum-portal-core-js/19.png)

#### 8) package에서 export 할 file 지정

![20](/images/front/post/2021-12-06-zum-portal-core-js/20.png){:style="display:block;margin:0;"}

#### 9) typescript를 사용한다면 build를 해서 js로 변환하는 작업이 필요합니다. 이에따라 npm script에 build를 추가해줍니다.

![21](/images/front/post/2021-12-06-zum-portal-core-js/21.png){:style="display:block;margin:0;"}

#### 10) nexus 로그인

```bash
# 이 명령어를 실행한 다음 username, password, email 등을 입력하여 로그인합니다.
> npm login --registry=http://ci-portal.zuminternet.com/nexus/repository/zum-portal-core-js/
```

![22](/images/front/post/2021-12-06-zum-portal-core-js/22.png)

#### 11) package 이름 지정

![23](/images/front/post/2021-12-06-zum-portal-core-js/23.png){:style="display:block;margin:0;"}

#### 12) typescript build 후, npm publish 실행

```bash
> npm run build
> npm publish
```

![24](/images/front/post/2021-12-06-zum-portal-core-js/24.png)

#### 13) 다른 프로젝트에서 core package 설치하기
- 먼저 dependencies에 package를 추가합니다.

```jsx
"dependencies": {
  /* ...생략... */
  "zum-portal-core-js": "1.1.0",
}
```

- `.npmrc`에 nexus(registry) 정보를 입력합니다.

```bash
# publish는 repository(/nexus/repository/zum-portal-core-js)에 하고
# 설치할 때는 group 에서 가져옵니다.
# group을 지정하게 되면 해당 group에 있는 다른 repository 또한 설치가 가능합니다.
registry=http://ci-portal.zuminternet.com/nexus/repository/zum-portal-npm/
```

- 이렇게 registry까지 등록이 되어야 설치가 가능합니다.

```bash
# npm으로 설치할 수도 있고
> npm install

# yarn으로 설치할 수도 있습니다.
> yarn install
```

### (4) 문제점

#### 1) 배포 시간

앞선 내용 처럼 frontend와 backend를 하나의 package로 관리했습니다.
이럴 경우 제일 큰 문제는 바로 **배포 시간이 생각보다 심각하게 올래 걸린다는 것**이었습니다.

![25](/images/front/post/2021-12-06-zum-portal-core-js/25.png)

배포 시간이 오래걸리는 이유는 다음과 같습니다.

- npm 패키지 설치
  - frontend 패키지 설치
  - backend 패키지 설치
- frontend build
  - CSR 빌드 (css, js, image, html 등의 static 파일 생성)
  - SSR 빌드 (ssr bundler 생성)

일단 이 패키지를 만들어서 사용할 당시에는 배포가 그렇게 빈번하게 일어나지 않았기 때문에 이정도 불편함은.. 감수하자고 생각했습니다.

#### 2) 점점 비대해지는 기능

이보다 더 큰 문제는 복잡한 기능을 유지보수 하기가 힘들다는 것이었습니다.
시간이 흐를 수록 zum-portal-core-js에 여러가지 기능이 추가되고,
version을 올리는 과정에서 오류가 발생하기도 하고 유지보수를 하기 힘들어지는 문제들이 있었습니다.

아무것도 수정하지 않고 프로젝트를 배포했는데 계속 timeout 오류가 발생해서 몇 시간 동안 고생한적이 있었는데 알고보니 zum-portal-core-js에 추가된 기능이 발생시킨 오류였습니다.

## 2. zum-portal-core-js@2.x.x ( NestJS 도입 )

![26](/images/front/post/2021-12-06-zum-portal-core-js/26.png)

### (0) NestJS 도입 계기

1. 유지보수의 문제점

그렇게 zum-portal-core-js를 만든지 1년 정도 지났을 때 `굳이 직접 Decorator를 만들어서 유지보수를 해야할까?` 라는 생각이 들었습니다. 최대한 코드를 쉽게 작성했다고 하더라도 내부의 복잡한 로직 자체를 모든 사람이 이해하긴 어려우며, 특히 zum-portal-core-js의 자체적인 오류가 있을 경우 이를 바로 찾아내서 수정하는 것은 패키지를 만든 사람 외에는 무척 힘든 일이었습니다.

1. 프론트엔드 파트 신설

그리고 프론트엔드 파트가 신설 되면서 Spring 사용자의 입장까지 고려할 필요가 없어졌습니다. 그리고 이 패키지를 사용하는 사람이 더욱 많아질 예정이기 때문에 더더욱 복잡한 내부의 코드를 한 명 한 명이 파악하고 이해하기란 쉬운 일이 아니었습니다.

위와 같은 이유들 때문에 파트원들과 상의하여 [NestJS](https://nestjs.com/)를 도입하기로 결정했습니다. NestJS의 경우 일단 공식문서가 무척 잘 작성되어있고, Cache나 Schedule 같은 기능도 프레임워크에서 제공하며 기능을 확장할 필요가 없어보였기 때문입니다.

### (1) 개선점

사실 이 때는 개선이라고 할게 딱히 없었습니다. 직접 작성한 decorator를 전부 제거하고, nestjs에서 제공하는 기능으로 대체했습니다.

### (2) 문제점

다만 NestJS를 적용하고 보니 다음과 같은 문제점이 있었습니다.

1. webpack 버전이 겹치는 현상

![27](/images/front/post/2021-12-06-zum-portal-core-js/27.png)

![28](/images/front/post/2021-12-06-zum-portal-core-js/28.png)

vue-cli의 경우 webpack 4버전을 사용하고, nestjs의 경우 webpack 5버전을 사용합니다. 그래서 npm으로 설치할 때는 오류가 발생하는 문제가 있었습니다. 일단 yarn으로 설치하면 오류는 없었기 때문에 무조건 yarn을 사용하도록 가이드했습니다.

1. cache 로직의 복잡도 증가

1.x.x 버전의 경우 다음과 같이 cache를 적용할 수 있었습니다.

```ts
@Service()
export class WeatherService {

  // 10초마다 이 메소드를 실행합니다.
  @Caching({ cron: "*/60 * * * * *" })
  public getWeathers() {
    return 날씨정보를_가져오는_메소드();
  }

}
```

그런데 NestJS에서는 주기적으로 메소드를 실행하여 cache하는 기능이 없었습니다. 대신 Cache와 Schedule을 조합하여 다음과 같이 사용해야 했습니다.

```ts
@Injectable()
export class WeatherService {

  contructor (
  @Inject(CACHE_MANAGER)
  private readonly cacheManager: Cache,
  ) {}

  // 10초마다 이 메소드를 실행합니다.
  @Cron("*/10 * * * * *")
  private refreshWeathers() {
    const data = 날씨정보를_가져오는_메소드();
  if (validate(data)) return;
  this.cacheManager.set("weathers", data, { ttl: Infinity });
  }

  // 10초마다 이 메소드를 실행합니다.
  public getWeathers() {
    return this.cacheManager.get("weathers");
  }

}
```

그리고 NestJS의 Cache의 경우 Decorator를 Controller layer 에서만 사용할 수 있었습니다. Service Layer 에서는 직접 Cache를 다루는 instance를 주입해서 사용해야 했습니다.

1. 여전히 오래 걸리는 배포 시간

![29](/images/front/post/2021-12-06-zum-portal-core-js/29.png)

그래도 1.x.x 에서는 backend를 구성할 때 express 외의 패키지는 거의 설치하지 않았는데, **NestJS의 경우 부가적으로 설치되는 패키지가 많아지면서 배포 시간이 더더욱 길어졌습니다.** 특히 제가 담당하는 프로젝트의 경우 배포를 무척 자주 했기 때문에 배포 시간 단축을 해결 하는 것이 무척 중요했습니다.

1. NodeJS를 사용하지 않는 프로젝트

이건 조금 다른 문제인데, 사내에서 관리되고 있는 CMS 프로젝트의 경우 전부 Spring으로 구성된 상태입니다. SSR을 할 필요도 없고, DB와 밀접한 프로젝트가 많기 때문에 NodeJS를 사용할 필요가 없기 때문입니다. 그런데 이런 프로젝트에 core package를 설치할 경우 불필요하게 Express 같은 패키지가 설치됩니다. 그래서 아예 frontend와 backend를 따로 떼어내는 작업이 필요했습니다.

## 3. 패키지 분리

위와 같은 문제점을 인지하여 기존에 하나의 package로 관리했던 zum-portal-core-js를 분할하기 시작했습니다. yarn workspace를 이용하여 `모노레포`로 만들었습니다.

![30](/images/front/post/2021-12-06-zum-portal-core-js/30.png)

![31](/images/front/post/2021-12-06-zum-portal-core-js/31.png)

zum-portal-core 사용 예시를 위한 프로젝트도 `모노레포`로 구성하여 사용했습니다.

### (0) Nexus에 repository 생성

![32](/images/front/post/2021-12-06-zum-portal-core-js/32.png)

먼저 다음과 같은 repository를 생성합니다.

- zum-portal-core-frontend
- zum-portal-core-backend
- zum-portal-core-banner
- eslint-config-zum

그리고 기존에 만들어두었던 zum-portal-core group에 해당 repository를 지정합니다. 이렇게 grouping 하여 repository를 관리할 수 있습니다.

### (1) @zum-portal-core/banner

별거아니지만 먼저 frontend와 backend에서 프로젝트를 시작할 때 출력하는 banner가 있습니다. 가볍게 이 banner와 관련된 내용부터 분리했습니다.

![33](/images/front/post/2021-12-06-zum-portal-core-js/33.png)

### (2) @zum-portal-core/frontend

배포시간을 줄이기 위해선 backend와 frontend의 명확한 구분이 필요했습니다. frontend 관련 package를 전부 devDependency로 가져와야했기 때문입니다.

기존에 vue-cli 3.x.x버전을 사용하고 있었는데, 패키지를 분리하는 과정에서 4.x.x 버전으로 업그레이드 했습니다.

```ts
"dependencies": {
  "@vue/cli-plugin-babel": "~4.5.0",
  "@vue/cli-plugin-router": "~4.5.0",
  "@vue/cli-plugin-typescript": "~4.5.0",
  "@vue/cli-plugin-vuex": "~4.5.0",
  "@vue/cli-service": "~4.5.0",
  "axios": "~0.21.1",
  "cookie-parser": "~1.4.4",
  "deepmerge": "~4.2.2",
  "express": "~4.17.1",
  "js-cookie": "~2.2.1",
  "core-js": "^3.6.5",
  "node-sass": "^4.14.0",
  "terser-webpack-plugin": "~2.3.2",
  "vue": "^2.6.11",
  "vue-loader": "~15.9.6",
  "vue-router": "^3.2.0",
  "vue-server-renderer": "~2.6.13",
  "vue-template-compiler": "^2.6.11",
  "vuex": "^3.4.0"
},
```

그리고 frontend 전용 nexus repository를 만들었으며 다음과 같이 package.json을 구성했습니다.

```ts
"name": "@zum-portal-core/frontend",
"version": "1.0.0",
"description": "Vue.js 환경설정을 위한 코어 프로젝트",
"publishConfig": {
  "registry": "http://ci-portal.zuminternet.com/nexus/repository/zum-portal-core-frontend/"
},
```

npm publish를 하면 기존의 `zum-portal-core-js`에 올라가는게 아니라 `zum-portal-core-frontend`에 올라가게 됩니다. 패키지 이름은 `@zum-portal-core/frontend` 로 지정했습니다.

이 외에도 자잘한 변화가 무척 많았는데 불필요한 설정을 제거하고, 조금 더 프로젝트 단위로 설정을 커스텀하기 쉽게 만들었습니다.

webpack-devserver로 개발할 때 환경변수를 통해서 ssl이 적용된 서버를 띄울 수 있도록 작업했습니다.

![34](/images/front/post/2021-12-06-zum-portal-core-js/34.png)

### (3) @zum-portal-core/backend

```ts
"name": "@zum-portal-core/backend",
"version": "1.0.0",
"description": "NestJS 백엔드 코어 프로젝트",
"main": "dist/index.js",
"publishConfig": {
  "registry": "http://ci-portal.zuminternet.com/nexus/repository/zum-portal-core-backend/"
},
```

package 이름은 `@zum-portal-core/backend`로 지정하였고, frontend와 마찬가지로 새로운 nexus repository를 만들어서 배포했습니다.

처음에는 특별한 기능을 추가하기보단 패키지 분리 위주의 작업을 했으나, 나중에 1.x.x 버전에 있던 Caching 기능을 NestJS 기반으로 만들어서 사용할 수 있도록 구성했습니다.

자세한 내용은 [NestJS Custom Caching Decorator 만들기](https://zuminternet.github.io/nestjs-custom-decorator/)에서 다루고 있습니다.

각설하고, `@ZumCache` 라는 Decorator로 만들었으며 다음과 같이 사용할 수 있습니다.

```ts

@Injectable()
export class WeatherService {

  contructor () {}

  // 60초마다 이 메소드를 실행합니다.
  @ZumCache({ cron: "*/60 * * * * *" })
  private refreshWeathers() {
    return 날씨정보를_가져오는_HTTP_메소드();
  }

}

@Injectable()
export class PostService {

  contructor () {}

  // 10초동안 결과값을 캐싱합니다.
  @ZumCache({ ttl: 10 })
  private getPost(id: number) {
    return ID값에_대한_Post를_가져오는_메소드(id);
  }

}
```

### (4) @zum-portal-core/eslint-config

이건 최근에 추가된 패키지인데, 팀 내에 코딩 컨벤션이라고 할만한게 딱히 없는 상태입니다. 그래서 eslint를 통해서 컨벤션을 만들어가고자 core project에 eslint 설정을 작성하여 관리하고 있습니다.

![35](/images/front/post/2021-12-06-zum-portal-core-js/35.png)

typescript lint와 vue lint를 추가해놨습니다. 빠른 시일 내에 모든 프로젝트에 이 lint 설정을 적용하는 것이 목표입니다.

### (5) 빌드 시간 개선을 위한 작업

![36](/images/front/post/2021-12-06-zum-portal-core-js/36.png)

먼저 기존에 frontend와 backend를 한 개의 repository로 관리하던 것들을 mono repository로 분리하는 작업이 필요했습니다.

![37](/images/front/post/2021-12-06-zum-portal-core-js/37.png)

앞선 내용 처럼 기능별로 패키지를 분리해놔서, core package를 가져올 때 frontend 관련 package는 devDependency로 설치하고, backend pacakge는 proudction dependency로 설치하여 사용함으로 인하여 배포 시간을 많이 줄일 수 있게 되었습니다.

그리고 위에 보이는 폴더구조를 통해서 알 수 있듯이 기존에는 frontend 설정 파일과 backend 설정 파일이 뒤섞여 있어서 이 프로젝트에 대해 처음 보는 사람의 경우 무척 당황하는 상황이 벌어질 수 있었는데, 이러한 문제 또한 개선할 수 있었습니다.

다시 의존성에 관련된 내용으로 돌아오자면,

- `root`: yarn의 `workspace`를 통해서 모노레포로 구성했습니다.

```jsx
    {
      "name": "zum-service-finance-pc-front",
      "version": "1.0.15",
      "description": "...",
      "author": "...",
      "private": true,
    
      // domain에는 front와 back에서 사용하는 공용 타입을 모아놨습니다.
      "workspaces": [
        "domain",
        "backend",
        "frontend"
      ],
    
      // build를 실행하면 ts로된 domain을 build하고, backend로 이동해서 다시 build 합니다.
      "scripts": {
        "build": "cd domain && yarn build && cd ../backend && yarn build"
      }
    }
```

- `frontend`: 전부 devDependencies로 관리하고 있습니다.

  ![38](/images/front/post/2021-12-06-zum-portal-core-js/38.png)

- `backend`: 전부 production dependencies로 관리하고 있습니다.

  ![39](/images/front/post/2021-12-06-zum-portal-core-js/39.png)


그리고 이 프로젝트를 배포할 때는 다음과 같은 내용의 Dockerfile을 이용하여 container 환경을 구성합니다.

```bash
##################################################################
#
#                도커라이징을 위한 설정 파일
#
# https://docs.google.com/document/d/1tk5TVgnPvM2i5rUWY_X_mcXc4f8-QIkOvPkchWhgMJA/edit
##################################################################

# Node.js 설치된 도커 컨테이너 획득
FROM node:14-slim

# 타임존 설정
ENV LANG=en_US.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# docker 디렉토리 생성 및 이동
RUN mkdir -p /data/www/app
WORKDIR /data/www/app

# 소스 복사
COPY . .

# 의존성 설치 및 빌드
## root에서 모노레포로 구성된 전체 패키지를 모두 설치합니다.
## 이 때 devDependencies는 설치하지 않도록 하려면 `--prod` 플래그를 붙이면 됩니다.
**RUN yarn install --frozen-lockfile --prod**

RUN yarn build

# 포트 개방. main.ts 파일의 포트와 일치하는지 확인할것
EXPOSE 8080

# backend 실행
WORKDIR ./backend
CMD yarn start
```

위에서 제일 중요한 부분은

```bash
# 의존성 설치 및 빌드
## root에서 모노레포로 구성된 전체 패키지를 모두 설치합니다.
## 이 때 devDependencies는 설치하지 않도록 하려면 `--prod` 플래그를 붙이면 됩니다.
**RUN yarn install --frozen-lockfile --prod**
```

이러게 install을 할 때 devDepedencies를 제외하는 것입니다. 추가로, `frozen-lockfile` 플래그의 경우 `yarn.lock` 을 기반으로 설치하기 때문에 설치 시간을 더욱 단축시켜줍니다.

- 참고링크
  - [yarn install](https://classic.yarnpkg.com/en/docs/cli/install/#toc-yarn-install)
  - [yarn install —production](https://classic.yarnpkg.com/en/docs/cli/install/#toc-yarn-install-production-true-false)

제일 중요한 부분인데, **배포하기전에 frontend에서 CSR build, SSR build를 실행하여 git에 반영해놔야 합니다.** 에초에 배포할 때 frontend 패키지가 필요한 이유는, **build를 위해서**입니다. build를 미리 해놓고 git에 올려놓는다면 frontend pacakge 자체가 불필요해집니다.

![40](/images/front/post/2021-12-06-zum-portal-core-js/40.png)

결과적으로 전체 배포시간을 3~4분 정도로 단축시킬 수 있게 되었습니다.

## 5. 앞으로의 핵심 과제

앞선 과정 처럼 지속적으로 core package를 개선하는 중입니다. 그리고 아직도 개선할 부분이 무척 많이 있습니다. 현재 생각중인 과제는 다음과 같습니다.

### (1) commonjs → <typescript + webpack> for esmodule

FE에서는 지금 commonjs 모듈을 사용하고 있습니다. 이를 typescript + webpack 으로 작업하여 build하여 제공할 수 있도록 개선하고자 생각중입니다.

그리고 아예 frontend의 config 설정과 utils를 분리하여 작업할 예정입니다. 설정파일만 필요한 프로젝트도 있을 것이고, 다양한 유틸리티 라이브러리가 필요한 프로젝트도 있을 것입니다. 그리고 Node.js를 사용하지 않는 환경(가령 어드민)에서도 코어 패키지를 사용해야 하기 때문입니다.

### (2) 문서화

기능만 계속 덕지덕지 붙이고 있고 문서화를 제대로 해놓지 않은 상황입니다. NestJS를 도입하기 전까지는 사용자가 알아야할 기능들이 무척 많았는데, 오히려 NestJS를 도입하니까 공식문서가 따로 있기 때문에 계속 미루는 중입니다. 이번 달 중으로 문서를 정리할 예정입니다.

### (3) Github 공개하기

제일 큰 과제는 바로 github에 공개하는 것입니다. 내부에서만 관리하다보니 코드를 대충 작성할 때도 생각보다 많았고, 테스트를 아예 고려하지 않는 등 무척 부끄러운 과정이 많았습니다.

줌인터넷의 프론트엔드 파트가 하는 일을 외부에 알리기도 하고, 코드의 퀄리티를 높이고 조금 더 신중하게 작성하기 위해 Github에 공개하는 것을 최종 목표로 하고 있습니다.

## 마치며

미루고 미루던 내용을 드디어 작성하게 되었네요. 무엇보다 외부에 줌인터넷의 프론트엔드 개발자들이 무엇을 하는지 알리는 것이 제일 큰 목적입니다. 1년도 안 된 신설 파트여서 부족한 부분이 많지만, 부족한 부분을 인지하고 지속적으로 개선하고자 노력중입니다 💪

github에 공개하면 다시 한 번 잘 다듬어서 소개해볼 예정입니다.

긴 글 읽어주셔서 감사합니다!