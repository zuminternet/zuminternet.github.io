---
layout: post

title: Tuist 도입부터 적용까지 알려ZUM요! (feat. iOS프로젝트)

description: ZUM에서 Tuist를 iOS프로젝트에 어떻게 적용하고 있는지 공유합니다.

image: /images/ios/2023-05-09-iOS-tuist-module/기술블로그이미지.svg

introduction: ZUM에서 Tuist를 iOS프로젝트에 어떻게 적용하고 있는지 공유합니다.

category: ios/tech

tag: [tuist, 모듈화, iOS, 리팩토링]

author: namsoo5

---

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fzuminternet.github.io%2FiOS-tuist-module%2F&count_bg=%235D5F5C&title_bg=%235D5F5C&icon=swift.svg&icon_color=%23FF9800&title=++++%F0%9F%A7%A1&edge_flat=false)](https://hits.seeyoufarm.com)

![graph5](/images/ios/2023-05-09-iOS-tuist-module/기술블로그이미지.svg)

> 안녕하세요 ZUM iOS개발자 김남수(Enes)입니다.
> 
> ZUM에서는 Tuist를 어떻게 도입하게 되었는지, 어떻게 사용하고 있는지와
> 
> Tuist를 적용한 프로젝트를 개선한 경험을 공유하고자 합니다.
> 
> 가이드 없이 맨땅에 시작한 Tuist와 모듈 아키텍쳐 학습을 기반으로 설계하고 개발한 경험을 공유하는 글이여서 부족한 부분이 있을 수 있습니다.
> 
> 편하게 읽어주시면 감사하겠습니다 :)

## Tuist 란?

Xcode 프로젝트 생성과 유지관리를 편리하게 하는 것을 목표로 하는 CLI 도구입니다.

`Project.swift`파일을 기반으로 프로젝트(.xcodeproj)를 생성해 줍니다.

이 파일에 프로젝트의 설정값을 정의하면 프로젝트 생성 시 정의한 설정값으로 생성됩니다.

이를 통해 프로젝트 설정값을 실수로 건드려서 일어날 에러를 방지할 수 있습니다.

## Tuist 도입

사실 Tuist의 도입을 특별하게 시도한 것은 아니였습니다.

제가 입사했을 때 이미 한 프로젝트에 사용 중이었습니다.

다른 툴들도 있지만 자연스럽게 Tuist를 먼저 사용하게 됐습니다.

Tuist를 학습하면서 느낀 편리한 점은 아래와 같습니다.

---

**1. xcodeproj 파일이 없다.**

프로젝트를 커맨드 명령어로 그때그때 생성해 주기 떄문에 github에 .xcodeproj 프로젝트를 올리지 않고 코드만 올립니다. 따라서 협업 시 쉽게 경험해 볼 수 있는 프로젝트 파일경로에 관한 git 충돌을 회피할 수 있습니다.

**2. 모듈화하기 편리하다.**

Project파일을 생성하고 프로젝트와 타겟을 만들어 주는 메서드를 정의해 두면 모듈 생성 시 호출만 해서 사용하면 모듈 셋팅이 금방 끝납니다.

**3. 프로젝트의 모듈 의존관계를 파악하기 쉽다.**

Tuist의 큰 장점 중 하나라고 생각합니다. 의존된 모듈을 찾아가지 않아도 명령어 하나면 이미지로 보기 쉽게 의존 그래프를 그려줍니다.

**4. swift언어를 이용해서 모듈과 프로젝트 설정을 정의할 수 있다.**

Tuist 모든 설정 파일을 정의할 땐 swift를 사용합니다.

---

기존 프로젝트는 모듈화 없이 하나의 모듈에 모든 코드가 있었습니다.

모듈화하여 빌드속도를 향상하고 협업의 능률을 올릴 수 있도록 개선할 수 있을 것 같다는 생각이 들었습니다.

