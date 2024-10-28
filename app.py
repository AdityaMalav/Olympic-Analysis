import streamlit as st
import pandas as pd
import  preprocessor, helper
import  plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import streamlit as st
import pandas as pd
import  preprocessor, helper
import  plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import streamlit as st
import pandas as pd
import  preprocessor, helper
import  plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff




df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df , region_df)

st.set_page_config(page_title="Aditya Olympic Analysis", page_icon="🏆", layout="wide")

# css = f"""
#      <style>
#      .stApp {{
#          background-image: url("https://cdn.pixabay.com/photo/2016/10/22/01/54/wood-1759566_1280.jpg");
#          background-attachment: fixed;
#          background-size: cover
#      }}
#      </style>
#      """
# st.markdown(css, unsafe_allow_html=True)


# _______________________________________________________________________________________

st.sidebar.image('pngwing.com (1).png')
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio('Select an Option',
                             ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis'))






### Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.coutry_year_list(df)

    select_year = st.sidebar.selectbox('Select Year', years)
    select_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally( df,select_year, select_country)

    if select_year == 'Overall' and select_country == 'Overall':
        st.title('Overall Tally')
    if select_year != 'Overall' and select_country == 'Overall':
        st.title('Medal Tally in ' + str(select_year) + ' Olympics')
    if select_year == 'Overall' and select_country != 'Overall':
        st.title(select_country + ' overall performance')
    if select_year != 'Overall' and select_country != 'Overall':
            st.title(select_country + ' performance in ' + str(select_year) + ' Olympics')

    st.table(medal_tally)



### Overall Analysis
if user_menu == 'Overall Analysis':
    year = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    Event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(year)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(Event)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    st.text("_________________________________________________________________________________________________________________")


    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)


    st.title('No. of Events over time(Every Sport)')
    fig, ax = plt.subplots(figsize= (20,20)   )
    x = df.drop_duplicates(['Year', "Sport", 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0), annot=True)
    st.pyplot(fig)


    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)





### Countrywise Analysis
if user_menu=='Country-wise Analysis':

    #1.
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',  country_list )

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y="Medal")
    st.title(selected_country + 'Medal Tally over the years')
    st.plotly_chart(fig)


    #2.
    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_headmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    #3.
    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countywise(df, selected_country)
    st.table(top10_df)





### Athleteswise Analysis
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Broze Medalist'],
                       show_hist=False, show_rug=False)
    fig.update_layout( autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)


    #-----
    x = []
    name = []
    famous_sports = [ 'Weightlifting', 'Cycling', 'Rowing', 'Sailing', 'Diving', 'Modern Pentathlon', 'Art Competitions',
                     'Synchronized Swimming', 'Handball', 'Canoeing', 'Table Tennis',
                     'Tennis', 'Taekwondo', 'Beach Volleyball', 'Trampolining', 'Golf', 'Equestrianism',
                     'Figure Skating', 'Rugby', 'Rugby Sevens', 'Cricket'
                     ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout( autosize=False, width=1000, height=600)
    st.title('Distribution of Age with respect to Sports(Gold Medalist)')
    st.plotly_chart(fig)


    #------

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'])

    st.pyplot(fig)



    #------
    st.title('Men Vs Women Paticipation Over the Years ')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout( autosize=False, width=1000, height=600)

    st.plotly_chart(fig)








df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df , region_df)

st.set_page_config(page_title="Aditya Olympic Analysis", page_icon="🏆", layout="wide")

# css = f"""
#      <style>
#      .stApp {{
#          background-image: url("https://cdn.pixabay.com/photo/2016/10/22/01/54/wood-1759566_1280.jpg");
#          background-attachment: fixed;
#          background-size: cover
#      }}
#      </style>
#      """
# st.markdown(css, unsafe_allow_html=True)


# _______________________________________________________________________________________

st.sidebar.image('pngwing.com (1).png')
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio('Select an Option',
                             ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis'))






### Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.coutry_year_list(df)

    select_year = st.sidebar.selectbox('Select Year', years)
    select_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally( df,select_year, select_country)

    if select_year == 'Overall' and select_country == 'Overall':
        st.title('Overall Tally')
    if select_year != 'Overall' and select_country == 'Overall':
        st.title('Medal Tally in ' + str(select_year) + ' Olympics')
    if select_year == 'Overall' and select_country != 'Overall':
        st.title(select_country + ' overall performance')
    if select_year != 'Overall' and select_country != 'Overall':
            st.title(select_country + ' performance in ' + str(select_year) + ' Olympics')

    st.table(medal_tally)



### Overall Analysis
if user_menu == 'Overall Analysis':
    year = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    Event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(year)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(Event)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    st.text("_________________________________________________________________________________________________________________")


    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)


    st.title('No. of Events over time(Every Sport)')
    fig, ax = plt.subplots(figsize= (20,20)   )
    x = df.drop_duplicates(['Year', "Sport", 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0), annot=True)
    st.pyplot(fig)


    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)





