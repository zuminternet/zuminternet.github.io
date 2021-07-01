---
layout: post
title: "카페 형식 게시판 구현 - 파일럿 프로젝트"
description: Spring Boot와 Vuejs를 이용한 동적인 게시판 구축하기
image: /images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/wallpaper2.png
introduction: Spring Boot와 Vuejs를 이용한 동적인 게시판 구축하기
category: portal/pilot
tag: [springboot, vue.js, pilot]
---

줌인터넷에는 **"파일럿 프로젝트"** 라는 좋은 개발 문화가 있습니다.
신입 개발자들이 실무에 들어가기 전 전반적인 웹 서비스 개발 기술을 숙지하고 개인 및 업무 역량을 강화할 수 있도록 도와주는 것이죠.<br>
파일럿 프로젝트를 통해서 앞으로 사용할 기술에 대한 두려움을 없앨 수 있었고 실무에서 수도 없이 많이 마주하게 될 문제들을 미리 경험해보면서 스스로 해결할 수 있는 능력을 강화시키고 위기를 극복함으로써 개발에 대한 자신감을 얻을 수 있었습니다.

> **[목차]**
> - 개요
>   - 프로젝트 주제 및 개발 스펙
>   - 프로젝트 상세 기능 
> - Project Architecture
> - FrontEnd
>   - VueRouter 구성
>   - 컴포넌트 구성
>   - Vuex, 상태 관리 도구
> - BackEnd
>   - 사용자 인증 과정
>   - 접근 권한 제어
>   - Class구조 
>   - 기본적인 Client 요청 처리 과정 
> - 맺음말 

---

## 개요
### 프로젝트 주제 및 개발 스펙
게시판 구현은 웹 서비스 개발에 있어서 가장 기본적인 프로젝트라고 생각합니다. 기본적인 CRUD 기능과 FrontEnd와 BackEnd 간의 통신 및 데이터 전달을 구현해볼 수 있기 때문입니다. <br>
저의 파일럿 프로젝트는 바로 기본적인 게시판 기능들과 함께, 하나의 게시판이 아닌 **여러 개의 게시판을 생성할 수 있는 카페 형식의 게시판**을 구현하는 것이었습니다. 여기에 **태그**(이하 키워드)에 해당하는 기능으로 게시글에 키워드를 달 수 있고, 사용자 또한 자신 만의 키워드를 등록하여 키워드와 관련된 게시글을 쉽게 볼 수 있도록 하는 기능이 추가되었습니다.

- 프로젝트 개발 스펙으로 주어진 내용은 아래와 같습니다.
![개발 스펙](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/tech-spec.png)

### 프로젝트 상세 기능
![프로젝트 전체 구조도](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/function-spec.png)

---

## Project Architecture 
- Spring Boot, Vue.js를 사용한 프로젝트 전체 구조도
![프로젝트 전체 구조도](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/project-architecture.png)
  - 구글 Oauth를 통한 소셜 로그인
  - Vue.js Framework 를 이용한 FrontEnd
    - ElementUI를 이용한 Component 구성 
    - Vuex를 이용한 상태 관리 
  - axios를 이용한 API 호출
  - Spring Security를 이용한 인증 및 권한 제어 
  - Spring Boot Framework를 이용한 BackEnd

<!-- ## 설계 과정
### 1. 테이블 설계
- 그림
- pk는 integer로 사용
  - **WHY?** 
- keyword는 

### 2. API 설계
![API 구조](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/api-structure.png)

### 3. UI 설계 
- 아래 FrontEnd 컴포넌트 구성 참고  -->

---

## FrontEnd
### 1. Vue Router 구성
- 기본 Route 구성 
![최상위 라우터 구성](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/root-component-structure2.png)
  - ***Vue Router:*** Vue를 이용한 SPA를 제작할 때 유용한 라우팅 라이브러리
  - 가장 기본적인 UI 구성으로 위와 같은 4개의 기본 페이지를 생각하였고, 이 기본 페이지를 최상위 컴포넌트로 구성하였습니다.
  - Vue Router을 이용하여 4개의 최상위 컴포넌트(여러 하위 컴포넌트들로 구성)로 이동할 수 있습니다.

