import cx_Oracle
import sys
import operator


def main():
    a = 0
    a = input('1. Find Average and Stand Deviation for Review length\
and percent of reviews above/below number inputed number\n\
2. Find Average Stars for Users that give lengthier/shorter Reviews \n\
3. Find Average Star Difference between Business averages\
and Longer/Shorter review stars \n\
4. Words in text analysis \n\
5. predictor \n\
Input: ')
    if a == 1:
        n = input('Review Length: ')
        m = input('1 for below and 2 for above: ')
        revlength(n,m)
    elif a == 2:
        averagestars()
    elif a == 3:
        n = input('Longer Review #: ')
        m = input('Shorter Review #: ')
        business(n,m)
    elif a == 4:
        n = input('option string, stars, both')
        if n == 'string':
            a = input('enter string: ')
            words(a)
        elif n == 'stars':
            a = input('enter number as string :')
            words1(a)
        elif n == 'both':
            a= input('enter number as string :')
            b= input('enter string: ')
            words2(a,b)
        else:
            main()
    elif a == 5:
        a = input('enter a string: ')
        legit(a)
    else:
        print "Invalid input. Try again."
        main()
    
              
              
def revlength(n,m):
    con = cx_Oracle.connect('yp','yp','xe')
    cur = con.cursor()
    cur.execute('select text from reviews11')
    reviews = cur.fetchall()
    reviewslist = []
    cur.close()
    con.close()
    revavg = 0
    z = []
    x = 0
    stdstep = 0
    std = 0
    mean = 0
    cntr= 0
    for i in range(0,len(reviews)):
        z.append(list(reviews[i]))
        cntr = cntr + 1
    for i in range(0,len(reviews)):
        if z[i][0] != None:
            x= float(x) + float(len(z[i][0].split()))
            cntr = cntr + 1
        else:
            x = float(x) + float(0)
    mean = x/cntr


    for i in range(0,len(reviews)):
        if z[i][0] != None:
            stdstep = float(stdstep) + float((float(len(z[i][0].split()))-float(mean))**2)
    std =  float(float((stdstep/cntr))**.5)     
      
    zztop = 0
    for i in range(0,len(reviews)):
        if z[i][0] != None and m == 1:
            if len(z[i][0].split()) <= n:
                zztop = float(zztop) + 1
        elif z[i][0] != None and m == 2:
            if len(z[i][0].split()) >= n:
                zztop = float(zztop) + 1      
    print ['mean =', mean,'std = ',std,'% =', zztop/cntr*100]
    print
    main()
def averagestars():
    con = cx_Oracle.connect('yp','yp','xe')
    cur = con.cursor()
    cur.execute('select user_id, text from reviews11')
    data = cur.fetchall()
    cur.close()
    cur = con.cursor()
    cur.execute('select distinct user_id, average_stars, review_count from users_reviews11')
    distinctusers = cur.fetchall()
    cur.close()
    con.close()
    reviewnumber = 0
    for i in range(0,len(data)):
        reviewnumber = reviewnumber + 1
    users = []
    for i in range(0,len(distinctusers)):
        users.append((distinctusers[i][0],float(distinctusers[i][1]),float(distinctusers[i][2]),float(0)))
    for i in range(0,len(users)):
        users[i] = list(users[i])
    userslower = []
    for i in range(0,len(distinctusers)):
        userslower.append((distinctusers[i][0],float(distinctusers[i][1]),float(distinctusers[i][2]),float(0)))
    for i in range(0,len(users)):
        userslower[i] = list(userslower[i])

    for i in range(0,len(data)):
        if len(data[i][1].split()) > 201:
            for j in range(0,len(distinctusers)):
                if data[i][0] == distinctusers[j][0]:
                    users[j][3] += 1
    for i in range(0,len(data)):
        if len(data[i][1].split()) <= 35:
            for j in range(0,len(distinctusers)):
                if data[i][0] == distinctusers[j][0]:
                    userslower[j][3] += 1                
    endgame = []
    sum = 0
    lowergame = []
    lowersum = 0
    for i in range(0,len(users)):
        if float(users[i][2]/users[i][1]) >= .5:
            endgame.append(users[i][1])
          
    for i in range(0,len(users)):
        if float(userslower[i][2]/userslower[i][1]) <= .5:
            lowergame.append(userslower[i][1])
    for i in range(0,len(endgame)):
        sum = sum + endgame[i]
       
    for i in range(0,len(lowergame)):
        lowersum = lowersum + lowergame[i]
    if(len(endgame)==0):
        endgame = " "
    lengthystars = float(sum/len(endgame))
    if(len(lowergame)==0):
        lowergame = " "
    shorterstars = float(lowersum/len(lowergame))
    print 'longer reviews:', lengthystars
    print 'shorter reviews:', shorterstars
    print
    main()
    
