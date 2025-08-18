import React, { useState } from 'react';
import StartScreen from './StartScreen';
import TicTacToe from './TicTacToe';
import MultiplayerTicTacToe from './MultiplayerTicTacToe';
import './App.css';

function App() {
  const [gameState, setGameState] = useState({
    isPlaying: false,
    boardSize: 3,
    gameMode: 1,
    isMultiplayer: false
  });

  const handleStartGame = ({ boardSize, gameMode }) => {
    const isMultiplayer = gameMode === 4; // 온라인 멀티플레이어 모드
    
    setGameState({
      isPlaying: true,
      boardSize,
      gameMode: isMultiplayer ? 1 : gameMode, // 멀티플레이어는 항상 PvP
      isMultiplayer
    });
  };

  const handleBackToMenu = () => {
    setGameState({
      isPlaying: false,
      boardSize: 3,
      gameMode: 1,
      isMultiplayer: false
    });
  };

  return (
    <div className="App">
      {gameState.isPlaying ? (
        <div className="app-background">
          {gameState.isMultiplayer ? (
            <MultiplayerTicTacToe
              boardSize={gameState.boardSize}
              gameMode={gameState.gameMode}
              onBackToMenu={handleBackToMenu}
            />
          ) : (
            <TicTacToe
              boardSize={gameState.boardSize}
              gameMode={gameState.gameMode}
              onBackToMenu={handleBackToMenu}
            />
          )}
        </div>
      ) : (
        <StartScreen onStartGame={handleStartGame} />
      )}
    </div>
  );
}

export default App;
