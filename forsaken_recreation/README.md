# Forsaken Py

A Python-based local multiplayer asymmetric horror game inspired by Roblox's Forsaken.

## Requirements
- Python 3.12+
- Pygame

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play
1. Run the game:
   ```bash
   python forsaken_recreation/main.py
   ```

   OR, if you prefer a single-file script:
   ```bash
   python forsaken_recreation/forsaken_game.py
   ```

2. **Controls**:
   - **Menu**: Arrow keys to navigate, Enter to select.
   - **Lobby**:
     - Player 1 (Left): WASD to change character, Space to Ready.
     - Player 2 (Right): Arrows to change character, Enter to Ready.
   - **Game**:
     - **Survivor (P1)**: WASD to move, Q for Ability (Sprint).
     - **Killer (P2)**: Arrows to move, RShift for Ability.

## Goal
- **Killer**: Catch the Survivor (touch them) 3 times.
- **Survivor**: Run away! (Objectives to be added).
