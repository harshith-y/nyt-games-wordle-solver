import math
from collections import defaultdict, Counter
from typing import List, Set, Tuple, Dict


class WordlePattern:
    """Represents a Wordle feedback pattern"""
    GRAY = 0   # Letter not in word
    YELLOW = 1 # Letter in word, wrong position
    GREEN = 2  # Letter in correct position
    
    @staticmethod
    def get_pattern(guess: str, answer: str) -> Tuple[int, ...]:
        """
        Generate the pattern for a guess against an answer.
        Returns a tuple of 5 integers (0=gray, 1=yellow, 2=green)
        
        Handles duplicate letters correctly (like real Wordle)
        """
        pattern = [WordlePattern.GRAY] * 5
        answer_letters = list(answer)
        
        # First pass: mark greens
        for i in range(5):
            if guess[i] == answer[i]:
                pattern[i] = WordlePattern.GREEN
                answer_letters[i] = None  # Mark as used
        
        # Second pass: mark yellows
        for i in range(5):
            if pattern[i] == WordlePattern.GRAY and guess[i] in answer_letters:
                pattern[i] = WordlePattern.YELLOW
                # Remove first occurrence of this letter
                answer_letters[answer_letters.index(guess[i])] = None
        
        return tuple(pattern)
    
    @staticmethod
    def pattern_to_string(pattern: Tuple[int, ...]) -> str:
        """Convert pattern to emoji string for display"""
        emoji_map = {0: '⬜', 1: '🟨', 2: '🟩'}
        return ''.join(emoji_map[p] for p in pattern)
    
    @staticmethod
    def pattern_to_text(pattern: Tuple[int, ...]) -> str:
        """Convert pattern to text for non-emoji terminals"""
        text_map = {0: '_', 1: 'Y', 2: 'G'}
        return ''.join(text_map[p] for p in pattern)


class WordleConstraints:
    """Tracks constraints from guesses"""
    
    def __init__(self):
        self.correct_positions: Dict[int, str] = {}  # position -> letter
        self.present_letters: Set[str] = set()  # letters that must be in word
        self.position_excludes: Dict[int, Set[str]] = defaultdict(set)  # position -> excluded letters
        self.absent_letters: Set[str] = set()  # letters not in word
    
    def add_guess(self, guess: str, pattern: Tuple[int, ...]):
        """Update constraints based on a guess and its pattern"""
        for i, (letter, result) in enumerate(zip(guess, pattern)):
            if result == WordlePattern.GREEN:
                self.correct_positions[i] = letter
                self.present_letters.add(letter)
            elif result == WordlePattern.YELLOW:
                self.present_letters.add(letter)
                self.position_excludes[i].add(letter)
            else:  # GRAY
                # Only mark as absent if it's not marked as present elsewhere
                if letter not in self.present_letters:
                    self.absent_letters.add(letter)
    
    def matches(self, word: str) -> bool:
        """Check if a word satisfies all constraints"""
        # Check correct positions
        for pos, letter in self.correct_positions.items():
            if word[pos] != letter:
                return False
        
        # Check all present letters are in the word
        for letter in self.present_letters:
            if letter not in word:
                return False
        
        # Check position excludes (yellows)
        for pos, excluded in self.position_excludes.items():
            if word[pos] in excluded:
                return False
        
        # Check absent letters
        for letter in self.absent_letters:
            if letter in word:
                return False
        
        return True


