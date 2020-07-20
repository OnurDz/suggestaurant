import statistics as st

def speed(sp):
    slow = -1.0
    sufficient = -1.0
    fast = -1.0

    if sp <= 5:
        slow = - sp/3 + 5/3
    if sp >= 4 and sp <= 6:
        sufficient = sp/2 - 2
    if sp > 6 and sp <= 8:
        sufficient = - sp/2 + 4
    if sp >= 7:
        fast = sp/2 - 7/2
    
    slow = fuzz(slow)
    sufficient = fuzz(sufficient)
    fast = fuzz(fast)

    return [slow, sufficient, fast]

def taste(ts):
    bad = -1
    sufficient = -1
    tasty = -1

    if ts <= 7:
        bad = - ts/2 + 7/2
    if ts >= 6 and ts <= 7.5:
        sufficient = (2*ts)/3 - 4
    if ts > 7.5 and ts <= 9:
        sufficient = - (2*ts)/3 + 6
    if ts >= 7.5:
        tasty = (2*ts)/3 - 5

    bad = fuzz(bad)
    sufficient = fuzz(sufficient)
    tasty = fuzz(tasty)

    return [bad, sufficient, tasty]

def serv_quality(qu):
    #  y = -1/2(x) + 7/2 ->   0 - 7    araligi
    #  y =  1/2(x) -  3  ->   6 - 10   araligi
    not_sufficient = -1
    sufficient = -1
    if qu <= 7:
        not_sufficient = - qu/2 + 7/2
    if qu >= 6:
        sufficient = qu/2 - 3

    not_sufficient = fuzz(not_sufficient)
    sufficient = fuzz(sufficient)

    return [not_sufficient, sufficient]

def rule_base(entry):

    sp = entry[0]
    ts = entry[1]
    qu = entry[2]

    lows = []
    meds = []
    highs = []

    #if speed is SLOW and taste is BAD then match is LOW
    lows.append(fuzzy_and(speed(sp)[0], taste(ts)[0]))
    #if speed is SLOW and taste is SUFFICIENT then match is LOW
    lows.append(fuzzy_and(speed(sp)[0], taste(ts)[1]))
    #if speed is SLOW and taste is TASTY then match is MED
    meds.append(fuzzy_and(speed(sp)[0], taste(ts)[2]))
    #if speed is SLOW and serv is not_sufficient then match is LOW
    lows.append(fuzzy_and(speed(sp)[0], serv_quality(qu)[0]))
    
    #if speed is SUFFICIENT and taste is TASTY then match is HIGH
    highs.append(fuzzy_and(speed(sp)[1], taste(ts)[2]))
    #if speed is SUFFICIENT and taste is SUFFICIENT then match is MED
    meds.append(fuzzy_and(speed(sp)[1], taste(ts)[1]))
    #if speed is SUFFICIENT and taste is BAD then match is LOW
    lows.append(fuzzy_and(speed(sp)[1], taste(ts)[0]))
    
    #if speed is FAST and taste is TASTY then match is HIGH
    highs.append(fuzzy_and(speed(sp)[2], taste(ts)[2]))
    #if speed is FAST and serv is SUFFICIENT then match is HIGH
    highs.append(fuzzy_and(speed(sp)[2], serv_quality(qu)[1]))
    #if speed is FAST and taste is SUFFICIENT then match is HIGH
    highs.append(fuzzy_and(speed(sp)[2], taste(ts)[1]))
    
    #if taste is BAD and serv is not_sufficient then match is LOW
    lows.append(fuzzy_and(taste(ts)[0], serv_quality(ts)[0]))
    #if taste is BAD and speed is FAST then MED
    meds.append(fuzzy_and(taste(ts)[0], speed(sp)[2]))
    
    #print(lows, meds, highs)
    low, med, high = st.mean(lows), st.mean(meds), st.mean(highs)
    #print(low, med, high)
    return [low, med, high]

def defuzz(entry):
    low, med, high = rule_base(entry)
    upper = low * (0 + 10 + 20 + 30 + 40) + med * (50 + 60 + 70) + high * (80 + 90 + 100)
    lower = 5 * low + 3 * med + 3 * high
    return upper/lower
    
def fuzz(x):
    if x > 1:
        x = 1
    elif x < 0:
        x = 0
    return x

def fuzzy_and(f, s):
    return (f + s) / 2
