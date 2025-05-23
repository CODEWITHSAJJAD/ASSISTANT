from PyQt5.QtWidgets import QApplication,QMainWindow,QTextEdit,QStackedWidget,QWidget,QLineEdit,QGridLayout,QVBoxLayout,QBoxLayout,QPushButton,QFrame,QLabel,QSizePolicy,QHBoxLayout
from PyQt5.QtGui import QIcon,QMovie,QPainter,QColor,QTextCharFormat,QFont,QPixmap,QTextBlockFormat
from PyQt5.QtCore import Qt,QSize,QTimer
from dotenv import dotenv_values
import sys
import os
env_vars=dotenv_values(".env")
Assistantname=env_vars.get("ASSISTANTNAME")
current_dir=os.getcwd()
old_chat_message=""
TempDirPath=rf"{current_dir}\Frontend\Files"
GraphicsDirPath=rf"{current_dir}\Frontend\Graphics"
def AnswerModifier(Answer):
    lines=Answer.split('\n')
    non_empty_lines=[line for line in lines if line.strip()]
    modified_answer='\n'.join(non_empty_lines)
    return modified_answer
def QueryModifier(Query):
    new_query=Query.lower().strip()
    query_words=new_query.split()
    question_words=["how","what","who","where","when","why","which","whose","whom","can you","what's","how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1]
        else:
            new_query+="?"                       
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1]+"."
        else:
            new_query+="."
    return new_query.capitalize()
def SetMicrophoneStatus(command):
    with open(rf"{TempDirPath}\Mic.data","w",encoding="utf-8") as file:
        file.write(command)
def GetMicrophoneStatus():
    with open(rf"{TempDirPath}\Mic.data","r",encoding="utf-8") as file:
        Status=file.read()
    return Status
def SetAssistantStatus(command):
    with open(rf"{TempDirPath}\Status.data","w",encoding="utf-8") as file:
        file.write(command)
def GetAssistantStatus():
    with open(rf"{TempDirPath}\Status.data","r",encoding="utf-8") as file:
        Status=file.read()
    return Status
def MicButtonInitialed():
    SetMicrophoneStatus("False")
def MicButtonClosed():
    SetMicrophoneStatus("True")
def GraphicsDirectoryPath(Filename):
    path=rf"{GraphicsDirPath}\{Filename}"
    return path
def TempDirectoryPath(Filename):
    path=rf"{TempDirPath}\{Filename}"
    return path
def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data","w",encoding="utf-8") as file:
        file.write(Text)
class ChatScren(QWidget):
    def __init__(self):
        super(ChatScren, self).__init__()  # Corrected here
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_lable=QLabel()
        self.gif_lable.setStyleSheet("border: none;")
        movie=QMovie(GraphicsDirectoryPath('jarvis.gif'))
        max_gif_size_W=480
        max_gif_size_H=270
        movie.setScaledSize(QSize(max_gif_size_W,max_gif_size_H))
        self.gif_lable.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_lable.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_lable)
        self.label=QLabel("")
        self.label.setStyleSheet("Color:white; font-size:16px; margin-right:105px;border:none;margin-top:-30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_lable)
        font=QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start()
        self.setStyleSheet("""
                            QScrollBar:vertical{
                           border:none;
                           background:black;
                           width:10px;
                           margin:0ox 0px 0px 0px
                           }
                           QScrollBar::handle:vertical{
                           background:white;
                           min-height:20px;
                           }
                           QScrollBar::add-line:vertical{
                           background:black;
                           subcontrol-position:bottom;
                           subcontrol-origin:margin;
                           }
                           QScrollBAr::sub-line:vertical{
                           background:black;
                           subcontrol-position:top;
                           subcontrol-origin:margin;
                           height:10px;
                           }
                           QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{
                           border:none;
                           background:none;
                           color:none;
                           }
                           QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
                           background:none;
                           }
                    """)
    def loadMessages(self):
        global old_chat_message
        with open(TempDirectoryPath('Responses.data'),"r",encoding='utf-8') as file:
            messages=file.read()
            if None==messages:
                pass
            elif len(messages)<=1:
                pass
            elif str(old_chat_message)==str(messages):
                pass
            else:
                self.addMessage(message=messages,color='White')
                old_chat_message=messages
    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'),"r",encoding='utf-8') as file:
            messages=file.read()
            self.label.setText(messages)
    def load_icon(self,path,width=60,height=60):
        pixmap=QPixmap(path)
        new_pixmap=pixmap.scaled(width,height)
        self.icon_label.setPixmap(new_pixmap)
    def toggle_icon(self,event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('microphone.png'),60,60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('mute.png'),60,60)
            MicButtonClosed()            
            self.toggled=not self.toggled
    def addMessage(self,message,color):
        cursor=self.chat_text_edit.textCursor()
        format=QTextCharFormat()
        formatm=QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message+"\n")
        self.chat_text_edit.setTextCursor(cursor)