def business(n,m):
    con = cx_Oracle.connect('yp','yp','xe')
    cur = con.cursor()
    cur.execute('select business1_id, text,stars, stars_b  from business_review11')
    data = cur.fetchall()
    cur.close()
    con.close()
    z=[]
    x=[]
    scorelong = 0
    scoreshort = 0


    for i in range(0,len(data)):
        if len(data[i][1]) >= n:
            z.append(list(data[i]))
        elif len(data[i][1]) <= m:
            x.append(list(data[i]))         
    for i in range(0,len(z)):
        scorelong += float(z[i][3]) - float(z[i][2])
        

    for i in range(0,len(x)):
        scoreshort += float(x[i][3]) - float(x[i][2])
    if(len(z) == 0):
        z = " "
    if(len(x) == 0):
        x = " "
    print float(scorelong/len(z))
    print float(scoreshort/len(x))
    print ""
    main()
        

def words(a):
    con = cx_Oracle.connect('yp','yp','xe')
    cur = con.cursor()
    cur.execute('select text, stars from reviews11')
    ##cur.execute('select text, stars from reviews123456')
    data = cur.fetchall()
    cur.close()
    con.close()
    z= 0
    d = {}
    data1 = []

    totalwords = 0
        


    for i in range(0,len(data)):
        z = 0
        z = data[i][0].split()
        for j in range(0,len(z)):
            if z[j] in d:
                d[z[j]] = d[z[j]] + 1
            else:
                d[z[j]] = 1
    totalwords= float(sum(d.values()))
    newdict = {}
    nd= {}

    if a in d:
        print d.get(a)
    print    
    main()    

         
def words1(a):
    con = cx_Oracle.connect('yp','yp','xe')
    cur = con.cursor()
    cur.prepare('select text, stars from reviews11 where stars = :b')
    cur.execute(None, {'b': a})
    ##cur.execute('select text, stars from reviews123456')
    data = cur.fetchall()
    cur.close()
    con.close()
    z= 0
    d = {}
    data1 = []

    totalwords = 0
        


    for i in range(0,len(data)):
        z = 0
        z = data[i][0].split()
        for j in range(0,len(z)):
            if z[j] in d:
                d[z[j]] = d[z[j]] + 1
            else:
                d[z[j]] = 1
    totalwords= float(sum(d.values()))
    newdict = {}
    nd= {}

    newdict = dict(sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:20])
    print newdict
    print
    main()

def words2(a,b):
    con = cx_Oracle.connect('yp','yp','xe')
    cur = con.cursor()
    cur.prepare('select text, stars from reviews11 where stars = :b')
    cur.execute(None, {'b': a})
    ##cur.execute('select text, stars from reviews123456')
    data = cur.fetchall()
    cur.close()
    con.close()
    z= 0
    d = {}
    data1 = []

    totalwords = 0
        


    for i in range(0,len(data)):
        z = 0
        z = data[i][0].split()
        for j in range(0,len(z)):
            if z[j] in d:
                d[z[j]] = d[z[j]] + 1
            else:
                d[z[j]] = 1
    totalwords= float(sum(d.values()))
    newdict = {}
    nd= {}
    if b in d:
        print d.get(b)
    print     

    main()
import cx_Oracle
import sys
import operator

def legit(a):
##    con = cx_Oracle.connect('yp','yp','xe')
##    cur = con.cursor()
##    ##cur.prepare('select text, stars from reviews123456 where stars = :b')
##    ##cur.execute(None, {'b': '1'})
##    cur.execute('select text, stars from reviews123456')
##    data = cur.fetchall()
##    cur.close()
##    con.close()
    z= 0
    d = {}
    data1 = []
    data = a.split()
    for i in range(0,len(data)):
        if data[i] in d:
            d[i] = d[i] + 1
        else:
            d[i] = 1
    

    totalwords = 0
        
    pos =['great', 'good', 'excellent', 'exceptional', 'favorable', 'marvelous', 'positive', \
     'satisfactory', 'satisfying', 'wonderful', 'superior', 'pleasing', 'happy',\
    'always','best', 'lovely','better','greater','perfect','first','prime','finest',\
    'terrific','supreme','delightful','inexpensive']
    neg = ['bad', 'atrocious', 'awful', 'crummy', 'dreadful', 'lousy', 'poor', 'rough',\
     'sad', 'unacceptable','garbage', 'gross', 'abomindable', 'amiss', 'cruddy',\
     'dissatisfactory', 'godawful', 'inadequate', 'unsatisfactory','frustrated',\
    'fusttration','sucks','overcooked']
    wm = 0
    totalwords= len(a.split())
    if totalwords > 62:
        wm = float(float(totalwords - 62)*-0.003030303)
    elif totalwords <=62:
        wm = float(float(totalwords-62)*0.0454668338)

    nd= {}
    pd = {}
    ##for i in remove:
    ##    if i in d.keys():
    ##        d.pop(i,None)
    for i in neg:
        if i in d.keys():
            nd[i] = d.get(i)
    for i in pos:
        if i in d.keys():
            pd[i] = d.get(i)
    sumspos = 0 
    sumspos = float(sum(pd.values()))
    sumsneg = 0
    sumsneg= float(sum(nd.values()))

    ##newdict = dict(sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:35])
    ##print sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:35]
    #print newdict
    ##print max(d.values())           
    predicatedrating = float(3.7) + float(float(.560784314)*sumspos) \
                       - float(sumsneg*float(1.9066666667)) + wm
    
    print [round(predicatedrating)]
    main()


    
main()