구조를 재설계했지만 이미 많은 개발이 이뤄진 프로젝트라 모든 구조를 수정하기에 아쉽게도 주어진 시간이 부족해서 실제로 적용하지 못했습니다.

기존 프로젝트에 적용하지 못 한 채 남겨진 모듈화를 새 프로젝트에서는 제대로 적용해 보고 싶었습니다.

처음부터 완벽하게 사용할 수 없는 기술이라고 생각하고, 모듈 아키텍처는 개발하며 개선할 부분이 보이면 수정될 수 있다는 마음을 갖고 시작했습니다.

## Tuist 사용

### 스키마 적용

프로젝트에서 Tuist를 어떻게 사용하는지 간단하게 알아보겠습니다. 

우선 프로젝트를 Tuist로 생성할 때 스키마를 선택합니다.

```shell
TUIST_MODE=INHOUSE tuist generate
```

TUIST_MODE라는 환경변수를 이용하여

개발용, 사내배포용, 마켓배포용을 구분하여 환경을 다르게 설정하고 있습니다.

이렇게 정의한 값은 딕셔너리형태로 값을 가져올 수 있고

```swift
// Project.swift
private let environments = ProcessInfo.processInfo.environment
private let modeString: String = environments["TUIST_MODE"] ?? "DEV"
private let mode: TuistMode = TuistMode(value: modeString)
```

위와 같이 타입으로 빼서 간편하게 사용하고 있습니다.

```swift
let project = Project.create(
    name: mainProjectName,
    packages: [],
    settings: Settings.projectSettings,
    targets: [targetWithMode(mode)],
    schemes: [schemeWithMode(mode)]
)
```

Project타입에 필요한 변수만 정의해서 사용할 수 있도록 내부적으로 create메서드를 정의해 줬고

처음에 터미널에 입력해 준 환경변수 모드에 따라서 타겟과 스키마를 정의하여 메인 프로젝트를 생성합니다.

```swift
private func targetWithMode(_ mode: TuistMode) -> Target {
    print("\n🐙 TUIST_MODE >>>> \(mode)")
    if mode == .release {
        return mainTarget
    } else if mode == .inhouse {
        return inhouseTarget
    } else {
        return devTarget
    }
}
```

터미널에서 생성 시에 해당 프로젝트가 어떤 모드로 생성되는지 눈으로 쉽게 확인할 수 있도록 로그도 추가해 줬습니다.

![tuistModeLog](/images/ios/2023-05-09-iOS-tuist-module/tuistModeLog.png)

위와 같이 터미널에서 확인하실 수 있습니다.

### Target Extension

글을 더 써 내려가기 전에 잠깐 모듈의 구조를 설명해야 아래의 글에 도움이 될 것 같아서 먼저 언급하려고 합니다.

저희 팀은 클린아키텍쳐를 지향하기 때문에 Presentation영역에 해당하는 Feature모듈

Domain영역에 해당하는 Domain모듈

Data영역에 해당하는 Repository, Service모듈로 구분해서 개발했습니다.

레이어별로 모듈을 생성하는 방법이 비슷해서 비슷한 모듈끼리 간편하게 생성할 수 있도록 공통화시켜 사용했습니다.

아래는 Service모듈 타겟 생성에 대한 함수입니다.

```swift
public static func createService(
    service: Service,
    infoPlist: [String: InfoPlist.Value],
    dependencies: [TargetDependency] = []
) -> Target {
    var baseDependencies: [TargetDependency] = [
        .coreProject
    ]
    dependencies.forEach { baseDependencies.append($0) }
    return Target.create(
        targetName: "\(service.rawValue)Service",
        product: .framework,
        infoPlist: infoPlist,
        isNeedResource: false,
        dependencies: baseDependencies
    )
}
```

Core모듈을 사용하기 때문에 기본적으로 의존성을 추가해 주고 외부에서 의존성을 추가 확장할 수 있도록 구현했습니다.

또한 생성 시 모듈의 네이밍을 맞추기 위해서 타입을 사용했습니다.

