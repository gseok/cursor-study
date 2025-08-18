import React, { useState, useEffect, useCallback } from 'react';
import './TicTacToe.css';

const TicTacToe = ({ boardSize = 3, gameMode = 1, onBackToMenu }) => {
  // 게임 상태
  const [board, setBoard] = useState(Array(boardSize * boardSize).fill(' '));
  const [currentPlayer, setCurrentPlayer] = useState('X');
  const [gameOver, setGameOver] = useState(false);
  const [aiThinking, setAiThinking] = useState(false);
  const [score, setScore] = useState({ X: 0, O: 0, draws: 0 });
  const [status, setStatus] = useState('게임을 시작하세요!');

  // 승리 패턴 생성 (동적으로 보드 크기에 맞춰)
  const generateWinPatterns = useCallback((size) => {
    const patterns = [];
    
    // 행 패턴
    for (let row = 0; row < size; row++) {
      const rowPattern = [];
      for (let col = 0; col < size; col++) {
        rowPattern.push(row * size + col);
      }
      patterns.push(rowPattern);
    }
    
    // 열 패턴
    for (let col = 0; col < size; col++) {
      const colPattern = [];
      for (let row = 0; row < size; row++) {
        colPattern.push(row * size + col);
      }
      patterns.push(colPattern);
    }
    
    // 주 대각선 패턴 (왼쪽 위 → 오른쪽 아래)
    const mainDiagonal = [];
    for (let i = 0; i < size; i++) {
      mainDiagonal.push(i * size + i);
    }
    patterns.push(mainDiagonal);
    
    // 부 대각선 패턴 (오른쪽 위 → 왼쪽 아래)
    const antiDiagonal = [];
    for (let i = 0; i < size; i++) {
      antiDiagonal.push(i * size + (size - 1 - i));
    }
    patterns.push(antiDiagonal);
    
    return patterns;
  }, []);

  const winPatterns = generateWinPatterns(boardSize);

  // 승자 확인
  const checkWinner = useCallback((boardState) => {
    for (const pattern of winPatterns) {
      const [a, b, c] = pattern;
      if (boardState[a] !== ' ' && 
          boardState[a] === boardState[b] && 
          boardState[b] === boardState[c]) {
        return { winner: boardState[a], pattern };
      }
    }
    return null;
  }, [winPatterns]);

  // 무승부 확인
  const isBoardFull = useCallback((boardState) => {
    return !boardState.includes(' ');
  }, []);

  // 게임 종료 확인
  const checkGameEnd = useCallback((boardState) => {
    const winResult = checkWinner(boardState);
    if (winResult) {
      setGameOver(true);
      setScore(prev => ({
        ...prev,
        [winResult.winner]: prev[winResult.winner] + 1
      }));
      setStatus(`🎉 플레이어 ${winResult.winner}가 승리했습니다!`);
      return { ended: true, winner: winResult.winner, pattern: winResult.pattern };
    }
    
    if (isBoardFull(boardState)) {
      setGameOver(true);
      setScore(prev => ({ ...prev, draws: prev.draws + 1 }));
      setStatus('🤝 무승부입니다!');
      return { ended: true, winner: null, pattern: null };
    }
    
    return { ended: false, winner: null, pattern: null };
  }, [checkWinner, isBoardFull]);

  // 플레이어 교대
  const switchPlayer = useCallback(() => {
    setCurrentPlayer(prev => prev === 'X' ? 'O' : 'X');
  }, []);

  // 랜덤 AI 움직임
  const getRandomMove = useCallback((boardState) => {
    const emptyPositions = boardState
      .map((cell, index) => cell === ' ' ? index : null)
      .filter(pos => pos !== null);
    
    return emptyPositions.length > 0 
      ? emptyPositions[Math.floor(Math.random() * emptyPositions.length)]
      : null;
  }, []);

  // 스마트 AI 움직임
  const getSmartMove = useCallback((boardState) => {
    // 1. 승리 가능한 수 찾기
    for (const pattern of winPatterns) {
      const values = pattern.map(i => boardState[i]);
      if (values.filter(v => v === 'O').length === 2 && 
          values.filter(v => v === ' ').length === 1) {
        return pattern[values.indexOf(' ')];
      }
    }

    // 2. 상대방 승리 차단
    for (const pattern of winPatterns) {
      const values = pattern.map(i => boardState[i]);
      if (values.filter(v => v === 'X').length === 2 && 
          values.filter(v => v === ' ').length === 1) {
        return pattern[values.indexOf(' ')];
      }
    }

    // 3. 중앙 선택
    if (boardState[4] === ' ') {
      return 4;
    }

    // 4. 코너 선택
    const corners = [0, 2, 6, 8];
    const availableCorners = corners.filter(i => boardState[i] === ' ');
    if (availableCorners.length > 0) {
      return availableCorners[Math.floor(Math.random() * availableCorners.length)];
    }

    // 5. 랜덤 선택
    return getRandomMove(boardState);
  }, [winPatterns, getRandomMove]);

  // AI 움직임 처리
  const handleAiMove = useCallback(async (boardState, player) => {
    setAiThinking(true);
    setStatus('🤖 AI가 생각 중...');

    // AI 생각 시간 시뮬레이션
    await new Promise(resolve => setTimeout(resolve, 800));

    if (gameOver) return;

    const position = gameMode === 2 
      ? getRandomMove(boardState)
      : getSmartMove(boardState);

    if (position !== null) {
      const newBoard = [...boardState];
      newBoard[position] = player;
      setBoard(newBoard);

      const gameResult = checkGameEnd(newBoard);
      if (!gameResult.ended) {
        switchPlayer();
        setStatus('당신의 차례입니다!');
      }
    }

    setAiThinking(false);
  }, [gameOver, gameMode, getRandomMove, getSmartMove, checkGameEnd, switchPlayer]);

  // 버튼 클릭 처리
  const handleCellClick = useCallback((position) => {
    if (gameOver || board[position] !== ' ' || aiThinking) {
      return;
    }

    const newBoard = [...board];
    newBoard[position] = currentPlayer;
    setBoard(newBoard);

    const gameResult = checkGameEnd(newBoard);
    if (!gameResult.ended) {
      switchPlayer();
      
      // AI 턴인지 확인
      if (gameMode > 1 && currentPlayer === 'X') {
        // 다음 턴이 O(AI)인 경우
        setTimeout(() => {
          handleAiMove(newBoard, 'O');
        }, 100);
      } else {
        setStatus('당신의 차례입니다!');
      }
    }
  }, [board, currentPlayer, gameOver, aiThinking, gameMode, checkGameEnd, switchPlayer, handleAiMove]);

  // 새 게임 시작
  const newGame = useCallback(() => {
    setBoard(Array(boardSize * boardSize).fill(' '));
    setCurrentPlayer('X');
    setGameOver(false);
    setAiThinking(false);
    setStatus('새 게임이 시작되었습니다!');
  }, [boardSize]);

  // 보드 크기 변경 시 게임 초기화
  useEffect(() => {
    setBoard(Array(boardSize * boardSize).fill(' '));
    setCurrentPlayer('X');
    setGameOver(false);
    setAiThinking(false);
    setScore({ X: 0, O: 0, draws: 0 });
    setStatus(`${boardSize}×${boardSize} 게임이 시작되었습니다!`);
  }, [boardSize]);

  // 점수 초기화
  const resetScore = useCallback(() => {
    setScore({ X: 0, O: 0, draws: 0 });
    setStatus('점수가 초기화되었습니다!');
  }, []);



  // 승리 패턴 확인 (하이라이트용)
  const getWinningPattern = useCallback(() => {
    const winResult = checkWinner(board);
    return winResult ? winResult.pattern : null;
  }, [board, checkWinner]);

  // 셀 렌더링
  const renderCell = (position) => {
    const value = board[position];
    const isWinningCell = getWinningPattern()?.includes(position);
    
    let cellClass = `cell cell-${boardSize}x${boardSize}`;
    if (value === 'X') cellClass += ' cell-x';
    if (value === 'O') cellClass += ' cell-o';
    if (isWinningCell) cellClass += ' cell-winner';
    if (gameOver || aiThinking) cellClass += ' cell-disabled';

    return (
      <button
        key={position}
        className={cellClass}
        onClick={() => handleCellClick(position)}
        disabled={gameOver || aiThinking || value !== ' '}
      >
        {value !== ' ' ? value : ''}
      </button>
    );
  };

  return (
    <div className="tictactoe-container">
      <div className="tictactoe-header">
        <div className="header-top">
          <button className="back-button" onClick={onBackToMenu}>
            ← 메뉴로 돌아가기
          </button>
          <div className="game-info">
            <h1>🎮 {boardSize}×{boardSize} 틱택토</h1>
            <p className="game-mode-display">
              {gameMode === 1 && '👥 플레이어 vs 플레이어'}
              {gameMode === 2 && '🤖 플레이어 vs AI (쉬움)'}
              {gameMode === 3 && '🧠 플레이어 vs AI (어려움)'}
            </p>
          </div>
        </div>

        {/* 현재 플레이어 */}
        <div className="current-player">
          현재 차례: <span className={`player-${currentPlayer.toLowerCase()}`}>{currentPlayer}</span>
        </div>
      </div>

      {/* 게임 보드 */}
      <div className={`game-board board-${boardSize}x${boardSize}`}>
        {Array.from({ length: boardSize * boardSize }, (_, i) => renderCell(i))}
      </div>

      {/* 점수 표시 */}
      <div className="score-board">
        <h3>📊 점수</h3>
        <div className="score-display">
          <div className="score-item">
            <span className="player-x">X</span>
            <span>{score.X}승</span>
          </div>
          <div className="score-item">
            <span>무승부</span>
            <span>{score.draws}회</span>
          </div>
          <div className="score-item">
            <span className="player-o">O</span>
            <span>{score.O}승</span>
          </div>
        </div>
      </div>

      {/* 컨트롤 버튼 */}
      <div className="controls">
        <button className="btn btn-primary" onClick={newGame}>
          🔄 새 게임
        </button>
        <button className="btn btn-secondary" onClick={resetScore}>
          📊 점수 초기화
        </button>
      </div>

      {/* 상태 표시 */}
      <div className="status">
        {status}
      </div>
    </div>
  );
};

export default TicTacToe;
