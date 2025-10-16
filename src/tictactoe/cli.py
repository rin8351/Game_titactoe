"""
CLI (Command Line Interface) for Tic-Tac-Toe game.
Provides interactive console-based gameplay.
"""

from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich import box
from .game import Game, GameStats, GameResult
from .player import PlayerType
from .board import Board


class TicTacToeCLI:
    """Command-line interface for the Tic-Tac-Toe game."""
    
    def __init__(self):
        """Initialize the CLI with Rich console."""
        self.console = Console()
        self.game: Optional[Game] = None
    
    def display_banner(self):
        """Display welcome banner."""
        banner = Text("🎮 TIC-TAC-TOE 🎮", style="bold magenta", justify="center")
        self.console.print(Panel(banner, box=box.DOUBLE, border_style="cyan"))
    
    def display_board(self, board: Board):
        """
        Display the game board in a nice format.
        
        Args:
            board: Board to display
        """
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        
        print("\n")
        for i, row in enumerate(board.grid):
            row_str = ' | '.join(symbols[cell] for cell in row)
            print(f"  {row_str}  ")
            if i < 2:
                print("  ---------")
        print("\n")
    
    def display_menu(self) -> int:
        """
        Display main menu and get user choice.
        
        Returns:
            Menu choice (1-4)
        """
        self.console.print("\n[bold cyan]Main Menu:[/bold cyan]")
        self.console.print("  1. Play against AI")
        self.console.print("  2. Watch AI vs AI")
        self.console.print("  3. Run simulation")
        self.console.print("  4. Exit")
        
        choice = IntPrompt.ask(
            "\n[yellow]Choose an option[/yellow]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        return choice
    
    def choose_ai_difficulty(self) -> PlayerType:
        """
        Let user choose AI difficulty.
        
        Returns:
            Selected AI PlayerType
        """
        self.console.print("\n[bold cyan]Choose AI Difficulty:[/bold cyan]")
        self.console.print("  1. Random (Easy)")
        self.console.print("  2. Strategic (Hard)")
        
        choice = IntPrompt.ask(
            "\n[yellow]Choose difficulty[/yellow]",
            choices=["1", "2"],
            default="2"
        )
        
        return PlayerType.AI_RANDOM if choice == 1 else PlayerType.AI_STRATEGY
    
    def choose_first_player(self) -> int:
        """
        Let user choose who goes first.
        
        Returns:
            Player number (1 for user, 2 for AI)
        """
        self.console.print("\n[bold cyan]Who goes first? Just enter the number of the player you want to go first.[/bold cyan]")
        self.console.print("  1. You (X)")
        self.console.print("  2. AI (O)")
        
        choice = IntPrompt.ask(
            "\n[yellow]Choose[/yellow]",
            choices=["1", "2"],
            default="1"
        )
        
        return choice
    
    def get_human_move(self, board: Board) -> tuple[int, int]:
        """
        Get move input from human player.
        
        Args:
            board: Current board state
            
        Returns:
            Tuple of (row, col)
        """
        while True:
            self.console.print("[bold yellow]Enter your move (row and column, 0-2):[/bold yellow]")
            
            try:
                row = IntPrompt.ask("Row", choices=["0", "1", "2"])
                col = IntPrompt.ask("Column", choices=["0", "1", "2"])
                
                if board.is_valid_move(row, col):
                    return row, col
                else:
                    self.console.print("[red]❌ That cell is already taken! Try again.[/red]")
            except Exception as e:
                self.console.print(f"[red]❌ Invalid input: {e}[/red]")
    
    def display_result(self, result: GameResult):
        """
        Display game result.
        
        Args:
            result: GameResult to display
        """
        if result.is_draw:
            message = Text("🤝 It's a Draw!", style="bold yellow")
        elif result.winner == 1:
            message = Text("🎉 Player 1 (X) Wins!", style="bold red")
        else:
            message = Text("🎉 Player 2 (O) Wins!", style="bold green")
        
        self.console.print("\n")
        self.console.print(Panel(message, box=box.DOUBLE, border_style="magenta"))
    
    def display_stats(self, stats: GameStats):
        """
        Display game statistics.
        
        Args:
            stats: GameStats to display
        """
        table = Table(title="📊 Game Statistics", box=box.ROUNDED, border_style="cyan")
        
        table.add_column("Metric", style="cyan", justify="left")
        table.add_column("Value", style="magenta", justify="right")
        
        table.add_row("Total Games", str(stats.total_games))
        table.add_row("Player 1 Wins", f"{stats.player1_wins} ({stats.get_win_rate(1):.1f}%)")
        table.add_row("Player 2 Wins", f"{stats.player2_wins} ({stats.get_win_rate(2):.1f}%)")
        table.add_row("Draws", str(stats.draws))
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
    
    def play_vs_ai(self):
        """Play a game: Human vs AI."""
        ai_type = self.choose_ai_difficulty()
        first_player = self.choose_first_player()
        
        # Setup game
        if first_player == 1:
            self.game = Game(PlayerType.HUMAN, ai_type)
        else:
            self.game = Game(ai_type, PlayerType.HUMAN)
            self.game.current_player = self.game.player1
        
        self.console.print("\n[bold green]Game started! You are 'X', AI is 'O'[/bold green]")
        
        # Game loop
        while True:
            self.display_board(self.game.board)
            
            # Current player's turn
            if self.game.current_player.player_type == PlayerType.HUMAN:
                self.console.print(f"[bold cyan]Your turn ({self.game.current_player.symbol}):[/bold cyan]")
                row, col = self.get_human_move(self.game.board)
                self.game.make_move(row, col)
            else:
                self.console.print(f"[bold cyan]AI's turn ({self.game.current_player.symbol})...[/bold cyan]")
                row, col = self.game.get_ai_move()
                self.game.make_move(row, col)
                self.console.print(f"AI played: ({row}, {col})")
            
            # Check game over
            is_over, result = self.game.check_game_over()
            if is_over:
                self.display_board(self.game.board)
                self.display_result(result)
                break
            
            # Switch player
            self.game.switch_player()
        
        # Ask to play again
        play_again = Prompt.ask("\n[yellow]Play again?[/yellow]", choices=["y", "n"], default="y")
        if play_again == "y":
            self.play_vs_ai()
    
    def watch_ai_vs_ai(self):
        """Watch AI vs AI game."""
        self.console.print("\n[bold cyan]Choose AI types:[/bold cyan]")
        
        self.console.print("\n[bold]Player 1 (X):[/bold]")
        ai1_type = self.choose_ai_difficulty()
        
        self.console.print("\n[bold]Player 2 (O):[/bold]")
        ai2_type = self.choose_ai_difficulty()
        
        self.game = Game(ai1_type, ai2_type)
        
        self.console.print("\n[bold green]Game started![/bold green]")
        self.console.print("Press Enter to see each move...")
        
        # Game loop
        while True:
            self.display_board(self.game.board)
            
            player_name = f"Player {self.game.current_player.number} ({self.game.current_player.symbol})"
            self.console.print(f"[bold cyan]{player_name}'s turn...[/bold cyan]")
            
            input()  # Wait for Enter
            
            row, col = self.game.get_ai_move()
            self.game.make_move(row, col)
            self.console.print(f"Played: ({row}, {col})")
            
            # Check game over
            is_over, result = self.game.check_game_over()
            if is_over:
                self.display_board(self.game.board)
                self.display_result(result)
                break
            
            # Switch player
            self.game.switch_player()
    
    def run_simulation(self):
        """Run multiple games and show statistics."""
        self.console.print("\n[bold cyan]Simulation Setup:[/bold cyan]")
        
        self.console.print("\n[bold]Player 1 (X):[/bold]")
        ai1_type = self.choose_ai_difficulty()
        
        self.console.print("\n[bold]Player 2 (O):[/bold]")
        ai2_type = self.choose_ai_difficulty()
        
        num_games = IntPrompt.ask(
            "\n[yellow]How many games to simulate?[/yellow]",
            default=100
        )
        
        self.game = Game(ai1_type, ai2_type)
        
        self.console.print(f"\n[bold green]Running {num_games} simulations...[/bold green]")
        
        with self.console.status("[bold green]Simulating games...[/bold green]"):
            stats = self.game.simulate_games(num_games)
        
        self.display_stats(stats)
    
    def run(self):
        """Run the main CLI application."""
        self.display_banner()
        
        while True:
            choice = self.display_menu()
            
            if choice == 1:
                self.play_vs_ai()
            elif choice == 2:
                self.watch_ai_vs_ai()
            elif choice == 3:
                self.run_simulation()
            elif choice == 4:
                self.console.print("\n[bold magenta]👋 Thanks for playing! Goodbye![/bold magenta]\n")
                break


def main():
    """Entry point for the CLI application."""
    cli = TicTacToeCLI()
    cli.run()


if __name__ == "__main__":
    main()