이와 같이 feature, domain, service, repository, demo앱 타겟을 편리하게 만들 수 있도록 정의된 함수를 사용합니다.

아래 코드는 위의 방식을 적용한 Project파일입니다.

```swift
// Project.swift
let authFeatureTarget = Target.createFeature(
    targetName: Feature.auth.name,
    infoPlist: infoPlist,
    dependencies: [
        .Domain.authProject
    ]
)

let authFeatureDemoTarget = Target.createDemoApp(
    targetName: Feature.auth.demoAppName,
    infoPlist: infoPlist,
    dependencies: [
        .target(authFeatureTarget)
    ]
)

// MARK: - Project

let project = Project.create(
    name: Feature.auth.name,
    packages: [
    ],
    targets: [
        authFeatureTarget,
        authFeatureDemoTarget
    ],
    schemes: []
)
```

### TargetDependency

TargetDependency는 아래와 같이 모듈 타입에 맞는 이름과 경로를 구현해 두고 사용하고 있습니다.

```swift
public protocol ModuleNaming: RawRepresentable<String> {
    var name: String { get }
    var rootPath: String { get }
}

extension ModuleNaming {
    public var name: String { "\(self.rawValue)\(type(of: self))" }
    var path: String { "\(type(of: self))/\(name)" }
    public var rootPath: String { "\(workspaceName)/\(path)" }
}

public enum Feature: String, ModuleNaming {
    case auth = "Auth"
}
```

상대경로를 사용했을 때 모듈 구조를 바꾼다던가 의존관계를 바꿨을 때 복잡해져서 절대적인 root경로를 사용하고 있습니다.

```swift
public extension TargetDependency {
    static let authProject: TargetDependency = .project(
        target: Feature.auth.name,
        path: .relativeToRoot(Feature.auth.rootPath)
    )
}
```

### 모듈 생성 템플릿 자동화

모듈을 생성할 때 해야 하는 작업으로

1. 원하는 위치에 모듈 디렉토리 만들기

2. Project 파일 만들기

3. target, project 정의하기

4. 상황에 맞게 Sources폴더, Demo폴더, Resources폴더 만들기

5. 빈 파일 만들기 (프로젝트 생성 시 빈 폴더는 안뜨기 때문)

6. 정의한 모듈을 사용하는 곳에 의존성 추가하기

보통 이렇게 이뤄집니다.

모듈을 한두 개 만들고 끝나는 게 아니라 여러 기능을 개발하며 계속 모듈을 추가하는 작업이 반복되니 비효율적이라 느껴졌습니다.

또한, 모듈 생성 시에 뭔가를 누락시켜서 휴먼에러가 발생할 확률을 낮추고 모듈끼리 포맷도 일치시키는 효과를 기대하며 1~5에 해당하는 부분을 **tuist의 scaffold를 사용한 stencil 템플릿으로 자동화**해서 모듈 생성에 사용되는 시간을 줄였습니다.

```shell
tuist scaffold {template이름} --name {모듈이름}
```

명령어를 통해 name값을 받아서 모듈의 이름을 어떤 이름으로 할 것인지 지정합니다.

위에서 받은 name값을 기반으로 모듈 이름과 경로를 생성해서 사용합니다.

```swift
let featureName = Template.Attribute.required("name")

let featureTemplate = Template(
    description: "Feature Template",
    attributes: [featureName],
    items: [
        .file(
            path: "\(workspaceName)/Feature/\(featureName)Feature/Project.swift",
            templatePath: "Project.stencil"
        ),
        .directory(
            path: "\(workspaceName)/Feature/\(featureName)Feature/",
            sourcePath: .relativeToRoot("Temp/Sources")
        ),
        .directory(
            path: "\(workspaceName)/Feature/\(featureName)Feature/",
            sourcePath: .relativeToRoot("Temp/Demo")
        )
    ]
)
```

위의 코드는 Feature모듈을 만들 때 사용되는 템플릿입니다.