- 중첩된 Route 구성 
![중첩 라우트 구성](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/nested-route-structure.png)  
  - 각각의 post마다 고유한 id가 존재하기 때문에 페이지별 url이 필요하다는 생각을 하게 되었고 이를 위해서 Vue의 중첩 라우트를 구성하게 되었습니다.
  - route 아래 children에 선언한 url로 요청이 들어온다면 최상위 컴포넌트에 구성되어 있는 `<router-view>` 내에 원하는 Component를 랜더링하게 됩니다. 
  - Ex) MainPageLayout 컴포넌트
    ![MainPage router-view 예시](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/mainpagelayout-example.png) 


```js
// MainPageLayout route 구성
{
  path: "/boards",
  name: 'Main',
  component: MainPageLayout,
  children: [
    {
      path: ":boardId",
      name: 'PostList',
      component: PostListView,
      props: true,
    },
    {
      path: "posts/:postId",
      name: 'PostDetail',
      component: PostDetailLayoutView,
    },
    {
      path: ":boardId/create",
      name: 'CreatePost',
      component: PostFormLayoutView,
    },
    {
      path: ":boardId/:postId/modify",
      name: 'ModifyPost',
      component: PostFormLayoutView,
    }
  ]
},
```  
```html
<!-- MainPageLayout.vue의 template 내용 -->
<template>
<div>
  <header-view></header-view>
  <el-container class="element-container">
    <el-aside width="230px">
      <board-list-view @getPostsByBoardId="getPostsByBoardId" @handleSelect="setNavDepth"></board-list-view>
      <widget-view v-if="user.id"></widget-view>
    </el-aside>
    <el-main>
      <location-nav-view>
        <el-breadcrumb-item slot="main-location" :to="{ path: '/' }">homepage</el-breadcrumb-item>
      </location-nav-view>

      <!-- 중첩 라우트의 children에 따라 원하는 Component를 랜더링 -->
      <router-view></router-view>

    </el-main>
  </el-container>
</div>
</template>
```

### 2. 컴포넌트 구성
- 4개의 최상위 컴포넌트에 대한 구체적인 컴포넌트 구성은 아래와 같습니다.
  - ***Vue Component:*** 화면에 비춰지는 Vue를 쪼개어 재활용이 가능한 형태로 관리하는 단위
  - 색이 칠해져 있는 컴포넌트는 재사용된 컴포넌트를 의미합니다.
![전체 컴포넌트 구성](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/total-component-structure.png)


### 3. Vuex, 상태 관리 도구
- Vue는 **Reactive** 하다.
  - ***반응성(Reactivity):*** 데이터가 변함에 따라 Vue에서 반사적으로 화면을 변화시키는 특성
  - 즉, 웹 페이지 상의 상태값 변화에 따라 Vue에서 자동으로 화면을 랜더링합니다.
- 모든 컴포넌트는 각각 자신의 scope를 갖기 때문에 하위 컴포넌트가 상위 컴포넌트의 값을 바로 참조할 수 없습니다. 다시 말해 Vue는 기본적으로 컴포넌트 간의 **직접적인 통신은 불가능**하도록 되어 있습니다.

- Vue에서의 기본적인 컴포넌트 통신 방법
![vue 기본 데이터 흐름](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/basic-vue-flow.png)  
  - 상위-하위 관계
    1. 하위 컴포넌트에서 이벤트가 발생한다.
    2. 하위 컴포넌트는 상위 컴포넌트에 이벤트가 발생한 사실을 알린다. (`$emit()`이용)
    3. 상위 컴포넌트는 이벤트에 맞게 적절한 데이터를 조작한다. (`axios` 이용)
    4. 조작한 데이터를 하위 컴포넌트에 `props 속성`을 통해 전달한다.
    5. 상위 컴포넌트로부터 받은 데이터에 따라 하위 컴포넌트의 화면이 갱신된다.
  - 동일 레벨 관계 (동일한 상위 컴포넌트를 가진 2개의 하위 컴포넌트 간의 통신)
    - 하위 -> 상위 -> 다른 하위 컴포넌트
  - 상위 컴포넌트가 없는 하위 컴포넌트 간의 통신
    - Event Bus 활용 

