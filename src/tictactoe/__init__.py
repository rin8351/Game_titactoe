"""
Tic-Tac-Toe Game Package
A modern implementation of the classic game with AI strategies.
"""

__version__ = "2.0.0"
__author__ = "Rin"

from .board import Board
from .game import Game
from .player import Player, PlayerType

__all__ = ["Board", "Game", "Player", "PlayerType"]

