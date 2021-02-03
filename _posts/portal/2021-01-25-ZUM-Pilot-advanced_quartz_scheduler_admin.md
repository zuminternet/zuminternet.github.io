---

layout: post
title: Quartz Scheduler Admin 고도화 - 파일럿 프로젝트
description: Dynamic Multi DataSource 구현 경험을 공유합니다.
image: /images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin
introduction: Dynamic Multi DataSource 구현 경험을 공유합니다.  
category: portal/tech
tag:  [experience, Springboot, JPA, Vue.js, pilot, MySQL]

---

> 개별 서비스에 직접적인 영향은 없으나 서비스 유지보수에 도움이 되는 공용 어드민에 대한 고도화 작업을 진행함으로서
  실무 투입전 포털개발팀에서 사용하는 기술 스펙 적응 및 업무 프로세스 등을 익히고
  파일럿 프로젝트 이후에도 계속 사용할 수 있는 산출물을 남김으로서 팀에 기여 하고자 하였습니다.

## Intro

### Quartz Scheduler Admin 이란?

![02-quart_job_scheduler](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/02-quartz_job_scheduler.PNG)

Quartz Job Scheduler 는 DB 기반으로 스케줄러 간의 클러스터링 기능을 제공합니다. 
![01-what_is_quartz_scheduler_admin](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/01-what_is_quartz_scheduler_admin.svg)
Quartz Scheduler Admin 은 Quartz Job Scheduler 의 DB 관리를 위한 CMS 입니다.  

### 배경
![03-quartz_admin_scheduler_before_after](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/03-quartz_admin_scheduler_before_after.svg)

기존에는 Common Scheduler DB 안에 모든 서비스의 Job Scheduler 정보를 담고 있었으며, 해당 DB 에 대한 Quartz Scheduler Admin CMS 가 존재하였습니다.     
하지만 DB 의 장애가 발생하였을 때 모든 서비스의 Batch 가 중단되는 문제가 있었습니다.    
이를 해결하기 위해 각 서비스 별 Scheduler DB 로 분산하게 되었고, Quartz Scheduler Admin CMS 는 더 이상 사용을 할 수 없게 되었습니다.  


### 목표
Common Scheduler DB 를 각 서비스 별 Scheduler DB 로 분산하게 되면서 사용이 중단된 Quartz Scheduler Admin CMS 을 
다시 사용할 수 있도록 프로젝트 구조를 변경하고 어플리케이션의 효용성을 높이기 위한 고도화를 진행하였습니다.

## 메뉴얼

배포 정보

### 1. 서비스 별 Scheduler DB 관리 기능 추가
![04-quartz-admin_before](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/04-quartz-admin_before.png)
기존에는 Common Scheduler DB 에 대해서만 Quartz Scheduler Admin CMS 를 사용할 수 있었습니다.

![05-dbconfig_main](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/05-dbconfig_main.jpg)
**[Management > DB Config]** 메뉴에서, 서비스 별 Scheduler DB 를 동적으로 관리할 수 있게 되었습니다.    
**Information Of DB Connection** 에서는 `SeriveKey` `DBConnectionName` `DriverClassName` `Url` `UserName` `Connection Status`를 조회할 수 있습니다.

<img style="width:50%" src="/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/06-dbcofig_sidebar.png"/>  
추가된 서비스는 사이드바 메뉴에 생성이 됩니다.       
`Connection` 이 유효하지 않는 DB 는 사이드바 메뉴에 나타나지 않습니다.

서비스가 늘어남에 따라 메뉴가 복잡해 질 것을 고려해, 서비스 별 메뉴와 같이 UI 를 개편이 필요할 것 같습니다.

![!07-dbconfig_add](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/07-dbconfig_add.png)
1. 우측 상단의 **Add** 버튼을 누르면 DB 를 추가할 수 있습니다.
2. `ServiceKey` 
    - ServiceKey 는 ASCII 문자만 입력가능합니다.  그 이유는, ServiceKey 가 유니코드외 문자라면 `path variables` 에 포함이 될 때 인코딩되는 문제가 발생하기 때문입니다.
    - 스프링 서버로 Http Request 요청 시 Header 에 포함됩니다. 스프링 서버는 Headers 의 `service-key` 의 값으로 DataSource 를 결정하게 됩니다.
    - 예시) news
3. `DBConnectionName`
    - 좌측 사이드바 메뉴에서 나타낼 DB 의 이름 입니다.
    - 예시) 뉴스
4. `DriverClassName`
    - 스프링 서버에서 사용할 JDBC 드라이버의 종류 입니다. 
    - 현재 버전에서는 `com.mysql.cj.jdbc.Driver` 만 사용 가능합니다. 
    - 기본 값은 `com.mysql.cj.jdbc.Driver` 입니다. 
5. `URL`
    - DB 의 URL 입니다.
    - 예시) jdbc:mysql://127.0.0.1:3306/database_name?serverTimezone=Asia/Seoul&characterEncoding=UTF-8
6. `UserName`
    - Database 의 username 입니다.
7. `Password`
    - Database 의 password 입니다.
    - 기본값은 빈 문자열 `''` 입니다.     
8. 폼을 모두 입력한 후 `Test Connection` 버튼을 누르면 해당 DB 접속 정보가 유효하여 연결이 가능한지 테스트 할 수 있습니다. 만약 테스트에 성공하면 성공 메세지와 함께 버튼의 색깔이 녹색으로 변합니다.

![08-dbconfig_detail](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/08-dbconfig_detail.jpg)

1. `Detail` 버튼을 눌러 자세한 DB 정보를 조회할 수 있습니다.
2. `Modify` 버튼을 눌러 DB Connection Detail 을 수정할 수 있습니다.
![09-dbconfig_modify](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/09-dbconfig_modify.jpg)

### 2. Job 실행 기능 개선
![10-add_simple_trigger](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/10-add_simple_trigger.gif)
해당 Job 을 즉시 실행하기 위해서는, Trigger 의 `StartTime` 을 현재시간보다 이전으로 설정하고,
`EndTime` 을 현재시간 이후로 설정을 해주면 됩니다. 

기존에는, 즉시 실행을 하기 위해서 SimpleTrigger 폼을 직접 입력해 주어야 했습니다.

![11-add_simple_trigger_after](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/11-add_simple_trigger_after.gif)