- 문제점??
  - 이런 기본적인 통신 방법으로 구현을 하다보니, 상위-하위 관계의 중간에 거쳐야 할 컴포넌트가 많은 경우에 이벤트를 알리거나 데이터를 전달하는 많은 **코드가 중복**되는 것을 알 수 있었습니다.
  - 또한 중간에 새로운 컴포넌트를 추가하거나 변경하였을 때 **유지보수가 어렵다**는 것도 쉽게 느낄 수 있었습니다.
  - Event Bus를 사용하는 경우 또한 복잡한 이벤트 처리에는 좋지 않으며, 컴포넌트가 전역 scope의 이벤트를 참조해야 하기 때문에 데이터 충돌 등에 대한 이슈가 발생할 수 있다는 문제점도 있습니다.
- 해결 방법??
  - 해당 프로젝트를 대규모라고 하긴 어렵지만, 컴포넌트를 재사용이 가능한 수준으로 최대한 잘게 쪼갰기 때문에 컴포넌트 간의 데이터 전달에 대해 좀 더 유기적으로 관리할 필요성을 느꼈습니다.
  - 이를 위해 Vue의 상태를 관리하는 라이브러리인 **Vuex**를 사용하게 되었습니다.
  - ***상태 관리(State Management):*** 컴포넌트 간 데이터 전달 및 이벤트 통신 등의 여러 컴포넌트의 관계를 한 곳에서 관리하기 쉽게 구조화하는 것

- Vuex를 통해 **중앙집중식**으로 상태 정보를 관리할 수 있게 되어 모든 컴포넌트들이 동일한 조건에서 접근할 수 있게 되었고 이에 따라 **효율적으로 상태값을 조작**할 수 있었습니다.
![vuex 기본 데이터 흐름](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/vuex-flow.png)  

```js
/** Vue Components */
// dispatch를 통해 actions를 호출
getPostListOfRelatedOneKeyword(keywordId, pageNum) {
  this.$store.dispatch("fetchPostListSelectedKeywordByPageNum", {
    keywordId: keywordId,
    pageNum: pageNum 
  }).then(() => {
    console.log("해당 키워드 관련 글 가져오기 성공!")
    this.postsListData = this.postsRelatedUserKeyword.posts;
  })
  .catch((error) => {
    console.log("해당 키워드 관련 글 가져오기 실패!");
    console.log(error);
  });
},
```
```js
/** Actions */
// 선택한 키워드 관련 글을 가져오는 API 호출 + commit을 통해 mutation을 호출
[Type.FETCH_POST_LIST_SELECTED_KEYWORD_BY_PAGENUM]: ({ commit }, { keywordId, pageNum }) => {
  const typeName = Type.FETCH_POST_LIST_SELECTED_KEYWORD_BY_PAGENUM;

  return new Promise((resolve, reject) => {
    postApi.fetchPostListSelectedKeywordByPageNum(keywordId, pageNum)
      .then(({ data }) => {
        console.log(data);
        commit(typeName, data);
        resolve();
      })
      .catch(error => {
        console.log(error);
        reject(error);
      });
  });
},
```
```js
/** API */
// 선택한 키워드 관련 글 가져오기 
[Type.FETCH_POST_LIST_SELECTED_KEYWORD_BY_PAGENUM](keywordId, pageNum) {
  return axios.get(`${config.apiUrl}posts/keywords/${keywordId}/list`, { 
    params: { page: pageNum }
  });
}
```
```js
/** Mutations */
// 선택한 키워드 관련 글에 해당하는 state 값 setter
[Type.FETCH_POST_LIST_SELECTED_KEYWORD_BY_PAGENUM](state, payload) {
  state.postsRelatedUserKeyword = {
    posts: payload.posts,
    totalPostCount: payload.totalPostCount
  }
  state.totalPostsCount = payload.totalPostCount; 
},
```

---

