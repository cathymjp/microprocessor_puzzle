# BounceBall
Number puzzle game using EBIMU sensors

## Environment
- 2020.1 ~ 2020.12 (12 months)
- Python3
- pygame
- Microprocessor


## Tools
- EBIMU-9DOFV4 (3-axis gyroscope, 3-axis acceleration sensor, 3-axis accelerometer sensor)
  - pitch, yaw, roll
  - x, y, z
- USB2UART
- serial 
  - Baudrate: 115200
- myCortex-STM32F4
- Comport Master (Program)


## Description
- Use EBIMU controller to sovle the number puzzle by moving the sensor in four directions. Starting at the location of the controller as the game starts, the program reads yaw and pitch movement. After holding the controller in stop motion for 3 seconds, the game moves the number according to the movmenet of the controller. 
