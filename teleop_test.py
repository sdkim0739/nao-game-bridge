import qi

class gameSession:
    "A sample standalone app, that demonstrates simple Python usage"
    def __init__(self, qiapp):
        self.qiapp = qiapp
        self.session = qiapp.session

    def on_start(self):
        try:
            self.session.service("ALTextToSpeech").say("Hello everybody! check out my eyes")
            self.session.service("ALLeds").rasta(2.0)
            self.session.service("ALTextToSpeech").say("Neat wasn't it?")
        finally:
            # Note, until we do this, this will run forever (which is sometimes what we want)
            return 1
            # self.stop()

    def run_utterance(self, msg):
        try:
            self.session.service("ALTextToSpeech").say(str(msg))
            print("Success")
        finally:
            # Note, until we do this, this will run forever (which is sometimes what we want)
            return 1
            # self.stop()

    def stop(self):
        "Standard way of stopping the application."
        self.qiapp.stop()

if __name__ == "__main__":
    qiapp = qi.Application()
    qiapp.start()
    gameSession = gameSession(qiapp)
    qi.runAsync(gameSession.on_start)
    qiapp.run()