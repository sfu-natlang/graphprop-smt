import sys
from operator import itemgetter
from collections import defaultdict


def map_using_map_file(map_file):
    map_dict=dict()
    for line in map_file:
        id, word=line.strip().split('\t', 1)
        map_dict[word.strip()]=id
        #map_dict[id]=word.strip()
    for line in sys.stdin:
    #for line in open('europarl+acquis+news/nostop-d0.3.1g-rmvFreq1/biGraph-n20-l20.label_prop_output'):
        ids=[]
        for word in line.strip().split():
            if word not in map_dict:
                sys.stderr.write('Error: word is not found %s\n'%word)
                #sys.exit(5)
                map_dict[word]=word
            ids.append(map_dict[word])
        print ' '.join(ids)
        
def reverse_map(map_file):
    map_dict=dict()
    for line in map_file:
        id, word=line.strip().split('\t', 1)
        #map_dict[word.strip()]=id
        map_dict[id]=word.strip()
    for line in sys.stdin:
    #for line in open('europarl+acquis+news/nostop-d0.3.1g-rmvFreq1/biGraph-n20-l20.label_prop_output'):
        words=[]
        for id in line.strip().split():
            if id not in map_dict:
                sys.stderr.write('Error: word is not found %s\n'%word)
                #sys.exit(5)
                map_dict[id]=id
            words.append(map_dict[id])
        print ' '.join(words) 

def map():
    curr_no=1
    lines=[]
    map_dict=dict()
    freqDict=defaultdict(int)
    for line in sys.stdin:
        line=line.strip()
        splits=line.split()
        lines.append(splits)
        for word in splits:
            freqDict[word]+=1
    items=freqDict.items()
    items.sort(key=itemgetter(1), reverse=True)
    for word, _ in items:
        map_dict[word]=str(curr_no)
        curr_no+=1
    for splits in lines:
        ids=[]
        for word in splits:
            ids.append(map_dict[word])
        print ' '.join(ids)
    f=open('map.id', 'w')
    items=map_dict.items()
    items.sort(key=lambda x:int(x[1]))
    for key, value in items:
        f.write('%s\t%s\n'%(value, key))
    f.close()    



#src_file=open(sys.argv[1])
if len(sys.argv)==1:
    map();
elif len(sys.argv)==2:
    map_file=open(sys.argv[1])
    map_using_map_file(map_file)
elif len(sys.argv)==3 and sys.argv[2]=='reverse': 
    map_file=open(sys.argv[1])
    reverse_map(map_file)
    
