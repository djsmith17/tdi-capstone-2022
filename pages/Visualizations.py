import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualizations")

st.header('Video Game Recommendation Engine\nAuthor: Dante J. Smith, PhD')
st.markdown('### Visualizations of the Games included in the IGDB')

st.markdown(f'The IGDB contains entries for over **{len(st.session_state.GameDB)} video games!!**')

st.header('Game Themes')
st.bar_chart(data=st.session_state.themeCountD,  x='Themes', width = 500, height = 500)

st.header('Game Genres')
st.bar_chart(data=st.session_state.genreCountD,  x='Genres', width = 500, height = 500)

st.header('User Ratings vs Critic Ratings')
# scatDF = st.session_state.GameDB[['name', 'themes', 'genres', 'rating', 'aggregated_rating']]
# thisScat = scatDF['themes' == 1 & 'genres' == 2]

# Set up the Matplotlib figure
stBGColor = np.array([14, 17, 23])/255
stPTColor = np.array([131, 201, 255])/255
fig, ax = plt.subplots(figsize=(12, 12), dpi = 300, facecolor = stBGColor)

# A bunch of custom matplotlib to make this look pretty
fig.patch.set_alpha(1)
ax.set_facecolor(stBGColor)
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.set_xlabel('User Rating', fontsize=25, color = 'white')
ax.set_ylabel('Critic Rating', fontsize=25, color = 'white') 
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
ax.xaxis.set_ticks(np.linspace(0,100,11))
ax.yaxis.set_ticks(np.linspace(0,100,11))  
ax.tick_params(axis='both', which='major', labelsize=16, colors = 'white')
ax.grid(which='both')

# Set up the annotation
annot_x = (plt.xlim()[1] + plt.xlim()[0])/2
annot_y = (plt.ylim()[1] + plt.ylim()[0])/2
txt = ax.text(annot_x, annot_y, "Chart Ready", 
              ha='center', fontsize=36, color='#DD4012')

#define definition
def hover(event):
    txt.set_text("")
fig.canvas.mpl_connect("motion_notify_event", hover)

# The actual data we care about
userD = np.random.rand(1, 10)*100
criticD = np.random.rand(1, 10)*100
ax.scatter(userD, criticD, color = stPTColor)

# Plot it as a 
st.pyplot(fig)