class WordleSolver:
    """Main solver using information theory"""
    
    def __init__(self, word_list: List[str], answer_list: List[str] = None):
        """
        Initialize solver with word lists.
        word_list: all valid guesses
        answer_list: possible answers (subset of word_list if provided)
        """
        self.all_words = [w.upper() for w in word_list if len(w) == 5]
        self.answers = [w.upper() for w in (answer_list or word_list) if len(w) == 5]
        self.constraints = WordleConstraints()
        self.remaining_answers = self.answers.copy()
        self.guess_history: List[Tuple[str, Tuple[int, ...]]] = []
    
    def calculate_entropy(self, guess: str, candidates: List[str]) -> float:
        """
        Calculate expected information (entropy) for a guess.
        Higher entropy = more information gained on average.
        """
        if not candidates:
            return 0.0
        
        # Group candidates by the pattern they would produce
        pattern_counts = defaultdict(int)
        for answer in candidates:
            pattern = WordlePattern.get_pattern(guess, answer)
            pattern_counts[pattern] += 1
        
        # Calculate entropy: -sum(p * log2(p))
        total = len(candidates)
        entropy = 0.0
        for count in pattern_counts.values():
            if count > 0:
                probability = count / total
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def get_best_guess(self, candidates: List[str] = None, 
                       use_hard_mode: bool = False,
                       max_words_to_check: int = 500) -> Tuple[str, float]:
        """
        Find the best guess using information theory.
        
        candidates: list of possible answers (uses self.remaining_answers if None)
        use_hard_mode: if True, only consider guesses from remaining candidates
        max_words_to_check: limit search space for performance
        
        Returns (best_word, entropy_score)
        """
        if candidates is None:
            candidates = self.remaining_answers
        
        if len(candidates) <= 2:
            # If only 1-2 words left, just guess one of them
            return candidates[0], 0.0
        
        # Determine which words to consider as guesses
        if use_hard_mode:
            guess_pool = candidates
        else:
            # In easy mode, can guess from all valid words
            guess_pool = self.all_words
        
        # For performance, limit search if candidate pool is large
        if len(guess_pool) > max_words_to_check:
            # Sample words with good letter coverage
            guess_pool = self._get_strategic_subset(guess_pool, candidates, max_words_to_check)
        
        best_guess = None
        best_score = -1
        
        for guess in guess_pool:
            # Use entropy as the scoring metric
            score = self.calculate_entropy(guess, candidates)
            
            # Tie-breaker: prefer words that are possible answers
            if guess in candidates:
                score += 0.001
            
            if score > best_score:
                best_score = score
                best_guess = guess
        
        return best_guess, best_score
    
    def _get_strategic_subset(self, guess_pool: List[str], 
                             candidates: List[str], sample_size: int = 500) -> List[str]:
        """Get a strategic subset of words to consider (for performance)"""
        # Always include remaining candidates
        subset = set(candidates)
        
        # Add common first guesses
        starter_words = ['SOARE', 'SLATE', 'CRANE', 'SLANT', 'TRACE', 'CRATE', 'ARISE', 'STARE']
        subset.update(w for w in starter_words if w in guess_pool)
        
        # Add words with high letter frequency
        letter_freq = Counter()
        for word in candidates:
            letter_freq.update(set(word))
        
        # Score words by letter frequency
        def score_word(word):
            return sum(letter_freq[letter] for letter in set(word))
        
        scored_words = sorted(guess_pool, key=score_word, reverse=True)
        subset.update(scored_words[:sample_size])
        
        return list(subset)
    
    def make_guess(self, guess: str, pattern: Tuple[int, ...]) -> List[str]:
        """
        Update solver state with a guess and its pattern.
        Returns the new list of remaining candidates.
        """
        guess = guess.upper()
        self.guess_history.append((guess, pattern))
        self.constraints.add_guess(guess, pattern)
        
        # Filter remaining answers
        self.remaining_answers = [
            word for word in self.remaining_answers 
            if self.constraints.matches(word)
        ]
        
        return self.remaining_answers
    
    def solve(self, answer: str, max_guesses: int = 6, 
              verbose: bool = True) -> List[Tuple[str, Tuple[int, ...]]]:
        """
        Solve for a specific answer.
        Returns the list of (guess, pattern) pairs.
        """
        answer = answer.upper()
        self.reset()
        guesses = []
        
        for attempt in range(1, max_guesses + 1):
            # Get best guess
            guess, score = self.get_best_guess()
            pattern = WordlePattern.get_pattern(guess, answer)
            
            if verbose:
                pattern_str = WordlePattern.pattern_to_string(pattern)
                print(f"Guess {attempt}: {guess} {pattern_str}")
                print(f"  Information gain: {score:.3f} bits")
            
            guesses.append((guess, pattern))
            
            # Check if solved
            if pattern == (2, 2, 2, 2, 2):
                if verbose:
                    print(f"✓ Solved in {attempt} guesses!")
                break
            
            # Update state
            self.make_guess(guess, pattern)
            
            if verbose:
                print(f"  Remaining candidates: {len(self.remaining_answers)}")
                if len(self.remaining_answers) <= 10:
                    print(f"  Possibilities: {', '.join(self.remaining_answers[:10])}")
            
            if verbose:
                print()
        
        return guesses
    
    def reset(self):
        """Reset solver state"""
        self.constraints = WordleConstraints()
        self.remaining_answers = self.answers.copy()
        self.guess_history = []


def load_word_list(filename: str) -> List[str]:
    """Load words from a file (one word per line)"""
    try:
        with open(filename, 'r') as f:
            words = [line.strip().upper() for line in f if len(line.strip()) == 5]
        return words
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        print(f"Make sure the file is in the same directory as this script.")
        return []
    except Exception as e:
        print(f"Error loading word list: {e}")
        return []