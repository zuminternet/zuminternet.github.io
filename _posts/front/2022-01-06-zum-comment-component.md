---
layout: post
title: 댓글 모듈 레거시 걷어내기 with TDD
description: 서브도메인에서 사용되는 댓글 모듈의 레거시코드를 걷어내고 Vue, TypeScript, 그리고 Jest를 사용하여 효율적인 유지보수가 가능한 댓글 컴포넌트를 만들어 사내에 배포한 과정을 소개합니다.
image: /images/front/post/2022-01-10-zum-comment-component/00_thumbnail.png
introduction: 서브도메인에서 사용되는 댓글 모듈의 레거시코드를 걷어내고 Vue, TypeScript, 그리고 Jest를 사용하여 효율적인 유지보수가 가능한 댓글 컴포넌트를 만들어 사내에 배포한 과정을 소개합니다.
category: portal/tech
tag: [프론트엔드, Front-end, FE, zum, zum-fe, Vue, TypeScript, Jest, 테스트코드, TDD, 리팩토링]
author: somedaycode
---

<p style="text-align: right">
  <img style="margin: 0; display: inline-block;" src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fzuminternet.github.io%2Fzum-comment-component%2F&count_bg=%23003BC6&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=%EC%A1%B0%ED%9A%8C%EC%88%98&edge_flat=true" alt="조회수" />
</p>

> 안녕하세요, 포털개발팀 프론트파트의 신입 개발자 김선규 입니다. 
이번 글은 파일럿 프로젝트로 진행하게 된 줌인터넷 댓글 모듈 개선과정에 대한 내용입니다.
> 

# TL;DR

- `JavaScript`, `jQuery` 기반으로 이루어진 댓글 모듈 →  `Vue`, `TypeScript` 로 개선
- TDD(테스트 주도 개발)로 프로젝트를 진행
- 댓글 모듈 컴포넌트 사내 라이브러리 배포

<br>

# 줌 소셜 댓글 모듈

현재, 줌인터넷의 서브 도메인(투자, 뉴스, 허브 등)은 모두 사진과 같은 댓글 모듈을 통해서 댓글을 입력하고 답글을 달게 됩니다.

![01_preview.png](/images/front/post/2022-01-10-zum-comment-component/01_preview.png)

## 문제점
여러 가지 문제점들을 설명하기에 앞서서, 왜 기존의 댓글 모듈을 개선하는 프로젝트를 담당하게 되었는지 간략하게 설명하겠습니다. 줌인터넷 기존의 서비스들은 MPA(Multi Page Application)로 구성이 되어있었습니다. 댓글 모듈도 이에 맞추어 페이지가 전환될 때마다 스크립트를 주입하는 방식으로 짜여 있었습니다. 기능적인 부분에서는 문제가 없었지만, 프론트엔드파트가 SPA(Single Page Application)로 서비스를 전환하는 과정에서 불편함을 겪게 되었고, 이러한 불편함을 해결하기 위해서는 기존의 댓글 모듈을 SPA에 맞추어 개선해야 하는 필요성이 있었습니다.

**불편함을 주었던 아래의 문제점들은 새로운 기능을 추가하거나 유지보수 하는 것을 어렵게 만들었습니다.**

- 페이지 전환 시 댓글 모듈 스크립트를 주입
- 최상위 document에 등록된 모든 이벤트
- 상태 추적의 어려움
- 가독성
- 언제 쓰이는지 파악하기 어려운 코드 덩어리들

### 페이지 전환시 스크립트를 브라우저에 주입하는 방식의 문제

기존의 MPA 방식에서는 댓글 모듈을 사용하기 위한 일련의 작업이 필수적으로 필요했습니다.
  1. HTML에 특정 엘리먼트를 삽입
  2. jQuery를 사용하기 위한 스크립트 추가
  3. 초기화 스크립트 등록

```html
<!-- HTML에 해당 엘리먼트 삽입 필요 -->
<div id="zca_main" class="zum_social_comment_wrap"></div>

<!-- jQuery 사용 -->
<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
<script src="/plugin/zum-comment/js/jquery.cookie.js"></script>

<!-- 초기화 스크립트 -->
<script th:inline="javascript">
  document.domain = 'zum.com';
  function zav_callback() {
    var sysCode = [[${sysCode}]];
    var articleIdx = [[${articleIdx}]];
    var zav = new Zav();
    zav.options.displayBtn = 'like';
    zav.init(sysCode, articleIdx);
  }

  function zca_callback() {
      var sysCode = [[${sysCode}]];
      var articleIdx = [[${articleIdx}]];
      var zcai = new Zcai();
      zcai.options.device = decodeURIComponent([[${device}]]);
      zcai.options.targetUrl = decodeURIComponent([[${targetUrl}]]);
      zcai.options.articleTitle = decodeURIComponent([[${articleTitle}]]);
      zcai.options.articleUrl = decodeURIComponent([[${articleUrl}]]);
      zcai.options.onCmntCountChange = decodeURIComponent([[${onCmntCountChange}]]);
      zcai.options.onCmntAdd = decodeURIComponent([[${onCmntAdd}]]);
      zcai.options.externalCounterId = decodeURIComponent([[${externalCounterId}]]);
      zcai.options.category = 'test';
      zcai.init(sysCode, articleIdx);
  }
</script>
```

Vue를 사용하고 있는 프론트엔드파트 내의 개발자들은 댓글 모듈을 사용하기 위해 이렇게 불편한 과정을 거쳐야 했습니다. 또한, `jQuery`를 사용하는 댓글 모듈 스크립트가 제대로 동작하기 위해서는 `jQuery` 스크립트가 먼저 실행되어야 하는데요. 이렇게 스크립트를 주입하는 방식은 모듈의 실행 순서에 의존적이게끔 만들었고, 디버깅을 힘들게 만드는 단점도 존재했습니다.

> 프론트엔드파트는 통계 관련 라이브러리를 스크립트로 주입하였지만, 메인 프로그램보다 나중에 실행되어 문제의 원인을 찾는 데 많은 고생을 했던 과거가 있습니다. 🥲

### 최상위 Document에 등록된 모든 이벤트가 불러오는 문제

