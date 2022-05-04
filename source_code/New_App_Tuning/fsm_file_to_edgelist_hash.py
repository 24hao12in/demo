"""
step
1: make a new folder for each frame 
2. cp subpattern file into the folder 
3. make 2 new folders edgelist & hash 
4. convert gspan output text file to edgelist and hash

"""

import os
from os import path
import shutil
import re
import csv

src = './output_for_fsm/'
ist = 'v 0'

files = [i for i in os.listdir(src) if i.endswith("percent")]
for f in files:
    print(f)
    fnum = f.split('_gspan')[0]
    dst = src+fnum +'_distinct/'
    if(os.path.isdir(dst) == False):
        os.mkdir(dst)
        os.mkdir(dst+'edgelist/')
        os.mkdir(dst+'hash/')
        shutil.copy(path.join(src, f), dst+fnum+'_distinct')
    
    entries = os.listdir(dst)
    for entry in entries:
        if entry.startswith('f'):
            readPath = dst + entry
            with open (readPath, 'r') as fin:
                count = 0
                for line in fin:
                    if ist in line:
                        writePath1 = dst+'edgelist/'+entry+'_'+str(count)+'.csv'
                        writePath2 = dst+'hash/'+entry+'_'+str(count)+'.csv'
                        count+=1
                        edgelist=[]
                        nodelist=[]
                        ee = [m.start() for m in re.finditer('e ', line)]
                        vv = [m.start() for m in re.finditer('v ', line)]
                        for idx in range(len(ee)):
                            if(idx+1 < len(ee)):
                                temp = line[ee[idx]+2:ee[idx+1]]
                                temp1 = [int(i) for i in temp.split()[:-1]]
                                edgelist.append(temp1)
        
                            else:
                                temp = line[ee[idx]+2:]
                                #edgelist.append(temp[:-2])
                                temp1 = [int(i) for i in temp.split()[:-1]]
                                edgelist.append(temp1)
        
                        for idx in range(len(vv)):
                            if(idx+1 < len(vv)):
                                temp = line[vv[idx]+2:vv[idx+1]]
                                temp1 = [i for i in temp.split()]
                                nodelist.append(temp1)
        
                            else:
                                temp = line[vv[idx]+2:ee[0]]
                                #edgelist.append(temp[:-2])
                                temp1 = [i for i in temp.split()]
                                nodelist.append(temp1)
                                
                           
                        file = open(writePath1, 'w', newline ='')        
                        with file:
                            write = csv.writer(file)
                            write.writerows(edgelist)
                
                       
                        file_hash = open(writePath2, 'w', newline ='')        
                        with file_hash:
                            write = csv.writer(file_hash)
                            write.writerows(nodelist)



