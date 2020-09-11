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

### (1) 날씨

![2-날씨모듈_1](/images/portal/post/2020-09-11-Zum-Chrome-Extension/2-날씨모듈_1.png){:style="height:75px;display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}
![2-날씨모듈_2](/images/portal/post/2020-09-11-Zum-Chrome-Extension/2-날씨모듈_2.png){:style="height:75px;display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}

### (2) 시계

![3-시계모듈](/images/portal/post/2020-09-11-Zum-Chrome-Extension/3-시계모듈.png){:style="height:75px;display:inline-block;box-shadow:0 0 10px #ddd;padding:0"}

### (3) 운세

![4-운세모듈](/images/portal/post/2020-09-11-Zum-Chrome-Extension/4-운세모듈.png){:style="height:200px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

### (4) 검색

![5-검색모듈](/images/portal/post/2020-09-11-Zum-Chrome-Extension/5-검색모듈.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

### (5) 추천사이트, 자주방문한 사이트

![6-바로가기모듈](/images/portal/post/2020-09-11-Zum-Chrome-Extension/6-바로가기모듈.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

### (6) 주제별 컨텐츠

![7-컨텐츠모듈](/images/portal/post/2020-09-11-Zum-Chrome-Extension/7-컨텐츠모듈.png)

### (7) 이슈검색어

![8-이슈검색어모듈](/images/portal/post/2020-09-11-Zum-Chrome-Extension/8-이슈검색어모듈.png){:style="height:400px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

### (8) 설정

![9-설정_0](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-설정_0.png){:style="height:200px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

![9-설정_1](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-설정_1.png){:style="height:50px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

![9-설정모듈_1](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-설정모듈_1.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

![9-설정모듈_2](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-설정모듈_2.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}

![9-설정모듈_3](/images/portal/post/2020-09-11-Zum-Chrome-Extension/9-설정모듈_3.png){:style="height:300px;box-shadow:0 0 10px #ddd;padding:0;margin:0;"}


## 3. 개발 과정 소개

## 4. 배포 과정 소개

## 5. 시스템 아키텍쳐

## 6. 지옥의 검수 과정

## 7. 앞으로의 계획

