# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                               {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                               {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                               {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                               {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                               ], #Labels and values to appear in drop down
                                    value='ALL', #Default drop down attribute
                                    placeholder='Select a launch site here', #Description about input area
                                    searchable=True #Allows us to enter keywords to search launch sites
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                           1000: '1000',
                                           2000: '2000',
                                           3000: '3000',
                                           4000: '4000',
                                           5000: '5000',
                                           6000: '6000',
                                           7000: '7000',
                                           8000: '8000',
                                           9000: '9000',
                                           10000: '10000'},
                                    value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Successful Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        #filter data to only the selected site
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        #Add a constant of one
        fdf2=filtered_df.copy()
        fdf2['launches']=1
        #pie chart
        fig = px.pie(fdf2, values='launches', 
        names='class', 
        title=f"Distribution of successful launches for {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
             )
def get_scatter_chart(entered_site,entered_payload):
    minp, maxp = entered_payload
    #Filter to selected payload range
    filtered = spacex_df[(spacex_df["Payload Mass (kg)"]>=minp) & (spacex_df["Payload Mass (kg)"]<=maxp)]
    if entered_site== 'ALL':
        #Scatter plot of all payloads by class, with booster version for colour
        fig= px.scatter(filtered,
                        x="Payload Mass (kg)",
                        y="class",
                        color="Booster Version Category",
                        title="Correlation between Payload and Success for all sites")
        return fig
    else:
        #Filter to selected site
        fdf2=filtered.copy()
        fdf2=fdf2[fdf2['Launch Site']==entered_site]
        #Scatter plot
        fig= px.scatter(fdf2,
                        x="Payload Mass (kg)",
                        y="class",
                        color="Booster Version Category",
                        title=f"Correlation between Payload and Success for {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