## BackEnd
### 1. 사용자 인증 과정
- Spring Security와 Oauth2를 적용한 인증 과정 흐름은 다음과 같습니다.
![사용자 인증 과정 흐름도](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/user-authentication.png)

1. 사용자가 구현한 Web Application(SpringBoot Tomcat Server)에 접속
2. HttpSession에 바인딩된 user 객체가 있는지 확인
  - **YES**: 세션에 바인딩된 user 객체를 반환(`session.getAttribute("user")`)
  - **NO**: 3번 진행
3. Google Oauth로 로그인을 수행
    - 로그인 성공시, google 계정의 profile 정보가 SecurityContext의 Authentication에 저장된다.
    - sub, name, given_name, family_name, profile, picture, email, email_verified, locale, hd 등의 값
4. Authentication에 저장된 정보를 통해 가입된 사용자인지 확인
    1. Authentication(인증된 사용자의 정보)에서 email 정보를 가져온다.
    `authentication.getPrincipal().getAttributes().get("email")`
    2. userRepository의 `findByEmail()`를 통해 가입된 사용자인지 확인한다.
      - **YES**: 해당 user 객체를 세션에 바인딩(`session.setAttribute("user")`) 후 반환
      - **NO**: 5번 진행
5. Authentication에 저장된 정보를 통해 새로운 객체를 생성
    1. user 객체를 생성하는데 필요한 정보들을 가지고 새로운 객체를 생성한다.
    2. 새로운 user 객체에 원하는 권한을 부여한다.
    3. userRepository의 `save()`를 통해 DB에 해당 객체를 저장한다. 
    4. 마찬가지로 새롭게 생성한 user 객체를 세션에 바인딩(`session.setAttribute("user")`) 후 반환

### 2. 접근 권한 제어
#### 1. Spring Security 설정을 통한 URL 접근 제어
- Java Config에서의 Spring Security 설정을 통해 아래와 같이 접근 권한을 제어할 수 있습니다.

```java
httpSecurity
  .authorizeRequests() // 인증 메커니즘 요청 설정 (요청 패턴 설정, 접근 허용 여부)
    .antMatchers("/admin/**").hasAuthority(ADMIN.getRoleName()) // admin page
    .antMatchers("/mypage/**").hasAnyAuthority(ADMIN.getRoleName(), USER.getRoleName()) // my page

    .antMatchers(HttpMethod.POST, "/api/**").hasAnyAuthority(ADMIN.getRoleName(), USER.getRoleName()) // 생성, 수정, 삭제
    .antMatchers(HttpMethod.PUT, "/api/**").hasAnyAuthority(ADMIN.getRoleName(), USER.getRoleName())
    .antMatchers(HttpMethod.DELETE, "/api/**").hasAnyAuthority(ADMIN.getRoleName(), USER.getRoleName())

    .antMatchers("/", "/loginSuccess", "/main/**", "/boards/**", "/posts/**", "/api/**").permitAll()
    .antMatchers("/login/**", "/oauth2/**", "/css/**", "/images/**", "/js/**", "/console/**").permitAll()

    /* 그 외에 인증되지 않은 사용자는 접근 불가능 (redirect login) */
    .anyRequest().authenticated() // 설정한 요청 이외의 요청은 인증된 사용자만이 요청 가능
```
- <mark>TIP</mark> hasAuthority와 hasRole의 차이?
  - `hasRole` 등 Role을 접미사로 사용하는 메서드는 **ROLE_** 이라는 접두사를 사용하는 권한을 체크
    - 즉, hasRole("ADMIN")을 사용하면 자동으로 앞에 ROLE_을 붙여주기 때문에 "ROLE_ADMIN"이 됩니다.
  - Spring Security 4에서는 `hasAuthority`를 사용하며, 
    - hasAuthority("ROLE_ADMIN")과 hasRole("ADMIN")은 동일합니다.
  - 저는 권한에 ROLE_ 접두사를 붙이지 않았기 때문에 hasAuthority를 사용하여 접근 권한을 확인하였습니다.


