---
layout: post
title: Redirect 서버 리팩토링 - 파일럿 프로젝트
description: 파일럿 프로젝트로 진행하게 된 Redirect 서버의 리팩토링 및 시스템 개선 과정을 정리해보았습니다.
image: /images/portal/post/2023-02-14-redirect-refactoring/thumbnail.png
introduction: 파일럿 프로젝트로 진행하게 된 Redirect 서버의 리팩토링 및 시스템 개선 과정을 정리해보았습니다.
category: portal/tech
tag:  [Spring Boot, Spring Data JPA, Querydsl, Logback, EhCache, nginx]
author : parkje0927
---
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fzuminternet.github.io%2Fredirect-refactoring%2F&count_bg=%233060D3&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![thumbnail.png](/images/portal/post/2023-02-14-redirect-refactoring/thumbnail.png)

<br>

> 안녕하세요. 포털개발팀 포털백엔드 개발파트의 박정현(Kate) 입니다.     
파일럿 프로젝트로 URL 리다이렉트 서버 레거시 시스템 개선 및 AWS 로 이관하는 업무를 맡게 되어 관련 내용을 공유드리려고 합니다.
> 

<br>

## 목차
```text
1. 프로젝트 설명
1-1. Intro

2. 전체 구성도
2-1. AS-IS
2-2. TO-BE

3. 파일럿 프로젝트 진행(1) - 설계
3-1. 기술 스택
3-2. 개발 일정
3-3. 목표
3-4. 전체 기능 리스트 및 엔티티 구조

4. 파일럿 프로젝트 진행(2) - 클릭 요청 API
4-1. Cache
4-2. Log
4-3. push API 와 연동

5. 추가 기능 - Short URL 적용

6. 회고

7. 참고 블로그 및 문서
```

<br>

## 프로젝트 설명

### Intro

이번 파일럿 프로젝트 주제는 **redirect 서버 리팩토링 및 log 적재 과정 개선, Short URL 적용** 입니다.

프로젝트에 대한 설명을 드리기 전에 리다이렉트에 대한 개념을 먼저 정리해보려고 합니다. 

리다이렉트는 어떤 링크를 클릭하여 그 URL 로의 이동을 요청했을 때 다른 URL 을 지시하는 것을 의미합니다. 

예를 들어 브라우저 상에서 `www.example.com/page1` 로 웹 서버에게 요청을 보내면 서버는 `www.example.com/page2` 로 응답을 보내며 다른 URL 을 전달할 수 있습니다. 이후 브라우저는 서버로 받은 응답 상태 코드가 302 이면 헤더에 있는 URL 로 재요청을 보내게 되어 다른 URL 로 이동을 하게 되는데 이를 리다이렉트라고 합니다.

![image1.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image1.png)

<br>

