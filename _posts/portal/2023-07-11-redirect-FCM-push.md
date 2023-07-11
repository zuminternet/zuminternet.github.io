---
layout: post
title: 리다이렉트 서버와 FCM 푸시 연동
description: 리다이렉트 서버와 FCM 푸시 연동과정을 정리해보았습니다.
image: /images/portal/post/2023-07-11-redirect-FCM-push/thumbnail.png
introduction: 리다이렉트 서버와 FCM 푸시 연동과정을 정리해보았습니다.
category: portal/tech
tag:  [Spring Boot, Firebase, Logback]
author : parkje0927
---
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fzuminternet.github.io%2Fredirect-FCM-push%2F&count_bg=%233060D3&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![thumbnail.png](/images/portal/post/2023-07-11-redirect-FCM-push/thumbnail.png)

<br>

> 안녕하세요. 포털개발팀 박정현(Kate) 입니다.     
이전 글에 이어서 FCM 푸시와 리다이렉트 서버와의 연동 과정을 작성하게 되었습니다.
과정 중에 만난 문제를 해결해가는 경험을 간략하게 작성을 해보았는데요, 재밌게 읽어주시면 감사하겠습니다.
> 

<br>

## 목차

```
1. 개요
2. 푸시 서버와 연동
3. 배경
	3-1. 내용
4. 클릭 외에도 노출 API 추가하여 log 적재
	4-1. 리다이렉트 서버 1차 요구사항 적용
	4-2. 리다이렉트 서버 2차 요구사항 적용
5. web 푸시 노출 로그의 문제점
	5-1. 푸시 서버 노출 로그 문제에 대한 해결방법 적용
6. 기존 푸시 cms 에 내용을 추가하여 확인
7. 마무리
```

<br>

## 개요

이전에 리다이렉트 서버 리팩토링 과정에서 리다이렉트 서버란 무엇이고 어떤 요구사항들을 해결했는지 정리를 해보았습니다.

이번에 다룰 내용은 리다이렉트 리팩토링 이후의 이야기인데요, 리팩토링 관련해서는 [이전 글](https://zuminternet.github.io/redirect-refactoring/)과 중복이 되기 때문에 여기서는 간략한 정리 이후 바로 본론으로 들어가려고 합니다. 그러니 자세한 내용은 [이전 글](https://zuminternet.github.io/redirect-refactoring/)을 참고해주세요🙂 

<br>

리팩토링 이후 전달 받은 새로운 요구사항은 리다이렉트 서버와 푸시 서버를 연동하는 것이었습니다.

사내 푸시 서버와 어떤 로직을 연동하는 것인지, 그러면 리다이렉트 서버에는 영향이 없는 것인지 등 좀 더 고도화된 요구사항들 속에서 혼란 가득했던 문제 해결 과정기를 그려보려고 합니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-0.png)

<br>

## 푸시 서버와 연동

## 배경

앞서 리다이렉트 서버와 푸시 서버를 연동한다고 말씀드렸습니다.

왜 연동 작업을 추가하게 되었을까요? 도입 배경은 아래 문제 상황과 연관이 되어 있습니다.

<br>

**문제 상황**

- 기존에는 푸시 전송 후 사용자의 반응을 확인하기가 어려웠습니다.
- 즉, 어떤 문구로 푸시가 전송되었을 때 리텐션이 올라가는지 확인이 어려웠습니다.

정리를 해보자면 푸시 전송 후 가장 중요한 것은 결국 푸시를 통해 앱으로 유입되는 사용자의 수를 증가시키는 것인데 해당 데이터 확인이 어려운 상태였습니다. 따라서 이번 연동 작업을 통해 사용자가 관심 가질 만한 푸시를 찾아서 리텐션을 올리는 것이 주요 목표였고 이를 위해 통계 작업이 필요하게 된 것입니다.

<br>

### 내용

**WHAT**

그렇다면 무엇을 연동하는 것일까요? 바로 푸시 메세지에 대한 클릭, 노출 데이터를 확인하기 위해 연동을 하는 것입니다. 그러면 클릭, 노출 데이터는 무엇일까요?

웹이나 앱에서 푸시 메세지를 받았을 때 이를 클릭하여 해당 푸시 내용을 확인하는 과정에서 여러 데이터가 수집될 수 있습니다. 여기서 우리는 2개의 통계를 내리기로 했습니다.