`Execution` 버튼 하나만으로 Job 을 즉시실행 할 수 있습니다.

`TriggerGroup` 과 `TriggerName` 은 다음과 같은 양식으로 랜덤으로 생성 됩니다.
- `TriggerGroup` : INTERNAL-`JobGroup`-triggerGroup-`UUIDv4`
- `TriggerName` : INTERNAL-`JobName`-triggerName-`UUIDv4`


### 3. 구글 oAuth 로그인 기능 추가
![12-login](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/12-login.gif)

구글 로그인 기능이 추가 되었습니다. 

![13-login_fail](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/13-login_fail.gif)

이스트소프트 계열사 도메인으로 로그인 가능한 이메일을 제한하였습니다.

- zuminternet.com
- estsoft.com
- estgames.com
- estsecurity.com
- deep-eye.co.kr
- mindmaple.com
- projectvanilla.kr

만약 이외의 도메인으로 로그인을 시도한다면, 로그인에러 페이지로 리디렉션 됩니다.
이 때, 다른 계정으로 로그인을 시도하려면 구글 계정을 완전히 로그아웃 시켜야 합니다. 

해당 링크로 접속하면, 현재 브라우저에 로그인 되어있는 구글 아이디를 로그아웃 할 수 있습니다.   
`https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout`


![14-logout_refresh](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/14-logout_refresh.gif)

우측 상단에 `logout` 혹은 `login` 버튼이 존재합니다.   
`logout` 버튼 왼쪽의 `refresh` 아이콘 버튼을 눌러 로그인을 재시도 하고 세션을 `refresh` 할 수 있습니다.    
마지막 Http Request 후 30 분이 지나거나, 유저의 권한이 변경될 때 세션이 만료됩니다. 

![16-user_login_history](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/16-user_login_history.png)
로그인 한 사용자의 기록은 **[Management > Login History]** 메뉴에서 확인 할 수 있습니다.   
로그인 시간, `IP`, 접속한 사용자의 이름과 이메일이 기록됩니다.

![15-user_auth](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/15-user_auth.PNG)
사용자의 권한에는 3가지가 존재합니다.
권한 별로 접근 가능한 메뉴와 API 가 달라집니다.
아래 리스트의 하위로 갈 수록 권한이 확장 됩니다.

- `BLOCK` 
    - Info  
- `USER`
    - DashBoard
    - Quartz Job
    - CronTrigger
    - SimpleTrigger
- `ADMIN`
    - Management
    
최초 로그인을 하였을 때, 사용자의 권한 레벨은 `BLOCK` 이기 때문에 `ADMIN` 의 승인이 필요합니다.

![17-user_auth_change](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/17-user_auth_change.gif)

**[Management > User]** 메뉴에서 사용자의 권한을 변경할 수 있습니다.    
이때, 해당 사용자의 권한이 변경되면 세션이 만료되므로 해당 사용자는 `logout` 버튼 왼쪽의 `refresh` 버튼을 클릭하여 세션을 다시 갱신해야 합니다.

### 4. 각 서비스 CMS 에서 연동하여 사용할 수 있는 API 개발

![18-scheduler_admin_api](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/18-scheduler_admin_api.svg)

서비스 별 어드민 서버에서, Quartz Scheduler Admin API 를 호출하여 해당 Job 실행 할 수 있습니다.

상세 api 스펙은 보안상 포스팅에서 다루지 않습니다.


### 5. job 실행 이력관리 기능
![18-job_history](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/18-job_history.gif)
**[Management > Job History]** 메뉴에서 Job 의 Simple Trigger 생성 히스토리를 조회할 수 있습니다. 

Simple Trigger 는 두가지 방법으로 추가할 수 있습니다. `Method` 컬럼의 값은 두가지가 있습니다.
- `INTERNAL` : Quartz Scheduler Admin CMS 내 에서 추가되었을 경우
- `EXTERNAL` : 각 서비스 CSM 서버의 요청으로 추가된 경우

추후, Job 의 실행 결과를 조회할 수 있는 기능이 업데이트 될 예정입니다.


## 프로젝트 설계

### Back end
- Spring Boot v2.1.6
- Gradle v5.4.1
- Java 8
- JPA

### Front end
- Webpack
- Vue Cli 3
- ES 2020
- Element-UI

### 1. Simple Service Structure
![19-service_architecture](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/19-service_architecture.svg)

### 2. Client 
![20-client_architecture](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/20-client_architecture.svg)

~~~sh
frontend
├─public
│      index.html   
└─src
   │  App.vue
   │  main.js
   ├─adapters                       # http request 모듈 
   ├─commons                        # 공용 모듈    
   ├─config                     
   │      AxiosIntercepter.js      
   ├─layout                     
   ├─router         
   ├─store
   └─views
   └─components
     └─base                         # 공용 컴포넌트
~~~


### 3. Server 
![21-spring_server_architecture](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/21-spring_server_architecture.svg)

~~~sh
└─com.quartz.admin
    │  QuartzVueAdminApplication.java
    ├─annotations
    ├─config
    │  │  WebMvcConfig.java
    │  ├─auth                 # spring security 와 google oauth2 설정
    │  └─dataSource           # RoutingDataSource 설정
    ├─controller
    │  ├─api
    │  ├─path
    │  └─view
    │  HomeViewController.java
    ├─property
    ├─domain
    └─util
~~~

### 4. DataBase

Spring Data JPA `Entity` 를 이용하여 테이블을 정의하였습니다. 

![22-database](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/22-database.svg)

1. `INFO_OF_DB_CONNECTION`
    - 각 서비스의 Database Connection 정보를 담고 있습니다.
1. `TRIGGER_HISTORY`
    - JOB 의 SIMPLE TRIGGER 생성 정보를 기록합니다. 
1. `JOB_HISTORY` 
    - TRIGGER_HISTORY 의 생성 정보를 기록합니다.
    - 외래키로 조인된 PRIMARY KEY 입니다.
        - `TRIGGER_HISTORY_ID` UNIQUE KEY
        - `INFO_OF_DB_CONNECTION_ID` 트리거 가 추가된 서비스 데이터베이스 정보 
    - 트리거가 생성될 때 생성시간, 생성자의 이메일, 아이피주소, 성명 을 수집합니다.
        `CREATED_AT`, `USER_EMAIL`, `IP_ADDRESS`, `USER_NAME`
