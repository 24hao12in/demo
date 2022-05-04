import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools

path1 = './fireStrick/FS_rawdata_node_occurance_f520_10x_f3120.csv'
df = pd.read_csv(path1 , header = 'infer')

list_to_plot3=[]
list_to_plot4 = []

# add scene column 
scene = []
for i in df['frame']: 
    if int(i) > 1650: 
        scene.append(1)
    else: 
        scene.append(0)
        
df['scene'] = scene

node_sort_0 = df[df.scene ==0]
node_sort_0 = node_sort_0.sort_values(by=['nodesize'])
node_set_0 = node_sort_0.drop_duplicates(subset=['nodesize'])['nodesize'].sort_values(ascending=True)
 
node_sort_1 = df[df.scene ==1]
node_sort_1 = node_sort_1.sort_values(by=['nodesize'])
node_set_1 = node_sort_1.drop_duplicates(subset=['nodesize'])['nodesize'].sort_values(ascending=True)


node_0_group=range(1,174)
node_1_group=range(1,174)
## for scene1 
for idx in range(6):
    small_set = set(itertools.islice(node_0_group, idx*10+0, idx*10+10))
    print(small_set)
#   print(each)
    temp1 =pd.DataFrame(columns = ['nodesize', 'occurance', 'frame'])
    for each in  small_set:

        temp = node_sort_0[node_sort_0.nodesize == each]
        temp1 = temp1.append(temp)
        sum_occ = sum(temp1['occurance'])

    list_to_plot3.append(sum_occ)
    
small_set = set(range(61,300))
for each in  small_set:
    temp = node_sort_0[node_sort_0.nodesize == each]
    temp1 = temp1.append(temp)
    sum_occ = sum(temp1['occurance'])

list_to_plot3.append(sum_occ)
list_to_plot3_sum = sum(list_to_plot3)
for each in list_to_plot3:
    tem = each/list_to_plot3_sum
    list_to_plot4.append(tem)    
##
    
    
## for scene2 , plot separately     
for idx in range(6):
    small_set = set(itertools.islice(node_1_group, idx*10+0, idx*10+10))
    print(small_set)
#   print(each)
    temp1 =pd.DataFrame(columns = ['nodesize', 'occurance', 'frame'])
    for each in  small_set:

        temp = node_sort_1[node_sort_1.nodesize == each]
        temp1 = temp1.append(temp)
        sum_occ = sum(temp1['occurance'])

    list_to_plot3.append(sum_occ)
    
small_set = set(range(61,300))
for each in  small_set:
    temp = node_sort_1[node_sort_1.nodesize == each]
    temp1 = temp1.append(temp)
    sum_occ = sum(temp1['occurance'])

list_to_plot3.append(sum_occ)

list_to_plot3_sum2 = sum(list_to_plot3[7:])
for each in list_to_plot3[7:]:
    print(each)
    tem = each/list_to_plot3_sum2
    list_to_plot4.append(tem)
#

# Create a figure instance
fig = plt.figure(1, figsize=(12,7))
labelsize=30
# Create an axes instance
ax = fig.add_subplot(111)
ax.xticks=([i for i in range(7)])
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
ax.set_yticks(np.arange(0,0.51, step=0.1000))       
plt.yticks([0, 0.1, 0.2,0.3,0.4,0.5],["0%","10%","20%","30%","40%","50%"])   
ax.set_xticks(x + dimw / 2)
for tick in ax.get_xticklabels():
    tick.set_rotation(45)
ax.tick_params(size=15)   
ax.tick_params(labelsize=labelsize)   
ax.set_xlabel('node count group', fontsize=labelsize)
ax.set_ylabel("% of graphs having specific node count", fontsize=labelsize-3)
ax3 = ax.twiny()
new_tick_locations = np.array([0, 0.5])
ax3.set_xticks(new_tick_locations)



ax3.set_xticklabels(['                                         Scene1',
                     '                                         Scene2'])

ax3.tick_params(labelsize=labelsize)
ax3.tick_params(size=labelsize-20)
ax3.grid( linestyle='-', linewidth=2)#