위 내용을 기반으로 **redirect 서버**의 역할을 유추해볼 수 있습니다. [zum.com](http://zum.com) 메인 화면에서 쇼핑 정보를 보다가 클릭을 하게 되면 해당 쇼핑몰로 이동을 하게 되는데 여기서 기존 요청과 다른 URL 즉 리다이렉트 URL 을 전달해주는 것이 바로 redirect 서버의 역할입니다.

![image2-1.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image2-1.png)

<br>

![image2-2.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image2-2.png)

<br>

## 전체 구성도

### AS-IS

![image3.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image3.png)

저는 이번 프로젝트에서 이 redirect 서버를 리팩토링하는 것을 목표로 잡았습니다. 이유로는 먼저 기존 프로젝트가 <U>Spring 3 + java 6</U> 버전으로 진행된 프로젝트로 최근에 업데이트가 된 적이 없기 때문에 코드를 개선할 필요가 있었습니다. 

또한 redirect 서버가 하는 역할에는 리다이렉트 주소를 전달하는 것도 있지만, log 적재도 중요한 역할 중 하나였는데 log 가 저장이 되면 Fluentd 를 통해 log 를 수집하고 이를 빅데이터팀에서 분석을 하는 구조입니다. 이때 log 에 포함되어져 있는 값에는 요청 파라미터에 포함되어있는 METHOD 값이 존재하고 있습니다. 

<br>

> 💡 여기서 잠시 METHOD 값에 대한 설명을 드리겠습니다.   
이후 설명에서도 계속 나오는데 자바 메소드와 명칭이 헷갈리기 때문에 아래 내용에서는 ***METHOD 카테고리*** 라고 칭하도록 하겠습니다.  
METHOD 카테고리에 들어올 수 있는 값은 쇼핑이나 광고 등이 있습니다. 만약 쇼핑 METHOD 와 광고 METHOD 가 있다면 이는 각각 쇼핑 목록을 클릭해서 들어온 경우와 광고를 클릭해서 들어온 경우로 이해가 될 수 있습니다.  
만약 다른 곳에서도 이 API 를 사용하여 log 를 쌓고 싶다면 이런 카테고리값이 필요하겠죠?~~(뒤에 앱/웹 push 내용을 위한 예고입니다.)~~
>

<br>

기존에는 성공과 실패의 경우로만 나뉘어져 있어서 METHOD 카테고리에 따라 구분을 할 수가 없었습니다. 이를 개선하는 것도 중요한 요구사항이었기에 전체적인 리팩토링이 필요했습니다.

<br>

### TO-BE

그래서 위 요구사항들을 적용하여 제가 설계한 아키텍처는 다음과 같습니다.

![image4.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image4.png)

1. Spring Boot + Gradle 프로젝트로 재설계
2. log 적재시에 METHOD 카테고리별 구분을 추가
3. (이후 추가된 내용) 앱/웹 푸시를 보낼 때 메세지 내용에 포함되어 있는 URL 을 그대로 보내는 것이 아닌 redirect 서버에서 리다이렉트 URL 을 보내도록 처리 → 푸시 log 적재
4. (이후 추가된 내용) 공유하기 기능을 활용할 때 긴 URL 대신 Short URL 을 공유

1, 2번은 위에서도 설명을 드린 내용이지만 3, 4번은 설계 과정에서 추가된 내용이라 간단하게 설명 드린 후 본론으로 들어가도록 하겠습니다.

먼저 3번의 경우 링크 클릭 이후의 로직 처리와 관련이 있습니다. 기존 푸시를 보내게 되면 클릭 이후에 해당 뉴스나 컨텐츠로 이동을 해야하기 때문에 링크가 필수적으로 추가되어 있습니다. 이때 3번과 같이 링크 클릭과 관련하여 Redirect 서버와 통신이 필요하게 되어 해당 기능을 추가하게 되었습니다.

또한 4번의 경우 역시 링크와 관련된 기능인데 링크를 공유할 때 긴 URL 이 아닌 Short URL 이 공유된다고 가정할 때, 해당 URL 을 클릭하면 원래의 긴 URL 로 이동이 되어야 합니다. 이때 그 Short URL 을 클릭한 후 log 적재 및 로직 처리를 새롭게 설계한 redirect 서버에서 진행할 수 있을 것이라 판단되어 기능을 추가하게 되었습니다. 

<br>

> 💡 여기서 1, 2, 3번의 경우에는 가장 주요한 로직인 클릭 요청 API 를 중심으로 하여 Cache, log 그리고 푸시 API 와의 연동을 설명드리겠으며 4번의 경우는 추가로 진행한 것이기에 마지막에 따로 설명을 드리겠습니다.
>

<br>

## 파일럿 프로젝트 진행(1) - 설계

### 기술 스택

먼저, 사용한 기술 스택에 대한 정리입니다. Java 와 Spring Boot 버전과 관련하여 고민이 많았지만 팀 내 보일러 플레이트 프로젝트 기준으로 설계를 시작하게 되어 Java 11, Spring Boot 2.5.4 버전으로 맞추게 되었습니다. 

- 언어
    - Java 11
- 프레임워크
    - Spring Boot 2.5.4
- 라이브러리
    - Lombok
    - EhCache
    - Logback
    - REST Docs
- 프로젝트 환경
    - Gradle 7.5
    - Spring Data JPA
    - Querydsl
    - nginx
- 데이터베이스
    - MySQL 5

<br>

### 개발 일정

![image5.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image5.png)

약 한 달 반 정도의 기간 동안 프로젝트를 진행했는데, 한 달 동안 설계 및 구현을 한 이후에 REST Docs 적용 및 QA 서버 배포와 발표 자료 작성에 약 2주 정도의 시간을 사용했습니다.

<br>

### 목표

프로젝트를 진행 하기 전에 제가 정한 목표는 아래와 같습니다.

**1) 동일 설정보다 동일 기능**

처음에는 기존 프로젝트의 설정을 모두 그대로 유지해야한다고 생각했습니다. 그런데 설정값에는 Spring Boot 버전업이 되면서 삭제된 설정도 있었고, default 로 변경된 것들도 있어서 하나씩 확인하는데 어려움이 있었습니다. 하지만 설정보다는 동일 기능이 중요하다는 피드백을 받게 되었고 기존 프로젝트의 기능과 추가 요구사항을 같이 정리해가며 구현해가는 것을 목표로 잡게 되었습니다.

