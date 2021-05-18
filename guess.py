import unittest

class Guess:

    def __init__(self, word):
        self.secretWord = word
        self.currentStatus = '_' * len(word)
        self.guessedChars = {'e', 'n'}
        self.guess(' ')

    def guess(self, character):
        self.guessedChars |= {character}
        if character not in self.secretWord:
            return False
        else:
            currentStatus = ''
            matches = 0
            for c in self.secretWord:
                if c in self.guessedChars:
                    currentStatus += c
                else:
                    currentStatus += '_'

            self.currentStatus = currentStatus

            return True


    def finished(self):
        if self.currentStatus == self.secretWord:
            return True
        else:
            return False


    def displayCurrent(self):
        guessWord = ''
        for c in self.currentStatus:
            guessWord += (c + ' ')
        return guessWord


    def displayGuessed(self):
        guessed = ''
        for c in sorted(list(self.guessedChars)):
            guessed += (c + ' ')
        return guessed

    def getGuessedChar(self):
        return self.guessedChars

    def getSecretWord(self):
        return self.secretWord

class TestGuess(unittest.TestCase):

    def setUp(self):
        self.p1 = Guess('gleeful')

    def testconstructor(self):
        self.assertEqual(self.p1.secretWord, 'gleeful')
        self.assertEqual(self.p1.displayCurrent(), '_ _ _ _ _ _ _ ')
        self.assertEqual(self.p1.displayGuessed(), '  e n ')

    def testDisplayCurrent(self):
        self.assertEqual(self.p1.displayCurrent(), '_ _ _ _ _ _ _ ')
        self.p1.guess('e')
        self.assertEqual(self.p1.displayCurrent(), '_ _ e e _ _ _ ')
        self.p1.guess('g')
        self.assertEqual(self.p1.displayCurrent(), 'g _ e e _ _ _ ')
        self.p1.guess('l')
        self.assertEqual(self.p1.displayCurrent(), 'g l e e _ _ l ')

    def testDisplayGuessed(self):
        self.assertEqual(self.p1.displayGuessed(), '  e n ')
        self.p1.guess('a')
        self.assertEqual(self.p1.displayGuessed(), '  a e n ')
        self.p1.guess('b')
        self.assertEqual(self.p1.displayGuessed(), '  a b e n ')
        self.p1.guess('c')
        self.assertEqual(self.p1.displayGuessed(), '  a b c e n ')

    def testGetGuessedChar(self):
        self.assertEqual(self.p1.displayGuessed(), '  e n ')
        self.p1.guess('a')
        self.assertEqual(self.p1.displayGuessed(), '  a e n ')
        self.p1.guess('b')
        self.assertEqual(self.p1.displayGuessed(), '  a b e n ')
        self.p1.guess('c')
        self.assertEqual(self.p1.displayGuessed(), '  a b c e n ')

    def testGetSecretWord(self):
        pass

    def testGuess(self):
        self.assertTrue(self.p1.guess('g'))
        self.assertTrue(self.p1.guess('e'))
        self.assertFalse(self.p1.guess('a'))
        self.assertFalse(self.p1.guess('b'))

    def testFin(self):
        self.p1.guess('g')
        self.assertFalse(self.p1.finished())
        self.p1.guess('l')
        self.assertFalse(self.p1.finished())
        self.p1.guess('e')
        self.assertFalse(self.p1.finished())
        self.p1.guess('f')
        self.assertFalse(self.p1.finished())
        self.p1.guess('u')
        self.assertTrue(self.p1.finished())


if __name__ == "__main__":
    unittest.main()