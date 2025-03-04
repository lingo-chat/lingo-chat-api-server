<div align="center">
  <h1>Lingo Chat Server</h1>
</div>

-   페르소나 캐릭터와 AI 채팅 기능을 제공하는 프로젝트 입니다.
-   서버의 부하를 줄이고 실시간 처리 성능을 최적화하기 위해 Socket Server와 API Server를 분리하여 개발되었습니다.

<br>

## 프로젝트 사용기술

**[BackEnd]** Nest.JS, Typescript, PostgreSQL, TypeORM, Redis, socket.io

**[DevOps]** GCP, GKE, Nginx, Docker, Docker compose, Kubernetes, Ubuntu, Git, Github Actions, Vault

<br>

## 프로젝트 아키텍처

프로젝트의 초기 인프라는 개발과 운영 환경의 일관성을 유지하고 컨테이너화된 애플리케이션을 손쉽게 배포하고 관리할 수 있도록 도커 기반의 인프라로 구축되었습니다. 단순히 컨테이너를 운영하는 것이 아닌 무중단 배포와 운영 자동화까지, 최선의 방안을 적용할 수 있도록 고려하였습니다.

-   Blue-Green 배포 방식을 도입하여 배포 중 발생할 수 있는 장애를 최소화하고 실시간 트래픽 전환을 통해 서비스 다운타임 없이 안전하게 배포
-   GitHub Actions를 활용한 CI/CD 파이프라인을 구축하여 코드 변경 사항이 자동으로 빌드-배포되도록 구성하여 배포 속도를 높이고 운영 부담 최소화

도커 기반의 아키텍처에서 적용할 수 있는 최선의 배포 및 운영 전략을 고려하여 적용했지만 서비스 확장성와 운영 자동화의 필요성이 커지면서 쿠버네티스 기반으로 전환하게 되었습니다.

### 전환된 인프라 아키텍처

<img width="782" alt="스크린샷 2025-03-04 오후 2 56 12" src="https://github.com/user-attachments/assets/0185c63f-a993-4a8d-af21-b37f27e430db" />

현재는 GCP의 GKE(Google Kubernetes Engine) 기반의 아키텍처로 전환하여 컨테이너 오케스트레이션과 서비스 확장성을 보장하도록 개선하였습니다.

-   기존 인프라에서는 장애 발생 시 복구를 수동으로 해야 했으나 쿠버네티스의 자동 복구(Self-Healing) 기능으로 비정상적인 컨테이너를 자동으로 감지하고 재시작할 수 있도록 개선
-   초기에는 컨테이너 개수를 수동으로 조정해야하는 한계가 있었으나 트래픽 변화에 따라 노드와 파드를 자동으로 조절할 수 있도록 고려
-   Helm 차트를 작성하여 애플리케이션 배포 및 구성을 템플릿화함으로써 버전 관리가 용이해지고 배포를 일관성 있게 수행
-   쿠버네티스의 서비스(Service)와 인그레스(Ingress) 기능을 활용하여 별도의 도구 없이 컨테이너 간 통신을 쉽게 설정

#### 진행 중인 사항

쿠버네티스 환경에 최적화된 CI/CD 워크플로우를 구성하고 있습니다.

-   Github Actions 및 ArgoCD를 활용한 GitOps 기반 배포 방식 도입

<br>

## 기술적 이슈와 해결 과정

-   확장성 높은 아키텍처로 전환하는 과정

    -   [Github Actions를 이용하여 CI/CD 구축하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%975-Github-Action%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-CICD-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0)
    -   [FrontEnd 배포 성능을 최적화하는 방법](https://velog.io/@showui96/Frontend-%EB%B0%B0%ED%8F%AC-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94-%ED%95%98%EA%B8%B0)
    -   [GKE 기반 쿠버네티스 아키텍처로 전환](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%97-7-%ED%99%95%EC%9E%A5%EC%84%B1-%EB%86%92%EC%9D%80-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%EB%A1%9C-%EC%A0%84%ED%99%98%ED%95%98%EA%B8%B0)
    -   [링고챗 Helm Chart 구축 및 분석](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%97-8-LingoChat-Helm-Chart-%EA%B5%AC%EC%B6%95)

-   코드 유지보수성과 데이터 정합성을 고려한 문제 해결

    -   [반복되는 응답처리를 AOP로 분리하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%971-%EB%B0%98%EB%B3%B5%EB%90%98%EB%8A%94-%EC%9D%91%EB%8B%B5%EC%B2%98%EB%A6%AC%EB%A5%BC-AOP%EB%A1%9C-%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0)
    -   [JWT 인증에서의 중복 로그인 방지하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%972-JWT-%EC%9D%B8%EC%A6%9D%EC%97%90%EC%84%9C%EC%9D%98-%EC%A4%91%EB%B3%B5-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EB%B0%A9%EC%A7%80%ED%95%98%EA%B8%B0)

-   핵심 기능 개발 과정에 대한 정리

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
