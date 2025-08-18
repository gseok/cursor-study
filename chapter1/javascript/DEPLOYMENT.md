# 🚀 무료 Node.js 서버 배포 가이드

틱택토 멀티플레이어 서버를 무료로 배포할 수 있는 플랫폼들과 배포 방법을 안내합니다.

## 🏆 추천 순위

### 1. **Railway** ⭐⭐⭐⭐⭐ (최고 추천)
**장점:**
- WebSocket 완벽 지원
- 무료 플랜: $5 크레딧/월 (충분함)
- 자동 HTTPS/WSS 설정
- 간단한 배포 과정
- 실시간 로그 확인
- 커스텀 도메인 지원

**무료 한도:**
- $5 크레딧/월 (약 500시간 실행)
- 512MB RAM, 1GB 디스크
- 무제한 대역폭

### 2. **Render** ⭐⭐⭐⭐
**장점:**
- WebSocket 지원
- 무료 플랜 제공
- 자동 SSL 인증서
- GitHub 연동 자동 배포

**단점:**
- 30분 비활성 시 슬립 모드
- 재시작 시 약간의 지연

### 3. **Fly.io** ⭐⭐⭐⭐
**장점:**
- 무료 플랜: 3개 앱까지
- WebSocket 지원
- 전 세계 엣지 배포
- Docker 기반

**무료 한도:**
- 3개 앱, 256MB RAM
- 3GB 데이터 전송/월

### 4. **Glitch** ⭐⭐⭐
**장점:**
- 매우 간단한 배포
- 실시간 코드 편집
- 무료 플랜

**단점:**
- 5분 비활성 시 슬립
- WebSocket 제한적 지원

---

## 🚀 Railway 배포 가이드 (추천)

### 1단계: 서버 코드 준비

먼저 서버 코드를 Railway에 맞게 수정하겠습니다.

```javascript
// server/server.js 수정 필요 부분
const PORT = process.env.PORT || 8080;

// Railway에서는 0.0.0.0으로 바인딩 필요
server.listen(PORT, '0.0.0.0', () => {
  console.log(`🎮 틱택토 멀티플레이어 서버가 포트 ${PORT}에서 실행 중입니다!`);
  console.log(`WebSocket 서버: ${process.env.RAILWAY_STATIC_URL ? 'wss://' + process.env.RAILWAY_STATIC_URL : 'ws://localhost:' + PORT}`);
});
```

### 2단계: Railway 배포

