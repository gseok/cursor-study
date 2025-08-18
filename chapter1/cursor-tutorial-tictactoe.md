# Python 틱택토 게임 만들기 - Cursor 튜토리얼

이 튜토리얼은 Python을 사용하여 콘솔 기반 틱택토 게임을 단계별로 만드는 방법을 안내합니다.

## 목표
- Python 기본 문법 학습
- 게임 로직 구현
- 사용자 입력 처리
- 조건문과 반복문 활용
- 함수 설계 및 구현

## 전체 단계 개요

### Step 1: 프로젝트 초기 설정
### Step 2: 게임 보드 생성 및 출력
### Step 3: 플레이어 입력 처리
### Step 4: 승리 조건 구현
### Step 5: 게임 메인 루프 작성
### Step 6: 고급 기능 추가 (선택사항)

---

## Step 1: 프로젝트 초기 설정

### 목표
- 새로운 Python 파일 생성
- 기본 게임 변수 정의
- 프로젝트 구조 이해

### 작업 내용

1. **새 파일 생성**
   ```python
   # tictactoe.py
   
   # 게임 보드 초기화 (3x3 그리드)
   board = [' ' for _ in range(9)]
   
   # 현재 플레이어 (X부터 시작)
   current_player = 'X'
   
   # 게임 상태
   game_over = False
   ```

2. **상수 정의**
   ```python
   # 게임 설정
   BOARD_SIZE = 3
   EMPTY_CELL = ' '
   PLAYER_X = 'X'
   PLAYER_O = 'O'
   ```

### 학습 포인트
- 리스트 컴프리헨션 사용법
- 전역 변수와 상수의 차이
- Python 네이밍 컨벤션

---

## Step 2: 게임 보드 생성 및 출력

### 목표
- 3x3 게임 보드를 시각적으로 표현
- 보드 상태를 콘솔에 출력하는 함수 작성

### 작업 내용

1. **보드 출력 함수 구현**
   ```python
   def print_board():
       """게임 보드를 콘솔에 출력합니다."""
       print("\n   |   |   ")
       print(f" {board[0]} | {board[1]} | {board[2]} ")
       print("___|___|___")
       print("   |   |   ")
       print(f" {board[3]} | {board[4]} | {board[5]} ")
       print("___|___|___")
       print("   |   |   ")
       print(f" {board[6]} | {board[7]} | {board[8]} ")
       print("   |   |   \n")
   ```

2. **보드 위치 안내 함수**
   ```python
   def print_board_positions():
       """보드 위치 번호를 안내합니다."""
       print("\n보드 위치 번호:")
       print("   |   |   ")
       print(" 1 | 2 | 3 ")
       print("___|___|___")
       print("   |   |   ")
       print(" 4 | 5 | 6 ")
       print("___|___|___")
       print("   |   |   ")
       print(" 7 | 8 | 9 ")
       print("   |   |   \n")
   ```

### 학습 포인트
- 함수 정의와 docstring 작성
- f-string을 이용한 문자열 포맷팅
- 콘솔 출력 디자인

---

## Step 3: 플레이어 입력 처리

### 목표
- 사용자로부터 유효한 입력 받기
- 입력 검증 로직 구현
- 게임 보드에 플레이어 마크 배치

### 작업 내용

1. **입력 검증 함수**
   ```python
   def is_valid_move(position):
       """입력된 위치가 유효한지 확인합니다."""
       try:
           pos = int(position)
           return 1 <= pos <= 9 and board[pos - 1] == EMPTY_CELL
       except ValueError:
           return False
   ```

2. **플레이어 입력 처리 함수**
   ```python
   def get_player_move():
       """플레이어로부터 유효한 움직임을 입력받습니다."""
       while True:
           try:
               move = input(f"플레이어 {current_player}의 차례입니다. 위치를 선택하세요 (1-9): ")
               if is_valid_move(move):
                   return int(move) - 1  # 0-based 인덱스로 변환
               else:
                   print("잘못된 입력입니다. 1-9 사이의 빈 위치를 선택해주세요.")
           except KeyboardInterrupt:
               print("\n게임을 종료합니다.")
               exit()
   ```

3. **보드 업데이트 함수**
   ```python
   def make_move(position, player):
       """보드에 플레이어의 마크를 배치합니다."""
       board[position] = player
   ```

### 학습 포인트
- try-except를 이용한 예외 처리
- while 루프를 이용한 입력 검증
- 사용자 친화적인 오류 메시지

---

## Step 4: 승리 조건 구현

### 목표
- 승리 조건 확인 로직 구현
- 무승부 상황 처리
- 게임 종료 조건 판단

### 작업 내용

1. **승리 패턴 정의**
   ```python
   # 승리 가능한 패턴들 (행, 열, 대각선)
   WINNING_PATTERNS = [
       [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 행
       [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 열
       [0, 4, 8], [2, 4, 6]              # 대각선
   ]
   ```

2. **승리 확인 함수**
   ```python
   def check_winner():
       """현재 보드 상태에서 승자가 있는지 확인합니다."""
       for pattern in WINNING_PATTERNS:
           if (board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != EMPTY_CELL):
               return board[pattern[0]]
       return None
   ```

3. **무승부 확인 함수**
   ```python
   def is_board_full():
       """보드가 가득 찼는지 확인합니다."""
       return EMPTY_CELL not in board
   ```

4. **게임 종료 확인 함수**
   ```python
   def check_game_over():
       """게임이 종료되었는지 확인합니다."""
       winner = check_winner()
       if winner:
           print_board()
           print(f"🎉 플레이어 {winner}가 승리했습니다!")
           return True
       elif is_board_full():
           print_board()
           print("🤝 무승부입니다!")
           return True
       return False
   ```

