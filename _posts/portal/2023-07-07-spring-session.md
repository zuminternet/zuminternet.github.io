---
layout: post
title: 제목은 Spring Session 도입기로 하겠습니다. 근데 이제 Redis를 곁들인
description: 지속 가능한 서비스를 만들기 위해 기존 아키텍처를 유지하면서 서비스를 개선하는 과정을 소개합니다.
image: /images/portal/post/2023-07-07-spring-session/thumbnail.png
introduction: 지속 가능한 서비스를 만들기 위해 기존 아키텍처를 유지하면서 서비스를 개선하는 과정을 소개합니다.
category: portal/tech
tag:  [Spring Boot, Spring Session, Redis]
author : minsoozz
---
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fzuminternet.github.io%2Fspring-session&count_bg=%23FF00D4&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![thumbnail.png](/images/portal/post/2023-07-07-spring-session/thumbnail.png)
> 안녕하세요. 줌인터넷 핀테크개발팀 김민수입니다. <br> 사내에서는 문제를 개선하고 지속 가능한 서비스를 만들기 위한 많은 노력을 하고 있습니다. 회원 서비스의 세션 저장소를 교체하면서 Spring Session을 도입한 경험을 공유합니다.

이런 분들이 읽으면 더 도움이 됩니다.

- 분산 환경에서 세션 동기화 문제를 해결하고자 하는 분
- Spring Session을 도입하고자 하는 분
- 기존 아키텍처를 유지하면서 서비스를 개선하는 과정이 궁금하신 분 등

목차는 아래와 같습니다.

