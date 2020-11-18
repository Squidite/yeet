# This file will only contain the GUI for the simulation and be imported into the backend file as a module or that imported into this, to be decided.

import sqlite3 # This is to create local data bases on the machine for saving and loading simulations
import numpy as np # This is imported like this as numpy convention and so that its easier to type
import pygame
import pygame_gui

fpsLim = 60

# These variables will be used to set the size of the screen and scale the UI to the different sizes
width = 1024
height = 576
widthScale = 0
heightScale = 0

clock = pygame.time.Clock()

# I manually initialise the pygame font modlue so that i can prerender the title font
# for all of the menus instead of doing it for each seperately
pygame.font.init() 
try:
    largeFont = pygame.font.Font("/System/Library/Fonts/Courier.dfont", 72)
    smallFont = pygame.font.Font("/System/Library/Fonts/Courier.dfont", 24)
except:
    largeFont = pygame.font.Font("C:\Windows\Fonts\calibri.ttf", 72)
    smallFont = pygame.font.Font("C:\Windows\Fonts\calibri.ttf", 24)

# SIDE NOT FOR PROJECT WRITE UP frist mistake was not using global variables and thus the width and height variables werent updating for the other windows.
# Then I had to add a dictionary for the screen sizes so that i can access them using the dropdown menus returned value as a key instead of having to cleen the string and spllit it into several inputs
# Dont forget about the shut down 'bug', fixed by clearing up the program with 'raise SystemExit'

def screenSize():
    # This initiates a window with a black background and the title 'Select a screen size'
    
    global width
    global height
    global widthScale
    global heightScale
    
    pygame.init()
    window_surface = pygame.display.set_mode((width, height))
    
    pygame.display.set_caption("Select a screen size")

    background = pygame.Surface((width, height))
    background.fill(pygame.Color("#000000"))

    manager = pygame_gui.UIManager((width, height))

    text = largeFont.render("Select a screen size", True, (182, 182, 182))
    textRect = text.get_rect()
    textRect.center = (width/2, 100)
    
    # These are all the screen size options the user will be able to chose from
    
    options = np.array(["1024x576(Default)","1152x648","1280x720","1366x768","1600x900","1920x1080","2560x1440","3840×2160"], dtype = "str")

    # Matches the selection of the user to a tuple that contains the selected dimensions so I don't have to do any string manipulation
    
    screenSizes = {"1024x576(Default)":(1024, 576), "1152x648":(1152, 648), "1280x720":(1280, 720), "1366x768":(1366, 768),
                  "1600x900":(1600, 900), "1920x1080":(1920, 1080), "2560x1440":(2560, 1440), "3840×2160":(3840,2160)}

    dropDown = pygame_gui.elements.UIDropDownMenu(relative_rect = pygame.Rect((width/2 - 300/2, 200), (300, 25)),
                                                  starting_option = "Select a screen size",
                                                  options_list = options,
                                                  manager = manager)

    confirmButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((width/2 - 150/2, 400), (150, 25)),
                                                 text = "Confirm selection",
                                                 manager = manager)

    is_running = True
    
    while is_running:
        time_delta = clock.tick(30)/1000 # This gets the time since the last frame in seconds and limits the program to 30 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                raise SystemExit

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    chosenSize = event.text
                    
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == confirmButton:
                        x = screenSizes[chosenSize]
                        width, height = x
                        widthScale = width/1024
                        heightScale = height/576
                        pygame.display.quit()
                        mainMenu()

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0,0))

        window_surface.blit(text, textRect)
        
        manager.draw_ui(window_surface)
            
        pygame.display.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def mainMenu():

    pygame.init()
    window_surface = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Creators cosmos")
    background = pygame.image.load("milkyway_bg.png")
    background = pygame.transform.scale(background, (width, height)).convert()

    manager = pygame_gui.UIManager((width, height))

    text = largeFont.render("Creator cosmos", True, (182, 182, 182))
    textRect = text.get_rect()
    textRect.center = (width/2, 100)

    newSimButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 200 * heightScale), (150 * widthScale, 25 * heightScale)),
                                               text = "New Simulation",
                                               manager = manager)
    loadSimButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 250 * heightScale), (150 * widthScale, 25 * heightScale)),
                                                 text = "Load a simulation",
                                                 manager = manager)
    tutorialButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 300 * heightScale), (150 * widthScale, 25 * heightScale)),
                                                   text = "Tutorial",
                                                   manager = manager)
    exitButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 350 * heightScale), (150 * widthScale, 25 * heightScale)),
                                                text = "Exit",
                                                manager = manager)

    is_running = True
    while is_running:
        time_delta = clock.tick(fpsLim)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == newSimButton:
                        newSim(manager, window_surface, background, textRect)
                    elif event.ui_element == loadSimButton:
                        loadSim(manager, window_surface, background, textRect)
                    elif event.ui_element == tutorialButton:
                        print("Load tutorial")
                        tutorial(manager, window_surface, background, textRect)
                    elif event.ui_element == exitButton:
                        pygame.quit()
                        raise SystemExit

