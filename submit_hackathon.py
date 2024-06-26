# -*- coding: utf-8 -*-
"""submit hackathon.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dn4mJgL-M4tFwpvAkTQhYx32UUFimL8N

# Data bersih
"""

import pandas as pd
data = pd.read_csv('Diabetes_2019.csv')
display(data)

data.columns

import pandas as pd
data_ovs = pd.read_csv('Diabetes_2019_oversampling.csv')
display(data_ovs)

data.describe().T

"""# Start"""

# Standard imports
import numpy as np
import pandas as pd

# EDA imports
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
px_template = "simple_white"

# Sklearn imports
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.naive_bayes import GaussianNB, MultinomialNB

# Classifiers imports
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb

# Metrics imports
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score, precision_score
from sklearn.metrics import confusion_matrix, classification_report # plot_confusion_matrix

# Save models imports
from joblib import dump, load

"""## Deskripsi Singkat Data yang Digunakan dalam Notebook

Tujuan dari BRFSS adalah untuk mengumpulkan data yang seragam dan spesifik negara bagian mengenai praktik kesehatan pencegahan dan perilaku risiko yang terkait dengan penyakit kronis, cedera, dan penyakit menular yang dapat dicegah pada populasi dewasa. Faktor-faktor yang dinilai oleh BRFSS mencakup penggunaan tembakau, cakupan perawatan kesehatan, pengetahuan atau pencegahan HIV/AIDS, aktivitas fisik, dan konsumsi buah dan sayuran. Data dikumpulkan dari sampel acak orang dewasa (satu per rumah tangga) melalui survei telepon.

Behavioral Risk Factor Surveillance System (BRFSS) adalah sistem utama survei telepon terkait kesehatan yang mengumpulkan data negara bagian tentang penduduk AS terkait perilaku risiko kesehatan, kondisi kesehatan kronis, dan penggunaan layanan pencegahan. Didirikan pada tahun 1984 dengan 15 negara bagian, BRFSS kini mengumpulkan data di semua 50 negara bagian serta Distrik Columbia dan tiga wilayah AS. BRFSS menyelesaikan lebih dari 400.000 wawancara dewasa setiap tahun, menjadikannya sistem survei kesehatan yang berkelanjutan terbesar di dunia.

### Data mentah dari tahun 2019 dan deskripsinya dapat ditemukan di sini:
https://www.cdc.gov/brfss/annual_data/annual_2019.html

### Subset Fitur Terpilih dari BRFSS 2019

Dengan mempertimbangkan faktor risiko utama, saya mencoba memilih fitur (kolom/pertanyaan) dalam BRFSS yang terkait dengan faktor risiko diabetes. Untuk membantu memahami arti kolom, saya merujuk ke BRFSS 2019 Codebook untuk melihat pertanyaan dan informasi tentang pertanyaan tersebut. Saya mencoba mencocokkan nama variabel dalam buku kode dengan nama variabel dalam dataset. Saya juga merujuk beberapa fitur yang sama yang dipilih untuk makalah penelitian oleh Zidian Xie et al untuk Membangun Model Prediksi Risiko untuk Diabetes Tipe 2 Menggunakan Teknik Pembelajaran Mesin menggunakan data dari BRFSS 2014.

### Buku Kode BRFSS 2019:
https://www.cdc.gov/brfss/annual_data/2019/pdf/codebook19_llcp-v2-508.HTML

### Makalah Penelitian Terkait yang Menggunakan BRFSS untuk Pembelajaran Mesin Diabetes:
https://www.cdc.gov/pcd/issues/2019/19_0109.htm

****
### Tujuan

Tujuan utama dari notebook ini adalah untuk menjawab pertanyaan:

* **Bisakah pertanyaan survei dari BRFSS memberikan prediksi akurat tentang apakah seseorang menderita diabetes?**
****

**Fitur yang dipilih** dari dataset BRFSS 2019 adalah:

##### Variabel Respon / Variabel Dependen:
1. **Diabetes**
    * (Pernah diberitahu) (Anda memiliki) diabetes? (Jika 'Ya' dan responden adalah wanita, tanyakan 'Apakah ini hanya saat Anda hamil?'. Jika Responden mengatakan pradiabetes atau diabetes borderline, gunakan kode respon 4.) --> DIABETE4

##### Variabel Independen:

1. **Tekanan Darah Tinggi**
    * Orang dewasa yang telah diberitahu bahwa mereka memiliki tekanan darah tinggi oleh dokter, perawat, atau profesional kesehatan lainnya --> _RFHYPE5


2. **Kolesterol Tinggi**
    * Apakah Anda pernah diberitahu oleh dokter, perawat atau profesional kesehatan lainnya bahwa kolesterol darah Anda tinggi? --> TOLDHI2
    * Pemeriksaan kolesterol dalam lima tahun terakhir --> _CHOLCH2


3. **BMI**
    * Indeks Massa Tubuh (BMI) --> _BMI5


4. **Merokok**
    * Apakah Anda pernah merokok setidaknya 100 batang rokok dalam hidup Anda? [Catatan: 5 bungkus = 100 batang rokok] --> SMOKE100
    
    
5. **Konsumsi Alkohol**
    * Pemabuk berat (pria dewasa yang mengonsumsi lebih dari 14 minuman per minggu dan wanita dewasa yang mengonsumsi lebih dari 7 minuman per minggu) --> _RFDRHV7
    

6. **Diet**
    * Konsumsi buah 1 atau lebih kali per hari --> _FRTLT1A
    * Konsumsi sayuran 1 atau lebih kali per hari --> _VEGLT1A


7. **Kondisi Kesehatan Kronis Lainnya**
    * (Pernah diberitahu) (Anda memiliki) gangguan depresi (termasuk depresi, depresi mayor, distimia, atau depresi ringan)? --> ADDEPEV3
    * (Pernah diberitahu) (Anda memiliki) penyakit paru obstruktif kronis, PPOK, emfisema atau bronkitis kronis? --> CHCCOPD2
    * Status asma terhitung --> _ASTHMS1
    * (Pernah diberitahu) Anda mengalami stroke --> CVDSTRK3
    * (Pernah diberitahu) Anda mengalami serangan jantung, juga disebut infark miokard? --> CVDINFR4
    * (Pernah diberitahu) Anda mengalami angina atau penyakit jantung koroner? --> CVDCRHD4


8. **Aktivitas Fisik**
    * Orang dewasa yang melaporkan melakukan aktivitas fisik atau olahraga selama 30 hari terakhir selain pekerjaan rutin mereka --> _TOTINDA


9. **Perawatan Kesehatan**
    * Apakah ada saat dalam 12 bulan terakhir ketika Anda perlu menemui dokter tetapi tidak bisa karena biaya? --> MEDCOST
    * Apakah Anda memiliki jenis asuransi kesehatan apa pun, termasuk asuransi kesehatan, rencana prabayar seperti HMO, atau rencana pemerintah seperti Medicare, atau Indian Health Service? --> HLTHPLN1


10. **Kesehatan Umum dan Kesehatan Mental**
    * Apakah Anda akan mengatakan bahwa secara umum kesehatan Anda adalah: --> GENHLTH
    * Sekarang memikirkan tentang kesehatan mental Anda, yang mencakup stres, depresi, dan masalah emosi, selama berapa hari dalam 30 hari terakhir kesehatan mental Anda tidak baik? --> MENTHLTH
    * Sekarang memikirkan tentang kesehatan fisik Anda, yang mencakup penyakit fisik dan cedera, selama berapa hari dalam 30 hari terakhir kesehatan fisik Anda tidak baik? --> PHYSHLTH
    * Apakah Anda mengalami kesulitan serius berjalan atau menaiki tangga? --> DIFFWALK


11. **Demografi**
    * Kategori usia empat belas tingkat --> _AGEG5YR
    * Variabel jenis kelamin terhitung --> _SEX
    * Apa tingkat pendidikan tertinggi atau tahun sekolah yang Anda selesaikan? --> EDUCA
    * Kategori pendapatan --> _INCOMG

## Notebook organization:
* Convert data from a SAS format to CSV format
* Create datasets with selected variables
* Clean the data
	- Modify and clean the values to be more suitable to ML algorithms
* Create Binary Dataset for diabetes vs. no diabetes
* EDA
	- Information of variables
	- Correlation between variables
	- Visualization of relationships between variables
* Trening and test data
* Model selection and evaluation functions
* Baseline models
* Modelling
	- Logistic Regression
	- SVM
	- Decision Tree Classifier
	- Random Forest Classifier
	- XGBoost Classifier
* Metrics
* Oversampling dataset
	- New trening and test data
	- Decision Tree Classifier on the oversampled dataset
	- XGBoost Classifier on the oversampled dataset
	- Metrics
* Conclusions
* Discussion

# CREATE DATASET
"""

