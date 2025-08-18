# 🚀 단계별 배포 가이드

틱택토 멀티플레이어 게임을 실제로 배포하는 단계별 가이드입니다.

## 🎯 목표
- WebSocket 서버를 Railway에 배포
- React 클라이언트를 Netlify에 배포
- 실제 인터넷을 통한 멀티플레이어 게임 구현

---

## 📋 사전 준비

### 1. GitHub 레포지토리 생성
```bash
# 프로젝트를 GitHub에 업로드
git init
git add .
git commit -m "Initial commit: Multiplayer TicTacToe"
git remote add origin https://github.com/your-username/tictactoe-multiplayer.git
git push -u origin main
```

### 2. 필요한 계정
- [Railway.app](https://railway.app) - 서버 배포용
- [Netlify.com](https://netlify.com) - 클라이언트 배포용
- GitHub 계정 (이미 있음)

---

## 🚂 1단계: Railway 서버 배포

### 1.1 Railway 계정 생성
1. [railway.app](https://railway.app) 접속
2. "Login with GitHub" 클릭
3. GitHub 계정으로 로그인

### 1.2 새 프로젝트 생성
1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 틱택토 레포지토리 선택
4. 서버 폴더 경로 설정: `server/`

### 1.3 환경 변수 설정
Railway 프로젝트 설정에서:
```
NODE_ENV=production
```

### 1.4 배포 확인
- 자동으로 배포가 시작됩니다
- 로그에서 "🎮 틱택토 멀티플레이어 서버가 실행 중입니다!" 확인
- Railway 도메인 확인 (예: `your-app.up.railway.app`)

### 1.5 테스트
브라우저에서 `https://your-app.up.railway.app/health` 접속하여 서버 상태 확인

---

## 🌐 2단계: Netlify 클라이언트 배포

### 2.1 환경 변수 설정
클라이언트 코드에서 WebSocket URL 업데이트:

```javascript
// src/hooks/useWebSocket.js 수정
const wsUrl = process.env.REACT_APP_WS_URL || 
             (process.env.NODE_ENV === 'production' 
              ? 'wss://your-actual-railway-domain.up.railway.app'  // 실제 도메인으로 변경
              : 'ws://localhost:8080');
```

### 2.2 GitHub에 변경사항 푸시
```bash
git add .
git commit -m "Update WebSocket URL for production"
git push
```

### 2.3 Netlify 배포
1. [netlify.com](https://netlify.com) 접속
2. "Add new site" → "Import an existing project"
3. GitHub 연결 후 레포지토리 선택
4. 빌드 설정:
   ```
   Base directory: (비워둠)
   Build command: npm run build
   Publish directory: build
   ```

### 2.4 환경 변수 설정 (Netlify)
Site settings → Environment variables:
```
REACT_APP_WS_URL=wss://cursor-study-production-4850.up.railway.app
```

### 2.5 재배포
환경 변수 설정 후 "Trigger deploy" 클릭

---

## 🧪 3단계: 전체 시스템 테스트

### 3.1 기본 연결 테스트
1. Netlify 도메인 접속 (예: `https://tictacto-gseok.netlify.app/`)
2. 시작 화면에서 "온라인 멀티플레이어" 선택
3. 플레이어 이름 입력 후 "게임 참여" 클릭
4. "상대방을 찾고 있습니다..." 메시지 확인

### 3.2 멀티플레이어 테스트
1. **두 개의 브라우저/탭**에서 동일한 URL 접속
2. 각각 다른 플레이어 이름으로 게임 참여
3. 자동 매칭 확인
4. 실시간 게임 플레이 테스트

### 3.3 모바일 테스트
- 스마트폰 브라우저에서 접속 테스트
- 반응형 디자인 확인

---

## 🔧 4단계: 문제 해결

### 4.1 서버 로그 확인
Railway 대시보드 → Deployments → View Logs

### 4.2 클라이언트 오류 확인
브라우저 개발자 도구 → Console 탭

### 4.3 일반적인 문제들

#### WebSocket 연결 실패
```javascript
// 해결: HTTPS에서는 WSS 사용 필수
❌ ws://your-domain.com
✅ wss://your-domain.com
```

#### CORS 오류
서버에 CORS 헤더 추가:
```javascript
// server.js에 추가
server.on('request', (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  // ... 나머지 코드
});
```

#### 환경 변수 미적용
- Railway: 환경 변수 설정 후 재배포 필요
- Netlify: 환경 변수 설정 후 "Clear cache and deploy site"

---

## 📊 5단계: 모니터링 및 최적화

### 5.1 서버 모니터링
Railway 대시보드에서 확인 가능:
- CPU/메모리 사용량
- 네트워크 트래픽
- 응답 시간

### 5.2 사용량 확인
```bash
# Railway 무료 크레딧 확인
- 대시보드에서 Usage 탭 확인
- $5/월 크레딧 소모량 모니터링
```

### 5.3 성능 최적화
```javascript
// 서버에 연결 제한 추가
const MAX_CONNECTIONS = 50; // Railway 무료 플랜 고려

wss.on('connection', (ws) => {
  if (wss.clients.size > MAX_CONNECTIONS) {
    ws.close(1008, 'Server capacity exceeded');
    return;
  }
  // ... 나머지 코드
});
```

---

## 🎉 완료!

### ✅ 배포 완료 체크리스트
- [ ] Railway 서버 정상 실행
- [ ] Netlify 클라이언트 배포 완료
- [ ] WebSocket 연결 성공
- [ ] 멀티플레이어 매칭 테스트 통과
- [ ] 실시간 게임 플레이 테스트 통과
- [ ] 모바일 브라우저 테스트 통과

### 🌟 최종 결과
- **서버**: `https://your-app.up.railway.app`
- **클라이언트**: `https://your-app.netlify.app`
- **게임**: 전 세계 어디서든 친구들과 실시간 멀티플레이어 틱택토!

### 📱 공유하기
친구들에게 Netlify URL을 공유하여 함께 게임을 즐겨보세요!

```
🎮 함께 틱택토 게임 해요!
👉 https://your-app.netlify.app

3x3, 4x4 보드 지원
실시간 멀티플레이어
모바일/데스크톱 모두 지원
```

---

## 💡 추가 개선 아이디어

### 단기 개선
- [ ] 플레이어 아바타 추가
- [ ] 채팅 기능
- [ ] 게임 통계 저장

### 장기 개선
- [ ] 토너먼트 모드
- [ ] 랭킹 시스템
- [ ] 소셜 로그인 (Google, Facebook)
- [ ] PWA (Progressive Web App) 변환

**축하합니다! 실제 인터넷에서 동작하는 멀티플레이어 게임을 만들었습니다!** 🎊🎮
