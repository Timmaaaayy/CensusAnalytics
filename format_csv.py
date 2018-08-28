# STYLE NOTE: All imports must be at the top in this order.
# 1) import <python packages>
# 2) import <your modules>

import os
import glob
import pandas as pd


dir_path = os.path.dirname(os.path.realpath(__file__))
region_path = dir_path + '\\Split into Regions\\'

region_list = ['Avondale', 'Bathurst', 'Bayview', 'Lansing', 'Newtonbrook NE',
               'Newtonbrook NW', 'Netwonbrook SW', 'Yonge East', 'Yonge West']



counter = 0
# Loop through all folders/regions (9)
for region in region_list:
    
    print (region_path + region)
    
    # Loop through all CSV files in each folder/region (130)
    for fname in glob.glob(region_path + region + '/*.csv'):
        
        counter +=1
        
    
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
        
        df = pd.read_csv(fname, encoding = "ISO-8859-1")
        df = df.reset_index()
        print (df)
        print (df.iloc[0])
        
        df = df.columns


print (counter)
# This is just a test area for handling the CSV data
# M2R Code (Area Code)
M2R = pd.read_csv("M2R Raw Data.csv", encoding = "ISO-8859-1")
M2R.fillna('', inplace=True)



print (len(M2R['Topic'].unique()))

topics = list(M2R['Topic'].unique())
    
    
topic_dict = {}

for item in topics:
    
    topic_dict[item] = M2R.loc[M2R['Topic'] == item]
    
    topic_dict[item] = topic_dict[item].set_index('Topic')
    
    #print (topic_dict[item])
    