- 클릭 통계
- 노출 통계

- 클릭, 노출 통계란?
    - 클릭 통계 : click log 를 통해 수집 / 사용자가 클릭한 카운트
    - 노출 통계 : view log 를 통해 수집 / 푸시 발신 카운트(푸시를 보낼 때 발생하는 이벤트이므로)

<br>

<aside>
💡 *참고 내용*

- pv : 페이지뷰, 홈페이지에 유입된 사용자가 우리 홈페이지에서 몇 개의 페이지를 둘러보았는지
- uv : 순방문자, 웹 페이지에 방문한 사람의 수
</aside>

<br>

즉, **클릭 통계**를 해당 푸시를 사용자가 몇 번 클릭했는지에 대한 통계로 정의하였고, 해당 푸시를 보낼 때 발생하는 이벤트인 **노출 통계**를 푸시 발신 카운트로 정의하였습니다.

<br>

**WHY & HOW**

그런데 이 통계 데이터가 리다이렉트와 무슨 연관이 있는 것일까요?

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-1.gif)

<br>

푸시를 보내면 클릭 후 이동할 URL 이 들어가 있는데, 기존에는 원본 URL 만 보냈지만 클릭 통계를 위해 **특정 도메인**으로 통계가 잡혀야 했습니다.
그래서 원본 URL 를 → 리다이렉트 서버로 보내서 **특정 도메인을 붙인 리다이렉트 URL** 을 만든 다음에 → 이를 푸시에 담아서 보내기로 했습니다.
그러면 유저가 푸시를 클릭하게 되면 → 리다이렉트 URL 을 클릭하여 리다이렉트 서버로 이동하게 되고 다시 원본 URL 을 return 하는 과정에서 log 가 적재되는 구조를 갖게 되는 것입니다.

<br>

좀 더 설명을 드리기에 앞서 이를 도식화하면 아래와 같습니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-2.png)

<br>

즉, 리다이렉트 서버와 연동을 하게 되면

- 1) 리다이렉트 서버를 호출하여 특정 도메인을 붙인 리다이렉트 URL 생성
- 2) 이때, 리다이렉트 log 적재

이렇게 2가지의 기능이 가능한데, 리다이렉트 URL 을 기반으로 클릭/노출 데이터 통계를 만들 때 적재된 log 데이터를 빅데이터팀에서 수집하여 클릭/노출 데이터 통계를 만들 수 있게 되므로 연동이 필요했습니다.

그리고 생성된 통계 데이터를 기존 푸시 API 에서 사용하고 있는 데이터베이스인 DynamoDB 에 쌓는 것으로 결정했습니다.

DynamoDB 를 선택한 이유는, 기존에 푸시 데이터를 푸시 고유 메세지 ID 별로 DynamoDB 에 쌓고 있었는데, 푸시 클릭/노출 count 도 같이 적재할 수 있다고 판단하여 DynamoDB 를 선택하게 되었습니다. 

<br>

💡 정리하자면 통계 데이터를 만들기 위해 리다이렉트 서버와 푸시 서버와의 연동이 필요한 것이고 이를 위한 수정들이 필요한 것입니다.

<br>

그러면 기존에 클릭 API & 클릭 log 만 존재했던 리다이렉트 서버에 기능 추가라는 확장성을 고려하여 어떻게 수정을 하였는지 살펴보도록 하겠습니다.

<br>

## 클릭 외에도 노출 API 추가하여 log 적재

노출 API 역시 클릭 API 와 동일한 파라미터를 받아서 log 를 적재하는 것이기에 기능 추가 자체는 어렵지 않았습니다. 다만, 지금과 같이 비슷한 기능을 가진 API 가 추가될 때를 대비하여 기존 코드를 확장성 있게 수정을 하고 싶었습니다.

사실 리다이렉트 서버 자체가 이렇게 기능이 확장될 거라고는 생각하지 못했고, 확장성을 고려하여 설계를 했다고 생각했으나 그러지 못했음을 느껴 반성하게 되었습니다.

<br>

그래서 먼저, 요구사항을 적용하기 위해 변하는 것과 변하지 않는 것을 구분하는 작업을 먼저 진행했습니다.

- 변하는 것 : log 경로
- 변하지 않는 것 : 비즈니스 로직, log 포맷

