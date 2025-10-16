"""
Game module for Tic-Tac-Toe.
Manages game flow and player interactions.
"""

from typing import Optional, Tuple
from .board import Board
from .player import Player, PlayerType
from .ai import RandomAI, StrategyAI


class GameResult:
    """Stores the result of a game."""
    
    def __init__(self, winner: Optional[int], is_draw: bool = False):
        """
        Initialize game result.
        
        Args:
            winner: Winner player number (1 or 2) or None
            is_draw: True if game ended in draw
        """
        self.winner = winner
        self.is_draw = is_draw
    
    def __str__(self) -> str:
        """String representation of result."""
        if self.is_draw:
            return "Draw"
        return f"Player {self.winner} wins!"


class GameStats:
    """Tracks statistics across multiple games."""
    
    def __init__(self):
        """Initialize empty statistics."""
        self.player1_wins = 0
        self.player2_wins = 0
        self.draws = 0
        self.total_games = 0
    
    def record_result(self, result: GameResult):
        """
        Record a game result.
        
        Args:
            result: GameResult to record
        """
        self.total_games += 1
        if result.is_draw:
            self.draws += 1
        elif result.winner == 1:
            self.player1_wins += 1
        elif result.winner == 2:
            self.player2_wins += 1
    
    def get_win_rate(self, player: int) -> float:
        """
        Get win rate for a player.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            Win rate as percentage (0-100)
        """
        if self.total_games == 0:
            return 0.0
        
        wins = self.player1_wins if player == 1 else self.player2_wins
        return (wins / self.total_games) * 100
    
    def reset(self):
        """Reset all statistics."""
        self.player1_wins = 0
        self.player2_wins = 0
        self.draws = 0
        self.total_games = 0
    
    def __str__(self) -> str:
        """String representation of statistics."""
        return (f"Games: {self.total_games} | "
                f"P1 Wins: {self.player1_wins} ({self.get_win_rate(1):.1f}%) | "
                f"P2 Wins: {self.player2_wins} ({self.get_win_rate(2):.1f}%) | "
                f"Draws: {self.draws}")


class Game:
    """
    Main game controller.
    
    Manages the game loop, player turns, and game state.
    """
    
    def __init__(self, player1_type: PlayerType, player2_type: PlayerType):
        """
        Initialize a new game.
        
        Args:
            player1_type: Type of player 1
            player2_type: Type of player 2
        """
        self.board = Board()
        self.player1 = Player(1, player1_type)
        self.player2 = Player(2, player2_type)
        self.current_player = self.player1
        self.stats = GameStats()
        
        # Initialize AI if needed
        self.ai_players = {}
        if player1_type == PlayerType.AI_RANDOM:
            self.ai_players[1] = RandomAI(1)
        elif player1_type == PlayerType.AI_STRATEGY:
            self.ai_players[1] = StrategyAI(1)
        
        if player2_type == PlayerType.AI_RANDOM:
            self.ai_players[2] = RandomAI(2)
        elif player2_type == PlayerType.AI_STRATEGY:
            self.ai_players[2] = StrategyAI(2)
    
    def get_ai_move(self) -> Tuple[int, int]:
        """
        Get move from AI player.
        
        Returns:
            AI's chosen (row, col) move
        """
        if self.current_player.number not in self.ai_players:
            raise ValueError("Current player is not an AI")
        
        ai = self.ai_players[self.current_player.number]
        return ai.get_move(self.board)
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move for the current player.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            True if move was successful
        """
        if self.board.make_move(row, col, self.current_player.number):
            return True
        return False
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
    
    def check_game_over(self) -> Tuple[bool, Optional[GameResult]]:
        """
        Check if game is over.
        
        Returns:
            Tuple of (is_over, result)
        """
        is_over, winner = self.board.is_game_over()
        if is_over:
            if winner is None:
                return True, GameResult(None, is_draw=True)
            return True, GameResult(winner)
        return False, None
    
    def reset(self):
        """Reset the game for a new round."""
        self.board.reset()
        self.current_player = self.player1
        
        # Reset AI strategies
        for ai in self.ai_players.values():
            if isinstance(ai, StrategyAI):
                ai.reset_strategy()
    
    def play_single_game(self, first_player: int = 1) -> GameResult:
        """
        Play a complete game automatically (AI vs AI).
        
        Args:
            first_player: Which player goes first (1 or 2)
            
        Returns:
            GameResult of the completed game
        """
        self.reset()
        self.current_player = self.player1 if first_player == 1 else self.player2
        
        while True:
            # Get AI move
            if self.current_player.number in self.ai_players:
                row, col = self.get_ai_move()
                self.make_move(row, col)
            else:
                raise ValueError("Cannot auto-play with human players")
            
            # Check if game is over
            is_over, result = self.check_game_over()
            if is_over:
                return result
            
            # Switch player
            self.switch_player()
    
    def simulate_games(self, num_games: int, first_player: int = 1) -> GameStats:
        """
        Simulate multiple games.
        
        Args:
            num_games: Number of games to simulate
            first_player: Which player goes first (1 or 2)
            
        Returns:
            GameStats with results
        """
        self.stats.reset()
        
        for _ in range(num_games):
            result = self.play_single_game(first_player)
            self.stats.record_result(result)
        
        return self.stats

