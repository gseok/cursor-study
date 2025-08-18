#!/usr/bin/env python3
"""
틱택토 게임 - CLI 기반 Python 구현
Cursor 튜토리얼 기반으로 작성된 완전한 틱택토 게임
"""

import random
import os
import sys

# 게임 설정 상수
BOARD_SIZE = 3
EMPTY_CELL = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

# 승리 가능한 패턴들 (행, 열, 대각선)
WINNING_PATTERNS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 행
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 열
    [0, 4, 8], [2, 4, 6]              # 대각선
]

# 게임 상태 변수
board = [EMPTY_CELL for _ in range(9)]
current_player = PLAYER_X
game_over = False
game_mode = 1  # 1: PvP, 2: PvAI(쉬움), 3: PvAI(어려움)
score = {PLAYER_X: 0, PLAYER_O: 0, 'draws': 0}


def clear_screen():
    """화면을 지웁니다."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome():
    """게임 시작 메시지를 출력합니다."""
    print("🎮 " + "="*50)
    print("🎮 " + " "*15 + "틱택토 게임" + " "*15)
    print("🎮 " + "="*50)
    print()


def print_board():
    """게임 보드를 콘솔에 출력합니다."""
    print("\n현재 게임 보드:")
    print("     |     |     ")
    print(f"  {board[0]}  |  {board[1]}  |  {board[2]}  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print(f"  {board[3]}  |  {board[4]}  |  {board[5]}  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print(f"  {board[6]}  |  {board[7]}  |  {board[8]}  ")
    print("     |     |     \n")


def print_board_positions():
    """보드 위치 번호를 안내합니다."""
    print("보드 위치 번호 참고:")
    print("     |     |     ")
    print("  1  |  2  |  3  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print("  4  |  5  |  6  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print("  7  |  8  |  9  ")
    print("     |     |     \n")


def is_valid_move(position):
    """입력된 위치가 유효한지 확인합니다."""
    try:
        pos = int(position)
        return 1 <= pos <= 9 and board[pos - 1] == EMPTY_CELL
    except ValueError:
        return False


def get_player_move():
    """플레이어로부터 유효한 움직임을 입력받습니다."""
    while True:
        try:
            move = input(f"플레이어 {current_player}의 차례입니다. 위치를 선택하세요 (1-9): ")
            if move.lower() in ['quit', 'exit', 'q']:
                print("\n게임을 종료합니다.")
                sys.exit(0)
            
            if is_valid_move(move):
                return int(move) - 1  # 0-based 인덱스로 변환
            else:
                print("❌ 잘못된 입력입니다. 1-9 사이의 빈 위치를 선택해주세요.")
        except KeyboardInterrupt:
            print("\n\n게임을 종료합니다.")
            sys.exit(0)


def get_ai_move():
    """AI의 움직임을 결정합니다 (랜덤 전략)."""
    available_moves = [i for i, cell in enumerate(board) if cell == EMPTY_CELL]
    return random.choice(available_moves) if available_moves else None


def get_smart_ai_move():
    """스마트 AI의 움직임을 결정합니다."""
    # 1. 승리 가능한 수 찾기
    for pattern in WINNING_PATTERNS:
        values = [board[i] for i in pattern]
        if values.count(PLAYER_O) == 2 and values.count(EMPTY_CELL) == 1:
            return pattern[values.index(EMPTY_CELL)]
    
    # 2. 상대방 승리 차단
    for pattern in WINNING_PATTERNS:
        values = [board[i] for i in pattern]
        if values.count(PLAYER_X) == 2 and values.count(EMPTY_CELL) == 1:
            return pattern[values.index(EMPTY_CELL)]
    
    # 3. 중앙 선택
    if board[4] == EMPTY_CELL:
        return 4
    
    # 4. 코너 선택
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if board[i] == EMPTY_CELL]
    if available_corners:
        return random.choice(available_corners)
    
    # 5. 랜덤 선택
    return get_ai_move()


def make_move(position, player):
    """보드에 플레이어의 마크를 배치합니다."""
    board[position] = player


def check_winner():
    """현재 보드 상태에서 승자가 있는지 확인합니다."""
    for pattern in WINNING_PATTERNS:
        if (board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != EMPTY_CELL):
            return board[pattern[0]]
    return None


def is_board_full():
    """보드가 가득 찼는지 확인합니다."""
    return EMPTY_CELL not in board


def check_game_over():
    """게임이 종료되었는지 확인합니다."""
    winner = check_winner()
    if winner:
        print_board()
        print(f"🎉 플레이어 {winner}가 승리했습니다!")
        update_score(winner)
        return True
    elif is_board_full():
        print_board()
        print("🤝 무승부입니다!")
        update_score('draw')
        return True
    return False


def switch_player():
    """현재 플레이어를 교대합니다."""
    global current_player
    current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X


def reset_game():
    """게임을 초기 상태로 리셋합니다."""
    global board, current_player, game_over
    board = [EMPTY_CELL for _ in range(9)]
    current_player = PLAYER_X
    game_over = False


def update_score(result):
    """게임 결과에 따라 점수를 업데이트합니다."""
    if result in [PLAYER_X, PLAYER_O]:
        score[result] += 1
    else:
        score['draws'] += 1


def print_score():
    """현재 점수를 출력합니다."""
    print("\n📊 현재 점수:")
    print(f"   플레이어 X: {score[PLAYER_X]}승")
    print(f"   플레이어 O: {score[PLAYER_O]}승")
    print(f"   무승부: {score['draws']}회")
    print("-" * 30)


def choose_game_mode():
    """게임 모드를 선택합니다."""
    print("\n🎯 게임 모드를 선택해주세요:")
    print("   1. 플레이어 vs 플레이어")
    print("   2. 플레이어 vs AI (쉬움)")
    print("   3. 플레이어 vs AI (어려움)")
    
    while True:
        choice = input("\n선택 (1-3): ")
        if choice in ['1', '2', '3']:
            return int(choice)
        print("❌ 잘못된 선택입니다. 1-3 중에서 선택해주세요.")


def play_game():
    """메인 게임 루프를 실행합니다."""
    global game_mode
    
    print_welcome()
    game_mode = choose_game_mode()
    
    print("\n💡 게임 중 'q', 'quit', 'exit'를 입력하면 종료됩니다.")
    print_board_positions()
    
    while not game_over:
        print_board()
        
        # AI 턴인지 확인
        is_ai_turn = (game_mode in [2, 3] and current_player == PLAYER_O)
        
        if is_ai_turn:
            print(f"🤖 AI(플레이어 {current_player})가 생각 중...")
            import time
            time.sleep(1)  # AI가 생각하는 시간 시뮬레이션
            
            if game_mode == 2:  # 쉬운 AI
                position = get_ai_move()
            else:  # 어려운 AI
                position = get_smart_ai_move()
            
            if position is not None:
                print(f"🤖 AI가 위치 {position + 1}을 선택했습니다.")
                make_move(position, current_player)
        else:
            # 플레이어 입력 받기
            position = get_player_move()
            make_move(position, current_player)
        
        # 게임 종료 확인
        if check_game_over():
            break
        
        # 플레이어 교대
        switch_player()


def main():
    """프로그램의 메인 함수입니다."""
    try:
        while True:
            reset_game()
            play_game()
            print_score()
            
            # 게임 재시작 여부 확인
            print("\n🔄 다시 플레이하시겠습니까?")
            play_again = input("   (y/yes: 재시작, n/no: 종료, m/mode: 모드 변경): ").lower().strip()
            
            if play_again in ['n', 'no', 'quit', 'exit']:
                break
            elif play_again in ['m', 'mode']:
                clear_screen()
                continue
            elif play_again not in ['y', 'yes', '']:
                print("❌ 잘못된 입력입니다. 게임을 종료합니다.")
                break
            
            clear_screen()
        
        print("\n🎮 게임을 종료합니다. 즐거운 시간이었습니다!")
        print_score()
        print("👋 안녕히 가세요!")
        
    except KeyboardInterrupt:
        print("\n\n🎮 게임이 중단되었습니다.")
        print("👋 안녕히 가세요!")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        print("게임을 종료합니다.")


if __name__ == "__main__":
    main()
