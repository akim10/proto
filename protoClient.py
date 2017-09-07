import socket
from _thread import *
from queue import Queue
from tkinter import *
import string
import pickle
import math

print("connected to server")
HOST = ''
PORT = 6887

class User(object):
    def __init__(self, elements):
        self.elements = elements

class Selector(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.top = self.y - self.height
        self.left = self.x - self.width
        self.right = self.x + self.width
        self.bottom = self.y + self.height

    def __eq__(self, other):
        return (isinstance(other, Selector) and (self.x == other.x) and 
            self.y == other.y and self.color == other.color)

    def __repr__(self):
        return 'Selector %d %d %s' % (self.x, self.y, self.color)

class TextBox(Selector):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color)
        self.top = self.y - self.height
        self.left = self.x - self.width
        self.right = self.x + self.width
        self.bottom = self.y + self.height
        self.text = text
        self.type = 'textBox'
        self.fontSize = ''

    def draw(self, canvas, xOffset=0):
        width = (self.right - self.left) / 2
        height = (self.bottom - self.top) / 2
        canvas.create_polygon((self.left + xOffset, self.top), (self.right + 
            xOffset, self.top), (self.right + xOffset, self.bottom),
        (self.left + xOffset, self.bottom), 
        fill=self.color, outline = 'black', width=2)
        canvas.create_text(self.x + xOffset, self.y, 
            text = self.text, font = 'Helvetica ' + self.fontSize)

class Buttonn(TextBox):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)
        self.type = 'button'
        self.linkedTo = None

    def draw(self, canvas, xOffset=0):
        shadowOffset = 4
        canvas.create_polygon((self.left + shadowOffset + xOffset, self.top + 8
            + shadowOffset), (self.left + 1 + shadowOffset + xOffset, self.top +
             4.5+ shadowOffset), (self.left + 2 + shadowOffset + xOffset, 
             self.top + 3+ shadowOffset), (self.left + 4.5 + shadowOffset + 
             xOffset, self.top + 1+ shadowOffset), (self.left + 8 + shadowOffset
              + xOffset, self.top+ shadowOffset),
            (self.right - 8 + shadowOffset + xOffset, self.top), (self.right - 5
             + shadowOffset + xOffset, self.top + 1), (self.right - 2 + 
             shadowOffset + xOffset, self.top + 3), (self.right - 1 + 
             shadowOffset + xOffset, self.top + 4.5), (self.right + shadowOffset
              + xOffset, self.top + 8+ shadowOffset), 
            (self.right + shadowOffset + xOffset, self.bottom - 8+ shadowOffset)
            ,(self.right - 1 + shadowOffset + xOffset, self.bottom - 4.5+ 
                shadowOffset),(self.right - 2 + shadowOffset + xOffset, 
                self.bottom - 3+ shadowOffset),(self.right - 4 + shadowOffset + 
                xOffset, self.bottom - 1+ shadowOffset),(self.right - 8 + 
                shadowOffset + xOffset, self.bottom+ shadowOffset),
            (self.left + 8 + shadowOffset + xOffset, self.bottom+ shadowOffset),
             (self.left + 4.5 + shadowOffset + xOffset, self.bottom - 1+ 
                shadowOffset), (self.left + 2 + shadowOffset + xOffset, 
                self.bottom - 3+ shadowOffset), (self.left + 1 + shadowOffset 
                + xOffset, self.bottom - 4+ shadowOffset), (self.left + 
                shadowOffset + xOffset, self.bottom - 8+ shadowOffset),
            fill='light grey',)
        canvas.create_polygon((self.left + xOffset, self.top + 8),(self.left
         + 1 + xOffset, self.top + 4.5), (self.left + 2 + xOffset, self.top 
         + 3), (self.left + 4.5 + xOffset, self.top + 1), (self.left + 8 + 
         xOffset, self.top),(self.right - 8 + xOffset, self.top),(self.right
          - 5 + xOffset, self.top + 1), (self.right - 2 + xOffset, self.top 
          + 3), (self.right - 1 + xOffset, self.top + 4.5), (self.right + 
          xOffset, self.top + 8), (self.right + xOffset, self.bottom - 8),
          (self.right - 1 + xOffset, self.bottom - 4.5),(self.right - 2 + 
            xOffset, self.bottom - 3),(self.right - 4 + xOffset, self.bottom
             - 1),(self.right - 8 + xOffset, self.bottom),(self.left + 8 + 
             xOffset, self.bottom), (self.left + 4.5 + xOffset, self.bottom
              - 1), (self.left + 2 + xOffset, self.bottom - 3), (self.left 
              + 1 + xOffset, self.bottom - 4), (self.left + xOffset, 
              self.bottom - 8),fill=self.color, outline = 'black', width=2)
        canvas.create_text(self.x + xOffset, self.y, text = self.text)

class Slider(Selector):
    def __init__(self, x, y, width, height, color, radius):
        super().__init__(x, y, width, height, color)
        self.r = radius
        self.type = 'slider'
        self.cx = self.x # have centers for circle independent of the rectangle
        self.cy = self.y
        self.slidColor = 'gray18'

    def draw(self, canvas, xOffset=0):
        shadowOffset = 2.75
        canvas.create_polygon((self.left + xOffset, self.top + 3.5), (self.left 
            + xOffset, self.top + 1.75), (self.left + 0.5 + xOffset, self.top + 
            0.75), (self.left + 1.75 + xOffset, self.top), (self.left + 3.5 + 
            xOffset, self.top),(self.right - 3.5 + xOffset,self.top),(self.right
             - 2 + xOffset, self.top), (self.right - 0.5 + xOffset, self.top +1)
            , (self.right + xOffset, self.top + 1.75), (self.right + xOffset, 
            self.top + 3.5), (self.right + xOffset, self.bottom-3.5),(self.right
             + xOffset, self.bottom - 1.75),(self.right - 0.5 + xOffset, 
             self.bottom - 1),(self.right - 1.5+xOffset,self.bottom),(self.right
              - 3.5 + xOffset, self.bottom),(self.left+3.5+xOffset,self.bottom),
            (self.left + 1.75 + xOffset, self.bottom ), (self.left + 0.5 + 
            xOffset, self.bottom - 1), (self.left + xOffset, self.bottom - 1.5),
            (self.left + xOffset, self.bottom - 3.5),
            fill='white', outline = 'black', width = 2)
        canvas.create_polygon((self.left + xOffset, self.top + 3.5), (self.left 
            + xOffset, self.top + 1.75), (self.left + 0.5 + xOffset, self.top + 
            0.75), (self.left + 1.75 + xOffset, self.top), (self.left + 3.5 + 
            xOffset, self.top),(self.cx - 3.5 + xOffset, self.top), (self.cx - 2
            + xOffset, self.top), (self.cx - 0.5 + xOffset, self.top + 1), 
            (self.cx + xOffset, self.top + 1.75), (self.cx + xOffset, self.top + 
            3.5), (self.cx + xOffset, self.bottom - 3.5),(self.cx + xOffset, 
            self.bottom - 1.75),(self.cx - 0.5 + xOffset,self.bottom-1),(self.cx
             - 1.5 + xOffset, self.bottom),(self.cx - 3.5 +xOffset,self.bottom),
            (self.left + 3.5 + xOffset, self.bottom), (self.left + 1.75+xOffset,
            self.bottom ), (self.left + 0.5 + xOffset, self.bottom-1),(self.left
             + xOffset, self.bottom - 1.5), (self.left+xOffset,self.bottom-3.5),
            fill=self.slidColor, outline = 'black', width = 2)
        canvas.create_oval(self.cx - self.r+xOffset,self.cy-self.r+shadowOffset,
        self.cx + self.r + xOffset, self.cy + self.r+ shadowOffset, 
        fill='light grey', width=0)

        canvas.create_oval(self.cx - self.r + xOffset, self.cy - self.r, self.cx
         + self.r + xOffset, self.cy + self.r, fill=self.color, width=2)

