import music_ai as m
import random

C_MAJ_DATA = '''C 3356 2562 2154 1322 530 36
G 3365 2681 2161 1528 612 41
E 2149 1877 1650 1140 423 30
D 1859 1978 1723 1123 481 31
F 1588 1475 1358 813 308 22
A 1586 1474 1248 895 344 26
B 1598 1468 1302 819 356 26
G# 517 500 451 254 77 13
D# 401 359 334 176 75 12
F# 531 601 614 384 149 13
A# 307 376 319 215 80 11
C# 320 374 339 214 70 10'''

def get_time_sig() -> (str,str):
    string = input('Enter a time signature, for example, "4/4":\n')
    l = string.split('/')   
        
    while len(l) != 2 or not is_power_two(int(l[1])):
        string = input('Enter a valid time signature:\n')
        l = string.split('/')
    return tuple(l)

def is_power_two(i:int)-> bool:
    while i%2 == 0:
        if i == 2:                  
            return True
        i = i//2  
    return False

T_4_4 = [20,1,4,1,10,2,4,1,16,1,4,1,10,2,4,1]
S_4_4 = {1:[0],2:[8],3:[4,12],4:[2,6,10,14],5:[1,3,5,7,9,11,13,15]}

def generate_rythym(l) -> list:
    """Generate a list, using list l as rythm probabilities out of 20, 
    containing the beats which have notes. Ex: [0,4,5,6,9,12]"""
    j = l[:]
    r_list = []
    for i in range(len(j)):
        probability = j[i]/20  
        #now, probability is between 0, 1, by this probability, add i to r_list
        if random.random() < probability:
            r_list.append(i)
    return r_list

def get_7th (s,start) -> list:
    l = s.split()
    result = []
    for i in range(start,len(l),7):
        result.append(l[i])
    return ( result)


def generate_notes(r_list:list) -> list:
    """>>>generate_notes([0,4,8,12,15])
    ['C','G','D','Eb','F']
    Now only works with major keys, and does not distinguish bw strong/weak 
    beats yet
    
    """
    
    notes_list = []
    for i in range(len(r_list)):
        #Choose a note
        #FIRST, figure out what type of beat it's on
        beat_strength = get_strength(r_list[i])
        #now, choose a note at random, using probabilities
        probabilities_list = get_freqs(beat_strength)
        #pick aa random index from 0 to 11, then get the note from m.NOTENAMES
        note_index = random.choices(range(12),weights=probabilities_list)
        #note index is actually a list - can use this to pick the best choice 
        #to ensure melody connectedness
        notes_list.append(m.NOTENAMES[note_index[0]])
    return notes_list
        
def get_strength(i:int) -> int:
    """Takes the beat number i and returns the strength of beat. 
    1 is beat 1, 2 is beat 3, 3 is 2+4, 4 is eighths, 5 is sixteenths.
    """
    actual_strength = 1
    for strength in S_4_4:
        if i in S_4_4[strength]:
            return strength  

def get_freqs(which_strength:int): 
    """Get the frequency list of C Major, given an int to specify beat strength.
    1 is beat 1, 2 is beat 3, 3 is 2+4, 4 is eighths, 5 is sixteenths.
    """
    cols = []
    for i in range(7):
        cols.append(get_7th(C_MAJ_DATA,i))
    #now, sort the list
    #for each element in m.notenames, find index i of cols[0] so that
    #cols[0][i] == notename such as 'C'
    # we are trying to get separate lists which are ordered in c,c#,d...
    result = []
    for notename in m.NOTENAMES:
        #notenames goes from c to b
        list_index = cols[0].index(notename)
        result.append(int(cols[which_strength][list_index]))
    return result

def generate_melody():
    r = generate_rythym(T_4_4)
    n = generate_notes(r)
    print(r)
    print(n)