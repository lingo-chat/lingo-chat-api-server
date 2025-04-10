<div align="center">
  <h1>Lingo Chat Server</h1>
</div>

-   페르소나 캐릭터와 AI 채팅 기능을 제공하는 프로젝트 입니다.
-   서버의 부하를 줄이고 실시간 처리 성능을 최적화하기 위해 Socket Server와 API Server를 분리하여 개발되었습니다.

<br>

## 프로젝트 사용기술

**[BackEnd]** Nest.JS, Typescript, PostgreSQL, TypeORM, Redis, socket.io

**[DevOps]** GCP, GKE, Nginx, Docker, Docker compose, Kubernetes, Ubuntu, Git, Github Actions, Argo, Vault

<br>

## 프로젝트 아키텍처

<img width="782" alt="스크린샷 2025-03-04 오후 2 56 12" src="https://github.com/user-attachments/assets/0185c63f-a993-4a8d-af21-b37f27e430db" />

프로젝트 초기의 도커 기반의 단일 서버 환경에서 GCP의 GKE(Google Kubernetes Engine)를 활용한 쿠버네티스 기반 아키텍처로 전환하여 운영 효율성과 확장성을 보장하도록 개선되었습니다.

-   자동 복구(Self-Healing) 기능을 통해 컨테이너의 비정상 동작을 자동으로 감지하고 재시작함으로써 가용성 증가
-   Helm Chart를 도입하여 애플리케이션 배포 및 구성을 템플릿화하고 서비스 버전 관리를 체계화하여 일관된 배포 및 롤백이 가능하도록 구성

<br>

### CI/CD 파이프라인

<img width="791" alt="스크린샷 2025-04-10 오전 11 51 44" src="https://github.com/user-attachments/assets/969f9c6e-5994-461f-9811-deb89eff7afe" />

초기에는 Github Actions를 활용한 단순한 CI/CD 파이프라인을 운영했으나 쿠버네티스 환경에 적합한 구조로 발전시키기 위해 GitOps 방식의 파이프라인으로 전환되었습니다.

Github Actions와 Argo CD를 조합하여 빌드부터 배포까지의 전 과정을 자동화하였으며 Git 리포지토리의 장태만으로 현재 클러스터의 구성을 추적하고 관리할 수 있습니다.

```
1. 소스 코드 푸시 및 태깅
    - Git-Flow 브랜치 전략을 바탕으로 한 버전 관리
    - 신규 릴리스를 위한 태그(ex: v1.0.0) 생성 및 푸시

2. Github Actions에서 CI 수행
	  - Docker 이미지 빌드 및 Docker Hub 푸시
    - Helm Chart 업데이트 (nginx, api, socket 각각의 이미지 버전 변경)

3. Argo CD + Argo Image Updater를 통한 CD 수행
	  - Lingo Chat Helm Chart Repository의 변경을 감지하여 자동으로 클러스터에 배포
    - Argo Image Updater가 이미지 태그 변경을 감지하고 Argo CD를 통해 최신 상태로 자동 업데이트
```

<br>

## 기술적 이슈와 해결 과정

### 확장성 높은 아키텍처로 전환하는 과정

-   [GKE 기반 쿠버네티스 아키텍처로 전환](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%97-7-%ED%99%95%EC%9E%A5%EC%84%B1-%EB%86%92%EC%9D%80-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%EB%A1%9C-%EC%A0%84%ED%99%98%ED%95%98%EA%B8%B0)

    -   프로젝트 서버 구조에 대한 전반적인 설명과 기존 인프라의 한계점부터 쿠버네티스로 전환하기까지의 세부 내용이 정리되어 있습니다.

-   [링고챗 Helm Chart 구축 및 분석](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%97-8-LingoChat-Helm-Chart-%EA%B5%AC%EC%B6%95)

    -   각 서비스(api, socket, nginx)는 별도의 Helm Chart로 구성되어 있으며 Helm Chart는 전용 리포지토리에서 관리되고 배포됩니다. 구조와 구성에 대한 세부 내용이 정리되어 있습니다.

