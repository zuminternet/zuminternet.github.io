---

layout: post

title: 게시판 CMS - 파일럿 프로젝트

description: 신입 파일럿 프로젝트

image: /images/portal/post/2019-06-05-ZUM-PILOT-WONOH/project-structure2.PNG

introduction: 신입 파일럿 프로젝트를 진행했던 경험을 공유합니다.

category: portal/tech

tag: [experience, Springboot, JPA, Vue.js, pilot, Swagger, MySQL, S3]

---


> 입사일부터 일주일간 세팅 및 적응기간을 마치고 팀에서 실무를 하기 위한 
> 전반적인 웹 기술들을 숙지하고자 하는 목적을 가지고 4주간 파일럿 프로젝트를 
> 진행하였습니다. 이 글에서는 제가 파일럿 프로젝트를 진행할 때 사용한 기술들 , 
> 진행하면서 어려웠던 점을 어떻게 해결하였는지 , 프로젝트를 마친 뒤 느낀 점에 대해 
> 공유하고자 합니다.
​

## 1. 프로젝트 주제

제가 전달받은 프로젝트 주제는 소셜 로그인을 이용한 게시판 서비스 및 CMS시스템 구현이었습니다. CMS라는 용어를 들어보기는 하였지만 정확히 어떤 의미를 가지고 있는지 몰라 우선 CMS가 무엇인지 찾아보았습니다.
​
> [CMS](https://namu.wiki/w/CMS)  
> Contents Management System 즉 콘텐츠 관리 시스템의 약자이다.  
> 시스템에서 제공되는 각종 정보나 그 내용물들을 관리하는 통합 시스템.  
> 게시판, 레이아웃, 모듈과 같은 기능을 모아둔 웹 프레임워크이다.
​

간단하게 말하면 CMS는 개발지식이 없는 사람도 홈페이지를 만들고 운영할 수 있는 
도구?라고 말할 수 있습니다. 대표적인 CMS로는 XpressEngine, 그누보드, 킴스큐 등 이 있다고합니다.
CMS에 대해 완벽하게 이해하지는 못했지만 주어진 기능들을 구현하면서 CMS가 왜 필요한지, 어떤
목적을 가지는지에 대해 알 수 있었습니다.

​

## 2. 프로젝트 기술 스펙
-   [x]  Java8
-   [x]  Intellij
-   [ ]  Spring5.x MVC
-   [x]  SpringBoot 2.x
-   [x]  Spring Security
-   [x]  JPA
-   [x]  MySQL
-   [x]  Logback
-   [x]  Gradle
-   [ ]  Freemarker
-   [x]  Vue
-   [x]  Webpack
-   [x]  Git
​

해당 프로젝트에 사용해야 할 기술 스펙에 대해 전달받았습니다.  
프로젝트를 하기 전 SpringBoot는 사용해본 적이 있었지만 Vue , Webpack 은 사용해본 
적이 없어 주어진 요구사항을 기간 내에 끝낼 수 있을지에 대한 두려움이 생겼습니다. 
하지만 관심이 있었던 기술이었고 배우고 싶었던 기술이었기 때문에 유튜브 강의 , 관련 서적, 
블로그 등을 통해 학습하였고 개발을 하기 전에 기본적인 개념을 익히고 시작할 수 있었습니다.
​


​

## 3. 프로젝트 기능

 > - 회원 기능
 >   - 구글 로그인
 >   - 페이스북 로그인 
 > - 게시판 CMS 기능
 >   - `게시글 관리 (조회,삭제)`
 >   - `댓글 관리 (조회,삭제)`
 >   - 게시판 관리 (조회,생성,수정,삭제)
 > - 기본 게시판 기능
 >   - \[번호, 제목, 내용, 글쓴이, 시간, 조회수\] 정보를 가진 게시글
 >   - 등록, 수정, 삭제 기능 및 권한 처리(내가 쓴 글만 수정, 삭제 가능)
 >   - 글자 수 제한(10000자) 
 >   - 이미지(jpg, png, gif) 업로드 기능
 >   - `임시 저장 기능`
 >   - `좋아요`
 >   - 댓글 글자 수 제한(140자)
 >   - 계증형 댓글 기능(대댓글 까지)
 > - 보안 (tag,script 입력 필터링)
 
 전체적인 프로젝트 기능은 위와 같습니다. **SpringBoot**를 이용하여 간단한 게시판을 만들어본 경험을 토대로 진행하였기 때문에 주어진 기능들을 구현하는데 큰 어려움이 없었지만 미적 감각이 없어 **Vue**로 UI를 만들어 내는 것이 힘들었고 가장 많은 시간을 들였습니다.. UI는 [Element UI](https://element.eleme.io/#/en-US) 라는 Vue 2.0 기반 라이브러리를 사용하였습니다. 공식 문서가 한글로 되어있지는 않았지만 생각보다 다양한 예제들이 있었고 적용시키는데 큰 어려움이 없었습니다.

​
## 4\. 프로젝트 구조
​

​
![프로젝트 구성도](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/project-structure.PNG)
​
-   **Vue**
    -   router를 통한 component 매칭
        
    -   vuex를 이용한 상태 관리
        
    -   axios를 통한 http 통신
        
-   **SpringBoot**
    -   spring security로 사용자 인증
        
    -   JPA를 이용하여 객체 지향적인 테이블 관리
        
    -   dto를 통한 도메인 순수성 보장
        

## 5\. 데이터베이스 구조
​
### **주어진 요구사항**
-   **사용자는 소셜 로그인을 할 수 있다.**
-   **로그인한 사용자는 게시글, 댓글을 작성할 수 있다.**
-   **로그인한 사용자는 댓글에 댓글을 작성할 수 있다.**
-   **로그인한 사용자는 게시글에 이미지를 업로드할 수 있다.**
-   **로그인한 사용자는 게시글을 작성하다 `임시저장`을 할 수 있다.**
-   **관리자는 게시판, `게시글, 댓글` 들을 관리할 수 있다.**
​

이러한 요구사항으로부터 테이블을 설계하였습니다. JPA를 사용하였기 때문에 테이블 간 연관관계를 매핑하고 효율적으로 테이블을 관리하기 위해 [JPA책](http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.saNo=001&sc.prdNo=240925953&gclid=EAIaIQobChMI0IbOhda_4gIVnQcqCh2zNgV6EAQYASABEgIsL_D_BwE&product2017=true)을 통하여 학습을 하였고, JPA의 장점을 극대화시키기 위한 방법들을 여럿 배우게 되었습니다. 하지만 테이블을 직접 설계하고 연관관계를 매핑하는 과정에서 많은 오류를 만났고 4주라는 시간 동안 혼자만의 능력으로 모든 것을 만들어야 하였기에 시간에 쫓기다 보니 아래 그림과 같은 ERD가 나오게 되었습니다......
​

![ERD](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/erd.PNG)
​

​
## 6\. 개발 내용 ( Vue )
​
​
### **Vue**
​
단순 Html , Css , JavaScript로는 프로젝트를 만들어 보았지만 Vue라는 프레임워크는 사용해본 적이 없었기에 개발을 시작하기 전 사전 지식을 학습할 시간이 필요하였습니다. [공식문서](https://kr.vuejs.org/v2/guide/index.html#Vue-js%EA%B0%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94) 가 한글로 되어있어 이해하기 쉬웠고, 이를 따라 하면서 지식을 습득하였습니다. 그리고 Captain Pangyo 님의 [블로그](https://joshua1988.github.io/web-development/vuejs/vuejs-tutorial-for-beginner/) 를 통해 더 많은 지식을 얻을 수 있었습니다.
​
Vue에 대한 기본적인 학습을 마치고 프로젝트를 구성하려고 할 때 Vue CLI라는 좋은 도구가 있다는 것을 알게 되었습니다.
​
> [Vue CLI](https://cli.vuejs.org/)?  
> 커맨드 라인 인터페이스 기반의 Vue 프로젝트 생성 도구입니다. 
> Vue 애플리케이션을 개발할 때 기본적인 폴더 구조, 라이브러리 등을 설정해줍니다.
​

Vue CLI는 꾸준하게 버전이 업그레이드되고 있으며, [이 곳 ](https://www.npmjs.com/package/@vue/cli?activeTab=versions)
에서 확인해 보실 수 있습니다.  저는 Vue CLI 3.6.3 버전으로 Vue 프로젝트를 구성하였습니다. CLI 3.x 를 CLI 2.x 와 비교하면 설정 파일 자동화 , 디렉터리 구조 등 변화된 부분이 많아 버전이 달라 적용이 안 되는 부분들은 그때그때 구글링을 통해 수정해주었습니다. 

Vue CLI 3.x 버전으로 Vue 프로젝트를 생성하면  
​
![Vue 프로젝트](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/vue-project-structure.PNG)
​
 이와 같은 구조로 프로젝트가 생성됩니다. 주어진 기술 스펙 중 Webpack을 사용하여 SpringBoot와 Vue를 연동하여야 하는 스펙이 있었기 때문에 추가 설정을 해주어야 합니다.
​
 Vue CLI 2.x 버전은 프로젝트 root 디렉터리 하위에 설정 파일인 webpack.config.js 파일이 자동으로 만들어지지만 Vue CLI 3.x 버전부터는 vue.config.js라는 이름으로 직접 생성해주어야 합니다.
​
[SpringBoot 와 Vue 연동하기](https://kimyhcj.tistory.com/233) 를참고하여 개발 시에는 서버를 따로 띄워두고 개발이 완료되면 번들링 하여 서버 하나만을 구동시켜 동작을 확인하였습니다.
​
### **Vue 컴포넌트 ( Element UI )**
​
![](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/component1.PNG)
![](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/component2.PNG)
![](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/component3.PNG)
​
### **Vuex**
​
> [Vuex](https://vuex.vuejs.org/kr/guide/)?  
> Vuex는 Vue.js 애플리케이션에 대한 상태 관리 패턴 + 라이브러리.  
> 애플리케이션의 모든 컴포넌트에 대한 중앙 집중식 저장소 역할을 하며 예측 가능한 방식으로 상태를 변경할 수 있습니다. 
> 또한 devtools [확장 프로그램](https://github.com/vuejs/vue-devtools)과 통합되어 
> 설정 시간이 필요 없는 디버깅 및 상태 스냅 샷 내보내기/가져오기와 같은 고급 기능을 제공합니다.

​
### **Why?**
​
![](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/vue-data-structure.PNG)
​
Vue 컴포넌트들은 위 그림처럼 자신만의 상태를 가질 수 있습니다. 하지만 이러한 구조로 컴포넌트 간 공유해야 할 데이터가 생긴다면 [props](https://kr.vuejs.org/v2/guide/components.html#Props) 를 통해 데이터를 전달하여야 하며, 데이터를 변경하기 위해서는 이벤트를 [emit](https://kr.vuejs.org/v2/guide/components.html) 하여 사용해야 합니다. 이때 새로운 데이터가 추가된다면 데이터를 공유하는 모든 컴포넌트 간의 props를 변경해야 합니다. 따라서 컴포넌트가 많아지고 애플리케이션이 복잡할수록 유지 보수하기가 어려워지므로 위와 같은 모델은 적합하지 않다고 판단하여 Vuex를 사용하여 컴포넌트들 간 공유되는 데이터들을 관리하였습니다.
​
![](/images/portal/post/2019-06-05-ZUM-PILOT-WONOH/vuex-structure.PNG)​
Vuex의 대략적인 흐름은 다음과 같습니다.


​
**1\. Component** 에서**Action** 을 호출(Dispatch)
​

~~~js
this.$store.dispatch('createCategory', categoryRequestDto)
                            .then(() => {
                                this.categories = this.$store.getters.getCategories;
                            })
                            .catch((error) =>{
                                this.$notify.error({
                                    title: 'Error',
                                    message: error.data.message
                                });
                            });
~~~
​
**2\. Action** 은 API 서버와 통신을 통해 응답을 받아**Muation** 을 호출(Commit)
​

~~~js
createCategory: function (context, payload) {
​
        return new Promise((resolve, reject) => {
            axios
                .post('api/category', payload)
                .then((response) => {
                    console.log(response);
                    context.commit('createCategory', response.data);
                    resolve();
                })
                .catch(error => {
                    console.log(error.response);
                    reject(error.response);
                })
​
        });
~~~
​

**3\. Mutation** 은 응답으로**State 를** 변경(Mutate)
​

~~~js
createCategory: function (state, payload) {
        
        payload.createdAt = COMMON.dateToYYYYMMDD(new Date(payload.createdAt));
        state.manage.categoryCount++;
        payload.board = [];
        state.categories.push(payload);
        
    }
~~~
​
**4\. State** 의 변경에 따라**Component** 에**Render.**
​

~~~html
<el-table   :data="categories"
            style="width: 100%;">
~~~
​


이처럼 Vuex를 사용하여 여러 컴포넌트들 간 공유할 데이터를 저장소를 통해 관리하였고 [Vue devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 로 디버깅을 하며 언제 어느 컴포넌트에서 데이터를 바꾸었는지 알 수 있게 되었습니다. 
​

​
## 7\. 개발 내용 (SpringBoot)
​

### **JPA Auditing**
> **[JPA Auditing?](https://docs.spring.io/spring-data/jpa/docs/1.7.0.DATAJPA-580-SNAPSHOT/reference/html/auditing.html)  
> Spring-data-jpa에서 제공하는 기능으로 엔티티를 생성하거나 변경한 사람, 변경된 시기를 자동으로 주입해주는 기술. @CreatedDate , @LastModifiedDate , @CreatedBy , @LastModifiedBy 어노테이션을 사용하여 주입.**
​


 
쉽게 말하면 `JPA Auditing` 은 테이블에 변화가 일어날 때 누가 언제 하였는지를 자동적으로 주입시켜주는 기술입니다. 
데이터베이스를 설계할 때 모든 엔티티의 기본키를 id 값으로 잡았기 때문에 Auditing 기능을 적용시킨 
추상 클래스를 만들고 그 클래스를 상속받는 식으로 적용시켜주었습니다.
저는 누구에 의해 생성되었고, 누구에 의해 수정되었는지에 대한 어노테이션인 `@CreatedBy` ,
`@LastModifiedBy` 가 필요 없는 엔티티에는 기본키인 id와 `@CreatedDate` , `@LastModifiedDate` 
어노테이션만 가지는 `BaseEntity`를 상속받아 사용하였고, @CreatedBy ,@LastModifiedBy 어노테이션이 
필요한 엔티티들은 BaseEntity를 상속받는 `BoardBaseEntity`를 만들어서 필요에 따라 상속받아 사용하였습니다.
​
```java
@Getter
@MappedSuperclass
@EntityListeners(value = {AuditingEntityListener.class})
public abstract class BaseEntity {
​
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    protected Long id;
​
    @Column(name = "created_at",updatable = false)
    @CreatedDate
    protected LocalDateTime createdAt;
​
    @Column(name = "modified_at")
    @LastModifiedDate
    protected  LocalDateTime modifiedAt;
​
}
```
​
```java
@Getter
@MappedSuperclass
@EntityListeners(value = {AuditingEntityListener.class})
public abstract class BoardBaseEntity extends BaseEntity  {
​
    @Column(name = "created_by",updatable = false)
    @CreatedBy
    protected String createdBy;
​
    @Column(name = "modified_by")
    @LastModifiedBy
    protected String modifiedBy;
    
}
```
​
이처럼 두 개의 추상 클래스를 만들어 놓고 엔티티에서는 상속만 받게 되면 테이블에 변경사항이 있을 때마다 자동적으로 주입을 해주기 때문에 편리한 기능이라고 생각이 들었습니다.
​

하지만 @CreatedBy와 @LastModifiedBy 컬럼들은 위 설정으로만 자동 주입되지는 않았습니다. [Auditing](https://docs.spring.io/spring-data/jpa/docs/1.7.0.DATAJPA-580-SNAPSHOT/reference/html/auditing.html) 문서를 살펴보면 이렇게 나와있습니다.
​
> In case you use either @CreatedBy or @LastModifiedBy, the auditing infrastructure somehow needs to become aware of the current principal. To do so, we provide an   
> AuditorAware<T>SPI interface that you have to implement to tell the infrastructure who the current user or system interacting with the application is. The generic type T defines of what type the properties annotated with @CreatedBy or @LastModifiedBy have to be.
​
​

간단히 말하면 @CreatedBy , @LastModifiedBy을 사용하는 경우 현재 보안 주체를 인식하여야 하며,
이를 위해 AuditorAware <T>라는 SPI 인터페이스를 구현해야 합니다. 

여기서 현재 보안 주체는 **SecurityContextHolder**에  들어있는 인증된 사용자를 뜻합니다. 제가 구현한 AuditorAware 코드를 확인해 보겠습니다.

```java
@EnableJpaAuditing(auditorAwareRef = "auditorAware")
@Configuration
public class JpaAuditingConfig {
​
    private final String ANONYMOUS_USER = "anonymousUser";
​
    @Bean
    public AuditorAware<String> auditorAware(){
            return () -> {
                Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
                if(authentication == null || authentication.getPrincipal().equals(ANONYMOUS_USER)){
                    return Optional.empty();
                }
                Account account = (Account) authentication.getPrincipal();
                return Optional.of(account.getNickname());
            };
    }
}
```
​
> **@EnableJpaAuditing**  
> JPA에서 auditing 기능을 활성화시키기 위한 어노테이션
​

먼저 현재  **SecurityContextHolder**에 들어있는 인증된 사용자 정보를 가져옵니다. 이 정보가 
`null` 이거나 `anonymousUser` 라면 빈 값을 리턴하고 인증된 사용자가 있다면 사용자 이름을 
리턴합니다.
​
​
[레퍼런스 문서](https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/config/EnableJpaAuditing.html)를 보시면 auditorAwareRef 은 String 타입으로 현재 주체를 조회하는 데 사용되는 AuditorAware Bean을 구성한다고 나와있습니다.
​

따라서, @CreatedBy , @LastModifiedBy 칼럼이 있는 엔티티에 어떠한 수정사항이 발생하였을 때
Bean으로 등록된 auditorAware 메서드가 실행되며 현재 주체를 조회하여 작성자, 수정자를 자동 
주입하게 되는 것입니다.
​
### **권한 처리**
​
**요청에 따른 접근권한 설정**
​
```java
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                /*.cors()
                .and()*/ // 개발시에만
                .csrf().disable()
                .anonymous()
                .and()
                .authorizeRequests()
                .antMatchers(HttpMethod.POST,"/api/**").authenticated() // /api 하위 모든 POST요청
                .antMatchers(HttpMethod.PUT,"/api/**").authenticated() // /api 하위 모든 PUT요청
                .antMatchers(HttpMethod.DELETE,"/api/**").authenticated() // /api 하위 모든 DELETE요청
                .antMatchers("/manage/**").hasAuthority("ROLE_ADMIN") // /manage 하위 모든 요청은 관리자만
                .antMatchers("/","/login","/profile","/api/**").permitAll() // 이외 접근가능한 경로
                .and()
                .exceptionHandling()
                .accessDeniedHandler(new OAuth2AccessDeniedHandler())
                .and()
                .addFilterBefore(ssoFilter(),BasicAuthenticationFilter.class);
```
​
어떠한 기능이 로그인을 한 사용자만 가능하다면 해당 요청에 대해 인증받아야 접근할 수 있게 시큐리티 필터에 설정을 해주었고, 역할에 따른 접근 권한 설정 , 로그인이 필요하지 않은 기능은 허용해주었습니다.
​

**내가 쓴 글만 수정, 삭제**
​
```java
@PutMapping
public ResponseEntity updateComment(@RequestBody @Valid CommentUpdateRequestDto dto,
                                    @AuthenticationPrincipal Account account){
​
      CommentResponseDto responseDto = commentService.updateComment(dto,account);
      
      return ResponseEntity.ok(responseDto);
      
}
```
​
> **@AuthenticationPrincipal**  
> 현재 SecurityContextHolder 안에 들어있는 Principal, 즉 인증된 주체를 가져온다.
​

따라서 회원 엔티티인 Account로 현재 로그인 사용자 정보를 주입받게 되는데 이때 내부적으로는 AuthenticationPrincipalArgumentResolver를 통해 Principal을 주입받게 되는 것입니다.
​

[레퍼런스 문서](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/web/method/annotation/AuthenticationPrincipalArgumentResolver.html)를 보면 다음과 같이 나와있습니다.
​
> Allows resolving the Authentication.getPrincipal() using the AuthenticationPrincipal annotation.
​

AuthenticationPrincipal 어노테이션을 사용할 때 SecurityContextHolder에 있는 주체를 주입시켜줍니다.
​
문서에서는 이를 커스텀 어노테이션을 만들어 동일하게 사용할 수 있다고 합니다.
​

**Custom 어노테이션 생성**
​
```java
@Target({ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@AuthenticationPrincipal
public @interface CurrentAccount {
​
            // Do Something
​
}
```
​
**컨트롤러에 적용**
​
```java
@PutMapping
public ResponseEntity updateComment(@RequestBody @Valid CommentUpdateRequestDto dto,
                                    @CurrentAccount Account account){
​
   CommentResponseDto responseDto = commentService.updateComment(dto,account);
   
   return ResponseEntity.ok(responseDto);
   
}
```
​

두 가지 방법 다 동일하게 현재 인증된 주체를 어노테이션만으로 가져올 수 있어, 기호에 맞게 편한 방식으로 사용하면 될 것 같습니다.
​

### **이미지 업로드**


처음에는 이미지 업로드를 어떻게 구현할지에 대한 고민이 많았습니다. 이미지 파일을 받아 데이터베이스에
저장을 시키자니 이미지가 많아졌을 때 과부하 문제가 발목을 잡았고 이미지 파일을 서버 내 리소스에
저장시켜놓고 데이터베이스엔 외부에서 접근할 수 있는 URL, 이름 등의 간단한 정보들만 저장시켜주는 방식은
접근 권한을 허용해주고 리소스 경로를 맞춰줘야 하는 불편함이 있었습니다.

**Amazon S3**

여러가지 방법을 찾아보다 웹 스토리지 서비스인 Amazon S3를 사용해보기로 결정했습니다. 
Amazon S3 는 무료서비스가 아니지만 저는 `프리티어`를 사용하여 무료로 사용할수 있었습니다!
학생때 Amazon EC2 를 사용하다 정책설정을 잘못하여 큰금액은 아니지만 돈을 냈던 기억이
있어 무섭긴 했지만 S3는 EC2보다 사용하기 쉽고 간단하여 사용해보았습니다.
이미지 업로드의 흐름은 다음과 같습니다.



**1\. 이미지 업로드 요청(MultipartFile)**

```js
imageUpload: function (context, payload) {
        const config = {headers: {'Content-Type': 'multipart/form-data'}};
        return new Promise((resolve, reject) => {
            axios
                .post('api/image', payload.image, config)
                .then((response) => {
                    console.log('이미지 업로드 성공 응답', response);
                    resolve(response);
                })
                .catch((error) => {
                        reject(error.response);
                    }
                )
        })
    }
```

**2\. S3 이미지 업로드**

~~~java

@Autowired
private S3Uploader s3Uploader;

@PostMapping
public ResponseEntity uploadImage(@RequestParam("image") MultipartFile file) throws IOException{

        if(!s3Uploader.validateType(file)){  // MultipartFile 인지 타입체크
            return ResponseEntity.badRequest().build();
        }

        ImageUploadDto dto = s3Uploader.upload(file,"static"); //upload (이미지파일,업로드 디렉토리)
        
        ...

~~~
~~~java
/**
 *  이미지 업로드
 * @param uploadFile convert 된 이미지 파일
 * @param dirName 업로드할 디렉토리 이름
 * @return 이미지 dto
 */
private ImageUploadDto upload(File uploadFile, String dirName) {

        String fileName = dirName
                + "/"
                + UUID.randomUUID().toString() // UUID 부여
                +"."
                + FilenameUtils.getExtension(uploadFile.getName());

        String uploadUrl = putS3(uploadFile, fileName);
        
        ...

~~~
~~~java
private final AmazonS3 amazonS3;

@Value("${cloud.aws.s3.bucket}")
private String bucket;  // S3 bucket name
/**
 *  S3 에 업로드하기
 * @param uploadFile convert 된 이미지 파일
 * @param fileName 업로드할 디렉토리 이름
 * @return 업로드된 이미지 url
 */
private String putS3(File uploadFile, String fileName) {
        try {
            amazonS3.putObject(new PutObjectRequest(bucket, fileName, uploadFile).withCannedAcl(CannedAccessControlList.PublicRead));
            return amazonS3.getUrl(bucket, fileName).toString(); // 이미지 URL
        } catch (Exception e) {
            removeNewFile(uploadFile);
            throw new AmazonS3Exception(bucket, e);
        }
    }

~~~

**3\. S3에 저장된 이미지 정보(ImageUploadDto)**

~~~java
/**
 *  이미지 업로드
 * @param uploadFile convert 된 이미지 파일
 * @param dirName 업로드할 디렉토리 이름
 * @return 이미지 dto
 */
private ImageUploadDto upload(File uploadFile, String dirName) {
        ...

        ImageUploadDto dto = ImageUploadDto.builder()
                .originalName(uploadFile.getName())
                .imagePath(uploadUrl)
                .imageName(uploadUrl.substring(uploadUrl.lastIndexOf("/")+1,uploadUrl.lastIndexOf(".")))
                .imageExtension(FilenameUtils.getExtension(uploadFile.getName()))
                .build();

        removeNewFile(uploadFile);
        return dto;
    }

~~~


**4\. 이미지 저장(ImageUploadDto)**
~~~java
/**
 *  이미지 업로드
 * @param file 업로드할 이미지 파일
 * @return 업로드된 이미지
 * @throws IOException
 */
@PostMapping
public ResponseEntity uploadImage(@RequestParam("image") MultipartFile file) throws IOException{

       ...

        Image savedImage = imageService.save(dto);
        return ResponseEntity.ok(savedImage);
    }
~~~

**5\. 이미지 저장(Image)**

~~~java
/**
 * 이미지 저장
 * @param dto 이미지 저장 dto
 * @return 저장된 이미지 엔티티
 */
@Transactional
public Image save(ImageUploadDto dto) {

        Image image = Image.builder()
                .imageExtension(dto.getImageExtension())
                .imageName(dto.getImageName())
                .imagePath(dto.getImagePath())
                .originalName(dto.getOriginalName())
                .build();

        return imageRepository.save(image);

    }
~~~





### **보안 ( tag , script ) 입력 필터링**
​
해당 요구사항은 XSS( cross-site scripting ) 공격을 방지해야하는 요구사항이었습니다. 
​
> [**XSS**](https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9D%B4%ED%8A%B8_%EA%B0%84_%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8C%85)    
> XSS는 웹 애플레이케이션에서 많이 나타나는 취약점의 하나로 웹사이트 관리자가 아닌 이가 웹페이지에 악성 스크립트를 삽입할 수 있는 취약점이다. 주로 여러 사용자가 보게 되는 게시판에 악성 스크립트가 담긴 글을 올리는 형태로 이루어진다.
​

저는 XSS가 무엇인지 몰랐습니다..  그래서 Spring 에서 XSS를 막는 방법을 찾아보다 네이버에서
 만든 [lucy-xss-servlet-filter](https://github.com/naver/lucy-xss-servlet-filter)(XSS 방지 필터) 
 가 Servlet filter 단에서 < 등의 특수 문자를 $lt; 등으로 변환해주며, 여러 가지 관련 설정을 
 편리하게 지정할 수 있다고 하여 필터를 등록하여 적용시켜보았습니다. 
​
하지만, lucy-xss-servlet-filter 를 적용시켜도 xss 방지가 되지 않았습니다.. 
해서 찾아보니 해당 필터의 처리는 form-data에 대해서만 적용되고 Request Raw Body로 
넘어가는 JSON에 대해서는 처리해주지 않는다고 합니다. 해당 프로젝트의 API는 JSON형식으로만 
데이터를 주고받게 설계하였기 때문에 JSON으로 주고받을 때의 방지를 직접 처리해주어야 했습니다.
​
[ Spring에서 JSON XSS 방지하기](https://homoefficio.github.io/2016/11/21/Spring%EC%97%90%EC%84%9C-JSON%EC%97%90-XSS-%EB%B0%A9%EC%A7%80-%EC%B2%98%EB%A6%AC-%ED%95%98%EA%B8%B0/) 를 참고하여 MessageConverter 를 사용하여 ObjectMapper가 JSON문자열을 생성 할 때 XSS 방지 처리를 해주었습니다.
​

**1\. 처리할 특수 문자 지정**
​

XSS 방지 처리할 특수 문자들을 다음과 같이 CharacterEscapes 를 상속한 클래스를 만들어서 
지정해줍니다.
​
```java
public class HTMLCharacterEscapes extends CharacterEscapes {
​
    private final int[] asciiEscapes;
​
    private final CharSequenceTranslator translator;
​
    /**
     *  xss 방어 custom escape 문자 설정 및 등록
     */
    public HTMLCharacterEscapes(){
​
        asciiEscapes = CharacterEscapes.standardAsciiEscapesForJSON();
        asciiEscapes['<'] = CharacterEscapes.ESCAPE_CUSTOM;
        asciiEscapes['>'] = CharacterEscapes.ESCAPE_CUSTOM;
        asciiEscapes['&'] = CharacterEscapes.ESCAPE_CUSTOM;
        asciiEscapes['('] = CharacterEscapes.ESCAPE_CUSTOM;
        asciiEscapes[')'] = CharacterEscapes.ESCAPE_CUSTOM;
​
        translator = new AggregateTranslator(
                new LookupTranslator(EntityArrays.BASIC_ESCAPE),  // <, >, &, " 는 여기에 포함됨
                new LookupTranslator(EntityArrays.ISO8859_1_ESCAPE),
                new LookupTranslator(EntityArrays.HTML40_EXTENDED_ESCAPE)
        );
​
    }
​
    @Override
    public int[] getEscapeCodesForAscii() {
        return asciiEscapes;
    }
​
    @Override
    public SerializableString getEscapeSequence(int ch) {
        return new SerializedString(translator.translate(Character.toString((char) ch)));
    }
    
}
​
```
​

**2\. ObjectMapper에 특수문자 처리기능 적용 후 MessageConverter 등록**
​

```java
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
​
​
    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
​
        converters.add(htmlEscapingConverter());
    }
​
    /**
     *  MappingJackson2HttpMessageConverter 를 커스터마이징 하여
     *  응답 객체 이스케이프 문자 설정
     * @return 커스텀 설정이 적용된 컨버터
     */
    @Bean
    public HttpMessageConverter htmlEscapingConverter() {
​
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.getFactory().setCharacterEscapes(new HTMLCharacterEscapes()); //  xss 처리 문자 세팅
        
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        
        MappingJackson2HttpMessageConverter htmlEscapingConverter =
                new MappingJackson2HttpMessageConverter();
        htmlEscapingConverter.setObjectMapper(objectMapper);
        return htmlEscapingConverter;
    }
}
```
​

위 코드처럼 WebMvcConfigurer를 구현하여 컨버터에 XSS 방지 처리가 된 ObjectMapper를 세팅해주면 클라이언트와 서버 간 JSON으로 데이터를 주고받을 때 등록된 특수문자가 변환되는 것을 확인하실 수 있습니다.  
​

제가 보았던 대부분의 예제들에서는 WebMvcConfigurerAdapter 라는 추상 클래스를 상속받아 컨버터를 등록해주었지만 Spring5.0부터는 deprecate 되었다고 합니다. 
​
WebMvcConfigurerAdapter [문서](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/servlet/config/annotation/WebMvcConfigurerAdapter.html)를 보시면
​
> as of 5.0 WebMvcConfigurer has default methods (made possible by a Java 8 baseline) and can be implemented directly without the need for this adapter
​

라고 나와있습니다. Java 8에서는 인터페이스에 대한 정의가 몇가지 변경되었는데 그중 하나가 
default 메서드로 메서드 구현을 포함하는 인터페이스를 정의할 수 있다는 점입니다.
​
따라서 Spring5.0(Java 8) 버전이 나오면서 추상클래스인 WebMvcConfigurerAdapter 가 필요없어졌고 WebMvcConfigurer 인터페이스만 구현하면 여러 default 메서드를 오버 라이딩하여 사용하실 수 있습니다.
​

​
## 8\. 프로젝트를 마치고
​

​
처음 파일럿 프로젝트를 시작했을 땐 4주라는 기간  동안 백엔드,프론트엔드 까지 모두 혼자 
개발하여야 하는 것이 굉장한 부담이었습니다. 하지만 **'무엇이든 열심히 하면 된다'**라는 마음으로
임했고 덕분에 어떤 오류를 만나도 끊임없이 생각하고 디버깅하며 하나의 완성된 프로젝트를
만들수 있었습니다.

개발을 마친 후 프로젝트를 발표할 때 선배님들에게 많은 피드백을 받았습니다.
이 프로젝트를 실제 서비스에 적용한다고 하였을 때 부족한 부분이나 개선해야 할 점 등
여러 피드백을 받았고 이를 통해 앞으로 실무를 할 때 조금 더 서비스적인 부분에 대해 생각해보고
더 많이 고민해봐야겠다고 느꼈습니다. 

파일럿 프로젝트를 통해 앞으로 개발자로서 어떤 문제가 발생했을 때 문제를 해결해나가는 과정을
배웠고 앞으로 잘할수 있다는 자신감을 얻었습니다!

긴글 읽어주셔서 감사합니다.
