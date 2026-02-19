#Importing the needed library
import subprocess
import threading
from pathlib import Path
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import backend
from backend import write_theme, read_theme, del_history

#Makes the resource path accessible
absolute_path = Path(__file__).resolve().parent
resource_path = absolute_path/ "resources"

# Screen Management
root = BoxLayout(orientation="vertical") # Creates the main layout for the app
screen_manager = ScreenManager()


# Defines needed variable
txt = "0"
ans = "0"
theme = read_theme()
font = "resources/DejaVuSans-Bold.ttf"
emoji = "resources/Segoe UI Emoji.TTF"
if theme == None:
    theme = "black"
if str(theme) == "black":
    thm= "white"
else:
    thm= "black"
app = App()
def windows(instance):  # Windows functions
    Window.size = (900, 600)   # Set window size
    Window.minimum_width = 900
    Window.maximum_width = 900
    Window.maximum_height = 600
    Window.minimum_height = 600
    Window.title = "Hex's Scientific Calculator"   # Window title
    Window.icon = str(resource_path / "icon.png")   # Set windows icon
    Window.opacity = 1 # Sets app opacity for style
    if theme == "black":
        Window.clearcolor = (0.02, 0.02, 0.02, 1)
    else:
        Window.clearcolor = (0.85,0.85,0.85,1)
windows(instance=Window) # Activate the windows function

backend.delete_kill()

def cleanup(*args):
    backend.write_kill()

Window.bind(on_request_close=cleanup)

def restart_self():
    script = "/home/hex/Documents/ICT_CALC_HEX/Main.py"
    python_exe = "/home/hex/Documents/ICT_CALC_HEX/venv/bin/python"
    subprocess.run([python_exe, script])

def kill(*args):
    x = backend.read_kill()
    if x == "1":
        App.get_running_app().stop()

Clock.schedule_interval(kill, 0.5)

def title_bar():  # Sets up title bar
    titlebar = BoxLayout(orientation="horizontal",
                         size_hint_y=None,
                         height=40,
                         padding=(0,5,0,10)) # Creates custom title bar
    icon = Image(source=str(resource_path/"icon.png"),
                 size_hint=(None, None),
                 size= (45,25)) # Creates app icon
    title = Label(text= "Hex's Scientific Calculator",
                  size_hint=(1, 1),
                  bold =True,
                  font_size= 17,
                  color= thm) # Create app title

    titlebar.add_widget(icon)
    titlebar.add_widget(title)
    return titlebar

