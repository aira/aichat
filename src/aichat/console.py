import readline  # noqa

from brain import Responder


class Console:
    def __init__(self, say=print, listen=input):
        self.responder = Responder()
        self.say = say
        self.listen = listen
        self.commands = {'exit': self.quit, 'quit': self.quit}

    def quit(self):
        self.running = False

    def execute(self, utterance=''):
        words = utterance.split()
        command = words[0].lower().strip() if words and len(words) else ''
        if command in self.commands:
            self.commands[command](self, ' '.join(words[1:]))
        else:
            self.say(self.responder[utterance])

    def run(self):
        while self.running:
            self.utterance = self.listen('> ')
            self.execute(self.utterance)
        self.print('Goodbye!')