<br>

**2) 수정 및 기능 추가는 쉽게**

해당 프로젝트는 업데이트가 자주 일어나는 프로젝트는 아니었지만 이번 리팩토링을 통해 다양한 METHOD 카테고리로 log 가 쌓이도록 설계가 된다면 더 활용도가 높은 프로젝트가 될 수 있을 것이라고 생각했습니다.

기존에는 METHOD 카테고리 구분 없이 log 가 쌓이고 log 를 생성할 때 `getLog()` 메소드에서 log 를 만들어서 저장하고 있었습니다. 

```java
/**
 * 각 METHOD 카테고리별 Dto 클래스에서 log 를 생성하는 메소드가 존재합니다.
 * 그 중 하나를 예시로 가져온 것입니다.
 */
public String getLog() {
    LogStringBuilder builder = new LogStringBuilder();
    builder.appendLogAndSeparator(method)
                 .appendLogAndSeparator(key)
               .appendLog(""); // -> 로그 포맷 자리수 맞추기 위해 빈값을 추가해야하는 경우 발생
        return builder.toString();
}
```

하지만 위 코드에서와 같이 log 를 생성하게 되면 변경이 이루어질 때 모든 METHOD 카테고리 Dto 클래스를 수정해야하기에 비효율적인 상황이 발생하게 됩니다. 이를 개선하기 위해 log 생성에서부터 저장까지의 로직을 개선할 필요가 있었고, 추가로 log 관련 설정 변경이 필요하면 이는 설정 파일에서 손쉽게 변경하도록 처리하는 것이 주요한 목표였습니다.

<br>

**3) 기존 오류는 수정하여 개선**

마지막 목표는 오류 수정입니다. 잘 활용해왔던 프로젝트였는데 무슨 오류가 있을까 했지만 캐싱과 비동기 처리 로직에서 둘 다 제대로 동작하지 않는 문제가 있었습니다. 모두 error 나 exception 을 일으키는 문제는 아니였지만 제대로 기능 동작이 되지 않고 있었기에 이것 역시 해결하는 것이 목표였습니다.

<br>

### 전체 기능 리스트 및 엔티티 구조

이 3가지 목표와 함께 전체적인 API 기능 리스트와 엔티티 구조에 대해 간단하게 설명드리도록 하겠습니다. 앞서 말씀드렸던 바와 같이 클릭 요청 중심으로 설명을 드리겠지만 전체적인 구조도 설명을 드려야할 것 같아서 간단하게 도식화해보았습니다.

<br>

먼저 전체 기능 리스트 및 엔티티 구조입니다.
- Cache, log 는 모두 RedirectUrl 에 의존적인 기능인데 특히 RedirectUrl 의 클릭 요청의 경우에는 두 기능에 모두 연결이 되어 있습니다.

![image6-1.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image6-1.png)

<br>

- 또한 데이터베이스 스키마는 다음과 같습니다. ad_redirect, adr_log 2개의 database 에 각각 redirect_url, adr_stat 테이블이 존재하며 adr_stat 의 경우에는 log 가 저장되는 테이블입니다. 스키마 구조 이미지는 삭제했습니다.

<br>

## 파일럿 프로젝트 진행(2) - 클릭 요청 API

전체적인 설계 구조를 살펴보았다면 이제부터 본론을 시작하도록 하겠습니다.

클릭 요청 API 는 전체 아키텍처에서 이 부분을 의미합니다.

![image7.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image7.png)

쇼핑 링크와 같이 이를 클릭하게 되면 Cache 혹은 DB 에서 RedirectUrl 을 조회해오는데 이때 성공, 실패 여부와 전달 받은 METHOD 카테고리에 따라 log 파일을 적재한 뒤 리다이렉트를 시키는 API 입니다.

여기서 Cache 와 log 에 대한 설명이 필요하기 때문에 하나씩 살펴보며 설명을 드리도록 하겠습니다.

<br>

### Cache

먼저 Cache 관련 로직은 다음과 같습니다. 이는 간단한 로직이기에 diagram 으로 설명을 대체합니다.

![image8.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image8.png)

- Cache 관련 기능
    - 전체 조회
        - monitoring 요청이 오면 저장된 전체 Cache 를 조회하여 List 로 반환합니다.
    - 업데이트
        - 1분마다 Scheduler Cron 이 동작하여 Cache 를 업데이트 해줍니다.
    - 전체 및 특정 Cache 삭제
        - (**기능 추가)** 전체 혹은 Cache 의 key 로 특정 Cache 만 삭제