# SIDE NOTE FOR PROJECT WRITE UP - just using "pygame.quit()" crshes the program in the screen size select, thus only close the display and then load the next menu
# "raise SystemExit" accomplishes the same as sys.exit() but without needing to import any modules and thus clears up the rest of the prgram and exits the shell
# on the main menu window you can use the "pygame.quit()" because the program will not need to open another window after that, then use "raise SystemExit" to clear up the program and return to shell

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0,0))

        window_surface.blit(text, textRect)
        
        manager.draw_ui(window_surface)
            
        pygame.display.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def newSim(manager, window_surface, background, textRect):

    manager.clear_and_reset()

    pygame.display.set_caption("Create a new simulation")

    text = largeFont.render("New simulation", True, (182, 182, 182))
    textRect.center = (width/2, 100)

    blankSim = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 200 * heightScale), (150 * widthScale, 25 * heightScale)),
                                            text = "Blank simulation",
                                            manager = manager)
    solarSim = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 250 * heightScale), (150 * widthScale, 25 * heightScale)),
                                            text = "Solar System",
                                            manager = manager)
    backToMenu = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 300 * heightScale),(150 * widthScale, 25 * heightScale)),
                                              text = "Main menu",
                                              manager = manager)

    is_running = True
    while is_running:
        time_delta = clock.tick(fpsLim)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == blankSim:
                        simUi(manager, window_surface)
                    elif event.ui_element == solarSim:
                        print("solar sim is working")
                    elif event.ui_element == backToMenu:
                        mainMenu()

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0,0))

        window_surface.blit(text,textRect)

        manager.draw_ui(window_surface)

        pygame.display.update()

def loadSim(manager, window_surface, background, textRect):

    # The files that are sued to 'load' in the drop down menu are just place holders as the part of the program that saves things hasent been created yet and thus can't be tested without them
    # The array that is used to store this temporary test data is also just temporary as for the real progarm it will be generated from the 'savedNames' text file

    manager.clear_and_reset()

    pygame.display.set_caption("Load a simulation")

    text = largeFont.render("Load simulation", True, (182, 182, 182))

    textRect.center = (width/2, 100)

    savedSim = np.array(["sim1", "sim2", "sim3", "sim4", "sim5", "sim6", "sim7"], dtype = "str")

    loadMenu = pygame_gui.elements.UIDropDownMenu(relative_rect = pygame.Rect(((width/2 - (300 * widthScale)/2), 200 * heightScale),(300 * widthScale, 25 * heightScale)),
                                                  starting_option = "Select a save file",
                                                  options_list = savedSim,
                                                  manager = manager)
    confirmChoice  = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 400 * heightScale), (150 * widthScale, 25 * heightScale)),
                                                  text = "Load file",
                                                  manager = manager)
    backToMenu = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 450 * heightScale),(150 * widthScale, 25 * heightScale)),
                                              text = "Main menu",
                                              manager = manager)

    
    is_running = True
    while is_running:
        time_delta = clock.tick(fpsLim)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    saveFile = event.text
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == confirmChoice:
                        #loadFile(saveFile)
                        print("Cofirm button works")
                    elif event.ui_element == backToMenu:
                        mainMenu()

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0,0))

        window_surface.blit(text,textRect)

        manager.draw_ui(window_surface)

        pygame.display.update()

def tutorial(manager, window_surface, background, textRect):

    manager.clear_and_reset()

    text = largeFont.render("Load simulation", True, (182, 182, 182))

    textRect.center = (width/2, 100)

    textBox = pygame_gui.elements.UITextBox(relative_rect = pygame.Rect(((width/2 - (800 * widthScale)/2), 150 * heightScale),(800 * widthScale, 350 * heightScale)),
                                             html_text = "testing text",
                                             manager = manager)
    backToMenu = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 520 * heightScale),(150 * widthScale, 25 * heightScale)),
                                              text = "Main menu",
                                              manager = manager)

    is_running = True
    while is_running:
        time_delta = clock.tick(fpsLim)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == backToMenu:
                        mainMenu()

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0,0))

        window_surface.blit(text,textRect)

        manager.draw_ui(window_surface)


        pygame.display.update()

def textEntry(container, manager, width, height, lat, lon):
    pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect(((lat * widthScale/2 - width * widthScale/2),lon * heightScale),(width * widthScale, height * heightScale)),
                                                                           container = container,
                                                                           manager = manager)

