# React 틱택토 게임

Python tkinter 버전을 기반으로 React로 구현한 틱택토 게임입니다.

## 🎮 주요 기능

### ✨ 게임 기능
- **3가지 게임 모드**
  - 플레이어 vs 플레이어
  - 플레이어 vs AI (쉬움) - 랜덤 전략
  - 플레이어 vs AI (어려움) - 스마트 전략
- **실시간 점수 추적**
- **승리 패턴 하이라이트**
- **게임 상태 표시**

### 🎨 UI/UX 특징
- **반응형 디자인** - 모바일, 태블릿, 데스크톱 지원
- **부드러운 애니메이션** - 호버, 클릭, 승리 효과
- **직관적인 인터페이스** - 명확한 버튼과 상태 표시
- **접근성 고려** - 키보드 네비게이션 지원

## 🚀 설치 및 실행

### 1. 프로젝트 설정
```bash
# Create React App으로 새 프로젝트 생성
npx create-react-app react-tictactoe
cd react-tictactoe

# 또는 기존 프로젝트에 파일 복사
```

### 2. 파일 구조
```
src/
├── App.js              # 메인 앱 컴포넌트
├── App.css             # 앱 전역 스타일
├── TicTacToe.jsx       # 틱택토 게임 컴포넌트
├── TicTacToe.css       # 게임 스타일
└── index.js            # React 진입점
```

### 3. 실행
```bash
npm install
npm start
```

## 🔧 컴포넌트 구조

### TicTacToe 컴포넌트
```jsx
const TicTacToe = () => {
  // 상태 관리
  const [board, setBoard] = useState(Array(9).fill(' '));
  const [currentPlayer, setCurrentPlayer] = useState('X');
  const [gameOver, setGameOver] = useState(false);
  const [gameMode, setGameMode] = useState(1);
  const [score, setScore] = useState({ X: 0, O: 0, draws: 0 });

  // 게임 로직
  const checkWinner = useCallback((boardState) => { ... });
  const handleCellClick = useCallback((position) => { ... });
  const handleAiMove = useCallback(async (boardState, player) => { ... });

  return (
    <div className="tictactoe-container">
      {/* UI 렌더링 */}
    </div>
  );
};
```

## 🎯 핵심 기능 구현

### 1. 게임 상태 관리
```jsx
// React Hooks를 사용한 상태 관리
const [board, setBoard] = useState(Array(9).fill(' '));
const [currentPlayer, setCurrentPlayer] = useState('X');
const [gameOver, setGameOver] = useState(false);
```

### 2. AI 구현
```jsx
// 스마트 AI 로직
const getSmartMove = useCallback((boardState) => {
  // 1. 승리 가능한 수 찾기
  // 2. 상대방 승리 차단
  // 3. 중앙/코너 선택
  // 4. 랜덤 선택
}, []);
```

### 3. 비동기 AI 처리
```jsx
const handleAiMove = useCallback(async (boardState, player) => {
  setAiThinking(true);
  await new Promise(resolve => setTimeout(resolve, 800));
  // AI 로직 실행
  setAiThinking(false);
}, []);
```

## 🎨 스타일링 특징

### CSS Grid 레이아웃
```css
.game-board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
```

### 반응형 디자인
```css
@media (max-width: 480px) {
  .cell {
    width: 70px;
    height: 70px;
    font-size: 2rem;
  }
}
```

### 애니메이션 효과
```css
.cell-winner {
  animation: pulse 0.6s ease-in-out infinite alternate;
}

@keyframes pulse {
  from { transform: scale(1); }
  to { transform: scale(1.1); }
}
```

## 🔄 Python 버전과의 차이점

| 특징 | Python (tkinter) | React |
|------|------------------|-------|
| **상태 관리** | 클래스 인스턴스 변수 | React Hooks (useState) |
| **UI 업데이트** | 직접 위젯 조작 | 선언적 렌더링 |
| **이벤트 처리** | 콜백 함수 | JSX 이벤트 핸들러 |
| **스타일링** | tkinter 스타일 옵션 | CSS + 클래스명 |
| **반응형** | 고정 크기 | CSS 미디어 쿼리 |
| **애니메이션** | 제한적 | CSS 애니메이션 |

## 🚀 확장 가능성

### 추가 가능한 기능
1. **온라인 멀티플레이어** - Socket.io 연동
2. **게임 기록** - localStorage 또는 데이터베이스
3. **테마 시스템** - 다크모드, 커스텀 테마
4. **사운드 효과** - Web Audio API
5. **터치 제스처** - 모바일 최적화
6. **AI 난이도 조절** - 더 정교한 알고리즘

### 성능 최적화
- `React.memo`로 불필요한 리렌더링 방지
- `useCallback`으로 함수 메모이제이션
- 가상화된 대용량 게임 보드 (확장 시)

## 📱 모바일 지원

- **터치 친화적** 버튼 크기
- **반응형 레이아웃** 
- **세로/가로 모드** 지원
- **PWA 가능** - 앱처럼 설치 가능

이제 React로 구현된 완전한 틱택토 게임을 즐길 수 있습니다! 🎉
