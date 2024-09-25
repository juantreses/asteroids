# Asteroids (But Worse)

**Like the classic asteroid game... but worse!**

## Overview

This project is a recreation of the classic arcade game **Asteroids**. You control a spaceship and shoot asteroids (or bubbles, you choose...), which split into smaller pieces.

## Requirements

- **Python 3** is required to run this project.
- The game relies on the **Pygame** library for rendering and game mechanics.

## Setup

1. **Clone this repository** and navigate to the project folder.

2. **Create a virtual environment** at the top level of your project directory:
   ```bash
   python3 -m venv venv
   ```
3. **Activate the virtual environment**:

   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
4. **Install the required dependcies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

To start playing the game, run:
```bash
python3 main.py
```

Enjoy the chaos and try to get a high score!

## How to Play

- **Movement**: Use arrow keys or [Z,Q,S,D] to move the ship (I'm sorry QWERTY users)
- **Shoot**: Press the spacebar to fire at asteroids.
- **Goal**: Destroy all asteroids and avoid collision to survive.

Currently there is a bug where on restart your ship will not be on the screen sometimes. All suggestions as to how to fix this are welcome.
