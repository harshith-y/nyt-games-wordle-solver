import random
from solver import WordleSolver, WordlePattern, load_word_list
from analyser import WordleAnalyzer


# ============================================================================
# CONFIGURATION - TOGGLE MODE HERE
# ============================================================================

# Set to True for automatic random mode, False for interactive menu
AUTO_RANDOM_MODE = False

# If AUTO_RANDOM_MODE is True, configure random testing here:
NUM_RANDOM_TESTS = 10        # How many random words to test
SHOW_DETAILED_SOLVE = True   # Show step-by-step solving (True) or just results (False)

# ============================================================================


def print_header():
    """Print welcome header"""
    print("\n" + "="*70)
    print("WORDLE SOLVER & ANALYZER")
    print("Information Theory Approach")
    print("="*70)


def load_words():
    """Load word list from wordle_answers.txt"""
    print("\nLoading word list from 'wordle_answers.txt'...")
    words = load_word_list('wordle_answers.txt')
    
    if not words:
        print("\n❌ Error: Could not load word list!")
        print("Make sure 'wordle_answers.txt' is in the same directory.")
        print("\nYou can download it with:")
        print("  curl -o wordle_answers.txt https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/wordle-answers-alphabetical.txt")
        return None
    
    print(f"✓ Loaded {len(words)} words")
    return words


def mode_random_solve(words):
    """Mode 1: Randomly pick a word and solve it"""
    print("\n" + "="*70)
    print("MODE: Random Solve")
    print("="*70)
    
    # Pick random word
    answer = random.choice(words)
    print(f"\nRandomly selected word: {answer}")
    print("Solving...\n")
    
    # Solve it
    solver = WordleSolver(words, words)
    guesses = solver.solve(answer, verbose=True)
    
    print(f"\n{'='*70}")
    print(f"Summary: Solved '{answer}' in {len(guesses)} guesses")
    print("="*70)


def mode_random_test_batch(words, num_tests=10):
    """Mode 2: Test solver on multiple random words"""
    print("\n" + "="*70)
    print(f"MODE: Batch Test ({num_tests} random words)")
    print("="*70)
    
    solver = WordleSolver(words, words)
    results = []
    
    # Pick random words
    test_words = random.sample(words, min(num_tests, len(words)))
    
    print("\nTesting solver on random words...\n")
    
    for i, answer in enumerate(test_words, 1):
        solver.reset()
        guesses = solver.solve(answer, verbose=False)
        results.append((answer, len(guesses)))
        
        # Show progress
        pattern_str = WordlePattern.pattern_to_string((2,2,2,2,2))
        print(f"{i:2}. {answer} - {len(guesses)} guesses {pattern_str}")
    
    # Show statistics
    print(f"\n{'='*70}")
    print("BATCH TEST RESULTS")
    print("="*70)
    guess_counts = [count for _, count in results]
    avg_guesses = sum(guess_counts) / len(guess_counts)
    
    print(f"Words tested: {len(results)}")
    print(f"Average guesses: {avg_guesses:.2f}")
    print(f"Best: {min(guess_counts)} guesses")
    print(f"Worst: {max(guess_counts)} guesses")
    
    # Histogram
    print("\nGuess distribution:")
    for i in range(1, 7):
        count = guess_counts.count(i)
        bar = "█" * count
        print(f"  {i} guesses: {bar} ({count})")


def mode_solve_specific(words):
    """Mode 3: Solve a specific word chosen by user"""
    print("\n" + "="*70)
    print("MODE: Solve Specific Word")
    print("="*70)
    
    # Get word from user
    while True:
        answer = input("\nEnter the word to solve (or 'back' to return): ").strip().upper()
        
        if answer.lower() == 'back':
            return
        
        if len(answer) != 5:
            print("❌ Word must be 5 letters!")
            continue
        
        if answer not in words:
            print(f"⚠️  Warning: '{answer}' is not in the word list, but I'll try anyway.")
        
        break
    
    print(f"\nSolving for: {answer}\n")
    
    # Solve it
    solver = WordleSolver(words, words)
    guesses = solver.solve(answer, verbose=True)
    
    print(f"\n{'='*70}")
    print(f"Summary: Solved '{answer}' in {len(guesses)} guesses")
    print("="*70)