### 학습 포인트
- 2차원 리스트의 1차원 표현
- 논리 연산자 활용
- 조건문 중첩 사용

---

## Step 5: 게임 메인 루프 작성

### 목표
- 전체 게임 플로우 구현
- 플레이어 턴 교대 로직
- 게임 재시작 기능

### 작업 내용

1. **플레이어 교대 함수**
   ```python
   def switch_player():
       """현재 플레이어를 교대합니다."""
       global current_player
       current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
   ```

2. **게임 초기화 함수**
   ```python
   def reset_game():
       """게임을 초기 상태로 리셋합니다."""
       global board, current_player, game_over
       board = [EMPTY_CELL for _ in range(9)]
       current_player = PLAYER_X
       game_over = False
   ```

3. **메인 게임 루프**
   ```python
   def play_game():
       """메인 게임 루프를 실행합니다."""
       print("🎮 틱택토 게임에 오신 것을 환영합니다!")
       print_board_positions()
       
       while not game_over:
           print_board()
           
           # 플레이어 입력 받기
           position = get_player_move()
           
           # 보드에 마크 배치
           make_move(position, current_player)
           
           # 게임 종료 확인
           if check_game_over():
               break
           
           # 플레이어 교대
           switch_player()
   ```

4. **프로그램 진입점**
   ```python
   def main():
       """프로그램의 메인 함수입니다."""
       while True:
           reset_game()
           play_game()
           
           # 게임 재시작 여부 확인
           play_again = input("\n다시 플레이하시겠습니까? (y/n): ").lower()
           if play_again != 'y' and play_again != 'yes':
               print("게임을 종료합니다. 감사합니다!")
               break
   
   if __name__ == "__main__":
       main()
   ```

### 학습 포인트
- global 키워드 사용법
- 프로그램 구조화
- `if __name__ == "__main__":` 관용구

---

## Step 6: 고급 기능 추가 (선택사항)

### 목표
- AI 플레이어 구현
- 점수 시스템 추가
- 게임 통계 기능

### 작업 내용

1. **간단한 AI 플레이어**
   ```python
   import random
   
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
       
       # 4. 랜덤 선택
       return get_ai_move()
   ```

2. **점수 시스템**
   ```python
   # 점수 변수
   score = {PLAYER_X: 0, PLAYER_O: 0, 'draws': 0}
   
   def update_score(result):
       """게임 결과에 따라 점수를 업데이트합니다."""
       if result in [PLAYER_X, PLAYER_O]:
           score[result] += 1
       else:
           score['draws'] += 1
   
   def print_score():
       """현재 점수를 출력합니다."""
       print(f"\n📊 현재 점수:")
       print(f"플레이어 X: {score[PLAYER_X]}승")
       print(f"플레이어 O: {score[PLAYER_O]}승")
       print(f"무승부: {score['draws']}회\n")
   ```

3. **게임 모드 선택**
   ```python
   def choose_game_mode():
       """게임 모드를 선택합니다."""
       print("게임 모드를 선택해주세요:")
       print("1. 플레이어 vs 플레이어")
       print("2. 플레이어 vs AI (쉬움)")
       print("3. 플레이어 vs AI (어려움)")
       
       while True:
           choice = input("선택 (1-3): ")
           if choice in ['1', '2', '3']:
               return int(choice)
           print("잘못된 선택입니다. 1-3 중에서 선택해주세요.")
   ```

### 학습 포인트
- 모듈 import 사용법
- 딕셔너리 자료형 활용
- 알고리즘 구현 (미니맥스 개념)

---

## 완성된 코드 구조

```
tictactoe.py
├── 상수 정의
├── 전역 변수
├── 보드 관련 함수
│   ├── print_board()
│   ├── print_board_positions()
│   └── reset_game()
├── 입력 처리 함수
│   ├── is_valid_move()
│   ├── get_player_move()
│   └── make_move()
├── 게임 로직 함수
│   ├── check_winner()
│   ├── is_board_full()
│   ├── check_game_over()
│   └── switch_player()
├── AI 관련 함수 (선택사항)
│   ├── get_ai_move()
│   └── get_smart_ai_move()
├── 점수 시스템 (선택사항)
│   ├── update_score()
│   └── print_score()
├── 게임 실행 함수
│   ├── play_game()
│   └── main()
└── 프로그램 진입점
```

---

## 추가 학습 과제

### 초급
1. 게임 보드 디자인 개선
2. 컬러 출력 추가 (colorama 라이브러리)
3. 입력 검증 강화

### 중급
1. 게임 기록 파일 저장/불러오기
2. 다양한 AI 난이도 구현
3. 웹 기반 인터페이스 (Flask)

### 고급
1. 미니맥스 알고리즘 구현
2. 게임 트리 시각화
3. 멀티플레이어 네트워크 게임

---

## 참고 자료

- [Python 공식 문서](https://docs.python.org/3/)
- [Python 게임 개발 가이드](https://realpython.com/python-game-development/)
- [알고리즘 학습 자료](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/)

---

## 마무리

이 튜토리얼을 통해 Python의 기본 문법부터 게임 로직 구현까지 단계별로 학습할 수 있습니다. 각 단계를 차근차근 따라하며 코딩 실력을 향상시켜보세요!

🎯 **학습 목표 달성 체크리스트:**
- [ ] Python 기본 문법 이해
- [ ] 함수 설계 및 구현
- [ ] 조건문과 반복문 활용
- [ ] 사용자 입력 처리
- [ ] 게임 로직 구현
- [ ] 예외 처리
- [ ] 코드 구조화
