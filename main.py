import streamlit as st
import pandas as pd
import random

def get_data():
    people_data = pd.read_csv('data/people.csv')
    rating_data = pd.read_csv('data/ratings.csv')
    movies_data = pd.read_csv('data/movies.csv')

    people_and_movies = people_data[["userId", "first_name","last_name","gender","job","country","age","car"]].merge(
        rating_data[["userId","movieId","rating","timestamp"]], on="userId", how="left")

    all_data = pd.merge(people_and_movies, movies_data, how="left")

    stats = {'First_name':all_data['first_name'], 'Last_name':all_data['last_name'], 'Gender':all_data['gender'],
     'Country':all_data['country'], 'Job':all_data['job'], 'Car':all_data['car'], 'Age':all_data['age'], 
     'Title':all_data['title'], 'Genre':all_data['genres'], 'Rating':all_data['rating']}

    stats = pd.DataFrame.from_dict(stats)
    return stats
        
def choose_film_by_age(data, age):
    data_DF = pd.DataFrame(data)
    data = data_DF[data_DF['Age'] == age]
    movies_list = list(data['Title'])
    #data.to_excel('data.xlsx')
    return random.sample(movies_list, 5)

def choose_film_by_job(data, job):
    data_DF = pd.DataFrame(data)
    data = data_DF[data_DF['Job'] == job]
    movies_list = list(data['Title'])
    #data.to_excel('data.xlsx')
    #data.sample(n=5) #return random rows
    return random.sample(movies_list, 5) #return random elements without replacement, otherwise like choices

def choose_film_by_rating(data, genres, rating):
    data_DF = pd.DataFrame(data)
    data = data_DF[(data_DF['Genre'] == genres) & (data_DF['Rating'] >= rating)]
    movies_list = list(data['Title'])
    return random.sample(movies_list, 3)

#show data using streamlit
st.write(""" # DRAW BY LOT FILM ACCORDING TO GIVING DATA """)
col1, col2 = st.columns(2)
data = get_data()
with col1:
    with st.form(key='my-form-age'):
        age = st.number_input(label='Your age:', min_value=1, max_value=75, value=1, step=1)
        submit = st.form_submit_button('Submit')
        if submit:
            st.write(choose_film_by_age(data, age))

with col2:
    with st.form(key='my-form-job'):
        job = st.selectbox('Your job:', list(dict.fromkeys(data['Job']))) #dict.fromkeys() remove redundancy from list
        submit = st.form_submit_button('Submit')
        if submit:
            st.write(choose_film_by_job(data, job))

with st.form(key='my-form-rating'):
    genres = st.selectbox('Genre:', list(dict.fromkeys(data['Genre'])))
    rating = st.slider(label='Rating:', min_value=0.5, max_value=5.0, step=0.5)
    submit = st.form_submit_button('Submit')
    if submit:
        st.write(choose_film_by_rating(data, genres, rating))