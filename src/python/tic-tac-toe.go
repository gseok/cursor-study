package main

import (
	"bufio"
	"fmt"
	"os"
	"os/signal"
	"strconv"
	"strings"
)

// TicTacToe 구조체는 틱택토 게임의 상태를 관리합니다
type TicTacToe struct {
	board         [9]string // 3x3 보드를 1차원 배열로 표현
	currentPlayer string    // 현재 플레이어 (X 또는 O)
	gameOver      bool      // 게임 종료 여부
	winner        string    // 승자 (X, O, 또는 빈 문자열)
}

// NewTicTacToe는 새로운 틱택토 게임 인스턴스를 생성합니다
func NewTicTacToe() *TicTacToe {
	return &TicTacToe{
		board:         [9]string{" ", " ", " ", " ", " ", " ", " ", " ", " "},
		currentPlayer: "X", // X가 먼저 시작
		gameOver:      false,
		winner:        "",
	}
}

// clearScreen은 터미널 화면을 지웁니다
func (t *TicTacToe) clearScreen() {
	// ANSI escape sequence를 사용하여 화면 지우기
	fmt.Print("\033[2J\033[H")
}

// displayBoard는 게임 보드를 출력합니다
func (t *TicTacToe) displayBoard() {
	fmt.Println("\n" + strings.Repeat("=", 25))
	fmt.Println("     TIC-TAC-TOE GAME")
	fmt.Println(strings.Repeat("=", 25))
	fmt.Println()
	fmt.Println("     |     |     ")
	fmt.Printf("  %s  |  %s  |  %s  \n", t.board[0], t.board[1], t.board[2])
	fmt.Println("_____|_____|_____")
	fmt.Println("     |     |     ")
	fmt.Printf("  %s  |  %s  |  %s  \n", t.board[3], t.board[4], t.board[5])
	fmt.Println("_____|_____|_____")
	fmt.Println("     |     |     ")
	fmt.Printf("  %s  |  %s  |  %s  \n", t.board[6], t.board[7], t.board[8])
	fmt.Println("     |     |     ")
	fmt.Println()
	fmt.Println("위치 번호:")
	fmt.Println("  1  |  2  |  3  ")
	fmt.Println("_____|_____|_____")
	fmt.Println("  4  |  5  |  6  ")
	fmt.Println("_____|_____|_____")
	fmt.Println("  7  |  8  |  9  ")
	fmt.Println()
}

// getPlayerMove는 플레이어의 이동 입력을 받습니다
func (t *TicTacToe) getPlayerMove() (int, error) {
	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Printf("플레이어 %s의 차례입니다. 위치를 선택하세요 (1-9): ", t.currentPlayer)
		input, err := reader.ReadString('\n')
		if err != nil {
			return 0, fmt.Errorf("입력 읽기 오류: %v", err)
		}

		input = strings.TrimSpace(input)

		// 종료 명령어 확인
		if strings.ToLower(input) == "quit" || strings.ToLower(input) == "exit" || strings.ToLower(input) == "q" {
			fmt.Println("게임을 종료합니다.")
			os.Exit(0)
		}

		// 숫자 변환
		move, err := strconv.Atoi(input)
		if err != nil {
			fmt.Println("올바른 숫자를 입력해주세요.")
			continue
		}

		// 범위 확인
		if move < 1 || move > 9 {
			fmt.Println("1부터 9 사이의 숫자를 입력해주세요.")
			continue
		}

		// 이미 선택된 위치인지 확인
		if t.board[move-1] != " " {
			fmt.Println("이미 선택된 위치입니다. 다른 위치를 선택해주세요.")
			continue
		}

		return move - 1, nil // 0-based 인덱스로 변환
	}
}

// makeMove는 보드에 플레이어의 표시를 놓습니다
func (t *TicTacToe) makeMove(position int) {
	t.board[position] = t.currentPlayer
}

