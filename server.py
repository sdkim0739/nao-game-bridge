#!/usr/bin/env python3
# Python3 WebSocket server
import qi
import asyncio
from websockets.server import serve
import json

class gameSession:
    "A sample standalone app, that demonstrates simple Python usage"
    def __init__(self, qiapp, condition):
        self.qiapp = qiapp
        self.session = qiapp.session
        self.condition = condition

        # writing topics' qichat code as text strings (end-of-line characters are important!)
        self.feedback_round_1 = ('topic: ~feedback_round_1()\n'
                        'language: enu\n'
                        'proposal: What do you think of my play?\n'
                        'u:(e:Dialog/NotSpeaking10) Thank you for your feedback.\n')
        
        self.feedback_round_5 = ('topic: ~feedback_round_5()\n'
                        'language: enu\n'
                        'proposal: How would you describe my performance in the game?\n'
                        'u:(e:Dialog/NotSpeaking10) Thank you for your feedback.\n')
        
        self.feedback_round_10 = ('topic: ~feedback_round_10()\n'
                        'language: enu\n'
                        'proposal: What are your final thoughts throughout the game?\n'
                        'u:(e:Dialog/NotSpeaking10) Thank you for your feedback.\n')

    def on_start(self):
        try:
            self.session.service("ALTextToSpeech").say("Hi, I'm NAO! \\pau=500\\ I'm the AI teammate. \\pau=500\\ I'm looking forward to playing this game with you.")

            if self.condition == "1":
                self.session.service("ALTextToSpeech").say("During this game, my decisions are remotely  controlled by a human operator.")
            elif self.condition == "2":
                self.session.service("ALTextToSpeech").say("During this game, my decisions are occasionally controlled by a human operator.")
            elif self.condition == "3":
                self.session.service("ALTextToSpeech").say("During this game, I  independently make my own decisions.")
            else:
                self.session.service("ALTextToSpeech").say("Error: condition not recognized")
        finally:
            # Note, until we do this, this will run forever (which is sometimes what we want)
            return 1
            # self.stop()

    def run_utterance(self, msg):
        try:
            self.session.service("ALTextToSpeech").say(str(msg))
            print(msg)
        finally:
            # Note, until we do this, this will run forever (which is sometimes what we want)
            # self.stop()
            return "Success"
        
    def performance_feedback(self, roundNum):
        # Getting the service ALDialog
        ALDialog = self.session.service("ALDialog")
        ALDialog.setLanguage("English")
        ALDialog.subscribe("feedback")

        # Loading the topics directly as text strings
        feedback_topic_1 = ALDialog.loadTopicContent(self.feedback_round_1)
        feedback_topic_5 = ALDialog.loadTopicContent(self.feedback_round_5)
        feedback_topic_10 = ALDialog.loadTopicContent(self.feedback_round_10)

        # Activating the loaded topics
        ALDialog.activateTopic(feedback_topic_1)
        ALDialog.activateTopic(feedback_topic_5)
        ALDialog.activateTopic(feedback_topic_10)

        # Subscribing to all topics
        ALDialog.subscribe('feedback_topics')
        try:
            if roundNum == 1:
                ALDialog.setFocus("feedback_round_1")
                ALDialog.forceOutput()
            elif roundNum == 5:
                ALDialog.setFocus("feedback_round_5")
                ALDialog.forceOutput()
            elif roundNum == 10:
                ALDialog.setFocus("feedback_round_10")
                ALDialog.forceOutput()

            input("\nSpeak to the robot using rules from both the activated topics. Press Enter when finished:")
        finally:
            # stopping the dialog engine
            ALDialog.unsubscribe('feedback_topics')

            # Deactivating all topics
            ALDialog.deactivateTopic(feedback_topic_1)
            ALDialog.deactivateTopic(feedback_topic_5)
            ALDialog.deactivateTopic(feedback_topic_10)

            # now that the dialog engine is stopped and there are no more activated topics,
            # we can unload all topics and free the associated memory
            ALDialog.unloadTopic(feedback_topic_1)
            ALDialog.unloadTopic(feedback_topic_5)
            ALDialog.unloadTopic(feedback_topic_10)

    def stop(self):
        "Standard way of stopping the application."
        self.qiapp.stop()

async def echo(websocket):
    async for message in websocket:
        event = json.loads(message)
        msg = event["message"]
        roundNum = event["round"]
        return_msg = gameSession.run_utterance(message)
        await websocket.send(str(return_msg)) # gameSession.run_utterance(message)

async def main():
    async with serve(echo, "127.0.0.1", 8080):
        await asyncio.Future()  # run forever 

if __name__ == "__main__":
    qiapp = qi.Application(url="tcp://10.137.14.52:9559")
    qiapp.start()
    gameSession = gameSession(qiapp, 1)
    qi.runAsync(gameSession.on_start)
    qiapp.run()
    asyncio.run(main())
