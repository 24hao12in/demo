"""
Find the max WL kernel values for each fsm in each game with other games
"""


import os 
import pandas as pd
 
src1 = './allshader_gspan_output/25percent_result/WL/'
   
games = [i for i in os.listdir(src1) if i.startswith('f') and i.endswith('_maxInCol.csv')]

temp1 =pd.DataFrame()
training =pd.DataFrame()

game1list = []
for game in games: 
    game1 = game.split('_to_')[0]
    game2 = game.split('_to_')[1]
    game1list.append(game1)
    wl_list = pd.read_csv(src1 +game, header = 'infer', index_col = 0)
    game3 = game1+'&'+game2
    temp1[game3] = wl_list
    
game1list1= list(dict.fromkeys(game1list))    
#temp1.to_csv(src1 + 'maxInCol_summary.csv', index=False)
    
    
### arrange to training data format 
temp1.columns = [i for i in range(420)] 

for i in range(29): # total 28 games
    temp = temp1.iloc[:, i:i+27]
    
    temp = temp.dropna()
    if(i<27):
        temp.insert(i, 'self', 1)
    else:
        temp['self']=1
    temp.columns = [i for i in range(21)]
    training = training.append(temp)
    
training.columns = [i for i in game1list1]    
training.to_csv(src1 + 'maxInCol_training.csv', index=False)
