# My Fitness Pal - Exercise Progression Tracker

A fitness tracking application with **exercise progression system** that helps you advance from easier to harder exercise variants.

## Features

- **Exercise Progression Chains**: Progress from easier to harder exercise variants
  - Example: Wall Push-ups → Counter Push-ups → Knee Push-ups → Full Push-ups → Diamond Push-ups
- **Workout Planning**: Create and manage workout routines
- **Progress Tracking**: Track your current level in each exercise progression
- **Automatic Progression Suggestions**: Get recommendations when you're ready to advance

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main
```

## Project Structure

```
my-fitness-pal/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── data/           # Exercise data and progressions
│   └── main.py         # Application entry point
├── tests/              # Unit tests
└── requirements.txt
```

## Exercise Progression System

Each exercise belongs to a **progression chain**. As you master an exercise, you can progress to the next, harder variant:

```
Progression Chain Example (Push-ups):
1. Wall Push-ups (Easiest)
2. Counter/Incline Push-ups
3. Knee Push-ups
4. Full Push-ups
5. Diamond Push-ups
6. Archer Push-ups
7. One-arm Push-ups (Hardest)
```

## License

MIT