// checkWinner는 승리 조건을 검사합니다
func (t *TicTacToe) checkWinner() bool {
	// 승리 조건들 (가로, 세로, 대각선)
	winningCombinations := [8][3]int{
		{0, 1, 2}, // 첫 번째 가로
		{3, 4, 5}, // 두 번째 가로
		{6, 7, 8}, // 세 번째 가로
		{0, 3, 6}, // 첫 번째 세로
		{1, 4, 7}, // 두 번째 세로
		{2, 5, 8}, // 세 번째 세로
		{0, 4, 8}, // 대각선 (왼쪽 위 -> 오른쪽 아래)
		{2, 4, 6}, // 대각선 (오른쪽 위 -> 왼쪽 아래)
	}

	for _, combination := range winningCombinations {
		if t.board[combination[0]] == t.board[combination[1]] &&
			t.board[combination[1]] == t.board[combination[2]] &&
			t.board[combination[0]] != " " {
			t.winner = t.board[combination[0]]
			t.gameOver = true
			return true
		}
	}

	// 무승부 검사 (모든 칸이 채워졌는지)
	allFilled := true
	for _, cell := range t.board {
		if cell == " " {
			allFilled = false
			break
		}
	}

	if allFilled {
		t.gameOver = true
		return false
	}

	return false
}

// switchPlayer는 플레이어를 교체합니다
func (t *TicTacToe) switchPlayer() {
	if t.currentPlayer == "X" {
		t.currentPlayer = "O"
	} else {
		t.currentPlayer = "X"
	}
}

// resetGame은 게임을 초기화합니다
func (t *TicTacToe) resetGame() {
	t.board = [9]string{" ", " ", " ", " ", " ", " ", " ", " ", " "}
	t.currentPlayer = "X"
	t.gameOver = false
	t.winner = ""
}

// playGame은 메인 게임 루프를 실행합니다
func (t *TicTacToe) playGame() {
	fmt.Println("틱택토 게임에 오신 것을 환영합니다!")
	fmt.Println("게임을 종료하려면 'quit', 'exit', 또는 'q'를 입력하세요.")
	fmt.Println("게임을 재시작하려면 'restart' 또는 'r'를 입력하세요.")
	fmt.Print("게임을 시작하려면 Enter를 누르세요...")

	reader := bufio.NewReader(os.Stdin)
	reader.ReadString('\n')

	for {
		t.clearScreen()
		t.displayBoard()

		if t.gameOver {
			if t.winner != "" {
				fmt.Printf("🎉 축하합니다! 플레이어 %s가 승리했습니다!\n", t.winner)
			} else {
				fmt.Println("🤝 무승부입니다!")
			}

			fmt.Println("\n게임 옵션:")
			fmt.Println("1. 새 게임 시작 (restart 또는 r)")
			fmt.Println("2. 게임 종료 (quit 또는 q)")

			for {
				fmt.Print("선택하세요: ")
				choice, err := reader.ReadString('\n')
				if err != nil {
					fmt.Printf("입력 오류: %v\n", err)
					continue
				}

				choice = strings.TrimSpace(strings.ToLower(choice))
				if choice == "restart" || choice == "r" || choice == "1" {
					t.resetGame()
					break
				} else if choice == "quit" || choice == "exit" || choice == "q" || choice == "2" {
					fmt.Println("게임을 종료합니다. 즐거운 시간이었습니다!")
					return
				} else {
					fmt.Println("올바른 선택을 해주세요 (restart/r 또는 quit/q)")
				}
			}
		} else {
			move, err := t.getPlayerMove()
			if err != nil {
				fmt.Printf("입력 오류: %v\n", err)
				continue
			}

			t.makeMove(move)

			if t.checkWinner() {
				continue
			}

			t.switchPlayer()
		}
	}
}

// handleInterrupt는 Ctrl+C 신호를 처리합니다
func handleInterrupt() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		<-c
		fmt.Println("\n\n게임이 중단되었습니다.")
		os.Exit(0)
	}()
}

// main 함수는 프로그램의 진입점입니다
func main() {
	// Ctrl+C 신호 처리 설정
	handleInterrupt()

	// 게임 인스턴스 생성 및 실행
	game := NewTicTacToe()
	game.playGame()
}
