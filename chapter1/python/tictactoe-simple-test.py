#!/usr/bin/env python3
"""
간단한 틱택토 GUI 테스트 버전
기본 기능만 구현하여 문제점 파악
"""

import tkinter as tk
from tkinter import messagebox

class SimpleTicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        
        self.root = tk.Tk()
        self.root.title("간단한 틱택토")
        self.root.geometry("400x500")
        self.root.configure(bg='white')
        
        self.setup_gui()
        
    def setup_gui(self):
        # 제목
        title = tk.Label(
            self.root, 
            text="틱택토 테스트", 
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='black'
        )
        title.pack(pady=10)
        
        # 현재 플레이어 표시
        self.player_label = tk.Label(
            self.root,
            text=f"현재 차례: {self.current_player}",
            font=('Arial', 14),
            bg='white',
            fg='black'
        )
        self.player_label.pack(pady=5)
        
        # 게임 보드 프레임
        board_frame = tk.Frame(self.root, bg='white')
        board_frame.pack(pady=20)
        
        # 3x3 버튼 생성
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                board_frame,
                text='',
                font=('Arial', 24, 'bold'),
                width=4,
                height=2,
                bg='lightgray',
                fg='black',
                command=lambda idx=i: self.button_click(idx)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(btn)
        
        # 새 게임 버튼
        reset_btn = tk.Button(
            self.root,
            text="새 게임",
            font=('Arial', 12),
            command=self.reset_game,
            bg='lightblue',
            fg='black'
        )
        reset_btn.pack(pady=10)
        
    def button_click(self, position):
        """버튼 클릭 처리"""
        print(f"버튼 {position} 클릭됨")  # 디버그용
        
        if self.game_over or self.board[position] != ' ':
            print("이미 선택된 위치이거나 게임 종료")
            return
            
        # 보드에 플레이어 마크 설정
        self.board[position] = self.current_player
        print(f"보드 상태: {self.board}")  # 디버그용
        
        # 버튼 업데이트
        if self.current_player == 'X':
            self.buttons[position].config(
                text='X',
                bg='red',
                fg='white',
                state='disabled'
            )
        else:
            self.buttons[position].config(
                text='O',
                bg='blue',
                fg='white',
                state='disabled'
            )
            
        # 승리 확인
        if self.check_winner():
            messagebox.showinfo("게임 종료", f"{self.current_player} 승리!")
            self.game_over = True
            return
            
        # 무승부 확인
        if ' ' not in self.board:
            messagebox.showinfo("게임 종료", "무승부!")
            self.game_over = True
            return
            
        # 플레이어 교대
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.player_label.config(text=f"현재 차례: {self.current_player}")
        
    def check_winner(self):
        """승리 확인"""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 행
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 열
            [0, 4, 8], [2, 4, 6]              # 대각선
        ]
        
        for pattern in win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] == 
                self.board[pattern[2]] != ' '):
                return True
        return False
        
    def reset_game(self):
        """게임 리셋"""
        print("게임 리셋")  # 디버그용
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        
        for btn in self.buttons:
            btn.config(
                text='',
                bg='lightgray',
                fg='black',
                state='normal'
            )
            
        self.player_label.config(text=f"현재 차례: {self.current_player}")
        
    def run(self):
        """게임 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    game = SimpleTicTacToe()
    game.run()
