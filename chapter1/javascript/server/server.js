const WebSocket = require('ws');
const http = require('http');

// HTTP 서버 생성
const server = http.createServer();
const wss = new WebSocket.Server({ server });

// 게임 상태 관리
class GameManager {
  constructor() {
    this.rooms = new Map(); // roomId -> Room
    this.players = new Map(); // playerId -> Player
    this.waitingPlayers = []; // 대기 중인 플레이어들
  }

  // 새 플레이어 추가
  addPlayer(ws, playerName) {
    const playerId = this.generateId();
    const player = {
      id: playerId,
      name: playerName,
      ws: ws,
      roomId: null,
      isReady: false
    };
    
    this.players.set(playerId, player);
    ws.playerId = playerId;
    
    return player;
  }

  // 플레이어 제거
  removePlayer(playerId) {
    const player = this.players.get(playerId);
    if (player) {
      // 방에서 제거
      if (player.roomId) {
        this.leaveRoom(playerId);
      }
      
      // 대기열에서 제거
      this.waitingPlayers = this.waitingPlayers.filter(p => p.id !== playerId);
      
      this.players.delete(playerId);
    }
  }

  // 게임 방 생성
  createRoom(player1, player2, boardSize, gameMode) {
    const roomId = this.generateId();
    const room = {
      id: roomId,
      players: [player1, player2],
      boardSize: boardSize,
      gameMode: gameMode,
      board: Array(boardSize * boardSize).fill(' '),
      currentPlayer: 'X',
      gameOver: false,
      winner: null,
      createdAt: new Date()
    };

    // 플레이어 할당
    player1.symbol = 'X';
    player2.symbol = 'O';
    player1.roomId = roomId;
    player2.roomId = roomId;

    this.rooms.set(roomId, room);
    
    // 양 플레이어에게 게임 시작 알림
    this.broadcastToRoom(roomId, {
      type: 'GAME_START',
      room: this.getRoomInfo(roomId)
    });

    return room;
  }

  // 방 떠나기
  leaveRoom(playerId) {
    const player = this.players.get(playerId);
    if (!player || !player.roomId) return;

    const room = this.rooms.get(player.roomId);
    if (!room) return;

    // 상대방에게 알림
    const opponent = room.players.find(p => p.id !== playerId);
    if (opponent) {
      this.sendToPlayer(opponent.id, {
        type: 'OPPONENT_LEFT',
        message: `${player.name}님이 게임을 떠났습니다.`
      });
      opponent.roomId = null;
    }

    // 방 삭제
    this.rooms.delete(player.roomId);
    player.roomId = null;
  }

  // 플레이어 매칭
  findMatch(player, boardSize, gameMode) {
    // 같은 설정을 원하는 대기 중인 플레이어 찾기
    const matchIndex = this.waitingPlayers.findIndex(p => 
      p.id !== player.id && 
      p.preferredBoardSize === boardSize &&
      p.preferredGameMode === gameMode
    );

    if (matchIndex !== -1) {
      // 매치 발견!
      const opponent = this.waitingPlayers.splice(matchIndex, 1)[0];
      
      // 대기열에서 현재 플레이어도 제거
      this.waitingPlayers = this.waitingPlayers.filter(p => p.id !== player.id);
      
      // 게임 방 생성
      return this.createRoom(player, opponent, boardSize, gameMode);
    } else {
      // 대기열에 추가
      player.preferredBoardSize = boardSize;
      player.preferredGameMode = gameMode;
      
      if (!this.waitingPlayers.find(p => p.id === player.id)) {
        this.waitingPlayers.push(player);
      }
      
      return null;
    }
  }

  // 게임 움직임 처리
  makeMove(playerId, position) {
    const player = this.players.get(playerId);
    if (!player || !player.roomId) return false;

    const room = this.rooms.get(player.roomId);
    if (!room || room.gameOver) return false;

    // 현재 플레이어 차례인지 확인
    if (player.symbol !== room.currentPlayer) return false;

    // 해당 위치가 비어있는지 확인
    if (room.board[position] !== ' ') return false;

    // 움직임 적용
    room.board[position] = player.symbol;

    // 승리 확인
    const winner = this.checkWinner(room.board, room.boardSize);
    if (winner) {
      room.gameOver = true;
      room.winner = winner;
    } else if (!room.board.includes(' ')) {
      room.gameOver = true;
      room.winner = 'draw';
    }

    // 플레이어 교대
    if (!room.gameOver) {
      room.currentPlayer = room.currentPlayer === 'X' ? 'O' : 'X';
    }

    // 방의 모든 플레이어에게 업데이트 전송
    this.broadcastToRoom(player.roomId, {
      type: 'GAME_UPDATE',
      room: this.getRoomInfo(player.roomId),
      move: {
        playerId,
        position,
        symbol: player.symbol
      }
    });

    return true;
  }

  // 승리 확인
  checkWinner(board, boardSize) {
    const patterns = this.generateWinPatterns(boardSize);
    
    for (const pattern of patterns) {
      const values = pattern.map(pos => board[pos]);
      if (values.every(val => val !== ' ' && val === values[0])) {
        return values[0];
      }
    }
    
    return null;
  }

