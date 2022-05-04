import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools

path1 = './fireStrick/rawdata_nodesize/FS_rawdata_edge_occurance_f520_10x_f3120.csv'
df = pd.read_csv(path1 , header = 'infer')

list_to_plot3 = []
list_to_plot4 = []
# add scene column 
scene = []
for i in df['frame']: 
    if int(i) > 1650: 
        scene.append(1)
    else: 
        scene.append(0)
        
df['scene'] = scene


edge_sort_0 = df[df.scene ==0]
edge_sort_0 = edge_sort_0.sort_values(by=['edgesize'])
edge_set_0 = edge_sort_0.drop_duplicates(subset=['edgesize'])['edgesize'].sort_values(ascending=True)

x = np.cumsum(edge_sort_0['occurance'])
edge_sort_0['cum_occ'] = x


edge_sort_1 = df[df.scene ==1]
edge_sort_1 = edge_sort_1.sort_values(by=['edgesize'])
edge_set_1 = edge_sort_1.drop_duplicates(subset=['edgesize'])['edgesize'].sort_values(ascending=True)

x = np.cumsum(edge_sort_1['occurance'])
edge_sort_1['cum_occ'] = x


edge_0_group=range(1,219)
edge_1_group=range(1,219)
## for scene1 
for idx in range(6):
    small_set = set(itertools.islice(edge_0_group, idx*10+0, idx*10+10))
    print(small_set)
#   print(each)
    temp1 =pd.DataFrame(columns = ['edgesize', 'occurance', 'frame'])
    for each in  small_set:
        temp = edge_sort_0[edge_sort_0.edgesize == each]
        temp1 = temp1.append(temp)
        sum_occ = sum(temp1['occurance'])

    list_to_plot3.append(sum_occ)
##
small_set = set(range(61,300))
for each in  small_set:
    temp = edge_sort_0[edge_sort_0.edgesize == each]
    temp1 = temp1.append(temp)
    sum_occ = sum(temp1['occurance'])

list_to_plot3.append(sum_occ)  
#len1 = len(list_to_plot3)  
list_to_plot3_sum = sum(list_to_plot3)
for each in list_to_plot3:
    tem = each/list_to_plot3_sum
    list_to_plot4.append(tem)    


## for scene2 , plot separately     
for idx in range(6):
    small_set = set(itertools.islice(edge_set_1, idx*10+0, idx*10+10))
    print(small_set)
#   print(each)
    temp1 =pd.DataFrame(columns = ['edgesize', 'occurance', 'frame'])
    for each in  small_set:

        temp = edge_sort_1[edge_sort_1.edgesize == each]
        temp1 = temp1.append(temp)
        sum_occ = sum(temp1['occurance'])

    list_to_plot3.append(sum_occ)
#
small_set = set(range(61,300))
for each in  small_set:
    temp = edge_sort_1[edge_sort_1.edgesize == each]
    temp1 = temp1.append(temp)
    sum_occ = sum(temp1['occurance'])

list_to_plot3.append(sum_occ)    

list_to_plot3_sum2 = sum(list_to_plot3[7:])
for each in list_to_plot3[7:]:
    print(each)
    tem = each/list_to_plot3_sum2
    list_to_plot4.append(tem)
    
    
# Create a figure instance
fig = plt.figure(1, figsize=(12,7))
labelsize=30
# Create an axes instance
ax = fig.add_subplot(111)
ax.xticks=([i for i in range(14)])
ax.set_xticklabels(('1-10', '11-20', '21-30','31-40','41-50','51-60'
                      ,'>60'
                      ,'1-10', '11-20', '21-30','31-40','41-50','51-60'
                      ,'>60'),ha='center')


dim = 14
w =7.75
dimw = w / dim

x = np.arange( 14)

y = [d for d in list_to_plot4]
ax.bar(x + 0.5 * dimw, y, dimw, bottom=0.001)
#y = [d[1] for d in list_to_plot3]
#ax.bar(x + 0 * dimw, y, dimw, bottom=0.001, label = '#input')
ax.set_yticks(np.arange(0,0.51, step=0.1000))
   
plt.yticks([0, 0.1, 0.2,0.3,0.4,0.5],["0%","10%","20%","30%","40%","50%"])  


ax.set_xticks(x + dimw / 2)
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

ax.tick_params(size=15)   
ax.tick_params(labelsize=labelsize)   
ax.set_xlabel('edge count group', fontsize=labelsize)

ax.set_ylabel(" % of graphs having specific edge count", fontsize=labelsize-3)

##----------ax3-----------------
ax3 = ax.twiny()
new_tick_locations = np.array([0, 0.5])
ax3.set_xticks(new_tick_locations)

ax3.set_xticklabels(['                                         Scene1',
                     '                                         Scene2'])

ax3.tick_params(labelsize=labelsize)
ax3.tick_params(size=labelsize-20)
ax3.grid( linestyle='-', linewidth=2)#