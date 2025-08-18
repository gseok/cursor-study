import React, { useState, useEffect, useCallback } from 'react';
import useWebSocket from './hooks/useWebSocket';
import './MultiplayerTicTacToe.css';

const MultiplayerTicTacToe = ({ boardSize, gameMode, onBackToMenu }) => {
  const [gameState, setGameState] = useState('connecting'); // connecting, waiting, playing, finished
  const [playerInfo, setPlayerInfo] = useState(null);
  const [roomInfo, setRoomInfo] = useState(null);
  const [board, setBoard] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('X');
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [playerName, setPlayerName] = useState('');
  const [isMyTurn, setIsMyTurn] = useState(false);
  const [status, setStatus] = useState('서버에 연결 중...');
  const [connectionError, setConnectionError] = useState(null);

  const {
    isConnected,
    isConnecting,
    error,
    connect,
    disconnect,
    findMatch,
    makeMove,
    leaveRoom,
    addMessageHandler,
    removeMessageHandler
  } = useWebSocket();

  // 메시지 핸들러 설정
  useEffect(() => {
    const handlers = [];

    // 서버 연결 성공
    handlers.push(addMessageHandler('JOINED', (data) => {
      console.log('서버 접속 완료:', data);
      setPlayerInfo({
        id: data.playerId,
        name: data.playerName
      });
      setGameState('finding');
      setStatus('상대방을 찾고 있습니다...');
      
      // 매치 찾기 시작
      findMatch(boardSize, gameMode);
    }));

    // 상대방 대기 중
    handlers.push(addMessageHandler('WAITING_FOR_OPPONENT', (data) => {
      setGameState('waiting');
      setStatus(data.message);
    }));

    // 게임 시작
    handlers.push(addMessageHandler('GAME_START', (data) => {
      console.log('게임 시작:', data);
      const room = data.room;
      setRoomInfo(room);
      setBoard(room.board);
      setCurrentPlayer(room.currentPlayer);
      setGameOver(room.gameOver);
      setWinner(room.winner);
      setGameState('playing');
      
      // 내 차례인지 확인
      const myPlayer = room.players.find(p => p.id === playerInfo?.id);
      setIsMyTurn(myPlayer?.symbol === room.currentPlayer);
      
      if (myPlayer) {
        setStatus(`게임 시작! 당신은 ${myPlayer.symbol}입니다.`);
      }
    }));

    // 게임 업데이트
    handlers.push(addMessageHandler('GAME_UPDATE', (data) => {
      console.log('게임 업데이트:', data);
      const room = data.room;
      setBoard(room.board);
      setCurrentPlayer(room.currentPlayer);
      setGameOver(room.gameOver);
      setWinner(room.winner);
      
      if (room.gameOver) {
        setGameState('finished');
        if (room.winner === 'draw') {
          setStatus('무승부입니다!');
        } else {
          const winnerPlayer = room.players.find(p => p.symbol === room.winner);
          const isMyWin = winnerPlayer?.id === playerInfo?.id;
          setStatus(isMyWin ? '🎉 승리했습니다!' : '😢 패배했습니다.');
        }
      } else {
        // 내 차례 확인
        const myPlayer = room.players.find(p => p.id === playerInfo?.id);
        const myTurn = myPlayer?.symbol === room.currentPlayer;
        setIsMyTurn(myTurn);
        setStatus(myTurn ? '당신의 차례입니다!' : '상대방의 차례입니다...');
      }
    }));

    // 상대방이 떠남
    handlers.push(addMessageHandler('OPPONENT_LEFT', (data) => {
      setGameState('finished');
      setStatus(data.message);
    }));

    // 잘못된 움직임
    handlers.push(addMessageHandler('INVALID_MOVE', (data) => {
      setStatus(data.message);
      setTimeout(() => {
        setStatus(isMyTurn ? '당신의 차례입니다!' : '상대방의 차례입니다...');
      }, 2000);
    }));

    // 에러 처리
    handlers.push(addMessageHandler('ERROR', (data) => {
      setConnectionError(data.message);
      setStatus('오류가 발생했습니다.');
    }));

    // 클린업
    return () => {
      handlers.forEach(cleanup => cleanup());
    };
  }, [addMessageHandler, boardSize, gameMode, findMatch, playerInfo?.id, isMyTurn]);

  // 플레이어 이름 입력 후 연결
  const handleConnect = useCallback(async () => {
    if (!playerName.trim()) {
      alert('플레이어 이름을 입력해주세요.');
      return;
    }

    try {
      setGameState('connecting');
      setStatus('서버에 연결 중...');
      await connect(playerName.trim());
    } catch (error) {
      setConnectionError('서버 연결에 실패했습니다.');
      setGameState('error');
    }
  }, [playerName, connect]);

  // 셀 클릭 처리
  const handleCellClick = useCallback((position) => {
    if (!isMyTurn || gameOver || board[position] !== ' ') {
      return;
    }

    makeMove(position);
  }, [isMyTurn, gameOver, board, makeMove]);

  // 게임 나가기
  const handleLeaveGame = useCallback(() => {
    leaveRoom();
    disconnect();
    onBackToMenu();
  }, [leaveRoom, disconnect, onBackToMenu]);

  // 다시 매치 찾기
  const handleFindNewMatch = useCallback(() => {
    setGameState('finding');
    setStatus('새로운 상대방을 찾고 있습니다...');
    findMatch(boardSize, gameMode);
  }, [findMatch, boardSize, gameMode]);

  // 승리 패턴 확인
  const getWinningPattern = useCallback(() => {
    if (!winner || !roomInfo) return null;
    
    const patterns = generateWinPatterns(boardSize);
    for (const pattern of patterns) {
      const values = pattern.map(pos => board[pos]);
      if (values.every(val => val === winner)) {
        return pattern;
      }
    }
    return null;
  }, [winner, roomInfo, board, boardSize]);

  // 승리 패턴 생성
  const generateWinPatterns = (size) => {
    const patterns = [];
    
    // 행, 열, 대각선 패턴 생성
    for (let row = 0; row < size; row++) {
      const rowPattern = [];
      for (let col = 0; col < size; col++) {
        rowPattern.push(row * size + col);
      }
      patterns.push(rowPattern);
    }
    
    for (let col = 0; col < size; col++) {
      const colPattern = [];
      for (let row = 0; row < size; row++) {
        colPattern.push(row * size + col);
      }
      patterns.push(colPattern);
    }
    
    const mainDiagonal = [];
    const antiDiagonal = [];
    for (let i = 0; i < size; i++) {
      mainDiagonal.push(i * size + i);
      antiDiagonal.push(i * size + (size - 1 - i));
    }
    patterns.push(mainDiagonal);
    patterns.push(antiDiagonal);
    
    return patterns;
  };

  // 셀 렌더링
  const renderCell = (position) => {
    const value = board[position] || ' ';
    const isWinningCell = getWinningPattern()?.includes(position);
    
    let cellClass = `mp-cell mp-cell-${boardSize}x${boardSize}`;
    if (value === 'X') cellClass += ' mp-cell-x';
    if (value === 'O') cellClass += ' mp-cell-o';
    if (isWinningCell) cellClass += ' mp-cell-winner';
    if (!isMyTurn || gameOver) cellClass += ' mp-cell-disabled';

    return (
      <button
        key={position}
        className={cellClass}
        onClick={() => handleCellClick(position)}
        disabled={!isMyTurn || gameOver || value !== ' '}
      >
        {value !== ' ' ? value : ''}
      </button>
    );
  };

  // 연결 화면
  if (gameState === 'connecting' || !isConnected) {
    return (
      <div className="mp-container">
        <div className="mp-connect-screen">
          <h1>🌐 멀티플레이어 게임</h1>
          <div className="mp-connect-form">
            <h2>{boardSize}×{boardSize} 멀티플레이어</h2>
            <p>다른 플레이어와 실시간으로 대전하세요!</p>
            
            {!isConnected && (
              <>
                <input
                  type="text"
                  placeholder="플레이어 이름을 입력하세요"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleConnect()}
                  className="mp-name-input"
                  maxLength={20}
                />
                <button
                  onClick={handleConnect}
                  disabled={isConnecting || !playerName.trim()}
                  className="mp-connect-btn"
                >
                  {isConnecting ? '연결 중...' : '게임 참여'}
                </button>
              </>
            )}
            
            {connectionError && (
              <div className="mp-error">
                {connectionError}
              </div>
            )}
            
            <button onClick={onBackToMenu} className="mp-back-btn">
              ← 메뉴로 돌아가기
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mp-container">
      <div className="mp-header">
        <button className="mp-leave-btn" onClick={handleLeaveGame}>
          ← 나가기
        </button>
        <div className="mp-game-info">
          <h1>🌐 {boardSize}×{boardSize} 멀티플레이어</h1>
          {roomInfo && (
            <div className="mp-players">
              {roomInfo.players.map((player, index) => (
                <div
                  key={player.id}
                  className={`mp-player ${player.id === playerInfo?.id ? 'mp-player-me' : ''}`}
                >
                  <span className={`mp-symbol mp-symbol-${player.symbol.toLowerCase()}`}>
                    {player.symbol}
                  </span>
                  <span className="mp-player-name">
                    {player.name}
                    {player.id === playerInfo?.id && ' (나)'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 게임 상태 표시 */}
      <div className="mp-status">
        <div className={`mp-status-text ${isMyTurn ? 'mp-my-turn' : ''}`}>
          {status}
        </div>
        {gameState === 'waiting' && (
          <div className="mp-loading">
            <div className="mp-spinner"></div>
          </div>
        )}
      </div>

      {/* 게임 보드 */}
      {board.length > 0 && (
        <div className={`mp-game-board mp-board-${boardSize}x${boardSize}`}>
          {Array.from({ length: boardSize * boardSize }, (_, i) => renderCell(i))}
        </div>
      )}

      {/* 게임 완료 후 옵션 */}
      {gameState === 'finished' && (
        <div className="mp-game-over">
          <div className="mp-game-over-actions">
            <button onClick={handleFindNewMatch} className="mp-play-again-btn">
              🔄 다시 플레이
            </button>
            <button onClick={handleLeaveGame} className="mp-menu-btn">
              📋 메뉴로 돌아가기
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MultiplayerTicTacToe;
