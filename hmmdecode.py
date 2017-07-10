import sys
import codecs
import ast
import math

def readText( file1 ):
    #fo = open(file1, "r")
    fo = codecs.open(file1, "r",encoding='utf8')
    text=fo.read()#.decode('utf-8')
    fo.close()
    return text

def writeOutput( str ):
    #wo = open("hmmoutput.txt","w")
    wo = codecs.open("hmmoutput.txt",'w',encoding="utf8")
    wo.write(str)
    wo.close()
    return

def tagLine( line  , d2 , dw , dt ,dlis):
    words = line.split(" ")
    lenght = len(words)
    back = {"q0,t0":""}
    prob1 = {}
    prob2 = {}
    prob3 = {}
    c=1
    
    #print tq0
    for tag in dlis:
        back[tag+",l"+str(c)]="q0,t0"
        prob1[tag]=d2["q0"][tag]
        if dw.has_key(words[0]):
            if dw[words[0]].has_key(tag):
                prob1[tag]=d2["q0"][tag]+math.log(int(dw[words[0]][tag])/float(dt[tag]))
                #print "in has key"
            else: 
                prob1[tag]=float("-infinity")

    #print "back: " + str(back)
    #print "prob1: " + str(prob1)


    #iterative next steps untill the end of line
    for i in range(1,lenght):
        for tag in dlis:
            #print tag
            if (dw.has_key(words[i])) and (not dw[words[i]].has_key(tag)):
                    prob2[tag]=float("-infinity")
            else:
                for it in prob1:
                    #back[tag+",l"+str(i+1)]=""
                    prob3[it]=prob1[it]+d2[it][tag]
                    if dw.has_key(words[i]):
                        if dw[words[i]].has_key(tag):
                            prob3[it]= prob3[it] + math.log(int(dw[words[i]][tag])/float(dt[tag]))
                            #print "in has key"
                        else: 
                            prob3[it]=float("-infinity")
                    
                maxv=float("-infinity")
                for k,v in prob3.iteritems():
                    if maxv<=v:
                        maxk=k
                        maxv=v
                backtag=maxk
                prob2[tag]=maxv
                back[tag+",l"+str(i+1)]=backtag+",l"+str(i)
                #print "prob2: "+ str(prob2)
        prob1=prob2.copy()
        #print "prob2:" +str(prob1)
    finalv=float("-infinity")
    for k,v in prob1.iteritems():
        if finalv<=v:
            finalk=k
            finalv=v
            #print str(k)+","+str(v)
    finaltag=finalk
    #print "\n New back: "+ str(back)
    #print "Final Tag: "+ finaltag
    taglist=[finaltag]
    last=finaltag+",l"+str(lenght)
    #print "old taglist : " +str(taglist)
    while 1:
        new=back[last]
        if new=="q0,t0":
            break
        taglist.append(new.split(',')[0])
        last=new
        
    taglist=taglist[::-1]
    #print "Taglist: " + str(taglist[::-1])
    op=""
    coun=0
    for w in words:
        op=op+w+"/"+taglist[coun]+" "
        coun+=1
    op=op.rstrip()
    return op


file1 = str(sys.argv[1]) #file path to test.txt
file2 = "hmmmodel.txt"
text = readText(file1)
model = readText(file2)
t2 = text.split("\n")     #t2 contains all the test lines
m2 = model.split("\n")      #m2 contains all the lines on the model.txt

#print m2[3]
d2 = ast.literal_eval(m2[1])
dw = ast.literal_eval(m2[3])
dt = ast.literal_eval(m2[5])

#print t2[14]
#print dw
dlis=dt.keys()
dlis.sort()

#print tagLine(t2[14],d2,dw,dt)
outputStr = ""
count = 0
while count<len(t2):
    if t2[count]!="":
        o = tagLine(t2[count],d2,dw,dt,dlis)
        outputStr += o
        if count != (len(t2)-1):
            outputStr += "\n"
    count+=1
#print outputStr
writeOutput(outputStr)
