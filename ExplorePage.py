import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def specializeCategories(categories,cutoff):
    '''
    A function that takes categories and cutoff number then
    return the categories which have elements more than the cutoff num
    and make the other categories in category "other"
    '''
    catigorical_map={}
    for i in range (len(categories)):
        if categories.values[i]>= cutoff:
            catigorical_map[categories.index[i]]=categories.index[i]
        else:
            catigorical_map[categories.index[i]]="other"
    return catigorical_map


def clean_experience(x):
    '''
    A function that change string values in experiance column to float
    :param x:
    experiance from the dataframe
    :return:
    float value of the experiance
    '''
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_edlevel(x):
    '''
    Takes education level and return cleaned categories
    '''
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Bachelor’s degree' in x:
        return "Bachelor’s degree"
    if 'Other doctoral' in x or 'Professional degree' in x:
        return 'post grad'
    return "less than a Bachelor"



def clean_age(x):
    '''

    :param x:
    range of age
    :return:
    number value
    '''
    if "25-34" in x:
        return 34
    if "35-44" in x:
        return 44
    if "45-54" in x:
        return 54
    if "18-24" in x:
        return 24
    if"55-64" in x:
        return 64
    if "65" in x:
        return 65
    if "18" in x:
        return 18
    if 'Prefer not to say' in x:
        return None


def clean_age1st(x):
    '''

    :param x:
    Age in the dataframe
    :return:
    number value
    '''
    if "64" in x:
        return 64
    elif '5' in x:
        return 5
    elif '11 - 17' in x:
        return 17
    elif '5 - 10' in x:
        return 10
    elif '25 - 34' in x:
        return 34
    elif '18 - 24' in x:
        return 24
    elif '35 - 44' in x:
        return 44
    elif '45 - 54' in x:
        return 54
    elif '55 - 64' in x:
        return 64

@st.cache
def loadData():
    '''
    load the data from the CSV file
    and cleaning it
    :returns:
    the cleaned dataframe
    '''
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Age", "Employment", "Age1stCode", "SurveyEase", 'SOComm',
             "ConvertedCompYearly"]]

    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()

    countryMap = specializeCategories(df.Country.value_counts(), 450)
    df["Country"] = df["Country"].map(countryMap)

    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != "other"]

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_edlevel)
    df['Age'] = df['Age'].apply(clean_age)
    df = df[df["Age"].notnull()]
    df['Age1stCode'] = df['Age1stCode'].apply(clean_age1st)

    return df

df=loadData()


def showExplorePage():

    '''
    Displaying Explore page
    '''
    st.title("Software Engineers salaries")
    st.write("""#### Data credits: Stack Overflow Developer Survey 2021""")

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)

    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
