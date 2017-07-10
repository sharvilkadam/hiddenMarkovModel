import sys
import codecs
import math

def readText( file1 ):
    fo = codecs.open(file1, "r",encoding='utf8')
    text=fo.read()#.decode('utf8')
    fo.close()
    return text

def learnLine( tx , d ):
    t1=tx.split(" ")
    count=0
    while count<(len(t1)):
		#tagarray = t1[count].split("/")
		#tag = tagarray[len(tagarray)-1]
		tag = t1[count].rsplit("/",1)[1]	#get the tag
		if d.has_key(tag):
			c = d.get(tag)
			c = int(c) + 1
			d[tag] = str(c)
		else:
			d[tag] = str(1)
		count+=1

    return

def learnLine2( tx , d , atags , dw , dt):
    t1=tx.split(" ")
    count=0
    pretag="q0"
    while count<(len(t1)):
		word= t1[count].rsplit("/",1)[0]	#get the word
		tag = t1[count].rsplit("/",1)[1]	#get the tag
		
		#update word and tag dict
		if dw.has_key(word):
			wtlist = dw.get(word)
			if wtlist.has_key(tag):
				cw = wtlist.get(tag)
				cw = int(cw) + 1
				dw[word][tag] = str(cw)
			else:
				dw[word][tag] = str(1)
		else:
			dw[word] = {tag: "1"}
			
		if dt.has_key(tag):
			tc = dt.get(tag)
			tc = int(tc) + 1
			dt[tag] = tc
		else:
			dt[tag] = str(1)
		
		#update transition dict
		if not (tag in atags):
			atags.append(tag)
		if d.has_key(pretag):
			tlist = d.get(pretag)
			if tlist.has_key(tag):
				c = tlist.get(tag)
				c = int(c) + 1
				tlist[tag] = str(c)
			else:
				tlist[tag] = str(1)
		else:
			d[pretag] = {tag: "1"}
		pretag=tag
		count+=1

    return

def smoothTDict( d , atags):
	count=0
	while count<(len(atags)):
		tag=atags[count]
		
		if d['q0'].has_key(tag):
			tagc = d['q0'].get(tag)
			tagc = int(tagc) + 1
			d['q0'][tag] = tagc
		else :
			d['q0'][tag] = 1
			
		for key in d:
			if not (key == 'q0'):
				if d[key].has_key(tag):
					tagc = d[key].get(tag)
					tagc = int(tagc) + 1
					d[key][tag] = tagc
				else :
					d[key][tag] = 1
		count+=1
	return

def calct(d2):
	for key in d2:
		t = sum(d2[key].itervalues())
		for tag in d2[key]:
			v=d2[key][tag]
			v=math.log(v/float(t))
			d2[key][tag]=v

	return


def writeModel2( d2, dw ,dt ):
    writeout = "Transition Dictionary: " + "\n"  + str(d2) + "\n" + "Word Dictionary: " + "\n" + str(dw) + "\n" +"Tag Dictionary: " + "\n" + str(dt) + "\n"
    wo = codecs.open("hmmmodel.txt",'w',encoding="utf8")
    #writeout =  codecs.encode(writeout,"utf8")
    wo.write(writeout)
    wo.close()
    return

def visualString ( d , plist , prior , count ):
    modelop = "Prior Probabilities [ Truthful , Deceptive , Positive , Negative ]\n"
    modelop += str(prior[0])+"/"+str(count) +" "+ str(prior[1])+"/"+str(count)+" " +str(prior[2])+"/"+str(count) +" "+str(prior[3])+"/"+str(count) + "\n"
    modelop += "\n"
    modelop += "Feature:\tTruthful Deceptive Positive Negative\n"

    for key , value in d.iteritems():
        vlist=value.split(",")
        modelop += "\n"+key+":\t"+vlist[0]+"/"+str(plist[0])+" "+vlist[1]+"/"+str(plist[1])+" "+vlist[2]+"/"+str(plist[2])+" "+vlist[3]+"/"+str(plist[3])
    return modelop



file1 = str(sys.argv[1]) #train data
text = readText(file1)

t2=text.split("\n")     #t2 contains all the training data

#print t2[0]
#d={}         #dict will have the key
#print "Befoer: " + str(d)
#learnLine(t2[0],d)

#count=0
#while count<(len(t2)-1):
#    learnLine(t2[count], d)
#    count+=1
	
#print "After: " + str(d)
#print "Length: " + str(len(d))

d2={}			#transition dictionaary
atags=[] 		#list of all the tags to be used later for smoothening
dw={}  			#word dictionaary.. p(word given tag) {"word":{"NC":1},{"VB":3}}
dt={}			#tag dictionaary.. P(tag) {"NC":22314}
#print "Befoer: " + str(d2)
#print t2[118]
#learnLine2(t2[118],d2, atags)
count=0
while count<(len(t2)-1):
    learnLine2(t2[count], d2 ,atags, dw, dt)
    count+=1
#print "After: " + str(d2)
#print "Atags: " + str(atags) + "Lenght of atags: " + str(len(atags))

smoothTDict(d2,atags)
#print "After Trans Dict: " + str(d2)
#print "After Word Dict: " + str(dw)
#print "After Tag Dict: " + str(dt)
#writeModel( str(d) )
calct(d2)
writeModel2( d2 , dw , dt)