class DropDown(TextBox):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)
        self.type = 'dropdown'
        self.opened = False
        self.text = text
        self.shownText = text

    def draw(self, canvas, xOffset=0):
        canvas.create_polygon((self.left + xOffset, self.top + 8), (self.left+1 
        + xOffset, self.top + 4.5), (self.left + 2  + xOffset, self.top + 3), 
        (self.left + 4.5  + xOffset, self.top + 1), (self.left + 8  + xOffset, 
        self.top),(self.right - 8  + xOffset, self.top), (self.right -5+xOffset,
         self.top + 1), (self.right - 2  + xOffset, self.top + 3), (self.right-1
        + xOffset, self.top + 4.5), (self.right+xOffset,self.top+8),(self.right 
        + xOffset, self.bottom - 8),(self.right - 1 + xOffset, self.bottom-4.5),
        (self.right - 2  + xOffset, self.bottom - 3),(self.right - 4  + xOffset,
         self.bottom - 1),(self.right - 8  + xOffset, self.bottom),(self.left+8 
        + xOffset, self.bottom), (self.left + 4.5 + xOffset, self.bottom - 1), 
        (self.left + 2  + xOffset, self.bottom - 3), (self.left + 1  + xOffset, 
        self.bottom - 4), (self.left  + xOffset, self.bottom - 8),
        fill=self.color,width=2, outline='black')

        canvas.create_line(self.right - 20 + xOffset, self.top, self.right + 
        xOffset - 20, self.bottom, width = 2)

        canvas.create_polygon(self.right + xOffset - 17, self.top+12,self.right 
        + xOffset - 3, self.top + 12, self.right + xOffset - 10, self.bottom -8,
        fill=self.color, outline='black', width=1.5)

        cx = (self.right - 20 + self.left) / 2
        canvas.create_text(cx + xOffset, self.y, text=self.shownText)

class AnimatedBox(Selector): 
    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.width, self.y - self.height, 
            self.x + self.width, self.y + self.height, fill=self.color, width=2)

def keyPressed(event, data):
    if data.mode == "editing":
        editingKeyPressed(event,data)
    elif data.mode == 'login':
        loginKeyPressed(event, data)
    elif data.mode == 'signup':
        signupKeyPressed(event, data)

def timerFired(data):
    if data.mode == "editing":
        editingTimerFired(data)
    elif data.mode == "testing":
        testingTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "editing":
        editingRedrawAll(canvas,data)
    elif data.mode == "testing":
        testingRedrawAll(canvas,data)
    elif data.mode == 'login':
        loginRedrawAll(canvas, data)
    elif data.mode == 'signup':
        signupRedrawAll(canvas, data)
    elif data.mode == 'help':
        helpRedrawAll(canvas, data)

def leftMousePressed(event, data):
    if data.mode == "editing":
        editingLeftMousePressed(event,data)
    elif data.mode == "testing":
        testingLeftMousePressed(event,data)
    elif data.mode == 'login':
        loginLeftMousePressed(event, data)
    elif data.mode == 'signup':
        signupLeftMousePressed(event, data)
    elif data.mode == 'help':
        helpLeftMousePressed(event, data)

def leftMouseMoved(event, data):
    if data.mode == "editing":
        editingLeftMouseMoved(event,data)
    elif data.mode == "testing":
        testingLeftMouseMoved(event,data)

def leftMouseReleased(event, data):
    if data.mode == "editing":
        editingLeftMouseReleased(event,data)
    elif data.mode == "testing":
        testingLeftMouseReleased(event,data)

def getElementBoxes():
    button = (20, 100, 120, 200, "button")
    slider = (20, 200, 120, 300, "slider")
    textBox = (20, 300, 120, 400, "textBox")
    dropDown = (20, 400, 120, 500, "dropDown")
    color = (20, 500, 120, 600, "color")
    return [button, slider, textBox, dropDown, color]

def getScreenButtons():
    h = 83 + (1/3) # height of a screen box
    s1 = (880, 100, 980, 100+h, '0')
    s2 = (880, 100+h, 980, 100+2*h, '1')
    s3 = (880, 100+2*h, 980, 100+3*h, '2')
    s4 = (880, 100+3*h, 980, 100+4*h, '3')
    s5 = (880, 100+4*h, 980, 100+5*h, '4')
    s6 = (880, 100+5*h, 980, 100+6*h, '5')
    return [s1, s2, s3, s4, s5, s6]

