

# 블로그 작성 가이드

ZUM 기술 블로그 작성 가이드 입니다.

모든 소스는 현재 repository에서 관리가 되며 github page의 포스팅 엔진 jekyll 규격을
준수합니다.
또한 포스팅 작성시 마크다운을 (https://kramdown.gettalong.org/syntax.html) 사용 합니다.

### (1) 작성 진행 순서 ###

* 작성을 하기 위해서는 반드시 [giihub]("https://github.com/zuminternet/zuminternet.github.io")에 대한 "write" 권한이 필요하기 때문에
관리자(beyondj2ee@zuminternet.com)에게 권한을 요청 합니다. 단, 요청을 보낼때 github 계정을 알려주셔야 합니다.
* jekyll를 설치를 합니다.
* 포스팅을 작성 하고 로컬에서 확인이 완료되면 github 레파지토리로 push를 보내면 배포가 완료 됩니다.

### (2) 설치 프로그램 ###

여기서는 window 버전으로만 설명을 드리겠습니다.

* Ruby(ruby, DevKit)
* Jekyll
* Python(Setuptool,pip,Pygments)
* rouge
* npm (선택)


### (3) Ruby 설치 하기 (Window 버전) ###

사이트에 접속 후 ruby 와 Devkit 같이 포함된 버전을 [다운로드]("https://rubyinstaller.org/downloads/") 받습니다.

![다운로드](/images/readme/1.png)

설치 시 실행파일을 Path에 포함하도록 선택 합니다.

![설치1](/images/readme/2.png)
![설치2](/images/readme/3.png)
![설치3](/images/readme/4.png)
![설치4](/images/readme/5.png)

설치 확인을 한다.

![설치5](/images/readme/33.png)

### (4) Jekyll 및 ruby 라이브러리 설치  ###
![설치5](/images/readme/7-1.png)

아래 라이브러리도 설치를 합니다.

* gem install rouge
* gem install minima
* gem install bundler
* gem install jekyll-feed
* gem install tzinfo-data
* gem install wdm

### (5) Python 설치  ###

지킬(Jekyll)에서 syntax highlighter를 사용하기 위해 Python을 설치가 필요 합니다.
[다운로드]("https://www.python.org/downloads/") 받습니다.


![설치5](/images/readme/9.png)
![설치5](/images/readme/10.png)
![설치5](/images/readme/11.png)
![설치5](/images/readme/12.png)

Pygments를 설치 합니다.
![설치5](/images/readme/14.png)

### (6) Jekyll 설치 확인  ###

최종적으로 설치가 완료가 되었는지 확인을 합니다.

![설치5](/images/readme/15.png)


### (7) 로컬 실행하기  ###
![설치5](/images/readme/g1-1.png)

소스를 clone 한다.
```text
    git clone https://github.com/zuminternet/zuminternet.github.io.git"
```

해당 소스 루트 디렉토리로 이동을 하고 서버를 기동 한다.

![설치5](/images/readme/20.png)

로컬서버 http://localhost:4000 에 접속해서 확인을 한다. 

![설치5](/images/readme/32_.png)

### (8) 포스트 디렉토리 가이드  ###

포스트를 작성하기 위해서는 **"_post"** 디렉토리(jekyll은 _post 디렉토리 안에 있는 것을 포스트로 인식 한다.) 와 이미지를 저장하기 위한 **"images"** 디렉토리를 사용한다.

![설치5](/images/readme/p2.png)

부서별 사용하는 디렉토리는 아래와 같다.

![설치5](/images/readme/t2.png)

포스트 파일명은 반드시 아래의 규칙을 준수한다.
(jekyll 표준)

**yyyy(4자리)-mm(2자리)-dd(2자리)-제목.md**

예) _posts/부서별 루트 디렉토리/2016-06-16-blog.md


![설치5](/images/readme/p4.png)


### (9) 포스트 작성 가이드  ###


포스트의 노출을 위해서 머릿말 속성을 반드시 숙지해야 한다.

![설치5](/images/readme/23_.png)

중요 속성은 아래와 같다.

![설치5](/images/readme/t1_.png)


title 속성은 아래와 같이 노출 된다.

![설치5](/images/readme/25_.png)

image 속성은 아래와 같이 노출 된다.

![설치5](/images/readme/24_.png)


introduction 속성은 아래와 같이 노출 된다.

![설치5](/images/readme/26_.png)

포트스 내용은 [kramdown]("https://kramdown.gettalong.org/syntax.html") 마크다운으로 작성한다.

![설치5](/images/readme/p99.png)


### (10) 포스트 발행하기  ###

로컬에서 확인이 완료되면 github에 푸시를 한다.

소스를 clone 한다.
```text
    git push origin master
```

포스트를 변경할 경우 cache 적용으로 인해서 30초 ~ 1분정도 지나서 업데이트가 된다.


### (11) 사이트 관리  ###

전체 페이지 레이아웃 및 css를 관리하려면 gulp로 빌드를 해야 한다.

gulp를 설치하고 build를 해야 한다.

npm install <br/>

npm install -g gulp gulp-cli <br/>

gulp <br/>

참고 사이트 (https://github.com/thiagorossener/jekflix-template)

