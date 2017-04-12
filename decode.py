timport sys,json,operator
from math import log10

reload(sys)
sys.setdefaultencoding('utf8')

f = open("hmmmodel.txt","r")
json_obj = json.load(f)

transition = json_obj["Transition"]
emission = json_obj["Emission"]
tagcount = json_obj["Tag_Count"]

#print transition
#print emission
#print tagc

f = open(sys.argv[1],"r")
lines  = f.readlines()
f.close()

maxval = -(sys.maxint) - 1
transval = 0
prevword = 'q0'
stateno = 0
prob = {}
backpt = {}
f = open('hmmoutput.txt', 'w+')
count = 0
for line in lines:
    #line = line.lower()
    count += 1
    words = line.split()
    stateno = 0
    prevword = 'q0'
    prob = {}
    backpt = {}
    for word in words:

        if word not in emission:
            for tags in tagcount:
                maxval = -(sys.maxint) - 1
                transval = 0
                if prevword != 'q0':
                    if prevword not in emission:
                        prevtaglist = tagcount.keys()
                    else:
                        prevtaglist = emission[prevword]
                    for ptag in prevtaglist:
                        transval = prob[stateno - 1][ptag] + log10(transition[ptag][tags])
                        if maxval < transval:
                            maxval = transval
                            if stateno not in prob:
                                prob[stateno] = {}
                                prob[stateno][tags] = transval
                            else:
                                prob[stateno][tags] = transval
                            if stateno not in backpt:
                                backpt[stateno] = {}
                                backpt[stateno][tags] = ptag
                            else:
                                backpt[stateno][tags] = ptag
                else:
                    transval = log10(transition['q0'][tags])
                    if stateno not in prob:
                        prob[stateno] = {}
                        prob[stateno][tags] = transval
                    else:
                        prob[stateno][tags] = transval
                    if stateno not in backpt:
                        backpt[stateno] = {}
                        backpt[stateno][tags] = 'q0'
                    else:
                        backpt[stateno][tags] = 'q0'
        else:
            for tag in emission[word]:
                maxval = -(sys.maxint) - 1
                transval = -(sys.maxint) - 1
                if prevword != 'q0':
                    if prevword not in emission:
                        prevtaglist = tagcount.keys()

                    else:
                        prevtaglist = emission[prevword]
                    for ptag in prevtaglist:
                        transval = prob[stateno - 1][ptag] + log10(emission[word][tag]) + log10(transition[ptag][tag])

                        if maxval < transval:
                            maxval = transval
                            if stateno not in prob:
                                prob[stateno] = {}
                                prob[stateno][tag] = transval
                            else:
                                prob[stateno][tag] = transval
                            if stateno not in backpt:
                                backpt[stateno] = {}
                                backpt[stateno][tag] = ptag
                            else:
                                backpt[stateno][tag] = ptag
                else:
                    transval = log10(transition['q0'][tag] * emission[word][tag])
                    if stateno not in prob:
                        prob[stateno] = {}
                        prob[stateno][tag] = transval
                    else:
                        prob[stateno][tag] = transval
                    if stateno not in backpt:
                        backpt[stateno] = {}
                        backpt[stateno][tag] = 'q0'
                    else:
                        backpt[stateno][tag] = 'q0'

        stateno += 1
        prevword = word

    #print prob
    #print backpt

    str = ''
    stats = prob[stateno - 1]

    s = max(stats.iteritems(), key=operator.itemgetter(1))[0]

    #print words[stateno - 1]
    #print s
    str = words[stateno - 1] + "/" + s

    try:
        for i in range(len(words) - 2, -1, -1):
            s = backpt[i + 1][s]
            str += " " + words[i] + "/" + s
    except:
        # str = ' '.join(reversed(str.split()))
        # print count
        pass
    str = ' '.join(reversed(str.split()))
    f.write(str + '\n')
f.close()