<br>

이를 바탕으로 기존 코드에서 변경이 필요한 곳은 아래 그림과 같습니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-3.png)

이를 바탕으로 수정이 필요한 사항을 찾아보니 아래 3가지 내용에서 수정이 필요했습니다.

- 1) 로그 경로가 나뉠 구분값(클릭, 노출) 추가
- 2) 클릭, 노출 logger 로 구분
- 3) logback 수정

초기에는 전략패턴을 활용하여 클릭, 노출과 같은 타입을 전달해주면 이에 맞는 logger 를 수행하도록 수정하려고 했으나, SuccessLogger, ErrorLogger 에서 경로만 구분을 해주면 될 것 같아 타입을 전달해주는 것으로 수정을 진행했습니다.

<br>

### 리다이렉트 서버 1차 요구사항 적용

> 1) 로그 경로가 나뉠 구분값(클릭, 노출) 추가 & 2) 클릭, 노출 logger 로 구분
> 

먼저 위에서 나온 요구사항에 맞게 수정을 진행했는데요, 클릭/노출의 값을 보내서 log 경로가 구분되도록 처리했고 logback 에서 logger 이름과 appender-ref 기능을 활용하여 각 클릭/노출 & 성공/실패 상황 별로 다른 경로에 쌓일 수 있도록 처리를 했습니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-4.png)

먼저 그림에서 볼 수 있듯이 클릭/노출이라는 구분자가 parameter 에 추가가 되었습니다. 이후 로직은 기존과 같지만 최종적으로 log 를 쌓는 곳에서 클릭 성공 로그 클릭 실패 로그 노출 성공 로그 노출 실패 로그 이렇게 4개의 logger 가 log 를 만들도록 수정했습니다.

<br>

> 3) logback 수정
> 

그러면 이 logger 의 변수명을 appender-ref 에 적어준 뒤 appender 양식을 작성해주면!!! 로그 경로가 쉽게 구분될 수 있음을 확인할 수 있습니다.

(예시 - 노출 성공 case)

```java
public static void writeLog(String method, RequestSubject subject, String logPattern, Object... args) {
    MDC.put("method", method);
    switch (subject) {
        case CLICK:
            clickSuccessLogger.info(logPattern, args);
            break;
        case VIEW:
            viewSuccessLogger.info(logPattern, args);
            break;
        default:
    }
    MDC.clear();
}
```

```xml
<appender name="viewSuccessAppender" class="ch.qos.logback.classic.sift.SiftingAppender">
    <discriminator>
        <key>method</key>
        <defaultValue>dev</defaultValue>
    </discriminator>
    <sift>
        <appender name="ViewSuccessRollingAppender" class="ch.qos.logback.core.rolling.RollingFileAppender">
            <file>${VIEW_SUCCESS_DIR}/${method}.log</file>
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
                <fileNamePattern>${VIEW_SUCCESS_DIR}/${method}.log.%d{yyyy-MM-dd-HH}</fileNamePattern>
            </rollingPolicy>
            <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
                <level>INFO</level>
            </filter>
            <encoder>
                <pattern>${FILE_LOG_PATTERN_dev}</pattern>
            </encoder>
        </appender>
    </sift>
</appender>

<logger name="viewSuccessLogger" additivity="true" level="INFO">
    <appender-ref ref="viewSuccessAppender" />
</logger>
```

<br>

### 리다이렉트 서버 2차 요구사항 적용

그런데 초기에 수정을 하다보니 새로운 요구사항이 추가가 되었습니다.

이는 바로, 푸시 메세지에 한하여 log 내용에 osType 도 추가가 되어야 한다는 내용이었습니다. osType 으로는 `aos`, `ios`, `web` 이 있으며 푸시에서 리다이렉트 서버로 redirectUrl 을 만들기 위해 한 번 호출을 할 때 해당 파라미터도 추가해서 보내면 log 내용에 이 osType 도 추가가 되어야 하는 내용이었습니다.