```js
    // 기존의 이벤트 관련 코드
    $(document).on('focus', '.input_write', function (event) {...});
    $(document).on('blur', '.input_write', function (event) {...});
    $(document).on('click', '.input_write', function (event) {...});
    $(document).on('keyup', itself.cmnt_text, function (event) {...);
    $(document).on('keyup', 'textarea[name="zca_scmnt_write"]',unction (event) {...});
    $(document).on('click', 'span[name="cmnt_like_span"]', function (event) {...});
    $(document).on('click', 'span[name="cmnt_hate_span"]', function (event) {...});
    $(document).on('click', 'span[name="scmnt_like_span"]', function (event) {...});
    $(document).on('click', 'span[name="scmnt_hate_span"]', function (event) {...});
    $(document).on('change', '.reply_blind .switch input', function () {...}
```

이벤트와 관련된 기존의 코드들이 `document` 에 등록된 것을 확인할 수 있습니다. 이렇게 모든 이벤트가 `document`에 등록되었을 때 원인을 파악하기 어려운 잠재적인 상태들이 어려움을 가져다주었습니다.

기존의 댓글 모듈이 SPA에서 사용되는 과정을 잠시 살펴보겠습니다.
 1. 페이지의 로딩
 2. 스크립트 로딩
 3. 댓글 모듈 마운트
 4. 다른 페이지로 이동
 5. `document`에 등록된 이벤트들의 제거가 필요
 6. 전부 찾아서 제거하는 것이 무척이나 까다로움

> 이러한 과정은 페이지를 이동할 때마다 일어나게 됩니다.

**결과적으로, 어떤 문제가 있을지 예측이 불가능한 상태가 되는데요.** 이러한 문제들로 인해서 페이지 이동 시 원인을 알 수 없는 몇 가지의 버그들이 발생하고는 했습니다.
 

### 코드 파악, 상태 추적의 어려움

```js
// 2000줄이 넘는 코드 라인을 가진 Zca 클래스

class Zca {
  // 모든 변수, 상수 값이 생성자 함수 내부에 존재
  constructor() {
    약 200줄...
  }

  2000줄이 넘는 코드...
  ...
}

export default Zca;
```

> Zca는 ZumCommentArea를 의미합니다.
> 위에서 언급한 가독성과 관련된 문제를 Class 이름에서도 볼 수 있습니다.

기존의 댓글 모듈은 `JavaScript`와 `jQuery`로 이루어진 **레거시의 집합체**로 **클래스 하나에 약 2,000줄이 넘는 코드**를 가지고 있습니다. 시간이 지나며 복잡도는 더해졌고 이제는 기능을 더 추가하면서 유지보수를 하는 것이 불가할 정도였습니다. 그뿐만 아니라, 과거에 머물러 있는 문서들로는 댓글 모듈이 포함한 기능을 이해하기 어려웠습니다.

이러한 이유로 새로 런칭한 줌 투자 페이지의 댓글 모듈은 위에서 언급된 여러 가지 문제로 인하여 새롭게 다시 만들게 되었습니다.

> **이렇게 불필요한 업무의 중복을 발생시키는 댓글 모듈의 개선은 필수적이었습니다.**

또한, 기존의 댓글 모듈은 Mustache라는 Template Engine을 사용하여 UI를 관리하고 있었는데요.

```html
<!-- Mustashe를 사용한 기존의 파일 -->
<!-- 원래는 {% raw %}{{}}{% endraw %}을 사용하지만 {}으로 표현하였습니다. -->
<div class="date"> {cmntTime} </div>
  {#cmntMember}
      <a href="javascript:void(0);"
        name="cmnt_delete_a"
        data-seq="{cmntSeq}"
        data-area="{areaType}"
        class="btn_delete">
      삭제
      </a>
  {/cmntMember}
  {^cmntMember}
  <!-- 사용자에게 단순히 답글을 보여주거나 가리기 위해서 여러 조건문이 중첩되어 있으며 인라인 스타일과 클래스를 섞어서 사용 -->
      <a href="javascript:void(0);"
        class="btn_report {#blind}blind_not{/blind}"
        {#blind}{#showBlind}style="display: none"{/showBlind}{/blind}>
        신고
      </a>
  {/cmntMember}
</div>
```

