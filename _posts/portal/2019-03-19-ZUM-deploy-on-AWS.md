---

layout: post

title: Public Cloud(AWS) 기반 CD(Continuous Delivery or Continuous Deploy) 도입

description: AWS CD(Continuous Delivery or Continuous Deploy) 사용기

image: /images/portal/post/2019-03-19-ZUM-deploy-on-AWS/00.PNG

introduction: AWS기반 배포 자동화 구축 및 사용 후기

category: portal/tech

tag: [experience, infra, deploy, aws, code-series, lambda, ec2]

---

> 이 글은 줌인터넷에서 개발자들에게 간편한 배포와 정확한 QA를 진행하기 위한 CD를 도입하면서 중요하게 생각한 점과 느낀점을 정리한 내용입니다. 보편적인 CI/CD 구축 및 운영하시는 분들에게 맞지 않는 구조가 될 수도 있으니 참고 부탁드립니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/00.PNG)

## 소개

줌인터넷의 서비스인프라팀은 public cloud를 효과적으로 운영하고 관리하며, 새로운 기술에 대해 연구하고 활용할 수 있도록 노력을 기울이는 부서입니다. 새롭게 개편된 모바일줌은 public cloud에서 운영되고 있으며 product(서비스)와 pre-product(QA)을 분리하여 접근성 및 배포 방식을 개선하였고 이에 따라 서비스 품질 향상을 기대하고 있습니다.


## 1. 도입 배경

기존 IDC(On-premise)에서 개발 및 운영을 해오던 개발자들은 개발부터 배포까지 많은 부분을 담당하고 있었고 인프라 엔지니어들 또한 배포에 적지 않은 리소스를 소모하였습니다. AWS에서 개발자들이 쉽게 개발하고 운영할 수 있도록 많은 부분을 개선하려고 노력하고 있지만, IDC와 환경이 다르다 보니 문제가 항상 따랐습니다. SaaS나 PaaS 서비스는 편리할지 몰라도 IaaS 서비스는 IDC와 환경이 달라 수작업이 더 많았고 저희 입맛에 맞게 꾸미기가 어려웠습니다. 게다가 보안도 겸비해야 하다 보니 접근 방식부터 서비스를 올리기까지 많은 번거로운 점이 있었죠.

이에 저희는 '개발자가 개발에 집중할 수 있도록 AWS에서 제공하는 관리형 CI/CD 서비스로 인프라를 제공하면 어떨까'로 시작하여 지금의 CD를 구성하게 되었습니다. 개발자들은 개발만 하여 빌드된 파일을 업로드만 하고 나머지는 AWS 서비스로 모든 것을 처리하도록 말입니다.

이 계획을 실행하기에 앞서 저희가 잡은 목표는 다음과 같습니다. 아주 편하고 쾌적한 운영 환경을 가질 수 있지 않겠냐는 기대감과 함께..

- **목 표**
 1. 개발자는 개발만
 2. 기획자 및 운영자들이 서비스에 준한 QA를 할 수 있는 환경 구축
 3. 배포 시 발생하는 불필요한 운영 리소스 감소
 4. 보안 강화
이제 저희가 현재 사용하고 있는 구조를 들여다볼까요?

## 2. 아키텍처

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/01.PNG)

기존 모바일 줌은 web server의 reverse proxy 기능을 사용하여 1대의 서버 내부에서 product과 pre-product을 나누어 pre-product에 선 배포 후 product로 전환하는 배포 방식을 사용하였습니다. 그러기 위해 한 서버에 2개 이상의 application이 구동되었고, 관리를 위한 설정 파일이 다수 필요하였습니다. 또한 무정지 배포를 진행하기위해 웹서버 config를 직접 수정할 수밖에 없는 부분이 있었습니다. 그러다보니....

- **문제점**
 1. 1대의 서버에 2개의 application을 실행해야 하므로 memory 낭비
 2. 보안강화를 위해 product 서버의 접근을 차단할 수가 없는 문제 (pre-product 접근 시 product 또한 접근이 가능)
 3. 배포작업마다 서버 config 수정이 필요 (auto scaling의 어려움)

이러한 문제를 해결하고자 다음과 같이 구조를 변경하였습니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/02.PNG)

product 장비와 pre-product 장비를 독립적으로 구성하였기 때문에 product 접근 제한이 가능해졌으며, 배포하지 않을 때에는 pre-product을 언제든 종료하여 비용을 절약할 수 있었습니다. 또한 QA 진행 시 product에는 전혀 영향을 끼치지 않고 테스트할 수 있었습니다.<br><br>

## 3. 배포자동화는 어떻게?

