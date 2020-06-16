import pandas as pd

def get_index(i,element):
    try:
        index = data['Nutrition'][i].index(element)
    except ValueError:
        return False
    return index

data = pd.read_csv("Yummly Data.csv")
data = data.drop(columns=['Unnamed: 0'])
data['Ingredients'] = [data['Ingredients'][i][2:-2].split("\', \'") for i in range(len(data['Ingredients']))]
data['Tags'] = [data['Tags'][i][2:-2].split("\', \'") for i in range(len(data['Tags']))]
data['Nutrition'] = [data['Nutrition'][i][2:-2].split("\', \'") for i in range(len(data['Nutrition']))]

SODIUM_percentage, SODIUM_amount, FAT_percentage, FAT_amount, PROTEIN_percentage, PROTEIN_amount, \
CARBS_percentage, CARBS_amount, FIBER_percentage, FIBER_amount = [], [], [], [], [], [], [], [], [], [] 

for i in range(len(data['Nutrition'])):
    if get_index(i,'SODIUM'):
        SODIUM_index = get_index(i,'SODIUM')  
        SODIUM_percentage.append(data['Nutrition'][i][SODIUM_index+1].split(' ')[0])
        SODIUM_amount.append(data['Nutrition'][i][SODIUM_index+2])
    else:
        SODIUM_percentage.append('N/A'), SODIUM_amount.append('N/A')

    if get_index(i,'FAT'):
        FAT_index = get_index(i,'FAT')  
        FAT_percentage.append(data['Nutrition'][i][FAT_index+1].split(' ')[0])
        FAT_amount.append(data['Nutrition'][i][FAT_index+2])
    else:
        FAT_percentage.append('N/A'), FAT_amount.append('N/A')

    if get_index(i,'PROTEIN'):
        PROTEIN_index = get_index(i,'PROTEIN')  
        PROTEIN_percentage.append(data['Nutrition'][i][PROTEIN_index+1].split(' ')[0])
        PROTEIN_amount.append(data['Nutrition'][i][PROTEIN_index+2])
    else:
        PROTEIN_percentage.append('N/A'), PROTEIN_amount.append('N/A')

    if get_index(i,'CARBS'):
        CARBS_index = get_index(i,'CARBS')  
        CARBS_percentage.append(data['Nutrition'][i][CARBS_index+1].split(' ')[0])
        CARBS_amount.append(data['Nutrition'][i][CARBS_index+2])
    else:
        CARBS_percentage.append('N/A'), CARBS_amount.append('N/A')

    if get_index(i,'FIBER'):
        FIBER_index = get_index(i,'FIBER')  
        FIBER_percentage.append(data['Nutrition'][i][FIBER_index+1].split(' ')[0])
        FIBER_amount.append(data['Nutrition'][i][FIBER_index+2])
    else:
        FIBER_percentage.append('N/A'), FIBER_amount.append('N/A')

extra_columns = [SODIUM_percentage, SODIUM_amount, FAT_percentage, FAT_amount, PROTEIN_percentage, \
                 PROTEIN_amount, CARBS_percentage, CARBS_amount, FIBER_percentage, FIBER_amount]

extra_columns_name = ["SODIUM_percentage", "SODIUM_amount", "FAT_percentage", "FAT_amount", "PROTEIN_percentage", \
                      "PROTEIN_amount", "CARBS_percentage", "CARBS_amount", "FIBER_percentage", "FIBER_amount"]

for items in range(len(extra_columns)):
    data['{}'.format(extra_columns_name[items])] = extra_columns[items]

data = data.drop(columns=['Nutrition'])
data.to_csv("CLEAN DATA.csv")
