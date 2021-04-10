#Append to a transcript file, where each index is a line of the transcript
def addTranscript():
    #Add the file name you want to put in here
    transcriptLines = []
    fname = open("filename.txt", "r")
    
    for x in fname:
        transcriptLines.append(x)

    fname.close()

    #Join the lines of the file together
    fullTranscript = ""
    fullTranscript.join(transcriptLines)

    return fullTranscript


addTranscript()