1. `USER`
    - Google OAuth 로 가입한 사용자의 이름, 이메일 주소, 권한 정보를 수집합니다.
1. `LOGIN_HISTORY`
    - Google OAuth 로 로그인을 할 때마다, 로그인한 사용자의 정보를 기록합니다.
    - 사용자의 이메일, 아이피 주소, 로그인시간, 성명 을 수집합니다.


## 코드
파일럿 프로젝트에서 학습하거나 개선한 코드를 소개 합니다. 

### 다중 DataSource 를 동적으로 변경하기

기능을 구현하기 위해 `AbstractRoutingDataSource` 를 상속한 `RoutingDataSource` 를 구현하였습니다. 
그 이유는 `AbstractRoutingDataSource` 특징인 다음과 같습니다.

1. 동일 DB 스키마에 대한 다중 DB 접속 처리 가능합니다.
기존의 공용 Scheduler DB 가 분산된 것이므로 각 서비스 별, 스키마, API 로직이 모두 동일합니다. 

2. DataSource 의 Target 데이터 소스는 `DataSourceLookupKeyContextHolder` 를 기반으로 런타임에 동적으로 결정될 수 있습니다.
3. IsolationLevelDataSourceRouter 트랜잭션 별 격리 수준을 보장합니다.

먼저 App 이 실행되면 제일 먼저 Admin Database 의 Datasource Bean 을 생성해야 합니다.
Admin Database 의 `INFO_OF_DB_CONNECTIONS` 테이블에 다른 서비스들의 Database Connection 정보들이 저장되어 있기 때문입니다. 


#### AbstractRoutingDataSource
`AbstractRoutingDataSource` 의 주요 멤버변수와 메서드는 다음과 같습니다.

```java
package org.springframework.jdbc.datasource.lookup;

public abstract class AbstractRoutingDataSource extends AbstractDataSource implements InitializingBean {

	private Map<Object, Object> targetDataSources;
	private Object defaultTargetDataSource;
	private Map<Object, DataSource> resolvedDataSources;
	private DataSource resolvedDefaultDataSource;
	public void setTargetDataSources(Map<Object, Object> targetDataSources);
	public void setDefaultTargetDataSource(Object defaultTargetDataSource);

	public void afterPropertiesSet(); 
	public Connection getConnection();

	protected DataSource determineTargetDataSource();
	protected abstract Object determineCurrentLookupKey();

}
```

1. private Map<Object, Object> targetDataSources
    - 각 서비스의 Datasource 정보들이 Map 으로 저장됩니다. 
    - `public void setTargetDataSources(Map<Object, Object> targetDataSources)` 메서드로 값을 저장할 수 있습니다.
    
2. private Object defaultTargetDataSource
    - `resolvedDataSources` 에서 `lookupKey` 를 찾지 못했을 때 사용하는 기본 DataSource 입니다.
    - `public void setDefaultTargetDataSource(Object defaultTargetDataSource)` 메서드로 값을 저장할 수 있습니다.
    
3.  private Map<Object, DataSource> resolvedDataSources; private DataSource resolvedDefaultDataSource
    - 데이터 소스를 결정할 때에는 `targetDataSources`, `defaultTargetDataSource` 가 아니라 `resolvedDataSources` `resolvedDefaultDataSource` 에서 참조합니다. 
    - `public void afterPropertiesSet()` 메서드에서 `targetDataSources`, `defaultTargetDataSource` 의 값을 `resolvedDataSources` `resolvedDefaultDataSource` 으로 복사합니다.

4. 	Database 와의 connection 을 생성합니다.

```java
public Connection getConnection() throws SQLException {
    return determineTargetDataSource().getConnection();
}
```

5. protected DataSource determineTargetDataSource()

```java
protected DataSource determineTargetDataSource() {
    Assert.notNull(this.resolvedDataSources, "DataSource router not initialized");
    Object lookupKey = determineCurrentLookupKey();
    DataSource dataSource = this.resolvedDataSources.get(lookupKey);
    if (dataSource == null && (this.lenientFallback || lookupKey == null)) {
        dataSource = this.resolvedDefaultDataSource;
    }
    if (dataSource == null) {
        throw new IllegalStateException("Cannot determine target DataSource for lookup key [" + lookupKey + "]");
    }
    return dataSource;
}
```

- connection 을 설정할 Datasource 를 결정합니다.
- 먼저 `Object lookupKey = determineCurrentLookupKey();` 를 호출하여 `lookupKey` 의 값을 가져옵니다. `resolvedDataSources` 에서 `lookupKey` 로 값을 가져 올 수 없다면 `resolvedDefaultDataSource` 를 사용합니다.

#### RoutingDataSource
`RoutingDataSource` 는 `AbstractRoutingDataSource` 을 상속한 클래스 입니다. 

상속한 AbstractRoutingDataSource 를 조작하기 위한 인터페이스를 갖는 것이 특징입니다.

여기서 눈 여겨 봐야 할 점은 오버라이드 한 `determineCurrentLookupKey()` 메서드 입니다.

```java
@Override
protected String determineCurrentLookupKey() {
    return DataSourceLookupKeyContextHolder.get();
}
```
DataSourceLookupKeyContextHolder 클래스의 `ThreadLocal` 타입인 `DATA_SOURCE_KEY` 를 참조하고 있습니다.
만약 `DATA_SOURCE_KEY` 의 값이 `news` 라면 `resolvedDataSources` 의 해시 값 중, 키가 `news` 인 Datasource 가 결정이 될 것 입니다.
 
```java
public class DataSourceLookupKeyContextHolder {
    private static final ThreadLocal<String> DATA_SOURCE_KEY = new ThreadLocal<>();

    public static void set(String dataSourceType) {
        DataSourceLookupKeyContextHolder.DATA_SOURCE_KEY.set(dataSourceType);
    }

    public static String get() {
        return DATA_SOURCE_KEY.get();
    }

    public static void remove() {
        DataSourceLookupKeyContextHolder.DATA_SOURCE_KEY.remove();
    }
}
```