def mode_analyze_your_game(words):
    """Mode 4: Analyze user's actual Wordle game"""
    print("\n" + "="*70)
    print("MODE: Analyze Your Game")
    print("="*70)
    
    # Get answer
    while True:
        answer = input("\nWhat was the answer word? ").strip().upper()
        
        if len(answer) != 5:
            print("❌ Answer must be 5 letters!")
            continue
        
        break
    
    # Get guesses
    print("\nEnter your guesses (one per line):")
    print("Press Enter on empty line when done, or 'cancel' to go back\n")
    
    guesses = []
    guess_num = 1
    
    while True:
        guess = input(f"Guess {guess_num}: ").strip().upper()
        
        if guess.lower() == 'cancel':
            return
        
        if not guess:
            if guesses:
                break
            else:
                print("❌ Please enter at least one guess!")
                continue
        
        if len(guess) != 5:
            print("❌ Guess must be 5 letters!")
            continue
        
        guesses.append(guess)
        guess_num += 1
        
        # Stop if they got it right
        if guess == answer:
            break
    
    # Analyze the game
    analyzer = WordleAnalyzer(words, words)
    print("\n")
    analyzer.analyze_game(answer, guesses)
    
    # Offer comparison
    print()
    compare = input("Would you like to see strategy comparison? (y/n): ").strip().lower()
    if compare == 'y':
        analyzer.compare_strategies(answer, guesses)


def mode_interactive_play(words):
    """Mode 5: Interactive play with solver assistance"""
    print("\n" + "="*70)
    print("MODE: Interactive Play (Solver Helps You)")
    print("="*70)
    
    # Pick or choose word
    print("\n1. Random word")
    print("2. I'll choose the word")
    choice = input("\nChoice (1-2): ").strip()
    
    if choice == '1':
        answer = random.choice(words)
        print(f"\nRandomly selected: {answer}")
    else:
        answer = input("Enter the word: ").strip().upper()
        if len(answer) != 5:
            print("❌ Word must be 5 letters!")
            return
    
    print(f"\nSolving: {answer}")
    print("The solver will suggest optimal guesses.\n")
    
    solver = WordleSolver(words, words)
    
    for attempt in range(1, 7):
        # Get solver's suggestion
        best_guess, score = solver.get_best_guess()
        remaining = len(solver.remaining_answers)
        
        print(f"{'='*70}")
        print(f"Attempt {attempt}")
        print(f"Remaining words: {remaining}")
        
        if remaining <= 10:
            print(f"Possibilities: {', '.join(solver.remaining_answers[:10])}")
        
        print(f"\n💡 Solver suggests: {best_guess} (entropy: {score:.2f} bits)")
        
        # User can accept or choose their own
        use_suggestion = input("Use this guess? (y/n, or type your own): ").strip()
        
        if use_suggestion.lower() == 'y' or use_suggestion == '':
            guess = best_guess
        else:
            guess = use_suggestion.upper()
            if len(guess) != 5:
                print("❌ Invalid guess, using solver's suggestion")
                guess = best_guess
        
        # Get pattern
        pattern = WordlePattern.get_pattern(guess, answer)
        pattern_str = WordlePattern.pattern_to_string(pattern)
        
        print(f"\nGuess: {guess} {pattern_str}")
        
        # Check if solved
        if pattern == (2, 2, 2, 2, 2):
            print(f"\n🎉 Solved in {attempt} guesses!")
            break
        
        # Update solver
        solver.make_guess(guess, pattern)
        print()
    
    print(f"\n{'='*70}")


def parse_pattern_input(pattern_str):
    """
    Parse user input pattern into tuple of integers.
    Accepts: G/g (green), Y/y (yellow), _/B/b (gray/black)
    Returns tuple of (0=gray, 1=yellow, 2=green) or None if invalid
    """
    pattern_str = pattern_str.strip().upper()
    
    if len(pattern_str) != 5:
        return None
    
    pattern = []
    for char in pattern_str:
        if char in ['G', '2']:  # Green
            pattern.append(2)
        elif char in ['Y', '1']:  # Yellow
            pattern.append(1)
        elif char in ['_', 'B', '0', '-', '.']:  # Gray/Black
            pattern.append(0)
        else:
            return None
    
    return tuple(pattern)


