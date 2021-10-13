
import sys, os, pygame, random, time

startprint = """MineSweeper
Minesweeper in python with pygame.(finished not polished)
If you lost right click with mouse to restart"""


def maine():
    pygame.init()
    print(startprint)
    clock = pygame.time.Clock()
    gameover = False
    scrsize = width,height = 585,415
    black = 0,0,0
    red = 200, 0, 0
    green = 0, 200, 0
    gray = (200,200,200)
    blue = 0,0,200
    yellow = 200, 200, 0
    purple = 200, 0, 200
    orange = 255, 128, 0
    brown = 100, 51, 0
    brown1 = 100, 52, 0
    brown2 = 100, 53, 0
    bgcolor = (220,220,220)  # light grey
    bgcolor2 = (120,120,120)  # dark grey
    mines = 80

    mineAmount = [0]

    LEFT = 1
    RIGHT = 3

    isBomb = False
    # to get the true full-screen size, do this BEFORE pygame.display.set_mode:
    fullscreen_sz = pygame.display.Info().current_w, pygame.display.Info().current_h
    print( 'screen size =', fullscreen_sz )


    # ---------- This works under Windows Vista, no promises elsewhere! ----------
    # initially center the pygame window by setting %SDL_VIDEO_WINDOW_POS%
    win_pos_left = 1 + ((fullscreen_sz[0] - width) // 2)
    win_pos_top = 1 + ((fullscreen_sz[1] - height) // 2)
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{0},{1}'.format(win_pos_left, win_pos_top)
    # ----------------------------------------------------------------------------

    screen = pygame.display.set_mode(scrsize, pygame.RESIZABLE)

    # ----------------------------------------------------------------------------
    os.environ['SDL_VIDEO_WINDOW_POS'] = ''
    # if you don't clear the environment variable, the window will reposition
    # every time pygame.display.set_mode() gets called due to a VIDEORESIZE event.
    # ----------------------------------------------------------------------------

    arial = pygame.font.SysFont( 'arial,microsoftsansserif,courier', 14 )
    txt2display = arial.render( "Minesweeper", True, black )
    txt2display_w = txt2display.get_size()[0]

    timedisplay = arial.render( "timeHere", True, black )
    timedisplay_w = timedisplay.get_size()[0]

    minedisplay = arial.render( str(mineAmount[0]), True, red )
    minedisplay_w = minedisplay.get_size()[0]

    amountDisplay = arial.render( str(1), True, red )
    amountDisplay_w = amountDisplay.get_size()[0]
    font_name = pygame.font.match_font('arial')
    startxpos = 15
    startypos = 45
    global xpos
    xpos = startxpos
    ypos = startypos
    size = 15 #15
    maxamount = 28 #28
    mayamount = 18 #18
    dictAvButtonPosOchSize = {}
    dictOmPressed = {}
    dictAvButtonColor = {}
    amountOfMines = 0
    global keyToPop
    keyToPop = None
    global pressedButton
    pressedButton = None
    numberOfTile = 0

    one = 1
    two = maxamount + 1
    three = maxamount - 1
    four = maxamount + 2
    five = maxamount - 2

    seed = {}
    """
    #onödiga if statements gö bara svaret till int
    if ((maxamount * mayamount) % 5) == 0:
        amountOfMines = (maxamount * mayamount) // 5
        print("DEBUG: Amount Of Mines =", amountOfMines)
    elif ((maxamount * mayamount) % 5) != 0:
        amountOfMines =  (maxamount * mayamount + 1) // 5
        print("DEBUG: Amount Of Mines =", amountOfMines)
    else:
        print("Error When Making Amount Of Mines")
    """
    def SeedGen():
        Amount = maxamount * mayamount
        butnumba = 0
        for xu in range(mayamount):

            for yu in range(maxamount):
                if random.randint(0, 5) == 1:
                    ss = {butnumba: 1}
                    seed.update(ss)
                else:
                    ss = {butnumba: 0}
                    seed.update(ss)
                butnumba += 1
            butnumba += 1
        bombamonta = 0
        for key, value in seed.items():
            if value == 1:
                bombamonta += 1

        if bombamonta != mines:
            SeedGen()
        else:
            print(seed)

    SeedGen()

    def buttonObject():

        global xpos
        xpos = startxpos
        ypos = startypos
        ButtonNumber = 0
        for y in range(mayamount):
            jonej = False

            for x in range(maxamount):
                pygame.draw.rect(screen, gray,(xpos,ypos,size,size))
                if seed[ButtonNumber] == 1:
                    isBomb = True
                    mineAmount[0] += 1
                else:
                    isBomb = False
                dictAvButtonPosOchSize.setdefault(ButtonNumber, {"Xcord": xpos,"Ycord": ypos, "size": size, "isBomb": isBomb, "haveBeenPressed": jonej})
                dd = {ButtonNumber: gray}
                dictAvButtonColor.update(dd)
                ButtonNumber += 1
                xpos += startxpos + 5
            ypos += startxpos + 5
            xpos = startxpos
            ButtonNumber += 1
        print("amount of mines:", mineAmount[0])
        minedisplay = arial.render( str(mineAmount[0]), True, red )

    def UpdateButtons():
        global xpos
        xpos = startxpos
        ypos = startypos
        ButtonNumber = 0


        for x in range(mayamount):

            thisXpos = dictAvButtonPosOchSize[ButtonNumber].get("Xcord")
            thisYpos = dictAvButtonPosOchSize[ButtonNumber].get("Ycord")
            isBomb = dictAvButtonPosOchSize[ButtonNumber].get("isBomb")

            for x in range(maxamount):
                buttonColor = dictAvButtonColor.get(ButtonNumber)
                haveBeenPressed = dictAvButtonPosOchSize[ButtonNumber].get("haveBeenPressed")

                if buttonColor == bgcolor2:
                    checkTiles(ButtonNumber)

                if haveBeenPressed == True:
                    print("pressed: ",haveBeenPressed)
                    pygame.draw.rect(screen, buttonColor,(xpos,ypos,size,size))

                elif haveBeenPressed == False and buttonColor != bgcolor2:
                    pygame.draw.rect(screen, buttonColor,(xpos,ypos,size,size))

                else:
                    pass
                    #print("ERROR 132")
                ButtonNumber += 1
                xpos += startxpos + 5

            ypos += startxpos + 5
            xpos = startxpos
            ButtonNumber += 1

    def draw_text(surface, text, size, color, x, y):
        """Draw text to surface

           surface - Pygame surface to draw to
           text    - string text to draw
           size    - font size
           color   - color of text
           x       - x position of text on surface
           y       - y position of text on surface
        """
        #amountDisplay = arial.render( str(1), True, red )
        #screen.blit( amountDisplay, ((scrsize[1]+100+amountDisplay_w)//10,200) )
        font = pygame.font.Font(font_name, 14)
        text_surf = arial.render(str(text), True, color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (int(x + size/3), y) # I use topleft here because that makes sense to me
                                   # for English (unless you want it centered).
                                   # But you can use any part of the rect to start drawing the text
        surface.blit(text_surf, text_rect)
    #making backround2size------
    nnn = 0
    for x in range(maxamount): nnn = size + 5
    backgrounds2sizex = maxamount * nnn + 5
    backgrounds2sizey = mayamount * nnn + 5
    #---------------------------
    def floodFill(key, numberOfTile):
        """
        d3 = {key: bgcolor2}
        dictAvButtonColor.update(d3)
        """
        if isBomb != True and dictAvButtonColor.get(key) != red:

            #print(checkTiles2(key))
            if checkTiles2(key) == 0:
                d5 = {key: bgcolor2}
                dictAvButtonColor.update(d5)

                abc = checkTiles2(key + 1)
                if abc == 0:
                    d5 = {key + 1: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key + 1, 0)
                else:
                    tileChange(key + 1, abc)

                abc2 = checkTiles2(key - 1)
                if abc2 == 0:
                    d5 = {key - 1: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key - 1, 0)
                else:
                    tileChange(key - 1, abc2)

                abc3 = checkTiles2(key + maxamount + 1)
                if abc3 == 0:
                    d5 = {key + maxamount + 1: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key + maxamount + 1, 0)
                else:
                    tileChange(key + maxamount + 1, abc3)

                abc4 = checkTiles2(key - maxamount - 1)
                if abc4 == 0:
                    d5 = {key - maxamount - 1: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key - maxamount - 1, 0)
                else:
                    tileChange(key - maxamount - 1, abc4)

                abc5 = checkTiles2(key + maxamount + 2)
                if abc5 == 0:
                    d5 = {key + maxamount + 2: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key + maxamount + 2, 0)
                else:
                    tileChange(key + maxamount + 2, abc5)

                abc6 = checkTiles2(key - maxamount)
                if abc6 == 0:
                    d5 = {key - maxamount: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key - maxamount, 0)
                else:
                    tileChange(key - maxamount, abc6)

                abc7 = checkTiles2(key - maxamount - 2)
                if abc7 == 0:
                    d5 = {key - maxamount - 2: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key - maxamount - 2, 0)
                else:
                    tileChange(key - maxamount - 2, abc7)

                abc8 = checkTiles2(key + maxamount)
                if abc8 == 0:
                    d5 = {key + maxamount: bgcolor2}
                    dictAvButtonColor.update(d5)
                    #floodFill2(key + maxamount, 0)
                else:
                    tileChange(key + maxamount, abc8)

    def checkTiles2(key):
        d2 = {key: blue}
        numberOfTile = 0
        try:
            try:
                #print("DEBUG: Tile", key + 1, "isBomb =",dictAvButtonPosOchSize[key + 1].get("isBomb"))
                #print("DEBUG: Tile Check 1")
                if dictAvButtonPosOchSize[key + 1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + 1, "does not exist")
                print("DEBUG: Tile Check 1")
                """
            try:
                #print("DEBUG: Tile", key - 1, "isBomb =",dictAvButtonPosOchSize[key - 1].get("isBomb"))
                #print("DEBUG: Tile Check 2")
                if dictAvButtonPosOchSize[key - 1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - 1, "does not exist")
                print("DEBUG: Tile Check 2")
                """

            try:
                #print("DEBUG: Tile", key + maxamount + 1, "isBomb =",dictAvButtonPosOchSize[key + maxamount + 1].get("isBomb"))
                #print("DEBUG: Tile Check 3")
                if dictAvButtonPosOchSize[key + maxamount +1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + maxamount +1, "does not exist")
                print("DEBUG: Tile Check 3")
                """

            try:
                #print("DEBUG: Tile", key - maxamount - 1, "isBomb =",dictAvButtonPosOchSize[key - maxamount - 1].get("isBomb"))
                #print("DEBUG: Tile Check 4")
                if dictAvButtonPosOchSize[key - maxamount -1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - maxamount -1, "does not exist")
                print("DEBUG: Tile Check 4")
                """

            try:
                #print("DEBUG: Tile", key + 2 + maxamount, "isBomb =",dictAvButtonPosOchSize[key + 2 + maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 5")
                if dictAvButtonPosOchSize[key + 2 + maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + 2 + maxamount, "does not exist")
                print("DEBUG: Tile Check 5")
                """

            try:
                #print("DEBUG: Tile", key - maxamount, "isBomb =",dictAvButtonPosOchSize[key - maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 6")
                if dictAvButtonPosOchSize[key - maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - maxamount, "does not exist")
                print("DEBUG: Tile Check 6")
                """

            try:
                #print("DEBUG: Tile", key - 2 - maxamount, "isBomb =",dictAvButtonPosOchSize[key - 2 - maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 7")
                if dictAvButtonPosOchSize[key - 2 - maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - 2 - maxamount, "does not exist")
                print("DEBUG: Tile Check 7")
                """

            try:
                #print("DEBUG: Tile", key + maxamount, "isBomb =",dictAvButtonPosOchSize[key + maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 8")
                if dictAvButtonPosOchSize[key + maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + maxamount, "does not exist")
                print("DEBUG: Tile Check 8")
                """


            return numberOfTile

        except:
            print("Error when checking nearby tiles")
            #time.sleep(1)

    def checkTiles(key):
        d2 = {key: blue}
        numberOfTile = 0
        try:
            try:
                #print("DEBUG: Tile", key + 1, "isBomb =",dictAvButtonPosOchSize[key + 1].get("isBomb"))
                #print("DEBUG: Tile Check 1")
                if dictAvButtonPosOchSize[key + 1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + 1, "does not exist")
                print("DEBUG: Tile Check 1")
                """

            try:
                #print("DEBUG: Tile", key - 1, "isBomb =",dictAvButtonPosOchSize[key - 1].get("isBomb"))
                #print("DEBUG: Tile Check 2")
                if dictAvButtonPosOchSize[key - 1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - 1, "does not exist")
                print("DEBUG: Tile Check 2")
                """

            try:
                #print("DEBUG: Tile", key + maxamount + 1, "isBomb =",dictAvButtonPosOchSize[key + maxamount + 1].get("isBomb"))
                #print("DEBUG: Tile Check 3")
                if dictAvButtonPosOchSize[key + maxamount +1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + maxamount +1, "does not exist")
                print("DEBUG: Tile Check 3")
                """

            try:
                #print("DEBUG: Tile", key - maxamount - 1, "isBomb =",dictAvButtonPosOchSize[key - maxamount - 1].get("isBomb"))
                #print("DEBUG: Tile Check 4")
                if dictAvButtonPosOchSize[key - maxamount -1].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - maxamount -1, "does not exist")
                print("DEBUG: Tile Check 4")
                """

            try:
                #print("DEBUG: Tile", key + 2 + maxamount, "isBomb =",dictAvButtonPosOchSize[key + 2 + maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 5")
                if dictAvButtonPosOchSize[key + 2 + maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + 2 + maxamount, "does not exist")
                print("DEBUG: Tile Check 5")
                """

            try:
                #print("DEBUG: Tile", key - maxamount, "isBomb =",dictAvButtonPosOchSize[key - maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 6")
                if dictAvButtonPosOchSize[key - maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - maxamount, "does not exist")
                print("DEBUG: Tile Check 6")
                """

            try:
                #print("DEBUG: Tile", key - 2 - maxamount, "isBomb =",dictAvButtonPosOchSize[key - 2 - maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 7")
                if dictAvButtonPosOchSize[key - 2 - maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key - 2 - maxamount, "does not exist")
                print("DEBUG: Tile Check 7")
                """

            try:
                #print("DEBUG: Tile", key + maxamount, "isBomb =",dictAvButtonPosOchSize[key + maxamount].get("isBomb"))
                #print("DEBUG: Tile Check 8")
                if dictAvButtonPosOchSize[key + maxamount].get("isBomb") == True:
                    numberOfTile = numberOfTile + 1

            except:
                pass
                """
                print(key + maxamount, "does not exist")
                print("DEBUG: Tile Check 8")
                """


            tileChange(key, numberOfTile)

        except:
            print("Error when checking nearby tiles")
            #time.sleep(1)

    def tileChange(key, numberOfTile):
        #print(numberOfTile)
        if numberOfTile == 0 and dictAvButtonColor.get(key) != red:
            d2 = {key: bgcolor2}
            dictAvButtonColor.update(d2)
            floodFill(key, numberOfTile)
        elif numberOfTile == 1 and dictAvButtonColor.get(key) != red:
            d2 = {key: blue}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 2 and dictAvButtonColor.get(key) != red:
            d2 = {key: green}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 3 and dictAvButtonColor.get(key) != red:
            d2 = {key: orange}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 4 and dictAvButtonColor.get(key) != red:
            d2 = {key: purple}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 5 and dictAvButtonColor.get(key) != red:
            d2 = {key: yellow}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 6 and dictAvButtonColor.get(key) != red:
            d2 = {key: brown}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 7 and dictAvButtonColor.get(key) != red:
            d2 = {key: brown1}
            dictAvButtonColor.update(d2)
        elif numberOfTile == 8 and dictAvButtonColor.get(key) != red:
            d2 = {key: brown2}
            dictAvButtonColor.update(d2)
        else:
            print("more than 6 mines, making it brown for now")
            d2 = {key: brown}
            dictAvButtonColor.update(d2)

        dictAvButtonColor.update(d2)
        numberOfTile = 0
        #time.sleep(1) #for debugging so I can read the logs

    buttonObject()

    while True:
        changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.VIDEORESIZE:
                scrsize = event.size  # or event.w, event.h
                screen = pygame.display.set_mode(scrsize,pygame.RESIZABLE)
                changed = True


        screen.fill( bgcolor )
        #The rectangle for background under the buttons
        pygame.draw.rect(screen, bgcolor2,(10,40,backgrounds2sizex,backgrounds2sizey))

        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        thisXpos = 0
        thisYpos = 0
        isBomb = False
        """
        for key, value in dictOmPressed.items():
            dictAvButtonPosOchSize[value].setdefault(value, {"haveBeenPressed": dictOmPressed[value].get("haveBeenPressed")})

            print("value:",value)
            print("key:",key)
        """
        UpdateButtons()
        #buttonObject()

        newdict = {}
        for key, value in dictAvButtonPosOchSize.items():
            thisXpos = dictAvButtonPosOchSize[key].get("Xcord")
            thisYpos = dictAvButtonPosOchSize[key].get("Ycord")
            isBomb = dictAvButtonPosOchSize[key].get("isBomb")
            haveBeenPressed = dictAvButtonPosOchSize[key].get("haveBeenPressed")
            buttonColor = dictAvButtonColor.get(key)
            #pygame.draw.rect(screen, buttonColor,(thisXpos,thisYpos,size,size))

            number = 0

            if buttonColor == blue:
                number = 1
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == green:
                number = 2
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == yellow:
                number = 5
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == orange:
                number = 3
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == purple:
                number = 4
                draw_text(screen, number, size, blue, thisXpos,thisYpos)
            elif buttonColor == brown:
                number = 6
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == brown1:
                number = 7
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == brown2:
                number = 8
                draw_text(screen, number, size, red, thisXpos,thisYpos)
            elif buttonColor == gray:
                pass
            elif buttonColor == bgcolor2:
                pass
            else:
                number = 0
                draw_text(screen, number, size, red, thisXpos,thisYpos)


            if thisXpos <= mouse[0] <= thisXpos+size and thisYpos <= mouse[1] <= thisYpos+size and gameover == False:
                if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT and haveBeenPressed == False:
                    #pygame.draw.rect(screen, green, (thisXpos, thisYpos, size, size))
                    if isBomb != True and dictAvButtonColor.get(key) != red:
                        checkTiles(key)
                    #print("key:",key," | color:",dictAvButtonColor.get(key))
                    if isBomb == True and dictAvButtonColor.get(key) != red:
                        print("GameOver")
                        gameover = True
                    """
                    elif dictAvButtonColor.get(key) != red:
                        pygame.draw.rect(screen, green, (thisXpos, thisYpos, size, size))
                        #dictAvButtonPosOchSize["haveBeenPressed"] = True
                        keyToPop = key
                        pressedButton = True
                        try:
                        if thisXpos != startxpos:
                            if thisYpos != startypos:
                                if dictAvButtonPosOchSize[key + 1].get("isBomb") == False:
                                    if dictAvButtonPosOchSize[key - 1].get("isBomb") == False:
                                        if dictAvButtonPosOchSize[key + 1 + maxamount].get("isBomb") == False:
                                            if dictAvButtonPosOchSize[key + maxamount].get("isBomb") == False:
                                                if dictAvButtonPosOchSize[key - maxamount].get("isBomb") == False:
                                                    if dictAvButtonPosOchSize[key - 1 - maxamount].get("isBomb") == False:
                                                        if dictAvButtonPosOchSize[key - 2 - maxamount].get("isBomb") == False:
                                                            if dictAvButtonPosOchSize[key + maxamount].get("isBomb") == False:
                                                                if dictAvButtonPosOchSize[key - 2 + maxamount].get("isBomb") == False:
                                                                    print("negher")
                        elif thisYpos == startypos:
                            pass
                        elif thisXpos == startxpos:
                            pass
                        elif thisYpos != startypos:
                            if thisXpos != startxpos:
                                pass
                            elif thisXpos == startxpos:
                                pass
                        elif thisYpos == startypos:
                            pass

                        break
                    """
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    pygame.draw.rect(screen, red, (thisXpos, thisYpos, size, size))
                    if dictAvButtonColor.get(key) == red:
                        d1 = {key: gray}
                        dictAvButtonColor.update(d1)
                        mineAmount[0] += 1
                    elif dictAvButtonColor.get(key) == gray:
                        d1 = {key: red}
                        dictAvButtonColor.update(d1)
                        mineAmount[0] -= 1
                    #print("key:",key," | color:",dictAvButtonColor.get(key))
                    time.sleep(0.2)

        """
        for key, value in dictOmPressed.items():
            dictAvButtonPosOchSize[value].setdefault(value, {"haveBeenPressed": dictOmPressed[value].get("haveBeenPressed")})

            print("value:",value)
            print("key:",key)

        """

        thisXpos = 0
        thisYpos = 0
        isBomb = False
        # if mouse is hovered on a button it
        # changes to lighter shade

        """
        if pressedButton == True:
            thisXpos = dictAvButtonPosOchSize[keyToPop].get("Xcord")
            thisYpos = dictAvButtonPosOchSize[keyToPop].get("Ycord")
            isBomb = dictAvButtonPosOchSize[keyToPop].get("isBomb")
            print(keyToPop)
            dictAvButtonPosOchSize.setdefault(keyToPop, {"Xcord": thisXpos,"Ycord": thisYpos, "size": size, "isBomb": isBomb, "haveBeenPressed": True})
        for key, value in dictAvButtonPosOchSize.items():
            haveBeenPressed = dictAvButtonPosOchSize[key].get("haveBeenPressed")
            if haveBeenPressed == True:
                pygame.draw.rect(screen, blue, (thisXpos, thisYpos, size, size))
                print("G")
        pressedButton = False
        """
        #draw things after this
        minedisplay = arial.render( str(mineAmount[0]), True, red )
        screen.blit( txt2display, ((scrsize[0]+1-txt2display_w)//2,1) )  # at top-center of screen
        screen.blit( timedisplay, ((scrsize[0]+1-timedisplay_w)+ 1,1) )
        screen.blit( minedisplay, ((scrsize[0]+1-minedisplay_w)//200,1) )

        if gameover == True:
            for key, value in dictAvButtonPosOchSize.items():
                thisXpos = dictAvButtonPosOchSize[key].get("Xcord")
                thisYpos = dictAvButtonPosOchSize[key].get("Ycord")
                isBomb = dictAvButtonPosOchSize[key].get("isBomb")
                if isBomb == True:
                    pygame.draw.rect(screen, black, (thisXpos, thisYpos, size, size))


        if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT and gameover == True:
            maine()


        pygame.display.update()
        if not changed:
            clock.tick(60) # limit to 60 fps
maine()