-   [GitOps 기반 CI/CD 구축하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%97-9-GitOps-%EA%B8%B0%EB%B0%98-CICD-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0)
    -   CI/CD 파이프라인은 Github Actions + Argo CD 조합으로 구성하였으며 전체 흐름 및 YAML 구성에 대해 구체적으로 서술되어 있습니다.
    -   Argo CD는 GitOps 방식으로 클러스터 내 배포를 자동화하며 Argo Image Updater를 통해 서비스 이미지 변경을 자동으로 반영합니다. 실제 App 구성과 배포 자동화 흐름이 정리되어 있습니다.

### 코드 유지보수성과 데이터 정합성을 고려한 문제 해결

-   [반복되는 응답처리를 AOP로 분리하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%971-%EB%B0%98%EB%B3%B5%EB%90%98%EB%8A%94-%EC%9D%91%EB%8B%B5%EC%B2%98%EB%A6%AC%EB%A5%BC-AOP%EB%A1%9C-%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0)
-   [JWT 인증에서의 중복 로그인 방지하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%972-JWT-%EC%9D%B8%EC%A6%9D%EC%97%90%EC%84%9C%EC%9D%98-%EC%A4%91%EB%B3%B5-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EB%B0%A9%EC%A7%80%ED%95%98%EA%B8%B0)

### 핵심 기능 개발 과정에 대한 정리

-   [웹소켓으로 실시간 챗봇 구현하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%973-%EC%9B%B9%EC%86%8C%EC%BC%93%EC%9C%BC%EB%A1%9C-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%B1%97%EB%B4%87-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0)
-   [채팅 로그 읽기 쓰기 전략](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%974-%EC%B1%84%ED%8C%85-%EB%A1%9C%EA%B7%B8-%EC%9D%BD%EA%B8%B0%EC%93%B0%EA%B8%B0-%EC%A0%84%EB%9E%B5)

<br>

## 핵심 기능

-   **AI 캐릭터와의 실시간 대화 기능**

    사용자가 선택한 AI 캐릭터와 실시간으로 대화할 수 있는 기능을 제공합니다.

-   **WebSocket을 통한 실시간 메시지 송수신**

    WebSocket을 사용하여 서버와 클라이언트 간의 실시간 메시지 송수신을 처리합니다. 소켓 서버를 통해 AI 서버와 클라이언트 간의 효율적인 통신이 가능하도록 구현했으며 AI 서버와의 빠른 데이터 전송이 가능하도록 하였습니다.

-   **중복 로그인 방지 프로세스**

    JWT 인증을 기반으로 중복 로그인을 방지하고 사용자가 여러 클라이언트에서 동시에 접속할 때 세션을 관리합니다.
    이를 통해 동일 사용자가 여러 장치에서 로그인할 때 발생할 수 있는 문제를 예방할 수 있도록 고려했습니다.

-   **메시지 큐를 활용한 대기열 관리**

    메시지 큐를 사용하여 대기열을 관리하고 메시지 과부하를 방지하도록 했습니다.
    채팅 메시지가 과도하게 몰리더라도 큐 시스템을 통해 처리 순서를 관리하며 서버 부하를 줄이고 안정적인 서비스 제공을 보장할 수 있도록 고려했습니다.

<br>

<br>

## ERD

<img width="1052" alt="스크린샷 2024-11-05 오후 6 04 11" src="https://github.com/user-attachments/assets/36c5a7b8-47c8-494a-b138-f2f9942b9822">

<br>
<br>

## 프로젝트 Repository

**[FrontEnd]** https://github.com/lingo-chat/lingo-chat

**[Socket-Server]** https://github.com/haeseung123/lingo-chat-socket-server

**[Helm Chart]** https://github.com/haeseung123/lingo-chat-helm