[ThreadLocal](https://javacan.tistory.com/entry/ThreadLocalUsage) 를 이용하면 쓰레드 영역에 변수를 설정할 수 있기 때문에, 
특정 쓰레드가 실행하는 모든 코드에서 그 쓰레드에 설정된 변수 값을 사용할 수 있게 되는 특징을 가지고 있습니다. 

![30-extends_abstract_rounting_ds](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/30-extends_abstract_rounting_ds.svg)
    

#### DataSourceConfig
다음은, RoutingDataSource 를 이용해 DataSource Bean 을 등록하는 과정에 대해 서술 합니다.

`DataSourceConfig` 클래스에서는 AdminDB 를 ResolvedDefaultDataSource 로 등록하고, 서비스 별 DB 들을 ResolvedDataSources 으로 가지고 있는 DataSource Bean 을 등록하게 됩니다.

##### 1. 스프링부트가 실행이 되면 `.yml` 의 `spring.datasource` 의 데이터를 바탕으로, 자동으로 단일 DataSource 를 authConfiguration 해줍니다.
하지만, 여기선 `AbstractRoutingDataSource` 를 사용하여 다중 DataSource 으로 커스텀 할 것이므로 `SpringBootApplication` 의 `DataSourceAutoConfiguration.class`을 `exclude` 해줍니다.

```java
@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
@EnableConfigurationProperties({ DefaultDBProperty.class })
public class QuartzVueAdminApplication {

  public static void main(String[] args) {
    // ...
  }
}
```

##### 2. Admin Database 를 DataSource 객체로 생성하는 과정 입니다.

![28-diagram1](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/28-diagram1.svg)

`application.yml` 의 `spring.datasource` 를 `DefaultDBProperty.class` 프로퍼티로 생성해 주었습니다.

```yaml
spring:
  datasource:
    service-key: "admin"
    db-connection-name: 관리자
    url: jdbc:mysql://...?serverTimezone=Asia/Seoul&characterEncoding=UTF-8
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: ...
    password: ...

```

`DefaultDBProperty` 멤버변수를 `InfoOfDBConnections` 타입으로 변환할 수 있는 `toInfoOfDbConnections()` 메서드가 존재합니다. 

```java
@Getter
@Setter
@NoArgsConstructor
@ConfigurationProperties(prefix="spring.datasource")
public class DefaultDBProperty {

  private String serviceKey;
  private String url;
  private String username;
  private String password;
  private String driverClassName;

  public InfoOfDBConnections toInfoOfDbConnections() {
    return InfoOfDBConnections.builder()
                              .serviceKey(serviceKey)
                              .url(url)
                              .username(username)
                              .password(password)
                              .driverClassName(driverClassName)
                              .build();
  }

}
```

![31-default_ds](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/31-default_ds.svg)

`toInfoOfDbConnections()` 가 존재하는 이유는,
아래 `DataSourceWrapper` 클래스 인스턴스 생성자 타입으로 InfoOfDBConnections 객체를 받아 `DataSourceWrapper` 인스턴스를 생성하기 때문입니다.

`DefaultDataSourceConfig` 클래스 에서는 `defaultDataSource` 라는 `DataSourceWrapper` 타입을 반환하는 Bean 을 생성합니다.
이 빈은, DefaultDBProperty 에 저장된 admin database 정보를 바탕으로, DataSource 를 만들어 냅니다. 

```java
@RequiredArgsConstructor
@Configuration
public class DefaultDataSourceConfig {

  private final DefaultDBProperty dbProperty;

  @Bean
  public DataSourceWrapper defaultDataSource() {
    return DataSourceWrapper.of(dbProperty.toInfoOfDBConnections());
  }

}
```

`DataSourceWrapper` 클래스는 RoutingDataSource 에 저장되는 DataSource 해시 값의 키-값의 정보 입니다.

`InfoOfDBConnections` 타입을 생성자의 인자로 받아, serviceKey 와 HikariDataSource 멤버 변수의 값을 저장합니다.

```java
@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class DataSourceWrapper {

    private String serviceKey;
    private HikariDataSource dataSource;

    public static DataSourceWrapper of(InfoOfDBConnections infoOfDBConnections) {
        return new DataSourceWrapper(infoOfDBConnections.getServiceKey(), createDataSource(infoOfDBConnections));
    }

    private static HikariDataSource createDataSource(
        InfoOfDBConnections infoOfDBConnections) {
        return DataSourceBuilder.create()
                                .url(infoOfDBConnections.getUrl())
                                .username(infoOfDBConnections.getUsername())
                                .password(infoOfDBConnections.getPassword())
                                .driverClassName(infoOfDBConnections.getDriverClassName())
                                .type(HikariDataSource.class)
                                .build();
    }

}
```


##### 3. RoutingDataSource 를 Datasource Bean 으로 등록합니다.

Admin Database 의 INFO_OF_DB_CONNECTIONS 테이블의 서비스 database connection 데이터들은 Application 실행 후 초기화 합니다. 
Bean 생성 단계에서 JPA Repository Bean 을 주입하려고 하면 순환 참조의 문제가 발생하기 때문입니다.

![32-circular_ref](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/32-circular_ref.svg)

1. JPA Repository Bean 은 DataSource Bean 이 주입되어야 합니다
2. DataSource 는 JDBC 관련 Bean 이 주입되어야 합니다
3. JDBC 관련 Bean 은 JPA Repository Bean 이 주입 되어야 합니다
4. JPA Repository Bean 은 DataSource Bean 이 주입되어야 합니다
5. ....


다음 이미지는 RoutingDataSource 에 DefaultTargetDataSource 와 TargetDataSources 를 Resolve 하는 과정을 보여줍니다.

![35-set_routing_sources](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/35-set_routing_sources.svg)

```java
@Configuration
@RequiredArgsConstructor
public class DataSourceConfig {

  private final DataSourceWrapper defaultDataSource;
  private final RoutingDataSource routingDataSource = RoutingDataSource.of();

  @Bean
  public DataSource dataSource() {
    routingDataSource.setDefaultDataSource(defaultDataSource.getDataSource());
    return routingDataSource;
  }

}
```

DataSourceConfig 에서는 `RoutingDataSource` 를 DataSource Bean 으로 등록합니다.
초기에 Bean 으로 등록할 때, Admin DataSource 만 DefaultDataSource 으로 등록 해 주었습니다. 

```java
public class RoutingDataSource extends AbstractRoutingDataSource {
    private HikariDataSource defaultTargetDS;

    public void setDefaultDataSource(HikariDataSource dataSource) {
        defaultTargetDS = dataSource;
        resolve();
    }

    public void setDataSources(List<InfoOfDBConnections> infoOfDBConnections) {
        targetDS = DataSources.of(infoOfDBConnections).get();
        resolve();
    }

    private void resolve() {
        setDefaultTargetDataSource(defaultTargetDS);
        setTargetDataSources(targetDS);
        afterPropertiesSet();
    }
}
```

`resolve()` 메서드는 다음과 같은 일을 합니다.
- `setDefaultTargetDataSource(defaultTargetDS);` : 확장한 AbstractRoutingDataSource 의 `defaultTargetDataSource` 멤버 변수에 값에 저장합니다.
- `setTargetDataSources(targetDS);` : 확장한 AbstractRoutingDataSource 의 `targetDataSources` 멤버 변수에 값을 저장합니다.
- `afterPropertiesSet();` : 확장한 AbstractRoutingDataSource 에서
    - defaultTargetDataSource 을 `resolvedDefaultDataSource` 에 복사합니다.
    - targetDataSources 를 `resolvedDataSources` 에 복사합니다.


`DataSources` 클래스는 
List<InfoOfDBConnections> 객체를 `Map<String, HikariDataSource>` 객체를 래핑하는 DataSources 객체로 변환 해 줄 수 있습니다.

```java
package com.quartz.admin.config.dataSource;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class DataSources {

  private Map<String, HikariDataSource> dataSources;

  private static void put(Map<String, HikariDataSource> dataSources, DataSourceWrapper dataSourceWrapper) {
    dataSources.put(dataSourceWrapper.getServiceKey(), dataSourceWrapper.getDataSource());
  }

  public static DataSources of(List<InfoOfDBConnections> infoOfDBConnections) {
    Map<String, HikariDataSource> dataSources = new HashMap<>();

    infoOfDBConnections.stream()
                       .filter(info -> info.getIsSuccess() == 1)
                       .forEach(info -> put(dataSources, DataSourceWrapper.of(info)));

    return new DataSources(dataSources);
  }

  public Map<Object, Object> get() {
    return new HashMap<>(dataSources);
  }

}
```

- `DataSources of(List<InfoOfDBConnections> infoOfDBConnections)` : `.filter(info -> info.getIsSuccess() == 1)` 연결 가능한 Database 만을 선정하여 DataSourceWrapper 로 래핑해 줍니다.
- `get()` : DataSources 를 실제 DataSource 의 TargetDataSources 에 저장할 때, `Map<Object, Object>` 타입으로 변환이 되어야 합니다.


##### 5. 서비스 별 DataSource 등록하기
앞서, Bean 초기화 단계에서 JPA Repository 의 의존성을 사용할 수 없다는 것을 확인했습니다.

문제를 해결하기 위해, 스프링 부트 Application 실행 후 서비스 별 DataSources 를 등록해야 했고,   
`ApplicationRunner` 를 구현해 `run` 메서드를 오버라이드 하는 방법을 사용했습니다.

```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
@EnableConfigurationProperties({ DefaultDBProperty.class })
public class QuartzVueAdminApplication {

  public static void main(String[] args) {
    // ...
  }

  @Component
  @RequiredArgsConstructor
  public static class RunAfterApplicationStart implements ApplicationRunner {

    @UpdateDataSource
    @Override
    public void run(ApplicationArguments args) { }
  }

}
```
    
run 의 본문은 비어있지만, `@UpdateDataSource` 라는 커스텀 Aspect 어노테이션을 사용했습니다.   
이 어노테이션은 DataSource 를 INFO_OF_DB_CONNECTIONS 테이블의 데이터와 동기화 하는 기능을 합니다.  
앱 실행 이외에도, INFO_OF_DB_CONNECTIONS 데이터 변경 시, 필요한 로직이기 때문에 annotation 으로 구현해 보았습니다. 

```java
@RequiredArgsConstructor
@Component
@Aspect
public class UpdateDataSourceAspect {
  private final RoutingDataSource routingDataSource;
  private final InfoOfDBConnectionService infoOfDBConnectionService;

  @Around("@annotation(UpdateDataSource)")
  public Object update(ProceedingJoinPoint joinPoint) throws Throwable {
    Object res = joinPoint.proceed();

    routingDataSource.setDataSources(infoOfDBConnectionService.findAllUpdatedIsSuccess());

    return res;
  }

}
```

![40-ds_update](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/40-ds_update.svg)

먼저 UpdateDataSourceAspect 에서, infoOfDBConnectionService.findAllUpdatedIsSuccess() 를 호출 합니다.

```java
public class InfoOfDBConnectionService {
  // ...

  public List<InfoOfDBConnections> findAllUpdatedIsSuccess() {
    return infoOfDBConnectionRepository.findAll()
                                       .stream()
                                       .map(info -> {
                                         byte result = 0;
                                         try {
                                           result = DBConnection.create().test(info);
                                         } catch (SQLException ignored) {}
                                         info.setIsSuccess(result);
                                         return infoOfDBConnectionRepository.save(info);
                                       }).collect(Collectors.toList());
  }
}
```

findAllUpdatedIsSuccess() 에서는, DataBase 의 연결가능 여부를 확인하고, 각 레코드의 IsSuccess 필드를 업데이트한 결과를 반환합니다.

DataBase 의 연결 가능여부를 확인할 때에는 `DBConnection.create().test(InfoOfDBConnection)` 을 사용합니다.
이 때, 직접 DriverManager.getConnection 을 사용하고, 어떤 에러가 발생하거나, 1초 내에 커넥션을 할 수 없을 경우, 
연결할 수 없음을 나타내는 0 을 반환하게 됩니다.

```java
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class DBConnection {
  private final String DEFAULT_DRIVER_CLASS_NAME = "com.mysql.cj.jdbc.Driver";
  private final String CONNECTION_TIMEOUT = "&connectTimeout=1000";
  private Connection conn = null;

  public static DBConnection create() {
    return new DBConnection();
  }

  public byte test(InfoOfDBConnections infoOfDBConnection) throws SQLException {
    try {
      infoOfDBConnection.setDriverClassName(DEFAULT_DRIVER_CLASS_NAME);

      Class.forName(infoOfDBConnection.getDriverClassName());
      conn = DriverManager.getConnection(
          infoOfDBConnection.getUrl() + CONNECTION_TIMEOUT,
          infoOfDBConnection.getUsername(),
          infoOfDBConnection.getPassword()
      );

      return 1;
    } catch (Exception e) {
      e.printStackTrace();
      return 0;
    } finally {
      close();
    }
  }

  private void close() throws SQLException {
    if (this.conn != null && !this.conn.isClosed()) {
      this.conn.close();
    }
  }

}
```

```java
@Getter
@NoArgsConstructor(access = AccessLevel.PRIVATE)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class RoutingDataSource extends AbstractRoutingDataSource {

    private Map<Object, Object> targetDS = new HashMap<>();
    private HikariDataSource defaultTargetDS;

    public void setDataSources(List<InfoOfDBConnections> infoOfDBConnections) {
        targetDS = DataSources.of(infoOfDBConnections).get();
        resolve();
    }

    private void resolve() {
        setDefaultTargetDataSource(defaultTargetDS);
        setTargetDataSources(targetDS);
        afterPropertiesSet();
    }

}
```

마지막으로 routingDataSource.setDataSources(List<InfoOfDBConnections>) 을 호출하면, DataSource 가 INFO_OF_DB_CONNECTIONS 테이블과 동기화 됩니다. 


#### 다중 DataSource 사용하기
메뉴에서 서비스를 선택할 때마다, Path Variable 이 변경이 됩니다.

![36-menu_service](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/36-menu_service.PNG)
![37-ds_path_var](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/37-ds_path_var.PNG)

![38-use_ds](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/38-use_ds.svg)

우선 Axios Interceptor 에서는 path variables 에 따라서 http request 에 service-key 헤더 값을 저장합니다.
그럼 매 요청마다 params 의 db 값을 보고, service-key 헤더값이 달라집니다.

```javascript
import axios from 'axios';
import router from "@/router";

const setup = () => {
  axios.interceptors.request.use(
    config => {
      config.headers['service-key'] = router?.history?.current?.params?.db
        ?? null;
      return config;
    },
    error => Promise.reject(error)
  );
};
```

스프링 부트에서는 WebMvcConfigurer 를 구현한 WebMvcConfig 클래스에서, `addInterceptors(InterceptorRegistry registry)` 를 오버라이드 합니다.
registry 에 
1. `DataSourceControllerInterceptor` 인터셉터 Bean 을 추가합니다.
2. `.addPathPatterns("/api" + WILD)` /api 로 시작하는 모든 path 에서 `DataSourceControllerInterceptor` 를 거치도록 합니다.
3. `.excludePathPatterns(notLoadList)`"/api/managements" 로 시작하는 모든 path 에서 `DataSourceControllerInterceptor` 를 제외합니다. 
admin Database 에 접근할 때에는 `ResolveDefaultDataSource` 를 이용할 것이기 때문 입니다.

```java
@RequiredArgsConstructor
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

  private final DataSourceControllerInterceptor dataSourceControllerInterceptor;
  private static final String WILD = "/**";

  private final List<String> notLoadList = Collections.singletonList(
      "/api/managements" + WILD
  );

  @Override
  public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(dataSourceControllerInterceptor)
            .addPathPatterns("/api" + WILD)
            .excludePathPatterns(notLoadList)
    ;
  }
}
```

DataSourceControllerInterceptor 는 다음과 같습니다.

```java
@RequiredArgsConstructor
@Component
public class DataSourceControllerInterceptor extends HandlerInterceptorAdapter {

  private final RoutingDataSource dataSource;

  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
      Object handler) throws Exception {

    String DATA_SOURCE_TYPE_HEADER_NAME = "service-key";
    String serviceKeyOfHeader = request.getHeader(DATA_SOURCE_TYPE_HEADER_NAME);
    dataSource.validateTargetKey(serviceKeyOfHeader);

    DataSourceLookupKeyContextHolder.set(serviceKeyOfHeader);

    return super.preHandle(request, response, handler);

  }

  @Override
  public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
      ModelAndView modelAndView) throws Exception {
    DataSourceLookupKeyContextHolder.remove();
    super.postHandle(request, response, handler, modelAndView);
  }

}
```

우선 request header 에서 service-key 의 값을 가져와 유효성을 검사합니다.
```java
String serviceKeyOfHeader = request.getHeader(DATA_SOURCE_TYPE_HEADER_NAME);
dataSource.validateTargetKey(serviceKeyOfHeader);
```

RoutingDataSource 의 targetDS 에서 service-key 가 발견되지 않으면 에러를 던집니다.

```java
public class RoutingDataSource extends AbstractRoutingDataSource {

    private Map<Object, Object> targetDS = new HashMap<>();

    public void validateTargetKey(String serviceKey) {
        Optional.ofNullable(targetDS.get(serviceKey))
                .orElseThrow(InvalidServiceKeyOfHttpRequestHeaderException::new);
    }
}
```

lookupKey 의 값을 바꿔줍니다. 
```java
DataSourceLookupKeyContextHolder.set(serviceKeyOfHeader);
```

로직을 수행하고 컨트롤러 메서드가 종료되면 DataSourceControllerInterceptor 의 postHandle 메서드가 호출됩니다.
여기서는 ThreadLocal 변수 DATA_SOURCE_KEY 를 remove 해줍니다. 
쓰레드가 종료될 때, 특히 웹 애플리케이션의 경우 쓰레드 pool 로 공유되기 때문에 기존 데이터 clear 가 필요하기 때문입니다.

#### 동적으로 DataSource 변경하기
![05-dbconfig_main](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/05-dbconfig_main.jpg)

**DB Config** 메뉴에서는 DatSource 의 추가, 삭제, 변경이 가능합니다.

![39-ds_aspect](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/39-ds_aspect.svg) 

InfoOfDBConnectionService 의 findAll, save, deleteById, updatePassword, updateExcludePassword 를 하고나면 `UpdateDataSourceAspect` 의 update 메서드를 실행합니다.

```java
// ...
public class InfoOfDBConnectionService {

  @UpdateDataSource
  public List<InfoOfDBConnectionDTO> findAll() {
    // ...
  }
  
  // ...
}
```

UpdateDataSourceAspect 이후 과정은 최초 DataSources 초기화 방식과 같습니다.



### FE. Adapter 리팩터링

#### Key Point
1. `Promise` 객체 생성, `then`, `catch` 핸들러가 중복적으로 존재한다.
1. 중복적으로 존재하는 API PATH 가 상수화 되어있지 않다. 

다음은 `adapter.js` 코드의 일부 입니다.
~~~javascript
import ErrorHandler from './errorHandler';

const PATH = '/api/jobs';

export default {

  getJobList() {
    return new Promise(function (resolve, reject) {
      Axios.get(PATH)
        .then(res => resolve(res.data))
        .catch((error) => ErrorHandler.error(error, reject))
    });
  },

  getJob(jobId) {
    return new Promise(function (resolve, reject) {
      Axios.get(PATH + '/scheduler-names/' + jobId.schedulerName + '/job-groups/' + jobId.jobGroup + '/job-names/' + jobId.jobName)
        .then(res => resolve(res.data))
        .catch((error) => ErrorHandler.error(error, reject))
    });
  },

  deleteJob(jobId) {
    return new Promise(function (resolve, reject) {
      Axios.delete(PATH + '/scheduler-names/' + jobId.schedulerName + '/job-groups/' + jobId.jobGroup + '/job-names/' + jobId.jobName)
        .then(res => resolve(res.data))
        .catch((error) => ErrorHandler.error(error, reject))
    });
  }
}
~~~

#### 1. Axios Interceptor 사용
[axios.interceptor.response.use](https://github.com/axios/axios#interceptors) 는
응답에서 `then` 이나 `catch` 로 처리되기 전에 요청이나 응답을 가로챌 수 있습니다.

첫번 째 인자는 status 가 `2xx` 일 때, `then` intercept 하여 처리할 콜백 입니다. 
응답 본문이 있는 `response.data` 값 만을 `resolve` 해 줍니다.

status 가 `2xx` 이외의 값이라면 `catch` 를 intercept 하는 두번째 콜백이 실행 됩니다.  

~~~javascript
import axios from 'axios';
import ErrorHandler from "@/adapters/errorHandler";
import router from "@/router";

const setup = () => {
  // ...

  axios.interceptors.response.use(
    response => response.data,
    error => ErrorHandler.error(error)
  );
};

export default setup;
~~~
setup 을 `main.js` 에서 호출 해 줍니다.
~~~javascript
import axiosInterceptorSetup from '@/config/AxiosIntercepter';
// ...

axiosInterceptorSetup();
// ...
~~~

#### 2. 모든 API PATH 를 상수화
모든 API PATH 를 상수화 해줌으로써 얻은 이점으로서 다음과 같이 느꼈습니다.
1. API PATH 관심사에만 집중 할 수 있습니다. 서버의 API PATH 가 바뀔 때 마다, 여러 API Adapter 모듈 중 API PATH 가 존재하는 모듈을 식별해야 하는 번거로움이 해결되었습니다.
1. `JOB_ID` `TRIGGER_ID` `PAGING` 과 같이 여러 Adapter 모듈에 존재하는 `Path Variable` 과 `Quary Parameter` 의 중복을 제거 할 수 있게 되었습니다.
1. 중복된 문자열들을 상수로 관리해 줌으로써, 코딩을 할 때의 실수를 줄여 줄 수 있었습니다.  

추가적으로 API PATH 상수를 서버와 일치시켜 주면 유지보수에 더욱 좋을 것 같다는 생각이 들었습니다. 
~~~javascript
const API = '/api';

// ...
export const JOB = `${API}/jobs`;

export const JOB_ID = ({ schedulerName, jobGroup, jobName }) => (
  `/scheduler-names/${schedulerName}/job-groups/${jobGroup}/job-names/${jobName}`
);

export const TRIGGER_ID = ({ schedulerName, triggerGroup, triggerName }) => (
  `/scheduler-names/${schedulerName}/trigger-groups/${triggerGroup}/trigger-names/${triggerName}`
);

export const PAGING = (page, size) => `?page=${page}&size=${size}`;
~~~

#### 개선 결과
Axios Response Interceptor 와 API PATH 의 상수화를 적용하여 `adapter.js` 를 다음과 같이 개선하였습니다.
~~~javascript
import Axios from 'axios';
import * as API from "./apiPath";

const PATH = API.JOB;

const getJobList = () => Axios.get(PATH);
const deleteJob = (jobId) => Axios.delete(PATH + API.JOB_ID(jobId));
const getJob = (jobId) => Axios.get(PATH + API.JOB_ID(jobId));

export default {
  getJobList, getJob,
  deleteJob
}
~~~

### FE. 모든 문자열 상수를 key value 쌍의 객체로 모듈화
Quartz Scheduler Admin 인 만큼 앱에서는 [Quartz 용어](https://www.baeldung.com/spring-quartz-schedule)들이 중복적으로 매우 많이 존재하였습니다. 

> Quartz 용어에 대해서는 아래 사이트에서 설명이 되어 있습니다.
> - [quartz-scheduler](http://www.quartz-scheduler.org/documentation/quartz-2.1.7/tutorials/tutorial-lesson-04.html)
> - [Spring Boot - 스프링 부트 Quartz!](https://kouzie.github.io/spring/Spring-Boot-%EC%8A%A4%ED%94%84%EB%A7%81-%EB%B6%80%ED%8A%B8-Quartz/#schedulerfactory-scheduler)
> - [baeldung](https://www.baeldung.com/spring-quartz-schedule)

하지만, 같은 용어지만 공백, 영어 대소문자 등 일치하지 않는 실수들이 많이 존재하게 되었습니다. 
그래서 `constants.js` 에서 key value 쌍의 객체를 내보내기 하였습니다.  
~~~javascript
export default Object.freeze({
  quartz_scheduler_admin: 'QUARTZ SCHEDULER ADMIN',
  db_connection_test_success: '테스트 연결 성공',
  db_connection_test_fail: '테스트 연결 실패',
  success: 'SUCCESS',
  error: 'ERROR',
  cron_trigger_list: 'Cron Trigger List',
  title: 'title',
  refresh: 'refresh',
  scheduler_name: 'SchedulerName',
  trigger_group: 'TriggerGroup',
  // ...
});
~~~ 

`constants.js` 모듈을 모든 vue 컴포넌트에서 `import` 없이 사용 가능하도록 하기위해,
 `main.js` 에서 vue 의 prototype 프로퍼티에 등록을 해주었습니다.
~~~javascript
import constants from '@/commons/constants';

// ...

Vue.prototype.$constants = constants;
~~~

vue 컴포넌트에서 import 없이 사용할 수 있게 되었습니다.
```html
<template>
  // ...
</template>
<script>
// ...
export default {
  // ... 
  computed: {
    nameOfLoginButton() {
      return this.myRole ? this.$constants.logout : this.$constants.login;
    },
  },
  // ...
};
</script>
```

Quartz 이외에도 중복된 문자들이 많이 존재하였습니다. 
이 왕 모든 문자열을 상수화 하는 시도를 해보았는데요, 현재 하나의 모듈에 상수의 종류 구분없는 방대한 상수 모듈이 탄생하게 되었습니다. 

추가적으로 상수를 관리방법의 이해와 개선이 필요할 것 같습니다.

### FE. Base 컴포넌트 생성 리팩터링

모든 view 에서 공통적인 요소 스타일들을 가지고 있으며, 하나의 view 에서 조차 중복된 코드들이 매우 많이 존재하였습니다.  
UI 의 통일성을 유지하기 위한 목적으로 하나의 컴포넌트로 만들어 재사용 하도록 변경하였습니다.

![23-base_components](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/23-base_components.PNG)

![24-base_components_modules](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/24-base_components_modules.PNG)

![25-base_componets_3](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/25-base_componets_3.svg)
![26-base_components_4](/images/portal/post/2021-01-25-ZUM-Pilot-advanced_quartz_scheduler_admin/26-base_components_4.svg)

그 중 `BaseDialogWrapper` 의 형태는 다음과 같습니다.

`App.vue` 의 최상단 컴포넌트에 위치하고 있습니다.
```html
<template>
  <div id="app">
    <Layout>
      <router-view></router-view>
    </Layout>
    <base-dialog-wrapper/>
  </div>
</template>
// ...
```

`BaseDialogWrapper.vue` 의 코드는 다음과 같습니다.
```html
<template>
  <el-dialog
      :title="modalTitle"
      :visible.sync="isModalOpen"
      :before-close="close"
  >
    <component
        v-if="isModalOpen"
        :is="component"
        :prop="modalData"
    />
  </el-dialog>
</template>

<script>
import {createNamespacedHelpers} from 'vuex';

const components = createNamespacedHelpers('components');

export default {
  name: 'BaseDialogWrapper',
  computed: {
    ...components.mapState([
      'isModalOpen',
      'modalTitle',
      'modalComponentPath',
      'modalCloseHandler',
      'modalData'
    ]),

    component() {
      if (!this.isModalOpen || !this.modalComponentPath) {
        return null;
      }
      return () => import(`@/components${this.modalComponentPath}`);
    },
  },

  methods: {
    ...components.mapMutations(['closeModal']),

    close() {
      this.modalCloseHandler && this.modalCloseHandler();
      this.closeModal();
    }
  }
};
</script>

<style>
.el-dialog {
  width: 80%;
  max-width: 700px;
  text-align: left;
}
</style>
```
이 컴포넌트의 대표적인 두 가지 특징이 있습니다.

1. 모든 상태값은 `components` 라는 namespace `store` 를 참조하고 있다.

```javascript
import {createNamespacedHelpers} from 'vuex';

const components = createNamespacedHelpers('components');
export default {
  // ...
 computed: {
    ...components.mapState([
      'isModalOpen',
      'modalTitle',
      'modalComponentPath',
      'modalCloseHandler',
      'modalData'
    ]),
  // ...
  }
}
```

2. `components` store 의 modalComponentPath 의 값으로 모듈을 동적으로 `import` 하고 있습니다.

```javascript
computed: {
    component() {
      if (!this.isModalOpen || !this.modalComponentPath) {
        return null;
      }
      return () => import(`@/components${this.modalComponentPath}`);
    },
}
```

다른 컴포넌트에서 Modal 을 Open 할 때 다음과 같이 사용을 할 수 있습니다.

```html
<template>
  <div>
    <!-- ... -->
    <base-data-table>
      <!-- simpleTrigger 를 추가하는 Modal 을 Open 하는 버튼 -->
      <el-table-column>
        <template slot-scope="scope">
          <el-button @click="addSimpleTrigger(scope.row)">
            {{ $constants.ADD }}
          </el-button>
        </template>
      </el-table-column>
      <!-- Job 의 Detail 을 조회하는 Modal 을 Open 하는 버튼 -->
      <el-table-column>
        <template slot-scope="scope">
          <base-detail-button :on-click-handler="() => showDetailJob(scope.row)"/>
        </template>
      </el-table-column>
    </base-data-table>
  </div>
</template>

<script>
import {createNamespacedHelpers} from "vuex";

const components = createNamespacedHelpers('components');

export default {
  name: 'QuartzJobList',
  // ...
  methods: {
    ...components.mapMutations(['openModal', 'closeModal']),
  
    // Simple Trigger 을 추가하는 컴포넌트를 포함하는 Modal 을 Open 합니다.
    addSimpleTrigger({ id }) {
      this.openModal({
        componentPath: '/SimpleTriggerAddForm',
        title: this.$constants.add_simple_trigger_title,
        data: {
          createSimpleTrigger: this.createSimpleTrigger(id, () => this.submitSimpleTriggerForm(id))
        }
      })
    },

    // Job 의 Detail 을 조회하는 컴포넌트를 포함하는 Modal 을 Open 합니다.
    showDetailJob({ id }) {
      this.openModal({
        componentPath: '/QuartzJobDetail',
        title: this.$constants.detail,
        data: {
          jobId: id,
        }
      })
    },
  },
};
</script>
```

## 후기


Reference
--
- [Spring Batch + Quartz 포털개발팀 권용근 (열람 권한 필요)](https://docs.google.com/presentation/d/1W2fB2nACLrV6vI1T_PHBf4NLWy5J08lbg8gyXmWvF88/edit#slide=id.g2419c9415d_0_266)
- [Quartz Job Scheduler란?](https://advenoh.tistory.com/51)