def init(data):
    data.width, data.height = 1000, 700
    data.phoneImage = PhotoImage(file='iphone.gif')
    data.save, data.load=PhotoImage(file='save.gif'),PhotoImage(file='load.gif')
    data.helpIcon = PhotoImage(file='helpIcon.gif')
    data.loginScreen = PhotoImage(file='login.gif')
    data.signupScreen = PhotoImage(file='signup.gif')
    data.helpScreen = PhotoImage(file='help.gif')
    data.iphone6Res, data.linkBox = (337.5, 580.3), [142.5, 185, 305.5, 255]
    data.elementBoxes, data.screenButtons = getElementBoxes(),getScreenButtons()
    data.elementHeld, data.currentHeld, data.editArea = None, None, None
    data.chooseColor, data.grabberSize = False, 8
    data.dropDownOptions = [142.5, 185, 305.5, 363]
    data.dropDownOptionsWidth, data.screenSelect = 1, False
    data.currentScreen, data.titleText, data.linkBoxWidth = '0', '', 1
    data.fontInput = [262.5, 160, 292.5, 190]
    data.fontInputWidth, data.timer, data.offset = 1, 0, 337.5
    data.firstClick = data.secondClick = data.editedText=data.movingCircle=None
    data.optionBoxes = {'0':[], '1':[], '2':[], '3':[], '4':[], '5':[]}
    data.colorBox = AnimatedBox(-90, 550, 175, 50, 'steel blue')
    data.colorChoices = getColorChoices()
    data.screenTransition= data.currentElement = data.checkFunction = None
    data.usernameInput, data.usernameInputWidth = (367, 306, 632, 353), 1
    data.passwordInput, data.passwordInputWidth = (367, 383, 632, 430), 1
    data.username, data.password = '', ''
    data.loginButton, data.signupButton = (510,460,630,503),(366,460,485.5,503)
    data.finishSignUpButton = (366, 460, 630, 503)
    data.returnToLoginButton = (366, 524, 630, 567)
    data.me = User( {'0':[], '1':[], '2':[], '3':[], '4':[], '5':[]})
    try:
        data.userInformation = pickle.load(open("userInfo.p", "rb"))
    except:
        data.userInformation = {}
    try:
        data.accounts = pickle.load(open("accounts.p", "rb"))
    except:
        data.accounts = {}
    data.xDifference, data.yDifference = None, None
    data.screenText, data.mode = (400, 650, 600, 700), 'login'
    data.screenName = {'0':'Screen 0', '1':'Screen 1', '2':'Screen 2', 
                        '3':'Screen 3', '4':'Screen 4', '5':'Screen 5'}
    data.darkBlue = getDarkBlueColor()
    (data.editingButtonBounds, data.loadBounds, data.saveBounds,data.testBounds,
    data.helpIconBounds) = getHeaderButtons()

def getColorChoices():
    return [(135, 510, 170.0, 545.0, 'red'), 
            (188, 510, 223.0, 545.0, 'orange'), 
            (241, 510, 276.0, 545.0, 'yellow'), 
            (294, 510, 329.0, 545.0, 'green'), 
            (347, 510, 382.0, 545.0, 'DeepSkyBlue2'), 
            (135, 558, 170.0, 597.0, 'purple'), 
            (188, 558, 223.0, 597.0, 'pink'), 
            (241, 558, 276.0, 597.0, 'brown'), 
            (294, 558, 329.0, 597.0, 'white'), 
            (347, 558, 382.0, 597.0, 'black')]

def getDarkBlueColor():
    R = 68
    G = 95
    B = 117
    return rgbString(R,G,B)

def getHeaderButtons():
    editingButtonBounds = (870, 635, 990, 685)
    loadBounds = (777, 0, 855, 50)
    saveBounds = (697, 0, 777, 50)
    testBounds = (855, 0, 1000, 50)
    helpIconBounds = (50, 0, 92, 50)
    return (editingButtonBounds,loadBounds,saveBounds,testBounds,helpIconBounds)

def loginKeyPressed(event, data):
    if event.keysym == 'Return':
        userInfo = pickle.load(open("userInfo.p", "rb"))
        if data.username in userInfo and userInfo[data.username]==data.password:
            data.mode = 'editing'
    if data.usernameInputWidth == 4: # username is currently being inputted
        if event.keysym in string.printable:
            data.username += event.keysym
        elif event.keysym == 'BackSpace':
            data.username = data.username[:-1]
    elif data.passwordInputWidth == 4:# password is currently being inputted
        if event.keysym in string.printable:
            data.password += event.keysym
        elif event.keysym == 'BackSpace':
            data.password = data.password[:-1]

def loginRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.loginScreen)
    if data.usernameInputWidth == 4 or data.username != '':
        canvas.create_rectangle(data.usernameInput, fill='white')
    if data.passwordInputWidth == 4 or data.password != '':
        canvas.create_rectangle(data.passwordInput, fill='white')
    canvas.create_rectangle(data.usernameInput, width=data.usernameInputWidth)
    canvas.create_text(380,328,text=data.username,font='Helvetica 25',anchor=W)
    canvas.create_rectangle(data.passwordInput, width=data.passwordInputWidth)
    canvas.create_text(380, 405,text=data.password,font='Helvetica 25',anchor=W)

def loginLeftMousePressed(event, data):
    if clickedInBounds(event.x, event.y, data.usernameInput):
        data.usernameInputWidth = 4
        data.passwordInputWidth = 1
    elif clickedInBounds(event.x, event.y, data.passwordInput):
        data.usernameInputWidth = 1
        data.passwordInputWidth = 4
    elif clickedInBounds(event.x, event.y, data.signupButton):
        data.mode = 'signup'
        data.usernameInputWidth = 1
        data.passwordInputWidth = 1  
        data.username = data.password = ''
    elif clickedInBounds(event.x, event.y, data.loginButton):
        userInfo = pickle.load(open("userInfo.p", "rb"))
        if data.username in userInfo and userInfo[data.username]==data.password:
            data.mode = 'editing'
    else:
        data.usernameInputWidth = 1
        data.passwordInputWidth = 1  

def signupKeyPressed(event, data): #user must have entered a username + password
    if event.keysym == 'Return' and data.password != '' and data.username != '':
        data.mode = 'login'
        data.usernameInputWidth = 1
        data.passwordInputWidth = 1  
        data.userInformation[data.username] = data.password
        data.username = data.password = ''
        pickle.dump(data.userInformation, open('userInfo.p', 'wb'))
    if data.usernameInputWidth == 4:
        if event.keysym in string.printable:
            data.username += event.keysym
        elif event.keysym == 'BackSpace':
            data.username = data.username[:-1]
    elif data.passwordInputWidth == 4:
        if event.keysym in string.printable:
            data.password += event.keysym
        elif event.keysym == 'BackSpace':
            data.password = data.password[:-1]

def signupRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.signupScreen)
    canvas.create_rectangle(data.returnToLoginButton)
    if data.usernameInputWidth == 4 or data.username != '':
        canvas.create_rectangle(data.usernameInput, fill='white')
    if data.passwordInputWidth == 4 or data.password != '':
        canvas.create_rectangle(data.passwordInput, fill='white')
    canvas.create_rectangle(data.usernameInput, width=data.usernameInputWidth)
    canvas.create_text(380, 328,text=data.username,font='Helvetica 25',anchor=W)
    canvas.create_rectangle(data.passwordInput, width=data.passwordInputWidth)
    canvas.create_text(380, 405,text=data.password,font='Helvetica 25',anchor=W)

def signupLeftMousePressed(event, data):
    if clickedInBounds(event.x, event.y, data.usernameInput):
        data.usernameInputWidth = 4
        data.passwordInputWidth = 1
    elif clickedInBounds(event.x, event.y, data.passwordInput):
        data.usernameInputWidth = 1
        data.passwordInputWidth = 4
    elif (clickedInBounds(event.x, event.y, data.finishSignUpButton) 
        and data.username != '' and data.password != ''):
        data.mode = 'login'
        data.usernameInputWidth = 1
        data.passwordInputWidth = 1  
        data.userInformation[data.username] = data.password
        data.username = data.password = ''
        pickle.dump(data.userInformation, open('userInfo.p', 'wb'))
    elif clickedInBounds(event.x, event.y, data.returnToLoginButton):
        data.mode = 'login'
        data.usernameInputWidth = 1
        data.passwordInputWidth = 1
        data.username = data.password = ''
    else:
        data.usernameInputWidth = 1
        data.passwordInputWidth = 1  

