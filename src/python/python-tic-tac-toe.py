#!/usr/bin/env python3
"""
Tic-Tac-Toe Game (틱택토 게임)
CLI로 구동되는 간단한 틱택토 게임입니다.

게임 규칙:
- 3x3 보드에서 두 명의 플레이어가 번갈아가며 O와 X를 놓습니다
- 가로, 세로, 대각선 중 하나를 먼저 완성하는 플레이어가 승리합니다
- 모든 칸이 채워져도 승자가 없으면 무승부입니다

사용법:
python python-tic-tac-toe.py
"""

import os
import sys


class TicTacToe:
    """틱택토 게임 클래스"""
    
    def __init__(self):
        """게임 초기화"""
        self.board = [' ' for _ in range(9)]  # 3x3 보드를 1차원 리스트로 표현
        self.current_player = 'X'  # 현재 플레이어 (X가 먼저 시작)
        self.game_over = False
        self.winner = None
        
    def clear_screen(self):
        """화면 지우기 (터미널 정리)"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_board(self):
        """게임 보드 출력"""
        print("\n" + "="*25)
        print("     TIC-TAC-TOE GAME")
        print("="*25)
        print()
        print("     |     |     ")
        print(f"  {self.board[0]}  |  {self.board[1]}  |  {self.board[2]}  ")
        print("_____|_____|_____")
        print("     |     |     ")
        print(f"  {self.board[3]}  |  {self.board[4]}  |  {self.board[5]}  ")
        print("_____|_____|_____")
        print("     |     |     ")
        print(f"  {self.board[6]}  |  {self.board[7]}  |  {self.board[8]}  ")
        print("     |     |     ")
        print()
        print("위치 번호:")
        print("  1  |  2  |  3  ")
        print("_____|_____|_____")
        print("  4  |  5  |  6  ")
        print("_____|_____|_____")
        print("  7  |  8  |  9  ")
        print()
    
    def get_player_move(self):
        """플레이어의 이동 입력 받기"""
        while True:
            try:
                move = input(f"플레이어 {self.current_player}의 차례입니다. 위치를 선택하세요 (1-9): ").strip()
                
                if move.lower() in ['quit', 'exit', 'q']:
                    print("게임을 종료합니다.")
                    sys.exit(0)
                
                move = int(move)
                
                if move < 1 or move > 9:
                    print("1부터 9 사이의 숫자를 입력해주세요.")
                    continue
                
                if self.board[move - 1] != ' ':
                    print("이미 선택된 위치입니다. 다른 위치를 선택해주세요.")
                    continue
                
                return move - 1  # 0-based 인덱스로 변환
                
            except ValueError:
                print("올바른 숫자를 입력해주세요.")
            except KeyboardInterrupt:
                print("\n게임을 종료합니다.")
                sys.exit(0)
    
    def make_move(self, position):
        """보드에 플레이어의 표시를 놓기"""
        self.board[position] = self.current_player
    
    def check_winner(self):
        """승리 조건 검사"""
        # 승리 조건들 (가로, 세로, 대각선)
        winning_combinations = [
            [0, 1, 2],  # 첫 번째 가로
            [3, 4, 5],  # 두 번째 가로
            [6, 7, 8],  # 세 번째 가로
            [0, 3, 6],  # 첫 번째 세로
            [1, 4, 7],  # 두 번째 세로
            [2, 5, 8],  # 세 번째 세로
            [0, 4, 8],  # 대각선 (왼쪽 위 -> 오른쪽 아래)
            [2, 4, 6]   # 대각선 (오른쪽 위 -> 왼쪽 아래)
        ]
        
        for combination in winning_combinations:
            if (self.board[combination[0]] == self.board[combination[1]] == 
                self.board[combination[2]] != ' '):
                self.winner = self.board[combination[0]]
                self.game_over = True
                return True
        
        # 무승부 검사 (모든 칸이 채워졌는지)
        if ' ' not in self.board:
            self.game_over = True
            return False
        
        return False
    
    def switch_player(self):
        """플레이어 교체"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def reset_game(self):
        """게임 초기화"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def play_game(self):
        """메인 게임 루프"""
        print("틱택토 게임에 오신 것을 환영합니다!")
        print("게임을 종료하려면 'quit', 'exit', 또는 'q'를 입력하세요.")
        print("게임을 재시작하려면 'restart' 또는 'r'를 입력하세요.")
        input("게임을 시작하려면 Enter를 누르세요...")
        
        while True:
            self.clear_screen()
            self.display_board()
            
            if self.game_over:
                if self.winner:
                    print(f"🎉 축하합니다! 플레이어 {self.winner}가 승리했습니다!")
                else:
                    print("🤝 무승부입니다!")
                
                print("\n게임 옵션:")
                print("1. 새 게임 시작 (restart 또는 r)")
                print("2. 게임 종료 (quit 또는 q)")
                
                while True:
                    choice = input("선택하세요: ").strip().lower()
                    if choice in ['restart', 'r', '1']:
                        self.reset_game()
                        break
                    elif choice in ['quit', 'exit', 'q', '2']:
                        print("게임을 종료합니다. 즐거운 시간이었습니다!")
                        return
                    else:
                        print("올바른 선택을 해주세요 (restart/r 또는 quit/q)")
            else:
                move = self.get_player_move()
                self.make_move(move)
                
                if self.check_winner():
                    continue
                
                self.switch_player()


def main():
    """메인 함수"""
    try:
        game = TicTacToe()
        game.play_game()
    except KeyboardInterrupt:
        print("\n\n게임이 중단되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
