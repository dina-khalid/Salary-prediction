import streamlit as st
import pickle
import numpy as np


def loadModel():
    '''

    :return:
    the model I saved before and the label transform for cols
    '''
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data= loadModel()


#declaring the label encoders and model
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_Employment = data['le_Employment']
le_surveyease = data['le_surveyease']
le_so = data['le_so']
le_OpSys=data['le_opSys']




def showPredictPage():
    '''
    Displays the prediction page

    '''
    st.title("Software Developer Salary Prediction")

    st.write("""### Enter your informations""")

    #Some informations labels
    Countries = ('United States',
                 'India',
                 'Germany',
                 'United Kingdom',
                 'Canada',
                 'France',
                 'Brazil',
                 'Poland',
                 'Netherlands',
                 'Spain',
                 'Australia',
                 'Italy',
                 'Russian Federation',
                 'Sweden',
                 'Switzerland',
                 'Turkey',
                 'Israel',
                 'Ukraine'
                 )

    Edducation = ('Master’s degree',
                  'Bachelor’s degree',
                  'post grad',
                  'less than a Bachelor')

    SurveyEase = ('Easy',
                  'Neither easy nor difficult',
                  'Difficult')

    Employment = ('Independent contractor, freelancer, or self-employed',
                  'Employed full-time',
                  'I prefer not to say',
                  'Employed part-time',
                  'Retired')

    SOComm = ('Yes, definitely',
              'Yes, somewhat',
              'Neutral',
              'No, not really',
              'No, not at all',
              'Not sure')

    System=('MacOS', 'Windows', 'Linux-based', 'BSD',
       'Windows Subsystem for Linux (WSL)','Other')

    language = ('Assembly', 'Bash/Shell/PowerShell', 'C', 'C#', 'C++', 'Dart',
                'Go', 'HTML/CSS', 'Haskell', 'Java', 'JavaScript', 'Julia',
                'Kotlin', 'Objective-C', 'PHP', 'Perl', 'Python', 'R', 'Ruby',
                'Rust', 'SQL', 'Scala', 'Swift', 'TypeScript', 'VBA')

    database = ('Cassandra', 'Couchbase', 'DynamoDB', 'Elasticsearch', 'Firebase',
                'IBM DB2', 'MariaDB', 'Microsoft SQL Server', 'MongoDB', 'MySQL',
                'Oracle', 'PostgreSQL', 'Redis', 'SQLite')



    #Display inputs fields
    country = st.selectbox("Country", Countries)

    edlevel = st.selectbox("Edducation Level", Edducation)

    experiance= st.slider("Years of experiance",0,40,3)

    age =  st.slider("Age",0,40,14)

    employmentStatus = st.selectbox("Employment status", Employment)

    firstAgeCod = st.slider("1st Age Code", 0, 60, 5)

    surveyEase = st.selectbox("Survey Ease", SurveyEase)

    soComm = st.selectbox("SOComm", SOComm)

    OpSys=st.selectbox("Operation System", System)
    if OpSys=="Other":
        OpSys="Other (please specify):"

    st.write("""Language worked with""")

    getlang=[st.checkbox(str(i)) for i in language]
    st.write("""Database worked with""")

    getdb= [st.checkbox(str(i)) for i in database]


    #change the value of input in database and language to lables that the model cen understand
    for i in range(len(getdb)):
        getdb[i] = 0 if getdb[i]== False else 1

    getdb = [int(i) for i in getdb]
    getlang = [int(i) for i in getlang]


    for i in range(len(getlang)):
        getlang[i] = 0 if getlang[i]== False else 1



    ok = st.button("Calculate Salary")




    if ok:
        #add the inpuut to an array
        X = [country, edlevel, experiance, age, employmentStatus,
             firstAgeCod, surveyEase,soComm,OpSys]

        #add the elements in datablse an language lists to X array
        for i in range(len(getlang)):
            X.append(getlang[i])
        for i in range(len(getdb)):
            X.append(getdb[i])
        X=np.array([X])


        #get the encoded label from the model
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X[:, 4] = le_Employment.transform(X[:, 4])
        X[:, 6] = le_surveyease.transform(X[:, 6])
        X[:, 7] = le_so.transform(X[:, 7])
        X[:, 8] = le_OpSys.transform(X[:, 8])

        X = X.astype(float)

        #predict the salary
        salary = regressor.predict(X)


        #print the Salary
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

