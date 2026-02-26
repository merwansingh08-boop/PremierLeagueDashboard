import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("⚽ Premier League Historical Dashboard")


@st.cache_data
def load_data():

    df = pd.read_csv('final_data_2.csv')
    return df

df = load_data()


st.sidebar.header("Filter Options")

teams = df['HomeTeam'].unique()
selected_team = st.sidebar.selectbox("Select a Team", teams)


team_data = df[(df['HomeTeam'] == selected_team) | (df['AwayTeam'] == selected_team)]


st.subheader(f"Match History for {selected_team}")
st.dataframe(team_data)

st.subheader(f"Elo History for {selected_team}")
df['Date'] = pd.to_datetime(df['Date'])
data = []
total = []
for i in range(len(df)):
    if df.loc[i,'HomeTeam'] == selected_team:
        data.append(df.loc[i,'Date'])
        total.append(df.loc[i,'UpdatedHomeElo'])
    elif df.loc[i,'AwayTeam'] == selected_team:
        data.append(df.loc[i, 'Date'])
        total.append(df.loc[i,'UpdatedAwayElo'])



# 5. Sort by Date, then make the Date the "Index"
# Streamlit automatically uses the Index as the X-axis for line charts!
df_chart = pd.DataFrame({
    'Match Date': data,
    'Total Goals': total
})
st.line_chart(df_chart, x='Match Date', y='Total Goals')

st.subheader("Goals Scored by Home Teams")
if 'FTHG' in df.columns:
    fig, ax = plt.subplots()
    df.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).head(10).plot(kind='bar', ax=ax)
    plt.ylabel("Total Home Goals")
    st.pyplot(fig)
else:
    st.write("Column 'HomeGoals' not found. Update the code with your actual CSV column names.")