[Zum Portal Core JS 소개](https://zuminternet.github.io/zum-portal-core-js/) 글에서도 언급되었듯이 Template Engine이 가지는 여러 가지 단점들이 개발에 불편함을 주었습니다.

- 같은 UI임에도 불구하고 중복되는 코드들
- 스타일 변경을 위한 조건문의 중첩
- 분리되지 않은 컴포넌트
- 상태 추적의 어려움


이러한 기존의 문제점들로 인해서 레거시 코드를 걷어내고 SPA에서 사용할 수 있는 새로운 소셜 댓글 모듈이 필요했고, **프론트파트 내에서 사내 라이브러리 배포를 통해 소셜 댓글 컴포넌트를 각 도메인에서 사용할 수 있도록 개선하는 파일럿 프로젝트**를 맡게 되었습니다.  

---

# 프로젝트 진행 과정

앞서 언급했던 여러 문제점을 해결하기 위한 리팩토링의 과정을 설명드리겠습니다.

- 주요목표와 기술 스택
- 컴포넌트 설계
- TDD의 시작

## 주요목표와 기술 스택

프로젝트의 주요 목표는 **댓글 모듈을 SPA에 적용할 수 있도록 만들기**로 기술스택은 아래와 같습니다. 

![07_techstacks.png](/images/front/post/2022-01-10-zum-comment-component/07_techstacks.png)

프론트엔드파트에서 담당하는 서브도메인에서 컴포넌트 라이브러리로 불러와 사용할 수 있도록 **어디에서나 재활용할 수 있도록 개선**해야했습니다.
![03_blueprint.png](/images/front/post/2022-01-10-zum-comment-component/03_blueprint.png)


## 컴포넌트 설계

프로젝트를 진행하면서 기존의 코드를 이해하고, 어떤 기능을 구현해야 하는지 감이 잘 잡히지 않았습니다. 기존의 댓글 모듈은 UI가 분리되어 있지 않아서 기능별로 컴포넌트를 분리하는 작업이 먼저 필요하다고 판단하였습니다. 댓글 모듈의 기능이 추가되고 스타일이 바뀌는 과정에서 문서는 그대로였기에 레거시로 남은 코드들을 파악하는 게 가장 힘들었던 것 같습니다. 하지만, 기존의 서비스를 이해하고 구현해야 할 기능들을 알기 위해서라도 컴포넌트를 분리하며 정리하는 과정이 필요했습니다.

![06_todolist.png](/images/front/post/2022-01-10-zum-comment-component/06_todolist.png)

이렇게 노션에 기존의 소셜 댓글 모듈이 가지고 있는 기능들을 하나하나 정리해나갔습니다.

#### 컴포넌트 폴더 구조

![04_directory.png](/images/front/post/2022-01-10-zum-comment-component/04_directory.png)
![05_directory.png](/images/front/post/2022-01-10-zum-comment-component/05_directory_2.png)

설계 이후, 구현해야 할 컴포넌트를 기능별로 나누니 프로젝트 진행을 위한 윤곽이 잡히기 시작했습니다. 처음 프로젝트를 진행할 당시에는 `모든 기능을 파악해서 놓치는 일이 없도록 해야지`라는 마음이 앞섰습니다. 그런 마음에, 무작정 기존의 레거시 코드들을 전부 이해하고자 코드만 보며 시간을 보내곤 했는데요. 이렇게 기능별로 컴포넌트를 구분한 이후에는 정리한 Task 문서를 토대로 **작은 기능들부터 차근차근 리팩토링해나갈 수 있었습니다.**

이렇게 작은 기능들부터 구현하며 상태를 관리해나가다 보니, (Vue, Vuex를 처음 사용해봄에도) Vuex Store 내부의 전역 상태들을 모듈로 자연스럽게 관리하게 되었습니다.

![11_modules.png](/images/front/post/2022-01-10-zum-comment-component/11_modules.png)

각 모듈은 상태, 뮤테이션, 액션, 게터를 가질 수 있습니다.

```ts
// index.d.ts line 123
export interface Module<S, R> {
  namespaced?: boolean;
  state?: S | (() => S);
  getters?: GetterTree<S, R>;
  actions?: ActionTree<S, R>;
  mutations?: MutationTree<S>;
  modules?: ModuleTree<R>;
}
```

또, 기존의 댓글 모듈은 중복되는 컴포넌트와 스타일이 매우 많았습니다. 이렇게 중복되는 코드들은 공통 컴포넌트로 재활용할 수 있도록 구분해가며 컴포넌트를 구현하였습니다.

![08_common.png](/images/front/post/2022-01-10-zum-comment-component/08_common.png)

#### 상수 값 분리

`Zca` 클래스는 생성자 함수 안에 정말 모든 값들을 가지고 있었습니다. ~~왜 그랬나요..~~

```js
class Zca {
  constructor() {
    this.zumInfo = {... 모든 URLs};
    this.indictInfo = {};
    this.deleteInfo = {};
    this.showNumInfo = { cmnt: 10, scmnt: 5, cmntIndex: 0, cmntListLength: 0 };
    this.paging = {...페이지네이션}
    this.electionInfo = { startDate: null, endDate: null }
    this.snsShare = { isShare: true };
    this.isLogin = '';
    this.loginedService = null;
    this.memberIdx = null;
    this.memberNick = null;
    this.memberCmntUrl = '/user_comment';
    this.orderInfo = '';
    this.orderType = {};

    ...
    ...많은 멤버 변수들...
  }
}
```

어디에서 사용되는지 파악하기 힘든 많은 값이 생성자 함수 내에서 관리되고 있었는데요. 어떤 값을 어디서 사용하게 되는지 정확하게 파악하기 위해서 상수들을 분리할 필요성이 있었습니다.

![09_const.png](/images/front/post/2022-01-10-zum-comment-component/09_const.png)

```ts
// constants.ts

// Cookies
export const LOGIN_COOKIE = '_ZIL';
export const BLIND_COOKIE = '_ZCB';

// Comment Response
export const CommentCreateResponse = {
  SUCCESS: 1,
  FAIL: 0,
  FAIL_BLOCK_WORD: -1,
  SUCCESS_BUT_BLIND_WORD: 2,
};

... more constants
```

> 기존에 존재하던 멤버 변수들은 대부분이 불필요한 값이였으며, 필요한 상수들만 모아서 정리하니 프로젝트를 진행하는 것이 더 수월해질 수 있었습니다.


## TDD (테스트 주도 개발)의 시작

이렇게 차근차근 구조를 만들어가고 기능을 구현하는 와중에도 **'잘하고 있는 건가?' 라는 의문**이 있었습니다. 아무래도 기존에 잘 작동되고 있던 모듈을 SPA를 위해 개선하는 것이다 보니 부담이 있었기 때문인데요.

또한, 아래와 같은 여러 가지 고민이 내면에서 떠오르고 있었습니다.
- 이미 운영되고 있는 서비스들을 내가 막 개선을 해도 될까?
- 개선 이후에 제대로 작동하지 않으면 어떡하지?
- 유지보수를 효율적으로 하려면?

테스트코드를 짜지 않는다면, 지금 리팩토링하고 있는 댓글 모듈도 누군가가 기능을 파악하기 위해 코드를 뜯어보고 문서를 훑어봐야 하는 상황이 오리라 싶었습니다. 더불어, 기능을 추가하거나, 수정을 해야 하는 상황에서 댓글 모듈이 확실하게 작동된다는 확신을 얻고자 했습니다. 결론적으로, **테스트코드를 통해서 불확실성을 없애고 추후의 유지보수 작업을 효율적으로 진행하고 싶었습니다.**

그렇게 TDD는 시작되었습니다.

## 테스트코드

테스트코드가 처음인 만큼 많은 우여곡절이 있었습니다. 테스트 프레임워크로는 `Jest`를 선택하였고, `Vuex`의 `Mutations`과 `Actions` 함수들을 중점적으로 **Unit Test를 진행**하였습니다.
> 많은 부분을 공식문서에 의지하며 TDD를 진행하였습니다.

TDD는 세 가지 단계를 반복하면서 개발을 하게 됩니다.

![10_tdd](/images/front/post/2022-01-10-zum-comment-component/10_tdd.png)

- 테스트 코드 작성
- 테스트를 통과하기 위한 코드 작성
- 리팩토링

이러한 과정들을 위해서 앞서 정리했던 기능 목록들을 바탕으로 시나리오를 작성한 이후, 테스트코드를 작성하고 개발을 진행하였습니다. 이를 통해서 불확실성을 제거하고 의존성이 낮은 함수들을 만들어가며 안정성 있는 개발을 할 수 있었습니다.

### 뮤테이션 (Mutations)

```ts
export type Mutation<S> = (state: S, payload?: any) => any;
```

> Vuex Store가 가진 상태(State) 값을 **변경**하기 위해서는 뮤테이션 함수를 사용해야 합니다.

뮤테이션과 관련된 테스트코드를 작성하는 것은 굉장히 간단했습니다.

예를 들어, 로그인을 완료한 유저의 정보를 관리하기 위해서 LoginStore라는 모듈에 데아터를 저장하고 싶다면 이러한 코드를 먼저 작성하게 됩니다. TDD를 위한 첫 발판으로 이제는 테스트코드를 작성하게 됩니다.

```tsx
export default {
  SET_LOGIN_MEMBER_INFO: (state, { memberInfo }) => {},
};
```

API 명세서를 보며 타입을 작성하고, 전달받을 유저의 정보를 Mock 객체로 만듭니다.

```tsx
import mutationTest from '../mutationTest';

// API 명세서를 참고한 타입 작성
export type MemberInfo = {
  memberIdx: string;
  nickname: string;
  loginedService: string;
};

// 뮤테이션 함수를 통해 상태를 변경하게 될 저장소
export type LoginStore = {
  memberInfo: MemberInfo;
};

// Mock 객체
export const mockMemberInfo: MemberInfo = {
  memberIdx: '6576143135935352832',
  nickname: '김선규',
  loginedService: 'ZUM',
};

describe('로그인과 관련한 뮤테이션 함수들', () => {
  it('로그인 된 유저의 상태를 저장한다.', () => {
    const state: LoginStore = {
      memberInfo: {
        memberIdx: '',
        nickname: '',
        loginedService: '',
      },
    };

    const payload = {
      memberInfo: { ...mockMemberInfo },
    };

    const { SET_LOGIN_MEMBER_INFO } = mutationTest;
    SET_LOGIN_MEMBER_INFO(state, payload);
    expect(state.memberInfo).toEqual({
      memberIdx: '6576143135935352832',
      nickname: '김선규',
      loginedService: 'ZUM',
    });
  });
});
```

- **describe**: 연관된 각 테스트를 그룹화하여 설명
- **it**: 진행하는 유닛 테스트
- **expect**: 들어오는 값이 특정 조건을 만족하는지 확인
- **.toEqual(value)**: expect의 메소드로 객체의 모든 속성 값이 정확히 일치하는지 확인 ("deep" equality)

해당 테스트를 돌리게 되면 아래와 같은 테스트의 실패를 확인 할 수 있습니다.

![12_mutation_fail](/images/front/post/2022-01-10-zum-comment-component/12_mutation_fail.png)

이제 테스트를 통과하기 위해서는 기존의 뮤테이션 함수를 수정해야합니다.

해당 테스트는 간단한 로직 추가를 통해 테스트를 통과할 수 있습니다.

```tsx
import type { LoginStore } from './__test__/login.spec';

type PayloadMemberInfo = Pick<LoginStore, 'memberInfo'>;

export default {
  SET_LOGIN_MEMBER_INFO: (
    state: LoginStore,
    { memberInfo }: PayloadMemberInfo
  ) => {
    state.memberInfo = memberInfo;
  },
};
```

![13_mutation_success](/images/front/post/2022-01-10-zum-comment-component/13_mutation_success.png)

### 액션 (Actions)

> 비동기 처리를 위해 사용되며, 내부에서 뮤테이션을 `commit`하여 상태를 변경합니다.

이렇게 전달받은 값을 뮤테이션을 통해 상태를 변경할 수 있게 되었다면, 액션을 이용해 API 함수를 호출하고 응답 값을 뮤테이션의 인자로 넘겨주는 테스트는 어떻게 진행해야할까요?

먼저 테스트하고자 하는 비동기 함수를 작성해줍니다.

```tsx
import type { Store } from 'vuex';
import type { LoginStore } from './__tests__/login.spec';

export default {
  async fetchLoginMemberInfo({ commit }: Store<LoginStore>) {},
};
```

저는 HTTP 통신 라이브러리로 `axios`를 사용했는데요. 테스트를 진행하기에 앞서서 `axios` 를 Mocking 하는 작업이 선행되어야 합니다. 이 과정을 통해서 **실제 환경과 테스트 환경을 분리**하게 됩니다. 이러한 작업이 필요한 이유는 **실제 API 요청을 보내는 것이 아니기 때문**입니다.

> 실제 API 요청을 테스트 도중 보내게 된다면 **실제 데이터 값이 변경될 수 있는 위험**이 있습니다.
> 또한, 불필요하게 테스트 시간이 더 길어질 수 있습니다.

타입스크립트 환경에서 axios 모듈을 Mocking 하기 위해 이러한 코드를 작성해 줍니다.

```tsx
import axios from 'axios';
jest.mock('axios');
export const mockedAxios = axios as jest.Mocked<typeof axios>;
```

더불어, 앞서 뮤테이션 함수에서도 사용했던 `MockMemberInfo` 도 가져와서 사용하며 테스트 코드를 작성합니다. 

> 테스트코드를 작성하다보면 스토어 내부에 있는 `state` 들과 `request` 그리고 `response` 값을 MocK으로 만들어 테스트하는 일이 잦아지게 되는데 이때 폴더를 분리하여 파일을 관리해주면 됩니다.
> 

```tsx
import { mockedAxios } from '../mocks/axios';
import { mockMemberInfo } from '../mocks/member';

import actions from '@/store/modules/login/actions';

import { API_END_POINT } from '@/consts/constants';

describe('로그인 유저의 정보를 가져오는 액션 함수들', () => {
  it('로그인 유저의 정보를 불러오는 API 함수를 호출하고 응답값을 뮤테이션 함수에 전달한다.', async () => {
    // commit 함수 Mocking
    const commit = jest.fn();
    const { fetchLoginMemberInfo } = actionsTest;
    let url = '';
    
    // API 호출시 이행된 프로미스를 전달
    mockedAxios.get.mockImplementationOnce((_url: string) => {
      url = _url;
      return Promise.resolve({ data: memberInfoMock });
    });

    // 비동기 함수 호출
    await fetchLoginMemberInfo({ commit });
    
    // URL 확인
    expect(url).toBe(`${API_END_POINT}/member/login`);
    
    // 뮤테이션 함수 및 전달 값 확인
    expect(commit).toHaveBeenCalledWith('SET_LOGIN_MEMBER_INFO', {
      memberInfo: memberInfoMock,
    });
  });
});
```

> [Vue 테스팅 핸드북](https://lmiller1990.github.io/vue-testing-handbook/ko/vuex-actions.html#%EC%95%A1%EC%85%98-%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0)에서는 액션 테스트를 통해 아래의 세 가지를 확인해야 한다고 설명해 주고 있습니다.
  - 사용한 API의 엔드포인트가 정확했는지?
  - 페이로드가 정확한지?
  - 결과적으로 올바른 뮤테이션을 커밋 했는지
> 

현재 테스트는 실제 함수에 아무런 로직도 작성되어 있지 않기 때문에 당연히 실패하게 됩니다.

**이제 이 테스트를 통과하기 위한 실제 코드를 작성해봅니다.**

```tsx
import axios from 'axios';
import { API_END_POINT } from '@/consts/constants';

import type { Store } from 'vuex';
import type { LoginStore } from './__tests__/login.spec';

export default {
  async fetchLoginMemberInfo({ commit }: Store<LoginStore>) {
    const PATH = 'member/login';
    const URL = `${API_END_POINT}/${PATH}`;
    const { data } = await axios.get(URL);

    commit('SET_LOGIN_MEMBER_INFO', { memberInfo: data });
  },
};
```

![14_action_success](/images/front/post/2022-01-10-zum-comment-component/14_action_success.png)


### 컴포넌트 테스트

프로젝트를 진행하면서 뮤테이션과 액션 함수를 테스트하는 것 뿐만 아니라, 몇몇 컴포넌트를 대상으로 컴포넌트 단위의 테스트를 진행하기도 하였습니다. 아래의 예시는 댓글 필터 컴포넌트의 데이터 변화를 확인하기 위한 테스트입니다.

> e2e 테스트를 프로젝트에 적용할 예정으로, 컴포넌트 단위의 테스트는 부분적으로만 적용하게 되었습니다.

![15_commentFilterTab](/images/front/post/2022-01-10-zum-comment-component/15_commentFilterTab.png)

댓글 목록을 필터링 해 줄 컴포넌트를 작성합니다.

```vue
<!-- CommentFilterTab.vue -->
<template>
  <div class="list_filter">
    <ul>
      <li class="newest">
        <button>최신순</button>
      </li>
      <li class="past">
        <button>과거순</button>
      </li>
      <li class="like">
        <button>추천순</button>
      </li>
      <li class="hate">
        <button>반대순</button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'CommentFilterTab',
});
</script>

<style lang="scss" scoped>
...style 관련
</style>
```

이제 사용자의 탭 클릭에 따라 가지고 있는 내부의 값이 false에서 true로 변경이 되어야 하는데요.

먼저 테스트코드를 작성해 봅니다. 여기서 중요한 점은 click 이벤트를 작동시킬 때, 클릭이 마무리될 때까지 기다려주기 위해서 `await` 을 앞에 써주어야 합니다.

```ts
import { shallowMount } from '@vue/test-utils';
import CommentFilterTab from '../CommentFilterTab.vue';

describe('CommentFilterTab.vue', () => {
  it('필터 리스트 버튼 클릭시 해당 버튼의 데이터는 true', async () => {
    // shallowMount를 통해 해당 컴포넌트가 가진 자식 컴포넌트들은 렌더링 하지 않습니다.
    const wrapper = shallowMount(CommentFilterTab, {
      data() {
        return {
          filters: {
            newest: true,
            past: false,
            like: false,
            hate: false,
          },
        };
      },
    });
    const likeTab = wrapper.find('.like');
    // 버튼이 브라우저에 존재하는지 확인하는 테스트는 통과합니다.
    expect(likeTab.exists()).toBe(true);
	  
    await likeTab.trigger('click');

    // 실패
    expect(wrapper.vm.$data.filters).toEqual({
      newest: false,
      past: false,
      like: true,
      hate: false,
    });
  });
});
```

테스트를 통과하기 위한 컴포넌트를 작성합니다.

```vue
<template>
  <div class="list_filter" @click="handleClickCommentFilterTab">
    <ul>
      <li class="newest">
        <button>최신순</button>
      </li>
      <li class="past">
        <button>과거순</button>
      </li>
      <li class="like">
        <button>추천순</button>
      </li>
      <li class="hate">
        <button>반대순</button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import type { FilterData } from './CommentFilterTab.type.ts'

export default Vue.extend({
  name: 'CommentFilterTab',
  data(): FilterData {
    return {
      filters: {
        newest: true,
        past: false,
        like: false,
        hate: false,
      },
    };
  },

  methods: {
    handleClickCommentFilterTab(e: MouseEvent) {
      const target = e.target as HTMLLIElement;
      if (!target.closest('LI')) return;

      const filterName = target.className;
      this.resetFiltersData();
      this.filters[filterName] = true;
    },

    resetFiltersData() {
      this.filters = {
        newest: false,
        past: false,
        like: false,
        hate: false,
      };
    },
  },
});
</script>
```

이렇게 작성된 컴포넌트는 테스트를 통과하게 됩니다.

> 컴포넌트 테스트를 통해서 화면의 변화가 어떻게 일어나는지 알게 되면서 브라우저에서 어떻게 변화가 일어나는지, 데이터가 어떻게 변경이 되는지 직접 확인하는 일이 점차 줄었습니다.

만약, Vuex Store에 있는 뮤테이션과 액션을 사용하는 컴포넌트 테스트를 짜기 위해서는 별도의 작업이 필요합니다. **사용되는 뮤테이션과 액션 함수들을 Mocking 하는 작업이 필요**한데요. Store에 정의를 따로 해주어야 <u>빨간 문장의 경고문을 피할 수 있습니다.</u> (테스트는 통과함)

```ts
import Vuex, { Store } from 'vuex';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import ComponentFilterTest from '../ComponentFilterTest.vue';

const localVue = createLocalVue();

localVue.use(Vuex);

describe('ComponentFilterTest.vue', () => {
  let store: Store<Record<string, unknown>>;
  let state = null;

  // 뮤테이션 함수 모킹
  const mutations = {
    사용되는 뮤테이션함수: jest.fn()
  };

  // 각 테스트가 실행될 때, Store를 초기화 해준다.
  beforeEach(() => {
    state = {};
    store = new Vuex.Store({
      state,
      mutations,
    });
  });

  it('필터 리스트 버튼 클릭시 해당 버튼의 데이터는 true', async () => {
    const wrapper = shallowMount(ComponentFilterTest, {
      localVue,
      store,
      data() { 컴포넌트 내부 데이터 },
    })
    ...테스트코드
  });
});
```

> 컴포넌트 내부에서 `Vuex`를 사용하는 경우에는 `createLocalVue`를 이용하여 테스트 내부에서 뮤테이션과 액션 함수들을 모킹해주는 작업이 따로 필요합니다.

컴포넌트 내부에서 Vuex Store에 존재하는 여러 모듈의 뮤테이션, 액션 함수들을 사용하다 보면 여러 곳에서 중복으로 사용하게 되는데요. 그때마다 `Store` 내부에 존재하는 모듈과 여러 함수들을 모킹 해주는 것은 비효율적인 일입니다. 이때, Store Mock을 만들어 사용한다면 조금 더 수월한 작업을 이어갈 수 있습니다. 더 나아가, 모듈이 커지게 된다면 분리하여 관리해준다면 좋을 것 같습니다.

```ts
// MockStore.ts
import Vuex from 'vuex';

export const createMockstore = () => {
  const modules = {
    commentFilterStore: {
      mutations: {
        '사용되는 뮤테이션함수': jest.fn(),
      },
    },
  };
  return new Vuex.Store({ modules });
};

// test.ts
describe('ComponentFilterTest.vue', () => {
  let store: Store<unknown>;

  beforeEach(() => {
    store = createMockstore();
  });
  
  it(...)
})
```

## 구현 과정에서의 어려움

컴포넌트를 설계하고 테스트코드를 짜며 리팩토링을 진행했음에도 구현 과정에서 여러가지 어려움들이 있었습니다. `Vue`를 처음 다루어 익숙하지 않았던 부분이 버그로 이어졌습니다. 비동기 처리와 관련된 부분들로 인해서 종종 애를 먹었습니다. 또한, 문서화가 잘 되어 있지 않았기 때문에 나중에서야 ~~(누구도 모르는)~~ 숨겨진 기능을 발견하고 급하게 기능을 구현하기도 하였습니다.

#### Vue 라이프 사이클과 비동기 처리

처음에는 Vue의 라이프 사이클인 `created`와 `mounted`의 차이를 정확히 이해하지 못해서 비동기 처리를 하는 부분에서 애를 먹었습니다. 특히, API 요청에 대한 응답 값을 받아 상태에 저장했음에도 불구하고 mount 된 컴포넌트에서 변화가 일어나지 않아서 원인을 찾기 위해 많은 시간을 소모했던 적이 있습니다. 한 예시로는 아이콘에 애니메이션 효과를 주기 위해서 API 응답 값을 사용해야 했던 것입니다.

```ts
// CommentIcons.vue
  computed: {
    voteType(): string {
      return (
        this.userCommentActions
          .filter(({ cmntSeq }) => cmntSeq === this.currentCommentSeq)
          .pop()
          .voteType ?? ''
      );
    },

  mounted():void {
    this.animateIcon(this.voteType);
  },
```

여기에서 `voteType`을 통해서 애니메이션 효과를 줄지 말지 결정하게 되는데요. `this.userCommentActions`라는 API 응답 값을 가지고 과거에 유저가 좋아요/싫어요를 눌렀는지 확인하고, 이에 맞는 `string('like'/'hate')` 값을 반환하게 됩니다. 이에 따라서 mount 된 이후 해당 아이콘에 애니메이션 효과를 주게 됩니다. 

![16_animateIcon](/images/front/post/2022-01-10-zum-comment-component/16_animateIcon.gif)

하지만, `userCommentActions`의 **값이 다 처리되지 않은 상태에서 mounted가 먼저 실행**되어서 종종 애니메이션 효과가 일어나지 않는 버그가 발생하였는데요. 이 부분을 해결하기 위해서 `watch`를 사용하여 응답 값을 보장받을 수 있도록 개선하였습니다.

```ts
  mounted(): void {
    // voteType 값이 들어왔다면 애니메이션 실행
    if (this.voteType) return this.animateIcon(this.voteType);

    // voteType 값이 아직 들어오지 않았다면 watch를 이용해 변경사항을 확인 후, watch 제거
    const $unwatchedVoteType = this.$watch('voteType', () => {
      this.animateIcon(this.voteType);
      $unwatchedVoteType();
    });
  },
```

#### SPA와는 맞지 않는 API 요청과 응답

또 다른 어려움으로는 참고하는 API 명세서가 불필요한 정보들을 많이 담고 있다는 것이었습니다. 기존 댓글 모듈의 코드를 보다 보면, `이게 도대체 어디서 사용되는거지?`라는 생각을 계속할 수밖에 없었는데요.

아무래도 기존의 API 설계는 `jQuery`를 사용한 직접적인 DOM 조작에 맞춘 것이다 보니, 현재 리팩토링하는 댓글 모듈에는 맞지 않다는 생각이 종종 들곤 했습니다. 대부분의 요청이 `Overfetching`으로 정말 많은 응답 값들을 한 번에 내려주곤 했습니다. 응답받은 데이터들이 기존에는 사용되었던 데이터들이었기에, 혹시나 놓치는 부분이 있지는 않을까 더블 체크를 하곤 했습니다.

> Overfetching 이란 하나의 정보를 얻기 위해서 다른 여러가지 불필요한 정보들도 함께 받게 되는 것을 말합니다.

---

## 사내 라이브러리 배포

테스트코드를 짜며 리팩토링을 해나가며 어려움들을 해결하니 댓글 모듈은 어느덧 완성이 되었고, 사내 라이브러리에 배포할 시간이 다가왔는데요.

이렇게 레거시를 걷어내고 Vue를 기반으로 만들어진 댓글 모듈은 프론트엔드파트에서 컴포넌트 라이브러리로 사용할 수 있도록 사내 Nexus(npm)에 배포하게 되었습니다.

저는 기본적으로 프로젝트의 환경을 `Vue-cli`를 통해 구성하였습니다. `Vue-cli`는 라이브러리를 배포하기 위한 별도의 스크립트를 지원해 주고 있습니다. 이를 통해 손쉽게 번들링을 진행하고 배포할 수 있었습니다.

```tsx
// package.json
"scripts": {
  "build:bundle": "vue-cli-service build --target lib --name index ./src/index.ts",
},
```

하지만, **손쉽게 만든 프로젝트 환경은 배포 과정에서 많은 삽질을 겪게 해주었습니다.**

번들링 된 파일을 확인하고 사용하려 하니 `cache-loader`의 에러, 불필요한 `css extraction`으로 인한 문제, `이미지 파일 용량으로 인한 문제` 등 예상치 못한 버그들이 발생하였습니다. 이러한 대부분의 문제들이 **`Vue-cli`를 통해 만들어진 환경이 어떻게 구성되어 있는지 모른다는 무지함에서 온 결과**였습니다.

> 이미지의 `limit` 값으로 인해서 배포된 컴포넌트가 필요한 이미지들을 가지지 못한 채로 번들링이 된 문제의 원인을 찾는 데 가장 많은 삽질을 했다.

이를 해결하기 위해서 `vue inspect` 명령어를 통해 production 환경에서의 패키지들을 확인한 후 `webpack chain`을 사용하여 추가적인 커스터마이징 작업을 거쳤습니다.

> webpack 설정을 위해 vue.config.js 다루어야했는데, 이 부분을 추가적으로 공부해야 하는 것이 webpack을 불필요하게 두 번 공부하는 느낌이였다.

```js
//vue.config.js

module.exports = {
  chainWebpack: (config) => {
    if (process.env.NODE_ENV === 'production') {
      // cache-loader 삭제
      config.module.rule('ts').uses.delete('cache-loader');

      // 이미지 limit를 늘렸음
      config.module
        .rule('images')
        .test(/\.(png|jpe?g|gif|webp)(\?.*)?$/)
        .use('url-loader')
        .loader('url-loader')
        .options({
          limit: 10240,
          options: {
            name: 'img/[name].[hash:8].[ext]',
          },
        });

      // ts-loader 옵션 수정
      config.module
        .rule('ts')
        .use('ts-loader')
        .loader('ts-loader')
        .tap((options) => ({
          ...options,
          transpileOnly: false,
          happyPackMode: false,
        }));
    }
  },

  // 라이브러리 번들링 과정에서의 에러를 해결하기 위해 수정
  parallel: false,
  css: { extract: false },  
};

```



> 처음 진행해 보는 vue 프로젝트로 환경을 vue-cli로 구성하였지만, 이후에는 `webpack` 혹은 `vite`를 사용하여 가볍게 번들링을 진행해야겠다는 생각이 들었습니다. 특히 vue inspect 명령어를 통해 어떤 환경에서 작업하는지 알아보고 수정하는 과정이 굉장히 수고스러운 일이었습니다. ~~(이럴 줄 알았다면 내가 다 처음부터 내가 설정...)~~

이러한 일련의 작업들을 마친 후, `build:bundle` 명령어를 통해 index.ts 파일을 번들링 하게 된다면 이런 결과를 얻을 수 있습니다.

![17_bundle](/images/front/post/2022-01-10-zum-comment-component/17_bundle.png)

여기서 라이브러리 배포를 위해 사용되는 파일은 `index.common.js` 파일로, 해당 모듈을 통해 댓글 컴포넌트를 import 하여 사용하게 됩니다. 이후 사내 nexus에 배포하기 위해 npm에 로그인을 진행한 후, `npm publish`로 번들링된 `dist` 폴더를 사내 [Nexus](https://www.sonatype.com/products/repository-oss)에 배포하게 됩니다.


> Nexus는 Maven, Docker, PyPI, npm 등의 패키지를 관리할 수 있는 설치형 Repository 입니다.

> Nexus 사내 라이브러리 배포과정이 더 자세히 알고 싶으시다면 [zum-portal-core-js의 '배포'를 참고해주세요](https://zuminternet.github.io/zum-portal-core-js/)


```ts
// index.ts
import ZumCommentModule from './views/ZumCommentModule.vue';
export { ZumCommentModule };
```


```json
// package.json
{
  "name": "zum-portal-comment",
  "version": "1.0.0",
  "author": "김선규 <skkim@zuminternet.com>",
  "main": "dist/index.common.js",
  "files": [
    "dist"
  ],
  "typings": "./dist/index.d.ts",
  "scripts": {
    ...
  },
  "publishConfig": {
    "registry": "줌인터넷 사내 라이브러리 주소"
  },
}
```

배포가 완료된 이후, `yarn add zum-portal-comment`명령어를 통해 패키지를 설치하여 댓글 모듈 컴포넌트를 불러와 사용할 수 있습니다.

```vue
<template>
  <zum-comment-module
    :options="{
      syscode: '시스템코드',
      articleIdx: '1234',
      targetUrl: 'https://zum.com',
      articleTitle: '댓글 모듈 리팩토링',
      articleUrl: 'https://zum.com',
    }"
  />
</template>

<script lang="ts">
import Vue from 'vue';
import { ZumCommentModule } from 'zum-portal-comment';

export default Vue.extend({
  name: 'App',
  components: {
    ZumCommentModule,
  },
});
</script>
```

![18_finish](/images/front/post/2022-01-10-zum-comment-component/18_finish.png)


> 잘 된다!
> 

---

# 느낀 점

기존에 존재하던 레거시 코드들을 뒤엎고 SPA에 맞춘 댓글 모듈을 만들면서 테스트코드도 짜보고 새로운 경험들을 할 수 있었습니다. 이 과정을 통해서 재활용이 가능한 컴포넌트들을 만들기 위해 많은 고민을 했으며, 특히 테스트코드를 짜면서 얻은 이점들이 많았다고 생각합니다.

### **DRY(Do not Repeat Yourself)**

더 쉬운 테스트, 더 나은 유지 보수를 생각하며 개발을 하다 보니, 반복적인 작업을 최소화하기 위해 노력했습니다. 지금 개선하는 댓글 모듈도 언젠가는 누군가의 레거시로 남겠지만, 테스트코드를 통해서 더 빠른 업무 파악이 가능하고 상태를 추적하는 일이 보다 쉬워질 거라 생각합니다.

### **관심사 분리(separation of concerns, SoC)**

비슷하고 반복되는 테스트 작성을 피하게 되면서 높은 추상화를 가지고 의존성이 낮은 컴포넌트를 만들어 재사용하기 위해 노력을 많이 했습니다. 왜냐하면 의존도가 높은 컴포넌트들이 테스트를 진행하기 어렵게 만들었으며 이런 부분들을 염두하면서 개발을 진행하다보니 좀 더 작은 컴포넌트 그리고 재사용을 하기 위해 고민을 하는 시간이 길어졌습니다.

폴더와 파일 구조부터 시작하여, 하나의 목적을 가진 컴포넌트들을 구성하며 저장소 또한 모듈별로 나누게 되었습니다.

![19_soc](/images/front/post/2022-01-10-zum-comment-component/19_soc.png)


특히, **서브도메인에서 사용되는 댓글 모듈은 약간씩 다른 기능을 가지고 있기 때문에** 몇몇 도메인에서는 특정 기능이 필요하지 않는데요. 이를 위해 `slot` 을 사용하여 사용하는 개발자가 **레고를 조립하듯이 모달 컴포넌트를 사용할 수 있도록 컴포넌트를 만들고자 하였습니다.**

```vue
<template>
  <div
    v-if="isOn"
    class="comment_layer_wrap"
    @click="handleClickOutsideModal"
  >
    <span class="layer_bg">
    <slot></slot>
  </div>
</template>
```

이렇게 슬롯을 가진 `BackgroundLayer` 컴포넌트는 다음과 같이 사용됩니다.

```html
<!-- background-layer 컴포넌트 내부에 원하는 모달을 추가하여 사용 -->
<background-layer>
  <login-modal />
  <report-modal />
</background-layer>

<background-layer>
  <login-modal />
  <report-modal />
  <my-comment-modal />
</background-layer>

<background-layer>
  <blind-alarm-modal />
</background-layer>
```

---

# 추후 개선 과제

사내 라이브러리에도 배포를 하고 댓글 모듈을 불러와서 사용할 수 있도록 개선을 하였습니다. 하지만 아직 개선해야 할 과제들이 많이 남아있습니다.

최종적으로, **프론트파트 내에서 댓글 모듈을 사용하여 도메인에 맞는 댓글 모듈로 재조합할 수  있도록 개선하는 것** 입니다.

현재는 <u>각 서브 도메인마다 조금씩 다른 UI와 기능들이 존재합니다.</u> 이를 위해서 댓글 모듈에 `prop`으로 전달되는 데이터를 사용하여 어떤 도메인에 사용되는지 판단하고 렌더링을 하게 되는데요. 추가적으로 데이터가 더 필요하다면 개발자는 더 많은 데이터를 입력해야 하는 불편함이 있습니다.

![20_plan](/images/front/post/2022-01-10-zum-comment-component/20_plan.png)


이러한 부분을 해결하기 위해 추가적으로 아래 예시 사진처럼 댓글 모듈을 개선할 예정입니다.

```vue
<template>
  <zum-comment-wrapper>
    <comment-text-box>
      <comment-icons />
    </comment-text-box>
    <comment-list props="comment-data" />
    <background-layer>
      <login-modal isOn:false />
      <policy-modal isOn:false />
    </background-layer>
  </zum-comment-wrapper>
</template>

<script lang="ts">
import Vue from 'vue';
import {
  ZumCommentWrapper,
  CommentIcons,
  CommentTextBox,
  LoginModal,
  CommentList,
  PolicyModal,
} from 'zum-portal-comment';

export default Vue.extend({
  name: 'App',
  components: {
    ZumCommentModule,
  },
});
</script>
```

> 비슷하지만 조금씩 다른 컴포넌트들을 프론트 파트 내에서 레고처럼 재조합하여 사용할 수 있도록 만들 계획 

# 마무리

줌인터넷에 입사하여 진행한 파일럿 프로젝트가 이미 잘 운영되고(?) 있는 댓글 모듈을 개선하는 것이었기 때문에 부담감이 있었던 것은 사실입니다. 처음 마주하는 방대한 레거시들은 정말 상상을 뛰어넘었고, 리팩토링이라는 말보다 ‘새롭게 만든다.’ 라는 말이 어울렸습니다. 하지만 이와 동시에 신입 개발자로서 **테스트코드를 공부하고 다른 팀원들을 위해 컴포넌트 라이브러리를 만들 수 있는 좋은 기회**이기도 했습니다.

파일럿 프로젝트를 진행하면서 다른 팀원들에게 들었던 말은 `선규 님이 테스트코드를 공부해서 프론트파트에 전파하면 될 것 같아요` 라는 말이었습니다. 2022년을 시작으로 프론트파트는 테스트코드를 모든 프로젝트에 도입하는 것을 목표로 삼고 있으며, 이를 위해서 추가적인 스터디를 진행할 예정에 있습니다.

많이 부족할 수 있는 글이지만, 제 경험과 고민들이 누군가에게 도움이 되면 좋겠습니다.

감사합니다.