### Countrywise Analysis
if user_menu=='Country-wise Analysis':

    #1.
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',  country_list )

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y="Medal")
    st.title(selected_country + 'Medal Tally over the years')
    st.plotly_chart(fig)


    #2.
    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_headmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    #3.
    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countywise(df, selected_country)
    st.table(top10_df)





### Athleteswise Analysis
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Broze Medalist'],
                       show_hist=False, show_rug=False)
    fig.update_layout( autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)


    #-----
    x = []
    name = []
    famous_sports = [ 'Weightlifting', 'Cycling', 'Rowing', 'Sailing', 'Diving', 'Modern Pentathlon', 'Art Competitions',
                     'Synchronized Swimming', 'Handball', 'Canoeing', 'Table Tennis',
                     'Tennis', 'Taekwondo', 'Beach Volleyball', 'Trampolining', 'Golf', 'Equestrianism',
                     'Figure Skating', 'Rugby', 'Rugby Sevens', 'Cricket'
                     ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout( autosize=False, width=1000, height=600)
    st.title('Distribution of Age with respect to Sports(Gold Medalist)')
    st.plotly_chart(fig)


    #------

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'])

    st.pyplot(fig)



    #------
    st.title('Men Vs Women Paticipation Over the Years ')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout( autosize=False, width=1000, height=600)

    st.plotly_chart(fig)








df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df , region_df)

st.set_page_config(page_title="Aditya Olympic Analysis", page_icon="🏆", layout="wide")

# css = f"""
#      <style>
#      .stApp {{
#          background-image: url("https://cdn.pixabay.com/photo/2016/10/22/01/54/wood-1759566_1280.jpg");
#          background-attachment: fixed;
#          background-size: cover
#      }}
#      </style>
#      """
# st.markdown(css, unsafe_allow_html=True)


# _______________________________________________________________________________________

st.sidebar.image('pngwing.com (1).png')
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio('Select an Option',
                             ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis'))






### Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.coutry_year_list(df)

    select_year = st.sidebar.selectbox('Select Year', years)
    select_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally( df,select_year, select_country)

    if select_year == 'Overall' and select_country == 'Overall':
        st.title('Overall Tally')
    if select_year != 'Overall' and select_country == 'Overall':
        st.title('Medal Tally in ' + str(select_year) + ' Olympics')
    if select_year == 'Overall' and select_country != 'Overall':
        st.title(select_country + ' overall performance')
    if select_year != 'Overall' and select_country != 'Overall':
            st.title(select_country + ' performance in ' + str(select_year) + ' Olympics')

    st.table(medal_tally)



### Overall Analysis
if user_menu == 'Overall Analysis':
    year = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    Event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(year)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(Event)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    st.text("_________________________________________________________________________________________________________________")


    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)


    st.title('No. of Events over time(Every Sport)')
    fig, ax = plt.subplots(figsize= (20,20)   )
    x = df.drop_duplicates(['Year', "Sport", 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0), annot=True)
    st.pyplot(fig)


    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)





### Countrywise Analysis
if user_menu=='Country-wise Analysis':

    #1.
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',  country_list )

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y="Medal")
    st.title(selected_country + 'Medal Tally over the years')
    st.plotly_chart(fig)


    #2.
    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_headmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    #3.
    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countywise(df, selected_country)
    st.table(top10_df)





### Athleteswise Analysis
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Broze Medalist'],
                       show_hist=False, show_rug=False)
    fig.update_layout( autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)


    #-----
    x = []
    name = []
    famous_sports = [ 'Weightlifting', 'Cycling', 'Rowing', 'Sailing', 'Diving', 'Modern Pentathlon', 'Art Competitions',
                     'Synchronized Swimming', 'Handball', 'Canoeing', 'Table Tennis',
                     'Tennis', 'Taekwondo', 'Beach Volleyball', 'Trampolining', 'Golf', 'Equestrianism',
                     'Figure Skating', 'Rugby', 'Rugby Sevens', 'Cricket'
                     ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout( autosize=False, width=1000, height=600)
    st.title('Distribution of Age with respect to Sports(Gold Medalist)')
    st.plotly_chart(fig)


    #------

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'])

    st.pyplot(fig)



    #------
    st.title('Men Vs Women Paticipation Over the Years ')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout( autosize=False, width=1000, height=600)

    st.plotly_chart(fig)