def simUi(manager, window_surface):
                          

    # SIDE NOTE FOR WRITE UP - the clock widget won't update, no solution other than putting it in the loop; the problem with this is that its inefficient and costly to redefine the button every frame
    # Also like this the clock ticks every frame instead of once per second, still need to add a limiter and time scale factor with the second iteration
    # Added UI states for the dynamic containers in the simulatoin, this is so that when the user selects a menu the program can hide the other menues and only show the relevant one
    # Trouble aligning containers - solution was found the same day by looking at the pygame_gui documentation, set panel margines to 0
    # last defined panel is shown until the user clicks the respective button after which the 'prevbutton' gets updated and the active panel can be updated
    # The solution for the above problem was to hide all of the panels before they are rendered so that they would only get activate after the button was clicked
    # Trouble placing text in the appropriate panels with pygame as the rect can't be added to the panel as its handles by a different library
    # The first attempt at replacing the large repetitive block that defines all of the text entry boxes was scrapped becase pygame_gui keeps giving an index must be an int or bool error on the manager.
    # The second attempt will try to create the UI object in a function which takes all of the necessary params which can be put in a loop to create all of the necessary text entry widgets
    # The second attempt is successful and saves about 36 lines of code
   
    # Note for future, replace large if-elif ladders with switchers

    blackground = pygame.Surface((width, height))
    blackground.fill(pygame.Color("#000000"))

    time = 0

    manager.clear_and_reset()

    panelWidth = 310

    mainPanel = pygame_gui.elements.UIPanel(relative_rect = pygame.Rect((5 * widthScale, 5 * heightScale),(panelWidth * widthScale, 565 * heightScale)),
                                            starting_layer_height = 1,
                                            margins = {"left":0, "right":0, "top":0, "bottom":0},
                                            manager = manager)
    selectPanel = pygame_gui.elements.UIPanel(relative_rect = pygame.Rect((5 * widthScale, 130 * heightScale),(panelWidth * widthScale, 370 * heightScale)),
                                              starting_layer_height = 2,
                                              margins = {"left":0, "right":0, "top":0, "bottom":0},
                                              manager = manager)
    createPanel = pygame_gui.elements.UIPanel(relative_rect = pygame.Rect((5 * widthScale, 130 * heightScale), (panelWidth * widthScale, 370 * heightScale)),
                                              starting_layer_height = 2,
                                              margins = {"left":0, "right":0, "top":0, "bottom":0},
                                              manager = manager)
    destroyPanel = pygame_gui.elements.UIPanel(relative_rect = pygame.Rect((5 * widthScale, 130 * heightScale), (panelWidth * widthScale, 370 * heightScale)),
                                               starting_layer_height = 2,
                                               margins = {"left":0, "right":0, "top":0, "bottom":0},
                                               manager = manager)
    enviPanel = pygame_gui.elements.UIPanel(relative_rect = pygame.Rect((5 * widthScale, 130 * heightScale), (panelWidth * widthScale, 370 * heightScale)),
                                            starting_layer_height = 2,
                                            margins = {"left":0, "right":0, "top":0, "bottom":0},
                                            manager = manager)
    savePanel = pygame_gui.elements.UIPanel(relative_rect = pygame.Rect((5 * widthScale, 130 * heightScale), (panelWidth * widthScale, 370 * heightScale)),
                                            starting_layer_height = 2,
                                            margins = {"left":0, "right":0, "top":0, "bottom":0},
                                            manager = manager)
    prevPanel = savePanel

    selectionMenu = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 10 * heightScale),(150 * widthScale, 25 * heightScale)),
                                                 text = "Selection menu",
                                                 container = mainPanel,
                                                 manager = manager)
    createButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 40 * heightScale),(150 * widthScale, 25 * heightScale)),
                                             text = "Create object",
                                             container = mainPanel,
                                             manager = manager)
    destroyButton = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 70 * heightScale),(150 * widthScale, 25 * heightScale)),
                                              text = "Destroy object",
                                              container = mainPanel,
                                              manager = manager)
    enviMenuBtn = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 100 * heightScale),(150 * widthScale, 25 * heightScale)),
                                                  text = "Enviroment menu",
                                                  container = mainPanel,
                                                  manager = manager)
    saveSimBtn = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 495 * heightScale),(150 * widthScale, 25 * heightScale)),
                                              text = "Save simulation",
                                              container = mainPanel,
                                              manager = manager)
    backToMenu = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 525 * heightScale),(150 * widthScale, 25 * heightScale)),
                                              text = "Main menu",
                                              container = mainPanel,
                                              manager = manager)

    temp = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Nepitune", "Uranus"]

    selectDropDown = pygame_gui.elements.UIDropDownMenu(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 300 * widthScale/2), 5 * heightScale),(300 * widthScale, 25 * heightScale)),
                                                        starting_option = "Select an object",
                                                        options_list = temp,
                                                        container = selectPanel,
                                                        manager = manager)
    selectChange = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 360 - 25 * heightScale),(150 * widthScale, 25 * heightScale)),
                                                text = "Select",
                                                container = selectPanel,
                                                manager = manager)
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    createName = createMass = createRadius = createPosx = createPosy = createPosz = createVelx = createVely = createVelz = createSpinx = createSpiny = createSpinz = None
    
    entryBox = np.array([createName,createMass,createRadius,createPosx,createPosy,createPosz,createVelx,createVely,createVelz,createSpinx,createSpiny,createSpinz], dtype = "object")