raw_df = pd.read_sas("LLCP2019.XPT")
raw_df.to_csv('LLCP2019.csv', sep=",", index=False)

BRFSS_2019 = pd.read_csv(r"LLCP2019.csv")
BRFSS_2019.shape

df = BRFSS_2019[['DIABETE4',
                 '_RFHYPE5',
                 'TOLDHI2', '_CHOLCH2',
                 '_BMI5',
                 'SMOKE100', '_RFDRHV7',
                 '_FRTLT1A', '_VEGLT1A',
                 'ADDEPEV3', 'CHCCOPD2', '_ASTHMS1', 'CVDSTRK3', 'CVDINFR4', 'CVDCRHD4',
                 '_TOTINDA',
                 'MEDCOST', 'HLTHPLN1',
                 'GENHLTH', 'MENTHLTH', 'PHYSHLTH', 'DIFFWALK',
                 '_AGEG5YR', '_SEX', 'EDUCA', '_INCOMG']].astype(float)
df.head()

df.shape

df.describe().T

"""# CLEAN DATASET

##  1 , 2, 3, 4
  ## 1. Missing value

  ## 2. Drop Duplicates

  ## 3. Modify the data

  ## 4. Check unique value
"""

# 1. drop missing value
df = df.dropna()
df.shape

df.isnull().sum()