  // 승리 패턴 생성
  generateWinPatterns(size) {
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
    
    // 대각선 패턴
    const mainDiagonal = [];
    const antiDiagonal = [];
    for (let i = 0; i < size; i++) {
      mainDiagonal.push(i * size + i);
      antiDiagonal.push(i * size + (size - 1 - i));
    }
    patterns.push(mainDiagonal);
    patterns.push(antiDiagonal);
    
    return patterns;
  }

  // 방 정보 가져오기
  getRoomInfo(roomId) {
    const room = this.rooms.get(roomId);
    if (!room) return null;

    return {
      id: room.id,
      players: room.players.map(p => ({
        id: p.id,
        name: p.name,
        symbol: p.symbol
      })),
      boardSize: room.boardSize,
      gameMode: room.gameMode,
      board: room.board,
      currentPlayer: room.currentPlayer,
      gameOver: room.gameOver,
      winner: room.winner
    };
  }

  // 방의 모든 플레이어에게 메시지 전송
  broadcastToRoom(roomId, message) {
    const room = this.rooms.get(roomId);
    if (!room) return;

    room.players.forEach(player => {
      if (player.ws.readyState === WebSocket.OPEN) {
        player.ws.send(JSON.stringify(message));
      }
    });
  }

  // 특정 플레이어에게 메시지 전송
  sendToPlayer(playerId, message) {
    const player = this.players.get(playerId);
    if (player && player.ws.readyState === WebSocket.OPEN) {
      player.ws.send(JSON.stringify(message));
    }
  }

  // ID 생성
  generateId() {
    return Math.random().toString(36).substr(2, 9);
  }

  // 통계 정보
  getStats() {
    return {
      totalPlayers: this.players.size,
      activeRooms: this.rooms.size,
      waitingPlayers: this.waitingPlayers.length
    };
  }
}

// 게임 매니저 인스턴스
const gameManager = new GameManager();

// WebSocket 연결 처리
wss.on('connection', (ws) => {
  console.log('새로운 클라이언트 연결');

  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      console.log('받은 메시지:', data);

      switch (data.type) {
        case 'JOIN':
          // 플레이어 등록
          const player = gameManager.addPlayer(ws, data.playerName);
          ws.send(JSON.stringify({
            type: 'JOINED',
            playerId: player.id,
            playerName: player.name
          }));
          break;

        case 'FIND_MATCH':
          // 매치 찾기
          const match = gameManager.findMatch(
            gameManager.players.get(ws.playerId),
            data.boardSize,
            data.gameMode
          );

          if (match) {
            console.log(`매치 성사: Room ${match.id}`);
          } else {
            ws.send(JSON.stringify({
              type: 'WAITING_FOR_OPPONENT',
              message: '상대방을 찾고 있습니다...'
            }));
          }
          break;

        case 'MAKE_MOVE':
          // 게임 움직임
          const success = gameManager.makeMove(ws.playerId, data.position);
          if (!success) {
            ws.send(JSON.stringify({
              type: 'INVALID_MOVE',
              message: '유효하지 않은 움직임입니다.'
            }));
          }
          break;

        case 'LEAVE_ROOM':
          // 방 떠나기
          gameManager.leaveRoom(ws.playerId);
          break;

        case 'GET_STATS':
          // 통계 정보
          ws.send(JSON.stringify({
            type: 'STATS',
            stats: gameManager.getStats()
          }));
          break;

        default:
          console.log('알 수 없는 메시지 타입:', data.type);
      }
    } catch (error) {
      console.error('메시지 처리 오류:', error);
      ws.send(JSON.stringify({
        type: 'ERROR',
        message: '서버 오류가 발생했습니다.'
      }));
    }
  });

  ws.on('close', () => {
    console.log('클라이언트 연결 종료');
    if (ws.playerId) {
      gameManager.removePlayer(ws.playerId);
    }
  });

  ws.on('error', (error) => {
    console.error('WebSocket 오류:', error);
  });
});

// 서버 시작
const PORT = process.env.PORT || 8080;
const HOST = process.env.NODE_ENV === 'production' ? '0.0.0.0' : 'localhost';

server.listen(PORT, HOST, () => {
  console.log(`🎮 틱택토 멀티플레이어 서버가 ${HOST}:${PORT}에서 실행 중입니다!`);
  
  if (process.env.NODE_ENV === 'production') {
    console.log(`WebSocket 서버: wss://${process.env.RAILWAY_STATIC_URL || 'your-domain.com'}`);
  } else {
    console.log(`WebSocket 서버: ws://localhost:${PORT}`);
  }
});

// 헬스체크 엔드포인트 (Railway, Render 등에서 사용)
server.on('request', (req, res) => {
  if (req.url === '/health' || req.url === '/') {
    res.writeHead(200, { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    });
    res.end(JSON.stringify({
      status: 'OK',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      stats: gameManager.getStats()
    }));
  }
});

// 주기적 통계 출력
setInterval(() => {
  const stats = gameManager.getStats();
  console.log(`📊 서버 상태 - 플레이어: ${stats.totalPlayers}, 활성 방: ${stats.activeRooms}, 대기 중: ${stats.waitingPlayers}`);
}, 30000); // 30초마다
