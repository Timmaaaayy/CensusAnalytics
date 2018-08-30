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
        
        #print (fname)
        
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


# Remove unnecessary rows and then save as Excel
    
remove_topics = ['Household type', 
                 'Knowledge of official languages', 
                 'First official language spoken',
                 'Other language spoken regularly at home', 
                 'Knowledge of languages',
                 'Immigrant status and period of immigration', 
                 'Age at immigration',
                 'Generation status', 
                 'Admission category and applicant type', 
                 'Aboriginal population', 
                 'Highest certificate; diploma or degree', 
                 'Major field of study - Classification of Instructional Programs (CIP) 2016',
                 'Location of study compared with province or territory of residence with countries outside Canada',
                 'Work activity during the reference year', 
                 'Class of worker', 
                 'Occupation - National Occupational Classification (NOC) 2016', 
                 'Industry - North American Industry Classification System (NAICS) 2012',
                 'Place of work status', 
                 'Other language used regularly at work',
                 'Mobility status - Place of residence 1 year ago', 
                 'Mobility status - Place of residence 5 years ago']


include_age = {'Age characteristics': ['0 to 14 years',
                                       '15 to 19 years',
                                       '20 to 24 years',
                                       '25 to 29 years',
                                       '30 to 34 years',
                                       '35 to 39 years',
                                       '40 to 44 years',
                                       '45 to 49 years',
                                       '50 to 54 years',
                                       '55 to 59 years',
                                       '60 to 64 years',
                                       '65 years and over']}
    
include_citizen = {'Citizenship': ['Canadian citizens aged under 18',
                                   'Canadian citizens aged 18 and over']}
    
remove_comm_dest = {'Commuting destination': ['Total - Commuting destination for the employed labour force aged 15 years and over in private households with a usual place of work - 25% sample data']}


remove_comm_dur = {'Commuting duration': ['Total - Commuting duration for the employed labour force aged 15 years and over in private households with a usual place of work or no fixed workplace address - 25% sample data']}

remove_comm_mode = {'Main mode of commuting': ['Total - Main mode of commuting for the employed labour force aged 15 years and over in private households with a usual place of work or no fixed workplace address - 25% sample data']}

# need to do ethnic and lanauge manually and its distorted already and mother tongue

# need to do family

# need to do household and dwelling

# need to do immigrants (the way it's highlighted, your pivot table total is going to be distorted)
# same with visible minority


include_household = {'Household characteistics': ['Owner', 
                                                   'Renter']}

include_income_dec = {'Income of economic families in 2015': ['In the bottom decile',
                                                              'In the second decile',
                                                              'In the third decile',
                                                              'In the fourth decile',
                                                              'In the fifth decile',
                                                              'In the sixth decile',
                                                              'In the seventh decile',
                                                              'In the eighth decile',
                                                              'In the ninth decile',
                                                              'In the top decile']}
    

# income for household and individuals needs to be manual
# same with low income
    
include_employment = {'Labour force status': ['Employed',
                                              'Unemployed',
                                              'Not in the labour force']}
    
    
    
include_marriage = {'Marital status': ['Married or living common law',
                                       'Not married and not living common law']}
    
    
    
remove_work_time = {'Time leaving for work': ['Total - Time leaving for work for the employed labour force aged 15 years and over in private households with a usual place of work or no fixed workplace address - 25% sample data']}

include_pop = {'Population and dwellings': ['Population; 2011',
                                            'Private dwellings occupied by usual residents']}

for region in region_list:
    
    region_df_dict[region]['Topic'] = region_df_dict[region]['Topic'].str.lstrip()
    region_df_dict[region]['Characteristics'] = region_df_dict[region]['Characteristics'].str.lstrip()
  
    region_df_dict[region] = region_df_dict[region].loc[~region_df_dict[region]['Topic'].isin(remove_topics)]
        
    region_df_dict[region].to_excel("Split into Regions (Organized)\\" + region + ".xlsx")
    
    
    