def mode_live_wordle_helper(words):
    """Mode 6: Live Wordle game helper - for playing actual Wordle!"""
    print("\n" + "="*70)
    print("MODE: Live Wordle Helper 🎮")
    print("="*70)
    print("\nUse this while playing actual Wordle!")
    print("Enter your guesses and the colors you got back.")
    print("\n" + "="*70)
    print("HOW TO ENTER COLORS:")
    print("="*70)
    print("  G or g = Green  🟩 (correct position)")
    print("  Y or y = Yellow 🟨 (wrong position)")
    print("  _ or B = Gray   ⬜ (not in word)")
    print("\nExample: If you got 🟩⬜🟨⬜🟩 type: G_Y_G")
    print("="*70)
    
    # Show some copy-paste squares for convenience
    print("\n📋 Copy-paste these if needed:")
    print("   🟩 🟨 ⬜")
    print()
    
    solver = WordleSolver(words, words)
    
    # First suggestion
    print("\n" + "="*70)
    print("GUESS 1")
    print("="*70)
    
    best_guess, score = solver.get_best_guess()
    print(f"\n💡 Suggested first word: {best_guess}")
    print(f"   (This has {score:.2f} bits of information)")
    print(f"\nOr use your own favorite starting word!")
    print(f"Total possible words: {len(solver.remaining_answers)}")
    
    # Main game loop
    for attempt in range(1, 7):
        print("\n" + "-"*70)
        
        # Get the word they used
        if attempt == 1:
            guess = input(f"\nWhat word did you guess? (or press Enter for {best_guess}): ").strip().upper()
            if not guess:
                guess = best_guess
        else:
            guess = input(f"\nWhat word did you guess? ").strip().upper()
        
        if len(guess) != 5:
            print("❌ Word must be 5 letters! Try again.")
            continue
        
        # Get the pattern they received
        print(f"\nWhat colors did you get for '{guess}'?")
        print("Enter 5 characters (G=green, Y=yellow, _=gray)")
        print("Example: GY__G or gy__g")
        
        while True:
            pattern_input = input("Colors: ").strip()
            pattern = parse_pattern_input(pattern_input)
            
            if pattern is None:
                print("❌ Invalid input! Use 5 characters: G (green), Y (yellow), _ (gray)")
                print("Example: GY__G")
                continue
            
            # Show them what we understood
            pattern_str = WordlePattern.pattern_to_string(pattern)
            print(f"✓ Got it: {guess} {pattern_str}")
            
            # Confirm
            confirm = input("Is this correct? (y/n): ").strip().lower()
            if confirm == 'y' or confirm == '':
                break
            else:
                print("Let's try again...")
        
        # Check if they won
        if pattern == (2, 2, 2, 2, 2):
            print(f"\n{'='*70}")
            print(f"🎉 CONGRATULATIONS! You solved it in {attempt} guesses!")
            print(f"{'='*70}")
            return
        
        # Update solver with this information
        solver.make_guess(guess, pattern)
        remaining = len(solver.remaining_answers)
        
        print(f"\n{'='*70}")
        print(f"ANALYSIS - After Guess {attempt}")
        print("="*70)
        print(f"Words remaining: {remaining}")
        
        if remaining == 0:
            print("\n❌ No words match these patterns!")
            print("Possible issues:")
            print("  - Word might not be in the word list")
            print("  - Pattern might have been entered incorrectly")
            print("  - There might be a typo in your guess")
            return
        
        if remaining <= 10:
            print(f"Possible words: {', '.join(sorted(solver.remaining_answers))}")
        elif remaining <= 20:
            print(f"Possible words: {', '.join(sorted(solver.remaining_answers[:20]))} ...")
        
        # Get next suggestion
        if remaining > 1 and attempt < 6:
            print("\n" + "="*70)
            print(f"GUESS {attempt + 1}")
            print("="*70)
            
            best_guess, score = solver.get_best_guess()
            print(f"\n💡 Suggested next word: {best_guess}")
            print(f"   (Expected information: {score:.2f} bits)")
            
            # Show alternatives
            if remaining > 2:
                print("\n📊 Other good options:")
                # Get a few alternatives
                alternatives = []
                for word in solver.remaining_answers[:5]:
                    if word != best_guess:
                        entropy = solver.calculate_entropy(word, solver.remaining_answers)
                        alternatives.append((word, entropy))
                
                alternatives.sort(key=lambda x: x[1], reverse=True)
                for word, entropy in alternatives[:3]:
                    print(f"   • {word} ({entropy:.2f} bits)")
    
    # If they didn't solve in 6
    print(f"\n{'='*70}")
    print("Out of guesses! Better luck next time! 🎯")
    if solver.remaining_answers:
        print(f"The word might have been one of: {', '.join(sorted(solver.remaining_answers[:5]))}")
    print("="*70)