![stencil_feature](/images/ios/2023-05-09-iOS-tuist-module/stencil_feature.png)

stencil파일을 사용하여 Project파일을 만들어 주고

모든 모듈에서 사용할 빈 파일을 구성해 놓은 Sources와

데모 앱의 시작점인 App 부분을 정의해 놓은 Demo를 가져다가 모듈을 구성해 줍니다.

명령어 실행 시 feature모듈을 생성할 때마다 입력해 줬던 코드와 동일하게 작성됩니다.

![stencil_feature](/images/ios/2023-05-09-iOS-tuist-module/stencilFilter.png)

stencil파일을 보면 이상한 문법의 코드가 하나 보이는데

이 코드는 name 단어(모듈 이름)에서 첫 번째만 소문자로 변환시키는 역할을 합니다.

변수명을 소문자로 쓰고 싶었기 때문에 추가해 줬습니다.

더 많은 문법은 stencil문법을 참고하시면 좋습니다.

계속해 줬던 반복 작업을 명령어 하나로 해결했습니다. 👏

## 모듈 아키텍처 구조 히스토리

모듈의 단위를 어떻게 가져갈 것인지 처음에 고민했습니다.

1.각 계층별로 가져가기 (feature, domain ,data영역이 각각모듈인 경우)

2.각 기능별로 가져가기 (feature, domain, data영역이 같은모듈인 경우)

각 케이스별로 모의 그래프를 그려가서 고민을 같이 논의했고 1번 케이스 같은경우 관리 포인트가 너무 많을 것 같다는 의견에 모듈수가 상대적으로 적게 나올 것 같은 2번 케이스로 시작했습니다.

시작은 아래 의존 그래프와 같습니다.

![graph4](/images/ios/2023-05-09-iOS-tuist-module/graph4.png)

기능별로 피쳐를 나누고 공통 모델을 Domain모듈로 빼고 UI, Core를 관심사에 맞게 분리했습니다.

FeatureAuth모듈에는 Auth관련 뷰와 AuthUseCase, AuthRepository, AuthService가 존재합니다.

저희 서비스의 특성상 공통으로 사용해야 하는 몇몇 UseCase들이 있었고

초기서비스라서 변경될 가능성이 크기 때문에

각각 피쳐에 똑같은 코드인 별도의 UseCase를 두기보다 공통으로 가져다가 쓰는 게 관리 측면에서 용이할 것 같다고 생각하여 공통 모델들을 사용할 모듈을 추가했습니다.

적용한 그림은 아래의 그래프와 같습니다.

![graph5](/images/ios/2023-05-09-iOS-tuist-module/graph5.png)

CommonLogic모듈에 공통으로 사용하는 UseCase를 넣어두고 사용하도록 했습니다.

하지만 이 구조에도 문제가 있었습니다.

다른 모듈의 화면 간 서로 참조가 일어나야 하는 경우 서로 모듈을 import해야 해서 dependency cycle에 걸린다는 문제가 있습니다.

이런 구조는 서로화면을 참조하지않고 독립적인 기능인 요구사항에 좀 더 적합하다고 생각했고

이 프로젝트에서는 뷰 간 서로 이동하는 요구사항이 좀 있었기 때문에 구조변경이 필요해 보였습니다.

고민하며 변경하다 보니 위에서 고민한 방식 중 1번처럼 각 계층별로 모듈을 다시 나누게 되었습니다.

나눈 뒤의 모듈의 그래프는 아래의 다이어그램과 같습니다.

<img src="/images/ios/2023-05-09-iOS-tuist-module/graph15.png" width="400" height="600">

Feature모듈에서 코디네이터를 이용해서 UseCase, Repository, Service 인스턴스 DI가 이뤄지기 때문에 모두 알아야 한다고 생각했습니다.