로그에 쌓여야하는 파라미터 추가는 쉽게 처리할 수 있었는데 그 이유는 [이전 글](https://zuminternet.github.io/redirect-refactoring/)에서 정리한 바와 같이 log 포맷을 yml 에 정리하였기 때문에 서비스 로직 내에서 해당 파라미터를 넘겨주도록 수정하는 것과 yml 파일 수정 정도로 손쉽게 요구사항을 처리할 수 있었습니다👍🏻 

```yaml
log:
  pattern:
    success:
      # 생략 ... param method, param sid, param bid, param osType
      PUSH_INTERNAL: '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
```

아래 예시는 local 에서 실행한 후 적재된 log 인데요, 실제 데이터와는 다르지만 대략적인 예제를 보여드리기 위해 첨부하였습니다.

```
INFO [2023-06-27 13:51:11,192] [SuccessLogger:writeLog] - [2023-06-27 13:51:11,192  127.0.0.1  Mozilla/5.0 (Windows NT 6.1; WOW64) ZUMN-CLIENT  PUSH_INTERNAL  push-message-id  web]
```

그러면 성공 log 만 가지고 통계를 쌓을 경우 아래와 같이 경우의 수가 생기게 되었습니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-5.png)

그런데, 이렇게만 수정하면 이 클릭/노출 통계가 잘 처리가 될거라고 생각했으나 실제로는 그러지 못했습니다..🤔

<br>

## web 푸시 노출 로그의 문제점

예상과 다르게 실제로는 앱 푸시와 달리 web 푸시로 전송이 될 때 해당 푸시의 노출 로그는 파악하기가 힘들다는 내용을 듣게 되었습니다. 웹의 보안 정책 상 앱과는 다르게 동작되는 점이 있어서 web + 노출 통계를 위해서는 다른 아이디어가 필요했습니다.

그래서 생각해낸 방법은 바로 푸시 메세지 속 이미지를 이용하는 것이었습니다!💡

<br>

### 푸시 서버 노출 로그 문제에 대한 해결방법 적용

사내에는 같은 DynamoDB 를 사용하고 있는 여러 푸시 프로젝트가 존재합니다.

- zum-app
- investingview

이와 같이 2개의 프로젝트가 존재하여 각 프로젝트마다 푸시를 보내고 데이터를 적재하는 형식인데 이런 프로젝트에 대한 데이터를 편의상 메타데이터로 부르고자 합니다.

<br>

저의 경우 zum-app 이라는 프로젝트로 푸시를 보내게 되는 것인데요, 만약 프로젝트마다 설정된 이미지 iconUrl 이 있다면 API 를 따로 호출하지 않아도 아이콘으로 카운트를 올릴 수 있기 때문에 이 장점을 활용하고자 했습니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-6.jpg)

위 이미지는 푸시가 왔을 때 화면을 스크린샷 한 이미지인데요, 즉 아이콘 이미지를 통해 최종적으로 쌓고자 하는 푸시 프로젝트에 한하여 노출 통계를 쌓을 수 있게 되는 것이지요

<br>

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-7.jpeg)

<br>

이를 바탕으로 아래와 같은 FLOW 를 그려볼 수 있습니다.

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-8.png)

- 푸시를 보낼 때 iconImage 를 같이 보내도록 하는데 이때 iconImage 는 아이콘 이미지 응답을 받는 푸시 서버 상의 엔드포인트를 넣어주게 됩니다.
- 그러면 푸시를 클릭하게 되면 해당 엔드포인트를 호출하게 되고 처음에는 push-external 모듈에서 해당 엔드포인트로 request 가 전달됩니다.
- 엔드 포인트에서는 푸시의 project 별로 DynamoDB 에 저장된 아이콘 이미지 응답을 보내주게 되고,
- 기기에서 푸시 아이콘 이미지를 보여주는 시점에 리다이렉트 노출 API 를 호출하게 되어 log 를 적재합니다.
- 최종적으로 해당 푸시에 대한 통계 카운트가 올라가게 됩니다.

<br>

> 1. internal 서버 → 푸시 전송 → external 서버
> 푸시 전송 후 푸시 클릭하면 parameter(프로젝트 이름, 푸시 통계 시 사용할 수 있는 parameter) 전달
>  
> 2. external 서버 → internal 서버
> 프로젝트 이름으로 푸시 메타데이터에서 iconUrl 가져온다.
> 여기서 DynamoDB 는 internal 서버에서만 접근 가능하여 통신이 필요하다. 
> 
> 3. external 서버 → 리다이렉트 서버
> iconUrl 이 null 이 아니라면 → 푸시 통계 시 사용할 수 있는 parameter 를 가지고 리다이렉트 서버를 호출하여
통계를 쌓는다.
> 
> 4. 마지막은 이미지 응답!
> 