주로 Cache 를 활용하는 곳은 클릭 요청 API 에서 @Cacheable 을 활용하여 RedirectUrl 을 조회해오는 부분입니다. 이 메소드를 설계하면서 직면한 **@Cacheable 이슈**를 중심으로 설명드리도록 하겠습니다.

<br>

> 주요 로직은 생략하여 작성했습니다.
> 

<br>

기존 프로젝트에서는 이와 같이 설정이 되어 있었습니다.

```java
import com.googlecode.ehcache.annotations.Cacheable;

@Cacheable(cacheName = SELECT_REDIRECT_CACHE_NAME, cacheNull = false, keyGeneratorName = "stringCacheKeyGenerator")
public RedirectUrl getRedirectUrl(RedirectUrlKey redirectUrlKey) throws HibernateException {
    /** 생략 **/
}
```

여기서 사용된 EhCache 는 `com.googlecode.ehcache.annotations` 의 @Cacheable 을 활용하였고, KeyGenerator 는 `com.googlecode.ehcache.annotations.key` 의 StringCacheKeyGenerator 를 활용했습니다.

처음에는 기존 프로젝트의 오류를 확인하지 못하여 새로운 프로젝트에서 그대로 설정 방법을 따라 구성해본 뒤 API 테스트를 해보았는데 Cache 는 Cache 대로 저장이 되고 이 곳 메소드에서는 계속 DB 에서 값을 가져오는 문제를 확인했습니다.🤔

<br>

i) 그래서 @Cacheable 이 잘 적용되지 않는 문제를 해결하기 위해 처음 시도한 방법은 먼저 googlecode 의 EhCache 가 아닌 **spring-boot-starter-cache + EhCache** 로 변경을 하고 **StringCacheKeyGenerator 를 삭제**하는 방법을 시도했습니다. 

그 이유는 spring-boot-starter-cache 를 사용하게 되면 CacheManager 와 같은 기본 설정은 추가적으로 진행하지 않아도 되기에 이 방법으로 변경했으며, StringCacheKeyGenerator 의 경우에도 Cache 의 key 에 parameter 값을 직접 활용할 수 있어 해당 모듈을 제거하고 구현을 해보았습니다.

```java
import org.springframework.cache.annotation.Cacheable;

@Cacheable(cacheNames = SELECT_REDIRECT_CACHE_NAME, key = "#param.convert().getRedirectUrlKey()", unless = "#result == null")
public RedirectUrl getRedirectUrl(RedirectParam param) {
    /** 생략 **/
}
```

이렇게 수정을 해보니 이전에 발생했던 캐싱이 잘 동작하지 않던 문제는 해결이 되었습니다.

하지만 이 방법이 갖는 한 가지 한계점을 알게 되었습니다. 같은 Cache 이름과(현재는 SELECT_REDIRECT_CACHE_NAME 을 의미) 같은 파라미터(RedirectParam)를 갖고 있는 메소드가 2개 이상 작성 되면 캐싱이 안 되는 문제가 있음을 알게 되었습니다.

지금은 위 조건에 해당하는 메소드가 1개뿐이지만 만약 추후에 더 생성이 된다면 custom 한 KeyGenerator 가 필요해지기 때문에 결국 기존에 사용했던 StringCacheKeyGenerator 를 사용하는 방법을 선택했습니다.

<br>

ii) 그런데 spring-boot-starter-cache 에 StringCacheKeyGenerator 를 더했을뿐인데 또 다른 문제가 나타나게 되었습니다.

해당 프로젝트에서는 Cache 를 1분마다 업데이트해주는 로직과 Cache 를 삭제해주는 로직이 있는데 특히 1분마다 업데이트를 진행하는 곳에서는 StringCacheKeyGenerator 의 generateKey 메소드를 활용하여 값을 저장하게 됩니다.

이때 해당 로직이 먼저 수행된 후에 클릭 요청을 보내면 저장된 Cache 에서 바로 값을 가져와야하는데 또 다시 DB 에서 가져와 문제를 원점으로 만들어버렸습니다..

즉,

- 클릭 요청이 먼저 수행된 경우 연달아서 2번 호출하게 되면 → 2번째 호출에서는 Cache 에서 조회
- 1분마다 Cache 업데이트가 먼저 수행된 후 → 클릭 요청이 수행된 경우에는 DB 에서 조회

이와 같은 상황이 나타나게 되었습니다.

<br>

iii) 다시 차분히 생각을 해보았습니다. 그러다보니 이전에 parameter 자체의 값을 그대로 캐싱했을 때는 생기지 않았던 문제임을 알게 되었고, 결국 StringCacheKeyGenerator 의 원리를 고려하지 않아서 생긴 문제임을 알게 되었습니다.

