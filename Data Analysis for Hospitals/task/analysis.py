import pandas as pd

pd.set_option('display.max_columns', 8)

df_g = pd.read_csv('test/general.csv')
df_p = pd.read_csv('test/prenatal.csv')
df_s = pd.read_csv('test/sports.csv')

######################################################################################################################
# Stage 1 ############################################################################################################
######################################################################################################################
# print(df_g.head(20))
# print(df_p.head(20))
# print(df_s.head(20))

######################################################################################################################
# Stage 2 ############################################################################################################
######################################################################################################################
# print(df_g.columns)
# print(df_p.columns)
# print(df_s.columns)
# Index(['Unnamed: 0', 'hospital', 'gender', 'age', 'height', 'weight', 'bmi',
#        'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray',
#        'children', 'months'],
#       dtype='object')
# Index(['Unnamed: 0', 'HOSPITAL', 'Sex', 'age', 'height', 'weight', 'bmi',
#        'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray',
#        'children', 'months'],
#       dtype='object')
# Index(['Unnamed: 0', 'Hospital', 'Male/female', 'age', 'height', 'weight',
#        'bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray',
#        'children', 'months'],
#       dtype='object')

# df_p = df_p.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'})
# df_s = df_s.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'})


df_p = df_p.set_axis(df_g.columns, axis=1)
df_s = df_s.set_axis(df_g.columns, axis=1)
# print(df_g.columns.all() == df_p.columns.all() == df_s.columns.all())  # True

df = pd.concat([df_g, df_p, df_s], ignore_index=True)
df = df.drop(columns='Unnamed: 0')
# print(df.sample(n=20, random_state=30))

######################################################################################################################
# Stage 3 ############################################################################################################
######################################################################################################################
#
# delete empty rows:
df = df.dropna(axis=0, how='all')

# fix multiple gender encodings:
# print(df.gender.unique())  # ['man' 'woman' nan 'female' 'male']
# see raplacing at near EoF to see how replace() could have been used here instead
df.loc[df.gender.isin(['man', 'male']), 'gender'] = 'm'
df.loc[df.gender.isin(['woman', 'female']), 'gender'] = 'f'
# print(df.gender.unique())  # ['m' 'f' nan]

# assume f for patients in prenatal hospital
df.loc[(df.hospital == 'prenatal') & (df.gender.isnull()), 'gender'] = 'f'

# replace NaNs with 0 in selected columns
for column in ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']:
    df[column].fillna(0, inplace=True)
# probably df.update[df['list', 'of, 'columns', 'here']].fillna(0)) would work here too
# printout time!
# print(df.shape)
# print(df.sample(n=20, random_state=30))

######################################################################################################################
# Stage 3 ############################################################################################################
######################################################################################################################
#
# Which hospital has the highest number of patients?
print('The answer to the 1st question is', df['hospital'].value_counts().idxmax())

# What share of the patients in the general hospital suffers from stomach-related issues? Round the result to the third decimal place.
print('The answer to the 2nd question is',
      round(df.loc[(df.hospital == 'general') & (df.diagnosis == 'stomach')].shape[0] /
            df.loc[(df.hospital == 'general')].shape[0], 3))
# What share of the patients in the sports hospital suffers from dislocation-related issues? Round the result to the third decimal place.
print('The answer to the 3rd question is',
      round(df.loc[(df.hospital == 'sports') & (df.diagnosis == 'dislocation')].shape[0] /
            df.loc[(df.hospital == 'sports')].shape[0], 3))

# What is the difference in the median ages of the patients in the general and sports hospitals?
tmp = df.groupby('hospital')['age'].median().loc[['general', 'sports']].to_list()
print('The answer to the 4th question is', tmp[0] - tmp[1])

#After data processing at the previous stages, the blood_test column has three values: t= a blood test was taken,
# f= a blood test wasn't taken, and 0= there is no information.
# In which hospital the blood test was taken the most often
# (there is the biggest number of t in the blood_test column among all the hospitals)?
# How many blood tests were taken?
tmp = df.loc[df.blood_test == 't'].groupby('hospital')['blood_test'].count()
print(f'The answer to the 5th question is {tmp.idxmax()}, {tmp[tmp.idxmax()]} blood tests')

######################################################################################################################
# From topics ########################################################################################################
######################################################################################################################

# count how many columns have nulls:
# print(df.isnull().any().sum())

# delete columns with >= 10 NaNs:
# data.dropna(axis=1, thresh=10, inplace=True)

# Replace NaNs:
# # Fill NaNs with the most frequent value (the mode in the language of statistics) for categorical features:
# mode_district = data['district'].mode()[0] # calculate the mode
# data['district'].fillna(mode_district, inplace=True) # replace NaNs with that mode

# 2) For numerical features, use the column average. In our dataset, we first process the totsp column:
# mean_totsp = data['totsp'].mean() # calculate the average
# data['totsp'].fillna(mean_totsp, inplace=True) # replace NaNs with that average

# Let's fill the missing values with the average for the district, where the given flat is located:
# data['dist2subway'] = data.groupby('district')['dist2subway'].apply(lambda x: x.fillna(x.mean()))

# 3) Fill the missing values with a median value for numerical features.
# This is usually the way to choose when a feature has outliers. They affect the average, so it no longer represents a typical value of this feature. Fortunately, outliers don't bother the median value.
# median_price = data['price'].median() # calculate the median value
# data['price'].fillna(median_price, inplace=True) # replace NaNs with that value

# use mean in all columns:
#df.fillna(df.mean())

# replacing
# (1) Replace a single value with a new value for an individual DataFrame column:
#
# df['column name'] = df['column name'].replace(['old value'], 'new value')
# (2) Replace multiple values with a new value for an individual DataFrame column:
#
# df['column name'] = df['column name'].replace(['1st old value', '2nd old value', ...], 'new value')
# (3) Replace multiple values with multiple new values for an individual DataFrame column:
#
# df['column name'] = df['column name'].replace(['1st old value', '2nd old value', ...], ['1st new value', '2nd new value', ...])
# (4) Replace a single value with a new value for an entire DataFrame:
#
# df = df.replace(['old value'], 'new value')