Repository는 DTO모델을 Domain모델로 변환하는 역할을 담당하므로 Domain에 대한 정보와 DTO에 대한 정보가 모두 있어야 했고,
Service는 통신을 담당하므로 DTO에 대한 정보가 있어야 했기에
Repository가 Service를 의존하고 Service가 Domain을 의존하게 된다면 자연스레 모두 알 수 있게 되고,
Feature가 Repository만 참조하도록 하면 나름 이쁜 그래프를 볼 수 있을 것 같아서 흡족해하면서 구성했습니다.

Feature -> Repository -> Service -> Domain 식의 의존 형태를 띄고 있습니다.

여기서 드는 의문이 하나 생깁니다.

Domain모듈은 Repository모듈을 모르는데 어떻게 사용하는가?

Domain모듈에서 Repository의 타입을 알아야 UseCase에서 Repository를 호출하여 원하는 동작을 실행 할 수 있을 것입니다.

```swift
public final class SomeUseCaseImpl: SomeUseCase {
    private let repository: any SomeRepository
}
```

이 문제를 DIP(의존성 역전 원칙)을 이용하여 
Domain모듈에 Repository인터페이스를 두고 Repository모듈에서 Domain모듈의 인터페이스를 채택하여 구현하느 방식으로 해결했습니다.

추가적으로, 그래프에서 보이는 컨테이너 모듈의 역할은 의존성을 모아주는 역할로 사용하고 있습니다.
모듈 추가 시 컨테이너에 의존성만 추가해 주면 위에서 편하게 사용할 수 있도록 하는 목적입니다.

하지만❗️

그래프가 한 방향으로 가는 게 이쁜 것 같았지만 몇 가지 개선점이 보였습니다.

클린아키텍쳐 구조를 생각해 보면

**프레젠테이션 영역은 데이터 영역을 굳이 알 필요는 없습니다.**

따라서 레이어별로 나눴기 때문에 모듈 아키텍처에도 적용해 볼 수 있겠다고 생각했습니다.

**또한, 현재 모듈 간 의존 그래프에서 빌드속도에 영향을 미치는 부분이 있어 보였습니다.**

컨테이너를 기준으로 하위의 모듈들이 모두 링킹돼야 상위 모듈 링킹이 진행될 것입니다.

**모듈 간 의존관계의 가시성이 좋지않습니다.**

`tuist graph`를 사용하여 그래프로 의존 관계를 봤을 때,
모든 모듈들이 Container에 연결돼 있기 때문에 소스 코드나 Project파일을 보지 않는 이상 모듈 간 의존관계를 파악하기 어려웠습니다.

실제로 테스트 한 결과

| 변경 전 아키텍처                                                                                             | 변경 전 빌드 타임로그                                                                                    |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| <img src="/images/ios/2023-05-09-iOS-tuist-module/moduleDiagram_before.png" width="500" height="600"> | <img src="/images/ios/2023-05-09-iOS-tuist-module/linking_before.png" width="500" height="300"> |

위의 사진같이 변경전 아키텍처일 때

링킹시 하위 모듈의 모든 빌드가 끝나야 이뤄지는 링킹 과정때문에 공백이 크게 있는 것을 확인 할 수 있었습니다.

모듈 다이어그램에서 이러한 부분이 발생하는 곳으로 예를 들면 Cotainer모듈이 있습니다.

병렬 빌드를 좀 더 활용하기 위해서 Feature모듈과 Repository모듈을 지금과 같이 상하관계로 의존하지 않고 별도로 구성한다면 빌드속도 향상을 기대해 볼 수 있을 것 같았습니다.

또한 불필요한 도메인까지 아는 것은 좋지 않다고 판단하여 도메인 컨테이너 모듈을 제거하고 필요한 도메인 모듈을 직접 참조하도록 변경했습니다.

제일 최상위인 메인 앱에서 DI를 해주도록 하기 위해 Feature와 Repository 컨테이너 모듈을 유지했습니다.

서로 분리했기 때문에 마지막으로 빌드되는 부분이고 이 모듈들은 속도에 큰 영향이 없다고 판단했습니다.

변경한 구조는 아래와 같습니다.

