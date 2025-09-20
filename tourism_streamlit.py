import streamlit as streamlt
import pandas as panda 
import plotly.express as plotly 

#Setup page configuration for streamlit (title, layout)
streamlt.set_page_config(page_title="Lebanese Tourism Infrastructure overview",
                         layout = "wide")
streamlt.title("Tourism Infrastructure across Lebanese Governorates")

#Load the tourism data set used from the previous plotly assignment as a csv file
tourism_dataset = r"C:\Users\burha\OneDrive\Documents\tourism_data_set.csv"
dataframe = panda.read_csv(tourism_dataset)

#Extract the governorate names from the reference links (refArea column) in the dataframe
dataframe['Governorate_name'] = dataframe['refArea'].apply(lambda x: x.split('/')[-1].replace('_',' '))

#Create new categories 
#Number of hotels and guest houses are combined into ACCOMMODATION!!! 
dataframe['Accommodation'] = dataframe['Total number of hotels'] + dataframe['Total number of guest houses']

#Number of restaurants and cafes are combined into FOOD & BEVERAGES!!!
dataframe['Food & Beverages'] = dataframe['Total number of restaurants'] + dataframe['Total number of cafes']

#Total infrastructure = Accommodation + Food & Beverages
dataframe['Total infrastructure'] = dataframe['Accommodation'] + dataframe['Food & Beverages']

#Assign the row of each town into its correspondant governorate and summarize the data
governorate_summary = dataframe.groupby('Governorate_name')[['Accommodation','Food & Beverages','Total infrastructure']].sum().reset_index() #columns to summarize

#Create a sidebar for filters 
streamlt.sidebar.header("Filters")

#Create a filter to display the governorates
filtered_governorates = streamlt.sidebar.multiselect(
    "Select Lebanese Governorates",
    options = governorate_summary['Governorate_name'].unique(),
    default = governorate_summary['Governorate_name'].unique()
)

#Create a slider to filter the minimum total infrastructure for each Lebanese governorate
minimum_infrastructure = streamlt.sidebar.slider(
    "Minimum Total Infrastructure",
    min_value = int(governorate_summary['Total infrastructure'].min()), #minimum value of the total infrastructure column
    max_value = int(governorate_summary['Total infrastructure'].max()), #maximum value of the total infrastructure column
    value = int(governorate_summary['Total infrastructure'].min()) #default value to start with on the slider
)

#Apply the filters to the dataframe
filtered_dataframe = governorate_summary[
    (governorate_summary['Governorate_name'].isin(filtered_governorates)) &
    (governorate_summary['Total infrastructure'] >= minimum_infrastructure)
] 

#Create an option to show the raw data table of lebanese governorates
if streamlt.sidebar.checkbox("Show raw data table"):
    streamlt.subheader("Tourism Infrastructure by Lebanese Governorates")
    streamlt.dataframe(filtered_dataframe)
    streamlt.markdown("<br>", unsafe_allow_html=True) #create more space


#context of dataset
streamlt.markdown("""
**Context:** 

The original tourism dataset given represented the tourism infrastructure across various towns in Lebanon as of 2017-12-31. 
                  
Before working on visulizatons, the dataset was cleaned and organized by combining towns into their respective governorates and dividing the variables into different categories 

The variables included in this dataset (hotels, guest houses, cafes, restaurants) were divided into two categories: Accommodation (hotels + guest houses) and Food & Beverages (cafes + restaurants).
                  
This dataset includes every Lebanese governorate EXCEPT BEIRUT! 

**The goal of this study is to analyze the distribution of tourism infrastructure across Lebanese Governorates by assessing their contributions for the food sector and accommodation sector**
""")
streamlt.markdown("<br>", unsafe_allow_html=True) #create space

#title of barchart
streamlt.subheader ("Grouped bar chart")

#context of grouped barchart
streamlt.markdown(""" 
This grouped bar chart compares accommodation facilities and food & beverage facilities across Lebanese governorates.
""")

#Create a grouped bar chart to compare accommodation and food & beverages for each governorate

fig_bar = plotly.bar(
    filtered_dataframe, 
    x='Governorate_name', # x-axis
    y=['Accommodation', 'Food & Beverages'], #y-axis
    barmode = 'group', #turn bar chart into a grouped bar chart
    text_auto= '.2s', #number on bars
    labels={'value':'Number of Facilities','Governorate name': 'Governorate'},
    title="Tourism infrastructure by Lebanese Governorate as of 2017-12-31"
)  

fig_bar.update_traces(textposition='outside') #numbers will be shown outside the bars
fig_bar.update_layout(
    yaxis=dict(showticklabels=False), #hide y-axis numbers to avoid creating a large mess
    xaxis_tickangle = -45,
    height=700

)
streamlt.plotly_chart(fig_bar, use_container_width=True)

#Insights for the grouped bar chart

streamlt.markdown("""
**Insights:** 

- Food & beverages significantly outperform accommodation in all Lebanese governorates, showing a stronger investment in the food sector compared to housing.

- Akkar & Baabda are key contributors for tourism in Lebanon. Despite being 2nd behind Baabda in food & beverages, Akkar is the only governorate to have 500+ food & beverage facilities and 100+ accommodation facilities, showing its strong contributions in both sectors. 

- Most governorates provide moderate contributions in both sectors.

- Beqaa has the lowest amount of facilities in both sectors, making it a priority for investment and infrastructure improvement.

""")
streamlt.markdown("<br>", unsafe_allow_html=True) #create space

#Create a bubble chart

streamlt.subheader("Bubble chart")
streamlt.markdown("""
Each bubble represents a governorate

The x-axis shows accommodation

The y-axis shows Food & Beverages

The bubble size/color indicates total infrastructure
            
""") #context for bubble chart

fig_bubble = plotly.scatter(
    filtered_dataframe,
    x='Accommodation',
    y='Food & Beverages',
    size='Total infrastructure',
    color='Total infrastructure',
    hover_name='Governorate_name',
    size_max=60,
    color_continuous_scale=plotly.colors.sequential.Viridis,
    title='Governorate tourism balance as of 2017-12-31'
)

fig_bubble.update_layout(height=700)
streamlt.plotly_chart(fig_bubble, use_container_width=True)


streamlt.markdown("""
**Insights:**
                  
- Bottom left with small bubbles: Underdeveloped governorates that need more investment in both sectors (Beqaa, Marjeyoun, Hasbaya)
                  
- Middle left: Moderate contributions in food sector but very poorly in accommodation (Sidon,Nabatiyeh,Hermel)
                  
- Upper middle with large bubble: Strong performer in food sector but very moderate in accomodations (Baabda, highest total infrastructure) 
                  
- Center: Moderate contributions in both sectors (Matn, Tyre, District)
                  
- Middle right: Strong performer in accommodations with moderate contributions for food (Baalbek)
                  
- Upper right with large bubble: Strong performer in both sectors ("Akkar")
                  
It was very easy to divide governorates into segments and determine which ones are in need of new policy changes and funding to attract tourism from the government and which ones are major contributors for the Lebanese tourism.
""")

