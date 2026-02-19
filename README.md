# Hex's Scientific Calculator

A fully-featured scientific calculator application built with Python and Kivy. This calculator provides advanced mathematical functions, graphing capabilities, and a clean, modern interface with theme support.

## Features

### Core Calculator Functions
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Scientific functions (trigonometry, logarithms, exponents, factorials)
- Constants (pi, e)
- Parentheses for complex expressions
- Answer memory (Ans) for chaining calculations
- Calculation history with ability to recall past results

### Advanced Mathematical Operations
- Trigonometric functions (sin, cos, tan)
- Inverse trigonometric functions (sin⁻¹, cos⁻¹, tan⁻¹)
- Hyperbolic functions (sinh, cosh, tanh)
- Logarithms (base 10, natural log)
- Powers and roots (square, cube, nth power, nth root)
- Exponential functions (e^x, 10^x)
- Factorial calculations

### Graphing Capabilities
- Plot custom functions (f(x) mode)
- Plot x/y coordinate pairs
- Support for mathematical expressions (e.g., x(2x+1), 3xsin(4x), xcos(2x))
- Range specification with syntax: `range(start,end,step)`

### User Interface
- Dark and light theme support (toggle with Style button)
- Custom title bar with app icon
- Scrollable calculation history panel
- Responsive button design with visual feedback
- Graph plotting popup windows
- Copyable results and equations

## Installation

### Prerequisites
- Python 3.x
- pip package manager

### Required Dependencies
```bash
pip install kivy
pip install matplotlib  # For graphing functionality
```

### Application Structure
The application consists of the following main components:
- `Main.py` - The main application file (this script)
- `backend.py` - Backend module containing calculation and graphing logic
- `resources/` - Directory containing font files and icons
  - `DejaVuSans-Bold.ttf` - Primary font
  - `Segoe UI Emoji.TTF` - Emoji font for special characters
  - `icon.png` - Application icon

## Usage

### Basic Operations
1. Launch the application
2. Use the keypad to input expressions
3. Press `=` to calculate the result
4. Results appear in the answer field and are saved to history

### Special Functions
- **AC** - Clear all input
- **⌫** - Delete last character
- **Ans** - Insert previous answer
- **%** - Percentage calculation
- **x!** - Factorial
- **1/x** - Reciprocal
- **x²** / **x³** - Square / Cube
- **xʸ** - Raise to power y
- **²√x** / **³√x** - Square root / Cube root
- **ln** / **log₁₀** - Natural log / Base-10 log
- **eˣ** / **×10ˣ** - Exponential / Scientific notation
- **sin**, **cos**, **tan** - Basic trigonometry
- **sinh**, **cosh**, **tanh** - Hyperbolic functions

### Graphing
The calculator offers two graphing modes:

#### Plot Mode (Plot button)
Enter comma-separated x and y values:
- X-axis: 1,2,3,4
- Y-axis: 10,20,30,40

#### Function Mode (f(x) button)
Enter a function and x-values:
- Function: x(2x+1)
- X-axis: 1,2,3,4  or  range(1,70,10)

The range syntax: `range(start,end,step)` generates a sequence of values.

### Theme Switching
Click the **Style** button to toggle between dark and light themes. The application will restart automatically to apply the new theme.

### History Management
- All calculations are automatically saved to history
- Click any history item to reload it into the calculator
- Use the trash button (🗑️) to clear all history

## Technical Details

### Backend Module (backend.py)
The application relies on a backend module that provides:
- `calculate(expression, ans)` - Evaluates mathematical expressions
- `get_history()` - Retrieves calculation history
- `write_history(expression)` - Saves calculations to history
- `del_history()` - Clears all history
- `plot(data)` - Generates plots using matplotlib
- `fx(function, x_values)` - Evaluates functions for graphing
- `read_theme()` / `write_theme(theme)` - Theme management
- Process management functions for clean shutdown

### Keyboard Input
The calculator uses on-screen buttons. Physical keyboard input is not directly supported but can be implemented by extending the application.

### Window Properties
- Fixed size: 900 x 600 pixels
- Custom title bar
- Rounded corners on all UI elements
- Smooth color transitions for button states

## Troubleshooting

### Common Issues

**Graphing doesn't work**
- Ensure matplotlib is installed: `pip install matplotlib`
- Check that x and y arrays have the same length
- Verify function syntax is valid

**Theme change doesn't apply**
- The application automatically restarts to apply themes
- Ensure write permissions in the application directory

**History not saving**
- Check write permissions for the database file
- Verify backend module is properly imported

**Application won't start**
- Verify all dependencies are installed
- Check that font files exist in the resources directory
- Ensure Python path includes the application directory

## File Structure
```
calculator_app/
├── Main.py                 # Main application file
├── backend.py              # Backend logic module
├── resources/              # Resource directory
│   ├── DejaVuSans-Bold.ttf
│   ├── Segoe UI Emoji.TTF
│   └── icon.png
└── README.md               # This file
```

## Credits
Developed by Hex as a scientific calculator application with advanced mathematical capabilities and graphing features.

## License
This project is for educational and personal use. All rights reserved.