def auto_random_mode(words, num_tests=10, detailed=True):
    """
    Automatic mode - runs random tests without user interaction
    Set AUTO_RANDOM_MODE = True at top of file to use this
    """
    print_header()
    print("\n🤖 AUTO RANDOM MODE ENABLED")
    print("="*70)
    print(f"Testing solver on {num_tests} random words...")
    print(f"Detailed output: {'Yes' if detailed else 'No'}")
    print("="*70 + "\n")
    
    solver = WordleSolver(words, words)
    results = []
    
    # Pick random words
    test_words = random.sample(words, min(num_tests, len(words)))
    
    for i, answer in enumerate(test_words, 1):
        solver.reset()
        
        if detailed:
            print(f"\n{'='*70}")
            print(f"TEST {i}/{num_tests}: {answer}")
            print("="*70)
            guesses = solver.solve(answer, verbose=True)
        else:
            guesses = solver.solve(answer, verbose=False)
            pattern_str = WordlePattern.pattern_to_string((2,2,2,2,2))
            print(f"{i:2}. {answer} - {len(guesses)} guesses {pattern_str}")
        
        results.append((answer, len(guesses)))
    
    # Show statistics
    print(f"\n{'='*70}")
    print("FINAL RESULTS")
    print("="*70)
    guess_counts = [count for _, count in results]
    avg_guesses = sum(guess_counts) / len(guess_counts)
    
    print(f"\nWords tested: {len(results)}")
    print(f"Average guesses: {avg_guesses:.2f}")
    print(f"Best: {min(guess_counts)} guesses")
    print(f"Worst: {max(guess_counts)} guesses")
    
    # Histogram
    print("\nGuess distribution:")
    for i in range(1, 7):
        count = guess_counts.count(i)
        bar = "█" * count
        percentage = (count / len(results)) * 100
        print(f"  {i} guesses: {bar} ({count} - {percentage:.1f}%)")
    
    # List any failures (>6 guesses - shouldn't happen but just in case)
    failures = [word for word, count in results if count > 6]
    if failures:
        print(f"\n⚠️  Failed to solve in 6 guesses: {', '.join(failures)}")
    
    print(f"\n{'='*70}")
    print("Auto random mode complete! 🎉")
    print("="*70)



def main():
    """Main menu - or auto-run if AUTO_RANDOM_MODE is enabled"""
    # Load word list
    words = load_words()
    if not words:
        return
    
    # Check if auto-random mode is enabled
    if AUTO_RANDOM_MODE:
        # Run automatic random testing
        auto_random_mode(words, num_tests=NUM_RANDOM_TESTS, detailed=SHOW_DETAILED_SOLVE)
        return
    
    # Otherwise, show interactive menu
    print_header()
    
    # Main menu loop
    while True:
        print("\n" + "="*70)
        print("MAIN MENU")
        print("="*70)
        print("\n1. Random Solve - Pick random word and solve it")
        print("2. Batch Test - Test solver on multiple random words")
        print("3. Solve Specific - Choose a word to solve")
        print("4. Analyze Your Game - Analyze your actual Wordle game")
        print("5. Interactive Play - Play with solver assistance")
        print("6. Live Wordle Helper - Use while playing actual Wordle! 🎮")
        print("7. Exit")
        
        choice = input("\nChoice (1-7): ").strip()
        
        if choice == '1':
            mode_random_solve(words)
        elif choice == '2':
            num_tests = input("How many words to test? (default 10): ").strip()
            num_tests = int(num_tests) if num_tests.isdigit() else 10
            mode_random_test_batch(words, num_tests)
        elif choice == '3':
            mode_solve_specific(words)
        elif choice == '4':
            mode_analyze_your_game(words)
        elif choice == '5':
            mode_interactive_play(words)
        elif choice == '6':
            mode_live_wordle_helper(words)
        elif choice == '7':
            print("\nThanks for using Wordle Solver! 🎮")
            break
        else:
            print("\n❌ Invalid choice!")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue!")