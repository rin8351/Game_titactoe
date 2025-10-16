"""
AI module for Tic-Tac-Toe game.
Implements different AI strategies.
"""

import random
import numpy as np
from typing import Tuple, List, Optional
from .board import Board


class BaseAI:
    """Base class for AI players."""
    
    def __init__(self, player_number: int):
        """
        Initialize AI player.
        
        Args:
            player_number: Player number (1 or 2)
        """
        self.player_number = player_number
        self.opponent_number = 2 if player_number == 1 else 1
    
    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        Get the AI's next move.
        
        Args:
            board: Current board state
            
        Returns:
            Tuple of (row, col) for the move
        """
        raise NotImplementedError("Subclasses must implement get_move()")


class RandomAI(BaseAI):
    """AI that makes random valid moves."""
    
    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        Get a random valid move.
        
        Args:
            board: Current board state
            
        Returns:
            Random (row, col) from available moves
        """
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            raise ValueError("No empty cells available")
        return random.choice(empty_cells)


class StrategyAI(BaseAI):
    """
    AI that uses strategic thinking.
    
    Original strategy from 2019 version:
    1. Block opponent's win (opponent one move from winning)
    2. Win if possible (one move away from winning)
    3. Continue/choose winning pattern strategy
    4. Random move as fallback
    
    Uses pattern-based approach with 8 winning combinations.
    """
    
    def __init__(self, player_number: int):
        """Initialize strategy AI with current strategy tracking."""
        super().__init__(player_number)
        self.current_strategy: Optional[np.ndarray] = None
        self.strategy_index = 0
    
    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        Get strategic move based on game state.
        
        Original algorithm from the 2019 version:
        1. Block opponent's winning move
        2. Take own winning move
        3. Follow strategic pattern
        4. Random move
        
        Args:
            board: Current board state
            
        Returns:
            Strategic (row, col) move
        """
        # Priority 1: Block opponent's win (original order)
        blocking_move = self._find_winning_move(board, self.opponent_number)
        if blocking_move:
            self.current_strategy = None
            return blocking_move
        
        # Priority 2: Win if possible
        winning_move = self._find_winning_move(board, self.player_number)
        if winning_move:
            self.current_strategy = None
            return winning_move
        
        # Priority 3: Strategic pattern-based move (original logic)
        strategic_move = self._get_strategic_move(board)
        if strategic_move:
            return strategic_move
        
        # Priority 4: Random valid move
        return random.choice(board.get_empty_cells())
    
    def _find_winning_move(self, board: Board, player: int) -> Optional[Tuple[int, int]]:
        """
        Find a move that would win the game for the given player.
        
        Args:
            board: Current board state
            player: Player number to check winning move for
            
        Returns:
            Winning move (row, col) or None
        """
        for pattern in board.winning_patterns:
            # Count how many cells match the pattern for this player
            matching_cells = []
            empty_cells = []
            
            for i in range(Board.SIZE):
                for j in range(Board.SIZE):
                    if pattern[i, j] == 1:
                        if board.grid[i, j] == player:
                            matching_cells.append((i, j))
                        elif board.grid[i, j] == 0:  # 0 = пустая клетка
                            empty_cells.append((i, j))
            
            # If 2 cells match and 1 is empty, this is a winning move
            if len(matching_cells) == 2 and len(empty_cells) == 1:
                return empty_cells[0]
        
        return None
    
    
    def _get_strategic_move(self, board: Board) -> Optional[Tuple[int, int]]:
        """
        Get move based on current or new strategy pattern.
        
        Args:
            board: Current board state
            
        Returns:
            Strategic move (row, col) or None
        """
        # Get available winning patterns for this player
        available_patterns = self._get_available_patterns(board)
        
        if not available_patterns:
            return None
        
        # If no current strategy, choose the best one
        if self.current_strategy is None:
            self.current_strategy = self._choose_best_pattern(board, available_patterns)
            self.strategy_index = 0
        
        # Check if current strategy is still valid
        if not self._is_pattern_valid(board, self.current_strategy):
            # Choose new strategy
            self.current_strategy = self._choose_best_pattern(board, available_patterns)
            self.strategy_index = 0
        
        # Make move according to strategy
        if self.current_strategy is not None:
            move = self._get_move_from_pattern(board, self.current_strategy)
            if move:
                return move
        
        return None
    
    def _get_available_patterns(self, board: Board) -> List[np.ndarray]:
        """
        Get winning patterns that are still achievable.
        
        Args:
            board: Current board state
            
        Returns:
            List of available winning patterns
        """
        available = []
        
        for pattern in board.winning_patterns:
            # Check if pattern is blocked by opponent
            blocked = False
            for i in range(Board.SIZE):
                for j in range(Board.SIZE):
                    if pattern[i, j] == 1 and board.grid[i, j] == self.opponent_number:
                        blocked = True
                        break
                if blocked:
                    break
            
            if not blocked:
                available.append(pattern)
        
        return available
    
    def _choose_best_pattern(self, board: Board, patterns: List[np.ndarray]) -> Optional[np.ndarray]:
        """
        Choose the best pattern based on current board state.
        Prefers patterns where we already have moves.
        
        Args:
            board: Current board state
            patterns: Available patterns
            
        Returns:
            Best pattern or None
        """
        if not patterns:
            return None
        
        # Score each pattern by how many of our moves it contains
        pattern_scores = []
        for pattern in patterns:
            score = 0
            for i in range(Board.SIZE):
                for j in range(Board.SIZE):
                    if pattern[i, j] == 1 and board.grid[i, j] == self.player_number:
                        score += 1
            pattern_scores.append((score, pattern))
        
        # Sort by score (descending) and return best
        pattern_scores.sort(reverse=True, key=lambda x: x[0])
        
        # If best score is 0, return random pattern
        if pattern_scores[0][0] == 0:
            return random.choice(patterns)
        
        return pattern_scores[0][1]
    
    def _is_pattern_valid(self, board: Board, pattern: np.ndarray) -> bool:
        """
        Check if a pattern is still valid (not blocked by opponent).
        
        Args:
            board: Current board state
            pattern: Pattern to check
            
        Returns:
            True if pattern is still achievable
        """
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if pattern[i, j] == 1 and board.grid[i, j] == self.opponent_number:
                    return False
        return True
    
    def _get_move_from_pattern(self, board: Board, pattern: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Get next move from a pattern.
        
        Args:
            board: Current board state
            pattern: Pattern to follow
            
        Returns:
            Next move (row, col) or None
        """
        # Get all pattern positions
        pattern_positions = []
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if pattern[i, j] == 1:
                    pattern_positions.append((i, j))
        
        # Find first empty position in pattern
        for pos in pattern_positions:
            if board.is_valid_move(pos[0], pos[1]):
                return pos
        
        return None
    
    def reset_strategy(self):
        """Reset current strategy (for new game)."""
        self.current_strategy = None
        self.strategy_index = 0