StringCacheKeyGenerator 는 다음과 같이 Cache 를 저장합니다. 

```java
/**
 * append 함수의 일부를 가져온 코드입니다.
 */
@Override
protected void append(StringGenerator generator, char[] a) {
    generator.builder.append("[");
    if (a.length > 0) {
        int index = 0;
        for (; index < a.length - 1; index++) {
            generator.builder.append(a[index]).append(",");
        }
        
        generator.builder.append(a[a.length - 1]);
    }
    generator.builder.append("], ");
}
```

이때 StringCacheKeyGenerator 의 generateKey 메소드를 활용하게 되면 key 값의 앞, 뒤로 [] 를 붙여서 String 타입으로 만들어주는데, 제가 구현한 @Cacheable 이 붙은 메소드에서는 이를 고려하지 않고  `key = "#param.convert().getRedirectUrlKey()"` 와 같이 조회해오려고 하여 Cache 에 저장된 값을 찾지 못했던 것이었습니다.

최종적으로 다음과 같이 코드를 수정하였고 기존 프로젝트의 오류를 수정함과 동시에 spring-boot-starter-cache 를 활용해 설계를 완성시킬 수 있었습니다.

```java
import org.springframework.cache.annotation.Cacheable;

@Cacheable(cacheNames = SELECT_REDIRECT_CACHE_NAME, key = "'[' + #param.convert().getRedirectUrlKey() + ']'", unless = "#result == null")
public RedirectUrl getRedirectUrl(RedirectParam param) {
    /** 생략 **/
}
```

<br>

추가적으로 Cache 관련 이슈를 하나 더 설명드리려고 합니다.

Cache 를 설정할 때 한 가지 놓쳤던 부분이 있었는데 이는 바로 **싱글톤 이슈**입니다. Spring Cache 는 따로 Bean 을 만들어주지 않아도 CacheManager, EhCacheManagerFactoryBean 이 생성이 되지만 테스트 코드를 작성할 때 CacheManager 가 여러 번 생성이 되게 되면 에러가 발생하게 됩니다.

<br>

<U>Exception : Another unnamed CacheManager already exists in the same VM.</U>

<br>

이는 Bean 을 직접 설정하고 싱글톤 여부를 true 로 설정해줌으로써 해결할 수 있었습니다.

```java
@Bean
public EhCacheManagerFactoryBean ehCacheCacheManager() {
    EhCacheManagerFactoryBean factoryBean = new EhCacheManagerFactoryBean();
    factoryBean.setConfigLocation(new ClassPathResource("ehcache.xml"));
    factoryBean.setShared(true);
    return factoryBean;
}
```

EhCacheManagerFactoryBean 은 EhCacheManager 의 적절한 관리 및 인스턴스를 제공하는데 필요하며 EhCache 설정 리소스를 구성하는 객체입니다. 여기서 setShared 설정이 CacheManager 의 싱글톤 여부를 의미하며 true 로 처리함으로써 위 문제를 해결할 수 있었습니다.

<br>

### Log

다음은 log 입니다. Cache 에서 설명드린 아키텍처 그림에는 최종적으로 log 를 저장하게 되는데 요구사항은 다음과 같습니다.

- (1) 성공, 실패 뿐만 아니라 METHOD 카테고리별로 log 가 쌓여야 한다.
- (2) METHOD 카테고리별로 log 포맷을 변경할 수 있어야 한다.
- (3) METHOD 카테고리별로 log 에 들어갈 변수의 개수가 변경될 수 있어야 한다.
- (4) 이외에 설정을 변경하게 될 때 쉽게 변경이 되어야 한다.

(1)번의 경우에는 Logback 의 MDC, SIFT Appender 기능을 활용하여 해결했습니다.

<br>

> 여기서 MDC 란?  
>