<br>

여기서 이미지 응답을 받는 과정은 마지막 참고 블로그 부분에서 링크를 작성해두었는데, `HttpServletResponse` 는 아래와 같이 설정을 하여 해당 api 를 호출하면 이미지를 다운로드 받을 수 있도록 처리했습니다. 

```java
//실제 실무에 적용된 내용과는 다른 내용이 있습니다.

response.setContentType(MediaType.APPLICATION_OCTET_STREAM_VALUE);
response.setHeader("Content-Disposition", "attachment; fileName=\"" + URLEncoder.encode(pushIconSrcReadRequestDto.getProjectName() + ".png", "UTF-8") + "\";");
response.setHeader("Content-Transfer-Encoding", "binary");
response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
response.setDateHeader("Expires", 0);

response.getOutputStream().write(bytes);
response.getOutputStream().flush();
response.getOutputStream().close();
```

<br>

## 기존 푸시 cms 에 내용을 추가하여 확인

그러면, 지금까지 구현된 내용이 어떻게 적재가 되어 통계로 쌓이는지 확인해보겠습니다.

그 전에 또 하나의 작업이 필요합니다..📚

통계의 경우 기존 글에서와 같이 파일로 저장된 성공 log 를 fluentd 를 활용하여 수집한 뒤 → 주기적으로 DynamoDB 에 적재할 수 있도록 데이터를 전달해주어야 확인할 수 있습니다. 

이를 위해서 데이터팀과 논의하여 아래와 같이 데이터 양식을 정하게 되었습니다.

```json
{
    "pushMessageId": "푸시 메세지 고유 ID",
    "click": {
        "web": 1,
        "android": 2,
        "ios": 3
    },
    "view": {
        "web": 4,
        "android": 5,
        "ios": 6
    }
}
```

json 타입을 데이터를 전달해주면 해당 pushMessageId(푸시 메세지 고유 ID)에 데이터가 update 될 수 있도록 로직 처리를 했습니다.

<br>

그렇다면 이를 확인하기 위해서는 cms 에서도 작업이 필요한데요, 기존 푸시 cms 에서 사용하고 있는 기술 스택 및 로직에 맞게 해당 내용을 수정하여 작업을 진행했습니다. 참고로 푸시 cms 는 Vue.js 프레임워크와 타입스크립트를 활용하고 있으며 로그 확인 페이지에서 통계 데이터를 같이 볼 수 있도록 버튼을 추가하게 되었습니다.

그래서 해당 버튼을 누르게 되면

![image1.png](/images/portal/post/2023-07-11-redirect-FCM-push/redirect-FCM-9.png)

이와 같이 통계 내역을 확인할 수 있게 됩니다.🎉

<br>

## 마무리

현재는 아직 데이터 작업 진행중이긴 하지만 이를 통해 리다이렉트 서버와 푸시 FCM 서버와의 통신 과정과 여러 문제를 해결하는 방법을 많이 배우고 느끼게 되었습니다. 더불어, 중간에 생각하지 못한 이슈들로 인해 코드도 여러 번 수정하게 되었던 부분이 좀 아쉬운 점으로 남았습니다.

초반에 관련 내용을 잘 논의하여 방법을 정해나가는 것이 중요함을 다시 알게 되기도 하였고, 또 여러 방법론들 중에서 이 방법을 선택할 수밖에 없었던 당위성에 대해 깊게 고민해보는 것도 매우 중요하다는 것을 알게 되었습니다.

이전 글과 이번 글을 작성하면서 리다이렉트와 푸시 프로젝트의 전체적인 사이클을 이해할 수 있게 되어 좋은 경험이었던 것 같습니다.

부족한 내용이긴 하지만 글 읽어주셔서 감사합니다🙇‍♀️

<br>

## 참고 블로그 및 출처
- 파일 업로드 및 다운로드
    - https://jaimemin.tistory.com/1892
    - https://lannstark.tistory.com/8
    - https://pygmalion0220.tistory.com/entry/Spring-boot-파일-다운로드-서버에서-다운
    - https://www.floodnut.com/69
- 이미지
    - flaticon.com