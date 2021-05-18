# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton, QInputDialog

from hangman import Hangman
from guess import Guess
from word import Word


class HangmanGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize word database        
        self.word = Word('words.txt')

        # Hangman display window
        self.hangmanWindow = QTextEdit()
        self.hangmanWindow.setReadOnly(True)
        self.hangmanWindow.setAlignment(Qt.AlignLeft)
        font = self.hangmanWindow.font()
        font.setFamily('Courier New')
        self.hangmanWindow.setFont(font)

        # Layout
        hangmanLayout = QGridLayout()
        hangmanLayout.addWidget(self.hangmanWindow, 0, 0)

        # Status Layout creation
        statusLayout = QGridLayout()

        # Display widget for current status
        self.currentWord = QLineEdit()
        self.currentWord.setReadOnly(True)
        self.currentWord.setAlignment(Qt.AlignCenter)
        font = self.currentWord.font()
        font.setPointSize(font.pointSize() + 8)
        self.currentWord.setFont(font)
        statusLayout.addWidget(self.currentWord, 0, 0, 1, 2)

        # Display widget for already used characters
        self.guessedChars = QLineEdit()
        self.guessedChars.setReadOnly(True)
        self.guessedChars.setAlignment(Qt.AlignLeft)
        self.guessedChars.setMaxLength(52)
        statusLayout.addWidget(self.guessedChars, 1, 0, 1, 2)

        # Display widget for message output
        self.message = QLineEdit()
        self.message.setReadOnly(True)
        self.message.setAlignment(Qt.AlignLeft)
        self.message.setMaxLength(52)
        statusLayout.addWidget(self.message, 2, 0, 1, 2)

        # Button for submitting a character
        self.guessButton = QToolButton()
        self.guessButton.setText('Guess!')
        self.guessButton.clicked.connect(self.guessClicked)
        statusLayout.addWidget(self.guessButton, 3, 1)

        # Input widget for user selected characters
        self.charInput = QLineEdit()
        self.charInput.setMaxLength(1)
        self.charInput.returnPressed.connect(self.guessButton.click)
        statusLayout.addWidget(self.charInput, 3, 0)

        # Layout placement
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(hangmanLayout, 0, 0)
        mainLayout.addLayout(statusLayout, 0, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle('Hangman Game')

        # Start a new game on application launch!
        self.startGame()

    def startGame(self):
        self.hangman = Hangman()
        self.guess = Guess(self.word.randFromDB())
        self.gameOver = False

        self.hangmanWindow.clear()
        self.hangmanWindow.setPlaceholderText(self.hangman.currentShape())
        self.currentWord.setFixedWidth(600)
        self.currentWord.setText(self.guess.displayCurrent())
        self.guessedChars.setText(self.guess.displayGuessed())
        self.message.clear()


    def guessClicked(self):
        guessedChar = self.charInput.text()
        self.charInput.clear()
        self.message.clear()

        if self.gameOver == True:
            # 메시지 출력하고 - message.setText() - 리턴
            self.message.setText('게임 진행 중이 아닙니다')
            return False

        # 입력의 길이가 1 인지를 판단하고, 아닌 경우 메시지 출력, 리턴
        if len(guessedChar) != 1:
            self.message.setText('Input a one character')
            return False

        # 이미 사용한 글자인지를 판단하고, 아닌 경우 메시지 출력, 리턴
        if guessedChar in self.guess.getGuessedChar():
            self.message.setText(guessedChar + ' is already guessed')
            return False

        success = self.guess.guess(guessedChar)
        if success == False:
            # 남아 있는 목숨을 1 만큼 감소
            self.hangman.decreaseLife()
            # 메시지 출력
            self.message.setText(guessedChar + ' is not true')

        # hangmanWindow 에 현재 hangman 상태 그림을 출력
        self.hangmanWindow.setText(self.hangman.currentShape())
        # currentWord 에 현재까지 부분적으로 맞추어진 단어 상태를 출력
        self.currentWord.setText(self.guess.displayCurrent())
        # guessedChars 에 지금까지 이용한 글자들의 집합을 출력
        self.guessedChars.setText(self.guess.displayGuessed())

        if self.guess.finished():
            # 메시지 ("Success!") 출력하고, self.gameOver 는 True 로
            self.message.setText('Success!')
            self.showWin()
            self.gameOver = False
        elif self.hangman.getRemainingLives() == 0:
            # 메시지 ("Fail!" + 비밀 단어) 출력하고, self.gameOver 는 True 로
            self.message.setText('Fail!  ' + self.guess.getSecretWord())
            self.showLose()
            self.gameOver = False

    # 이기면 더 할건지 창 띄우기
    def showWin(self):
        items = ('Yes', 'No')
        item, ok = QInputDialog.getItem(self, 'You Win! Play again?', 'Choice:', items, 0, False)
        if ok and item == 'Yes':
            self.startGame()
        else:
            QCoreApplication.instance().quit()

    # 지면 더 할건지 창 띄우기
    def showLose(self):
        items = ('Yes', 'No')
        item, ok = QInputDialog.getItem(self, 'You Lost! Play again?', 'Choice:', items, 0, False)
        if ok and item == 'Yes':
            self.startGame()
        else:
            QCoreApplication.instance().quit()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())