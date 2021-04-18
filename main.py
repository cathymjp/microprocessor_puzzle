import json

import pygame, sys, random, serial, time
from pygame.locals import *

BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4 # number of rows in the board
TILESIZE = 130
WINDOWWIDTH = 1500
WINDOWHEIGHT = 760
FPS = 70  #프레임 속도
BLANK = None

# 색상 선언      R    G    B
BLACK =      (  0,   0,   0)
WHITE =      (255, 255, 255)
PERIWINKLE = (213, 224, 254)
LIGHTRED =   (255, 115, 105)
GRAY =       ( 92,  90, 104)

#색상 변수 지정
BGCOLOR = PERIWINKLE
TILECOLOR = LIGHTRED
TEXTCOLOR = WHITE
BORDERCOLOR = GRAY
BASICFONTSIZE = 24
BUTTONCOLOR = WHITE
MESSAGECOLOR = GRAY

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 30))) / 2) #x 여백
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 50))) / 2) #y 여백

#방향 변수 선언
UP = 'up' #위
DOWN = 'down' #아래
LEFT = 'left' #왼쪽
RIGHT = 'right' #오른쪽

#시리얼 통신
port = "COM8"
ser = serial.Serial(port, 115200, bytesize=8, parity='N', stopbits=1, timeout=10)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock() #initialize a window for display
    DISPLAYSURF = pygame.display.set_mode((0, 0), FULLSCREEN)
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('C:\Windows\Fonts\Ocraext.ttf', BASICFONTSIZE)

    # New Game option
    NEW_SURF, NEW_RECT = makeText(' New Game  ', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 30, WINDOWHEIGHT + 100)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
    allMoves = [] # list of moves made from the solved configuration

    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide
        msg = 'Move the controller to slide tiles' # contains the message to show in the upper left corner.
        if mainBoard == SOLVEDBOARD:
            msg = 'CONGRATULATIONS! YOU SOLVED THE PUZZLE!!!!'
        drawBoard(mainBoard, msg)

        ser.flushInput()
        str = ser.readline().decode().rstrip().replace("#", "").split(",")
        print(str)
        time.sleep(.4)
        if len(str) > 2:
            if str[0]:
                if str[1]:
                    if (float(str[0]) <= -80.0) and (float(str[0]) >= -100.0):
                        terminate()
                    if (float(str[0]) <= 45.0) and isValidMove(mainBoard, DOWN):
                        slideTo = DOWN
                    elif (float(str[0]) >= 135.0) and isValidMove(mainBoard, UP):
                        slideTo = UP
                    elif (float(str[1]) <= -50.0) and isValidMove(mainBoard, RIGHT):
                        slideTo = RIGHT
                    elif (float(str[1]) >= 40.0) and isValidMove(mainBoard, LEFT):
                        slideTo = LEFT

        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)  # clicked on New Game button
                        allMoves = []
                else:
                    # check if the clicked tile was next to the blank spot
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Move the controller to slide tiles', 12) # show slide on screen; 속도 = 타일 움직이는 속도
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS) #init 부터 지난 시간


#IMU 값 받아오기
def getIMU():
    while True:
        ser.flushInput()
        str = ser.readline().decode().rstrip().replace("#", "").split(",")
        print(str)
        time.sleep(.5)
        getValue(str)

def getValue(list):
    if float(list[0]) <= 40.0:
        return 'down'
    elif float(list[0]) >= 130.0:
        return 'up'
    elif float(list[1]) <= -50.0:
        return 'right'
    elif float(list[1]) >= 50.0:
        return 'left'

#게임 종료
def terminate():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

#보드 순차적으로 정렬시키기
def getStartingBoard():
    # Return a board data structure with tiles in the solved state: [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)

def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX + 170)
    top = YMARGIN + (tileY * TILESIZE) + (tileY + 140)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR) #배경화면 색상
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 280, 175)
        DISPLAYSURF.blit(textSurf, textRect)

    #????????????????
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    #회색 박스 그리기
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 4, top - 4, width + 10, height + 10), 4) #회색 박스

    #메뉴
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)

def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and animate these moves)
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()