#### 2. Custom Security Expression을 통한 UPDATE, DELETE 접근 제어
- 본인이 작성한 게시글이나 댓글에 대해서만 수정하고 삭제할 수 있도록 접근을 제어해야 합니다.
  - 우선, 기본적으로 FrontEnd 구현에서 작성자에게만 수정, 삭제 버튼이 보이도록 합니다.
  - 또한 간접적으로 해당 API를 호출하는 경우를 대비하여 BackEnd에서의 처리도 필요합니다.
    - 이를 위해 Custom Annotaion을 구현하여 수정, 삭제에 대한 기능을 수행하는 메서드단에서 해당 기능에 대한 접근을 제어하였습니다.
- Custom Annotaion 구현
  - **장점**
    - 게시글 또는 댓글의 수정 및 삭제 권한에 대한 중복 로직을 **AOP(관점 지향 프로그래밍) 기반**으로 처리할 수 있도록 annotaion을 통해 접근을 제어하였습니다.
    - 또한 해당 방법을 통해 URL 단의 접근 제어가 아닌 **메서드 단에서의 보안**을 위한 권한을 확인하는 기능을 수행할 수 있습니다.
    - Annotaion으로 로직을 처리하기 때문에 **간단하게 사용이 가능**하다는 장점도 있습니다. 단지 권한 체크가 필요한 Controller 메서드에 해당 Custom Annotation만 달면 원하는 동작을 수행할 수 있습니다.
  - **구현 과정**
    1. PermissionEvaluator Interface 구현체 CustomPermissionEvaluator 정의
        - `hasPermission` 메서드를 오버라이드
          - 접근 권한을 확인할 target의 Object 또는 id를 parameter로 받아 적절한 로직을 구현합니다.
          - 해당 프로젝트에서는 target의 pk를 parameter로 넘겨받아 Service Layer로부터 해당 target Object를 가져오는 과정을 수행하였습니다. 
        - hasPermission 메서드 구현 내용 
          - 해당 게시글 또는 댓글에 대한 권한이 있으면 return true, 없으면 return false
          - 즉, 게시글 또는 댓글의 작성자가 해당 Controller의 사용을 요청하는 사용자(현재 인증된 사용자)인지 확인하는 과정을 수행합니다.
    2. Java Config에서의 MethodSecurity 설정 
        - `@PreAuthorize`을 사용하기 위해 prePostEnabled 활성화 
        - CustomPermissionEvaluator에서 사용할 Bean들을 생성자로 주입
        - ExpressionHandler에 CustomPermissionEvaluator를 set 
    3. Controller Method 단에서의 Custom Annotation 사용 
        - `@PreAuthorize("hasPermission(#postId, 'post', 'delete')")`와 같이 사용
        - cf. parameter로 Object를 넘겨 받는 경우는 `@PreAuthorize("hasPermission(#post, 'delete')")`와 같이 사용 