- [개요](#개요)
- [도입 배경](#도입-배경)
- [Spring Session](#spring-session)
- [아키텍처](#아키텍처)
- [코드로 살펴보는 개선 과정](#코드로-살펴보는-개선-과정)
- [해치웠나?](#해치웠나)
- [마무리](#마무리)

## 개요

줌인터넷의 회원 서비스는 분산 환경에서 운영되고 있습니다. <br>
분산 환경에서 세션 동기화 문제를 해결하기 위해 사용하고 있는 세션 저장소를 Redis로 교체하게 된 이유와 <br>
기존 아키텍처를 유지하면서 안정적으로 Spring Session을 도입하는 과정을 소개합니다. <br>

---

## 도입 배경

저희 팀은 전사적 기술 안정성 향상을 위해 기존 Aerospike에서 Redis로의 전환을 결정하게 되었습니다. <br> Aerospike를 사용하며 큰 장애가 발생하지 않았지만, 전환을 통해 아래와 같은 이점을 기대하고자 하였습니다.

- Spring Session의 도입 가능
  - Spring Session은 Redis 이외에도 다양한 세션 저장소를 지원하여 세션 정보를 유연하게 관리할 수 있습니다. 이는 다음에 세션 저장소를 변경해야 할 경우에도 유연성을 제공합니다.
- 유지보수 용이성 향상
  - Redis는 현재 팀에서 적극적으로 사용하고 있으며, 신규 인프라 구축 비용이 발생하지 않습니다. 
  - Aerospike 관련 레퍼런스가 부족하여 러닝 커브가 큰 점을 고려할 때 Redis로 전환하게 되면 학습에서 발생하는 리소스 비용을 줄일 수 있습니다.

위와 같은 이유로 세션 저장소를 Aerospike에서 Redis로 전환하면서 Spring Session을 도입하게 되었습니다. <br>

---

## Spring Session

Spring Session은 스프링 기반 애플리케이션에서 세션 관리를 효과적으로 처리하기 위한 기술입니다. <br>
기본적으로 스프링 세션은 세션 데이터를 서버의 메모리에 저장하는 대신 외부 스토리지에 저장하고 관리합니다. <br>
Spring Session은 세션 데이터를 외부 스토리지에 저장함으로써 여러 서버 간에 세션 데이터를 공유하고 로드 밸런싱과 확장성을 지원합니다. 이는 분산 환경에서 여러 서버가 같은 세션 데이터에 접근하고 처리할 수 있도록 해주는 장점을 제공합니다.

Spring Session은 사용자의 세션 정보를 관리하기 위해 API 및 구현체를 제공합니다. <br>
Spring Boot 설정에서는 `springSessionRepositoryFilter`라는 이름의 Filter 인터페이스를 구현한 빈을 생성합니다.
서블릿 컨테이너는 모든 요청에 대해 `springSessionRepositoryFilter`를 사용하도록 설정해야 하지만 이 과정은 Spring Boot가 이러한 단계를 자동으로 처리해줍니다. <br>

아래는 Spring Session 적용을 위한 설정 예시입니다.

#### build.gradle

```groovy
dependencies {
    // Spring Boot에서 Redis를 사용하기 위한 의존성입니다. 
    implementation 'org.springframework.boot:spring-boot-starter-data-redis'
    // Spring Session을 Redis에 저장하기 위한 의존성입니다.
    implementation 'org.springframework.session:spring-session-data-redis'
}
```

`build.gradle`에 Redis와 Spring Session을 사용하기 위한 의존성을 추가합니다. <br>

#### application.yml

```yaml
server:
  servlet:
    session:
      cookie:
        path: / # 적용될 URL 경로를 나타냅니다. 예를 들어, path를 "/"로 설정하면 해당 도메인의 모든 경로에서 쿠키가 사용될 수 있습니다.
        name: JSESSIONID # 이름을 지정합니다.
        domain: zum.com # 유효 도메인을 지정합니다. 예를 들어, domain을 "zum.com"으로 설정하면 해당 도메인과 그 서브도메인에서 쿠키가 유효합니다.
        http-only: true # 브라우저에서 해당 쿠키에 대한 JavaScript 접근을 제한합니다. 이를 통해 XSS 공격을 방지할 수 있습니다.
        secure: true # 쿠키가 HTTPS(SSL/TLS) 연결을 통해서만 전송되어야 함을 나타냅니다. 즉, HTTPS로 암호화된 연결에서만 쿠키가 전송되어야 합니다.
      timeout: 3600 # 세션의 유효 시간을 지정합니다. 단위는 초입니다.

spring:
  redis:
    host: 127.0.0.1
    port: 6379
    password:
  session:
    store-type: redis # 세션 저장소를 지정합니다.
    redis:
      namespace: zum:session # 세션을 저장하는 데 사용되는 키의 네임스페이스를 지정합니다.
```

`application.yml`에서 `server.servlet.session.cookie`를 통해 쿠키의 속성을 지정할 수 있습니다. <br>
`spring.session.store-type`을 지정해주면 별도의 설정 없이 Spring Boot의 마법 같은 `AutoConfiguration` 으로 인해 `@EnableRedisHttpSession` 을 추가한 것과 같은 효과를 냅니다. <br>

또한 Spring Boot는 `spring.session.store-type` 속성을 기반으로 실제 사용할 구현체를 결정합니다. <br> 기본적으로 인메모리 저장소인 `MapSessionRepository` 클래스가 사용됩니다.
예를 들어, Redis를 사용하려는 경우 Redis 세션 저장소 구현체인 `RedisIndexedSessionRepository` 클래스가 Bean으로 등록됩니다. <br>

![spring-session-3.png](/images/portal/post/2023-07-07-spring-session/spring-session-3.png)


## 아키텍처

먼저 기존 아키텍처와 개선된 아키텍처의 흐름을 소개하겠습니다.

### AS-IS

기존 구성되어 있는 기존 아키텍처 흐름은 다음과 같습니다.

![spring-session-1.png](/images/portal/post/2023-07-07-spring-session/spring-session-1.png)
![spring-session-5.png](/images/portal/post/2023-07-07-spring-session/spring-session-5.png)

회원 서비스는 위와 같이 각 모듈을 독립적으로 서버에 배포하여 운영하고 있습니다. <br>

기존 아키텍처에서는 모듈마다 같은 `ID Generator`를 사용하여 세션 아이디를 생성하고 있습니다. <br>
생성된 세션 아이디를 통해 각 모듈은 세션 서버에 요청하여 세션 저장소에 접근합니다. <br>
이렇게 각 모듈마다 `ID Generator`가 존재하는 경우 만약 세션 아이디 생성 전략이 변경되었다면, 변경된 전략을 적용하기 위해 각 모듈을 전부 재배포해야 합니다. 또한 새로운 모듈이 추가된다면 매번 `ID Generator`를 추가해야 합니다.
매우 낮은 확률이지만 중복된 세션 아이디가 생성될 수 있다는 가능성도 고려하였습니다. <br>

### TO-BE

위에서 언급한 문제점을 고려하여 아키텍처 흐름을 변경하였습니다. 변경된 아키텍처 흐름은 다음과 같습니다.

![spring-session-2.png](/images/portal/post/2023-07-07-spring-session/spring-session-2.png)
![spring-session-6.png](/images/portal/post/2023-07-07-spring-session/spring-session-6.png)

세션 아이디 생성 전략을 담당하는 `ID Generator`를 하나의 모듈에서 관리하도록 변경하였습니다. <br> 개선된 세션 아이디 발행 과정을 차례대로 표현하면 다음과 같습니다. <br>

1. 사용자가 각 모듈에 접근합니다.
2. 각 모듈은 세션 서버에 세션 아이디를 요청합니다.
3. 세션 서버는 세션 아이디를 발행하고 세션 아이디와 함께 응답합니다.
4. 각 모듈은 발급받은 세션 아이디를 클라이언트에 전송합니다.

위와 같이 `ID Generator`를 한 곳에서 관리하면 모듈 간 응집도가 높아지며 <br> 필요한 변경이 있을 때도 해당 모듈만 수정하여 유지보수와 서비스의 확장을 유연하게 할 수 있습니다. <br>
`ID Generator`를 하나의 모듈에서 관리하고, `Redis`를 통해 세션 정보를 관리하도록 변경하였습니다. <br>
이를 통해 아키텍처를 개선하고, 중복된 코드를 제거할 수 있었습니다. <br>

하지만 `ID Generator`Z 한 곳에서 관리되기 때문에 `SPOF(Single Point of Failure)`가 발생할 수 있습니다. `SPOF`란 시스템에서 단일 실패 지점으로, 해당 지점에 장애가 발생하면 전체 시스템이 영향을 받는 상황을 말합니다.
이러한 문제를 해결하기 위해 세션 서버의 인스턴스를 분산하여 구성하였습니다. <br>

---

## 코드로 살펴보는 개선 과정

개선 과정의 이해를 돕기 위해 기존 코드와 개선된 코드를 예시를 통해 살펴보겠습니다. <br>
예시 코드는 해당 포스팅을 위해 모두 새롭게 작성되었으며, 실제 코드와는 차이가 있을 수 있습니다. <br>

프로젝트 환경은 아래와 같습니다.

- Java 8
- Spring Boot 2.x
- Spring Security 5.x

### AS-IS

기존 아키텍처에서 사용자가 요청 시 세션 아이디가 발행되는 과정입니다.

#### SessionIdFilter

```java
public class SessionIdFilter extends OncePerRequestFilter {

    private static final ThreadLocal<String> sessionIdHolder = new ThreadLocal<>();
    private static final String SESSION_KEY = "JSESSIONID";

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        
        String sessionId = CookieUtils.getCookieValue(request, SESSION_KEY); // 쿠키에서 세션 아이디를 조회합니다.
        
        if (Strings.isBlank(sessionId)) { // 세션 아이디가 존재하지 않는 경우 새로운 세션 아이디를 생성합니다.
            sessionIdHolder.set(SessionIdGenerator.generate());
            CookeUtils.addCookie(response, SESSION_KEY);
        }
        
        sessionIdHolder.set(sessionId); // 세션 아이디를 ThreadLocal에 저장합니다.
        filterChain.doFilter(request, response); // 다음 필터로 요청을 전달합니다.
        sessionIdHolder.remove(); // ThreadLocal에 저장된 세션 아이디를 제거합니다.
    }
}
```
해당 필터에서는 사용자의 요청마다 세션 쿠키가 존재하는지 확인하고, 만약 존재하지 않을 때에는 <br> `ID Generator`를 통해 세션 아이디를 생성하고 쿠키에 저장합니다. 
<br><br>

#### CustomSecurityContextRepository

```java
public class CustomSecurityContextRepository implements SecurityContextRepository {

    private final SessionAdapter sessionAdapter; // 세션 서버와 통신하기 위한 SessionAdapter

    public ZumContextRepository(SessionAdapter sessionAdapter) {
        this.sessionAdapter = SessionAdapter;
    }
    
    @Override
    public SecurityContext loadContext(HttpRequestResponseHolder requestResponseHolder) { // 세션 아이디를 통해 세션 정보를 조회합니다.
        return SessionAdapter.getSession()
            .map(this::createSecurityContext)
            .orElseGet(this::emptyContext);
    }

    private SecurityContext createSecurityContext(final User user) { // 세션 정보를 통해 SecurityContext를 생성합니다.
        UsernamePasswordAuthenticationToken usernamePasswordAuthenticationToken =
            new UsernamePasswordAuthenticationToken(user, user.getAuthorities());
        return new SecurityContextImpl(usernamePasswordAuthenticationToken);
    }

    private SecurityContext emptyContext() { // 세션 정보가 존재하지 않는 경우 빈 SecurityContext를 생성합니다.
        return SecurityContextHolder.createEmptyContext();
    }
}
```
Spring Security에서 기본적으로는 HttpSession을 사용하여 SecurityContext를 저장하고 로드합니다. <br>
다른 세션 저장소를 사용하기 위해  SecurityContextRepository를 구현한 클래스입니다. SessionAdapter를 통해 세션 모듈에서 세션 정보 가져오고, SecurityContext를 생성하여 반환합니다.
<br><br>

#### SpringSecurityConfiguration

```java
@EnableWebSecurity
public class SpringSecurityConfiguration extends WebSecurityConfigurerAdapter {

    private final SessionAdapter sessionAdapter;

    public SecurityConfig(SessionAdapter sessionAdapter) {
        this.sessionAdapter = SessionAdapter;
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
            .and()
            .securityContext() // SecurityContext를 설정합니다.
            .securityContextRepository(new CustomSecurityContextRepository(SessionAdapter)) // SecurityContextRepository를 설정합니다.
            .and()
            .addFilterBefore(new SessionIdFilter(), SecurityContextPersistenceFilter.class); // SessionIdFilter를 SecurityContextPersistenceFilter 이전에 실행합니다.
    }
}
```

Spring Security 설정 클래스입니다. SecurityContextPersistenceFilter는 SecurityContextRepository를 사용하여 SecurityContext의 저장 및 로드를 처리합니다. 
SessionIdFilter는 SecurityContextPersistenceFilter 이전에 실행되며, CustomSecurityContextRepository를 SecurityContextRepository로 설정합니다.
<br><br>

### TO-BE

#### SessionAdapter

```java
public class SessionAdapter {

  @Cacheable(value = "session", key = "#sessionId")
  public ZumSessionDto getSession(String sessionId) {
    ResponseEntity<User> response = restTemplate.exchange(
            "http://localhost:8080/api/v2/session",
            HttpMethod.GET,
            createRequestEntityWithHttpHeader(sessionId),
            User.class); // 세션 서버에서 세션 정보를 조회합니다.
    String responseSessionId = getSessionIdFromResponseHeaders(response.getHeaders()); // 세션 서버에서 응답받은 세션 ID를 가져옵니다.
    return ZumSessionDto.of(response.getBody(), responseSessionId); // 세션 정보를 Dto 변환합니다.
  }

  private String getSessionIdFromResponseHeaders(HttpHeaders headers) {
    String cookie = headers.getFirst("X-SESSION-ID");
    if (Strings.isNotBlank(cookie)) {
        return cookie;
    }
    return null;
  }

  private HttpEntity<Object> createRequestEntityWithHttpHeader(String sessionId) {
    HttpHeaders requestHeaders = new HttpHeaders();
    requestHeaders.add("X-Session-ID", sessionId);
    return new HttpEntity<>(null, requestHeaders);
  }
}
```

`SessionAdapter`는 각 모듈에서 세션 서버에 요청하기 위해 존재하는 Adapter 입니다. <br>
기존 구조에서는 세션 정보를 조회하기 위해 매번 네트워크 I/O 비용이 발생하는 문제가 있었습니다. 여러 가지 방법을 고민해보았지만,
세션 서버 요청의 90% 이상이 GET 요청으로 이루어지고 있어, 캐싱 시스템을 도입하여 세션 정보를 조회하는 비용을 줄이기로 했습니다. <br>

![spring-session-8.png](/images/portal/post/2023-07-07-spring-session/spring-session-8.png)

Look-aside 전략은 캐시 시스템에서 사용되는 하나의 전략으로, 데이터를 캐시에 저장하고 검색할 때 데이터베이스 또는 백엔드 시스템에 대한 추가 작업을 최소화하는 것을 목표로 합니다.

Look-aside 전략은 다음과 같이 작동합니다

1. 데이터를 읽거나 검색하기 전에, 먼저 캐시에서 데이터를 찾습니다.
2. 데이터가 캐시에 존재하면, 해당 데이터를 반환하고 추가적인 백엔드 작업을 수행하지 않습니다.
3. 데이터가 캐시에 존재하지 않으면, 데이터를 백엔드 시스템에서 검색한 후, 해당 데이터를 캐시에 저장하고 반환합니다.
4. 이후 같은 데이터에 대한 요청이 들어올 때는 캐시에서 데이터를 반환합니다. 

이러한 방식으로 Look-aside 전략은 세션 서버에 대한 요청을 최소화하고, 데이터를 빠르게 반환하여 성능을 향상시킬 수 있습니다. 만약 데이터의 업데이트가 발생하면, `@CacheEvict`를 통해 캐시를 업데이트 하도록 구현했습니다.
세션 정보가 필요할 때 마다 네트워크 I/O 비용이 발생하는 문제는 캐싱 시스템을 도입함으로써 해결하였으며 캐시 정합성 문제는 `@CacheEvict`를 통해 해결하였습니다. <br>


다시 코드를 살펴보겠습니다. 코드를 보면 특이하게도 세션 서버에 요청할 때 세션 아이디를 쿠키가 아닌 헤더에 담아 요청하고 응답을 받습니다.
아래 사진처럼 Spring Session은 세션 아이디를 기본적으로 쿠키를 통해 발행하도록 구현되어 있지만 세션 아이디를 헤더에 담아서 요청과 응답을 하는 것이 현재 아키텍처에서 더욱 적합하다고 생각했습니다. <br>

![spring-session-4.png](/images/portal/post/2023-07-07-spring-session/spring-session-4.png)

이유는 아래와 같습니다.
고
1. `Set-Cookie` 헤더는 브라우저가 응답받고 쿠키를 저장하는 과정을 거치기 때문에 브라우저가 없는 서버 간 요청에서는 쿠키를 저장할 수 없습니다.
2. 쿠키는 클라이언트 보안 정책에 따라 다르지만, 기본적으로 같은 도메인 간에만 공유됩니다. 하지만 헤더는 타사 도메인 간 요청에서 커스텀 헤더를 통해 데이터를 전달할 수 있습니다. 이는 추후 줌인터넷에서 제공하는 서비스가 만약 다른 도메인을 가질 때 유연하게 대응할 수 있다고 판단했습니다. 

따라서 세션 아이디를 헤더에 발행하는 방법으로 Spring Session을 커스터마이징하여 구현하였습니다. <br>

#### CustomSessionIdResolver

```java
import org.springframework.session.web.http.HeaderHttpSessionIdResolver;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;

public class CustomSessionIdResolver extends HeaderHttpSessionIdResolver {
    
    public CustomSessionIdResolver(String headerName) {
        super(headerName);
    }

    @Override
    public List<String> resolveSessionIds(HttpServletRequest request) {
        List<String> sessionIds = super.resolveSessionIds(request);
        if (sessionIds.isEmpty()) {
            String sessionId = request.getHeader("X-Session-ID"); // 헤더에서 세션 아이디를 읽어옵니다.
            if (sessionId != null) {
                sessionIds.add(sessionId);
            }
        }
        return sessionIds;
    }

    @Override
    public void setSessionId(HttpServletRequest request, HttpServletResponse response, String sessionId) {
        super.setSessionId(request, response, sessionId);
        response.setHeader(HEADER_SESSION_ID, sessionId); // 헤더에 세션 아이디를 추가합니다.
    }
}
```

HeaderHttpSessionIdResolver 클래스는 Spring Session에서 제공하는 HttpSessionIdResolver 인터페이스의 구현체입니다. 이 클래스를 사용하면 세션 아이디를 HTTP 헤더에 포함하여 전달할 수 있습니다. <br>
해당 클래스의 생성자는 세션 아이디를 담을 헤더의 이름을 인자로 받을 수 있습니다. <br>

#### HttpSessionIdResolverConfiguration

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.session.data.redis.config.annotation.web.http.EnableRedisHttpSession;
import org.springframework.session.web.http.HttpSessionIdResolver;

@Configuration
public class HttpSessionIdResolverConfiguration {
    @Bean
    public HttpSessionIdResolver httpSessionIdResolver() {
        return new CustomSessionIdResolver("X-Session-ID"); // 세션 아이디를 담을 헤더 이름을 지정합니다.
    }
}
```

위의 코드를 통해 CustomSessionIdResolver 클래스가 Bean으로 등록됩니다.

#### SessionController

```java
@RestController
@RequestMapping("/api/v2/session")
public class SessionController {

    private final ObjectMapper objectMapper;

    public SessionController(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @GetMapping
    User session(HttpSession httpSession) {
        return objectMapper.convertValue(httpSession.getAttribute("user"), User.class); // 세션에서 user attribute를 꺼내서 응답합니다.
    }
}
```

세션 서버의 역할은 간단합니다. SessionController 에서는 각 모듈에서 요청한 attribute를 세션에서 꺼내서 응답합니다.
Spring Session을 적용하였기 때문에 기존의 HttpSession 객체는 Spring Session이 제공하는 세션 객체로 대체되며, 데이터는 Redis에 저장되고 관리됩니다.

## 해치웠나?

![spring-session-7.png](/images/portal/post/2023-07-07-spring-session/spring-session-7.png)
<center>(개선 후 뿌듯함에 웅장해진 내 모습)</center>

<br>
어느 정도 마무리 단계에 이르렀고 테스트를 진행하면서 세션 서버를 직접 호출하는 `지름길(?)` 을 사용하는 서비스가 있는지 확인했습니다.
세션 정보를 조회하는 별도의 모듈이 존재하고 각 서비스는 해당 모듈을 통해 세션 정보를 조회하도록 API를 제공하고 있지만, 세션 서버를 직접 호출하는 서비스가 존재할 수 있어서 이를 확인해야 했습니다. <br>

아니나 다를까 우려했던 것처럼 세션 서버를 직접 호출하는 서비스가 존재했습니다. <br>

회원 서비스는 전사 서비스이기 때문에 다른 서비스에 장애 전파가 발생하지 않도록 특히 주의해야 합니다. 기존 서비스의 수정 없이 세션 서버에서 대응할 수 있는 방법을 찾아야 했고, Nginx를 통해 세션 서버로의 요청을 가로챈 후 헤더에 세션 아이디를 담아서 요청을 보내는 방법을 선택했습니다. <br>

#### nginx.conf

```agsl
http { 
    server {
        listen 80;
        server_name example.com;

        location /api/v1/session {  # 특정 URL로 요청이 들어오면
            set $session_id ""; # 세션 아이디를 담을 변수를 선언합니다.
            if ($args ~* "(?:^|&)JSESSIONID=([^&]+)") { # URL에 세션 아이디가 담겨있다면
                set $session_id $1; # 세션 아이디를 변수에 담습니다.
            }

            proxy_set_header X-Session-ID $session_id; # 세션 아이디를 헤더에 담습니다.
            proxy_pass http://backend;
            # 나머지 프록시 설정
        }
        # 나머지 서버 설정
    }
}
```

## 마무리

세션 저장소를 교체하는 작은 업무로 시작했지만, 과정속에 문제점을 도출하고 이를 해결하는 과정에서 많은 것을 배울 수 있었습니다.
`No Silver Bullet` 라는 표현이 있듯이 기존 아키텍처를 유지하면서 개선한 결과가 정답은 아니라고 생각합니다. 그래도 개선을 이루고 서비스 성장에 기여를 한 값진 프로젝트 경험이라고 생각합니다. <br>
바쁜 업무 속에서도 좋은 방향성을 위해 함께 고민해주신 동료분들께 감사드립니다. <br>