| 변경 후 아키텍처                                                                                            | 변경 후 빌드 타임로그                                                                                   |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| <img src="/images/ios/2023-05-09-iOS-tuist-module/moduleDiagram_after.png" width="700" height="400"> | <img src="/images/ios/2023-05-09-iOS-tuist-module/linking_after.png" width="300" height="300"> |

Feature -> Domain

Repository -> Domain

식의 의존 형태입니다.

변경 전과 다른 점으로는 빌드시 Repository를 기다린 뒤 Feature모듈이 링킹됬다면

변경 후에는 Repository와 Feature상관없이 먼저 빌드가 끝나는 대로 링킹되는 걸 확인 할 수 있었습니다.

구조를 변경하여 빌드 진행시 유휴시간을 줄임으로써

변경 전 빌드속도와 변경 후 빌드속도를 체크했을 때

![buildtime_beforeMax](/images/ios/2023-05-09-iOS-tuist-module/buildtime_beforeMax.png)
![buildtime_afterMax](/images/ios/2023-05-09-iOS-tuist-module/buildtime_afterMin.png)

**빌드속도가 최대 38초로 약 25% 향상**된 것을 확인할 수 있었습니다.

<br/>

모듈화를 하면서 개인적으로 생각한 장단점입니다.

##### 모듈화했을 때 불편하다고 생각한 점

- 모듈화 러닝 커브

- 접근제어자의 설정

##### 모듈화했을 때 좋다고 생각한 점

- 아키텍처 컨벤션

- 빌드속도의 향상 ⭐️

- 모듈별로 앱을 실행할 수 있어서 개발 용이

- 접근제어자의 설정

- 협업 용이

모듈 아키텍처를 구성해 놓고 개발하게 되면 코드의 분리로 인하여 불필요한 접근을 막을 수 있고 모듈에 해당하는 기능에 집중하여 개발할 수 있습니다.

접근제어자를 변경하게 됐을 때 변경돼야 할 부분이 많아서 불편하지만, 다른 모듈에서 쓰는 부분과 안 쓰는 부분을 구분할 수 있어 좋다고 생각했기 때문에 두 곳 모두 적었습니다.

주목적은 빌드속도의 향상이었기 때문에 모듈화를 통해 큰 성과를 얻었다고 생각합니다.

## 끝내며...

하나의 모듈로 구성된 프로젝트일 땐 개발하며 코드의 위치나 관계에 많은 신경을 쓰지 않았던 것 같습니다.

파일이나 코드가 어디에 위치하더라도 사용할 수 있기 때문에 신경을 쓰더라도 놓친 부분도 있었을 겁니다.

보통 private과 internal정도의 구분을 고려하며 개발한다면 모듈화를 하면서 public과 internal의 구분도 고려하게 됩니다.

모듈화를 진행하면서부터는 다른 모듈에 접근해야 하므로 위치를 신경 썼고 기능들이 잘 분리되도록 고민했습니다.

처음엔 복잡해서 어려움이 있었지만, 많은 시행착오를 겪었고 수정을 반복하며 개발 요구사항과 잘 맞고 최선이라고 생각하는 구조를 선택해서 결정했습니다.

그땐 힘들었더라도 지금 돌아보면 모듈화를 직접 고민하고 적용해 볼 수 있는 좋은 기회와 좋은 경험을 한 것 같다는 생각이 듭니다.

아직도 현재 구성한 구조가 좋은 구조라는 확신은 없습니다.

다음에 개선할 점이 보이거나 더 좋은 인사이트를 접하게 된다면 열린 마음으로 수정할 예정입니다.

<br/>

Tuist사용과 모듈화를 어떻게 시작해서 변경시켜 왔는지 의식의 흐름처럼 글을 써가서 말이 이상하거나 부족한 부분이 있을 수 있습니다.

부족하지만 모듈화에 대해 고민하시는 분들께 이 자료가 참조되고 도움이 됐기를 바라며 짧지 않은 글 읽어주셔서 감사합니다.