```text
Mapped Diagnostic Context 의 약자로 log 를 기록할 때 요청마다 고유의 ID 를 부여해서 log 를 기록하게 되면 그 ID 를 이용해서 각 요청마다의 log 를 묶어서 볼 수 있습니다. 이를 Correlation ID 라고 하는데, Java 에서는 ThreadLocal 이라는 변수를 통해서 해결할 수 있다고 합니다.     

이 변수는 Thread 가 살아있을 동안에 계속 유지되는 변수인데 ThreadLocal 의 ID 변수에 Correlatoin ID 를 저장해놓고, 각 메소드에서 이 값을 불러서 log 출력시 함께 출력하는 방법입니다. 

그러나 이를 일일이 구현하기에는 불편할 수 있어서 이 기능을 제공해주는 것이 MDC 입니다.  

MDC 를 사용할 때는 MDC.put(key, value) 로 값을 넣고 지울 때는 MDC.remove(key) 로 지우거나 전체를 지울 때는 MDC.clear() 를 사용하여 지울 수 있습니다. 참고로 공식 문서에서는 put() 함수는 remove() 함수와 균형을 이루는 것을 권장하고 있습니다.  

즉, remove 나 clear 를 실행하지 않고 put 만 수행하게 될 경우 특정 키에 대한 값이 계속 남아있는 것을 방지하고자 같이 수행되는 것을 추천하기 때문에 저 역시 clear 함수를 수행하도록 설계했습니다.
```

<br>

클릭 요청에는 METHOD 카테고리가 같이 전달이 되기 때문에 log 를 생성하는 부분에서 `MDC.put(”method”, METHOD 카테고리);` 로 값을 저장하고, logback.xml 에서 값을 가져와서 SIFT Appender 를 통해 log 파일을 생성하도록 처리했습니다. 꼭 SIFT Appender 를 사용해야만 MDC 를 사용할 수 있는 것은 아니지만 log 경로를 동적으로 변경하기 위해 사용하게 되었습니다.

<br>

```java
/**
 * Success 상황만 고려했습니다.
 * 비즈니스 로직 처리 이후에 최종적으로 log 를 생성하는 부분입니다.
 */
public static void writeLog(String method, String logPattern, Object args) {
    MDC.put("method", method);
    logger.info(logPattern, args);
    MDC.clear();
}
```

<br>

이를 logback.xml 에서는 다음과 같이 처리할 수 있습니다.

```xml
<appender name="siftSuccessAppender" class="ch.qos.logback.classic.sift.SiftingAppender">
    <discriminator>
        <key>method</key>
        <defaultValue>dev</defaultValue>
    </discriminator>
    <sift>
        <appender name="SuccessRollingAppender" class="ch.qos.logback.core.rolling.RollingFileAppender"
            <file>${REDIRECT_SUCCESS_DIR}/${method}.log</file>
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
                <fileNamePattern>${REDIRECT_SUCCESS_DIR}/${method}.log.%d{yyyy-MM-dd-HH}</fileNamePattern>
            </rollingPolicy>
            <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
                <level>INFO</level>
            </filter>
            <encoder>
                <pattern>${FILE_LOG_PATTERN_${method}}</pattern>
            </encoder>
        </appender>
    </sift>
</appender>
```

<br>

discriminator 에서 key 로 넘겨받은 method 를 찾고, 그 값인 ${method} 를 파일 이름으로 하여 REDIRECT_SUCCESS_DIR 아래에 생성해줍니다.

그러면 최종적으로 SUCCESS_DIR 혹은 ERROR_DIR 아래에 요청으로 들어온 METHOD 카테고리명으로 구분되어 파일이 생성이 됩니다.

<br>

또한 여기서 자연스럽게 (2), (3), (4)번으로 넘어가게 됩니다. 

먼저 (2)번의 경우에는 (1)번과 같이 넘겨 받은 ${method} 를 활용하여 log 포맷을 원하는대로 설정할 수 있습니다. 

만약, METHOD 카테고리가 SHOPPING 일 때, logback.xml 파일에서 아래와 같이 property 를 선언했다면

```xml
<property name="FILE_LOG_PATTERN_SHOPPING" value="%5p [%d] [%C:%M] --SHOPPING-- [%m]%n"/>
```

logback.xml 에서는 encoder 부분에 아래와 같이 작성해주면 log 포맷을 METHOD 카테고리마다 다르게 적용시킬 수 있습니다.

```xml
<encoder>
    <pattern>${FILE_LOG_PATTERN_${method}}</pattern>
</encoder>
```

<br>

(3)번의 경우도 해결할 수 있는데, 위 코드에서 parameter 에는 method 뿐만 아니라 logPattern 과 args 가 같이 존재합니다. 

블로그 내용 초반에 기존 프로젝트에서는 log 내용을 Dto 클래스에서 생성해서 전달해준다는 점을 말씀드린바가 있습니다. 이렇게 되면 요구사항 (3)번을 해결할 수 없기에 이 부분을 해결하고자 log 내용에 포함되는 변수들을 parameter 로 던지도록 구성을 바꾸었고, 이를 writeLog 메소드에서 가변 인자로 받도록 수정했습니다.