# 2. drop duplicates
df = df.drop_duplicates()
df.shape


# Modify and clean the values to be more suitable to ML algorithms
def CleanDiabete(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 was no diabetes or only during pregnancy,
         - 1 is prediabetes or borderline diabetes,
         - 2 is a diabetic respondent
    '''

    df.drop(df[(df["DIABETE4"] == 7) | (df["DIABETE4"] == 9)].index, inplace=True)
    df['DIABETE4'] = [0 if (x == 2 or x == 3) else (1 if x == 4 else 2) for x in df['DIABETE4']]
    return df

def CleanHighBlood(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent without high blood pressure,
         - 1 is the respondent with high blood pressure
    '''

    df.drop(df[(df["_RFHYPE5"] == 9)].index, inplace=True)
    df['_RFHYPE5'] = [0 if x == 1 else 1 for x in df['_RFHYPE5']]
    return df

def CleanCholAware(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the doctor never told the respondent that he had high cholesterol,
         - 1 is the doctor told the respondent that he had high cholesterol
    '''

    df.drop(df[(df["TOLDHI2"] == 7) | (df["TOLDHI2"] == 9)].index, inplace=True)
    df['TOLDHI2'] = [0 if x == 2 else 1 for x in df['TOLDHI2']]
    return df

def CleanCholCheck(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent did not check the cholesterol level in the last 5 years,
         - 1 is the respondent checked the level of cholesterol in the last 5 years
    '''

    df.drop(df[(df["_CHOLCH2"] == 9)].index, inplace=True)
    df['_CHOLCH2'] = [0 if (x == 2 or x == 3) else 1 for x in df['_CHOLCH2']]
    return df

def CleanBMI(df):
    '''Change the BMI value to the classic scale from 1 to 100 and convert the values into categories.
         - 1 is Underweight (BMI less then 18.5)
         - 2 is Normal Weight (BMI between 18.5–24.9)
         - 3 is Overweight (BMI between 25 - 29.9)
         - 4 is Obesity I degree (BMI between 30–34,9)
         - 5 is Obesity II degree (BMI between 35–39.9)
         - 6 is Obesity III degree (BMI 40 and more)
    '''

    df['_BMI5'] = df['_BMI5'].div(100).round(1)
    df.loc[df['_BMI5'] < 18.5, '_BMI5'] = 1.0
    df.loc[(df['_BMI5'] >= 18.5) & (df['_BMI5'] <= 24.9), '_BMI5'] = 2.0
    df.loc[(df['_BMI5'] >= 25) & (df['_BMI5'] <= 29.9), '_BMI5'] = 3.0
    df.loc[(df['_BMI5'] >= 30) & (df['_BMI5'] <= 34.9), '_BMI5'] = 4.0
    df.loc[(df['_BMI5'] >= 35) & (df['_BMI5'] <= 39.9), '_BMI5'] = 5.0
    df.loc[df['_BMI5'] >= 40, '_BMI5'] = 6.0
    return df

def CleanSmoke(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent does not smoke cigarettes,
         - 1 is the respondent smokes cigarettes
    '''

    df.drop(df[(df["SMOKE100"] == 7) | (df["SMOKE100"] == 9)].index, inplace=True)
    df['SMOKE100'] = [0 if x == 2 else 1 for x in df['SMOKE100']]
    return df

def CleanAlcohol(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent does not abuse alcohol,
         - 1 is the respondent is abusing alcohol
    '''

    df.drop(df[(df["_RFDRHV7"] == 9)].index, inplace=True)
    df['_RFDRHV7'] = [0 if x == 1 else 1 for x in df['_RFDRHV7']]
    return df

def CleanFruit(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent consumed less than 1 fruit time per day,
         - 1 is the respondent consumed 1 or more pieces of fruit per day
    '''

    df.drop(df[(df["_FRTLT1A"] == 9)].index, inplace=True)
    df['_FRTLT1A'] = [0 if x == 2 else 1 for x in df['_FRTLT1A']]
    return df

def CleanVegetable(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent consumed less than 1 vegetables time per day,
         - 1 is the respondent consumed 1 or more pieces of vegetables per day
    '''

    df.drop(df[(df["_VEGLT1A"] == 9)].index, inplace=True)
    df['_VEGLT1A'] = [0 if x == 2 else 1 for x in df['_VEGLT1A']]
    return df

def CleanDepress(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent had no depressive disorder,
         - 1 is the respondent had depressive disorders
    '''

    df.drop(df[(df["ADDEPEV3"] == 7) | (df["ADDEPEV3"] == 9)].index, inplace=True)
    df['ADDEPEV3'] = [0 if x == 2 else 1 for x in df['ADDEPEV3']]
    return df

def CleanCOPD(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent had no chronic obstructive pulmonary disease,
         - 1 is the respondent had chronic obstructive pulmonary disease
    '''

    df.drop(df[(df["CHCCOPD2"] == 7) | (df["CHCCOPD2"] == 9)].index, inplace=True)
    df['CHCCOPD2'] = [0 if x == 2 else 1 for x in df['CHCCOPD2']]
    return df

def CleanAsthma(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent never had asthma,
         - 1 is the respondent currently has asthma,
         - 2 is the respondent had asthma in the past
    '''

    df.drop(df[(df["_ASTHMS1"] == 7) | (df["_ASTHMS1"] == 9)].index, inplace=True)
    df['_ASTHMS1'] = [0 if x == 3 else (1 if x == 1 else 2) for x in df['_ASTHMS1']]
    return df

def CleanStroke(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent did not have a stroke,
         - 1 is the respondent had a stroke
    '''

    df.drop(df[(df["CVDSTRK3"] == 7) | (df["CVDSTRK3"] == 9)].index, inplace=True)
    df['CVDSTRK3'] = [0 if x == 2 else 1 for x in df['CVDSTRK3']]
    return df

def CleanHeartAttack(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent did not have a heart attack,
         - 1 is the respondent had a heart attack
    '''

    df.drop(df[(df["CVDINFR4"] == 7) | (df["CVDINFR4"] == 9)].index, inplace=True)
    df['CVDINFR4'] = [0 if x == 2 else 1 for x in df['CVDINFR4']]
    return df

def CleanCoronaryHeart(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent did not have a coronary heart disease,
         - 1 is the respondent had a coronary heart disease
    '''

    df.drop(df[(df["CVDCRHD4"] == 7) | (df["CVDCRHD4"] == 9)].index, inplace=True)
    df['CVDCRHD4'] = [0 if x == 2 else 1 for x in df['CVDCRHD4']]
    return df

def CleanPhysicalActivity(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent who have reported physical activity or exercise in the last 30 days,
         - 1 is the respondent who have not reported physical activity or exercise in the last 30 days
    '''

    df.drop(df[(df["_TOTINDA"] == 9)].index, inplace=True)
    df['_TOTINDA'] = [0 if x == 2 else 1 for x in df['_TOTINDA']]
    return df

def CleanMedCost(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent who could not afford an appointment with a doctor in the last 12 months,
         - 1 is the respondent who could afford a visit to a doctor in the last 12 months, regardless of the costs
    '''

    df.drop(df[(df["MEDCOST"] == 7) | (df["MEDCOST"] == 9)].index, inplace=True)
    df['MEDCOST'] = [0 if x == 2 else 1 for x in df['MEDCOST']]
    return df

def CleanHealthCare(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent who does not have any health insurance,
         - 1 is the respondent who has any health insurance
    '''

    df.drop(df[(df["HLTHPLN1"] == 7) | (df["HLTHPLN1"] == 9)].index, inplace=True)
    df['HLTHPLN1'] = [0 if x == 2 else 1 for x in df['HLTHPLN1']]
    return df

def CleanGeneralHealth(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 1 is the respondent feels excellent
         - 2 is the respondent feels very good
         - 3 is the respondent feels good
         - 4 is the respondent feels fair
         - 5 is the respondent feels pood
    '''

    df.drop(df[(df["GENHLTH"] == 7) | (df["GENHLTH"] == 9)].index, inplace=True)
    return df

def CleanMental(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent who has not had a single day of poor mental health in the last 30 days,
         - each subsequent number represents the number of days the respondent felt mentally unwell in the last 30 days
    '''

    df.drop(df[(df["MENTHLTH"] == 77) | (df["MENTHLTH"] == 99)].index, inplace=True)
    df['MENTHLTH'] = df['MENTHLTH'].replace({88:0})
    return df

def CleanPhysical(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent who has not had a single day of poor physical health in the last 30 days,
         - each subsequent number represents the number of days the respondent felt physically unwell in the last 30 days
    '''

    df.drop(df[(df["PHYSHLTH"] == 77) | (df["PHYSHLTH"] == 99)].index, inplace=True)
    df['PHYSHLTH'] = df['PHYSHLTH'].replace({88:0})
    return df

def CleanDiffWalk(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is the respondent has no difficulty walking,
         - 1 is the respondent has difficulty walking
    '''

    df.drop(df[(df["DIFFWALK"] == 7) | (df["DIFFWALK"] == 9)].index, inplace=True)
    df['DIFFWALK'] = [0 if x == 2 else 1 for x in df['DIFFWALK']]
    return df

def CleanSex(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 0 is Female,
         - 1 is Male
    '''

    df['_SEX'] = [0 if x == 2 else 1 for x in df['_SEX']]
    return df

def CleanAge(df):
    '''Removes values that are of no use to the later predictions. Age in five-year age categories.
       Organizing data so that:
         - 1 is 18-24
         - 13 is 80 and older,
    '''

    df.drop(df[(df["_AGEG5YR"] == 14)].index, inplace=True)
    return df

def CleanEducation(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 1 is the respondent never attended school or kindergarten
         - 2 is the respondent completed elementary school
         - 3 is the respondent attended some high school
         - 4 is the respondent graduated from high school
         - 5 is the respondent attended some college or technical college
         - 6 is the respondent graduated from college
    '''

    df.drop(df[(df["EDUCA"] == 9)].index, inplace=True)
    return df

def CleanIncome(df):
    '''Removes values that are of no use to the later predictions.
       Organizing data so that:
         - 1 is the respondent earns less than $ 15,000 per year
         - 2 is the respondent earns between $ 15,000 and $ 25,000 per year
         - 3 is the respondent earns between $ 25,000 and $ 35,000 per year
         - 4 is the respondent earns between $ 35,000 and $ 50,000 per year
         - 5 is the respondent earns more than $ 50,000 per year
    '''

    df.drop(df[(df["_INCOMG"] == 9)].index, inplace=True)
    return df

CleanDiabete(df);
CleanHighBlood(df);
CleanCholAware(df);
CleanCholCheck(df);
CleanBMI(df);
CleanSmoke(df);
CleanAlcohol(df);
CleanFruit(df);
CleanVegetable(df);
CleanDepress(df);
CleanCOPD(df);
CleanAsthma(df);
CleanStroke(df);
CleanHeartAttack(df);
CleanCoronaryHeart(df);
CleanPhysicalActivity(df);
CleanMedCost(df);
CleanHealthCare(df);
CleanGeneralHealth(df);
CleanMental(df);
CleanPhysical(df);
CleanDiffWalk(df);
CleanSex(df);
CleanAge(df);
CleanEducation(df);
CleanIncome(df);
print('finish')

df.shape

# 4. check unique value

unique_values = {}
for col in df.columns:
    unique_values[col] =df[col].value_counts().shape[0]

pd.DataFrame(unique_values, index=['unique value count']).transpose()

"""## 5. Make feature names more readable"""

data = df.rename(columns = {'DIABETE4':'Diabetes',
                            '_RFHYPE5':'HighBloodPressure',
                            'TOLDHI2':'HighCholesterol', '_CHOLCH2':'CholesterolChecked',
                            '_BMI5':'BMI',
                            'SMOKE100':'Smoker', '_RFDRHV7':'HeavyAlcoholConsumption',
                            '_FRTLT1A':'Fruits', '_VEGLT1A':"Vegetables",
                            'ADDEPEV3':'DepressiveDisorded', 'CHCCOPD2':'ChronicOPD', '_ASTHMS1':'Asthma',
                            'CVDSTRK3':'Stroke', 'CVDINFR4':'HeartAttack', 'CVDCRHD4':'CoronaryHeartDisease',
                            '_TOTINDA':'PhysicalActivity',
                            'MEDCOST':'TreatmentCostTooHigh', 'HLTHPLN1':'HealthCareCoverage',
                            'GENHLTH':'GeneralHealth', 'MENTHLTH':'MentallHealth',
                            'PHYSHLTH':'PhysicalHealth', 'DIFFWALK':'DifficultyWalking',
                            '_AGEG5YR':'Age', '_SEX':'Sex', 'EDUCA':'Education', '_INCOMG':'Income'
                           }).astype(int)
data.head()

"""## 6. Handling Imbalanced Data"""

data.groupby(['Diabetes']).size()

diabetes_counts = df['Diabetes'].value_counts().reset_index()
diabetes_counts.columns = ['Diabetes', 'Count']

# Membuat plot batang menggunakan Plotly
fig = px.bar(diabetes_counts, x='Diabetes', y='Count', title='Distribution of Diabetes', labels={'Diabetes': 'Diabetes', 'Count': 'Count'})

# Menampilkan plot
fig.show()

import plotly.express as px

# make binary dataset
data_binary = data
data_binary['Diabetes'] = data_binary['Diabetes'].replace({2:1})
data_binary = data_binary.rename(columns = {'Diabetes': 'Diabetes_01'}).reset_index(drop=True)
data_binary.Diabetes_01.unique()

data_binary.groupby(['Diabetes_01']).size()


counts = data_binary['Diabetes_01'].value_counts().reset_index()
counts.columns = ['Diabetes', 'Count']
figure = px.bar(counts, x='Diabetes', y='Count', title='Diabetes Disease Frequency', labels={'Diabetes': 'Diabetes', 'Count': 'Frequency'})
figure.show()

class_0 = data_binary[data_binary['Diabetes_01'] == 0]
class_1 = data_binary[data_binary['Diabetes_01'] == 1]

class_1_over = class_1.sample(len(class_0), replace=True)
data_binary_over = pd.concat([class_1_over, class_0], axis=0)

data_binary_over.groupby(['Diabetes_01']).size()

counts = data_binary_over['Diabetes_01'].value_counts().reset_index()
counts.columns = ['Diabetes', 'Count']
figure = px.bar(counts, x='Diabetes', y='Count', title='Diabetes Disease Frequency', labels={'Diabetes': 'Diabetes', 'Count': 'Frequency'})
figure.show()

data_binary_over.to_csv('Diabetes2019-oversampling.csv')

"""# Exploratory Data Analysis (EDA)"""

# for this section, i used data_binary dataframe and didn't use data_binary_over dataframe

data_binary.info()

data_binary.hist(figsize=(20,15));

# Creat mask
mask = np.zeros_like(data_binary.corr())
mask[np.triu_indices_from(mask)] = True
# Heatmap of correlation
plt.figure(figsize = (20,15))
sns.heatmap(data_binary.corr(), mask=mask, annot=True, cmap ='PuOr', square=False, linewidths=0.5, fmt=".2f", center=0)
plt.title("Correlation of all features")
plt.show()

data_binary.drop('Diabetes_01', axis=1).corrwith(data_binary.Diabetes_01).plot(
    kind='bar', grid=True, figsize=(20, 10),
    title="Correlation between the Diabetes and all independent variables",color="green");

"""# Building Models

## Training and testing data
"""

y_over = data_binary_over.Diabetes_01
# Features
X_over = data_binary_over.drop(['Diabetes_01'], axis=1)

# Splitting the features and label into train and test with test size = 20% and train size = 80%
X_over_train, X_over_test, y_over_train, y_over_test = train_test_split(X_over, y_over, test_size = 0.2, random_state = 0)

# Shape of train and test sets
print('Oversampled X_train:', X_over_train.shape, 'Oversampled X_test:', X_over_test.shape)
print('Oversampled y_train:', y_over_train.shape, 'Oversampled y_test:', y_over_test.shape)

"""## Making 2 function : OPTIMIZE MODEL and EVALUATE MODEL"""

# function for tuning hyperparams of a classifiers

X_train = []
y_train = []

X_test = []
y_test = []
def optimize_model(model, param_grid, cv = 5, X_train = X_train, y_train = y_train):
    '''Performs grid search over param_grid with cv-fold cross validation.

    Function arguments:
        model: sklearn classifier
        param_grid (dict): parameters grid
        cv (int): number of folds in cross validation
        X_train (array): training set
        y_train (array): training labels

    Returns:
        Best model found, fitted on the entire data set.
    '''

    optimizer = GridSearchCV(model, param_grid = param_grid, scoring="accuracy", cv = cv, n_jobs = 1, verbose = True)
    optimizer.fit(X_train, y_train)
    print('Best parameters found:')
    print(optimizer.best_params_)
    print('\nBest score: %0.6f' % (optimizer.best_score_))

    return optimizer.best_estimator_

# function to evalute tuned models on the test set

def evaluate_model(model, X_test = X_test, y_test = y_test):
    '''
    Function arguments:
        model: fitted sklearn classifier
        X_test (array): testing set
        y_test (array): testing labels
    '''

    y_pred = model.predict(X_test)
    print('\nClassification report: ')
    print(classification_report(y_test, y_pred))

"""## Decision Tree Classifier on the oversampled dataset"""

# create a pipeline
tree_model_over = Pipeline([("scaler", StandardScaler()), ("model", DecisionTreeClassifier())])

# create parameter grids
tree_over_param_grid = {'model__criterion': ['gini', 'entropy'],
                        'model__max_depth': [2, 5, 10, 20, 30],
                        'model__min_samples_leaf': [5, 10, 20, 30]}

# -------------------------------------------------------------------------------------

#%%time

tree_model_over = optimize_model(tree_model_over, tree_over_param_grid,
                                 X_train = X_over_train, y_train = y_over_train)
evaluate_model(tree_model_over, X_test = X_over_test, y_test = y_over_test)

#%%time

tree_model_over = Pipeline([("scaler", StandardScaler()), ("model", DecisionTreeClassifier(criterion = 'entropy'))])
tree_over_param_grid = {'model__max_depth': [30, 50, 100],
                        'model__min_samples_leaf': [2, 5, 7, 10]}
tree_model_over = optimize_model(tree_model_over, tree_over_param_grid,
                                 X_train = X_over_train, y_train = y_over_train)
evaluate_model(tree_model_over, X_test = X_over_test, y_test = y_over_test)

#%%time

tree_model_over = Pipeline([("scaler", StandardScaler()), ("model", DecisionTreeClassifier(criterion = 'entropy'))])
tree_over_param_grid = {'model__max_depth': np.arange(50,100,1),
                        'model__min_samples_leaf': [1, 2, 3]}
tree_model_over = optimize_model(tree_model_over, tree_over_param_grid,
                                 X_train = X_over_train, y_train = y_over_train)
evaluate_model(tree_model_over, X_test = X_over_test, y_test = y_over_test)

# Melatih model menggunakan data latih
tree_model_over.fit(X_over_train, y_over_train)

# Membuat prediksi menggunakan data uji
y_pred = tree_model_over.predict(X_over_test)
cm = confusion_matrix(y_over_test, y_pred)

# Menampilkan confusion matrix menggunakan seaborn
plt.figure(figsize=(5, 3))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted label')
plt.ylabel('Actual label')
plt.show()

dump(tree_model_over, 'tree_model_oversampled.joblib');

"""## XGBooster Classifier on the oversampled dataset"""

# create a pipeline
xgb_model_over = Pipeline([("scaler", StandardScaler()), ("model", xgb.XGBClassifier(eval_metric = 'error'))])

# create parameter grids
xgb_over_param_grid  = {'model__n_estimators': [200, 400, 800],
                        'model__max_depth': [5, 10, 20],
                        'model__learning_rate': [0.05, 0.1, 0.2],
                        'model__min_child_weight': [1, 10, 100]}

##%%time

xgb_model_over = optimize_model(xgb_model_over, xgb_over_param_grid,
                                 X_train = X_over_train, y_train = y_over_train)
evaluate_model(xgb_model_over, X_test = X_over_test, y_test = y_over_test)

#%%time

xgb_model_over = Pipeline([("scaler", StandardScaler()), ("model", xgb.XGBClassifier(eval_metric = 'error',
                                                                                     min_child_weight = 1))])
xgb_over_param_grid  = {'model__n_estimators': [600, 800, 1000],
                        'model__max_depth': [20, 50],
                        'model__learning_rate': [0.2, 0.5]}
xgb_model_over = optimize_model(xgb_model_over, xgb_over_param_grid,
                                 X_train = X_over_train, y_train = y_over_train)
evaluate_model(xgb_model_over, X_test = X_over_test, y_test = y_over_test)

#%%time

xgb_model_over = Pipeline([("scaler", StandardScaler()), ("model", xgb.XGBClassifier(eval_metric = 'error',
                                                                                     min_child_weight = 1,
                                                                                     learning_rate = 0.2))])
xgb_over_param_grid  = {'model__n_estimators': [700, 800, 900],
                        'model__max_depth': [50, 100]}
xgb_model_over = optimize_model(xgb_model_over, xgb_over_param_grid,
                                 X_train = X_over_train, y_train = y_over_train)
evaluate_model(xgb_model_over, X_test = X_over_test, y_test = y_over_test)

# Melatih model menggunakan data latih
xgb_model_over.fit(X_over_train, y_over_train)

# Membuat prediksi menggunakan data uji
y_pred = xgb_model_over.predict(X_over_test)
cm = confusion_matrix(y_over_test, y_pred)

# Menampilkan confusion matrix menggunakan seaborn
plt.figure(figsize=(5, 3))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted label')
plt.ylabel('Actual label')
plt.show()

dump(xgb_model_over, 'xgb_model_oversampled.joblib');

"""# Metrics"""

from sklearn import metrics
model_name = []
accuracy_score = []
f1_score = []
roc_auc_score = []
recall_score = []
precision_score = []

def metrics_models(name, model, X_test = X_test, y_test = y_test):
    models = list()
    models.append((name, model))

    for name, model in models:
        model_name.append(name)
        accuracy_score.append(metrics.accuracy_score(y_test, model.predict(X_test)))
        f1_score.append(metrics.f1_score(y_test, model.predict(X_test)))
        roc_auc_score.append(metrics.roc_auc_score(y_test, model.predict(X_test)))
        recall_score.append(metrics.recall_score(y_test, model.predict(X_test)))
        precision_score.append(metrics.precision_score(y_test, model.predict(X_test)))

metrics_models('DecisionTreeClassifier Oversampled', tree_model_over,
                    X_test = X_over_test, y_test = y_over_test)
metrics_models('XGBoostClassifier Oversampled', xgb_model_over,
                    X_test = X_over_test, y_test = y_over_test)

metrics_df = pd.DataFrame({'Model': model_name,
                           'Accuracy': accuracy_score,
                           'F1-score': f1_score,
                           'AUC': roc_auc_score,
                           'Recall': recall_score,
                           'Precision': precision_score})

metrics_df