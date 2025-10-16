"""
Board module for Tic-Tac-Toe game.
Handles the game board state and win condition checks.
"""

import numpy as np
from typing import List, Tuple, Optional


class Board:
    """
    Represents a 3x3 Tic-Tac-Toe board.
    
    Attributes:
        grid: 3x3 numpy array representing the board state
        winning_patterns: All possible winning combinations
    """
    
    SIZE = 3
    
    def __init__(self):
        """Initialize an empty 3x3 board."""
        self.grid = np.zeros((self.SIZE, self.SIZE), dtype=int)
        self.winning_patterns = self._generate_winning_patterns()
    
    def _generate_winning_patterns(self) -> List[np.ndarray]:
        """
        Generate all possible winning patterns.
        
        Returns:
            List of 3x3 numpy arrays, each representing a winning pattern
        """
        patterns = []
        
        # Horizontal rows
        for row in range(self.SIZE):
            pattern = np.zeros((self.SIZE, self.SIZE), dtype=int)
            pattern[row, :] = 1
            patterns.append(pattern)
        
        # Vertical columns
        for col in range(self.SIZE):
            pattern = np.zeros((self.SIZE, self.SIZE), dtype=int)
            pattern[:, col] = 1
            patterns.append(pattern)
        
        # Diagonal (top-left to bottom-right)
        pattern = np.eye(self.SIZE, dtype=int)
        patterns.append(pattern)
        
        # Anti-diagonal (top-right to bottom-left)
        pattern = np.fliplr(np.eye(self.SIZE, dtype=int))
        patterns.append(pattern)
        
        return patterns
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            True if the move is valid, False otherwise
        """
        if not (0 <= row < self.SIZE and 0 <= col < self.SIZE):
            return False
        return self.grid[row, col] == 0  # 0 = пустая клетка
    
    def make_move(self, row: int, col: int, player: int) -> bool:
        """
        Make a move on the board.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            player: Player number (1 or 2)
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False
        
        self.grid[row, col] = player
        return True
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get all empty cells on the board.
        
        Returns:
            List of (row, col) tuples for empty cells
        """
        empty_positions = np.where(self.grid == 0)  # 0 = пустая клетка
        return list(zip(empty_positions[0], empty_positions[1]))
    
    def check_winner(self, player: int) -> bool:
        """
        Check if a player has won.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            True if the player has won, False otherwise
        """
        for pattern in self.winning_patterns:
            # Check if all positions in the pattern match the player
            if np.all((pattern == 1) == (self.grid == player)):
                return True
        return False
    
    def is_full(self) -> bool:
        """
        Check if the board is full.
        
        Returns:
            True if no empty cells remain, False otherwise
        """
        return len(self.get_empty_cells()) == 0
    
    def is_game_over(self) -> Tuple[bool, Optional[int]]:
        """
        Check if the game is over.
        
        Returns:
            Tuple of (is_over, winner) where winner is None for draw
        """
        if self.check_winner(1):  # Проверка победы игрока 1
            return True, 1
        if self.check_winner(2):  # Проверка победы игрока 2
            return True, 2
        if self.is_full():
            return True, None  # Ничья
        return False, None
    
    def reset(self):
        """Reset the board to empty state."""
        self.grid = np.zeros((self.SIZE, self.SIZE), dtype=int)
    
    def copy(self) -> 'Board':
        """
        Create a deep copy of the board.
        
        Returns:
            New Board instance with copied state
        """
        new_board = Board()
        new_board.grid = self.grid.copy()
        return new_board
    
    def __str__(self) -> str:
        """
        String representation of the board.
        
        Returns:
            Formatted board string
        """
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        lines = []
        for i, row in enumerate(self.grid):
            line = ' | '.join(symbols[cell] for cell in row)
            lines.append(line)
            if i < self.SIZE - 1:
                lines.append('-' * 9)
        return '\n'.join(lines)
    
    def __repr__(self) -> str:
        """Detailed representation of the board."""
        return f"Board(grid=\n{self.grid})"

