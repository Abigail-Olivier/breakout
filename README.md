# Breakout Arcade Game

An arcade-style clone of the classic Breakout game built using Pygame. The player controls a paddle to bounce a ball upward, breaking rows of multicolored bricks while managing lives and collecting power-ups.

## Features

* **Directional Ball Reflection:** Implements customized reflection angles based on exactly where the ball strikes the paddle.
* **Visual Particle Effects:** Spawns custom-colored explosion particle fragments whenever a brick is shattered.
* **Randomized Power-Up Drops:** Features a 35% chance to drop temporary, paddle-widening power-ups whenever bricks are destroyed.
* **Leaderboard:** Saves and tracks high score records across distinct game sessions using automatic file input/output processes.

## How to Run

1. Clone this repository or download the source code files.
2. Ensure you have Python 3 and the `pygame` library installed.
3. Run the application from your terminal or IDE:

```bash
python main.py