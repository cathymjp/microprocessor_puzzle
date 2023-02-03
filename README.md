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
  - x, y, z
- USB2UART
- Serial 
- myCortex-STM32F4
- Comport Master (Program)


## Description
- Use EBIMU controller to sovle the number puzzle by moving the sensor in four directions. Starting at the location of the controller as the game starts, the program reads yaw and pitch movement. After holding the controller in stop motion for 3 seconds, the game moves the number according to the movmenet of the controller. 
1. Start the gmae
2. Hold the device in still position
3. Make a move to solve to puzzle
4. wait for 3 seconds
5. Repeat steps 3 and 4 until the puzzle is solved