```java
// 1. PermissionEvaluator Interface 구현체 CustomPermissionEvaluator 정의
@AllArgsConstructor
@NoArgsConstructor
@Component
public class CustomPermissionEvaluator implements PermissionEvaluator {

    private MessageSourceAccessor messageSourceAccessor;
    private PostService postService;
    private CommentService commentService;

    private static final Logger log = LoggerFactory.getLogger(CustomPermissionEvaluator.class);

    @Override
    public boolean hasPermission(Authentication authentication, Object targetDomainObject, Object permission) {
       throw new UnsupportedOperationException("This method is not supperted by this application");
    }

    /**
     * 해당 객체의 수정, 삭제 권한이 있는지 확인하는 메서드
     *
     * @param authentication 현재 인증된 사용자의 정보
     * @param targetId 접근 권한을 확인할 타겟 객체의 pk
     * @param targetType 타겟 객체의 클래스 타입
     * @param permission 인자로 받은 String data
     * @return 해당 객체의 수정, 삭제 권한이 있으면 return true, 없으면 throw UnAuthorizedException
     */
    @Override
    public boolean hasPermission(Authentication authentication, Serializable targetId, String targetType, Object permission) {
        if ((authentication == null) || (targetId == null) || (targetType == null) || !(permission instanceof String)) {
            return false;
        }
        int convertId = (int) targetId;
        String targetTypeUpper = targetType.toUpperCase();
        log.debug("target 객체의 pk, target 클래스 type: {}", convertId + ", " + targetTypeUpper);

        boolean result = checkIsOwner(authentication, getTargetObject(convertId, targetTypeUpper), permission.toString().toUpperCase());
        if (!result) {
            throw new UnAuthorizedException(messageSourceAccessor.getMessage(ErrorMessage.UNAUTHORIZED.getMessageKey()));
        }
        return true;
    }

    /**
     * targetType 에 따라 Service Layer 에서 해당 객체를 가져와 Object 로 반환하는 메서드
     */
    private Object getTargetObject(int targetId, String targetType) {
        if ("POST".equals(targetType)) {
            return postService.getPostById(targetId);
        } else if ("COMMENT".equals(targetType)) {
            return commentService.getCommentById(targetId);
        }
        return null;
    }

    /**
     * 현재 로그인한 사용자에 target 객체를 수정/삭제할 권한이 있는지 확인하는 메서드
     * 권한이 있으면 return true, 없으면 return false
     */
    private boolean checkIsOwner(Authentication auth, Object targetDomainObject, String permission) {
        if (targetDomainObject == null) {
            throw new NotFoundException(messageSourceAccessor.getMessage(ErrorMessage.NULL_OBJECT.getMessageKey()));
        }

        String userPrincipal = getUserPrincipal(auth);

        if (targetDomainObject instanceof Post) {
            return isOwnerOfPost((Post) targetDomainObject, userPrincipal);
        } else if (targetDomainObject instanceof Comment) {
            return isOwnerOfComment((Comment) targetDomainObject, userPrincipal);
        }
        return false;
    }

    /**
     * 현재 로그인한 사용자의 Principal 값에서 "sub" Key 값의 value 를 반환하는 메서드
     */
    private String getUserPrincipal(Authentication authentication) {
        Map<?, ?> map = (Map<String, Object>) authentication.getPrincipal();
        return map.get("sub").toString();
    }

    private boolean isOwnerOfPost(Post post, String userPrincipal) {
        return post.isOwner(userPrincipal);
    }

    private boolean isOwnerOfComment(Comment comment, String userPrincipal) {
        return comment.isOwner(userPrincipal);
    }
}
```
```java
// 2. Java Config에서의 MethodSecurity 설정 
@AllArgsConstructor
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true, securedEnabled = false, jsr250Enabled = false)
public class MethodSecurityConfig extends GlobalMethodSecurityConfiguration {

    private final MessageSourceAccessor messageSourceAccessor;
    private final PostService postService;
    private final CommentService commentService;

    @Override
    protected MethodSecurityExpressionHandler createExpressionHandler() {
        CustomPermissionEvaluator customPermissionEvaluator = new CustomPermissionEvaluator(messageSourceAccessor, postService, commentService);

        DefaultMethodSecurityExpressionHandler expressionHandler = new DefaultMethodSecurityExpressionHandler();
        expressionHandler.setPermissionEvaluator(customPermissionEvaluator);

        return expressionHandler;
    }
}
```
```java
// 3. Controller Method 단에서의 Custom Annotation 사용
/**
  * 해당 게시글 삭제하기
  * @param postId 특정 게시글의 id
  */
@IsUser
@PreAuthorize("hasPermission(#postId, 'post', 'delete')")
@DeleteMapping("/{postId}")
public ResponseEntity delete(@PathVariable int postId) {
    postService.deletePost(postId);
    return ResponseEntity.ok().build();
}
```

### 3. Class 구조 
![BackEnd 기본 흐름](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/spring-backend-flow.png)
- DAO와 Entity의 개념 
  - ***DAO(Data Transfer Object):*** 계층 간 데이터 교환을 위한 클래스
  - ***Entity:*** 실제 DB의 table과 매칭되는 클래스 
