import { useState, useEffect, useRef, useCallback } from 'react';

const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState(null);
  const [lastMessage, setLastMessage] = useState(null);
  
  const ws = useRef(null);
  const messageHandlers = useRef(new Map());
  const reconnectTimeout = useRef(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  // WebSocket 연결
  const connect = useCallback((playerName) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      return Promise.resolve();
    }

    setIsConnecting(true);
    setError(null);

    return new Promise((resolve, reject) => {
      try {
        // WebSocket 서버 URL (환경별 설정)
        const wsUrl = process.env.REACT_APP_WS_URL || 
                     (process.env.NODE_ENV === 'production' 
                      ? 'wss://cursor-study-production-4850.up.railway.app'  // Railway 도메인
                      : 'ws://localhost:8080');
        
        console.log('WebSocket 연결 시도:', wsUrl);
        ws.current = new WebSocket(wsUrl);

        ws.current.onopen = () => {
          console.log('WebSocket 연결 성공');
          setIsConnected(true);
          setIsConnecting(false);
          setError(null);
          reconnectAttempts.current = 0;

          // 플레이어 등록
          if (playerName) {
            sendMessage({
              type: 'JOIN',
              playerName: playerName
            });
          }

          resolve();
        };

        ws.current.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            console.log('받은 메시지:', data);
            
            setLastMessage(data);

            // 타입별 핸들러 실행
            const handler = messageHandlers.current.get(data.type);
            if (handler) {
              handler(data);
            }

            // 전체 메시지 핸들러 실행
            const allHandler = messageHandlers.current.get('*');
            if (allHandler) {
              allHandler(data);
            }
          } catch (error) {
            console.error('메시지 파싱 오류:', error);
          }
        };

        ws.current.onclose = (event) => {
          console.log('WebSocket 연결 종료:', event.code, event.reason);
          setIsConnected(false);
          setIsConnecting(false);

          // 정상적인 종료가 아닌 경우 재연결 시도
          if (event.code !== 1000 && reconnectAttempts.current < maxReconnectAttempts) {
            const delay = Math.pow(2, reconnectAttempts.current) * 1000; // 지수 백오프
            console.log(`${delay}ms 후 재연결 시도 (${reconnectAttempts.current + 1}/${maxReconnectAttempts})`);
            
            reconnectTimeout.current = setTimeout(() => {
              reconnectAttempts.current++;
              connect(playerName);
            }, delay);
          }
        };

        ws.current.onerror = (error) => {
          console.error('WebSocket 오류:', error);
          setError('연결 오류가 발생했습니다.');
          setIsConnecting(false);
          reject(error);
        };
      } catch (error) {
        console.error('WebSocket 연결 실패:', error);
        setError('서버에 연결할 수 없습니다.');
        setIsConnecting(false);
        reject(error);
      }
    });
  }, []);

  // WebSocket 연결 해제
  const disconnect = useCallback(() => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current);
      reconnectTimeout.current = null;
    }

    if (ws.current) {
      ws.current.close(1000, 'User disconnected');
      ws.current = null;
    }

    setIsConnected(false);
    setIsConnecting(false);
    setError(null);
    reconnectAttempts.current = 0;
  }, []);

  // 메시지 전송
  const sendMessage = useCallback((message) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      try {
        const jsonMessage = JSON.stringify(message);
        ws.current.send(jsonMessage);
        console.log('메시지 전송:', message);
        return true;
      } catch (error) {
        console.error('메시지 전송 오류:', error);
        setError('메시지 전송에 실패했습니다.');
        return false;
      }
    } else {
      console.warn('WebSocket이 연결되지 않았습니다.');
      setError('서버 연결이 끊어졌습니다.');
      return false;
    }
  }, []);

  // 메시지 핸들러 등록
  const addMessageHandler = useCallback((type, handler) => {
    messageHandlers.current.set(type, handler);
    
    // 클린업 함수 반환
    return () => {
      messageHandlers.current.delete(type);
    };
  }, []);

  // 메시지 핸들러 제거
  const removeMessageHandler = useCallback((type) => {
    messageHandlers.current.delete(type);
  }, []);

  // 컴포넌트 언마운트 시 연결 해제
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  // 연결 상태 확인
  const getConnectionState = useCallback(() => {
    if (!ws.current) return 'CLOSED';
    
    switch (ws.current.readyState) {
      case WebSocket.CONNECTING:
        return 'CONNECTING';
      case WebSocket.OPEN:
        return 'OPEN';
      case WebSocket.CLOSING:
        return 'CLOSING';
      case WebSocket.CLOSED:
        return 'CLOSED';
      default:
        return 'UNKNOWN';
    }
  }, []);

  return {
    // 상태
    isConnected,
    isConnecting,
    error,
    lastMessage,
    connectionState: getConnectionState(),
    
    // 메서드
    connect,
    disconnect,
    sendMessage,
    addMessageHandler,
    removeMessageHandler,
    
    // 편의 메서드들
    findMatch: useCallback((boardSize, gameMode) => {
      return sendMessage({
        type: 'FIND_MATCH',
        boardSize,
        gameMode
      });
    }, [sendMessage]),
    
    makeMove: useCallback((position) => {
      return sendMessage({
        type: 'MAKE_MOVE',
        position
      });
    }, [sendMessage]),
    
    leaveRoom: useCallback(() => {
      return sendMessage({
        type: 'LEAVE_ROOM'
      });
    }, [sendMessage]),
    
    getStats: useCallback(() => {
      return sendMessage({
        type: 'GET_STATS'
      });
    }, [sendMessage])
  };
};

export default useWebSocket;
