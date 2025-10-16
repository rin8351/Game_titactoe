"""
Player module for Tic-Tac-Toe game.
Defines player types and base player class.
"""

from enum import Enum


class PlayerType(Enum):
    """Types of players in the game."""
    HUMAN = "human"
    AI_RANDOM = "ai_random"
    AI_STRATEGY = "ai_strategy"


class Player:
    """
    Base player class.
    
    Attributes:
        number: Player number (1 or 2)
        player_type: Type of player
        symbol: Symbol to display (X or O)
    """
    
    def __init__(self, number: int, player_type: PlayerType):
        """
        Initialize a player.
        
        Args:
            number: Player number (1 or 2)
            player_type: Type of player
        """
        if number not in [1, 2]:
            raise ValueError("Player number must be 1 or 2")
        
        self.number = number
        self.player_type = player_type
        self.symbol = 'X' if number == 1 else 'O'
    
    def __str__(self) -> str:
        """String representation of the player."""
        return f"Player {self.number} ({self.symbol}) - {self.player_type.value}"
    
    def __repr__(self) -> str:
        """Detailed representation of the player."""
        return f"Player(number={self.number}, type={self.player_type})"