class InitialScreen(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        desktop=QApplication.desktop()
        screen_width=desktop.screenGeometry().width()
        screen_height=desktop.screenGeometry().height()
        content_layout=QVBoxLayout()
        content_layout.setContentsMargins(0,0,0,0)
        gif_label=QLabel()
        movie=QMovie(GraphicsDirectoryPath('jarvis.gif'))
        gif_label.setMovie(movie)
        max_gif_size_H=int(screen_width/16*9)
        movie.setScaledSize(QSize(screen_width,max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)        
        self.icon_label=QLabel()
        pixmap=QPixmap(GraphicsDirectoryPath('microphone.png'))
        new_pixmap=pixmap.scaled(60,60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150,150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled=True
        self.toggle_icon()
        self.icon_label.mousePressEvent=self.toggle_icon
        self.label=QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px;margin-bottom:0;")
        content_layout.addWidget(gif_label,alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label,alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label,alignment=Qt.AlignCenter)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color:black;")
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'),"r",encoding='utf-8') as file:
            messages=file.read()
            self.label.setText(messages)
    def load_icon(self,path,width=60,height=60):
        pixmap=QPixmap(path)
        new_pixmap=pixmap.scaled(width,height)
        self.icon_label.setPixmap(new_pixmap)
    def toggle_icon(self,event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('microphone.png'),60,60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('mute.png'),60,60)
            MicButtonClosed()
        self.toggled=not self.toggled
class MessageScreen(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        desktop=QApplication.desktop()
        screen_width=desktop.screenGeometry().width()
        screen_height=desktop.screenGeometry().height()
        layout=QVBoxLayout()        
        label=QLabel("")
        layout.addWidget(label)
        chat_section=ChatScren()
        layout.addWidget(chat_section)                
        self.setLayout(layout)        
        self.setStyleSheet("background-color:black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
class CustomTopBar(QWidget):
    def __init__(self, parent,stacked_widged):
        super().__init__(parent)
        self.initUI()
        self.current_section=None
        self.stacked_widged=stacked_widged
    def initUI(self):
        self.setFixedHeight(50)
        layout=QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button=QPushButton()
        home_icon=QIcon(GraphicsDirectoryPath('home.png'))
        home_button.setIcon(home_icon)
        home_button.setText(" HOME")
        home_button.setStyleSheet("height:40px;line-height:40px;background-color:white;color:black")
        message_button=QPushButton()
        message_icon=QIcon(GraphicsDirectoryPath('chat.png'))
        message_button.setIcon(message_icon)
        message_button.setText(" CHAT")
        message_button.setStyleSheet("height:40px;line-height:40px;background-color:white;color:black")
        minimize_button=QPushButton()
        minimize_icon=QIcon(GraphicsDirectoryPath('minimize1.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button=QPushButton()
        self.maximize_icon=QIcon(GraphicsDirectoryPath('maximize.png'))
        self.restore_icon=QIcon(GraphicsDirectoryPath('minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        # self.maximize_icon.setFlash(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button=QPushButton()
        close_icon=QIcon(GraphicsDirectoryPath('close.png'))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)
        line_frame=QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color:black;")
        tittle_label=QLabel()
        tittle_label.setStyleSheet("color:black; font-size:18px;; background-color:white")
        home_button.clicked.connect(lambda:self.stacked_widged.setCurrentIndex(0))
        message_button.clicked.connect(lambda:self.stacked_widged.setCurrentIndex(1))
        layout.addWidget(tittle_label)
        layout.addStretch(1)    
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable=True
        self.offset=None
    def paintEvent(self,event):
        painter=QPainter(self)
        painter.fillRect(self.rect(),Qt.white)
        super().paintEvent(event)
    def minimizeWindow(self):
        self.parent().showMinimized()
    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)
    def closeWindow(self):
        self.parent().close()
    def mousePressEvent(self,event):
        if self.draggable:
            self.offset=event.pos()
    def mouseMoveEvent(self,event):
        if self.draggable and self.offset:
            new_pos=event.globalPos()-self.offset
            self.parent().move(new_pos)
    def showMessageScreen(self):
        if self.current_screen is not None:
            self.currentScreen.hide()
        message_screen=MessageScreen(self)
        layout=self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen=message_screen
    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        Initial_screen=InitialScreen(self)
        layout=self.parent().layout()
        if layout is not None:
            layout.addWidget(Initial_screen)
        self.current_screen=Initial_screen
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
    def initUI(self):
        desktop=QApplication.desktop()
        screen_width=desktop.screenGeometry().width()
        screen_height=desktop.screenGeometry().height()
        stacked_widget=QStackedWidget(self)
        initial_screen=InitialScreen()
        message_screen=MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0,0,screen_width,screen_height)
        self.setStyleSheet("background-color:black;")
        top_bar=CustomTopBar(self,stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)
def GraphicalUerInterFace():
    app=QApplication(sys.argv)
    Window=MainWindow()
    Window.show()
    sys.exit(app.exec_())
if __name__=="__main__":
    GraphicalUerInterFace()
####################################################
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, 
                            QLineEdit, QVBoxLayout, QPushButton, QFrame, QLabel, QHBoxLayout,
                            QScrollArea, QSizePolicy, QSpacerItem)
from PyQt5.QtGui import (QIcon, QMovie, QPainter, QColor, QTextCharFormat, QFont, 
                        QPixmap, QTextBlockFormat, QPalette, QLinearGradient)
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from dotenv import dotenv_values
import sys
import os
import webbrowser

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("ASSISTANTNAME")
Username = env_vars.get("USERNAME")

current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how","what","who","where","when","why","which","whose","whom","can you","what's","how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1]
        else:
            new_query += "?"                       
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicrophoneStatus(command):
    with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
        file.write(command)

def GetMicrophoneStatus():
    with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def SetAssistantStatus(command):
    with open(rf"{TempDirPath}\Status.data", "w", encoding="utf-8") as file:
        file.write(command)

def GetAssistantStatus():
    with open(rf"{TempDirPath}\Status.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    path = rf"{GraphicsDirPath}\{Filename}"
    return path

def TempDirectoryPath(Filename):
    path = rf"{TempDirPath}\{Filename}"
    return path

def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        self._animation.setDuration(200)
        
    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-5, -5, 5, 5))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(5, 5, -5, -5))
        self._animation.start()
        super().leaveEvent(event)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import webbrowser


class SideBar(QWidget):
    def __init__(self, parent=None, stacked_widget=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setFixedWidth(250)
        self.setStyleSheet("""
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f0c29, stop:1 #302b63
            );
            border-radius: 15px;
            margin: 10px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(20)

        # ----- User Profile -----
        user_profile = QWidget()
        user_layout = QVBoxLayout(user_profile)
        user_layout.setAlignment(Qt.AlignCenter)

        self.user_avatar = QLabel()
        self.user_avatar.setFixedSize(80, 80)
        self.user_avatar.setPixmap(QPixmap(GraphicsDirectoryPath('user.png')).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.user_avatar.setStyleSheet("""
            border-radius: 40px;
            border: 2px solid #00d2ff;
        """)

        self.user_name = QLabel(Username or "User")
        self.user_name.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        """)
        self.user_name.setAlignment(Qt.AlignCenter)

        user_layout.addWidget(self.user_avatar)
        user_layout.addWidget(self.user_name)

        # ----- Navigation Buttons -----
        nav_buttons = QWidget()
        nav_layout = QVBoxLayout(nav_buttons)
        nav_layout.setSpacing(10)

        self.home_btn = self.create_nav_button(" Home", 'home.png', lambda: self.stacked_widget.setCurrentIndex(0))
        self.chat_btn = self.create_nav_button(" Chat", 'chat.png', lambda: self.stacked_widget.setCurrentIndex(1))
        self.settings_btn = self.create_nav_button(" Settings", 'setting.png', lambda: print("Open Settings"))

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.chat_btn)
        nav_layout.addWidget(self.settings_btn)

        # ----- Spacer -----
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # ----- Social Links -----
        social_links = QWidget()
        social_layout = QVBoxLayout(social_links)
        social_layout.setSpacing(10)

        social_label = QLabel("Connect with me")
        social_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 5px;
        """)

        icon_size = QSize(30, 30)

        linkedin_btn = self.create_social_button('linkedin.png', "https://linkedin.com", icon_size)
        github_btn = self.create_social_button('github.png', "https://github.com", icon_size)
        instagram_btn = self.create_social_button('instagram.png', "https://instagram.com", icon_size)
        youtube_btn = self.create_social_button('youtube.png', "https://youtube.com", icon_size)

        social_icons_layout = QHBoxLayout()
        social_icons_layout.addWidget(linkedin_btn)
        social_icons_layout.addWidget(github_btn)
        social_icons_layout.addWidget(instagram_btn)
        social_icons_layout.addWidget(youtube_btn)

        social_layout.addWidget(social_label)
        social_layout.addLayout(social_icons_layout)

        # ----- Copyright -----
        copyright_label = QLabel("© 2025 @CodeWithSajjad")
        copyright_label.setStyleSheet("""
            background: None;
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            margin-top: 20px;
        """)
        copyright_label.setAlignment(Qt.AlignCenter)

        # ----- Assemble Layout -----
        layout.addWidget(user_profile)
        layout.addWidget(nav_buttons)
        layout.addItem(spacer)
        layout.addWidget(social_links)
        layout.addWidget(copyright_label)

    def create_nav_button(self, text, icon_name, callback):
        button = QPushButton(text)
        button.setIcon(QIcon(GraphicsDirectoryPath(icon_name)))
        button.setIconSize(QSize(20, 20))
        button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 16px;
                text-align: left;
                padding: 12px;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-left: 4px solid #00d2ff;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        button.clicked.connect(callback)
        return button

    def create_social_button(self, icon_name, link, size):
        button = QPushButton()
        button.setIcon(QIcon(GraphicsDirectoryPath(icon_name)))
        button.setIconSize(size)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
            }
        """)
        button.clicked.connect(lambda: webbrowser.open(link))
        return button

class ChatScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.messages = []  # Add this to track messages
        
    def initUI(self):
        self.setStyleSheet("""
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f0c29, stop:1 #302b63
            );
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Chat Area
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(30, 30, 30, 0.3);
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.1);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f0c29, stop:1 #302b63
            );
            }
        """)
        
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: transparent;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_layout.setSpacing(15)
        self.chat_layout.setAlignment(Qt.AlignTop)
        
        self.chat_area.setWidget(self.chat_container)
        
        # Input Area
        input_area = QWidget()
        input_area.setStyleSheet("""
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f0c29, stop:1 #302b63
            );
            border-top: 1px solid #333;
            padding: 15px;
        """)
        
        input_layout = QHBoxLayout(input_area)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)
        
        # Text Input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type your message here...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #444;
                border-radius: 20px;
                padding: 10px 15px;
                color: white;
                font-size: 14px;
                selection-background-color: #00d2ff;
            }
            QLineEdit:focus {
                border: 1px solid #00d2ff;
            }
        """)
        
        # Send Button
        send_btn = QPushButton()
        send_btn.setIcon(QIcon(GraphicsDirectoryPath('send.png')))
        send_btn.setIconSize(QSize(24, 24))
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d2ff;
                border: none;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                
            }
            QPushButton:pressed {
                background-color: #009cc2;
            }
        """)
        
        # Mic Button
        self.mic_btn = QPushButton()
        self.mic_btn.setIcon(QIcon(GraphicsDirectoryPath('microphone.png')))
        self.mic_btn.setIconSize(QSize(24, 24))
        self.mic_btn.setCheckable(True)
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:checked {
                background-color: #ff4757;
            }
            QPushButton:hover {
                background-color: #00b8e0;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """)
        self.mic_btn.toggled.connect(self.toggle_mic)
        
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(send_btn)
        input_layout.addWidget(self.mic_btn)
        
        main_layout.addWidget(self.chat_area)
        main_layout.addWidget(input_area)
        
        # Timer for updating messages
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(100)  # Check for new messages every 100ms
        
    def toggle_mic(self, checked):
        if checked:
            MicButtonClosed()
            self.mic_btn.setIcon(QIcon(GraphicsDirectoryPath('mute.png')))
        else:
            MicButtonInitialed()
            self.mic_btn.setIcon(QIcon(GraphicsDirectoryPath('microphone.png')))
    
    def update_messages(self):
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                
                if messages:
                    # Split messages by line and add them to chat
                    for line in messages.split('\n'):
                        if line.strip() and line not in self.messages:
                            self.messages.append(line)
                            self.add_message(line)
                            
        except Exception as e:
            print(f"Error updating messages: {e}")
    
    def add_message(self, text):
        message_widget = QWidget()
        message_widget.setStyleSheet("background-color: transparent;")
        
        message_layout = QHBoxLayout(message_widget)
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(10)
        
        # Determine if message is from user or assistant
        if text.startswith(f"{Username} :"):
            # User message
            label = QLabel(text.replace(f"{Username} :", "").strip())
            label.setStyleSheet("""
                QLabel {
                    background-color: #00d2ff;
                    color: black;
                    border-radius: 15px;
                    padding: 10px 15px;
                    font-size: 14px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
            label.setWordWrap(True)
            label.setMaximumWidth(400)
            
            # Add spacer to push message to right
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            message_layout.addItem(spacer)
            message_layout.addWidget(label)
        else:
            # Assistant message
            label = QLabel(text.replace(f"{Assistantname} :", "").strip())
            label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    border-radius: 15px;
                    padding: 10px 15px;
                    font-size: 14px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                """)
            label.setWordWrap(True)
            label.setMaximumWidth(400)
            
            message_layout.addWidget(label)
            # Add spacer to push next message to right
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            message_layout.addItem(spacer)
        
        self.chat_layout.addWidget(message_widget)
        # Scroll to bottom after adding new message
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Gradient background
        self.setStyleSheet("""
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f0c29, stop:1 #302b63
            );
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # AI Animation
        self.ai_animation = QLabel()
        self.ai_animation.setAlignment(Qt.AlignCenter)
        
        self.movie = QMovie(GraphicsDirectoryPath('jarvis.gif'))
        self.ai_animation.setMovie(self.movie)
        self.movie.start()
        
        # Status Label
        self.status_label = QLabel("Ready to assist you")
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 18px;
                margin-top: 20px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # Mic Button
        self.mic_btn = QPushButton()
        self.mic_btn.setIcon(QIcon(GraphicsDirectoryPath('microphone.png')))
        self.mic_btn.setIconSize(QSize(60, 60))
        self.mic_btn.setCheckable(True)
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 210, 255, 0.2);
                border: 2px solid #00d2ff;
                border-radius: 40px;
                padding: 20px;
                margin: 30px;
            }
            QPushButton:checked {
                background-color: rgba(255, 71, 87, 0.2);
                border: 2px solid #ff4757;
            }
            QPushButton:hover {
                background-color: rgba(0, 210, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(0, 210, 255, 0.4);
            }
        """)
        self.mic_btn.toggled.connect(self.toggle_mic)
        
        layout.addStretch(1)
        layout.addWidget(self.ai_animation)
        layout.addWidget(self.status_label)
        layout.addWidget(self.mic_btn, 0, Qt.AlignCenter)
        layout.addStretch(1)
        
        # Timer for updating status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)
    
    def toggle_mic(self, checked):
        if checked:
            MicButtonClosed()
            self.mic_btn.setIcon(QIcon(GraphicsDirectoryPath('mute.png')))
        else:
            MicButtonInitialed()
            self.mic_btn.setIcon(QIcon(GraphicsDirectoryPath('microphone.png')))
    
    def update_status(self):
        status = GetAssistantStatus()
        if status:
            self.status_label.setText(status)

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        self.setFixedHeight(40)
        self.setStyleSheet("""
            background-color: #2e295f;
            color: white;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Title
        self.title = QLabel(f"{Assistantname} AI Assistant")
        self.title.setStyleSheet("background-color: None;font-size: 14px; font-weight: bold;")
        
        # Window controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(5)
        
        # Minimize Button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon(GraphicsDirectoryPath('minimize.png')))
        self.minimize_btn.setFixedSize(20, 20)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        
        # Maximize/Restore Button
        self.maximize_btn = QPushButton()
        self.maximize_btn.setIcon(QIcon(GraphicsDirectoryPath('maximize.png')))
        self.maximize_btn.setFixedSize(20, 20)
        self.maximize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        # Close Button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon(GraphicsDirectoryPath('close.png')))
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff4757;
                border-radius: 10px;
            }
        """)
        self.close_btn.clicked.connect(self.parent.close)
        
        controls_layout.addWidget(self.minimize_btn)
        controls_layout.addWidget(self.maximize_btn)
        controls_layout.addWidget(self.close_btn)
        
        layout.addWidget(self.title)
        layout.addStretch(1)
        layout.addWidget(controls)
        
        self.mouse_pos = None
    
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_btn.setIcon(QIcon(GraphicsDirectoryPath('maximize.png')))
        else:
            self.parent.showMaximized()
            self.maximize_btn.setIcon(QIcon(GraphicsDirectoryPath('restore.png')))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if self.mouse_pos:
            delta = QPoint(event.globalPos() - self.mouse_pos)
            self.parent.move(self.parent.pos() + delta)
            self.mouse_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        self.mouse_pos = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Window settings
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f0c29, stop:1 #302b63
            );
        """)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        
        # Create screens
        self.main_screen = MainScreen()
        self.chat_screen = ChatScreen()
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.chat_screen)
        
        # Create sidebar
        self.sidebar = SideBar(stacked_widget=self.stacked_widget)
        
        # Create title bar
        self.title_bar = TitleBar(self)
        
        # Layout for right side (title bar + content)
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        right_layout.addWidget(self.title_bar)
        right_layout.addWidget(self.stacked_widget)
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(right_side)
        
        # Set window properties
        self.setWindowTitle(f"{Assistantname} AI Assistant")
        
        # Start with main screen
        self.stacked_widget.setCurrentIndex(0)

def GraphicalUerInterFace():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create palette for dark theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(50, 50, 50))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 210, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 210, 255))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUerInterFace()