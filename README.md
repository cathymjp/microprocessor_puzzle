# Number Puzzle
Number puzzle game using an EBIMU controller

## Environment
- 2020.3 ~ 2020.6 (3 months)
- Python3
- pygame
- Microprocessor


## Microprocessor Tools
- EBIMU-9DOFV4 (3-axis gyroscope, 3-axis acceleration sensor, 3-axis accelerometer sensor)
  - pitch, yaw, roll
- USB2UART
- Serial 
- myCortex-STM32F4
- Comport Master (Program)


## Description
- Move the EBIMU controller in four directions to sovle the number puzzle. Starting from a stable position, the program reads roll and pitch movement. When the controller is in stop motion for 0.5 seconds, the game moves the number tiles according to the movement of the controller.

<img src="https://user-images.githubusercontent.com/45842934/216951906-25a6e581-ebff-4b18-aa4d-0e4285f01cda.png" height=300 />


Code Reference: https://itsourcecode.com/free-projects/python-projects/puzzle-game-in-python-with-source-code/