그리고 그 가변 인자의 개수에 맞게 log 가 작성이 되어야 하므로 application.yml 파일에 METHOD 카테고리별로 logPattern 을 작성한 뒤,

```yaml
log:
  pattern:
    success:
      SHOPPING: '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
      # 그 외 다른 METHOD 카테고리
```

이를 Map 으로 저장하도록 코드를 설계했습니다.

```java
@ConstructorBinding
@ConfigurationProperties(prefix = "log.pattern")
@RequiredArgsConstructor
@Getter
public class LogPatternProperties {

    private final Map<String, String> success;
    private final Map<String, String> error;
}
```

그러면 METHOD 카테고리별로 그에 맞는 logPattern 과 그 변수들을 전달해준다면 → 이전에는 log 포맷이 통일 되어야 했지만 그럴 필요 없이 서로 다른 내용의 log 가 작성이 될 수 있으며 → 여기에 더하여 서로 다른 log 포맷으로 저장이 될 수 있게 된 것입니다.

이 결과로 (4)번도 해결이 되었습니다. 물론 log 내용이 아예 바뀌게 되면 코드 수정은 불가피하겠지만 이전처럼 모든 METHOD 카테고리에 영향을 주는 것이 아닌 각각 별개로 구성을 바꿀 수 있고 이는 logback.xml, application.yml 파일 수정으로 간단하게 변경할 수 있게 되었습니다.

<br>

**(추가 기능)** 추가로 logback 관련 기능을 소개드리려고 합니다.

- 만약 어떤 내용이 포함되어 있을 경우 log 를 저장하지 않도록 처리하고 싶다면 EvaluatorFilter 를 활용하면 됩니다.
- “do not print test” 라는 내용이 포함되어 있으면 log 를 저장하지 않도록 하는 상황을 예시로 들어보았습니다.

```xml
<filter class="ch.qos.logback.core.filter.EvaluatorFilter">
    <evaluator>
        <expression>return formattedMessage.contains("do not print test");</expression>
    </evaluator>
    <OnMatch>DENY</OnMatch>
    <OnMismatch>NEUTRAL</OnMismatch>
</filter>
```

- 또 일정 기간 이후에 log 파일을 삭제하고 싶다면 maxHistory 설정을 줄 수 있습니다.
- 기준은 rollingPolicy 이기 때문에 현재 설정은 yyyy-MM-dd-HH 로 시간 기준이 됩니다.
- 따라서 10일 이후에 쌓인 log 파일이 삭제되길 원한다면 240으로 설정해주면 됩니다.

```xml
<rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
    <fileNamePattern>${REDIRECT_SUCCESS_DIR}/${method}.log.%d{yyyy-MM-dd-HH}</fileNamePattern>
    <!-- 일정 기간 이후 log 파일 삭제 -->
    <maxHistory>240</maxHistory>
</rollingPolicy>
```

<br>

### push API 와 연동

redirect 서버를 QA 서버에 배포한 뒤 기존 push API 와 연동을 해보았습니다.

![image9.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image9.png)

앱/웹 push (이하 푸시) 를 클릭하면 해당 기사나 컨텐츠로 이동을 해야하기 때문에 링크가 삽입되어져 있습니다. 이때 해당 링크를 redirect 서버에서 조회해오도록 수정하여 링크를 클릭하게 되면 이 요청 역시 **redirect 서버의 클릭 요청**으로 넘어가게 되어 log 를 적재할 수 있게 되기 때문에 연동 작업을 진행하게 되었습니다.

즉, 아래 내용으로 요약을 할 수 있습니다.

- redirect 서버에 update/url API 를 호출하여 푸시내 url 을 insert or update 시킨다.
- 이때 저장 성공 시 RedirectUrl 객체의 컬럼값인 urlHashCode 를 반환한다.
- 결과를 받은 push API 는 urlHashCode 와 푸시용 도메인을 활용하여 redirect url 을 생성하여 PushMessage 에 set 하고, 유저에게 push 를 보낸다.
- 유저가 그 링크를 클릭하면 클릭 요청으로 전달이 되어 log 를 저장시킬 수 있다.

<br>

또한 push API 에서 redirect 서버와 통신 방법은 다른 서브 모듈을 참고하여 설정을 했으며 응답 결과에 따라 이후 비즈니스 로직 처리가 달라지기 때문에 동기 처리 방식인 RestTemplate 을 활용하여 구현했습니다.

