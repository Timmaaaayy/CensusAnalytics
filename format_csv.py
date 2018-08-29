# STYLE NOTE: All imports must be at the top in this order.
# 1) import <python packages>
# 2) import <your modules>

import os
import glob
import pandas as pd


dir_path = os.path.dirname(os.path.realpath(__file__))
region_path = dir_path + '\\Split into Regions\\'

region_list = ['Avondale', 'Bathurst', 'Bayview', 'Lansing', 'Newtonbrook NE',
               'Newtonbrook NW', 'Newtonbrook SW', 'Yonge East', 'Yonge West']

df_dict = {}
# TEST AREA FOR CSV
M2R = pd.read_csv("M2R Raw Data.csv", encoding = "ISO-8859-1")
M2R.fillna('', inplace=True)

print (len(M2R['Topic'].unique()))
topics = list(M2R['Topic'].unique())
    
topic_dict = {}

for item in topics:
    
    topic_dict[item] = M2R.loc[M2R['Topic'] == item]
    topic_dict[item] = topic_dict[item].set_index('Topic')






# ACTUAL CODE
for region in region_list:  # this should fixed to simply loop through a series of randomly named folders
    
    print (region_path + region)
    
    # Loop through all CSV files in each folder/region (130)

    for fname in glob.glob(region_path + region + '/*.csv'):

        file_name = (fname.split('\\', 6)[-1])      # 123456789.csv
        file_code = str((file_name.split('.')[0]))  # just 123456789
        
        print (fname)
        
        """
        # SECTION 1: Removing useless stuff at bottom 
        # Keep this just in case the files get refreshed somehow
        with open(fname, 'r+') as f:
            s = f.read()
            f.seek(0)
            s = (s.split("Symbols:")[0])         # Only keep before lame comments
            #print (s)
            f.write(s)
            f.truncate()
            f.close()
        """        
        
        df = pd.read_csv(fname, skiprows=1, encoding = "ISO-8859-1")
        
        df = df[['Topic', 'Characteristics', 'Male', 'Female', 'Total']]
        df['file_code'] = file_code
        df['Region'] = region
        
        df_dict[file_code] = df
        
region_df_dict = {}

for region in region_list:
    
    region_df_dict[region] = pd.DataFrame(columns=['Topic', 'Characteristics', 'Male', 'Female', 'Total', 'file_code', 'Region'])
    
    for code, data in df_dict.items():
        
        if data['Region'].str.contains(region).all():
            
            region_df_dict[region] = pd.concat([region_df_dict[region], data])
            
for key, value in region_df_dict.items():
    
    region_df_dict[key] = region_df_dict[key].sort_values(by=['Topic'])

for region in region_list:
    
    region_df_dict[region].to_excel("Split into Regions (Organized)\\" + region + ".xlsx")
    
    
    
