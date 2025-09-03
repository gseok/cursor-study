import pygame
import sys
import random
from typing import List, Tuple, Optional

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# 게임 상수
BOARD_SIZE = 8
CELL_SIZE = 60
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
WINDOW_WIDTH = BOARD_WIDTH + 100  # 보드 양옆 여백만
WINDOW_HEIGHT = BOARD_HEIGHT + 300  # 하단에 정보 영역 공간 추가

class OthelloGame:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1  # 1: 흑돌, 2: 백돌
        self.game_over = False
        self.valid_moves = []
        
        # 초기 배치 (오셀로 규칙)
        self.board[3][3] = 2  # 백돌
        self.board[3][4] = 1  # 흑돌
        self.board[4][3] = 1  # 흑돌
        self.board[4][4] = 2  # 백돌
        
        self.update_valid_moves()
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """보드 범위 내의 유효한 위치인지 확인"""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    
    def get_opponent(self, player: int) -> int:
        """상대방 플레이어 번호 반환"""
        return 2 if player == 1 else 1
    
    def get_directions(self) -> List[Tuple[int, int]]:
        """8방향 벡터 반환"""
        return [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def can_flip_in_direction(self, row: int, col: int, direction: Tuple[int, int], player: int) -> bool:
        """특정 방향으로 뒤집을 수 있는 돌이 있는지 확인"""
        dr, dc = direction
        opponent = self.get_opponent(player)
        
        # 인접한 셀이 상대방 돌인지 확인
        next_row, next_col = row + dr, col + dc
        if not self.is_valid_position(next_row, next_col) or self.board[next_row][next_col] != opponent:
            return False
        
        # 상대방 돌들을 따라가면서 자신의 돌을 찾음
        while True:
            next_row += dr
            next_col += dc
            
            if not self.is_valid_position(next_row, next_col):
                return False
            
            if self.board[next_row][next_col] == 0:  # 빈 공간
                return False
            
            if self.board[next_row][next_col] == player:  # 자신의 돌 발견
                return True
    
    def is_valid_move(self, row: int, col: int, player: int) -> bool:
        """해당 위치에 돌을 놓을 수 있는지 확인"""
        if not self.is_valid_position(row, col) or self.board[row][col] != 0:
            return False
        
        # 8방향 중 하나라도 뒤집을 수 있는 돌이 있으면 유효한 수
        for direction in self.get_directions():
            if self.can_flip_in_direction(row, col, direction, player):
                return True
        
        return False
    
    def flip_stones_in_direction(self, row: int, col: int, direction: Tuple[int, int], player: int):
        """특정 방향의 돌들을 뒤집음"""
        dr, dc = direction
        opponent = self.get_opponent(player)
        
        next_row, next_col = row + dr, col + dc
        while self.board[next_row][next_col] == opponent:
            self.board[next_row][next_col] = player
            next_row += dr
            next_col += dc
    
    def make_move(self, row: int, col: int, player: int) -> bool:
        """돌을 놓고 뒤집기"""
        if not self.is_valid_move(row, col, player):
            return False
        
        self.board[row][col] = player
        
        # 8방향으로 뒤집을 수 있는 돌들을 뒤집음
        for direction in self.get_directions():
            if self.can_flip_in_direction(row, col, direction, player):
                self.flip_stones_in_direction(row, col, direction, player)
        
        return True
    
    def update_valid_moves(self):
        """현재 플레이어의 유효한 수들을 업데이트"""
        self.valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, self.current_player):
                    self.valid_moves.append((row, col))
    
    def switch_player(self):
        """플레이어 교체"""
        self.current_player = self.get_opponent(self.current_player)
        self.update_valid_moves()
        
        # 유효한 수가 없으면 상대방에게 턴을 넘김
        if not self.valid_moves:
            self.current_player = self.get_opponent(self.current_player)
            self.update_valid_moves()
            
            # 상대방도 유효한 수가 없으면 게임 종료
            if not self.valid_moves:
                self.game_over = True
    
    def get_score(self) -> Tuple[int, int]:
        """흑돌과 백돌의 개수 반환"""
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)
        return black_count, white_count
    
    def get_winner(self) -> Optional[int]:
        """승자 반환 (1: 흑돌 승, 2: 백돌 승, None: 무승부)"""
        if not self.game_over:
            return None
        
        black_count, white_count = self.get_score()
        if black_count > white_count:
            return 1
        elif white_count > black_count:
            return 2
        else:
            return None

class OthelloGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Othello Game")
        self.clock = pygame.time.Clock()
        
        # 한글 폰트 설정 (시스템 폰트 사용)
        try:
            # macOS에서 사용 가능한 한글 폰트들
            font_paths = [
                '/System/Library/Fonts/AppleSDGothicNeo.ttc',
                '/System/Library/Fonts/Helvetica.ttc',
                '/Library/Fonts/Arial Unicode MS.ttf',
                '/System/Library/Fonts/Helvetica.ttc'
            ]
            
            self.font = None
            self.small_font = None
            
            for font_path in font_paths:
                try:
                    self.font = pygame.font.Font(font_path, 24)
                    self.small_font = pygame.font.Font(font_path, 18)
                    break
                except:
                    continue
            
            # 폰트 로드 실패 시 기본 폰트 사용
            if self.font is None:
                self.font = pygame.font.Font(None, 24)
                self.small_font = pygame.font.Font(None, 18)
                
        except:
            # 폰트 로드 실패 시 기본 폰트 사용
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        
        self.game = OthelloGame()
        self.selected_pos = None
    
    def draw_board(self):
        """보드 그리기"""
        # 보드 배경
        board_rect = pygame.Rect(50, 50, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.screen, GREEN, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 2)
        
        # 격자선 그리기
        for i in range(BOARD_SIZE + 1):
            # 세로선
            pygame.draw.line(self.screen, BLACK, 
                           (50 + i * CELL_SIZE, 50), 
                           (50 + i * CELL_SIZE, 50 + BOARD_HEIGHT), 2)
            # 가로선
            pygame.draw.line(self.screen, BLACK, 
                           (50, 50 + i * CELL_SIZE), 
                           (50 + BOARD_WIDTH, 50 + i * CELL_SIZE), 2)
        
        # 돌 그리기
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.game.board[row][col] != 0:
                    center_x = 50 + col * CELL_SIZE + CELL_SIZE // 2
                    center_y = 50 + row * CELL_SIZE + CELL_SIZE // 2
                    radius = CELL_SIZE // 2 - 5
                    
                    color = BLACK if self.game.board[row][col] == 1 else WHITE
                    pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
                    pygame.draw.circle(self.screen, BLACK, (center_x, center_y), radius, 2)
        
        # 유효한 수 표시
        for row, col in self.game.valid_moves:
            center_x = 50 + col * CELL_SIZE + CELL_SIZE // 2
            center_y = 50 + row * CELL_SIZE + CELL_SIZE // 2
            radius = 8
            
            color = RED if self.game.current_player == 1 else BLUE
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
    
    def draw_ui(self):
        """UI 요소 그리기 - 하단에 배치"""
        ui_y = BOARD_HEIGHT + 60  # 보드 아래쪽에 UI 배치
        ui_width = BOARD_WIDTH - 20  # 보드 너비에 맞춤
        ui_x = 50  # 좌측 여백
        
        # 현재 플레이어 표시 (더 큰 폰트와 색상으로 강조)
        player_text = "Black" if self.game.current_player == 1 else "White"
        player_color = BLACK if self.game.current_player == 1 else WHITE
        
        # 현재 턴 배경 박스
        turn_rect = pygame.Rect(ui_x, ui_y, ui_width, 50)
        pygame.draw.rect(self.screen, GRAY, turn_rect)
        pygame.draw.rect(self.screen, BLACK, turn_rect, 2)
        
        # 현재 턴 텍스트
        turn_surface = self.font.render("Current Turn:", True, BLACK)
        self.screen.blit(turn_surface, (ui_x + 10, ui_y + 10))
        
        # 현재 플레이어 표시 (큰 원으로)
        player_center_x = ui_x + ui_width - 30
        player_center_y = ui_y + 25
        player_radius = 15
        pygame.draw.circle(self.screen, player_color, (player_center_x, player_center_y), player_radius)
        pygame.draw.circle(self.screen, BLACK, (player_center_x, player_center_y), player_radius, 2)
        
        # 플레이어 이름
        player_name_surface = self.font.render(player_text, True, BLACK)
        self.screen.blit(player_name_surface, (ui_x + 150, ui_y + 15))
        
        # 점수 표시
        black_count, white_count = self.game.get_score()
        
        # 점수 배경 박스
        score_rect = pygame.Rect(ui_x, ui_y + 60, ui_width, 50)
        pygame.draw.rect(self.screen, WHITE, score_rect)
        pygame.draw.rect(self.screen, BLACK, score_rect, 2)
        
        # 점수 제목
        score_title = self.font.render("Score", True, BLACK)
        self.screen.blit(score_title, (ui_x + 10, ui_y + 70))
        
        # 흑돌 점수 (원과 함께)
        black_center_x = ui_x + 100
        black_center_y = ui_y + 85
        pygame.draw.circle(self.screen, BLACK, (black_center_x, black_center_y), 10)
        black_score_surface = self.font.render(f"Black: {black_count}", True, BLACK)
        self.screen.blit(black_score_surface, (ui_x + 120, ui_y + 75))
        
        # 백돌 점수 (원과 함께)
        white_center_x = ui_x + 250
        white_center_y = ui_y + 85
        pygame.draw.circle(self.screen, WHITE, (white_center_x, white_center_y), 10)
        pygame.draw.circle(self.screen, BLACK, (white_center_x, white_center_y), 10, 2)
        white_score_surface = self.font.render(f"White: {white_count}", True, BLACK)
        self.screen.blit(white_score_surface, (ui_x + 270, ui_y + 75))
        
        # 게임 상태 표시
        if self.game.game_over:
            # 게임 종료 배경 박스
            status_rect = pygame.Rect(ui_x, ui_y + 120, ui_width, 50)
            pygame.draw.rect(self.screen, RED, status_rect)
            pygame.draw.rect(self.screen, BLACK, status_rect, 2)
            
            winner = self.game.get_winner()
            if winner is None:
                status_text = "Game Over - Draw!"
            else:
                winner_text = "Black" if winner == 1 else "White"
                status_text = f"{winner_text} Wins!"
            
            status_surface = self.font.render(status_text, True, WHITE)
            self.screen.blit(status_surface, (ui_x + 10, ui_y + 130))
            
            # 재시작 안내
            restart_text = "Press R to restart"
            restart_surface = self.small_font.render(restart_text, True, WHITE)
            self.screen.blit(restart_surface, (ui_x + ui_width - 120, ui_y + 135))
        else:
            # 게임 진행 중 상태
            status_rect = pygame.Rect(ui_x, ui_y + 120, ui_width, 50)
            pygame.draw.rect(self.screen, GREEN, status_rect)
            pygame.draw.rect(self.screen, BLACK, status_rect, 2)
            
            # 유효한 수 개수 표시
            moves_text = f"Valid moves: {len(self.game.valid_moves)}"
            moves_surface = self.font.render(moves_text, True, WHITE)
            self.screen.blit(moves_surface, (ui_x + 10, ui_y + 130))
            
            # 게임 진행 중 표시
            playing_text = "Game in progress"
            playing_surface = self.small_font.render(playing_text, True, WHITE)
            self.screen.blit(playing_surface, (ui_x + ui_width - 120, ui_y + 135))
    
    def get_board_position(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """마우스 위치를 보드 좌표로 변환"""
        x, y = mouse_pos
        if 50 <= x < 50 + BOARD_WIDTH and 50 <= y < 50 + BOARD_HEIGHT:
            col = (x - 50) // CELL_SIZE
            row = (y - 50) // CELL_SIZE
            return row, col
        return None
    
    def handle_click(self, pos: Tuple[int, int]):
        """마우스 클릭 처리"""
        if self.game.game_over:
            return
        
        board_pos = self.get_board_position(pos)
        if board_pos:
            row, col = board_pos
            if self.game.make_move(row, col, self.game.current_player):
                self.game.switch_player()
    
    def restart_game(self):
        """게임 재시작"""
        self.game = OthelloGame()
    
    def run(self):
        """메인 게임 루프"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 왼쪽 클릭
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # R키로 재시작
                        self.restart_game()
            
            # 화면 그리기
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = OthelloGUI()
    game.run()
