---
layout: post
title: NestJS Custom Caching Decorator 만들기
description: NestJS 서비스 로직에 Caching Decorator를 적용하기 위한 삽질 과정을 다루고 있습니다. 
image: /images/front/post/2021-11-11-nestjs-custom-decorator/thumbnail.jpg
introduction: NestJS 서비스 로직에 Caching Decorator를 적용하기 위해 공식문서와 오픈소스를 분석하고 삽질하는 과정을 다룹니다. 
category: portal/tech
tag: [프론트엔드, NestJS, Decorator, Cron, Cache, Custom Decorator]
author: junilhwang
---


<p style="text-align: right">
  <img style="margin: 0; display: inline-block;" src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fzuminternet.github.io%2Fnestjs-custom-decorator%2F&count_bg=%230099FF&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=%EC%A1%B0%ED%9A%8C%EC%88%98&edge_flat=true" alt="조회수" />
</p>

> 본 포스트는 NestJS에 호환 되는 Chaching Decorator 를 만들기 위한 삽질 과정을 담고 있습니다.

안녕하세요! 약 한 달 만에 기술블로그에 투고를 합니다.
조금 더 자주 해야 할텐데.. 글쓰기는 항상 어렵네요 😭

줌인터넷 프론트엔드 파트는 프론트 서버에서 [NestJS](https://nestjs.com/)를 사용합니다.
정확히는 NestJS를 이용하여 `Backend Core Package`를 별도로 구성하여 사용하고 있습니다.
이에 대한 내용은 다음에 제대로 다루도록 하고,
최근에 NestJS의 컨테이너에서 작동하는 `Custom Decorator`를 만들었는데 **이건 꼭 공유해야겠다**고 생각하여 최대한 빠르게 글을 작성하게 되었습니다.

## 0. 불편함을 감지하기

처음에 언급한 것 처럼, 팀 내에서 2020년 초에 자체적으로 express.js를 이용하여 `zum-portal-core-js`를 만들어서 사용했습니다.

> **[모바일 줌 SpringBoot → NodeJS 전환기 (feat. VueJS SSR)](https://zuminternet.github.io/ZUM-Mobile-NodeJS/)**
> - 기존에 SpringBoot로 구축된 서비스를 NodeJS로 전환하면서 만들게된 `zum-portal-core-js` 입니다.
> - Typescript와 Decorator의 조합으로 Spring의 Singleton Container와 Annotation을 사용하는 것 처럼 만들었습니다.

이 때 만들었던 기능 중에 제일 핵심적인 기능이 바로 `Caching Decorator` 입니다.
아무래도 포털이라는 서비스 특성상 Cache를 무척 많은 곳에서 사용했고,
사실상 **사용자가 조회하는 대부분의 데이터가 Caching된 데이터**였습니다.

### (1) 기존의 캐싱 로직

기존의 Caching Decorator는 다음과 같이 사용되었습니다.

```typescript
/**
 * 1. 30초 간격으로 메소드를 실행합니다. (cron schedule 사용)
 * 2. 실행 결과가 unless의 함수를 통과하면 캐싱됩니다.
 * 3. 어플리케이션이 초기화 될 때 실행됩니다.
 * 4. 이 메소드를 호출하면, 캐싱된 값을 반환합니다.
 */
@Caching({
  refreshCron: '0/30 * * * * *',
  runOnStart: true,
  unless: (result) => !result
})
public async getCommonResponse(): Promise<CommonData> {
  try {
    // 내부 망에서 사용하는 API를 호출하여 결과값을 반환합니다.
    const { data } = await this.adapter.get<CommonData>({
      url: this.internalApi.common.url,
      version: this.internalApi.common.version,
      stub: ResourceLoader(`stub/api/common/common_data.js`),
      typePredicate: value => !!value.gnbRoutes
    });
    return data;
  } catch (e) {
    logger.error(`There is an error when fetching mobile zum common data. `, e);
  }
}
```

주석에 설명한 것 처럼, 어플리케이션이 시작되면 Caching Decorator가 씌워진 메소드들은 한 번 실행 후 결과값을 캐싱합니다. 그리고 해당 메소드를 직접 코드상에서 호출할 경우 캐싱된 데이터를 반환하는 방식입니다.

**이를 날것의 express router 코드로 표현**하자면 다음과 같습니다.

```jsx
const cached = {};
const COMMON_DATA_KEY = 'COMMON_DATA_KEY';

function getCommonData () { /* 데이터를 가져옴 */ }
function refreshCommonData () {
  const data = getCommonData();
  if (!data) return;
  cached[COMMON_DATA_KEY] = data;
}

// 어플리케이션이 실행되자 서비스 로직을 실행하고 캐싱하여 저장함
refreshCommonData();

// 여담으로 이렇게 사용할 경우 cron expression과는 많이 다음
// setInterval의 경우 어플리케이션이 시작된 다음 부터 30초 간격으로 실행하는 것이고
// cron은 정각을 기준으로 실행함.
// 예를 들자면, 00:00:00, 00:00:30, 00:01:00 처럼 실제 시간을 기반으로 실행
setInterval(refreshCommonData, 1000 * 30);

app.get('/api/commonData', (req, res) => {
  res.send(cached[COMMON_DATA_KEY]); 
});
```

지금은 한 개의 서비스 로직에 대해 표현했지만, 만약에 서비스 로직이 무척 많다고 생각하면 위의 코드를 사용할 때 유지보수하기가 무척 힘들 것입니다.
**그래서 Caching Decorator를 만들어 사용함으로 인하여 유지보수 비용도 줄어들고, 손쉽게 캐싱 로직을 적용**할 수 있었습니다.

### (2) NestJS 도입

처음에는 가볍게 사용할 목적으로 코어 라이브러리를 만들었는데, **어느 순간 여러가지 기능이 계속해서 추가** 되고 있었습니다.
이럴 경우 오히려 **코어 라이브러리 때문에 유지보수 하기 힘든 경우**가 생길 수 있고,
제일 큰 문제는 코어 라이브러리 때문에 **예상하지 못한 구간에서 장애가 발생**하기도 했습니다.

그래서 관리 비용을 더욱 줄이기 위한 고민을 하다가 [NestJS](https://nestjs.com/) 도입을 결정하였습니다.

> NestJS는 효율적이고 안정적이며 확장 가능한 서버 측 애플리케이션을 구축하기 위한 점진적인 Node.js 프레임워크입니다.

NestJS의 경우 이미 잘 알려지고 많이 사용 되고 있는 **객체지향 + 싱글톤 컨테이너 기반의 NodeJS Framework** 였기 때문에 기존의 코어를 대체하기가 좋았습니다.



### (3) 변경된 캐싱 로직

NestJS를 사용하는 것은 좋았으나 기존에 만들어 두었던 Caching Decorator와 유사한 기능이 없었습니다.
대신에 NestJS 공식 문서에 있는 `Cache`와 `Schedule`을 이용하여 다음과 같이 수동으로 메소드를 하나 하나 작업해줘야 했습니다.

```typescript
@Injectable()
export class HomeDataService {
  // 의존성 주입
  constructor(
    // Provider(싱글톤 instance)에서 캐시를 사용하기 위해선
    // 이렇게 cacheManager를 주입하여 사용해야 합니다.
    @Inject(CACHE_MANAGER)
    private readonly cacheManager: Cache,
  ) {
    // 생성 시점에 직접 메소드 실행합니다.
    // 기존 Caching 데코레이터의 `runOnStart` 옵션의 기능입니다.
    this.refreshHomeData();
  }

  // 특정 API를 호출하는 서비스 로직
  // private method로 구성됨.
  private async _fetchHomeData(): Promise<HomeDataResponse | null> {
    try {
      const { data } = await adapter.get<HomeDataResponse>({ url: "..." });
      return data;
    } catch (e) {
      console.error(`메인페이지 데이터를 가져오는 과정에서 오류가 발생했습니다.`, e);
      return null;
    }
  }

  // 외부에서는 캐싱된 데이터를 사용함
  public fetchHomeData(): Promise<HomeDataResponse | null> {
    return this.cacheManager.get(CACHE_HOME_DATA);
  }

  // 30초마다 데이터를 갱신함
  @Cron("*/30 * * * * *")
  public async refreshHomeData() {
    const data = await this._fetchHomeData();
    if (!data) return;
    this.cacheManager.set(CACHE_HOME_DATA, data, {ttl: Infinity});
  }

}
```

위의 코드 처럼 무척 번거로운 과정을 거치게 됩니다.
서비스 로직이 많이 없다면 크게 문제되지 않겠지만,
**문제는 이런 메소드가 거의 50개 정도 되는 상황이었습니다.**

그래서 이를 꼭 개선하자고 다짐하였고, NestJS Container 기반의 `ZumCache Decorator`를 만들게 되었습니다.

## 1. 기존 패키지

일단 NestJS에서 제공하는 Cache Decorator를 분석해봤습니다.

### (1) NestJS Cache

원래 NestJS의 `Cache Decorator`는 `Provider(Singleton Instance) Layer` 보단 `Controller Layer`에서 사용하는 것을 목적으로 염두해두고 만들어졌습니다. [공식문서](https://docs.nestjs.com/techniques/caching)에 있는 내용을 살펴보면 다음과 같습니다.

먼저 `cache-manager`를 설치해야 합니다.

```bash
> npm install cache-manager
> npm install -D @types/cache-manager
```

캐시를 적용할 모듈에 Cache를 등록합니다.

```typescript
import { CacheModule, Module } from '@nestjs/common';
import { AppController } from './app.controller';

@Module({
  imports: [CacheModule.register()],
  controllers: [AppController],
})
export class AppModule {}
```

다음과 같이 사용할 수 있습니다.

```typescript
@Controller()
@UseInterceptors(CacheInterceptor)
export class AppController {
  @Get()
  findAll(): string[] {
    return [];
  }

  @CacheKey('custom_key')
  @CacheTTL(20)
  findAll2(): string[] {
    return [];
  }
}
```

- 기본적으로 **Request URL을 기반으로 캐싱**합니다.
- Request URL 대신 `CacheKey`를 이용하여 별도의 Key 값을 지정할 수 있습니다.
- `CacheTTL`을 이용하여 **캐시의 유효시간**을 설정할 수 있습니다.

사실 컨트롤러 레이어에서만 캐시를 사용한다면 이렇게 만들어도 큰 문제는 없습니다. 다만 **복잡한 서비스 로직에서는 각각의 서비스 로직에 대해 캐시를 적용해야 효과적**입니다.

- **한 개의 endpoint에 여러 개의 서비스 로직**이 적용될 수 있습니다.
- 각각의 서비스 로직에 대해 캐싱을 해야 응답 속도를 최소한으로 줄일 수 있습니다.

NestJS는 서비스 로직에서 캐시를 사용해야 하는 경우, `cacheManager`를 주입하여 직접 서비스 로직에 코드를 작성해야 합니다.

```typescript
@Injectable()
export class DataService {
  constructor(
    // 의존성 주입
    @Inject(CACHE_MANAGER) private readonly cacheManager: Cache,
  ) {}

  public async fetchNews({
    category,
    date,
    page = 1
  }): Promise<HomeCategoryNewsResponse> {
    try {
      const url = "...";
      const params = { category, date, page };
      
      // 캐싱된 데이터가 있을 경우, 해당 데이터를 반환
      const cacheKey = `DataService.fetchNews(${JSON.stringify(params)})`;
      const cachedData = await cacheManager.get(cacheKey);
      if (cachedData) return cachedData;

      // 캐싱된 데이터가 없을 경우, 데이터를 가져온 후, 캐싱을 한 다음에 반환
      const {data} = await adapter.get<HomeCategoryNewsResponse>({ url, params });
      cacheManager.set(cachedData, data, {
        ttl: 60 // 캐시 유효기간을 60초로 설정
      });
      return data;
    } catch (e) {
      console.error(`데이터를 가져오는 과정에서 오류가 발생했습니다.`, e);
      return null;
    }
  }
}
```

단순한 캐싱 작업도 앞선 코드의 내용 처럼 무척 손이 많이 가는 상황입니다.

### (2) NestJS Schedule

[공식문서(Task Scheduling)](https://docs.nestjs.com/techniques/task-scheduling)에 나와있는 내용은 다음과 같습니다.

먼저 `@nestjs/schedule` 과 `@types/cron`을 설치해야 합니다.

```bash
> npm install --save @nestjs/schedule
> npm install --save-dev @types/cron
```

그리고 `전역 모듈`로 등록하여 사용할 수 있습니다.

```typescript
import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';

@Module({
  imports: [
    // ScheduleModule은 기본적으로 전역 모듈로 사용됩니다.
    ScheduleModule.forRoot()
  ],
})
export class AppModule {}
```

cron, timeout, interval 등 다양한 기능이 있지만, 우리에게 필요한 것은 오직 cron이기 때문에 이에 대한 내용만 살펴보자면

```typescript
import { Injectable, Logger } from '@nestjs/common';
import { Cron } from '@nestjs/schedule';

@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  @Cron('45 * * * * *')
  handleCron() {
    this.logger.debug('Called when the current second is 45');
  }
}
```

- 생성자에서 별도의 의존성(Provider)을 주입할 필요가 없습니다.
- Provider의 메소드에 Decorator를 붙여서 사용할 수 있습니다.
- **void type의 메소드에게 적합한 형태**라고 볼 수 있습니다.

## 2. ZunCache 설계

앞선 내용을 토대로 어떤 식으로 Decorator를 만들지 생각해봤습니다. 
일단 Decorator의 이름은 `ZumCache` 라고 정의하였습니다.

### (1) Cache

```typescript
@ZumCache({
  ttl: 60,
  validate: value => Boolean(value), // 단순하게 Boolean을 넘겨도 됨
  logger: console.log, // 로깅에 사용될 함수
})
public async fetchNews({
    category,
    date,
    page = 1
}): Promise<HomeCategoryNewsResponse> {
  try {
    const url = "...";
    const params = { category, date, page };
    const {data} = await adapter.get<HomeCategoryNewsResponse>({ url, params });
    return data;
  } catch (e) {
    console.error(`데이터를 가져오는 과정에서 오류가 발생했습니다.`, e);
    return null;
  }
}
```

- 먼저 `cacheManager` 라는 Provider를 주입하지 않아도 되도록 만들 것입니다.
- `CacheKey`가 **자동으로 지정**됩니다.
  - 메소드의 매개변수가 없다면, `ClassName.MethodName` 처럼 key 값이 지정되고
  - 매개변수가 있다면 `ClassName.MethodName(JSON.stringify(params))` 처럼 key 값이 지정됩니다.
- 혹은 `key`라는 옵션을 통해서 **고정된 문자열**로 CacheKey를 지정할 수 있습니다.

```typescript
@ZumCache({ ttl: 60, key: "FETCH_NEWS" })
public async fetchNews(): Promise<HomeCategoryNewsResponse> { /* 생략 */ }
```

- `validate`를 통과해야 캐싱됩니다.
- `로깅`에 필요한 함수를 주입할 수 있습니다.

### (2) Schedule(Cron)

기존의 `@nestjs/schedule`의 cron은 실행된 메소드의 값을 저장하고 캐싱하는 기능이 없습니다.
즉, 오직 주기적으로 메소드를 실행하는 것이 목적입니다.
하지만 `ZumCache`는 **메소드를 주기적으로 실행하고, 결과값을 캐싱하여 저장하는 것**을 목적으로 합니다.

```typescript
@ZumCache({
  cron: "45 * * * * *",
  validate: value => Boolean(value), // 단순하게 Boolean을 넘겨도 됨
  logger: console.log, // 로깅에 사용될 함수
})
public async fetchCommonData(): Promise<HomeCommonResponse> {
  try {
    const url = "...";
    const {data} = await adapter.get<HomeCommonResponse>({ url });
    return data;
  } catch (e) {
    console.error(`데이터를 가져오는 과정에서 오류가 발생했습니다.`, e);
    return null;
  }
}
```

- 별도의 의존성을 주입하지 않아도 됩니다.
- **return된 값이 자동으로 캐싱**됩니다.
  - cron의 경우 매개변수가 따로 없기 때문에 `ClassName.MethodName` 형태의 key 값을 가집니다.
- `validate`를 통과해야 캐싱됩니다.
- `로깅`에 필요한 함수를 주입할 수 있습니다.

이제 어떻게 만들지 정의했으니, 구현을 해야합니다.

## 3. 근본적인 문제 분석

### (1) Decorator가 실행되는 시점

일단 Decorator가 정확히 어떤 시점에 실행되는지 알아야합니다.
이를 위해 간단하게 코드를 작성해서 확인해보면 될 것 같습니다.

> `Method Decorator`에 대한 내용은 [이 문서](https://www.typescriptlang.org/docs/handbook/decorators.html#method-decorators)를 참고해주세요


**Decorator는 보통 class가 초기화되는 시점에 실행되며,**
`descriptor`를 이용해 instance의 method를 참조할 수 있게 됩니다.

즉, method가 실행되는 시점이 아닌 method가 **정의 되는 시점에 관여**할 수 있는 것입니다.

```typescript
// 기본적으로 3개의 파라미터를 받습니다.
function methodDecorator (
  target, // instance
  property, // method의 이름
  descriptor, // method의 descriptor
) {
  console.log("methodDecorator", descriptor); // [3]
}

function methodDecorator2 (..args) {
  console.log("args", args) // [1]
  return (target, property, descriptor) => {
    console.log("methodDecorator2", descriptor); // [2]
  }
}

class Foo {
  @methodDecorator
  @methodDecorator2("abc", [1,2,3], { key: 'value' })
  public bar () {
    console.log('test'); // [4]
  } 
}

// [1] ~ [3]은 instance가 만들어지지 않아도 실행되며
// instance를 만든 후, 메소드를 실행해야 [4]가 출력됨
new Foo().bar();
```

![1](/images/front/post/2021-11-11-nestjs-custom-decorator/1.png)

- 주석에도 언급했지만, `[1]` ~ `[3]`의 경우 **class가 선언되는 시점**에 실행됩니다.
- `[4]`의 경우, instance가 만들어지고, 메소드까지 실행해야 출력됩니다.

따라서 Decorator를 이용하여 메소드의 내용에 관여하려면 결국 **NestJS에서 관리되고 있는 Singleton Container에 접근할 수 있는 방법**을 알아야 합니다.

### (2) 빈약한 공식 문서

앞서 언급한 것 처럼 NestJS에서 Singleton Container에 접근하는 방법을 알아내기 위해 **공식문서를 모두 훑어봤지만 어디에도 이에 대한 내용을 다루고 있지 않고 있습니다.**

[NestJS Custom Decorator 문서](https://docs.nestjs.com/custom-decorators)의 경우 모두 **Controller Layer에 사용되는 Decorator에 대한 내용** 뿐이었습니다.

```typescript
// 기본적으로 제공해주는 Decorator 함수가 Controller 기반 입니다.
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

// Controller에 붙여서 사용될 Param Decorator를 정의합니다.
export const User = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;

    return data ? user?.[data] : user;
  },
);
```
위의 코드 처럼, Request 값에 관여하는 Decorator를 만드는 내용이 전부입니다 🤦‍♂️.
그래서 어떻게 구현해야 좋을지 막막했습니다.

😭😭😭😭😭😭😱😱😱😱😱😱


## 4. NestJS Schedule 코드 분석

그럼 대체 어떻게 컨테이너에 접근할 수 있을까 고민하다가, `@Cron` 데코레이터가 생각났습니다.
아마 공식문서에 유일하게(?) 나와 있는, **Provider 단에서 사용되는 Decorator**가 아닌가 싶습니다.

```typescript
@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  @Cron('45 * * * * *')
  handleCron() {
    this.logger.debug('Called when the current second is 45');
  }
}
```

결국 이 Decorator가 정상적으로 작동하기 위해서는, **NestJS의 Container에 접근할 수 있어야 합니다.**

그래서 [Github Repository(@nestjs/schedule)](https://github.com/nestjs/schedule) 에 들어가서 직접 코드를 확인했습니다.

### (1) Cron Decorator

먼저 `Cron Decorator` 코드는 다음과 같습니다.

**[cron.decorator.ts](https://github.com/nestjs/schedule/blob/master/lib/decorators/cron.decorator.ts)**

```typescript
import { applyDecorators, SetMetadata } from '@nestjs/common';
import { SchedulerType } from '../enums/scheduler-type.enum';
import {
  SCHEDULER_NAME,
  SCHEDULER_TYPE,
  SCHEDULE_CRON_OPTIONS,
} from '../schedule.constants';

// Decorator에서 받아올 Options를 정의합니다.
export interface CronOptions {
  name?: string;
  timeZone?: string;
  utcOffset?: string | number;
  unrefTimeout?: boolean;
}

// 데코레이터 함수를 정의합니다.
export function Cron(
  cronTime: string | Date,
  options: CronOptions = {},
): MethodDecorator {
  const name = options && options.name;
  
  // applyDecorators로 여러 개의 Decorator를 한 번에 적용할 수 있습니다.
  return applyDecorators(
    SetMetadata(SCHEDULE_CRON_OPTIONS, {
      ...options,
      cronTime,
    }),
    SetMetadata(SCHEDULER_NAME, name),
    SetMetadata(SCHEDULER_TYPE, SchedulerType.CRON),
  );
}
```

- applyDecorators는 Decorator를 조합해주는 역할을 합니다.
- [SetMetadata](https://github.com/nestjs/nest/blob/master/packages/common/decorators/core/set-metadata.decorator.ts)는 instance의 method에 대한 metatadata를 등록하고, instance를 반환해주는 `Decorator function` 입니다.

이 코드에서는 딱 봐도 **Container에 접근하는 부분은 없는 것**을 확인할 수 있습니다.

### (2) Schedule Module

그래서 `module`쪽 코드를 살펴봤더니 눈에 띄는 부분이 있었습니다.

**[schedule.module.ts](https://github.com/nestjs/schedule/blob/master/lib/schedule.module.ts)**

```typescript
import { DynamicModule, Module } from '@nestjs/common';
import { DiscoveryModule } from '@nestjs/core';
import { SchedulerMetadataAccessor } from './schedule-metadata.accessor';
import { ScheduleExplorer } from './schedule.explorer';
import { SchedulerOrchestrator } from './scheduler.orchestrator';
import { SchedulerRegistry } from './scheduler.registry';

@Module({
  // @nestjs/core에서 제공해주는 모듈을 주입하고 있습니다.
  imports: [DiscoveryModule],
  providers: [SchedulerMetadataAccessor, SchedulerOrchestrator],
})
export class ScheduleModule {
  static forRoot(): DynamicModule {
    return {
      global: true,
      module: ScheduleModule,
      providers: [ScheduleExplorer, SchedulerRegistry],
      exports: [SchedulerRegistry],
    };
  }
}
```

위의 코드에서 주목해야 할 부분은 바로 `DiscoveryModule` 입니다.
주석에 언급한 것 처럼 `@nestjs/core` 에서 제공하고 있는 `Module`입니다.
뭔가 있어보이지 않나요?

### (3) DiscoveryModule

해당 Module의 코드는 다음과 같습니다.

**[discovery-moduels.ts](https://github.com/nestjs/nest/blob/master/packages/core/discovery/discovery-module.ts)**

```typescript
import { Module } from '@nestjs/common';
import { MetadataScanner } from '../metadata-scanner';
import { DiscoveryService } from './discovery-service';

@Module({
  providers: [MetadataScanner, DiscoveryService],
  exports: [MetadataScanner, DiscoveryService],
})
export class DiscoveryModule {}
```

뭔가 딱 봐도 **Container에 접근할 수 있을 것 같은 느낌**이 들지 않나요?

`DiscoveryService`를 확인해보면 다음과 같습니다.

**[discover-service.ts](https://github.com/nestjs/nest/blob/master/packages/core/discovery/discovery-service.ts)**

```typescript
import { flatten, Injectable } from '@nestjs/common';
import { InstanceWrapper } from '../injector/instance-wrapper';
import { Module } from '../injector/module';
import { ModulesContainer } from '../injector/modules-container';

export interface DiscoveryOptions {
  include?: Function[];
}

@Injectable()
export class DiscoveryService {
  constructor(private readonly modulesContainer: ModulesContainer) {}

  getProviders(
    options: DiscoveryOptions = {},
    modules: Module[] = this.getModules(options),
  ): InstanceWrapper[] { /* 생략 */ }

  getControllers(
    options: DiscoveryOptions = {},
    modules: Module[] = this.getModules(options),
  ): InstanceWrapper[] { /* 생략 */ }

  protected getModules(options: DiscoveryOptions = {}): Module[] { /* 생략 */ }
  private includeWhitelisted(include: Function[]): Module[] { /* 생략 */ }
}
```

메소드 이름만 봐도 container에 있는 `controller`와 `provider(singleton instance)`를 **가져올 수 있는 것**을 알 수 있습니다.

실제로 `@nestjs/schedule`에 있는 **[schedule.explorer.ts](https://github.com/nestjs/schedule/blob/master/lib/schedule.explorer.ts)**에서 다음과 같이 활용되고 있습니다.

```typescript
import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { DiscoveryService } from '@nestjs/core';
import { InstanceWrapper } from '@nestjs/core/injector/instance-wrapper';
import { MetadataScanner } from '@nestjs/core/metadata-scanner';
import { SchedulerType } from './enums/scheduler-type.enum';
import { SchedulerMetadataAccessor } from './schedule-metadata.accessor';
import { SchedulerOrchestrator } from './scheduler.orchestrator';

@Injectable()
export class ScheduleExplorer implements OnModuleInit {
  private readonly logger = new Logger('Scheduler');

  constructor(
    private readonly schedulerOrchestrator: SchedulerOrchestrator,
    private readonly discoveryService: DiscoveryService,
    private readonly metadataAccessor: SchedulerMetadataAccessor,
    private readonly metadataScanner: MetadataScanner,
  ) {}

  // 모듈 초기화 되는 시점에 실행됩니다.
  onModuleInit() {
    this.explore();
  }

  explore() {
    // container에 있는 모든 instance를 가져옵니다.
    const instanceWrappers: InstanceWrapper[] = [
      ...this.discoveryService.getControllers(),
      ...this.discoveryService.getProviders(),
    ];

    // Cron, Interval, Timeout 등의 Decorator가 사용된 method에 대해 Task를 등록합니다.
    instanceWrappers
      .filter((wrapper) => wrapper.isDependencyTreeStatic())
      .forEach((wrapper: InstanceWrapper) => {
        const { instance } = wrapper;
        if (!instance || !Object.getPrototypeOf(instance)) {
          return;
        }
        this.metadataScanner.scanFromPrototype(
          instance,
          Object.getPrototypeOf(instance),
          (key: string) => this.lookupSchedulers(instance, key),
        );
      });
  }

  lookupSchedulers(
    instance: Record<string, Function>,
    key: string
  ) { /* 생략*/ }

  private wrapFunctionInTryCatchBlocks(
    methodRef: Function,
    instance: object
  ) { /* 생략*/ }
}
```

### (5) 결론

위의 코드들을 통해 다음과 같은 결론을 도출할 수 있습니다.

- `OnModuleInit`이 실행되는 시점에 인스턴스에 접근해야 합니다.
  - `OnModuleInit`은 **호스트 모듈의 종속성이 해결되면 호출되는 NestJS의 Life cycle event** 입니다.
  - 참고링크: [https://docs.nestjs.com/fundamentals/lifecycle-events#lifecycle-events](https://docs.nestjs.com/fundamentals/lifecycle-events#lifecycle-events)
- `DiscoveryService`로 Singleton Container에 있는 `instance에 접근`할 수 있습니다.
- `MetadataScanner`로 decorator의 instance에 대한 `metadata`를 가져올 수 있습니다.
  - 즉, 앞에서 언급된 **SetMetadata로 등록된 값들을 조회**하는 것입니다.

이제 우리가 원하는 Decorator를 구현할 수 있을 것 같지 않나요?

## 5. 구현하기

### (1) Decorator

먼저 Decorator를 정의해야 합니다.

`**zum-cache.decorator.ts**`

```typescript
import { applyDecorators, SetMetadata } from "@nestjs/common";

// metadata에 대한 상수 정의
// core에서만 사용되고, app layer에서는 사용되지 않음
export const ZUM_CACHE_METADATA = 'ZUM_CACHE_METADATA';

// 옵션 정의
export interface ZumCacheOptions {
  // cron expression을 받아올수 있음.
  cron?: string;

  // key값을 받아올 수 있음
  key?: string;

    // cache의 유효 시간을 받아올 수 있음
  ttl?: number; 

    // 값에 대한 검증 함수를 받아올 수 있음
  validate?: (value: any) => boolean; 

    // 로깅에 필요한 함수를 받아올 수 있음
  logger?: Function 
}

// 데코레이터 함수 정의
export function ZumCache(
  options: ZumCacheOptions = {}
): MethodDecorator {
    // applyDecorators는 사용하지 않아도 됨
  // 데코레이터 체이닝에 대한 가능성을 염두에 두고 작업하였음
  return applyDecorators(
      // method에 대한 metadata를 정의함
    // 나중에 `MetadataScanner`를 통해서 값을 가져옴
    SetMetadata(ZUM_CACHE_METADATA, options),
  )
}
```

decorator의 parameter를 `MetadataScanner`를 통해서 받아올 수 있습니다. 이 부분은 module에서 자세히 확인할 수 있습니다.

### (2) 패키지 설치

이어서 cache-manager와 cron을 설치해야 합니다.

```bash
> npm install cache-manager cron
> npm install -D @types/cache-manager @types/cron
```

### (3) Module

그리고 해당 Decorator를 이용하여 캐싱 로직을 등록해주는 Module을 만들어야 합니다.

**`zum-cache.module.ts`**

```typescript
import { DiscoveryModule, DiscoveryService, MetadataScanner, Reflector } from "@nestjs/core";
import { CACHE_MANAGER, CacheModule, DynamicModule, Inject, Module, OnModuleInit } from "@nestjs/common";
import { Cache } from "cache-manager";
import { CronJob } from "cron";
import { ZUM_CACHE_METADATA, ZumCacheOptions } from "./zum-cache.decorator";

@Module({
  imports: [
    // Container에 접근하기 위해 DiscoveryModule을 주입합니다.
    DiscoveryModule,

    // cache를 사용하기 위해 CacheModule을 주입합니다.
    CacheModule.register(),
  ],
})

// OnModuleInit Lifecycle event에 사용될 Hook을 만들어줍니다.
export class ZumCacheModule implements OnModuleInit {

  constructor(
    // DiscoveryModule을 불러와야 DiscoveryService와 MetadataScanner을 주입할 수 있습니다.
    private readonly discovery: DiscoveryService,
    private readonly scanner: MetadataScanner,

    // Reflector는 모든 모듈에서 접근할 수 있는 provider 입니다.
    private readonly reflector: Reflector,

    // cacheManager를 주입합니다.
    @Inject(CACHE_MANAGER) private readonly cacheManager: Cache,
  ) {}

  // 전역 모듈로 등록하기 위한 static method 입니다.
  // 참고링크: https://docs.nestjs.com/modules#dynamic-modules
  static forRoot(): DynamicModule {
    return {
      module: ZumCacheModule,
      global: true
    }
  }

  // OnModuleInit event에 이 메소드를 실행합니다.
  onModuleInit() {
    // getProviders를 통해서 모든 singleton instance를 가져옵니다.
    this.discovery.getProviders()
        .filter(wrapper => wrapper.isDependencyTreeStatic())
        .filter(({ instance }) => instance && Object.getPrototypeOf(instance))
        .forEach(({ instance }) => {
          
        // 모든 Provider instance의 method를 순회합니다.
        this.scanner.scanFromPrototype(
          instance,
          Object.getPrototypeOf(instance),

          // callback 함수에 instnace의 methodName을 전달합니다.
          // 아마 `Object.getPrototypeOf(instance)`의 메소드를 읽어들이는게 아닌가 싶습니다.
          methodName => {
            const metadata = reflector.get(ZUM_CACHE_METADATA, instance[methodName];
            if (!metadata) return;
            
            // 이렇게 console을 띄워보면, ZumCache Decorator가 사용된
            // method의 정보와, 해당 Decorator에 넘긴 metadata를 확인할 수 있습니다.
            console.log(methodName, instance[methodName], metadata);
          }
        );
      });
  }

}
```

> 일단 앞서 정의된 모듈만 AppModule에 주입하여 확인해보면 다음과 같이 출력 되는 것을 확인할 수 있습니다.
> `ZumCache Decorator`가 사용된 Method만 로그에 찍힙니다.
> ![2](/images/front/post/2021-11-11-nestjs-custom-decorator/2.png)

위와 같은 과정을 통해서

- instance
- method
- metadata

등 3가지의 정보에 접근할 수 있다는 것을 알았으니, 이제 원하는 작업을 진행할 수 있게 되었습니다.

`onModuleInit`에 모든 코드를 작성하는 것이 아니라, `registerAllCache` 메소드와 `registerCacheAndJob` 메소드를 만들어서 기능을 위임해야 합니다.

```typescript
onModuleInit() {
  this.registerAllCache();
}

// 별도의 메소드로 분리하고
registerAllCache() {
  this.discovery.getProviders()
      .filter((wrapper) => wrapper.isDependencyTreeStatic())
      .filter(({ instance }) => instance && Object.getPrototypeOf(instance))
      .forEach(({ instance }) => {
        this.scanner.scanFromPrototype(
          instance, 
          Object.getPrototypeOf(instance),

          // 콜백함수도 다음과 같이 분리합니다.
          this.registerCacheAndJob(instance)
        );
      });
}

// 함수를 반환하는 메소드로 정의하여 콜백을 처리할 수 있도록 합니다.
registerCacheAndJob(instance) {
  return methodName => {
    // 1. metadata를 가져오고
    // 2. metadata가 아예 없다면, 바로 함수를 종료합니다.
    // 3. 메소드에 캐시 로직을 끼워넣고
    // 4. cron이 있다면, job을 등록합니다.
  }
}
```

`registerCacheAndJob` 의 내용을 차근 차근 채워보도록 하겠습니다.

```typescript
registerCacheAndJob(instance: any) {
  // this에서 cacheManger와 reflector를 가져옵니다.
  // 불필요한 선언을 방지하기 위함입니다.
  const { cacheManager, reflector } = this;
  
  return methodName => {
    // 1. metadata를 가져오고
    const methodRef = instance[methodName];
    const metadata: ZumCacheOptions = reflector.get(ZUM_CACHE_NAME, methodRef);

    // 2. metadata가 아예 없다면, 바로 함수를 종료합니다.
    if (!metadata) return;

    // 3-1. metadata를 destructuring(구조해제할당) 하여 기본 값을 정의하고
    const {
      ttl = Infinity,
      cron,
      key: customKey,
      validate = Boolean,
      logger = () => null
    } = metadata;

    // 3-2. cacheKey를 정의합니다.
    const cacheKeyPrefix = `${instance.constructor.name}.${methodName}`;
    
    // 3-3. ZumCache Decorator가 사용되는 메소드를 실행하는 함수를 정의합니다.
    const originMethod = (...args: unknown[]) => methodRef.call(instance, ...args);

    // 3. 메소드에 캐시로직을 끼워넣습니다.
    instance[methodName] = async (...args: unknown[]) => {
      // 먼저 캐시된 데이터를 가져오고
      const key = customKey   ? customKey :
                  args.length ? JSON.stringify(args) : null;
      const cacheKeySuffix = key ? `(${key})` : '';
      const cacheKey = cacheKeyPrefix + cacheKeySuffix;
      const cached = await cacheManager.get(cacheKey);

      logger({ cacheKey });

      // 캐시된 데이터가 있다면, 해당 데이터를 바로 반환합니다.
      if (Boolean(cached)) {
        logger({ cached });
        return cached;
      }

      // 캐시된 데이터가 없다면, 원본 메소드를 실행하여 값을 가져옵니다.
      const data = await originMethod(...args);

      // 검증 로직을 통과하지 못하면, 일단 에러를 발생시킵니다.
      if (!validate(data)) {
        // 이 부분은 별도의 작업이 필요합니다.
        // 나중에 retry 같은 작업을 추가할 생각입니다.
        throw new Error('cache error');
      }

      logger({ data });

      // 정상적인 data라면, 캐시를 한 다음에 반환합니다.
      // 따라서 이 메소드가 다시 실행될 때는 캐시된 데이터를 반환할 것입니다.
      await cacheManager.set(cacheKey, data, { ttl });
      return data;
    }

    // 4. cron이 있다면, job을 등록합니다.
    if (!cron) return;
    this.registerCron(
      cron,
      cacheKeyPrefix,
      originMethod,
      validate,
      logger
    );
  }
}

registerCron (
  cron: string,
  cacheKey: string,
  job: Function,
  validate: Function,
  logger: Function
) {
  // 1. job을 실행합니다.
  // 2. job의 결과를 검증합니다.
  // 3. 검증을 통과하면 job의 결과를 새로운 캐시 데이터로 등록합니다.
  // 4. 검증을 통과하지 못하면, 이전에 캐시된 데이터를 반환하고
  // 1 ~ 4 를 수행하는 CronJob을 만들고 실행합니다.
}
```

이제 `registerCron`을 구현해봅시다.

```typescript
registerCron(
  cron: string,
  cacheKey: string,
  job: Function,
  validate: Function,
  logger: Function
) {
  const { cacheManager } = this;
  const handleTick = async () => {
    // 0. 캐시 데이터를 미리 가져옵니다.
    const cached = await cacheManager.get(cacheKey);

    // 1. job을 실행합니다.
    const jobData = await job();
    logger({ cacheKey, jobData });

    // 2. job의 결과를 검증하고,
    // 3. 검증을 통과하면 해당 결과를 새로운 캐시 데이터로 갱신합니다.
    // 4. 검증을 통과하지 못하면, 이전에 캐시된 데이터를 그대로 사용합니다.
    const refreshedData = validate(jobData) ? jobData : cached;
    await cacheManager.set(cacheKey, refreshedData, {
      // cache의 유효기간을 무한대로 둡니다.
      // cron이 실행될 때 정상적인 값이라면 캐시 데이터가 갱신되기 때문입니다.
      ttl: Infinity
    });
  }

  // 1 ~ 4 를 수행하는 CronJob을 만들고 실행합니다.
  new CronJob(cron, handleTick).start();
  handleTick();
}
```

사실 만든지 얼마 안 된 코드라서 무척 지저분합니다. 앞으로 계속 개선해나갈 생각이랍니다!

## 6. 사용하기

앞서 정의한 `ZumCacheModule`과 `ZumCache Decorator`는 다음과 같이 사용할 수 있습니다.

### (1) Module 등록

**`app.module.ts`**

```typescript
import { ZumCacheModule } from "@zum-portal-core/backend";

@Module({
  imports: [ ZumCacheModule.forRoot() ],
})
export class AppModule {}
```

- **최상단 모듈**인 `AppModule`에 등록하여 사용할 수 있습니다.
- `ZumCacheModule`은 `global module`로 정의하였기 때문에 **하위 Module에서 다시 주입하여 사용할 필요가 없습니다.**

### (2) Decorator 사용

그리고 서비스 로직에서는 다음과 같이 사용하면 됩니다.

```typescript
// 결과값에 대한 캐싱을 사용할 경우
@ZumCache({
  ttl: 60,
  validate: value => Boolean(value), // 단순하게 Boolean을 넘겨도 됨
  logger: console.log, // 로깅에 사용될 함수
})
public async fetchNews({
  category,
  date,
  page = 1
}): Promise<HomeCategoryNewsResponse> {
  try {
    const url = "...";
    const params = { category, date, page };
    const {data} = await adapter.get<HomeCategoryNewsResponse>({ url, params });
    return data;
  } catch (e) {
    console.error(`데이터를 가져오는 과정에서 오류가 발생했습니다.`, e);
    return null;
  }
}

// 주기적으로 실행되는 결과값에 대해 캐싱을 사용할 경우
@ZumCache({
  cron: "45 * * * * *",
  validate: value => Boolean(value), // 단순하게 Boolean을 넘겨도 됨
  logger: console.log, // 로깅에 사용될 함수
})
public async fetchCommonData(): Promise<HomeCommonResponse> {
  try {
    const url = "...";
    const {data} = await adapter.get<HomeCommonResponse>({ url });
    return data;
  } catch (e) {
    console.error(`데이터를 가져오는 과정에서 오류가 발생했습니다.`, e);
    return null;
  }
}
```

이 외에도 다양한 삽질 과정이 있었지만, 핵심적인 내용만 최대한 간추려서 소개했습니다.

부디 NestJS를 이용할 때 조금이나마 도움이 되길 바라며, 글을 마무리합니다 🙇‍♂️

## Reference

- NestJS 공식문서
  - [Lifecycle Events](https://docs.nestjs.com/fundamentals/lifecycle-events)
  - [Caching](https://docs.nestjs.com/techniques/caching)
  - [Task scheduling](https://docs.nestjs.com/techniques/task-scheduling)
  - [Custom Decorators](https://docs.nestjs.com/custom-decorators)
  - [Dynamic Module](https://docs.nestjs.com/modules#dynamic-modules)
- `@nestjs/schedule`
  - [cron-decorator.ts](https://github.com/nestjs/schedule/blob/master/lib/decorators/cron.decorator.ts)
  - [schedule.module.ts](https://github.com/nestjs/schedule/blob/master/lib/schedule.module.ts)
  - [schedule.explorer.ts](https://github.com/nestjs/schedule/blob/master/lib/schedule.explorer.ts)
- `@nestjs/core`
  - [discovery-module.ts](https://github.com/nestjs/nest/blob/master/packages/core/discovery/discovery-module.ts)
  - [discovery-service.ts](https://github.com/nestjs/nest/blob/master/packages/core/discovery/discovery-service.ts)
- `@nestjs/common`
  - [set-metadata.decorator.ts](https://github.com/nestjs/nest/blob/master/packages/common/decorators/core/set-metadata.decorator.ts)