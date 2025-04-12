import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import matplotlib.ticker as mtick
from scipy.stats import shapiro
from scipy.stats import chi2_contingency
import statsmodels.api as sm
from scipy.stats import ttest_rel


data = pd.read_excel(r"C:\Users\hp\Desktop\sem 4 projects\python ca 2\modified datset.xlsx")
print(data.head())
print(data.tail())
print(data.describe())
data.info()
print("Is ther any null values:")
print(data.isnull().sum())
print("Is there any duplicates:")
print(data.duplicated().sum())


# Objective 1:- Descriptive Statistics for Literacy Rate



state_data = data[(data['Distt_Code'] == 0) & (data['Age_group'] == 'All ages') & (data['Total_or_Rural_or_Urban'] == 'Total')&(data['State_Code']!=0)]
state_population =state_data['Total_Persons'].copy()
state_data.loc[:, 'Literacy_Rate'] = (state_data['Literate_Persons'] / state_population) * 100
print(state_data['Literacy_Rate'].describe().apply(lambda x: "{:.2f}".format(x)))
plt.figure(figsize=(9, 6))
ax=sns.histplot(data=state_data,bins=10, x='Literacy_Rate', color='skyblue',kde=True)
plt.title('Distribution of Literacy Rate Across States')
plt.xlabel('Literacy Rate (%)')
plt.ylabel('Frequency')
for patch in ax.patches:
    height = patch.get_height()
    if height > 0:
        ax.text(patch.get_x() + patch.get_width() / 2,   
                height + 0.2,                             
                int(height),                             
                ha='center', fontsize=9, color='black')

plt.show()






# Objective 2:- To compare male and female literacy rates statistically using t-tests and visualize disparities through bar charts