def editingKeyPressed(event, data):
    for element in data.me.elements[data.currentScreen]:
        if element == data.currentElement:
            # delete the element if you select it and press backspace
            if event.keysym == 'BackSpace' and data.editedText == None:
                data.me.elements[data.currentScreen].remove(element)
                data.checkFunction = None
                break
    if data.editedText != None:
        if data.fontInputWidth == 4: # font is currently being inputed
            editFontSize(event, data)
        elif data.editedText == data.currentElement:
            editElementText(event,data)
        elif data.editedText == data.currentScreen:
            editScreenText(event, data)

def editFontSize(event, data):
    if event.keysym in string.digits:
        data.currentElement.fontSize += event.keysym
    if event.keysym == 'BackSpace':
        data.currentElement.fontSize = data.currentElement.fontSize[:-1]
    if event.keysym == 'Return':
        data.fontInputWidth = 1
    if data.currentElement.fontSize!=''and int(data.currentElement.fontSize)>99:
        data.currentElement.fontSize = '99' # max font size is 99

def editElementText(event, data):
    if event.keysym in string.printable:
        data.currentElement.text += event.keysym
    if event.keysym == 'BackSpace': # [:-2] because the character line ('|') is
                                    # a character added to the end of the string
        data.currentElement.text = data.currentElement.text[:-2]
    if event.keysym == 'space':
        data.currentElement.text += ' '
    if event.keysym == 'Return':
        data.currentElement.text += '\n'
    if event.keysym == 'Tab':
        data.currentElement.text += '\t'
    if data.currentElement.type == 'dropdown': #showntext is the 1st item listed
        data.currentElement.shownText = data.currentElement.text.split('\n')[0]

def editScreenText(event, data):
    if event.keysym in string.printable:
        data.screenName[data.currentScreen] += event.keysym
    if event.keysym == 'BackSpace':
        data.screenName[data.currentScreen] = data.screenName[
                                                        data.currentScreen][:-2]
    if event.keysym == 'space':
        data.screenName[data.currentScreen] += ' '
    if event.keysym == 'Tab':
        data.screenName[data.currentScreen] += '\t'

# create the server and connect to it
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.connect((HOST,PORT))

# recieves and decodes the incoming server messages
def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  while True:
    try:
        msg = pickle.loads(server.recv(16384))
    except: # msg recieved is not an updated dict of elements,so decode normally
        msg = server.recv(16384)
    serverMsg.put(msg)

# when text is no longer being edited, remove the char. bar ('|')
def clearCharacterBar(data):
    for element in data.me.elements[data.currentScreen]:
        if element != data.currentElement:
            if (element.type == 'button' or element.type == 'dropdown' or 
                                                    element.type == 'textBox'):
                element.text = element.text.replace('|', '')
    for screen in data.screenName:
        if screen != data.currentScreen or data.editedText == None:
            data.screenName[screen] = data.screenName[screen].replace('|', '')
    if data.firstClick != None:
        if data.timer - data.firstClick > 15:
            data.firstClick = None
    if data.editedText != None:
        if data.editedText == data.currentElement:
            data.currentElement.text = data.currentElement.text.replace('|', '')
            data.currentElement.text += '|'
        elif data.editedText == data.currentScreen:
            data.screenName[data.currentScreen] = (data.screenName
                                          [data.currentScreen].replace('|', ''))
            data.screenName[data.currentScreen] += '|'

def editingTimerFired(data):
    data.timer += 1
    clearCharacterBar(data)
    # if there is a msg recieved
    # socket code template used from https://drive.google.com/a/andrew.cmu.edu/
                                   #folderview?id=0B8s_apgePQWIRGw0WklVa2hyd3M&
                                   #usp=sharing&tid=0B8s_apgePQWIQXg3dV9hUUVQRHc
    if (serverMsg.qsize() > 0):
        msg, currElementScreen = serverMsg.get(False), False
        if msg != data.me.elements and type(msg) == dict:
            for screen in data.me.elements: #before you update the dictionary,
                if data.editedText != None: #remember the current editedText
                    for element in data.me.elements[screen]:
                        if element == data.editedText:
                            textScreen = screen
                            textIndex = data.me.elements[screen].index(data
                                                                    .editedText)
                if data.currentElement != None:
                    for element in data.me.elements[screen]:
                        if element == data.currentElement:
                            currElementScreen = screen
                            currElementIndex=data.me.elements[screen].index(data
                                                                .currentElement)
            # update the client's dictionary to the decoded msg
            data.me.elements = msg
            try:
                # remembering the editedText allows text to still be edited
                # even after the dict is updated
                if data.editedText != None and type(data.editedText) != str:
                    data.editedText = data.me.elements[textScreen][textIndex]
                if data.currentElement != None and currElementScreen:
                    data.currentElement = data.me.elements[currElementScreen
                                                         ][currElementIndex]
            except:
                return
        serverMsg.task_done()

# used from graphics notes-https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

def drawUI(canvas, data):
    canvas.create_rectangle(-2, -5, 1000, 1000, fill=data.darkBlue)#background
    canvas.create_rectangle(0, 0, 1000, 50, fill='steel blue', width = 3)#header
    canvas.create_rectangle(0, 650, 1000, 699,fill='steel blue', width=3)#footer
    canvas.create_rectangle(data.width/2 - data.iphone6Res[0]/2, data.height/2 - 
        data.iphone6Res[1]/2 + 10, data.width/2 + data.iphone6Res[0]/2,
        data.height/2 + data.iphone6Res[1]/2 - 10, fill='white', width=4)#screen
    canvas.create_polygon(887, 10, 917, 25, 887, 40, fill='black')#play button
    canvas.create_text(947, 25, text='Test', font='Helvetica 20')
    canvas.create_line(855, 0, 855, 50, width=2)