1. **Railway 계정 생성**
   - [railway.app](https://railway.app) 접속
   - GitHub 계정으로 로그인

2. **새 프로젝트 생성**
   ```bash
   # GitHub에 서버 코드 푸시 후
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 해당 레포지토리 선택
   ```

3. **환경 설정**
   - 자동으로 Node.js 감지
   - `package.json`의 `start` 스크립트 실행

4. **도메인 확인**
   - 배포 완료 후 Railway 도메인 제공
   - 예: `your-app.up.railway.app`

### 3단계: 클라이언트 설정 업데이트

```javascript
// src/hooks/useWebSocket.js 수정
const connect = useCallback((playerName) => {
  // ... 기존 코드
  
  // 프로덕션 WebSocket URL 설정
  const wsUrl = process.env.NODE_ENV === 'production' 
    ? 'wss://your-app.up.railway.app'  // Railway 도메인으로 변경
    : 'ws://localhost:8080';
    
  ws.current = new WebSocket(wsUrl);
  // ... 나머지 코드
}, []);
```

---

## 🔧 Render 배포 가이드

### 1단계: Render 계정 생성
- [render.com](https://render.com) 접속
- GitHub 연동

### 2단계: Web Service 생성
1. "New +" → "Web Service" 선택
2. GitHub 레포지토리 연결
3. 설정:
   ```
   Name: tictactoe-server
   Environment: Node
   Build Command: npm install
   Start Command: npm start
   ```

### 3단계: 환경 변수 설정 (선택사항)
```
NODE_ENV=production
```

---

## ⚡ Fly.io 배포 가이드

### 1단계: Fly CLI 설치
```bash
# macOS
brew install flyctl

# 다른 OS는 https://fly.io/docs/getting-started/installing-flyctl/
```

### 2단계: 로그인 및 앱 생성
```bash
# 로그인
flyctl auth login

# 앱 생성
flyctl apps create tictactoe-server
```

### 3단계: Dockerfile 생성
```dockerfile
# server/Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8080
CMD ["npm", "start"]
```

### 4단계: fly.toml 설정
```toml
# server/fly.toml
app = "tictactoe-server"

[build]
  dockerfile = "Dockerfile"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  
  [[services.ports]]
    port = 80
    handlers = ["http"]
  
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

### 5단계: 배포
```bash
flyctl deploy
```

---

## 🌐 클라이언트 배포 (Netlify/Vercel)

서버 배포 후 클라이언트도 배포하는 것을 추천합니다.

### Netlify 배포
1. [netlify.com](https://netlify.com)에서 GitHub 연결
2. React 앱 루트 디렉토리 선택
3. Build 설정:
   ```
   Build command: npm run build
   Publish directory: build
   ```

### 환경 변수 설정
```
REACT_APP_WS_URL=wss://your-server-domain.com
```

---

## 📋 배포 후 체크리스트

### ✅ 서버 확인사항
- [ ] WebSocket 연결 테스트
- [ ] HTTPS/WSS 프로토콜 확인
- [ ] 로그 모니터링 설정
- [ ] 에러 처리 확인

### ✅ 클라이언트 확인사항
- [ ] 프로덕션 WebSocket URL 설정
- [ ] 빌드 및 배포 성공
- [ ] 크로스 오리진 정책 확인
- [ ] 모바일 브라우저 테스트

### ✅ 전체 시스템 테스트
- [ ] 멀티플레이어 매칭 테스트
- [ ] 실시간 게임 플레이 테스트
- [ ] 연결 끊김/재연결 테스트
- [ ] 다양한 브라우저에서 테스트

---

## 🔧 프로덕션 최적화 팁

### 1. 서버 최적화
```javascript
// server/server.js에 추가
// CORS 설정
const allowedOrigins = [
  'https://your-client-domain.netlify.app',
  'http://localhost:3000' // 개발용
];

// 헬스체크 엔드포인트
server.on('request', (req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('OK');
  }
});

// 연결 제한
const MAX_CONNECTIONS = 100;
let connectionCount = 0;

wss.on('connection', (ws) => {
  connectionCount++;
  console.log(`연결 수: ${connectionCount}`);
  
  if (connectionCount > MAX_CONNECTIONS) {
    ws.close(1008, 'Server full');
    return;
  }
  
  ws.on('close', () => {
    connectionCount--;
  });
});
```

### 2. 모니터링 추가
```javascript
// 서버 통계 API
app.get('/stats', (req, res) => {
  res.json({
    connections: connectionCount,
    rooms: gameManager.rooms.size,
    players: gameManager.players.size,
    uptime: process.uptime()
  });
});
```

### 3. 환경별 설정
```javascript
// config/config.js
module.exports = {
  development: {
    port: 8080,
    wsUrl: 'ws://localhost:8080'
  },
  production: {
    port: process.env.PORT || 8080,
    wsUrl: process.env.WS_URL || 'wss://your-domain.com'
  }
};
```

---

## 💡 추천 조합

**최고의 조합 (무료):**
- **서버**: Railway (WebSocket 지원 + 안정성)
- **클라이언트**: Netlify (React 앱 + CDN)
- **모니터링**: Railway 내장 로그

**대안 조합:**
- **서버**: Render (무료 + 간단)
- **클라이언트**: Vercel (Next.js 호환)

---

## 🎯 결론

**Railway를 가장 추천**합니다! WebSocket 지원이 완벽하고, 무료 크레딧으로 충분히 테스트할 수 있으며, 배포 과정이 매우 간단합니다.

배포 후에는 실제 인터넷을 통해 친구들과 멀티플레이어 틱택토 게임을 즐길 수 있습니다! 🎮🌐
