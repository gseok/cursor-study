#!/usr/bin/env python3
"""
깔끔한 틱택토 게임 - 최소한의 GUI 업데이트로 안정적인 동작
"""

import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

class CleanTicTacToe:
    def __init__(self):
        # 게임 상태
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.ai_thinking = False
        self.game_mode = 1  # 1: PvP, 2: PvAI(쉬움), 3: PvAI(어려움)
        self.score = {'X': 0, 'O': 0, 'draws': 0}
        
        # 승리 패턴
        self.win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 행
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 열
            [0, 4, 8], [2, 4, 6]              # 대각선
        ]
        
        self.setup_gui()
        
    def setup_gui(self):
        """GUI 초기 설정"""
        self.root = tk.Tk()
        self.root.title("틱택토 게임")
        self.root.geometry("500x600")
        self.root.configure(bg='white')
        self.root.resizable(False, False)
        
        # 제목
        title_label = tk.Label(
            self.root,
            text="🎮 틱택토 게임",
            font=('Arial', 24, 'bold'),
            bg='white',
            fg='black'
        )
        title_label.pack(pady=15)
        
        # 게임 모드 선택
        self.create_mode_selection()
        
        # 현재 플레이어 표시
        self.player_label = tk.Label(
            self.root,
            text="현재 차례: X",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='black'
        )
        self.player_label.pack(pady=10)
        
        # 게임 보드
        self.create_game_board()
        
        # 점수 표시
        self.create_score_display()
        
        # 컨트롤 버튼
        self.create_control_buttons()
        
        # 상태 표시
        self.status_label = tk.Label(
            self.root,
            text="게임을 시작하세요!",
            font=('Arial', 12),
            bg='white',
            fg='gray'
        )
        self.status_label.pack(pady=10)
        
    def create_mode_selection(self):
        """게임 모드 선택 UI"""
        mode_frame = tk.Frame(self.root, bg='white')
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="게임 모드:", font=('Arial', 12, 'bold'), 
                bg='white', fg='black').pack(side=tk.LEFT, padx=(0, 10))
        
        self.mode_var = tk.StringVar(value="1")
        
        modes = [("플레이어 vs 플레이어", "1"), ("vs AI (쉬움)", "2"), ("vs AI (어려움)", "3")]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame, text=text, variable=self.mode_var, value=value,
                font=('Arial', 10), bg='white', fg='black',
                command=self.on_mode_change
            ).pack(side=tk.LEFT, padx=8)
    
    def create_game_board(self):
        """게임 보드 생성"""
        board_frame = tk.Frame(self.root, bg='white')
        board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            row, col = i // 3, i % 3
            
            btn = tk.Button(
                board_frame,
                text='',
                font=('Arial', 32, 'bold'),
                width=4,
                height=2,
                bg='lightgray',
                fg='black',
                relief='solid',
                borderwidth=2,
                command=lambda idx=i: self.on_button_click(idx)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)
    
    def create_score_display(self):
        """점수 표시 UI"""
        score_frame = tk.Frame(self.root, bg='white')
        score_frame.pack(pady=15)
        
        tk.Label(score_frame, text="📊 점수", font=('Arial', 14, 'bold'), 
                bg='white', fg='black').pack()
        
        info_frame = tk.Frame(score_frame, bg='white')
        info_frame.pack(pady=5)
        
        # X 점수
        x_frame = tk.Frame(info_frame, bg='white')
        x_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(x_frame, text="X", font=('Arial', 12, 'bold'), 
                bg='white', fg='red').pack()
        self.x_score_label = tk.Label(x_frame, text="0승", font=('Arial', 10), 
                                     bg='white', fg='black')
        self.x_score_label.pack()
        
        # 무승부 점수
        draw_frame = tk.Frame(info_frame, bg='white')
        draw_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(draw_frame, text="무승부", font=('Arial', 12, 'bold'), 
                bg='white', fg='black').pack()
        self.draw_score_label = tk.Label(draw_frame, text="0회", font=('Arial', 10), 
                                        bg='white', fg='black')
        self.draw_score_label.pack()
        
        # O 점수
        o_frame = tk.Frame(info_frame, bg='white')
        o_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(o_frame, text="O", font=('Arial', 12, 'bold'), 
                bg='white', fg='blue').pack()
        self.o_score_label = tk.Label(o_frame, text="0승", font=('Arial', 10), 
                                     bg='white', fg='black')
        self.o_score_label.pack()
    
    def create_control_buttons(self):
        """컨트롤 버튼들"""
        control_frame = tk.Frame(self.root, bg='white')
        control_frame.pack(pady=15)
        
        tk.Button(
            control_frame, text="🔄 새 게임", font=('Arial', 14, 'bold'),
            bg='lightgreen', fg='black', padx=20, pady=8,
            command=self.new_game
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            control_frame, text="📊 점수 초기화", font=('Arial', 14, 'bold'),
            bg='orange', fg='black', padx=20, pady=8,
            command=self.reset_score
        ).pack(side=tk.LEFT, padx=10)
    
    def on_mode_change(self):
        """게임 모드 변경 시"""
        new_mode = int(self.mode_var.get())
        if new_mode != self.game_mode:
            self.game_mode = new_mode
            self.new_game()
            mode_names = {1: "플레이어 vs 플레이어", 2: "vs AI (쉬움)", 3: "vs AI (어려움)"}
            self.status_label.config(text=f"모드: {mode_names[self.game_mode]}")
    
    def on_button_click(self, position):
        """버튼 클릭 처리 - 여기서만 GUI 업데이트"""
        # 유효성 검사
        if self.game_over or self.board[position] != ' ' or self.ai_thinking:
            return
        
        # 플레이어 움직임 처리
        self.board[position] = self.current_player
        self.update_single_button(position)
        
        # 게임 종료 확인
        if self.check_game_end():
            return
        
        # 플레이어 교대
        self.switch_player()
        
        # AI 턴 처리
        if self.game_mode in [2, 3] and self.current_player == 'O':
            self.handle_ai_turn()
    
    def update_single_button(self, position):
        """단일 버튼만 업데이트"""
        btn = self.buttons[position]
        
        if self.board[position] == 'X':
            btn.config(text='X', bg='red', fg='white', state='disabled')
        elif self.board[position] == 'O':
            btn.config(text='O', bg='blue', fg='white', state='disabled')
    
    def switch_player(self):
        """플레이어 교대"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.player_label.config(text=f"현재 차례: {self.current_player}")
    
    def handle_ai_turn(self):
        """AI 턴 처리"""
        self.ai_thinking = True
        self.status_label.config(text="🤖 AI가 생각 중...")
        
        # AI 동작을 별도 스레드에서 실행
        def ai_move():
            time.sleep(0.8)  # AI 생각 시간
            
            if self.game_over:  # 게임이 끝났으면 중단
                return
            
            # AI 위치 결정
            if self.game_mode == 2:
                position = self.get_random_move()
            else:
                position = self.get_smart_move()
            
            # 메인 스레드에서 GUI 업데이트
            self.root.after(0, self.execute_ai_move, position)
        
        threading.Thread(target=ai_move, daemon=True).start()
    
    def execute_ai_move(self, position):
        """AI 움직임 실행 - GUI 업데이트"""
        if self.game_over or position is None:
            return
        
        self.ai_thinking = False
        self.board[position] = self.current_player
        self.update_single_button(position)
        
        if self.check_game_end():
            return
        
        self.switch_player()
        self.status_label.config(text="당신의 차례입니다!")
    
    def get_random_move(self):
        """랜덤 AI 움직임"""
        empty_positions = [i for i, cell in enumerate(self.board) if cell == ' ']
        return random.choice(empty_positions) if empty_positions else None
    
    def get_smart_move(self):
        """스마트 AI 움직임"""
        # 1. 승리 가능한 수
        for pattern in self.win_patterns:
            values = [self.board[i] for i in pattern]
            if values.count('O') == 2 and values.count(' ') == 1:
                return pattern[values.index(' ')]
        
        # 2. 상대방 승리 차단
        for pattern in self.win_patterns:
            values = [self.board[i] for i in pattern]
            if values.count('X') == 2 and values.count(' ') == 1:
                return pattern[values.index(' ')]
        
        # 3. 중앙 선택
        if self.board[4] == ' ':
            return 4
        
        # 4. 코너 선택
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == ' ']
        if available_corners:
            return random.choice(available_corners)
        
        # 5. 랜덤 선택
        return self.get_random_move()
    
    def check_game_end(self):
        """게임 종료 확인"""
        winner = self.check_winner()
        
        if winner:
            self.game_over = True
            self.highlight_winner(winner)
            self.update_score(winner)
            messagebox.showinfo("게임 종료", f"🎉 {winner} 승리!")
            return True
        
        if ' ' not in self.board:
            self.game_over = True
            self.update_score('draw')
            messagebox.showinfo("게임 종료", "🤝 무승부!")
            return True
        
        return False
    
    def check_winner(self):
        """승자 확인"""
        for pattern in self.win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] == 
                self.board[pattern[2]] != ' '):
                return self.board[pattern[0]]
        return None
    
    def highlight_winner(self, winner):
        """승리 패턴 하이라이트"""
        for pattern in self.win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] == 
                self.board[pattern[2]] == winner):
                for pos in pattern:
                    self.buttons[pos].config(
                        bg='yellow',
                        fg='black',
                        font=('Arial', 36, 'bold')
                    )
                break
    
    def update_score(self, result):
        """점수 업데이트"""
        if result == 'X':
            self.score['X'] += 1
            self.x_score_label.config(text=f"{self.score['X']}승")
        elif result == 'O':
            self.score['O'] += 1
            self.o_score_label.config(text=f"{self.score['O']}승")
        else:
            self.score['draws'] += 1
            self.draw_score_label.config(text=f"{self.score['draws']}회")
    
    def new_game(self):
        """새 게임 시작"""
        # 게임 상태 초기화
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.ai_thinking = False
        
        # 모든 버튼 초기화
        for btn in self.buttons:
            btn.config(
                text='',
                bg='lightgray',
                fg='black',
                state='normal',
                font=('Arial', 32, 'bold')
            )
        
        # UI 업데이트
        self.player_label.config(text="현재 차례: X")
        self.status_label.config(text="새 게임 시작!")
    
    def reset_score(self):
        """점수 초기화"""
        self.score = {'X': 0, 'O': 0, 'draws': 0}
        self.x_score_label.config(text="0승")
        self.o_score_label.config(text="0승")
        self.draw_score_label.config(text="0회")
        self.status_label.config(text="점수가 초기화되었습니다!")
    
    def run(self):
        """게임 실행"""
        self.root.mainloop()

def main():
    """메인 함수"""
    game = CleanTicTacToe()
    game.run()

if __name__ == "__main__":
    main()