def drawGrabbers(canvas, data): #the small white boxes that user edits size with
    for element in data.me.elements[data.currentScreen]:
            element.draw(canvas)
            if element == data.currentElement:
                if element.type == 'textBox' or element.type == 'button':
                    canvas.create_rectangle(element.left, element.top, 
                        element.left + data.grabberSize, element.top + 
                        data.grabberSize, fill= 'white', width=2)
                    canvas.create_rectangle(element.left, element.bottom - 
                        data.grabberSize, element.left + data.grabberSize, 
                        element.bottom, fill= 'white', width=2)
                    canvas.create_rectangle(element.right - data.grabberSize, 
                        element.top, element.right, element.top + 
                        data.grabberSize, fill= 'white', width=2)
                    canvas.create_rectangle(element.right - data.grabberSize, 
                        element.bottom - data.grabberSize, element.right, 
                        element.bottom, fill= 'white', width=2)
                else:
                    canvas.create_rectangle(element.left, element.y - 
                        data.grabberSize/2, element.left + data.grabberSize, 
                        element.y + data.grabberSize/2, fill= 'white', width=2)
                    canvas.create_rectangle(element.right - data.grabberSize, 
                        element.y - data.grabberSize/2, element.right, element.y
                         + data.grabberSize/2, fill= 'white', width=2)

def drawScreenButtons(canvas, data):
    for screen in data.screenButtons:
        width = 2 # thicker width indicates which screen is currently selected
        if data.screenSelect == True:
            width = 4
        elif screen[-1] == data.currentScreen:
            width = 4
            scx = data.width/2 # screen center x
            scy = data.height/2 # screen center y
            canvas.create_text(scx, scy -25 + data.height/2, 
                text = data.screenName[screen[-1]],font= 'Helvetica 30', 
                fill='black')
        else:
            width = 2
        canvas.create_rectangle(screen[:-1], width=width, fill='white')
        bcx = (screen[0] + screen[2]) / 2 # box center x
        bcy = (screen[1] + screen[3]) / 2 # box center y
        canvas.create_text(bcx, bcy + 30, text=data.screenName[screen[-1]])

def editingRedrawAll(canvas, data):
    drawUI(canvas, data)
    drawGrabbers(canvas, data)
    chooseColor(canvas, data)
    # covers up the color chooser box sliding in from the left side
    canvas.create_rectangle(0, 490, 20, 610, fill=data.darkBlue, width=0)  
    for elementBox in data.elementBoxes: #draw the left side element boxes
        canvas.create_rectangle(elementBox[:-1], fill='white', width=2)
        boxType = elementBox[-1]
        drawElementInBox(canvas, data, boxType)
    drawScreenButtons(canvas, data)
    if data.elementHeld != None:
        data.elementHeld.draw(canvas)
    if data.checkFunction != None:
        functionPicker(canvas, data, data.checkFunction)
    canvas.create_line(697, 0, 697, 50, width=2)
    canvas.create_image(735, 25, image=data.save) #save icon
    canvas.create_image(70, 25, image=data.helpIcon) # help icon
    canvas.create_line(777, 0, 777, 50, width=2)
    canvas.create_image(815, 25, image=data.load) #load icon

def drawElementInBox(canvas, data, boxType):
    if boxType == 'button':
        boxButton = Buttonn(70, 150, 40, 20, 'white', 'button')
        boxButton.draw(canvas, 0)
    elif boxType == 'slider':
        boxSlider = Slider(70, 250, 45, 3.2, 'white', 10)
        boxSlider.draw(canvas, 0)
    elif boxType == 'textBox':
        boxTextBox = TextBox(70, 350, 40, 20, 'white', "text box")
        boxTextBox.draw(canvas)
    elif boxType == 'dropDown':
        boxDropDown = DropDown(70, 450, 40, 15, 'white', "")
        boxDropDown.draw(canvas)
    elif boxType == 'color':
        canvas.create_oval(30, 515, 75, 560, fill="blue", width=2)
        canvas.create_oval(65, 515, 110, 560, fill="yellow",width=2)
        canvas.create_oval(47.5, 545, 92.5, 590, fill="red",width=2)

def clickedColor(x, y, colorChoice, data):
    r = 17.5 # radius of color circle
    cx = (colorChoice[0] + colorChoice[2]) / 2
    cy = (colorChoice[1] + colorChoice[3]) / 2
    dist = math.sqrt((cx - x)**2  + (cy - y)**2)
    if dist <= r:
        if data.currentElement.type == 'slider':
            data.currentElement.slidColor = colorChoice[-1]
        else:
            data.currentElement.color = colorChoice[-1]

def screenSelect(event, data):
    for screen in data.screenButtons:
        if clickedInBounds(event.x, event.y, screen):
            if data.screenSelect == True: # user is prompted to select a screen 
                data.screenSelect = False               # to link the button to
                data.currentElement.linkedTo = screen[-1]
            elif data.screenSelect == False:
                data.checkFunction = None
                data.currentScreen = screen[-1]
                data.currentElement = None
                data.editedText = None

def selectElement(event, data):
    for element in data.me.elements[data.currentScreen]:
        if element.type == 'slider':
            dist = math.sqrt((element.cx - event.x)**2 +(element.cy-event.y)**2)
            if dist <= element.r: # clicked within the circle 
                data.currentElement = element
                data.checkFunction = element
                break
        if (element.left < event.x < element.right and #selected an element
            element.top < event.y < element.bottom):
            data.currentElement = element
            data.checkFunction = element
            break
        elif (data.width/2 - data.iphone6Res[0]/2 < event.x  < data.width/2 + 
            data.iphone6Res[0]/2 and data.height/2 - data.iphone6Res[1]/2  
            < event.y < data.height/2 + data.iphone6Res[1]/2): # deselect
            if data.editedText != None:
                if data.editedText == data.currentElement:
                    data.currentElement.text = (data.currentElement.text
                                                              .replace('|', ''))
            if (not clickedInBounds(event.x, event.y,(347, 510, 382.0, 545)) 
                and not clickedInBounds(event.x, event.y,(347, 558, 382, 597))): 
                                     # didn't click in the blue or black colors
                data.currentElement= data.editedText = data.checkFunction = None

 # selects which area is going to be edited for text box and button
def startEditTextBoxOrButton(event, data, element, clickableRadius, 
                                    bottomRight, bottomLeft, topRight, topLeft):
    if (bottomRight[0] - clickableRadius < event.x < bottomRight[0] + 
        clickableRadius and bottomRight[1] - clickableRadius < event.y < 
        bottomRight[1] + clickableRadius):
        data.editArea = 'bottomRight'
    elif (bottomLeft[0] - clickableRadius < event.x < bottomLeft[0] + 
        clickableRadius and bottomLeft[1] - clickableRadius < event.y < 
        bottomLeft[1] + clickableRadius):
        data.editArea = 'bottomLeft'
    elif (topRight[0] - clickableRadius < event.x < topRight[0] + 
        clickableRadius and topRight[1] - clickableRadius < event.y < 
        topRight[1] + clickableRadius):
        data.editArea = 'topRight'
    elif (topLeft[0] - clickableRadius < event.x < topLeft[0] + 
        clickableRadius and topLeft[1] - clickableRadius < event.y < 
        topLeft[1] + clickableRadius):
        data.editArea = 'topLeft'
    elif (element.left < event.x < element.right and 
                                        element.top < event.y < element.bottom):
        data.editArea = 'position'
        data.xDifference = element.right - event.x
        data.yDifference = element.bottom - event.y

 # selects which area is going to be edited for slider or dropdown