def screen_1(): # Sets up first screen
    # ===============================History layout setup==================================
    def histt():
        global hist, history
        hist = BoxLayout(orientation= "vertical", size_hint=(None,1), width=285)    #Creates parent layout for the widgets
        histc = hist.canvas
        with histc.before:    #Designs the widgets
            if theme == "black":
                Color(rgba=(0.15, 0.15, 0.15, 1))
            else:
                Color(rgba=(0.5,0.5,0.5, 1))

            hist.rect = RoundedRectangle(pos=hist.pos, size=hist.size, radius=[15])
        hist.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))     #Binds design with the widgets
        hist.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

        ht = BoxLayout(orientation= "horizontal",
                       size_hint=(1,None),
                       height=50,
                       padding = (20, 10,20,10))

        hbutton = Button(text="🗑️",  # Button to delete the calculator history
                         size_hint=(None, None),
                         bold=True,
                         background_color=(1, 1, 1, 0),
                         size= (30,30),
                         color= thm,
                         font_name=emoji,
                         font_size=20,)
        hbc =hbutton.canvas
        with hbc.before:
            if theme == "black":
                Color(rgba=(0.3,0.3,0.3, 1))
            else:
                Color(rgba=(1,1,1, 1))
            hbutton.rect = RoundedRectangle(pos=hbutton.pos,
                                            size=hbutton.size,
                                            radius=[5])

        hbutton.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))
        hbutton.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

        def btn_pressed(instance):
            with instance.canvas.before:
                if instance.text in "÷×−=+":
                    Color(rgba=(0.8, 0.4, 0, 1))
                elif instance.text in "AC⌫%":
                    Color(rgba=(0.2, 0.2, 0.2, 1))
                else:
                    if theme == "black":
                        Color(rgba=(0.1, 0.1, 0.1, 1))
                    else:
                        Color(rgba=(0.9,0.9,0.9, 1))

                instance.rect = RoundedRectangle(pos=instance.pos,
                                                 size=instance.size,
                                                 radius=[5])

        def btn_released(instance):
            del_history()
            history_pane.clear_widgets()
            for i in backend.get_history():  # Generates the history from the database
                tn = Button(text=i,
                            size_hint=(1, None),
                            height=60,
                            background_color=(1, 1, 1, 0),
                            font_size=20,
                            font_name=font)
                if len(tn.text) > 135:
                    tn.height = 60 + (30 * 9)
                elif len(tn.text) > 120:
                    tn.height = 60 + (30 * 8)
                elif len(tn.text) > 105:
                    tn.height = 60 + (30 * 7)
                elif len(tn.text) > 90:
                    tn.height = 60 + (30 * 6)
                elif len(tn.text) > 75:
                    tn.height = 60 + (30 * 5)
                elif len(tn.text) > 60:
                    tn.height = 60 + (30 * 4)
                elif len(tn.text) > 45:
                    tn.height = 60 + (30 * 3)
                elif len(tn.text) > 30:
                    tn.height = 60 + (30 * 2)
                elif len(tn.text) > 15:
                    tn.height = 60 + (30 * 1)

                with tn.canvas.before:
                    if theme == "black":
                        Color(rgba=(0.5, 0.5, 0.5, 1))
                    else:
                        Color(rgba=(0.8, 0.8, 0.8, 1))
                    tn.rr = RoundedRectangle(pos=tn.pos, size=tn.size, radius=[15])

                tn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
                tn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))

                def pressed(instance):
                    with instance.canvas.before:
                        if theme == "black":
                            Color(rgba=(0.3, 0.3, 0.3, 1))
                        else:
                            Color(rgba=(0.9, 0.9, 0.9, 1))
                        instance.rr = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])

                def released(instance):
                    global txt
                    with instance.canvas.before:
                        if theme == "black":
                            Color(rgba=(0.5, 0.5, 0.5, 1))
                        else:
                            Color(rgba=(0.8, 0.8, 0.8, 1))
                        txt = instance.text
                        equ.text = txt
                        instance.rr = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])

                tn.bind(on_press=pressed)
                tn.bind(on_release=released)
                history_pane.add_widget(tn)
            with instance.canvas.before:
                if instance.text in "÷×−=+":
                    Color(rgba=(1, 0.6, 0.05, 1))
                elif instance.text in "AC⌫%":
                    Color(rgba=(0.4, 0.4, 0.4, 1))
                else:
                    if theme == "black":
                        Color(rgba=(0.2, 0.2, 0.2, 1))
                    else:
                        Color(rgba=(1,1,1, 1))

                instance.rect = RoundedRectangle(pos=instance.pos,
                                                 size=instance.size,
                                                 radius=[5])

        hbutton.bind(on_press=btn_pressed)
        hbutton.bind(on_release=btn_released)

        history = ScrollView(size_hint=(None, 1), width=(280))  # Create a scroll layout for the history
        global history_pane
        history_pane = BoxLayout(orientation='vertical',
                                 size_hint_y=None,
                                 spacing=5,
                                 padding=5)

        history_pane.bind(minimum_height=history_pane.setter('height'))


        for i in backend.get_history():     #Generates the history from the database
            tn = Button(text=i,
                        size_hint=(1, None),
                        height=60,
                        background_color=(1, 1, 1, 0),
                        font_size=20,
                        font_name=font,
                        disabled_color=thm,
                        disabled=True
                        )
            if len(tn.text)> 135:
                tn.height= 60 + (30*9)
            elif len(tn.text)> 120:
                tn.height= 60 + (30*8)
            elif len(tn.text)> 105:
                tn.height= 60 + (30*7)
            elif len(tn.text)> 90:
                tn.height= 60 + (30*6)
            elif len(tn.text)> 75:
                tn.height= 60 + (30*5)
            elif len(tn.text)> 60:
                tn.height= 60 + (30*4)
            elif len(tn.text)> 45:
                tn.height= 60 + (30*3)
            elif len(tn.text)> 30:
                tn.height= 60 + (30*2)
            elif len(tn.text)> 15:
                tn.height= 60 + (30*1)

            with tn.canvas.before:
                if theme == "black":
                    Color(rgba=(0.5,0.5,0.5, 1))
                else:
                    Color(rgba=(0.8,0.8,0.8, 1))
                tn.rr= RoundedRectangle(pos= tn.pos, size=tn.size, radius=[15])

            tn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
            tn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))

            def pressed(instance):
                with instance.canvas.before:
                    if theme == "black":
                        Color(rgba=(0.3,0.3,0.3, 1))
                    else:
                        Color(rgba=(0.9,0.9,0.9, 1))
                    instance.rr = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])

            def released(instance):
                global txt
                with instance.canvas.before:
                    if theme == "black":
                        Color(rgba=(0.5, 0.5, 0.5, 1))
                    else:
                        Color(rgba=(0.8, 0.8, 0.8, 1))
                    def disp():
                        global cxc,txt2, txt
                        txt = "0"+instance.text
                        txt2 = ""
                        for c in txt:
                            if c == '²':
                                c = "^2"
                            elif c == '³':
                                c = "^3"
                            elif c == "−":
                                c = "-"
                            elif c == 'ʸ':
                                c = "^"
                            elif c == "E":
                                c = "e^"
                            elif c == 'ˣ':
                                c = "×10^"
                            elif c == "i":
                                c = "1/("
                            elif c == "r":
                                c = "√"
                            elif c == "R":
                                c = "³√"
                            elif c == "n":
                                c = "ln("
                            elif c == "l":
                                c = "log("
                            elif c == "s":
                                c = "sin("
                            elif c == "c":
                                c = "cos("
                            elif c == "t":
                                c = "tan("
                            elif c == "A":
                                c = "Ans"
                            elif c == "S":
                                c = "sinh("
                            elif c == "C":
                                c = "cosh("
                            elif c == "T":
                                c = "tanh("
                            txt2 = txt2 + c

                            equ.text = txt2
                            if len(txt) > 1:
                                equ.text = txt[1:]
                        cxc = txt[1:]

                        pq= backend.calculate(cxc, ans)
                        if pq !="Error":
                            answer.text = "=" + pq
                    disp()
                    instance.rr = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])


            tn.bind(on_press=pressed)
            tn.bind(on_release=released)
            history_pane.add_widget(tn)

        l = Label(text= "History",
                            font_size= 30,
                            size_hint=(None, None),
                            size = (200, 30),
                            bold= True)
        history.add_widget(history_pane)
        ht.add_widget(Label(text=""))
        ht.add_widget(l)
        ht.add_widget(Label(text=""))
        ht.add_widget(hbutton)
        hist.add_widget(ht)
        hist.add_widget(history)
        return hist

    # ==================================Calculator interface===============================
    def display():
        global answer, equ
        Display = BoxLayout(orientation= "vertical",
                            size_hint=(1,0.4),
                            padding=10,
                            spacing=5)

        # Display widgets for the equations and answers
        answer = TextInput(text= "=",
                           height= 42,
                           font_size= 24,
                           size_hint= (1, None),
                           foreground_color= (0.5,0.5,0.5,1),
                            readonly= True,
                           multiline= False,
                           background_color= (1,1,1,0),
                           font_name= font,
                           allow_copy= True,
                           selection_color= (0.6, 0.1,1, 0.3))
        equ =  TextInput(text= txt,
                         height= 100,
                         font_size= 60,
                         size_hint= (1, 0.7),
                         readonly= True,
                         foreground_color= thm,
                         padding= (0, 25,0,0),
                         multiline= True,
                         background_color= (1,1,1,0),
                         font_name= font,
                         allow_copy= True,
                         selection_color= (0.6, 0.1,1, 0.3))

        Display.add_widget(answer)
        Display.add_widget(equ)
        return Display

    def keys():
        key = GridLayout(rows=5,
                         cols=9,
                         padding= (10,10,10,0),
                         spacing= 8,
                         size_hint= (1,0.75))

        buttons = [     #All keys in the calculator
            # Row 1
            "(", ")", "x!", "1/x", "×10ˣ", "AC", "⌫", "%", "÷",
            # Row 2
            "Hex", "x²", "x³", "xʸ", "eˣ", "7", "8", "9", "×",
            # Row 3
            "f(x)", "²√x", "³√x", "ln", "log₁₀", "4", "5", "6", "−",
            # Row 4
            "Plot", "sin", "cos", "tan", "e", "1", "2", "3", "+",
            # Row 5
            "Style", "sinh", "cosh", "tanh", "π", "Ans", "0", ".", "=",
        ]

        for i in buttons:       #Creates each button in the calculator
            btn = Button(
                text=i,
                font_size=20,
                color=thm,
                bold=True,
                background_color=(0.2, 0.2, 0.2, 0),
                font_name=font,
            )

            # Initial color
            with btn.canvas.before:
                if btn.text in "÷×−=+":
                    Color(rgba=(1, 0.6, 0.1, 1))
                elif btn.text in "AC⌫%":
                    if theme == "black":
                        Color(rgba=(0.4, 0.4, 0.4, 1))
                    else:
                        Color(rgba=(0.7,0.7,0.7, 1))
                elif btn.text == "Hex" or btn.text=="Style" or btn.text=="Plot" or btn.text=="f(x)":
                    btn.color= (0.9,0.9,0.9,1)
                    Color(rgba=(0.35, 0, 0.8, 1))
                else:
                    if theme == "black":
                        Color(rgba=(0.2, 0.2, 0.2, 1))
                    else:
                        Color(rgba=(1, 1, 1, 1))
                btn.rect = RoundedRectangle(pos=btn.pos,
                                            size=btn.size,
                                            radius=[20])

            # Ensure rectangle follows button
            btn.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))
            btn.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

            # Press/release handlers
            def btn_pressed(instance):
                with instance.canvas.before:
                    if instance.text in "÷×−=+":
                        Color(rgba=(0.8, 0.4, 0, 1))
                    elif instance.text in "AC⌫%":
                        if theme == "black":
                            Color(rgba=(0.2, 0.2, 0.2, 1))
                        else:
                            Color(rgba=(0.5,0.5,0.5, 1))
                    elif instance.text == "Hex" or instance.text=="Style" or instance.text=="Plot" or instance.text=="f(x)":
                        Color(rgba=(0.25, 0, 0.7, 1))
                    else:
                        if theme == "black":
                            Color(rgba=(0.15, 0.15, 0.15, 1))
                        else:
                            Color(rgba=(0.9,0.9,0.9, 1))
                    instance.rect = RoundedRectangle(pos=instance.pos,
                                                     size=instance.size,
                                                     radius=[20])

            # Ensures operators will override old operators
            def operators(x):
                global txt
                if txt[-1] in "÷×−+":
                    txt = txt[:-1] + x
                else:
                    txt = txt + x


            def btn_released(instance):
                global txt, theme, thm, txt2
                #Designs each key
                with instance.canvas.before:
                    if instance.text in "÷×−=+":
                        Color(rgba=(1, 0.6, 0.1, 1))
                    elif instance.text in "AC⌫%":
                        if theme == "black":
                            Color(rgba=(0.4, 0.4, 0.4, 1))
                        else:
                            Color(rgba=(0.7,0.7,0.7, 1))

                    elif instance.text == "Hex" or instance.text=="Style" or instance.text=="Plot" or instance.text=="f(x)":
                        Color(rgba=(0.35, 0, 0.8, 1))
                    else:
                        if theme == "black":
                            Color(rgba=(0.2, 0.2, 0.2, 1))
                        else:
                            Color(rgba=(1, 1, 1, 1))
                    instance.rect = RoundedRectangle(pos=instance.pos,
                                                     size=instance.size,
                                                     radius=[20])

                def text_size(instance):
                    #Creates functionality for each key
                    def disp():
                        global cxc,txt2
                        txt2 = ""
                        for c in txt:
                            if c == '²':
                                c = "^2"
                            elif c == '³':
                                c = "^3"
                            elif c == "−":
                                c = "-"
                            elif c == 'ʸ':
                                c = "^"
                            elif c == "E":
                                c = "e^"
                            elif c == 'ˣ':
                                c = "×10^"
                            elif c == "i":
                                c = "1/("
                            elif c == "r":
                                c = "√"
                            elif c == "R":
                                c = "³√"
                            elif c == "n":
                                c = "ln("
                            elif c == "l":
                                c = "log("
                            elif c == "s":
                                c = "sin("
                            elif c == "c":
                                c = "cos("
                            elif c == "t":
                                c = "tan("
                            elif c == "A":
                                c = "Ans"
                            elif c == "S":
                                c = "sinh("
                            elif c == "C":
                                c = "cosh("
                            elif c == "T":
                                c = "tanh("
                            txt2 = txt2 + c

                            equ.text = txt2
                            if len(txt) > 1:
                                equ.text = txt2[1:]
                        cxc = txt2[1:]

                        pq= backend.calculate(cxc, ans)
                        if pq !="Error":
                            answer.text = "=" + pq

                    #Creates a display animation for displaying answer
                    disp()
                    answer.multiline = False
                    equ.multiline = True
                    equ.height = 100
                    equ.font_size = 60
                    equ.foreground_color = thm
                    answer.height = 42
                    answer.font_size = 24
                    answer.foreground_color = (0.5, 0.5, 0.5, 1)
                    length = len(equ.text)
                    if length > 23:
                        equ.font_size = 30
                    elif length > 17:
                        equ.font_size = 40
                    elif length > 10:
                        equ.font_size = 50
                    else:
                        equ.font_size = 60

                #Adds more functionality to the code
                if instance.text == "(":
                    txt = txt + '('
                    text_size(instance)
                if instance.text == ")":
                    txt = txt + ')'
                    text_size(instance)
                if instance.text == "AC":
                    txt = "0"
                    text_size(instance)
                    answer.text= "="
                if instance.text == "⌫":
                    if len(txt) > 1:
                        txt= txt[:-1]
                    text_size(instance)
                if instance.text == "%":
                    txt = txt + '%'
                    text_size(instance)
                if instance.text == "÷":
                    operators('÷')
                    text_size(instance)
                if instance.text == "x²":
                    txt = txt + '²'
                    text_size(instance)
                if instance.text == "x³":
                    txt = txt + '³'
                    text_size(instance)
                if instance.text == "xʸ":
                    txt = txt + 'ʸ'
                    text_size(instance)
                if instance.text == "eˣ":
                    txt = txt + 'E'
                    text_size(instance)
                if instance.text == "×10ˣ":
                    txt = txt + 'ˣ'
                    text_size(instance)
                if instance.text == "7":
                    txt = txt + '7'
                    text_size(instance)
                if instance.text == "8":
                    txt = txt + '8'
                    text_size(instance)
                if instance.text == "9":
                    txt = txt + '9'
                    text_size(instance)
                if instance.text == "×":
                    operators('×')
                    text_size(instance)
                if instance.text == "1/x":
                    txt = txt + 'i'
                    text_size(instance)
                if instance.text == "²√x":
                    txt = txt + 'r'
                    text_size(instance)
                if instance.text == "³√x":
                    txt = txt + 'R'
                    text_size(instance)
                if instance.text == "ln":
                    txt = txt + 'n'
                    text_size(instance)
                if instance.text == "log₁₀":
                    txt = txt + 'l'
                    text_size(instance)
                if instance.text == "4":
                    txt = txt + '4'
                    text_size(instance)
                if instance.text == "5":
                    txt = txt + '5'
                    text_size(instance)
                if instance.text == "6":
                    txt = txt + '6'
                    text_size(instance)
                if instance.text == "−":
                    operators('−')
                    text_size(instance)
                if instance.text == "x!":
                    txt = txt + '!'
                    text_size(instance)
                if instance.text == "sin":
                    txt = txt + 's'
                    text_size(instance)
                if instance.text == "cos":
                    txt = txt + 'c'
                    text_size(instance)
                if instance.text == "tan":
                    txt = txt + 't'
                    text_size(instance)
                if instance.text == "e":
                    txt = txt + 'e'
                    text_size(instance)
                if instance.text == "1":
                    txt = txt + '1'
                    text_size(instance)
                if instance.text == "2":
                    txt = txt + '2'
                    text_size(instance)
                if instance.text == "3":
                    txt = txt + '3'
                    text_size(instance)
                if instance.text == "+":
                    operators('+')
                    text_size(instance)
                if instance.text == "Ans":
                    txt = txt + 'A'
                    text_size(instance)
                if instance.text == "sinh":
                    txt = txt + 'S'
                    text_size(instance)
                if instance.text == "cosh":
                    txt = txt + 'C'
                    text_size(instance)
                if instance.text == "tanh":
                    txt = txt + 'T'
                    text_size(instance)
                if instance.text == "π":
                    txt = txt + 'π'
                    text_size(instance)
                if instance.text == "0":
                    txt = txt + '0'
                    text_size(instance)
                if instance.text == ".":
                    txt = txt + '.'
                    text_size(instance)
                if instance.text == "=":
                    global ans
                    pq = backend.calculate(cxc, ans)
                    answer.text= "="+pq
                    if pq != "Error":
                        ans = pq
                        backend.write_history(txt2[1:])
                        history_pane.clear_widgets()
                        for i in backend.get_history():  # Generates the history from the database
                            tn = Button(text=i,
                                        size_hint=(1, None),
                                        height=60,
                                        background_color=(1, 1, 1, 0),
                                        font_size=20,
                                        font_name=font,
                                        disabled_color=thm,
                                        disabled=True
                                        )
                            if len(tn.text) > 135:
                                tn.height = 60 + (30 * 9)
                            elif len(tn.text) > 120:
                                tn.height = 60 + (30 * 8)
                            elif len(tn.text) > 105:
                                tn.height = 60 + (30 * 7)
                            elif len(tn.text) > 90:
                                tn.height = 60 + (30 * 6)
                            elif len(tn.text) > 75:
                                tn.height = 60 + (30 * 5)
                            elif len(tn.text) > 60:
                                tn.height = 60 + (30 * 4)
                            elif len(tn.text) > 45:
                                tn.height = 60 + (30 * 3)
                            elif len(tn.text) > 30:
                                tn.height = 60 + (30 * 2)
                            elif len(tn.text) > 15:
                                tn.height = 60 + (30 * 1)

                            with tn.canvas.before:
                                if theme == "black":
                                    Color(rgba=(0.5, 0.5, 0.5, 1))
                                else:
                                    Color(rgba=(0.8, 0.8, 0.8, 1))
                                tn.rr = RoundedRectangle(pos=tn.pos, size=tn.size, radius=[15])

                            tn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
                            tn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))

                            def pressed(instance):
                                with instance.canvas.before:
                                    if theme == "black":
                                        Color(rgba=(0.3, 0.3, 0.3, 1))
                                    else:
                                        Color(rgba=(0.9, 0.9, 0.9, 1))
                                    instance.rr = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])

                            def released(instance):
                                global txt
                                with instance.canvas.before:
                                    if theme == "black":
                                        Color(rgba=(0.5, 0.5, 0.5, 1))
                                    else:
                                        Color(rgba=(0.8, 0.8, 0.8, 1))

                                    def disp():
                                        global cxc, txt2, txt
                                        txt = "0" + instance.text
                                        txt2 = ""
                                        for c in txt:
                                            if c == '²':
                                                c = "^2"
                                            elif c == '³':
                                                c = "^3"
                                            elif c == "−":
                                                c = "-"
                                            elif c == 'ʸ':
                                                c = "^"
                                            elif c == "E":
                                                c = "e^"
                                            elif c == 'ˣ':
                                                c = "×10^"
                                            elif c == "i":
                                                c = "1/("
                                            elif c == "r":
                                                c = "√"
                                            elif c == "R":
                                                c = "³√"
                                            elif c == "n":
                                                c = "ln("
                                            elif c == "l":
                                                c = "log("
                                            elif c == "s":
                                                c = "sin("
                                            elif c == "c":
                                                c = "cos("
                                            elif c == "t":
                                                c = "tan("
                                            elif c == "A":
                                                c = "Ans"
                                            elif c == "S":
                                                c = "sinh("
                                            elif c == "C":
                                                c = "cosh("
                                            elif c == "T":
                                                c = "tanh("
                                            txt2 = txt2 + c

                                            equ.text = txt2
                                            if len(txt) > 1:
                                                equ.text = txt[1:]
                                        cxc = txt2[1:]

                                        pq = backend.calculate(cxc, ans)
                                        if pq != "Error":
                                            answer.text = "=" + pq

                                    disp()
                                    instance.rr = RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])

                            tn.bind(on_press=pressed)
                            tn.bind(on_release=released)
                            history_pane.add_widget(tn)
                    answer.height = 100
                    answer.font_size = 60
                    answer.foreground_color = thm
                    equ.height = 42
                    equ.font_size = 24
                    equ.foreground_color = (0.5, 0.5, 0.5, 1)
                    length = len(answer.text)
                    if length > 23:
                        answer.font_size = 30
                    elif length > 17:
                        answer.font_size = 40
                    elif length > 10:
                        answer.font_size = 50
                    else:
                        answer.font_size = 60
                    answer.multiline = True
                    equ.multiline= False
                if instance.text == "Style":
                    if theme== "black":
                        write_theme("white")
                    else:
                        write_theme("black")
                    Window.opacity = 1
                    Window.borderless = True
                    Window.minimize()
                    try:
                        t = threading.Thread(target= restart_self)
                        t.daemon=True
                        t.start()
                    except:
                        popup = Popup(
                            title="Error",
                            size_hint=(0.3, 0.2),
                            auto_dismiss=False,
                            background_color=(1, 1, 1, 0),
                        )
                        with popup.canvas.before:
                            Color(rgba=(0.3, 0.3, 0.3, 0.8))
                            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[15])

                        popup.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))  # Binds design with the widgets
                        popup.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))
                        popup.open()
                        Window.opacity = 1
                        Window.borderless = False
                        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
                if instance.text == "Plot":
                    def open_plot_popup():
                        popup = Popup(
                            title="Graph ploter",
                            size_hint=(0.6, 0.5),
                            auto_dismiss=False,
                            background_color=(1,1,1,0),
                        )

                        with popup.canvas.before:
                            Color(rgba=(0.3, 0.3, 0.3, 0.8))
                            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[15])

                        popup.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))  # Binds design with the widgets
                        popup.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

                        layout = BoxLayout(orientation="vertical", spacing=10, padding=15)

                        err = Label(text="", color=(1, 0, 0, 1), size_hint=(1, 0.15))

                        x_input = TextInput(
                            hint_text="x-axis = 1,2,3,4",
                            multiline=False,
                            background_color=(1,1,1,1),
                            font_name=font,
                            font_size= 18
                        )

                        y_input = TextInput(
                            hint_text="y-axis = 10,20,30,40",
                            multiline=False,
                            background_color=(1,1,1,1),
                            font_name=font,
                            font_size= 18
                        )

                        # ---------- parsing helper ----------
                        def parse_array(text):
                            for c in text:
                                if c not in "0123456789.,":  # allow decimal dots too
                                    return None
                            if not text:
                                return None
                            try:
                                return [float(i) for i in text.split(",") if i.strip() != ""]
                            except:
                                return None

                        # ---------- process button ----------
                        def process(instance):
                            xs = parse_array(x_input.text)
                            ys = parse_array(y_input.text)

                            if xs is None or ys is None:
                                err.text = "Invalid number format"
                                return

                            if len(xs) != len(ys):
                                err.text = "X and Y must have the same length"
                                return

                            err.text = ""
                            backend.plot([xs, ys])
                            popup.dismiss()

                        # ---------- buttons ----------
                        btns = BoxLayout(size_hint=(1, 1), spacing=10)

                        close_btn = Button(text="Close", background_color=(1,1,1,0))
                        close_btn.bind(on_release=lambda x: popup.dismiss())
                        with close_btn.canvas.before:
                            Color(rgba=(0.8, 0,0, 1))
                            close_btn.rr = RoundedRectangle(pos=close_btn.pos, size=close_btn.size, radius=[5])

                        close_btn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
                        close_btn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))

                        plot_btn = Button(text="Plot", background_color=(1,1,1,0))
                        with plot_btn.canvas.before:
                            Color(rgba=(0.5,0.5,0.5, 1))
                            plot_btn.rr = RoundedRectangle(pos=plot_btn.pos, size=plot_btn.size, radius=[5])

                        plot_btn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
                        plot_btn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))
                        plot_btn.bind(on_release=process)

                        btns.add_widget(close_btn)
                        btns.add_widget(plot_btn)

                        # ---------- assemble ----------
                        layout.add_widget(Label(text="X-axis", font_name=font))
                        layout.add_widget(x_input)
                        layout.add_widget(Label(text="Y-axis", font_name=font))
                        layout.add_widget(y_input)
                        layout.add_widget(err)
                        layout.add_widget(btns)

                        popup.content = layout

                        popup.open()
                    open_plot_popup()
                if instance.text == "f(x)":
                    def open_fx_popup():
                        import math

                        popup = Popup(
                            title="Graph ploter",
                            size_hint=(0.6, 0.5),
                            auto_dismiss=False,
                            background_color=(1, 1, 1, 0),
                        )
                        with popup.canvas.before:
                            Color(rgba=(0.3, 0.3, 0.3, 0.8))
                            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[15])

                        popup.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))  # Binds design with the widgets
                        popup.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

                        layout = BoxLayout(orientation="vertical", spacing=10, padding=15)
                        err = Label(text="", color=(1, 0, 0, 1), size_hint=(1, 0.15))

                        func_input = TextInput(
                            hint_text="Function = x(2x+1), 3xsin(4x), xcos(2x)",
                            multiline=False,
                            background_color=(1,1,1,1),
                            font_name=font,
                            font_size= 18
                        )

                        x_input = TextInput(
                            hint_text="x-axis = 10,20,30,40  or  range(1,70,10)",
                            multiline=False,
                            background_color=(1,1,1,1),
                            font_name=font,
                            font_size= 18
                        )

                        # ---------- helper: parse number list ----------
                        def parse_list(text):
                            if not text:
                                return None
                            for c in text:
                                if c not in "0123456789.,-":
                                    return None
                            try:
                                arr = [float(v) for v in text.split(",") if v.strip() != ""]
                                return arr if len(arr) > 0 else None
                            except:
                                return None

                        # ---------- helper: parse range(1,70,10) ----------
                        def parse_range(text):
                            if not text.startswith("range(") or not text.endswith(")"):
                                return None
                            try:
                                inner = text[6:-1]  # remove range(  )
                                parts = [p.strip() for p in inner.split(",")]

                                if len(parts) != 3:
                                    return None

                                start = float(parts[0])
                                end = float(parts[1])
                                step = float(parts[2])

                                if step <= 0:
                                    return None
                                if end <= start:
                                    return None
                                if step > (end - start):
                                    return None

                                values = []
                                x = start
                                while x <= end:
                                    values.append(x)
                                    x += step

                                return values if len(values) > 0 else None

                            except:
                                return None

                        # ---------- main parser for x-axis ----------
                        def parse_x_axis(text):
                            if "range(" in text:
                                return parse_range(text)
                            return parse_list(text)

                        # ---------- button logic ----------
                        def process(instance):
                            func_str = func_input.text.strip()
                            xs = parse_x_axis(x_input.text.strip())

                            if xs is None:
                                err.text = "Invalid x-axis values"
                                return

                            if not func_str:
                                err.text = "Function is empty"
                                return

                            # Try evaluating using backend.fx
                            try:
                                result = backend.fx(func_str, xs)
                            except:
                                err.text = "Invalid function syntax"
                                return

                            if result is None:
                                err.text = "Function parsing error"
                                return

                            x_arr, y_arr = result

                            # Detect invalid y values
                            if any([math.isnan(v) or math.isinf(v) for v in y_arr]):
                                err.text = "Math domain error (log of negative, sqrt of negative, etc.)"
                                return

                            err.text = ""
                            backend.plot([x_arr, y_arr])
                            popup.dismiss()

                        # ---------- buttons ----------
                        btns = BoxLayout(size_hint=(1, 1), spacing=10)

                        close_btn = Button(text="Close", background_color=(1, 1, 1, 0))
                        close_btn.bind(on_release=lambda x: popup.dismiss())
                        with close_btn.canvas.before:
                            Color(rgba=(0.8, 0, 0, 1))
                            close_btn.rr = RoundedRectangle(pos=close_btn.pos, size=close_btn.size, radius=[5])

                        close_btn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
                        close_btn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))

                        plot_btn = Button(text="Plot", background_color=(1, 1, 1, 0))
                        with plot_btn.canvas.before:
                            Color(rgba=(0.5, 0.5, 0.5, 1))
                            plot_btn.rr = RoundedRectangle(pos=plot_btn.pos, size=plot_btn.size, radius=[5])

                        plot_btn.bind(pos=lambda instance, value: setattr(instance.rr, 'pos', value))
                        plot_btn.bind(size=lambda instance, value: setattr(instance.rr, 'size', value))
                        plot_btn.bind(on_release=process)

                        btns.add_widget(close_btn)
                        btns.add_widget(plot_btn)

                        # ---------- assemble ----------
                        layout.add_widget(Label(text="Function", font_name=font))
                        layout.add_widget(func_input)
                        layout.add_widget(Label(text="X-axis", font_name=font))
                        layout.add_widget(x_input)
                        layout.add_widget(err)
                        layout.add_widget(btns)

                        popup.content = layout
                        popup.open()

                    open_fx_popup()

            btn.bind(on_press=btn_pressed)
            btn.bind(on_release=btn_released)

            key.add_widget(btn)

        return key


    calc_interface = BoxLayout(orientation="vertical",
                               size_hint=(1,1))
    calc_interface.add_widget(display())
    calc_interface.add_widget(keys())

    # =======================Adds the necessary widgets to the app=============================
    Screen1 = Screen(size_hint=(1, 1))  # Creates first screen
    calc = GridLayout(rows=1,
                      cols=2,
                      size_hint=(1, 1),
                      padding=(10,0,10,15))
    calc.add_widget(histt())
    calc.add_widget(calc_interface)
    Screen1.add_widget(calc)
    return Screen1



# Root functions
screen_manager.add_widget(screen_1())
root.add_widget(title_bar())
root.add_widget(screen_manager)

if __name__ == "__main__":
    App.build = lambda self: root    # Adds the root layout to the window app
    App().run() # Runs the app