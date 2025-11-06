# Wordle Solver - Information Theory Approach 🎯

A Python implementation inspired by NYT WordleBot that uses information theory to optimally solve Wordle and analyze your gameplay!

## Quick Start

```bash
python demo.py
```

## What You've Built

### Core Files

1. **`wordle_solver.py`** - The brain of the operation
   - `WordlePattern`: Generates feedback patterns (🟩🟨⬜)
   - `WordleConstraints`: Tracks what we know about the answer
   - `WordleSolver`: Uses entropy to find optimal guesses

2. **`wordle_analyzer.py`** - Like NYT WordleBot
   - Analyzes your guesses
   - Gives skill ratings (0-99)
   - Suggests better alternatives
   - Calculates luck score

3. **`demo.py`** - See it in action

## The Information Theory Magic ✨

### What is Entropy?

**Entropy = Measure of Uncertainty**

```python
# If you have 8 equally likely candidates:
entropy = log₂(8) = 3 bits

# After a good guess, you might have 2 candidates left:
new_entropy = log₂(2) = 1 bit

# Information gained = 3 - 1 = 2 bits!
```

### How the Solver Works

```
For each possible guess:
  1. Simulate it against all remaining candidates
  2. See what patterns it produces
  3. Count how many words remain for each pattern
  4. Calculate entropy: -Σ(p * log₂(p))
  5. Pick the guess with HIGHEST entropy!
```

**Example:**
- 100 candidates remain
- Guess A might split them: [50, 30, 20] 
- Guess B might split them: [25, 25, 25, 25]
- Guess B has higher entropy → better guess!

### Why This Works

The key insight: **Even splits give maximum information**

- Worst case: [99, 1] → You learn almost nothing
- Best case: [50, 50] or [25, 25, 25, 25] → Maximum info

This is the same math behind:
- Binary search algorithms
- 20 Questions game  
- Decision trees in ML
- Data compression

## Example Output

```
Guess 1: SLATE 🟨⬜⬜⬜🟩
  Skill: 95/99 (Excellent!)
  Information gained: 5.82 bits
  Words remaining: 2309 → 34

Guess 2: HORSE ⬜🟩⬜🟨🟩
  Skill: 88/99 (Great)
  Information gained: 3.21 bits
  Words remaining: 34 → 4

OVERALL: Solved in 3 guesses
Average skill: 92/99 (Expert)
```

## Usage

### Solve a Word

```python
from wordle_solver import WordleSolver

words = ['SLATE', 'HOUSE', 'MOUSE', ...]
solver = WordleSolver(words, words)
solver.solve('MOUSE', verbose=True)
```

### Analyze Your Game

```python
from wordle_analyzer import WordleAnalyzer

analyzer = WordleAnalyzer(words, words)
your_guesses = ['STARE', 'HOUSE', 'MOUSE']
analyzer.analyze_game('MOUSE', your_guesses)
analyzer.compare_strategies('MOUSE', your_guesses)
```

## Key Concepts

### Skill Rating (0-99)
Compares your guess's entropy to the optimal guess:
- 90-99: Excellent!
- 70-89: Great
- 50-69: Good  
- 30-49: OK
- 0-29: Needs work

### Luck Score (0-99)
Did you eliminate more/fewer words than expected?
- 75+: Very lucky!
- 60-74: Lucky
- 40-59: Average
- 0-39: Unlucky

### Information Gained (bits)
- First guess: ~5 bits (narrows 2000+ words to ~50)
- Middle guesses: ~3 bits  
- Final guesses: ~1-2 bits

## Getting Word Lists

You need:
1. **Answers** (~2300 words): Possible Wordle solutions
2. **Valid guesses** (~12000 words): All accepted words

Find these online or from the Wordle source code. For now, the demo uses a small list.

## Advanced Features

### Hard Mode
Only guess from remaining candidates:
```python
solver.get_best_guess(use_hard_mode=True)
```

### Custom Metrics
Instead of entropy, minimize expected remaining:
```python
score = solver.calculate_expected_remaining(guess, candidates)
```

## Why Information Theory?

This isn't just a Wordle solver - it's a window into how:
- Search algorithms work (binary search)
- Machine learning makes decisions (decision trees)
- Data gets compressed (Huffman coding)
- AI systems reason under uncertainty

**Learning Wordle = Learning Computer Science fundamentals!**

## Next Steps

Ideas to extend this:
- Add visualization of the decision tree
- Implement different solving strategies
- Add multiplayer analysis (comparing players)
- Create a web interface
- Analyze Wordle statistics over time
- Add support for Wordle variants (6-letter, etc.)

## Resources

- **NYT WordleBot**: https://www.nytimes.com/games/wordle/index.html
- **Information Theory**: Claude Shannon's papers
- **Entropy in games**: 3Blue1Brown videos on YouTube

---

Built to learn information theory through Wordle! 🎓🎮