def startEditSliderOrDropDown(event, data, element, clickableRadius,
                                    bottomRight, bottomLeft, topRight, topLeft):
    if element.type == 'slider':
        dist = math.sqrt((element.cx - event.x)**2 + (element.cy - event.y)**2)
        if dist <= element.r:
            data.editArea = 'position'
            data.xDifference = element.right - event.x
            data.yDifference = element.bottom - event.y
    if (element.left < event.x < element.right and 
                                    element.top < event.y < element.bottom):
        data.editArea = 'position'
        data.xDifference = element.right - event.x
        data.yDifference = element.bottom - event.y
    if (element.left - clickableRadius < event.x < element.left +clickableRadius
     and element.y - clickableRadius < event.y < element.y + clickableRadius):
        data.editArea = 'left'
    if (element.right - clickableRadius < event.x <element.right+clickableRadius
     and element.y - clickableRadius < event.y < element.y + clickableRadius):
        data.editArea = 'right'


def editingLeftMousePressed(event, data):
    screenSelect(event, data)
    for elementBox in data.elementBoxes: # opening/closing color picker box
        if clickedInBounds(event.x, event.y, elementBox):
            if elementBox[-1] == 'color':
                data.chooseColor = not data.chooseColor
            data.currentHeld = elementBox[-1]
    if data.chooseColor == True and data.currentElement != None:
        for colorChoice in data.colorChoices:
            clickedColor(event.x, event.y, colorChoice, data)
    #clicked within the screen
    if (data.width/2 - data.iphone6Res[0]/2 < event.x  < data.width/2 + 
        data.iphone6Res[0]/2 and data.height/2 - data.iphone6Res[1]/2  
        < event.y < data.height/2 + data.iphone6Res[1]/2):
        if data.editedText == data.currentScreen:
            data.editedText = None
    selectElement(event, data)
    clickableRadius = 10
    for element in data.me.elements[data.currentScreen]:
        if element == data.currentElement: 
            bottomRight = (element.right, element.bottom)
            bottomLeft = (element.left, element.bottom)
            topRight = (element.right, element.top)
            topLeft = (element.left, element.top)
            if element.type == 'button' or element.type == 'textBox':
                startEditTextBoxOrButton(event, data, element, clickableRadius, 
                                    bottomRight, bottomLeft, topRight, topLeft)
            else:
                startEditSliderOrDropDown(event, data, element, clickableRadius,
                                    bottomRight, bottomLeft, topRight, topLeft)
    clickedInFunctionPickers(event, data)
    doubleClickedForTextEdit(event, data)
    clickedInHeaderButtons(event, data)


def clickedInFunctionPickers(event, data):
    totalScreenButtonBounds = (900, 50, 1050, 650)
    if clickedInBounds(event.x, event.y, data.linkBox):
        data.linkBoxWidth = 4 # width determines if it is being edited or not
        if data.titleText == 'Button':
            data.screenSelect = not data.screenSelect
    elif data.screenSelect and not clickedInBounds(event.x, event.y, 
    totalScreenButtonBounds): # didnt click in the screens on the right side
        data.screenSelect = False
    if clickedInBounds(event.x, event.y, data.dropDownOptions):
        data.dropDownOptionsWidth = 4 
        if data.currentElement != None and data.currentElement.type=='dropdown':
            data.editedText = data.currentElement
    if clickedInBounds(event.x, event.y, data.fontInput):
        data.fontInputWidth = 4
        data.editedText = data.currentElement.fontSize
    else:
        data.fontInputWidth = 1
        data.linkBoxWidth = 1

def doubleClickedForTextEdit(event, data):
    if clickedInBounds(event.x, event.y, data.screenText):
        if data.firstClick == None: data.firstClick = data.timer
        elif data.firstClick != None: data.secondClick = data.timer
        if data.firstClick != None and data.secondClick != None:
            if data.secondClick - data.firstClick <= 15: #must be a short enough
                                                #to be considered a double click
                data.editedText = data.currentScreen
            else: data.editedText = None
            data.firstClick = data.secondClick = None
    for element in data.me.elements[data.currentScreen]:
        if (element.left < event.x < element.right and 
                element.top < event.y < element.bottom):
            if (element.type == 'textBox' or element.type == 'button'):
                if data.firstClick == None: data.firstClick = data.timer
                elif data.firstClick != None: data.secondClick = data.timer
            if data.firstClick != None and data.secondClick != None:
                if data.secondClick - data.firstClick <= 15:
                    if element.type == 'textBox'or element.type == 'button':
                        data.editedText = element
                else: data.editedText = None
                data.firstClick = data.secondClick = None
            break

def clickedInHeaderButtons(event, data):
    if clickedInBounds(event.x, event.y, data.saveBounds):
        data.accounts[(data.username, data.password)] = data.me.elements
        pickle.dump(data.accounts, open('accounts.p', 'wb'))
    elif clickedInBounds(event.x, event.y, data.loadBounds):
        accounts = pickle.load(open("accounts.p", "rb"))
        if (data.username, data.password) in accounts:
            data.me.elements = accounts[(data.username, data.password)]
    if clickedInBounds(event.x, event.y, data.helpIconBounds):
        data.mode = 'help'
    if clickedInBounds(event.x, event.y, data.testBounds):
        data.mode = 'testing'

def clickedInBounds(x, y, bounds): 
    # where x and y are the click coordinates and
    # bounds is a set of coordinates representing the clickable area
    if bounds[0] < x < bounds[2] and bounds[1] < y < bounds[3]:
        return True

def chooseColor(canvas, data):
    r = 17.5 # radius of color circle
    numColors = 10
    colors = ['red', 'orange', 'yellow', 'green', 'DeepSkyBlue2', 
              'purple', 'pink', 'brown', 'white', 'black']
    i = 0
    yMargin = 10
    xMargin = 90
    if data.chooseColor == True:
        data.colorBox.draw(canvas)
        data.colorBox.x += 50 # slide the box
        if data.colorBox.x + data.colorBox.width > 395: 
            data.colorBox.x = 395 - data.colorBox.width # stop the slide
        for row in range(2): #draw each color
            for col in range(5):
                i += 1
                left = data.colorBox.x - data.colorBox.width
                top = data.colorBox.y - data.colorBox.height
                canvas.create_oval(left + xMargin + col*53, top + yMargin + 
                    row*48, left + xMargin + 2*r + col*53, top + yMargin + 2*r +
                    row*48, fill=colors[i-1])
    else:
        data.colorBox.draw(canvas) # slide the colors back into the left side
        data.colorBox.x -= 50
        if data.colorBox.x + data.colorBox.width < 0:
            data.colorBox.x = -data.colorBox.width
        for row in range(2):
            for col in range(5):
                i += 1
                left = data.colorBox.x - data.colorBox.width
                top = data.colorBox.y - data.colorBox.height
                canvas.create_oval(left + xMargin + col*53, top + yMargin + 
                    row*48, left + xMargin + 2*r + col*53, top + yMargin + 2*r +
                    row*48, fill=colors[i-1])

