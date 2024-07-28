# HCMUS Logistic Co. LTD
Fundamentals of AI - Project 1: Delivery System
This project is a simulation of logistics operations using pathfinding algorithms.

## Project Structure

```
├── assets/  
│   ├── maps/           
│   │    ├── map1.txt          
│   │    ├── map2.txt           
│   │    ├── map3.txt           
│   │    ├── map4.txt           
│   │    └── map5.txt           
│   └── fonts/           
│        ├── Barbra.ttf          
│        ├── Kanit.ttf          
│        ├── Merienda.ttf          
│        └── Pinko.txt          
├── config.py           
├── controller.py           
├── main.py          
├── menu.py          
├── README.md           
├── render.py          
└── requirements.txt
```

## Prerequisites

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Run

1. Navigate to the project directory.

2. Run the main script:
   ```
   python main.py
   ```

3. The program will start, and you'll see the main menu of "HCMUS Logistic Co. LTD".

4. Use the menu to navigate through different options:
   - Start the simulation
   - Adjust settings
   - Quit the program

5. During the simulation:
   - Press SPACE to start pathfinding
   - Press ESC to return to the main menu

## Controls

- Use mouse to navigate through menus
- SPACE: Start pathfinding / Show path
- ESC: Return to main menu / Quit simulation

## Configuration

You can modify game parameters in the `config.py` file, including:
- Screen size
- Colors
- Font sizes
- Game levels

## Additional Information

- The project uses Pygame for rendering graphics and handling user input.
- Different maps are available in the `assets/maps/` directory.
- Custom fonts are stored in the `assets/fonts/` directory.

For more detailed information about the implementation, please refer to the individual Python files in the project.
