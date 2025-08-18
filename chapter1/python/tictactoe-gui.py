#!/usr/bin/env python3
"""
틱택토 게임 - tkinter GUI 구현
CLI 버전을 기반으로 한 그래픽 사용자 인터페이스 버전
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import time

class TicTacToeGUI:
    def __init__(self):
        # 게임 상수
        self.EMPTY_CELL = ' '
        self.PLAYER_X = 'X'
        self.PLAYER_O = 'O'
        
        # 승리 패턴
        self.WINNING_PATTERNS = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 행
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 열
            [0, 4, 8], [2, 4, 6]              # 대각선
        ]
        
        # 게임 상태
        self.board = [self.EMPTY_CELL for _ in range(9)]
        self.current_player = self.PLAYER_X
        self.game_over = False
        self.game_mode = 1  # 1: PvP, 2: PvAI(쉬움), 3: PvAI(어려움)
        self.score = {self.PLAYER_X: 0, self.PLAYER_O: 0, 'draws': 0}
        self.ai_thinking = False
        
        # GUI 초기화
        self.setup_gui()
        
    def setup_gui(self):
        """GUI 인터페이스를 설정합니다."""
        self.root = tk.Tk()
        self.root.title("🎮 틱택토 게임")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg='white')
        
        # 스타일 설정
        self.setup_styles()
        
        # 메인 프레임
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 제목
        self.title_label = tk.Label(
            self.main_frame, 
            text="🎮 틱택토 게임", 
            font=('Arial', 24, 'bold'),
            bg='white',
            fg='black'
        )
        self.title_label.pack(pady=(0, 20))
        
        # 게임 모드 선택
        self.setup_mode_selection()
        
        # 현재 플레이어 표시
        self.setup_player_display()
        
        # 게임 보드
        self.setup_game_board()
        
        # 점수 표시
        self.setup_score_display()
        
        # 컨트롤 버튼들
        self.setup_control_buttons()
        
        # 상태 바
        self.setup_status_bar()
        
        # 초기 게임 상태 설정 (UI 업데이트 없이)
        self.reset_game_state_only()
        
    def setup_styles(self):
        """GUI 스타일을 설정합니다."""
        self.button_style = {
            'font': ('Helvetica', 32, 'bold'),
            'width': 5,
            'height': 2,
            'relief': 'solid',
            'borderwidth': 2,
            'bg': 'white',
            'fg': 'black',
            'activebackground': 'lightgray',
            'activeforeground': 'black',
            'highlightbackground': 'white',
            'highlightcolor': 'black'
        }
        
    def setup_mode_selection(self):
        """게임 모드 선택 UI를 설정합니다."""
        mode_frame = tk.Frame(self.main_frame, bg='white')
        mode_frame.pack(pady=(0, 15))
        
        tk.Label(
            mode_frame, 
            text="게임 모드:", 
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='black'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.mode_var = tk.StringVar(value="1")
        
        modes = [
            ("플레이어 vs 플레이어", "1"),
            ("플레이어 vs AI (쉬움)", "2"),
            ("플레이어 vs AI (어려움)", "3")
        ]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                font=('Arial', 10),
                bg='white',
                fg='black',
                command=self.change_game_mode
            ).pack(side=tk.LEFT, padx=5)
    
    def setup_player_display(self):
        """현재 플레이어 표시 UI를 설정합니다."""
        player_frame = tk.Frame(self.main_frame, bg='white')
        player_frame.pack(pady=(0, 15))
        
        self.player_label = tk.Label(
            player_frame,
            text=f"현재 차례: {self.current_player}",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='black'
        )
        self.player_label.pack()
        
    def setup_game_board(self):
        """게임 보드 UI를 설정합니다."""
        board_frame = tk.Frame(self.main_frame, bg='white')
        board_frame.pack(pady=(0, 20))
        
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                board_frame,
                text="",
                command=lambda idx=i: self.make_move(idx),
                **self.button_style
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(btn)
    
    def setup_score_display(self):
        """점수 표시 UI를 설정합니다."""
        score_frame = tk.Frame(self.main_frame, bg='white')
        score_frame.pack(pady=(0, 15))
        
        tk.Label(
            score_frame,
            text="📊 점수",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='black'
        ).pack()
        
        score_info_frame = tk.Frame(score_frame, bg='white')
        score_info_frame.pack()
        
        self.score_labels = {}
        
        # X 플레이어 점수
        x_frame = tk.Frame(score_info_frame, bg='white')
        x_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(x_frame, text="플레이어 X", font=('Arial', 10, 'bold'), fg='black', bg='white').pack()
        self.score_labels['X'] = tk.Label(x_frame, text="0승", font=('Arial', 10), bg='white', fg='black')
        self.score_labels['X'].pack()
        
        # 무승부 점수
        draw_frame = tk.Frame(score_info_frame, bg='white')
        draw_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(draw_frame, text="무승부", font=('Arial', 10, 'bold'), bg='white', fg='black').pack()
        self.score_labels['draws'] = tk.Label(draw_frame, text="0회", font=('Arial', 10), bg='white', fg='black')
        self.score_labels['draws'].pack()
        
        # O 플레이어 점수
        o_frame = tk.Frame(score_info_frame, bg='white')
        o_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(o_frame, text="플레이어 O", font=('Arial', 10, 'bold'), fg='black', bg='white').pack()
        self.score_labels['O'] = tk.Label(o_frame, text="0승", font=('Arial', 10), bg='white', fg='black')
        self.score_labels['O'].pack()
    
    def setup_control_buttons(self):
        """컨트롤 버튼들을 설정합니다."""
        control_frame = tk.Frame(self.main_frame, bg='white')
        control_frame.pack(pady=(0, 15))
        
        tk.Button(
            control_frame,
            text="🔄 새 게임",
            command=self.reset_game,
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='black',
            activebackground='#45a049',
            activeforeground='black',
            padx=25,
            pady=10,
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            control_frame,
            text="📊 점수 초기화",
            command=self.reset_score,
            font=('Arial', 16, 'bold'),
            bg='#ff9800',
            fg='black',
            activebackground='#e68900',
            activeforeground='black',
            padx=25,
            pady=10,
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=10)
        
    def setup_status_bar(self):
        """상태 바를 설정합니다."""
        self.status_label = tk.Label(
            self.main_frame,
            text="게임을 시작하세요!",
            font=('Arial', 10),
            bg='white',
            fg='black'
        )
        self.status_label.pack(side=tk.BOTTOM)
    
    def change_game_mode(self):
        """게임 모드를 변경합니다."""
        new_mode = int(self.mode_var.get())
        if new_mode != self.game_mode:  # 실제로 모드가 변경된 경우만 리셋
            self.game_mode = new_mode
            self.reset_game()
            
            mode_names = {1: "플레이어 vs 플레이어", 2: "플레이어 vs AI (쉬움)", 3: "플레이어 vs AI (어려움)"}
            self.status_label.config(text=f"모드 변경: {mode_names[self.game_mode]}")
    
    def make_move(self, position):
        """플레이어가 움직임을 만듭니다."""
        if self.game_over or self.board[position] != self.EMPTY_CELL or self.ai_thinking:
            return
        
        # 플레이어 움직임 실행
        self.board[position] = self.current_player
        self.update_button(position)
        
        # 게임 종료 확인
        if self.check_game_over():
            return
        
        # 플레이어 교대
        self.switch_player()
        
        # AI 턴인지 확인
        if self.game_mode in [2, 3] and self.current_player == self.PLAYER_O:
            self.ai_thinking = True
            self.status_label.config(text="🤖 AI가 생각 중...")
            
            # AI 움직임을 별도 스레드에서 실행 (UI 블로킹 방지)
            threading.Thread(target=self.ai_move, daemon=True).start()
    
    def ai_move(self):
        """AI가 움직임을 만듭니다."""
        time.sleep(1)  # AI 생각 시간 시뮬레이션
        
        # 게임이 이미 종료되었거나 AI 차례가 아니면 중단
        if self.game_over or not self.ai_thinking:
            return
        
        if self.game_mode == 2:
            position = self.get_ai_move()
        else:
            position = self.get_smart_ai_move()
        
        if position is not None and not self.game_over:
            # GUI 업데이트를 메인 스레드에서 실행
            self.root.after(0, self.execute_ai_move, position)
    
    def execute_ai_move(self, position):
        """AI 움직임을 실행합니다."""
        # 게임이 이미 종료되었으면 실행하지 않음
        if self.game_over or not self.ai_thinking:
            return
        
        # AI 상태 먼저 해제
        self.ai_thinking = False
            
        self.board[position] = self.current_player
        self.update_button(position)
        
        # 게임 종료 확인
        if self.check_game_over():
            return
        
        # 플레이어 교대
        self.switch_player()
        self.status_label.config(text="당신의 차례입니다!")
    
    def get_ai_move(self):
        """AI의 움직임을 결정합니다 (랜덤 전략)."""
        available_moves = [i for i, cell in enumerate(self.board) if cell == self.EMPTY_CELL]
        return random.choice(available_moves) if available_moves else None
    
    def get_smart_ai_move(self):
        """스마트 AI의 움직임을 결정합니다."""
        # 1. 승리 가능한 수 찾기
        for pattern in self.WINNING_PATTERNS:
            values = [self.board[i] for i in pattern]
            if values.count(self.PLAYER_O) == 2 and values.count(self.EMPTY_CELL) == 1:
                return pattern[values.index(self.EMPTY_CELL)]
        
        # 2. 상대방 승리 차단
        for pattern in self.WINNING_PATTERNS:
            values = [self.board[i] for i in pattern]
            if values.count(self.PLAYER_X) == 2 and values.count(self.EMPTY_CELL) == 1:
                return pattern[values.index(self.EMPTY_CELL)]
        
        # 3. 중앙 선택
        if self.board[4] == self.EMPTY_CELL:
            return 4
        
        # 4. 코너 선택
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == self.EMPTY_CELL]
        if available_corners:
            return random.choice(available_corners)
        
        # 5. 랜덤 선택
        return self.get_ai_move()
    
    def update_button(self, position):
        """버튼을 업데이트합니다."""
        btn = self.buttons[position]
        
        if self.board[position] == self.PLAYER_X:
            # X는 빨간색 배경에 흰색 텍스트로 확실히 보이게
            btn.config(
                text='X',
                fg='white',
                bg='red',
                font=('Helvetica', 40, 'bold'),
                state='disabled',
                disabledforeground='white'
            )
        elif self.board[position] == self.PLAYER_O:
            # O는 파란색 배경에 흰색 텍스트로 확실히 보이게
            btn.config(
                text='O',
                fg='white',
                bg='blue',
                font=('Helvetica', 30, 'bold'),
                state='disabled',
                disabledforeground='white'
            )
        else:
            # 빈 셀인 경우 기본 스타일 복원
            btn.config(
                text='',
                fg='black',
                bg='white',
                font=('Helvetica', 32, 'bold'),
                activebackground='lightgray',
                activeforeground='black',
                state='normal'
            )
    
    def check_winner(self):
        """승자를 확인합니다."""
        for pattern in self.WINNING_PATTERNS:
            if (self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != self.EMPTY_CELL):
                return self.board[pattern[0]]
        return None
    
    def is_board_full(self):
        """보드가 가득 찼는지 확인합니다."""
        return self.EMPTY_CELL not in self.board
    
    def check_game_over(self):
        """게임 종료를 확인합니다."""
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.highlight_winning_pattern()
            self.update_score(winner)
            messagebox.showinfo("게임 종료", f"🎉 플레이어 {winner}가 승리했습니다!")
            self.status_label.config(text=f"플레이어 {winner} 승리!")
            return True
        elif self.is_board_full():
            self.game_over = True
            self.update_score('draw')
            messagebox.showinfo("게임 종료", "🤝 무승부입니다!")
            self.status_label.config(text="무승부!")
            return True
        return False
    
    def highlight_winning_pattern(self):
        """승리 패턴을 하이라이트합니다."""
        winner = self.check_winner()
        if not winner:
            return
        
        for pattern in self.WINNING_PATTERNS:
            if (self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] == winner):
                for pos in pattern:
                    if winner == self.PLAYER_X:
                        self.buttons[pos].config(
                            text='X',
                            bg='yellow',  # 노란색 배경으로 강조
                            fg='red',     # 빨간색 텍스트
                            font=('Helvetica', 45, 'bold'),
                            disabledforeground='red'
                        )
                    else:
                        self.buttons[pos].config(
                            text='O',
                            bg='yellow',  # 노란색 배경으로 강조
                            fg='blue',    # 파란색 텍스트
                            font=('Helvetica', 35, 'bold'),
                            disabledforeground='blue'
                        )
                break
    
    def switch_player(self):
        """현재 플레이어를 교대합니다."""
        self.current_player = self.PLAYER_O if self.current_player == self.PLAYER_X else self.PLAYER_X
        self.update_player_display()
    
    def update_player_display(self):
        """현재 플레이어 표시를 업데이트합니다."""
        self.player_label.config(
            text=f"현재 차례: {self.current_player}",
            fg='black'
        )
    
    def update_score(self, result):
        """점수를 업데이트합니다."""
        if result in [self.PLAYER_X, self.PLAYER_O]:
            self.score[result] += 1
        else:
            self.score['draws'] += 1
        
        # GUI 점수 표시 업데이트
        self.score_labels['X'].config(text=f"{self.score[self.PLAYER_X]}승")
        self.score_labels['O'].config(text=f"{self.score[self.PLAYER_O]}승")
        self.score_labels['draws'].config(text=f"{self.score['draws']}회")
    
    def reset_game_state_only(self):
        """게임 상태만 리셋합니다 (UI 업데이트 없음)."""
        self.board = [self.EMPTY_CELL for _ in range(9)]
        self.current_player = self.PLAYER_X
        self.game_over = False
        self.ai_thinking = False
    
    def reset_game(self):
        """게임을 리셋합니다."""
        self.reset_game_state_only()
        
        # 버튼 리셋 - update_button 호출하지 않고 직접 리셋
        for btn in self.buttons:
            btn.config(
                text="",
                bg='white',
                fg='black',
                activebackground='lightgray',
                state='normal'
            )
        
        self.update_player_display()
        self.status_label.config(text="새 게임이 시작되었습니다!")
    
    def reset_score(self):
        """점수를 초기화합니다."""
        self.score = {self.PLAYER_X: 0, self.PLAYER_O: 0, 'draws': 0}
        self.score_labels['X'].config(text="0승")
        self.score_labels['O'].config(text="0승")
        self.score_labels['draws'].config(text="0회")
        self.status_label.config(text="점수가 초기화되었습니다!")
    
    def run(self):
        """게임을 실행합니다."""
        self.root.mainloop()


def main():
    """메인 함수"""
    try:
        game = TicTacToeGUI()
        game.run()
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
