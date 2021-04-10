#Append to a transcript file, where each index is a line of the transcript
def main():
    #Add the file name you want to put in here
    transcriptLines = []
    fname = open("filename.txt", "r")
    
    for x in fname:
        transcriptLines.append(x)

    fname.close()

    
