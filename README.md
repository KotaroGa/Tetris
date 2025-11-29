
## 🎮 Terminal Tetris

A professional, terminal-based Tetris game built with Python following software engineering best practices.

![Tetris Gameplay](https://img.shields.io/badge/Status-Playable-brightgreen)
![Python](https://img.shields.io/badge/Python-3.6+-blue)
![GitFlow](https://img.shields.io/badge/Workflow-GitFlow-orange)

### ✨ Features

- 🧩 **All 7 classic tetrominoes** with authentic rotation
- 🏆 **NES-accurate scoring** (40/100/300/1200 points)
- 📈 **Level progression** with increasing speed
- ⌨️ **Professional controls** with curses interface
- 🧹 **Line clearing** with blocks falling down
- 🧪 **Test-Driven Development** with comprehensive test suite
- 🔄 **GitFlow workflow** for professional version control

### 🎯 Quick Start

```bash
# Clone the repository
git clone https://github.com/KotaroGa/terminal-tetris.git
cd terminal-tetris

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Play the game!
python -m tetris
