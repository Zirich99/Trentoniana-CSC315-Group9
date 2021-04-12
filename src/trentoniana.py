#File imports
from playsound import playsound

#Append to a transcript file, where each index is a line of the transcript
def addTranscript(transcriptFileName):
    #Add the file name you want to put in here
    transcriptLines = []
    fname = open(transcriptFileName, "r")
    
    for x in fname:
        transcriptLines.append(x)

    fname.close()

    #Join the lines of the file together
    fullTranscript = ""
    fullTranscript = fullTranscript.join(transcriptLines)

    print(fullTranscript)

    return fullTranscript

#Testing function for playing an audiofile
def playAudioFile(audioFileName):
    playsound(audioFileName)


#Main method used for importing files

#Base variables for taking input
userSelection = " "
transcriptFileName = " "
audioFileName = " "

while userSelection != "exit":
    #Ask the user which choice they would like to make.
    print("Please select one of the following options:")
    print("1. Add a transcript")
    print("2. Play an audio file")
    print("3. Exit the file addition software")
    userSelection = input("Select one of the above numbers.")

    if userSelection == "1":
        transcriptFileName = input("Please provide a filename, in .txt format, for input.")
        addTranscript(transcriptFileName)   
    if userSelection == "2":
        audioFileName = input("Please provide a filename, in .mp3, for input.")
        playAudioFile(audioFileName)
    if userSelection == "3":
        print("Exiting file addition software...")
        exit()
    