from solver import WordleSolver, WordlePattern
from typing import List, Tuple, Dict
import statistics


class GuessAnalysis:
    """Analysis for a single guess"""
    def __init__(self, guess: str, pattern: Tuple[int, ...], 
                 guess_number: int, remaining_before: int, remaining_after: int):
        self.guess = guess
        self.pattern = pattern
        self.guess_number = guess_number
        self.remaining_before = remaining_before
        self.remaining_after = remaining_after
        self.optimal_guess = None
        self.optimal_entropy = 0.0
        self.actual_entropy = 0.0
        self.skill_rating = 0  # 0-99 scale
        self.alternatives: List[Tuple[str, float]] = []  # Better alternatives


class WordleAnalyzer:
    """Analyzes Wordle gameplay like NYT WordleBot"""
    
    def __init__(self, word_list: List[str], answer_list: List[str] = None):
        self.solver = WordleSolver(word_list, answer_list)
        self.word_list = word_list
        self.answer_list = answer_list or word_list
    
    def analyze_game(self, answer: str, guesses: List[str], 
                     verbose: bool = True) -> Dict:
        """
        Analyze a complete game.
        
        answer: the correct answer
        guesses: list of guesses made by the player
        
        Returns analysis dictionary with statistics and suggestions
        """
        answer = answer.upper()
        guesses = [g.upper() for g in guesses]
        
        self.solver.reset()
        analyses = []
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"WORDLE ANALYSIS - Answer: {answer}")
            print(f"{'='*60}\n")
        
        for i, guess in enumerate(guesses, 1):
            # Get current state
            remaining_before = len(self.solver.remaining_answers)
            pattern = WordlePattern.get_pattern(guess, answer)
            
            # Calculate optimal guess for this state
            optimal_guess, optimal_entropy = self.solver.get_best_guess()
            
            # Calculate entropy for the actual guess
            actual_entropy = self.solver.calculate_entropy(guess, self.solver.remaining_answers)
            
            # Update solver state
            self.solver.make_guess(guess, pattern)
            remaining_after = len(self.solver.remaining_answers)
            
            # Create analysis
            analysis = GuessAnalysis(
                guess=guess,
                pattern=pattern,
                guess_number=i,
                remaining_before=remaining_before,
                remaining_after=remaining_after
            )
            analysis.optimal_guess = optimal_guess
            analysis.optimal_entropy = optimal_entropy
            analysis.actual_entropy = actual_entropy
            analysis.skill_rating = self._calculate_skill_rating(
                actual_entropy, optimal_entropy, remaining_before
            )
            
            # Find top alternatives
            analysis.alternatives = self._find_top_alternatives(
                guess, self.solver.remaining_answers, optimal_guess, top_n=3
            )
            
            analyses.append(analysis)
            
            if verbose:
                self._print_guess_analysis(analysis, i == len(guesses))
            
            # Stop if solved
            if pattern == (2, 2, 2, 2, 2):
                break
        
        # Overall game analysis
        if verbose:
            self._print_overall_analysis(analyses, len(guesses))
        
        return {
            'answer': answer,
            'guesses': guesses,
            'num_guesses': len(guesses),
            'solved': analyses[-1].pattern == (2, 2, 2, 2, 2),
            'analyses': analyses,
            'average_skill': statistics.mean(a.skill_rating for a in analyses),
            'luck_score': self._calculate_luck(analyses)
        }
    
    def _calculate_skill_rating(self, actual_entropy: float, 
                                optimal_entropy: float, remaining: int) -> int:
        """
        Calculate skill rating (0-99) for a guess.
        Similar to NYT WordleBot's rating system.
        """
        if remaining <= 2 or optimal_entropy == 0:
            # If only 1-2 words left, just guessing one is optimal
            return 99 if actual_entropy >= optimal_entropy * 0.95 else 50
        
        # Ratio of actual to optimal entropy
        if optimal_entropy > 0:
            ratio = actual_entropy / optimal_entropy
        else:
            ratio = 0
        
        # Convert to 0-99 scale
        if ratio >= 0.99:
            return 99
        elif ratio >= 0.95:
            return 90 + int((ratio - 0.95) / 0.04 * 9)
        elif ratio >= 0.85:
            return 70 + int((ratio - 0.85) / 0.10 * 20)
        elif ratio >= 0.70:
            return 40 + int((ratio - 0.70) / 0.15 * 30)
        else:
            return max(0, int(ratio / 0.70 * 40))
    
    def _find_top_alternatives(self, actual_guess: str, candidates: List[str],
                              optimal: str, top_n: int = 3) -> List[Tuple[str, float]]:
        """Find top alternative guesses better than the actual guess"""
        if len(candidates) <= 2:
            return []
        
        # Sample words to check (for performance)
        check_pool = self.solver._get_strategic_subset(
            self.solver.all_words, candidates, sample_size=200
        )
        
        alternatives = []
        for word in check_pool:
            if word != actual_guess:
                entropy = self.solver.calculate_entropy(word, candidates)
                alternatives.append((word, entropy))
        
        # Sort by entropy (descending)
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N that are better than actual guess
        actual_entropy = self.solver.calculate_entropy(actual_guess, candidates)
        better_alternatives = [
            (word, ent) for word, ent in alternatives[:top_n]
            if ent > actual_entropy
        ]
        
        return better_alternatives
    
    def _calculate_luck(self, analyses: List[GuessAnalysis]) -> int:
        """
        Calculate luck score (0-99).
        Higher = luckier (reduced candidates more than expected).
        """
        luck_scores = []
        
        for analysis in analyses:
            if analysis.remaining_before <= 2:
                continue
            
            # Expected reduction based on entropy
            if analysis.actual_entropy > 0:
                expected_remaining = analysis.remaining_before / (2 ** analysis.actual_entropy)
            else:
                expected_remaining = analysis.remaining_before
            
            actual_remaining = analysis.remaining_after
            
            # How much better/worse than expected?
            if expected_remaining > 0:
                luck_ratio = expected_remaining / max(actual_remaining, 1)
            else:
                luck_ratio = 1.0
            
            # Convert to score (1.0 = neutral, >1.0 = lucky, <1.0 = unlucky)
            if luck_ratio >= 2.0:
                luck_scores.append(99)
            elif luck_ratio >= 1.5:
                luck_scores.append(75 + int((luck_ratio - 1.5) / 0.5 * 24))
            elif luck_ratio >= 1.0:
                luck_scores.append(50 + int((luck_ratio - 1.0) / 0.5 * 25))
            elif luck_ratio >= 0.5:
                luck_scores.append(25 + int((luck_ratio - 0.5) / 0.5 * 25))
            else:
                luck_scores.append(int(luck_ratio / 0.5 * 25))
        
        return int(statistics.mean(luck_scores)) if luck_scores else 50
    
    def _print_guess_analysis(self, analysis: GuessAnalysis, is_final: bool):
        """Print analysis for a single guess"""
        pattern_str = WordlePattern.pattern_to_string(analysis.pattern)
        
        print(f"Guess {analysis.guess_number}: {analysis.guess} {pattern_str}")
        print(f"  Skill: {analysis.skill_rating}/99", end="")
        
        # Skill description
        if analysis.skill_rating >= 90:
            skill_desc = "Excellent!"
        elif analysis.skill_rating >= 70:
            skill_desc = "Great"
        elif analysis.skill_rating >= 50:
            skill_desc = "Good"
        elif analysis.skill_rating >= 30:
            skill_desc = "OK"
        else:
            skill_desc = "Could be better"
        print(f" ({skill_desc})")
        
        print(f"  Words remaining: {analysis.remaining_before} → {analysis.remaining_after}")
        
        if analysis.remaining_before > 2:
            print(f"  Information gained: {analysis.actual_entropy:.2f} bits")
            
            # Show optimal if different
            if analysis.guess != analysis.optimal_guess:
                print(f"  💡 Optimal guess: {analysis.optimal_guess} "
                      f"({analysis.optimal_entropy:.2f} bits)")
            
            # Show alternatives if any are better
            if analysis.alternatives:
                print(f"  📊 Better alternatives:")
                for alt_word, alt_entropy in analysis.alternatives[:3]:
                    print(f"     • {alt_word} ({alt_entropy:.2f} bits)")
        
        if not is_final and analysis.remaining_after <= 10 and analysis.remaining_after > 1:
            remaining_words = [w for w in self.solver.remaining_answers[:10]]
            candidates_str = ', '.join(remaining_words)
            print(f"  Remaining words: {candidates_str}")
        
        print()
    
    def _print_overall_analysis(self, analyses: List[GuessAnalysis], num_guesses: int):
        """Print overall game analysis"""
        avg_skill = statistics.mean(a.skill_rating for a in analyses)
        luck_score = self._calculate_luck(analyses)
        
        print(f"{'='*60}")
        print(f"OVERALL PERFORMANCE")
        print(f"{'='*60}")
        print(f"Solved in: {num_guesses} guesses")
        print(f"Average skill: {avg_skill:.0f}/99", end=" ")
        
        if avg_skill >= 90:
            print("(Masterful!)")
        elif avg_skill >= 75:
            print("(Expert)")
        elif avg_skill >= 60:
            print("(Strong)")
        elif avg_skill >= 45:
            print("(Solid)")
        else:
            print("(Room for improvement)")
        
        print(f"Luck score: {luck_score}/99", end=" ")
        if luck_score >= 75:
            print("(Very lucky!)")
        elif luck_score >= 60:
            print("(Lucky)")
        elif luck_score >= 40:
            print("(Average luck)")
        else:
            print("(Unlucky)")
        
        # Compare to optimal
        print(f"\n💭 Analysis:")
        
        suboptimal_guesses = [a for a in analyses if a.guess != a.optimal_guess and a.remaining_before > 2]
        if suboptimal_guesses:
            print(f"   • {len(suboptimal_guesses)} guess(es) could be improved")
            worst = min(suboptimal_guesses, key=lambda a: a.skill_rating)
            print(f"   • Guess {worst.guess_number} ({worst.guess}) had the most room for improvement")
        else:
            print(f"   • All guesses were optimal! Perfect play!")
        
        print()
    
    def compare_strategies(self, answer: str, player_guesses: List[str]):
        """Compare player's strategy to optimal strategy"""
        answer = answer.upper()
        
        print(f"\n{'='*60}")
        print("STRATEGY COMPARISON")
        print(f"{'='*60}\n")
        
        # Player's game
        print("YOUR GAME:")
        print("-" * 60)
        player_result = self.analyze_game(answer, player_guesses, verbose=False)
        for i, (guess, analysis) in enumerate(zip(player_guesses, player_result['analyses']), 1):
            pattern_str = WordlePattern.pattern_to_string(analysis.pattern)
            print(f"  {i}. {guess} {pattern_str} (Skill: {analysis.skill_rating}/99)")
        print(f"\nTotal guesses: {len(player_guesses)}")
        print(f"Average skill: {player_result['average_skill']:.0f}/99")
        
        # Optimal game
        print(f"\n{'='*60}")
        print("OPTIMAL STRATEGY:")
        print("-" * 60)
        self.solver.reset()
        optimal_guesses = self.solver.solve(answer, verbose=False)
        for i, (guess, pattern) in enumerate(optimal_guesses, 1):
            pattern_str = WordlePattern.pattern_to_string(pattern)
            print(f"  {i}. {guess} {pattern_str}")
        print(f"\nTotal guesses: {len(optimal_guesses)}")
        
        # Comparison
        print(f"\n{'='*60}")
        guess_diff = len(player_guesses) - len(optimal_guesses)
        if guess_diff == 0:
            print("🎉 You matched the optimal number of guesses!")
        elif guess_diff > 0:
            print(f"📊 You used {guess_diff} more guess(es) than optimal")
        else:
            print(f"🎊 You beat the optimal by {-guess_diff} guess(es)! (Lucky!)")