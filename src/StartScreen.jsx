import React from 'react';
import './StartScreen.css';

const StartScreen = ({ onStartGame }) => {
  const handleStartGame = (boardSize, gameMode) => {
    onStartGame({ boardSize, gameMode });
  };

  const gameModes = [
    { id: 1, name: '플레이어 vs 플레이어', icon: '👥', type: 'local' },
    { id: 2, name: '플레이어 vs AI (쉬움)', icon: '🤖', type: 'ai' },
    { id: 3, name: '플레이어 vs AI (어려움)', icon: '🧠', type: 'ai' },
    { id: 4, name: '온라인 멀티플레이어', icon: '🌐', type: 'multiplayer' }
  ];

  const boardSizes = [
    { size: 3, name: '3×3 클래식', description: '전통적인 틱택토', difficulty: '쉬움' },
    { size: 4, name: '4×4 챌린지', description: '더 복잡한 전략 게임', difficulty: '어려움' }
  ];

  return (
    <div className="start-screen">
      <div className="start-container">
        <header className="start-header">
          <h1 className="game-title">
            <span className="title-icon">🎮</span>
            틱택토 게임
          </h1>
          <p className="game-subtitle">
            친구와 함께 또는 AI와 대결해보세요!
          </p>
        </header>

        <div className="game-options">
          {/* 보드 크기 선택 */}
          <section className="option-section">
            <h2 className="section-title">
              <span className="section-icon">🎯</span>
              게임 보드 선택
            </h2>
            <div className="board-size-grid">
              {boardSizes.map(board => (
                <div key={board.size} className="board-size-section">
                  <div className="board-preview">
                    <div className={`preview-grid grid-${board.size}x${board.size}`}>
                      {Array.from({ length: board.size * board.size }, (_, i) => (
                        <div key={i} className="preview-cell">
                          {i === 0 && <span className="preview-x">×</span>}
                          {i === board.size + 1 && <span className="preview-o">○</span>}
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="board-info">
                    <h3 className="board-name">{board.name}</h3>
                    <p className="board-description">{board.description}</p>
                    <span className={`difficulty-badge ${board.difficulty === '쉬움' ? 'easy' : 'hard'}`}>
                      {board.difficulty}
                    </span>
                  </div>
                  
                  {/* 게임 모드 버튼들 */}
                  <div className="game-mode-buttons">
                    {gameModes.map(mode => (
                      <button
                        key={`${board.size}-${mode.id}`}
                        className={`mode-button mode-${mode.id}`}
                        onClick={() => handleStartGame(board.size, mode.id)}
                      >
                        <span className="mode-icon">{mode.icon}</span>
                        <span className="mode-name">{mode.name}</span>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* 게임 규칙 */}
          <section className="rules-section">
            <h2 className="section-title">
              <span className="section-icon">📋</span>
              게임 규칙
            </h2>
            <div className="rules-grid">
              <div className="rule-item">
                <div className="rule-icon">🎯</div>
                <div className="rule-content">
                  <h4>3×3 모드</h4>
                  <p>가로, 세로, 대각선으로 3개를 먼저 연결하면 승리!</p>
                </div>
              </div>
              <div className="rule-item">
                <div className="rule-icon">🔥</div>
                <div className="rule-content">
                  <h4>4×4 모드</h4>
                  <p>가로, 세로, 대각선으로 4개를 먼저 연결하면 승리!</p>
                </div>
              </div>
              <div className="rule-item">
                <div className="rule-icon">🤖</div>
                <div className="rule-content">
                  <h4>AI 모드</h4>
                  <p>쉬움: 랜덤 전략, 어려움: 스마트 전략으로 도전!</p>
                </div>
              </div>
            </div>
          </section>
        </div>

        <footer className="start-footer">
          <p>즐거운 게임 되세요! 🎉</p>
        </footer>
      </div>
    </div>
  );
};

export default StartScreen;
