
import sys, os, pygame, random, time
pygame.init()

clock = pygame.time.Clock()
gameover = False
scrsize = width,height = 585,415
black = 0,0,0
red = 200, 0, 0
green = 0, 200, 0
gray = (200,200,200)
blue = 0,0,200
bgcolor = (220,220,220)  # light grey
bgcolor2 = (120,120,120)  # dark grey
mines = 0



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

minedisplay = arial.render( str(mines), True, red )
minedisplay_w = minedisplay.get_size()[0]

startxpos = 15
startypos = 45
global xpos
xpos = startxpos
ypos = startypos
size = 15 #15
maxamount = 28 #28
mayamount = 18 #17
dictAvButtonPosOchSize = {}
dictOmPressed = {}
dictAvButtonColor = {}
amountOfMines = 0
global keyToPop
keyToPop = None
global pressedButton
pressedButton = None

#onödiga if statements gö bara svaret till int
if ((maxamount * mayamount) % 5) == 0:
    amountOfMines = (maxamount * mayamount) // 5
    print("DEBUG: Amount Of Mines =", amountOfMines)
elif ((maxamount * mayamount) % 5) != 0:
    amountOfMines =  (maxamount * mayamount + 1) // 5
    print("DEBUG: Amount Of Mines =", amountOfMines)
else:
    print("Error When Making Amount Of Mines")

def buttonObject():

    global xpos
    xpos = startxpos
    ypos = startypos
    ButtonNumber = 0
    for y in range(mayamount):
        jonej = False

        for x in range(maxamount):
            pygame.draw.rect(screen, gray,(xpos,ypos,size,size))
            if random.randint(0, 5) == 3:
                isBomb = True
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
            if haveBeenPressed == True:
                print("pressed: ",haveBeenPressed)
                pygame.draw.rect(screen, buttonColor,(xpos,ypos,size,size))
            elif haveBeenPressed == False:
                pygame.draw.rect(screen, buttonColor,(xpos,ypos,size,size))
            else:
                print("ERROR 132")
            ButtonNumber += 1
            xpos += startxpos + 5
        ypos += startxpos + 5
        xpos = startxpos
        ButtonNumber += 1
#making backround2size------
nnn = 0
for x in range(maxamount): nnn = size + 5
backgrounds2sizex = maxamount * nnn + 5
backgrounds2sizey = mayamount * nnn + 5
#---------------------------
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
    for key, value in dictOmPressed.items():
        dictAvButtonPosOchSize[value].setdefault(value, {"haveBeenPressed": dictOmPressed[value].get("haveBeenPressed")})
        print("value:",value)
        print("key:",key)
    UpdateButtons()
    #buttonObject()
    newdict = {}
    for key, value in dictAvButtonPosOchSize.items():
        thisXpos = dictAvButtonPosOchSize[key].get("Xcord")
        thisYpos = dictAvButtonPosOchSize[key].get("Ycord")
        isBomb = dictAvButtonPosOchSize[key].get("isBomb")
        haveBeenPressed = dictAvButtonPosOchSize[key].get("haveBeenPressed")
        buttonColor = dictAvButtonColor.get(key)
        pygame.draw.rect(screen, buttonColor,(thisXpos,thisYpos,size,size))


        if thisXpos <= mouse[0] <= thisXpos+size and thisYpos <= mouse[1] <= thisYpos+size and gameover == False:
            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT and haveBeenPressed == False:
                #pygame.draw.rect(screen, green, (thisXpos, thisYpos, size, size))
                if dictAvButtonColor.get(key) != red:
                    d2 = {key: blue}
                    dictAvButtonColor.update(d2)
                print("key:",key," | color:",dictAvButtonColor.get(key))
                if isBomb == True and dictAvButtonColor.get(key) != red:
                    print("GameOver")
                    gameover = True
                elif dictAvButtonColor.get(key) != red:
                    pygame.draw.rect(screen, green, (thisXpos, thisYpos, size, size))
                    #dictAvButtonPosOchSize["haveBeenPressed"] = True
                    keyToPop = key
                    pressedButton = True
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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                pygame.draw.rect(screen, red, (thisXpos, thisYpos, size, size))
                if dictAvButtonColor.get(key) == red and dictAvButtonColor.get(key) != blue:
                    d1 = {key: gray}
                elif dictAvButtonColor.get(key) != blue:
                    d1 = {key: red}

                dictAvButtonColor.update(d1)
                print("key:",key," | color:",dictAvButtonColor.get(key))
                time.sleep(0.2)
    for key, value in dictOmPressed.items():
        dictAvButtonPosOchSize[value].setdefault(value, {"haveBeenPressed": dictOmPressed[value].get("haveBeenPressed")})
        print("value:",value)
        print("key:",key)

    thisXpos = 0
    thisYpos = 0
    isBomb = False
    # if mouse is hovered on a button it
    # changes to lighter shade
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
    #draw things after this

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

    pygame.display.update()
    if not changed:
        clock.tick(60) # limit to 60 fps