<div align="center">
  <h1>Lingo Chat Server</h1>
</div>

-   페르소나 캐릭터와 AI 채팅 기능을 제공하는 프로젝트 입니다.
-   서버의 부하를 줄이고 실시간 처리 성능을 최적화하기 위해 Socket Server와 API Server를 분리하여 개발되었습니다.
-   안정적인 서비스 운영을 위해 Blue-Green 배포 방식을 적용한 인프라를 설계하였습니다. 이를 위해 Docker 기반의 인프라를 사용하여 높은 가용성과 무중단 배포를 보장할 수 있도록 했습니다.

### 진행 중인 작업 / 예정 작업

Kubernetes 클러스터로의 마이그레이션은 현재의 아키텍처보다 애플리케이션의 확장성, 고가용성을 향상시켜 고도화하고
배포 속도와 자동화를 그에 맞게 개선하여 개발 및 운영 효율성을 극대화하기 위해 CI/CD 파이프라인 최적화 작업을 진행하고 있습니다.

-   **Kubernetes 클러스터로 마이그레이션** 진행 중
-   Github Actions CI, Helm Chart를 활용한 Argo CD 구축 예정

<br>

## 프로젝트 사용기술

**[BackEnd]** Nest.JS, Typescript, PostgreSQL, TypeORM, Redis, socket.io

**[DevOps]** GCP, Nginx, Docker, Docker compose, Ubuntu, Git, Github Actions

<br>

## 프로젝트 아키텍처

<img width="917" alt="스크린샷 2024-11-05 오후 6 18 14" src="https://github.com/user-attachments/assets/3a0fb7d7-8e40-4e33-99b1-8591feec7273">

### CI/CD Workflow

```
1. 소스 코드 변경사항 Push
GitHub에 소스 코드 변경사항이 푸시되면 CI 파이프라인의 트리거가 되어 GitHub Actions 워크플로우 실행

2. GitHub Actions CI 파이프라인 동작
- Docker Image Build: GitHub Actions에서 Docker 이미지 빌드
- Docker Registry Push: 빌드된 Docker 이미지를 Docker 레지스트리에 푸시
- Nginx Load Balancer Update: Nginx 설정을 자동으로 업데이트하여 새로운 Docker 이미지를 사용할 수 있도록 함

3. Nginx Load Balancer를 통한 배포
- api-deploy.sh: 배포 스크립트를 통해 Blue/Green 배포 전략을 적용하여 무중단 배포를 처리
- 신규 버전 배포 → Nginx 설정 업데이트 → 구 버전 종료
```

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

-   **클라우드 환경(GCP)에서 서버 인프라 배포 및 운영**

    Google Cloud Platform(GCP)을 활용하여 서버 인프라를 안정적으로 운영하고 프로젝트의 확장성을 고려한 인프라 설계를 적용하고 개선해 나가고 있습니다.

-   **CI/CD 및 무중단 배포 (Blue-Green 배포 적용)**

    GitHub Actions를 사용하여 CI/CD 파이프라인을 구축하고 자동화된 배포 시스템을 구현했습니다.
    Blue-Green 배포 전략을 통해 배포 과정에서 서비스 중단 없이 새로운 버전의 애플리케이션을 운영할 수 있습니다.

<br>

## Technical Issue

[반복되는 응답처리를 AOP로 분리하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%971-%EB%B0%98%EB%B3%B5%EB%90%98%EB%8A%94-%EC%9D%91%EB%8B%B5%EC%B2%98%EB%A6%AC%EB%A5%BC-AOP%EB%A1%9C-%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0)

[JWT 인증에서의 중복 로그인 방지하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%972-JWT-%EC%9D%B8%EC%A6%9D%EC%97%90%EC%84%9C%EC%9D%98-%EC%A4%91%EB%B3%B5-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EB%B0%A9%EC%A7%80%ED%95%98%EA%B8%B0)

[웹소켓으로 실시간 챗봇 구현하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%973-%EC%9B%B9%EC%86%8C%EC%BC%93%EC%9C%BC%EB%A1%9C-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%B1%97%EB%B4%87-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0)

[채팅 로그 읽기/쓰기 전략](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%974-%EC%B1%84%ED%8C%85-%EB%A1%9C%EA%B7%B8-%EC%9D%BD%EA%B8%B0%EC%93%B0%EA%B8%B0-%EC%A0%84%EB%9E%B5)

[Github Actions를 이용하여 CI/CD 구축하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%975-Github-Action%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-CICD-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0)

<br>

## ERD

<img width="1052" alt="스크린샷 2024-11-05 오후 6 04 11" src="https://github.com/user-attachments/assets/36c5a7b8-47c8-494a-b138-f2f9942b9822">

<br>
<br>

## 프로젝트 Repository

[FrontEnd] https://github.com/lingo-chat/lingo-chat

[Socket-Server] https://github.com/haeseung123/lingo-chat-socket-server

[Helm Chart] https://github.com/haeseung123/lingo-chat-helm