잠시나마 배포 과정을 설명하기에 앞서 AWS 서비스를 간단히 설명해 드리자면..

 - **code pipeline**<br>
 빠르고 안정적인 애플리케이션 및 인프라 업데이트를 위해 배포 파이프라인을 구축하고 자동화가 가능하도록 지원을 해주는 AWS의 완전관리형 CD 서비스, 사용자가 정의한 모델을 기반으로 소스, 빌드, 배포 단계를 지원하며 플러그인을 지원하여 다른 3rd party 도구들과 통합 가능.
 - **code deploy**<br>
 AWS 컴퓨팅 서비스 및 IDC 서버까지 배포를 지원하는 완전관리형 배포 서비스, 애플리케이션을 배포하는 동안에 트래픽을 제어하고 스크립트 작업을 지원하여 인적과실을 줄이고 장애 예방 가능.

위 서비스들은 AWS 내에서 아주 유용하고 장점이 많은 서비스로 많은 사용자가 배포 자동화를 위해 사용하고 있습니다. 이를 활용하고자 다음과 같이 각 서비스를 배치하여 구성도를 그려보았습니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/03.PNG)

구성도도 완성되었겠다 하나씩 해보려고 문서를 보자마자 각 단계별로 문제점을 찾게됩니다.

- **source 단계**
    - gitlab 연동 미지원 (webhook을 통한 개발 필요)
    - 외부 소스코드 저장소(AWS code commit) 사용 시 보안 및 관리 문제

개발자가 소스코드 업로드 시 자동으로 pipline이 시작되게끔 이벤트를 발생해야 하는데 gitlab 플러그인을 지원하지 않아 추가로 개발이 필요했습니다. 이를 해결하기 위해 AWS code commit이라는 대체 서비스가 있었으나 사내 gitlab과 code commit을 이중으로 관리하는 비효율적인 문제와 보안 문제도 무시하지 못했죠.

- **build 단계**
    - EC2 내부에 설치된 Jenkins나 AWS code build만 사용 가능, 따라서 IDC 내부에 위치한 Jenkins 사용 불가

각 팀별로 Jekins를 관리하고 있었기 때문에 AWS의 code build의 사용이나, EC2에서 jenkins를 추가로 운영하거나 이전하기가 어려웠습니다. 내부 repository도 호출해야 됐었고 보안적인 부분도 추가로 관리가 필요했기 어쩔 수 없이 구성 변경이 필요했습니다.

- **deploy 단계**
    - code deploy의 blue/green 배포 사용 시 배포 진행 중 세밀한 traffic 흐름 제어의 어려움, 이에 따른 신속한 배포의 어려움

AWS 자체적으로 장애를 방지하기 위해 code deploy가 ELB를 제어를 전담합니다. 다만 이 과정에서 트래픽의 처리 과정을 육안으로 식별하기 어려웠으며, code deploy의 내부 처리 과정에 의해 배포시간이 결정되므로 신속한 배포가 어려웠습니다. 이는 ELB(loadbalancer) 앞단에 CloudFront(CDN)을 이용하다 보니 배포 상태에 따라 문제를 일으키는 요인이 있었으며, 아직 code deploy의 제어에 있어 미숙한 요소들도 있었으므로 간단하게 처리할 필요가 있었습니다.

위의 문제점을 고려하여 다음과 같이 구조를 변경하였습니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/04.PNG)

그랬는데..!? 해결해야 할 부분이 또 생겨납니다.

- **문제점 추가**
 1. 신규로 생성되어 동적으로 변하는 private IP를 사용하는 EC2 접속 처리?
 2. product와 pre-product 이 전환될 때 target group 등록과 ELB내 listener rule(라우팅) 처리는 어떻게 할 것인지?
 3. 배포가 다 된 EC2는 어떻게 처리할 것인지?
 4. 각각의 배포를 처리할 Lambda 함수(batch job)가 매번 늘어날텐데 어떻게 관리할 것인지?
 5. ETC..

가정을 해보면 한 번의 배포당 무려 4개의 lambda 함수가 필요했고 배포 작업이 추가될 때마다 4배수의 lambda 함수를 수정하고 생성해야 했습니다. 또한 개발자들이 동적으로 변하는 private IP를 가진 EC2에 배포된 것을 EC2에 접근하여 확인할 때마다 IP를 확인해야 하는 수고가 있었고, ELB에서 listener rule은 1개의 rule만 처리할 수 있었기에 수작업으로는 도저히 실시간으로 처리할 수 없는 부분이 많이 생겨났습니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/05.PNG)

수많은 고민 끝에 단계당 1개, 총 4개의 lambda 함수로 모든 파이프라인을 처리할 수 있도록 작성하여 관리하는 부분을 최대한 줄였으며, CloudWatch(모니터링 서비스) Event rule을 통해 각 단계의 완료 상태를 모니터링 하고 SNS를 통해 개발자에게 배포 완료 알림을 주도록 했습니다. 또한 route53을 통해 private zone을 구성하여 각 개발자가 domain을 통해 EC2에 접근할 수 있도록 처리하였으며, code pipeline의 수동 승인 항목을 탑재하여 배포가 완료된 EC2는 삭제 처리하고 문제 발생 시 바로 롤백할 수 있도록 처리하였습니다.

