<div align="center">
  <h1>Lingo Chat Server</h1>
</div>

- 페르소나 캐릭터와 AI 채팅 기능을 제공하는 프로젝트 입니다.
- 서버의 부하를 줄이고 실시간 처리 성능을 최적화하기 위해 Socket Server와 API Server를 분리하여 개발되었습니다.
- 안정적인 서비스 운영을 위해 Blue-Green 배포 방식을 적용한 인프라를 설계하였습니다. 이를 위해 Docker 기반의 인프라를 사용하여 높은 가용성과 무중단 배포를 보장할 수 있도록 했습니다.

<br>

## 프로젝트 사용기술
**[BackEnd]** Nest.JS, Typescript, PostgreSQL, TypeORM, Redis, socket.io

**[DevOps]** GCP, Nginx, Docker, Docker compose, Ubuntu, Git, Github Actions

<br>

## 프로젝트 아키텍처
<img width="917" alt="스크린샷 2024-11-05 오후 6 18 14" src="https://github.com/user-attachments/assets/3a0fb7d7-8e40-4e33-99b1-8591feec7273">


<br>

## Technical Issue
[반복되는 응답처리를 AOP로 분리하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%971-%EB%B0%98%EB%B3%B5%EB%90%98%EB%8A%94-%EC%9D%91%EB%8B%B5%EC%B2%98%EB%A6%AC%EB%A5%BC-AOP%EB%A1%9C-%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0)

[JWT 인증에서의 중복 로그인 방지하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%972-JWT-%EC%9D%B8%EC%A6%9D%EC%97%90%EC%84%9C%EC%9D%98-%EC%A4%91%EB%B3%B5-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EB%B0%A9%EC%A7%80%ED%95%98%EA%B8%B0)
  
[웹소켓으로 실시간 챗봇 구현하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%973-%EC%9B%B9%EC%86%8C%EC%BC%93%EC%9C%BC%EB%A1%9C-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%B1%97%EB%B4%87-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0)

[채팅 로그 읽기/쓰기 전략](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%974-%EC%B1%84%ED%8C%85-%EB%A1%9C%EA%B7%B8-%EC%9D%BD%EA%B8%B0%EC%93%B0%EA%B8%B0-%EC%A0%84%EB%9E%B5)

[Github Actions를 이용하여 CI/CD 구축하기](https://velog.io/@showui96/%EB%A7%81%EA%B3%A0%EC%B1%975-Github-Action%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-CICD-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0)

<br>

## 프로젝트 주요 기능 및 중점 사항
- 중복 로그인 방지 프로세스
- 클라이언트 <-> API 서버 <-> AI 서버 간의 실시간 통신 및 채팅 기능
- AI 서버와 효율적인 통신을 위한 소켓 서버 구축
- 신규 채팅방 정보의 실시간 업데이트
- 효율적인 채팅 로그의 읽기/쓰기
- 메시지의 과부하 발생 방지를 위한 메시지 큐를 이용한 대기열 관리
- 서버의 확장성
- Github Actions를 사용하여 CI/CD 파이프라인 구축
- shell 스크립트를 사용한 CD 구현
- 무중단 서비스를 위한 블루 그린 배포 적용
- Nginx의 Reversed-Proxy를 이용한 트래픽 처리

<br>

## ERD
<img width="1052" alt="스크린샷 2024-11-05 오후 6 04 11" src="https://github.com/user-attachments/assets/36c5a7b8-47c8-494a-b138-f2f9942b9822">

<br>
<br>

### 프로젝트 Front/Socket Server Repository
https://github.com/lingo-chat/lingo-chat

https://github.com/haeseung123/lingo-chat-socket-server
