class Hello:

    def __init__(self, name):
        self.name = name

    def say(self):
        print('Hello %s!' % self.name)


if __name__ == '__main__':
    hello = Hello('demo my first apppppp!')
    hello.say()