실제 저희 서비스에 사용되는 code pipeline의 단계입니다.

- source
![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/06.PNG)
- deploy
![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/07.PNG)
- product release
![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/08.PNG)

## 4. 도입시 가장 공들였던 부분은?

AWS 기반 CD 도입 시 가장 공들였던 부분은 표준화에 있었습니다. 하나의 서비스가 몇 개의 프로젝트로 이루어지고 하나의 프로젝트 내에 수많은 컴포넌트가 자리할 텐데 이 모두를 신경쓰는 것이 어려웠습니다. 특히 한번 정하면 변경이 어려운 항목(S3 bucket, ALB, target group, lambda 등)이 많았기 때문에 어떤 서비스에 CD를 도입하더라도 사용할 수 있게끔 만드는 것이 가장 어려웠고 많은 시간을 투자했습니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/09.PNG) <center>대부분의 엔지니어들의 고민거리인 네이밍. (사진=JTBC 마녀사냥 99회 캡처)</center>

앞서 말했지만 한번 정하면 변경이 어려운 항목이 많았기에 고심 끝에 활용한 것이 바로 tag입니다. Tag는 언제든 자유롭게 변경이 가능하며, 이를 통해 비용계산도 쉽게 할 수 있을뿐더러 원하는 리소스를 필요한 만큼 뽑아서 쓸 수 있기 때문입니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/10.PNG)

위의 tag를 AWS SDK와 접합하여 S3의 object 파일 선택, 자동으로 생성되는 instance의 name tag, code deploy의 deployment group 등 많은 부분에 활용할 수 있습니다. 단 주의해야 할 점은 tag 기반으로 resource를 검색할 시 pattern 추가가 필요한데 원하는 포맷으로 추출하기가 까다로우니 API를 여러 번 호출해야 할 수도 있습니다. (저희 기준)

두번째로 lambda 함수를 통합하는데 있어서 쓸모가 있었던 기능 중 하나가 바로 environment variables입니다. 이 기능을 활용하여 각 서비스에 맞는 환경 변수를 선언해두고 불러와서 사용할 수 있었습니다.

![](/images/portal/post/2019-03-19-ZUM-deploy-on-AWS/11.PNG)
* lambda_handler.py

```python
...
string_dic = os.environ[serviceRole]
_dic = ast.literal_eval(string_dic)

_list = []
ec2_subnet_list = eval(_dic['SUBNET'])
ec2_ami = _dic['AMI']
ec2_type = _dic['INSTANCE_TYPE']
ec2_sg = _dic['SG']
ec2_eip = _dic['EIP']
...
```

사실 코드안에 따로 설정을 첨부해도 됩니다만 관리도 힘들어지는 것 같아 이 기능을 사용했습니다. key, value로 원하는 값을 설정할 수 있으며, lambda 내에서도 다음과 같이 기술할 경우 편하게 불러와서 사용할 수 있습니다.<br><br>

## 5. 마치며

현재 구성된 CD 파이프라인은 아주 간단하게 구성되었으며, 앞으로 추가 기능(ex. AutoScalingGroup, CloudFormation template 등)을 도입하여 더 편리하고 효율적인 구조로 변경이 이루어질 예정입니다.

퍼블릭 클라우드 서비스라고 해서 우리 입맛에 맞게 모든 것을 제공해 주진 않으며, 대부분 사용자가 편하다 해도 첫 사용자들은 구성하기는 어렵습니다. 예시도 잘 들어주고, 사용자도 많고, 이것만큼 좋은 도구는 없다고 AWS 측은 말하지만 서로 다른 환경에 필요한 기술지원이 어려운 부분도 있고, 이를 해결하기 위해 여러 방법을 사용하다 보니 문제가 있을 수밖에 없습니다. 그만큼 클라우드 환경에 맞게 인프라도 바뀌어야 하며 정책 및 인식 또한 개선되어야 한다고 생각합니다. 

여러분! 첫 도입이 어렵긴 하지만 한번 구축해둔 만큼 안정성이 높아지고 기존에 해오던 수작업들이 자동화되며 간편하고 업무 생산성이 높아지니 도전해 보시는 건 어떤가요? 구축하는 방법에는 어떠한 정답도 없습니다. 우리 회사에서 우리 서비스에 맞게 인프라를 사용하는데, 가장 편하고 안전하며 관리에 일관성을 유지하는 것이 정답이라고 생각합니다.

감사합니다.


