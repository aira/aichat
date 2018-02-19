import readline

from brain import Responder


class Console:
    def __init__(self):
        self.responder = Responder()
        self.states = {}
        self.commands = Verbs.verbs
        self.running = True
        self.context = {}
        self.say = print
        self.listen = input

        self.tests = {}

    def execute(self, line):
        line = line.split()
        verb = line[0]
        if verb in self._verbs:
            self._verbs[verb](self, *line[1:])
        else:
            self.print("I don't understand. To hear the kinds of things I can do, just ask 'What can you do?'.")

    def run(self):
        self._verbs['look'](self)
        while self.running:
            self.execute(self.input('> '))
        self.print('Goodbye!')
