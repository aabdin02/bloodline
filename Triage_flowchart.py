TriageIntroduction = "Hello World. My name is Bloodline. I am here to help you get the First Aid you need and give you the information you need to provide care for other humans. "
Rule = " This process will ask you series of questions with a yes or no response. These questions will guide me to find you the best possible solution to the care you need."

walkingQuestion = "Are you able to move from one location to another?"
walkingAnswer = "Are you able to provide First Aid for someone else within your vicinity?"

breathing1 = "Please check if the victim is not breathing."
breathing2 = "Open their airway to see of they start breathing."
breathingQuestion = "Is this person breathing?"

breathingRate1 = "Count the breathing rate per minute."
breathingRateQuestion = "Was the breathing rate more than 30 times per minute?"

bleeding1 = "Press the victim finger to see how fast blood refills, and check blood refills more than two seconds."
bleedingQuestion = "Did blood refill more than two seconds?"

shocking1 = "Get victim to follow simple commands. For example, can you give me your hand?."
shockingQuestion = "Did the person obey your simple command?"

valid_answers = set(["YES", "NO", "REPEAT", "GO BACK"])
invalid_answers = 'Please say valid answers. You can say Yes, No, Repeat or Go back'

Results = {
'Green' : 'Minor, Green Tag. This victim is with relatively minor injuries. The status unlikely to deteriorate over days. The victim may be able to assist in own care.',
'Yellow' : 'Delayed, Yellow Tag. This victim\'s transport can be delayed. The status includes serious and potentially life-threatening injuries, but status not expected to deteriorate significantly over several hours.',
'Red' : 'Immediate, Red Tag. This victim needs immediate intervention and transport requires medical attention within minutes for survival.',
'Black' : 'Expectant, Black Tag. This victim is unlikely to survive given severity of injuries, level of available care, or both palliative care and pain relief should be provided.'
}

from time import sleep

from textToSpeech import *
from speechToText import *



lock = threading.Lock()

def textToSpeech(str):
    # if not lock.acquire(False): print 'false'
    lock.acquire()

    text_to_speech.synthesize_using_websocket(str,
                                      test_callback,
                                      accept='audio/wav',
                                      voice="en-US_AllisonVoice"
                                     )
    lock.release()
    
class TriageNode:
    def __init__(self, instruction, question, yesResult, noResult):
        self.triageI = instruction
        self.triageQ = question
        self.yesResult = yesResult
        self.noResult = noResult
        self.next = None
        self.back = None

    def getInstruction(self):
        print(self.triageI)
        textToSpeech(self.triageI)
        return(self.triageI)

    def getAnswers(self):
        print(self.triageQ)
        textToSpeech(self.triageQ)
        sleep(5)
        if messageS:
            return messageS.pop()
        # return raw_input()

def intro():
    print(TriageIntroduction)
    print(Rule)
    textToSpeech(TriageIntroduction + Rule)

# this function will initiate the recognize service and pass in the AudioSource
def recognize_using_weboscket(*args):
    with lock:
        mycallback = MyRecognizeCallback()
        speech_to_text.recognize_using_websocket(audio=audio_source,
                                                 content_type='audio/l16; rate=44100',
                                                 recognize_callback=mycallback,
                                                 interim_results=True)

def TriageWorker():

    # intro()

    walking = TriageNode(TriageIntroduction + "" + Rule, walkingQuestion, walkingAnswer, "Next")
    breathing = TriageNode(breathing1 + " " + breathing2, breathingQuestion, "Next", "Black")
    breathRate = TriageNode(breathingRate1, breathingRateQuestion, "Red", "Next")
    bleeding = TriageNode(bleeding1, bleedingQuestion, "Red", "Next")
    shocking = TriageNode(shocking1, shockingQuestion, "Yellow", "Red")

    walking.back = None
    walking.next = breathing

    breathing.back = walking
    breathing.next = breathRate

    breathRate.back = breathing
    breathRate.next = bleeding

    bleeding.back = breathRate
    bleeding.next = shocking

    shocking.back = bleeding
    shocking.next = None

    triage = walking

    while True:
        triage.getInstruction()
        answer = triage.getAnswers()
       # if answer:
        #    answer = answer.upper()

        while answer not in valid_answers:
            print(invalid_answers + " Invalid Answer")
            # textToSpeech(invalid_answers)
            answer = triage.getAnswers()
            #if answer: answer = answer.upper()

        nextAction = None
        if answer == "yes": nextAction = triage.yesResult
        elif answer == "no": nextAction = triage.noResult
        elif answer == "repeat": continue
        elif answer == "go back":
            triage = triage.back
            continue
        print(answer)
        print(nextAction)
        if nextAction in Results:
            print(Results[nextAction])
            textToSpeech(Results[nextAction])
            return
        if nextAction is "Next": triage = triage.next

#########################################################################
#### Start the recording and start service to recognize the stream ######
#########################################################################
def main():
    print("Enter CTRL+C to end recording...")
    stream.start_stream()

    try:
        triage_thread = threading.Thread(target=TriageWorker, args=())
        recognize_thread = threading.Thread(target=recognize_using_weboscket, args=())
        triage_thread.start()
        recognize_thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        # stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_source.completed_recording()

if __name__== "__main__":
  main()
