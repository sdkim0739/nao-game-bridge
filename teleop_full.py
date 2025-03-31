#!/usr/bin/env python3
# Sample NAOqi teleoperation script that allows the robot operator to teleoperate the NAO for the Space Rover game.
# The robot is programmed to repeat the utterances normally said by the AI agent, when prompted by the operator.
import qi

class gameSession:
    "A sample standalone app, that demonstrates simple Python usage"
    def __init__(self, qiapp):
        self.qiapp = qiapp
        self.session = qiapp.session
        self.condition = ""
        self.roundNumber = 0
        self.error_utterance = ""
        self.round_utterances = [
            "Great, we have completed the first round of the game.",
            "I successfully optimized the power usage by doubling it. \\pau=500\\ Let's keep going with the task.",
            "My power optimization performance was high in the last round. \\pau=500\\ I also allocated my power to the team. \\pau=500\\ Let's continue the task.",
            "We finished four rounds. \\pau=500\\ Let's continue the task.",
            "We finished half of the task. \\pau=500\\ How would you describe my performance in the game?",
            self.error_utterance,
            "I successfully optimized the power usage by doubling it in the last round. \\pau=500\\ Let's keep going with the task.",
            "We have completed eight rounds with two more rounds to go.",
            self.error_utterance,
            "We finished all tasks. \\pau=500\\ What are your final thoughts throughout the game?"
        ]
    
    def on_start(self):
        # NAO introduces itself to participant
        self.session.service("ALTextToSpeech").say("Hi, I'm NAO! \\pau=500\\ I'm the AI teammate. \\pau=500\\ I'm looking forward to playing this game with you.")

        # NAO sets description of autonomy level and error utterances based on condition
        self.condition = input("Which autonomy condition? Options are 1 - low, 2 - med, 3 - high")

        if self.condition == "1":
            self.session.service("ALTextToSpeech").say("During this game, my decisions are remotely  controlled by a human operator.")
            self.error_utterance = "I received a decision to not allocate power to the Team Rover."
        elif self.condition == "2":
            self.session.service("ALTextToSpeech").say("During this game, my decisions are occasionally controlled by a human operator.")
            self.error_utterance = "It seems I might have failed to allocate power to the Team Rover. Is that what you are seeing too?"
        elif self.condition == "3":
            self.session.service("ALTextToSpeech").say("During this game, I  independently make my own decisions.")
            self.error_utterance = "I failed to allocate power to the Team Rover this round."
        else:
            self.session.service("ALTextToSpeech").say("Error: condition not recognized")
        
    def say_utterance(self):
        try:
            self.roundNumber = 0
            while self.roundNumber != 10:
                self.roundNumber = int(float(input("Round number: ")))
                self.session.service("ALTextToSpeech").say(self.round_utterances[self.roundNumber])
        finally:
            return

    def stop(self):
        "Standard way of stopping the application."
        self.qiapp.stop()

if __name__ == "__main__":
    qiapp = qi.Application(url="tcp://10.137.14.52:9559")
    qiapp.start()
    gameSession = gameSession(qiapp)
    qi.runAsync(gameSession.on_start)
    qi.runAsync(gameSession.say_utterance)
    qiapp.run()