def editingLeftMouseMoved(event, data):
    rightBound = data.iphone6Res[0]/2 + data.width/2
    leftBound = data.width/2 - data.iphone6Res[0]/2
    bottomBound = data.iphone6Res[1]/2 + data.height/2 - 10
    topBound = data.height/2 - data.iphone6Res[1]/2 + 10
    # dragging the actual buttons
    if data.currentHeld == "button":
        data.elementHeld = Buttonn(event.x, event.y, 40, 20, 'white', 'button')
    elif data.currentHeld == "slider":
        data.elementHeld = Slider(event.x, event.y, 50, 3, 'white', 10)
    elif data.currentHeld == "textBox":
        data.elementHeld = TextBox(event.x, event.y, 40, 20, 'white', "text box")
    elif data.currentHeld == "dropDown":
        data.elementHeld = DropDown(event.x, event.y, 40, 15, 'white', '')
    for element in data.me.elements[data.currentScreen]:
        if element == data.currentElement: 
            editSize(event, data, element, rightBound, leftBound, bottomBound, 
                                                                       topBound)
            limitSize(event, data, element)
            width, height = editPosition(event, data, element)
            limitPosition(event, data, element,  width, height, rightBound, 
                                               leftBound, bottomBound, topBound)

#changing the size of the elements
def editSize(event, data, element, rightBound, leftBound, bottomBound,topBound):
    # print(data.)
    bottomRight = (element.right, element.bottom)
    bottomLeft = (element.left, element.bottom)
    topRight,topLeft =(element.right,element.top),(element.left,element.top)
    if data.editArea =='bottomRight':
        element.right, element.bottom = event.x, event.y
        if element.right > rightBound: element.right = rightBound
        if element.bottom > bottomBound: element.bottom = bottomBound
    elif data.editArea == 'bottomLeft':
        element.left, element.bottom = event.x, event.y
        element.bottom = event.y
        if element.left < leftBound: element.left = leftBound
        if element.bottom > bottomBound: element.bottom = bottomBound
    elif data.editArea == 'topRight':
        element.right, element.top = event.x, event.y
        if element.right > rightBound: element.right = rightBound
        if element.top < topBound: element.top = topBound
    elif data.editArea =='topLeft':
        element.left, element.top = event.x, event.y
        if element.left < leftBound: element.left = leftBound
        if element.top < topBound: element.top = topBound
    elif data.editArea == 'left':
        element.left = event.x
        if element.left < leftBound: element.left = leftBound
    elif data.editArea == 'right':
        element.right = event.x
        if element.right > rightBound: element.right = rightBound

#they are limited by certain constraints
def limitSize(event, data, element):
    if (element.right - element.left < 10 and element.type != 'slider' and 
                                                    element.type != 'dropdown'):
        if 'left' in data.editArea.lower():
            element.left = element.right - 10
        else:
            element.right = element.left + 10
    if element.right - element.left < 40 and element.type:
        if 'left' in data.editArea.lower():
            element.left = element.right - 40
        else:
            element.right = element.left + 40
    if (element.bottom - element.top < 10 and element.type != 'slider' and 
                                                    element.type != 'dropdown'):
        if 'top' in data.editArea.lower():
            element.top = element.bottom - 10
        else:
            element.bottom = element.top + 10

# move the element around
def editPosition(event, data, element):
    if data.editArea == 'position':
        width = (element.right - element.left)
        height = (element.bottom - element.top)
        element.right = event.x + data.xDifference
        element.left = event.x - (width - data.xDifference)
        element.bottom = event.y + data.yDifference
        element.top = event.y - (height - data.yDifference)
    if element.type == 'slider':
        element.cx = (element.right + element.left) / 2
        element.cy = (element.top + element.bottom) / 2
    element.x = (element.right + element.left) / 2 # update x and y after moving
    element.y = (element.top + element.bottom) / 2
    width = (element.right - element.left)
    height = (element.bottom - element.top)
    return width, height

# prevent element from being dragged off screen
def limitPosition(event, data, element,  width, height, rightBound, 
                                            leftBound, bottomBound, topBound):
    if element.x + width/2 >= data.iphone6Res[0]/2 + data.width/2: # right
        element.right = rightBound
        element.left = rightBound - width
        element.x = rightBound - width/2
    if element.x - width/2 <= data.width/2 - data.iphone6Res[0]/2:
        element.left = leftBound
        element.right = leftBound + width
        element.x = leftBound + width/2
    if element.y + height/2 >= data.iphone6Res[1]/2 + data.height/2 - 10:
        element.bottom = bottomBound
        element.top = bottomBound - height
        element.y = bottomBound - height/2
    if element.y - height/2 <= data.height/2 - data.iphone6Res[1]/2 + 10:
        element.top = topBound
        element.bottom = topBound + height
        element.y = topBound + height/2
    if element.type == 'slider':
        element.cy = element.y
        element.cx = element.x
        element.right = element.cx + width/2
        element.left = element.cx - width/2

def editingLeftMouseReleased(event, data):
    if data.elementHeld != None:
        if (data.width/2 - data.iphone6Res[0]/2 + data.elementHeld.width 
        < event.x < 
        data.width/2 + data.iphone6Res[0]/2  - data.elementHeld.width and 
        data.height/2 - data.iphone6Res[1]/2  + data.elementHeld.height 
        < event.y < # if the object is placed within the screen bounds
        data.height/2 + data.iphone6Res[1]/2  - data.elementHeld.height):
            data.me.elements[data.currentScreen].append(data.elementHeld)
        data.elementHeld = None
        data.currentHeld = None
    data.editArea = None
    # once a user clicks, send the most recent version of the element dictionary
    elementsPlacedMsg = pickle.dumps(data.me.elements)
    data.server.send(elementsPlacedMsg)

def functionPicker(canvas, data, element):
    if element.type == 'button':
        getButtonFunctions(canvas, data, element)
    elif element.type == 'textBox':
        getTextBoxFunctions(canvas, data, element)
    elif element.type == 'dropdown':
        getDropDownFunctions(canvas, data, element)
    elif element.type == 'slider':
        data.titleText = ''
    canvas.create_text(223, 125, text=data.titleText, font='Helvetica 17')

def getButtonFunctions(canvas, data, element):
    canvas.create_rectangle(132.5, 100, 315.5, 265, fill='white', width=2)
    data.titleText = 'Button'
    canvas.create_text(142.5, 175, text='Button Links to:', anchor=W)
    canvas.create_rectangle(data.linkBox, width = data.linkBoxWidth)
    if data.currentElement.linkedTo != None:
        cx = (data.linkBox[0] + data.linkBox[2]) / 2
        cy = (data.linkBox[1] + data.linkBox[3]) / 2
        canvas.create_text(cx, cy, 
        text=data.screenName[data.currentElement.linkedTo], font='Helvetica 18')