print("Descriptive Statistics for Literacy Rate (%):")
state_data['Male_Literacy_Rate'] = (state_data['Literate_Males'] / state_data['Total_Males']) * 100
state_data['Female_Literacy_Rate'] = (state_data['Literate_Females'] / state_data['Total_Females']) * 100
#checking the both male and female literacy rate for normal distribution before t-testing
plt.figure(figsize=(12, 5))
# Histogram for Male Literacy Rate
plt.subplot(1, 2, 1)
sns.histplot(state_data['Male_Literacy_Rate'], kde=True, color='blue', bins=15)
plt.title('Histogram of Male Literacy Rate (%)')
plt.xlabel('Literacy Rate (%)')
plt.ylabel('Frequency')
# Histogram for Female Literacy Rate
plt.subplot(1, 2, 2)
sns.histplot(state_data['Female_Literacy_Rate'], kde=True, color='pink', bins=15)
plt.title('Histogram of Female Literacy Rate (%)')
plt.xlabel('Literacy Rate (%)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
#since from histplot , males literacy rate is not clear that it is normally distributed  or not. so we check shapiro test for males.
stat, p_value = shapiro(state_data['Male_Literacy_Rate'])
print(f"Statistic: {stat:.4f}")
print(f"P-value: {p_value:.4f}")
if p_value < 0.05:
    print("Conclusion: Male_Literacy_Rate is not normally distributed (reject H0).")
else:
    print("Conclusion: Male_Literacy_Rate is normally distributed (fail to reject H0).")

state_data.plot(x='State_Code', y=['Male_Literacy_Rate', 'Female_Literacy_Rate'], 
                kind='bar', figsize=(14,6))
plt.ylabel('Literacy Rate (%)')
plt.title('Comparison of Male and Female Literacy Rates by State')
plt.xticks(rotation=90)
plt.show()
#from picture we can see that male literacy rate is greater than female literacy rate . so we will perform paired t-test
t_stat, p_value = ttest_rel(state_data['Male_Literacy_Rate'], state_data['Female_Literacy_Rate'])
print(f"P-value: {p_value:.4f}")
if p_value < 0.05:
    print("Significant Difference in Literacy Rates.")
else:
    print("No Significant Difference in Literacy Rates.")
#form above test we conclude that diffrence between male and female ratio in india is significant.
state_data['Literacy_gap']=state_data['Male_Literacy_Rate']-state_data['Female_Literacy_Rate']
print(f"On average,  male literacy greater than female literacy data is:{state_data['Literacy_gap'].mean():.4f}")

#objective 3:- To identify relationships between primary, secondary, and higher education levels using correlation matrices and heatmaps.
education_data = state_data[['Edu_level_primary_persons', 'Edu_level_middle_persons', 'Edu_level_matric_or_secondary_persons', 'Edu_level_secondary_persons', 'Edu_level_non_techincal_persons','Edu_level_techincal_persons','Edu_level_gruduate_and_above_persons']]
education_data.rename(columns={
    'Edu_level_primary_persons': 'Primary',
    'Edu_level_middle_persons': 'Middle',
    'Edu_level_matric_or_secondary_persons': 'Matric',
    'Edu_level_secondary_persons': 'Secondary',
    'Edu_level_non_techincal_persons': 'Non-Tech',
    'Edu_level_techincal_persons': 'Technical',
    'Edu_level_gruduate_and_above_persons': 'Graduate'
}, inplace=True)
correlation_matrix = education_data.corr()
print("correlation Matrix:\n",correlation_matrix)
#heatmap 
plt.figure(figsize=(8,7))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Education Levels')
plt.show()

#objective 4:- To visualize how educational attainment progresses across age groups using stacked bar charts.

age_wise = data[(data['Total_or_Rural_or_Urban'] == 'Total') & 
                (data['Distt_Code'] == 0) & 
                (~data['Age_group'].isin(['All ages', 'Age not stated']))]
age_group_data = age_wise.groupby('Age_group')[['Edu_level_primary_persons', 'Edu_level_middle_persons',
                                                'Edu_level_matric_or_secondary_persons', 'Edu_level_secondary_persons',
                                                'Edu_level_non_techincal_persons', 'Edu_level_techincal_persons',
                                                'Edu_level_gruduate_and_above_persons']].sum()
education_data = age_group_data.rename(columns={
    'Edu_level_primary_persons': 'Primary',
    'Edu_level_middle_persons': 'Middle',
    'Edu_level_matric_or_secondary_persons': 'Matric',
    'Edu_level_secondary_persons': 'Secondary',
    'Edu_level_non_techincal_persons': 'Non-Tech',
    'Edu_level_techincal_persons': 'Technical',
    'Edu_level_gruduate_and_above_persons': 'Graduate+'
})

# Plot with Short Names
education_data.plot(kind='bar', stacked=True, figsize=(7,5))

plt.title('Age-Wise Education Progression Patterns')
plt.xlabel('Age Group')
plt.ylabel('Number of Persons')
plt.legend(loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
plt.show()


#objective 5:- To evaluate the statistical significance of urban-rural differences in graduate-level education using chi-square tests.
rural_graduate=data[(data['Distt_Code'] == 0) & (data['Age_group'] == 'All ages') & (data['Total_or_Rural_or_Urban'] == 'Rural')&(data['State_Code']!=0)]['Edu_level_gruduate_and_above_persons'].sum()
urban_graduate=data[(data['Distt_Code'] == 0) & (data['Age_group'] == 'All ages') & (data['Total_or_Rural_or_Urban'] == 'Urban')&(data['State_Code']!=0)]['Edu_level_gruduate_and_above_persons'].sum()
rural_total = data[(data['Distt_Code'] == 0) & (data['Age_group'] == 'All ages') & 
                   (data['Total_or_Rural_or_Urban'] == 'Rural') & 
                   (data['State_Code'] != 0)]['Total_Persons'].sum()

urban_total = data[(data['Distt_Code'] == 0) & (data['Age_group'] == 'All ages') & 
                   (data['Total_or_Rural_or_Urban'] == 'Urban') & 
                   (data['State_Code'] != 0)]['Total_Persons'].sum()
data_table= [[rural_graduate, rural_total - rural_graduate],
              [urban_graduate, urban_total - urban_graduate]]
chi2, p, dof, expected = chi2_contingency(data_table)

print("Chi-Square Value:", chi2)
print("P-Value:", p)
if p < 0.05:
    print("Significant difference in Graduate level education between Rural and Urban areas.")
else:
    print("No significant difference in Graduate level education between Rural and Urban areas.")

