
import random, time, pygame, sys
from pygame.locals import *

FPS = 25
STARTTIME = 0 # for timer
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE)/2)
TOPMARGIN = WINDOWHEIGHT-(BOARDHEIGHT*BOXSIZE)-5

#For mute
MUTE = 0
# Color definitions
WHITE = (255,255,255)
GRAY = (185,185,185)
BLACK = (0,0,0)
PINK = (249,32,142)
LIGHTPINK = (255,52,162)
ORANGE = (251,86,49)
LIGHTORANGE = (255,106,69)
YELLOW = (254,189,6)
LIGHTYELLOW = (255,209,26)
YELLOWISH_GREEN= (113,189,49)
LIGHTYELLOWIS_GREEN = (189,252,162)
VIOLET = (143,52,183)
LIGHTVIOLET = (163,72,203)
SEMI_GRAY = (157,157,157)
LIGHTSEMI_GRAY = (177,177,177)
B_COLOR = (10,226,213)

BORDERCOLOR = B_COLOR
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR=GRAY
COLORS=(PINK,ORANGE,YELLOW,YELLOWISH_GREEN,VIOLET,SEMI_GRAY)
LIGHTCOLORS=(LIGHTPINK,LIGHTORANGE,LIGHTYELLOW,LIGHTYELLOWIS_GREEN,LIGHTVIOLET,LIGHTSEMI_GRAY)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, FRAMECOUNT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('PrStart.ttf', 18)
    BIGFONT = pygame.font.SysFont('PrStart.ttf', 100)
    pygame.display.set_caption('TETRIS')

    showTextScreen(" ")
    while True: # game loop
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('videogames1.mp3')
        else:
            pygame.mixer.music.load('videogames2.mp3')
        pygame.mixer.music.play(-1, 0.0)
        pygame.time.delay(100)
        runGame()
        pygame.mixer.music.stop()
        ending = pygame.image.load('start_ending.png')
        DISPLAYSURF.blit(ending, (0, 0))
        showTextScreen('THE END')


def runGame():
    global MUTE
    pygame.time.delay(1000)
    # setup variable for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    framecount = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece() # the block in play, starting value
    nextPiece = getNewPiece() # the block on deck, starting value

    while True: # main game loop
        if fallingPiece == None:
            pygame.time.delay(250)
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over pal

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game

                    pause_display = pygame.image.load('CHANGE.png')
                    DISPLAYSURF.blit(pause_display, (0, 0))
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('cheer_up.mp3')
                    pygame.mixer.music.play(-1, 0.0)
                    showTextScreen('pause') # pause until a key press
                    pygame.time.delay(100)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                # stopping left, right, and down movement when releasing button
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False
                elif (event.key == K_m):
                    if(MUTE == 0):
                        MUTE = 1
                        pygame.mixer.music.pause()
                    else:
                        MUTE = 0
                        pygame.mixer.music.unpause()
            elif event.type == KEYDOWN:
                # moving the block sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1): # adjX=-1 checks 1 space to the left of the block (adjusted)
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1): # adjX=1 checks 1 space to the right of the block (adjusted)
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating block (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    # moves to next value in rotation index (% part rolls over value to zero if it exceeds total number of possible rotations)
                    # e.g. 3%4 = 3, 4%4 = 0, 5%4 = 1. Remember, 4 rotations are counted 0-3 because COMPUTERS!
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):                                                        # if rotating puts it somewhere illegal...
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])  # ... rotate it the other way!
                elif (event.key == K_b): #rotate the other direction (flip the script)
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = fallingPiece['rotation'] + 1 % len(PIECES[fallingPiece['shape']])
                # fast falling with down
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 2 #move the block down two spaces
                    lastMoveDownTime = time.time()
                # move the current block all the way down
                elif event.key == K_SPACE or event.key == K_END:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the block because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the block down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # TIMER LOGIC
        # http://programarcadegames.com/python_examples/f.php?file=timer.py
        # Calculate total seconds
        total_seconds = STARTTIME - (framecount // FPS)
        if total_seconds < 0:
            total_seconds = 0
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
        # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level, output_string)
        drawNextPiece(nextPiece)
        left_side = pygame.image.load('left_side.png')
        right_side = pygame.image.load('right_side.png')
        DISPLAYSURF.blit(left_side, (0, 0))
        DISPLAYSURF.blit(right_side, (428, 280))
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        framecount += 1
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN event to remove them from the event queue.
    # SEE WORMY CHAPTER!!
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    if(text == 'pause'):
        # Draw the text drop shadow
        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)-52)
        DISPLAYSURF.blit(titleSurf, titleRect)
        # Draw the text
        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 55)
        DISPLAYSURF.blit(titleSurf, titleRect)
    else:
        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))
        DISPLAYSURF.blit(titleSurf, titleRect)


        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH/2) - 3, int(WINDOWHEIGHT/2) - 3)
        DISPLAYSURF.blit(titleSurf, titleRect)

    if(text == ' '):
        initial_diplay = pygame.image.load('start_ending.png')
        DISPLAYSURF.blit(initial_diplay, (0, 0))
        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = makeTextObjs(' ', BASICFONT, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2) + 100)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    elif(text == 'THE END'):
        pressKeySurf, pressKeyRect = makeTextObjs('Do you want to play again? Press any key to ROCK!', BASICFONT, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    else:
        pressKeySurf, pressKeyRect = makeTextObjs('Press any key to ROCK!', BASICFONT,
                                                  TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()
    pygame.mixer.music.stop()
    if random.randint(0, 1) == 0:
        pygame.mixer.music.load('videogames1.mp3')
    else:
        pygame.mixer.music.load('videogames2.mp3')
    pygame.mixer.music.play(-1, 0.0)
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02) # fallFrequency will be less than 0 at level 14. This is maximum speed, updating as fast as the game loop.
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1), #random rotation value between 0 and one less than total possible rotations for shape
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, #start it above the board (less than zero)
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece

def addToBoard(board, piece):
    # fill in the board based on the piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range (TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:    # if a space on the board is not empty (because a block is there)...
                board[x + piece['x']][y + piece['y']] = piece['color']      # ... add that piece as solid in the board data structure.

def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line is filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 #start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY - 1]
            # Set very top line to blank.
            # Since pullDown function copies row value down one row, the top row must be cleared or it will just be copied.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also complete, it will be removed.
        else:
            y -= 1 #move on to the check the next row up.
    return numLinesRemoved

def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has 4 boxes) at xy coordinates on the board.
    # Or, if pixelx and pixely are specified, draw to the pixel coordinates stored in pixelx and pixely (for "Next" piece)
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawStatus(score, level, output_string):
    # draw the score text
    scoreSurf = BASICFONT.render('Lines: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # draw the timer
    #timerSurf = BASICFONT.render(output_string, True, TEXTCOLOR)
    #timerRect = timerSurf.get_rect()
    #timerRect.topleft = (WINDOWWIDTH - 150, 250)
    #DISPLAYSURF.blit(timerSurf, timerRect)

    FPSCLOCK.tick(FPS)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx and pixely haven't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the blocks that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox (None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    main()