```java
try {
    List<RedirectUrlRequest> redirectParams = new ArrayList<>();
    //내부 로직은 삭제처리했습니다.
    redirectParams.add(redirectUrlRequest);

    final ApiResponseObject<RedirectUrlResponse> apiResponseObject =
            redirectAdapterClient.post(UPDATE_URL, null, redirectParams,
                    null, new ParameterizedTypeReference<RedirectUrlResponse>() {
                    });
    return apiResponseObject.isSuccess() ? (apiResponseObject.getObject().getValue()).get(0) : null;
} catch (Exception e) {
    return null;
}
```

푸시 테스트 결과 전송된 푸시를 클릭했을 때 redirect 서버쪽에서 푸시 log 가 생성됨을 확인하였고, 새로운 METHOD 카테고리 추가를 해도 큰 로직 변경 없이 이를 처리할 수 있었습니다.

<br>

## 추가 기능 - Short URL 적용

이제 마지막 요구사항인 Short URL 에 대한 내용입니다. 한 예시로 YouTube 상에서 URL 을 공유할 때 Short URL 로 공유가 되는 것을 볼 수 있는데요, 이와 같이 도메인과 특정 값으로 구성된 URL 로 진입시 nginx 상에서 rewrite 해주어 기존 요청으로 전달될 수 있도록 하는 것이 해당 기능의 목적이었습니다.

여기서 nginx rewrite 이란 요청을 통해서 주어진 URL 의 규칙을 변경해 웹 서비스를 보다 유연하게 만드는 방법을 의미합니다. 또한 nginx 와 관련하여 reverse_proxy 와 proxy_pass 라는 개념이 나오는데 먼저 **reverse_proxy** 는 클라이언트가 reverse_proxy_server 에 요청을 보내고, 요청을 받은 reverse_proxy 는 내부 서버에 전달을 하게 되어 높은 보안성이 유지되는 장점을 갖고 있는 개념을 의미합니다. 

그리고 이를 위한 설정은 **proxy_pass** 뒤에 서버 주소를 입력해줄 수 있습니다. 그렇게 되면 클라이언트에서 서버에 직접 요청하는 것이 아니라 요청을 location 상의 URL 로 보내면 proxy 가 그걸 받아서 실제 서버에 요청을 보내 데이터를 받아와주게 됩니다.

![image10.png](/images/portal/post/2023-02-14-redirect-refactoring/redirect-refactoring-image10.png)

이를 참고하여 제가 설정한 방법은 다음과 같습니다. 

```bash
server {
    listen 8082;
    server_name localhost;
    location / {
        rewrite ^/([0-9]+) /click?urlHashCode=$1&method=SHORT_URL break; 
        proxy_pass http://localhost:8080;
    } 
}
```

- 아직 local 상에서만 설정을 했으며 애플리케이션 port 는 8080, nginx port 는 8082로 설정되어 있는 상태입니다.
- 만약 [`localhost:8082`](http://localhost:8082) 뒤에 hash_code 가 붙어서 요청이 들어온다면 클릭 요청으로 넘어가도록 설정했습니다.
- 이때 hash_code 는 그대로 전달하고 METHOD 파라미터만 설정해주어 전달했습니다.
- 여기서 hash_code 는 RedirectUrl 엔티티의 한 컬럼값을 의미합니다.

<br>

위 설정을 통해 Short URL 에 대한 처리도 이 곳 redirect 서버에서 처리가 가능하게 되었으며 이 METHOD 카테고리 역시 log 를 적재할 수 있게 되었습니다.

<br>

## 회고

리팩토링을 통해 수정을 최소화하고 기능을 확장시키는 것에 대한 고민을 오래해볼 수 있어서 좋았습니다. 특히 Short URL 의 경우 아직 활용을 하고 있지는 않지만 이번 redirect 서버 리팩토링을 통해 새로운 METHOD 카테고리가 추가되어도 Dto 클래스 정도의 추가를 제외하고는 기존 로직을 거의 수정하지 않은채 기능을 확장시킬 수 있음을 경험하게 되었습니다.

또한 현재 IDC 에 배포된 서버를 AWS 로 이관하는 과정을 경험함으로써 부족한 부분도 더 느끼게 되었고 이를 바탕으로 앞으로 해나가야 할 방향을 잘 알게 된 것 같아 좋은 기회였던 것 같습니다. 

감사합니다.

<br>

## 참고 블로그 및 문서

- Cache 관련
    - [Spring Boot + EhCache](https://jojoldu.tistory.com/57)
- log 관련
    - [Logback 공식 문서](https://logback.qos.ch/manual/appenders.html)
    - [Correlation ID & MDC](https://bcho.tistory.com/1316)
- Short URL 관련
    - [nginx rewrite 공식 문서](https://www.nginx.com/blog/creating-nginx-rewrite-rules/)