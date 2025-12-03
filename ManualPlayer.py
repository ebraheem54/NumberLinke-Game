class ManualPlayer:

    def __init__(self, game):
        self.game = game

    def start(self):
        print("\n=== MANUAL PLAY MODE ===")
        print("Instructions:")
        print("  - Choose a color to play")
        print("  - Enter direction: up/down/left/right")
        print("  - Type 'reset' to restart the game")
        print("  - Type 'quit' to go back\n")

        while not self.game.isGameCompleted():
            if not self.game.choose_color_to_play():
                choice = input("Cancel selection. Type 'quit' to exit, Enter to continue: ").strip().lower()
                if choice == "quit":
                    return
                else:
                    continue
            
            while True:
                self.game.printGameStatus()
                moves = self.game.getMovesAsDirections(self.game.current_color)
                print(f"Available moves for color {self.game.current_color}: {moves}")
                
                direction = input("Enter direction (up/down/left/right/reset/quit): ").lower()
                
                if direction == "reset":
                    self.game.resetGame()
                    print("Game reset!\n")
                    break
                
                if direction == "quit":
                    print("Leaving this color...\n")
                    self.game.current_color = None
                    break
                
                result = self.game.move(direction)
                
                if result == "completed":
                    print(f"✓ Color {self.game.current_color} completed!\n")
                    break
                elif result is None and direction in ["up", "down", "left", "right"]:
                    print("Invalid move! Try again.\n")
                
                if self.game.isGameCompleted():
                    print("\n" + "="*60)
                    print("   CONGRATULATIONS! GAME COMPLETED! ")
                    print("="*60)
                    self.game.printGameStatus()
                    return
        
        print("\n" + "="*60)
        print("   CONGRATULATIONS! GAME COMPLETED!")
        print("="*60)
        self.game.printGameStatus()