- <mark>TIP</mark> Entity 클래스와 DTO 클래스를 분리하는 이유?
  - Domain Model을 아무리 잘 설계했다고 해도 각 View 내에서 Domain Model의 getter만을 이용해서 원하는 정보를 표시하기가 어려운 경우가 종종 있습니다. <br> 이런 경우 Domain Model 내에 Presentation을 위한 필드나 로직을 추가하게 되는데, 이러한 방식이 모델링의 순수성을 깨고 Domain Model 객체를 망가뜨리게 됩니다.
  - 또한 Domain Model을 복잡하게 조합한 형태의 Presentation 요구사항들이 있기 때문에 Domain Model을 직접 사용하는 것은 어렵습니다.
  - 즉, DTO는 Domain Model을 복사한 형태로 다양한 Presentation Logic을 추가한 정도로 사용하며, Domain Model 객체는 Persistent만을 위해서 사용합니다.

### 4. 기본적인 Client 요청 처리 과정 
#### 1. Client의 API 호출
- 사용자(`USER`) 권한을 가진 Client가 댓글을 저장하기 위해 Server에 아래와 같이 요청합니다.
  - `POST http://localhost:8080/posts/3/comments`
- Client가 작성한 댓글의 내용이 담긴 json 형태의 text를 Request Body에 담습니다. (PUT 또는 POST의 경우에만 Request Body에 내용이 존재합니다.)
  - `{  "content" : "정말 유익한 내용이네요~!"  }`

#### 2. Client 권한 체크 및 URL Mapping 처리 
Server에서는 Client의 요청 url과 맞는 controller method를 찾아 실행시킵니다. <br>
인증된 Client인지, 관리자/사용자 권한을 가진 Client인지를 확인한 후 해당 method를 수행합니다. 

```java
// 권한 enum class
public enum Role {
    ADMIN("관리자"),
    USER("사용자");
}
```
```java
// 인증된 사용자 및 권한 체크에 대한 Custom Annotaion
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@PreAuthorize("isAuthenticated() and hasAnyAuthority('관리자', '사용자')")
public @interface IsUser {}
```

#### 3. ApiController 역할 
Controller는 Client 요청으로부터 Request Body 데이터를 DTO로 받아 유효성 검사를 한 후, 적절한 Service에 인자로 넘겨 해당 Service를 호출합니다. 

```java
@NoArgsConstructor
@AllArgsConstructor
@Getter
public class CommentRequestDto {
    @NotBlank
    @Size(max = 200)
    private String content;

    public Comment toEntity(Post post) {
        return new Comment(this.content, post);
    }

    public Comment toEntity() {
        return new Comment(this.content);
    }
}
```
```java
/**
  * 해당 게시글에 댓글 생성하기
  *
  * @param postId 댓글을 생성할 특정 게시글의 id
  * @param commentRequestDto 댓글 제목과 내용에 대한 Request DTO
  * @param loginUser 현재 로그인한 사용자
  * @return 생성한 댓글에 대한 ResponseEntity CommentDto
  */
@IsUser
@PostMapping("/{postId}/comments")
public ResponseEntity<CommentDto> create(@PathVariable int postId, @RequestBody @Valid CommentRequestDto commentRequestDto, @LoginUser User loginUser) {
    return ResponseEntity.status(HttpStatus.CREATED).body(commentService.saveComment(postId, commentRequestDto, loginUser));
}
```

#### 4. Service 역할 
요청에 따른 Business Logic을 수행합니다.
- Controller로부터 넘겨받은 데이터(DTO)를 Entity로 변환합니다.
- 변환한 Entity를 Repository를 통해 DB에 저장합니다.
- 저장 후 Repository를 통해 넘겨받은 Entity를 다시 DTO로 변환하여 반환하게 됩니다.

```java
/**
  * 댓글의 내용을 받아 저장하는 메서드
  *
  * @param postId 댓글을 작성한 게시글의 id
  * @param commentRequestDto 댓글 내용에 대한 comment Request DTO
  * @param loginUser 로그인한 사용자
  * @return 생성한 댓글의 CommentDTO
  */
@Transactional
public CommentDto saveComment(int postId, CommentRequestDto commentRequestDto, User loginUser) {
    Post post = postService.getPostById(postId);
    Comment comment = commentRepository.save(commentRequestDto.toEntity(post));

    post.addComment(comment);
    comment.addWriter(loginUser);

    return CommentDto.fromEntity(comment, loginUser);
}
```