##    for i in range(12):
##        entryBox[i][0] = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect(((panelWidth * widthScale - 152 * widthScale),(2 + 26 * i) * heightScale),(150 * widthScale, 24 * heightScale)),
##                                                             container = createPanel,
##                                                             manager = manager)

    createName = textEntry(createPanel, manager, 152, 24, panelWidth, 2)
    
        
    nameRect = massRect = radiusRect = posxRect = posyRect = poszRect = velxRect = velyRect = velzRect = spinxRect = spinyRect = spinzRect = colourRect = None

    labels = np.array([[nameRect, "Name :"],[massRect, "Mass (kg) :"],[radiusRect, "Radius (km) :"],[posxRect, "Position, x(km) :"],
                       [posyRect, "Position, y(km) :"],[poszRect, "Position, z(km) :"],[velxRect, "Velocity, x(km/h) :"],
                       [velyRect, "Velocity, y(km/h) :"],[velzRect, "Velocity, z(km/h) :"],[spinxRect, "Spin, x(km/h) :"],
                       [spinyRect, "Spin, y(km/h) :"],[spinzRect, "Spin, z(km/h) :"],[colourRect, "Colour (R,G,B) :"]], dtype = "object")

    for i in range(13):
        labels[i][0] = smallFont.render(labels[i][1], True, (182, 182, 182))
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    destroyDropDown = pygame_gui.elements.UIDropDownMenu(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 300 * widthScale/2), 5 * heightScale),(300 * widthScale, 25 * heightScale)),
                                                        starting_option = "Destroy an object",
                                                        options_list = temp,
                                                        container = destroyPanel,
                                                        manager = manager)
    destroyChange = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(((panelWidth * widthScale/2 - 150 * widthScale/2), 360 - 25 * heightScale),(150 * widthScale, 25 * heightScale)),
                                                text = "Destroy",
                                                container = destroyPanel,
                                                manager = manager)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    saveNameRect = smallFont.render("Save Name :", True, (182, 182, 182))

    saveName = textEntry(savePanel, manager, 152, 24, panelWidth, 2)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    selectPanel.hide()
    createPanel.hide()
    destroyPanel.hide()
    enviPanel.hide()
    savePanel.hide()

    is_running = True
    while is_running:
        time += 1
        time_delta = clock.tick(fpsLim)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == selectionMenu:
                        prevPanel.hide()
                        selectPanel.show()
                        prevPanel = selectPanel
                    elif event.ui_element == createButton:
                        prevPanel.hide()
                        createPanel.show()
                        prevPanel = createPanel
                    elif event.ui_element == destroyButton:
                        prevPanel.hide()
                        destroyPanel.show()
                        prevPanel = destroyPanel
                    elif event.ui_element == enviMenuBtn:
                        prevPanel.hide()
                        enviPanel.show()
                        prevPanel = enviPanel
                    elif event.ui_element == saveSimBtn:
                        prevPanel.hide()
                        savePanel.show()
                        prevPanel = savePanel
                    elif event.ui_element == backToMenu:
                        mainMenu()

                

            manager.process_events(event)

        #clockLen = len(str(time))

        #simClock = pygame_gui.elements.UITextBox(relative_rect = pygame.Rect(((width/2 - (150 * widthScale)/2), 10 * heightScale),(30 + (widthScale + (clockLen * 8.3)), 35)),
        #                                 html_text = str(time),
        #                                 manager = manager)

        manager.update(time_delta)

        window_surface.blit(blackground, (0,0))

        manager.draw_ui(window_surface)

        if prevPanel == createPanel:
            for i in range(13):
                window_surface.blit(labels[i][0], (10 * widthScale, 132 * heightScale + 3 * i + i * 28))
        elif prevPanel == savePanel:
            window_surface.blit(saveNameRect, (10 * widthScale, 132 * heightScale + 3 * 28))
        pygame.display.update()

            
    
        

# There is a list of all modules (that are commented out) so that i can test them indevidually while developing
screenSize()
#mainMenu()
#print(pygame.font.match_font('courier new'))
