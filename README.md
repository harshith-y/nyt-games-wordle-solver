# 🎯 Wordle Solver - Information Theory Approach

An optimal Wordle solver using **information theory** (entropy maximization), inspired by the NYT WordleBot. This isn't just a solver - it's a complete analysis and learning tool!

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🧮 **Information Theory Based** - Uses entropy to maximize information gain
- 🎮 **Live Game Helper** - Use while playing actual Wordle!
- 📊 **Game Analyzer** - Analyze your games like NYT WordleBot
- 🎯 **Skill Ratings** - Get 0-99 skill scores for each guess
- 💡 **Smart Suggestions** - See better alternatives and optimal strategies
- 🎲 **Multiple Modes** - Random testing, batch analysis, interactive play
- 📚 **Educational** - Learn information theory through gameplay!

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/wordle-solver.git
cd wordle-solver
```

### 2. Download Word List

```bash
curl -o wordle_answers.txt https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/wordle-answers-alphabetical.txt
```

### 3. Run

```bash
python main.py
```

## 📖 Usage

### Main Menu

```
1. Random Solve - Pick random word and solve optimally
2. Batch Test - Test solver on multiple random words
3. Solve Specific - Choose a word to solve
4. Analyze Your Game - Get skill ratings and suggestions
5. Interactive Play - Play with solver assistance
6. Live Wordle Helper - Use while playing actual Wordle! 🎮
7. Exit
```

### Mode 6: Live Wordle Helper (Most Useful!)

Use this while playing actual Wordle:

```bash
python main.py
# Choose option 6
```

**How it works:**
1. Get AI suggestion (e.g., RAISE)
2. Enter that word in Wordle
3. Type the colors: `G` for 🟩, `Y` for 🟨, `_` for ⬜
4. Get next optimal suggestion
5. Repeat until solved!

**Example:**
```
💡 Suggested word: RAISE

What word did you guess? raise
What colors did you get? __y_g
✓ Got it: RAISE ⬜⬜🟨⬜🟩

Words remaining: 34
💡 Next suggestion: GLIDE
```

## 🧠 How It Works

### Information Theory

The solver uses **entropy** to measure information gain:

```
H = -Σ(p * log₂(p))
```

For each possible guess:
1. Simulate it against all remaining candidates
2. Calculate what patterns would result
3. Compute entropy (higher = more information)
4. Pick the guess with maximum entropy

### Why This Matters

- **First guess (~5.9 bits):** Narrows 2,315 words → ~50 words
- **Second guess (~3.5 bits):** Narrows 50 words → ~5 words  
- **Third guess (~2.0 bits):** Narrows 5 words → ~1 word

This is the **same algorithm** used by NYT WordleBot!

## 📊 Example Output

```
Guess 1: ARISE ⬜⬜⬜🟩🟩
  Skill: 99/99 (Excellent!)
  Information gained: 5.88 bits
  Words remaining: 2315 → 9

Guess 2: TOUCH ⬜🟩🟩⬜🟨
  Information gained: 3.17 bits
  Words remaining: 9 → 1

Guess 3: HOUSE 🟩🟩🟩🟩🟩
  ✓ Solved in 3 guesses!

OVERALL PERFORMANCE
Solved in: 3 guesses
Average skill: 96/99 (Masterful!)
```

## 📁 Project Structure

```
wordle-solver/
├── main.py              # Interactive interface with 7 modes
├── solver.py            # Core information theory solver
├── analyser.py          # Game analyzer (WordleBot-style)
├── wordle_answers.txt   # Word list (download separately)
├── .gitignore
└── README.md
```

## 🎓 What You'll Learn

This project teaches real computer science concepts:

- **Information Theory** - Entropy, information gain, optimal decisions
- **Search Algorithms** - How to explore solution spaces efficiently
- **Probability** - Expected values, distributions
- **Optimization** - Finding optimal strategies

The same principles power:
- Binary search algorithms
- Machine learning decision trees
- Data compression (Huffman coding)
- AI reasoning systems

## 🔬 Advanced Features

### Analyze Your Games

```python
from analyser import WordleAnalyzer

analyzer = WordleAnalyzer(words, words)
analyzer.analyze_game('HOUSE', ['STARE', 'CLONE', 'HOUSE'])
```

Output:
```
Guess 1: STARE - Skill: 88/99 (Great)
  💡 Optimal: SLATE (5.88 bits)
  
Guess 2: CLONE - Skill: 82/99 (Great)
  💡 Better alternatives: CHILD, WHILE

Average skill: 85/99 (Expert)
Luck score: 55/99 (Average)
```

### Batch Testing

```python
from solver import WordleSolver

solver = WordleSolver(words, words)

for word in test_words:
    solver.reset()
    guesses = solver.solve(word, verbose=False)
    print(f"{word}: {len(guesses)} guesses")
```

### Custom Strategies

Modify scoring in `solver.py`:

```python
# Use expected remaining instead of entropy
score = solver.calculate_expected_remaining(guess, candidates)
```

## 📝 Configuration

At the top of `main.py`:

```python
# Toggle between interactive menu and auto-testing
AUTO_RANDOM_MODE = False

# If True, configure random testing:
NUM_RANDOM_TESTS = 10
SHOW_DETAILED_SOLVE = True
```

## 🎮 Tips

### Best Starting Words
- **RAISE** - 5.879 bits (optimal for this list)
- **ARISE** - 5.879 bits  
- **SLATE** - 5.878 bits (WordleBot's choice)
- **STARE** - 5.876 bits

All within 0.01 bits - essentially tied!

### Playing Strategy
1. Use the Live Helper (Mode 6) while playing
2. Trust the suggestions - they're mathematically optimal
3. Learn from the skill ratings
4. Watch how remaining words decrease

### Understanding Skill Ratings
- **90-99:** Optimal or near-optimal guess
- **70-89:** Very good choice
- **50-69:** Reasonable guess
- **Below 50:** Could be improved

## 🤝 Contributing

Feel free to:
- Add new analysis features
- Implement different strategies
- Add visualizations
- Support Wordle variants

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Inspired by the NYT WordleBot
- Based on information theory principles by Claude Shannon
- Word lists from the official Wordle game

## 📚 Further Reading

- [Information Theory](https://en.wikipedia.org/wiki/Information_theory)
- [Entropy in Game Theory](https://en.wikipedia.org/wiki/Entropy_(information_theory))
- [NYT WordleBot](https://www.nytimes.com/games/wordle/index.html)
- [3Blue1Brown - Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA)

---

**Learn information theory while improving your Wordle game!** 🎓🎮

Made with ❤️ and lots of entropy calculations