def getTextBoxFunctions(canvas, data, element):
        canvas.create_rectangle(132.5, 100, 315.5, 215, fill='white', width=2)
        data.titleText = 'Text Box'
        canvas.create_text(152.5, 175, text='Font Size', anchor=W)
        canvas.create_rectangle(data.fontInput, width = data.fontInputWidth)
        canvas.create_text(277.5, 175, text=element.fontSize)

def getDropDownFunctions(canvas, data, element):
    canvas.create_rectangle(132.5, 100, 315.5, 375, fill='white', width=2)
    data.titleText = 'Dropdown Menu'
    canvas.create_text(142.5, 175, text='Menu options:', anchor=W)
    canvas.create_rectangle(data.dropDownOptions, 
        width =data.dropDownOptionsWidth)
    canvas.create_text(147.5, 190, text=element.text, anchor=NW)

def testingTimerFired(data):
    # get rid of any char bars
    for element in data.me.elements[data.currentScreen]:
        if (element.type == 'button' or element.type == 'dropdown' or 
                                                    element.type == 'textBox'):
            element.text = element.text.replace('|', '')

def testingRedrawAll(canvas, data):
    for element in data.me.elements[data.currentScreen]:
        if element.type == 'dropdown':
            if element.opened == True:
                drawOpenedDropDownMenu(canvas, data, element)
        if data.screenTransition == None:
            element.draw(canvas)
    if data.screenTransition != None:
        animateScreen(canvas, data, data.screenTransition)
    canvas.create_image(data.width/2, data.height/2, image=data.phoneImage)
    editingButton = Buttonn(930, 660, 60, 25, 'SteelBlue3', 'Return to Editing')
    editingButton.draw(canvas)

def drawOpenedDropDownMenu(canvas, data, element):
    menuOptions = element.text.split('\n')
    for i in range(1, len(menuOptions) + 1):
        height = element.height*2
        cx = (element.left + element.right)/2
        cy = ((element.bottom + (i-1)*height) + (element.bottom + i*height)) / 2
        # draw each individual box for each option listed
        canvas.create_rectangle(element.left + 5, element.bottom + (i-1)*height, 
            element.right - 5, element.bottom + i*height, fill='white', width=2)
        if menuOptions[i-1] != '|':
            if '|' in menuOptions[i-1]:
                menuOptions[i-1] = menuOptions[i-1].replace('|', '')
            canvas.create_text(cx, cy, text=menuOptions[i-1])
            optionBoxBounds = [element.left, element.bottom + (i-1)*height, 
            element.right, element.bottom + i*height, menuOptions[i-1]]
            # append these boxes to a list in order to check if you clicked them
            if optionBoxBounds not in data.optionBoxes[data.currentScreen]:
                data.optionBoxes[data.currentScreen].append(optionBoxBounds)

def animateScreen(canvas, data, screenTransition):
    # when testing, animate the screen sliding in from the right
    # essentially draw all elements at an offset and decrease it to 0
    incomingScreenOffset = data.offset
    outgoingScreenOffset = data.offset - 337.5
    canvas.create_line(500 - (337.5)/2 + data.offset, 350 - 580.3, 500 - 
        (337.5)/2 + data.offset, 350 + 580.3)
    for incomingElement in data.me.elements[screenTransition]:
        incomingElement.draw(canvas, incomingScreenOffset)
    for outgoingElement in data.me.elements[data.currentScreen]:
        outgoingElement.draw(canvas, outgoingScreenOffset)
    data.offset -= 25
    if data.offset <= 0:
        data.offset = 0
        data.currentScreen = screenTransition


def testingLeftMousePressed(event, data):
    if clickedInBounds(event.x, event.y, data.editingButtonBounds):
        data.mode = 'editing'
        data.checkFunction = data.screenTransition = data.currentElement = None
    for element in data.me.elements[data.currentScreen]:
        if element.type == 'slider': # clicking the slider circle
            dist = math.sqrt((element.cx - event.x)**2 +(element.cy-event.y)**2)
            if dist <= element.r: data.movingCircle = element
            element.opened = False
        elif (element.left < event.x < element.right and  # clicked on element
                                        element.top < event.y < element.bottom):
                if element.type == 'button' and element.linkedTo != None:
                    data.screenTransition = element.linkedTo
                    data.offset = 337.5 #reset offset for the next transition
                elif element.type == 'dropdown':
                    element.opened = not element.opened
        elif element.type == 'dropdown':
            # clicking the dropdown and changing the selected option
            if element.opened == True:
                for screen in data.optionBoxes:
                    for optionBox in data.optionBoxes[screen]:
                        if clickedInBounds(event.x, event.y, optionBox):
                            element.shownText = optionBox[-1]
            element.opened = False

def testingLeftMouseMoved(event, data):
    # dragging the slider circle
    if data.movingCircle != None:
        data.movingCircle.cx = event.x
        if data.movingCircle.cx > data.movingCircle.right:
            data.movingCircle.cx = data.movingCircle.right
        elif data.movingCircle.cx < data.movingCircle.left:
            data.movingCircle.cx = data.movingCircle.left

def testingLeftMouseReleased(event, data):
    data.movingCircle = None

def helpRedrawAll(canvas, data):
    canvas.create_image(500, 350, image=data.helpScreen) #save icon
    editingButton = Buttonn(930, 660, 60, 25, 'SteelBlue3', 'Return to Editing')
    editingButton.draw(canvas)

def helpLeftMousePressed(event, data):
    if clickedInBounds(event.x, event.y, data.editingButtonBounds):
        data.mode = 'editing'
        data.checkFunction = None
        data.screenTransition = None
        data.currentElement = None

####################################
# use the run function as-is
####################################


def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def leftMousePressedWrapper(event, canvas, data):
        leftMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def leftMouseReleasedWrapper(event, canvas, data):
        leftMouseReleased(event, data)
        redrawAllWrapper(canvas, data)

    def leftMouseMovedWrapper(event, canvas, data):
        leftMouseMoved(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    root.wm_title("PROTO")
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height, 
                    highlightthickness=0, relief='ridge')
    canvas.pack()
    # set up events
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Button-1>", lambda event: 
                            leftMousePressedWrapper(event, canvas, data))
    canvas.bind("<B1-Motion>", lambda event:
                            leftMouseMovedWrapper(event, canvas, data))
    root.bind("<B1-ButtonRelease>", lambda event:
                            leftMouseReleasedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
start_new_thread(handleServerMsg, (server, serverMsg))

run(1000, 800, serverMsg, server)