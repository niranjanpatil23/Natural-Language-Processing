f = open('hmmoutput.txt', 'r')
lines = f.readlines()
f.close()

f = open('catalan_corpus_dev_tagged.txt', 'r')
lines1 = f.readlines()
f.close()
total = 0
eq = 0
cnt = 0
k=0
sum = 0
for i in range(0,len(lines1)):

    words = lines[i].split()
    words1 = lines1[i].split()
    flag = 0
    k=0

    for j in range(0,len(words1)):
        total +=1
        if(words[j] == words1[j]):
            eq += 1
        else:
            flag =1
            cnt += 1
            k += 1
            print words[j],words1[j]
        if j == (len(words) - 1):
            if flag == 1:
                sum += 1
                print (i+1), k
                print

print "\n"
print sum

print eq
print cnt
print total
print (eq*1.0)/total