#### 5. Repository 역할 
실제 DB에 접근하여 적절한 결과값을 반환하는 역할을 수행합니다. 

```java
public interface CommentRepository extends JpaRepository<Comment, Integer> {
    Page<Comment> findByPost(Post post, Pageable pageable);
}
```

---

## 맺음말
파일럿 프로젝트를 마치면서 든 생각과 앞으로의 포부에 대해 짧게나마 맺음말을 적어보려 합니다. 

우선 FrontEnd부터 BackEnd까지 하나의 서비스를 온전히 스스로 구현해야 되는 일이 쉽지 않았습니다. 특히 이전까지 FrontEnd를 제대로 경험해본 적이 없는 저로서는 화면을 구현하는 모든 것이 어렵게 느껴졌습니다. HTML, CSS, JS의 기본적인 개념과 문법도 잘 알지 못하는 상태에서 관련된 수많은 정보들을 한 번에 접하다보니 마치 하면 할수록 더 바보가 되어가는 느낌이었달까요.. 그래서 처음에 Vue.js라는 Framework를 이해하는 데에도 굉장히 많은 시간이 걸린 것 같습니다. 수많은 시도에 따른 실패와 성공의 반복을 통해 관련 기술들을 (아주 조금씩) 활용할 수 있게 되었습니다. 그 이후부터는 습득 속도가 조금씩 더 빨라진다는 느낌을 받게 되었습니다. 스스로가 신기하고 재미있는 경험이었죠.
![멋지구나](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/good.png)

새로운 기술을 배우는 데에는 많은 노력이 필요합니다. 물론 저는 기본 개발 스펙으로 주어진 조건이 있었지만, 그 안에서 필요한 라이브러리 같은 경우에는 스스로 해당 기술이 정말 필요한 것인지에 대한 점검이 필요하다는 것도 느낄 수 있었습니다. 사용하는 기술에 대한 명확한 목적 없이 사용한다면 배보다 배꼽이 더 커질 수도 있기 때문입니다. (간단한 어플리케이션에 맞지 않는 거대한 라이브러리를 사용하게 될 수도..)

"파일럿 프로젝트"는 신입 개발자로서 입사하자마자 곧바로 실무에 투입되는 것이 아닌 앞으로 사용하게 될 관련 기술들을 미리 익힐 수 있게 해주는 좋은 기회였고 그 기회를 최대한 잘 이용하기 위해 노력하면서 더 많은 것을 배우고 싶다는 성장 욕구를 얻게 되었습니다.  
실력있는 개발자가 되기 위해서 끊임없이 성장하기 위해 노력해야겠다는 다짐과 함께, 수많은 문제들을 마주했을 때 이겨낼 수 있는 강한 멘탈을 얻을 수 있었습니다. 또한 새로운 기술에 대한 두려움을 없애고 아주 조금은 성장하지 않았나하는 자신감도 얻게 해준 의미 있는 프로젝트였다고 생각합니다. 
![명쾌한 정리](/images/portal/post/2019-04-19-ZUM-Pilot-dynamic-board/the-end.png)

감사합니다. 

---

## Reference
- [https://vuejs.org/](https://vuejs.org/)
- [https://vuex.vuejs.org/kr/](https://vuex.vuejs.org/kr/)
- [https://joshua1988.github.io/web-development/vuejs/vuejs-tutorial-for-beginner/](https://joshua1988.github.io/web-development/vuejs/vuejs-tutorial-for-beginner/)
- [http://arahansa.github.io/docs_spring/security.html#el-common-built-in](http://arahansa.github.io/docs_spring/security.html#el-common-built-in)
- [https://www.baeldung.com/spring-security-create-new-custom-security-expression](https://www.baeldung.com/spring-security-create-new-custom-security-expression)
- [https://gmlwjd9405.github.io/2018/12/25/difference-dao-dto-entity.html](https://gmlwjd9405.github.io/2018/12/25/difference-dao-dto-entity.html)





