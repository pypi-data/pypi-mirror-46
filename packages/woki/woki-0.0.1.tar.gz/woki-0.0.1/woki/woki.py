import wikipedia
import os,re
def find(query):
    summary1= wikipedia.summary(query, sentences=2) #it brings summary about anything from wikipedia in 2 sentences
    summary1= re.sub(r'\([^)]*\)',"",summary1)#it will replace brackets and special symbols from that summary
    return summary1

