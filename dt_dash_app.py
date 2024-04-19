# Import required libraries
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',8)

# Read the airline data into pandas dataframe
df = pd.read_csv(r'C:\Users\chikwesa\OneDrive - Vodafone Group\PC Backup 9 February 2021\Group Network Quality\Analytics\Programs\Python\Campaign 9 CS_PS Trialing Failure Analysis Details 3_10_2022.csv')
a = df.head()
print(a)
print('')

b = df.shape
print(b)
print('')

missing_data = df.isnull()
c = missing_data.head()
print(c)
print('')

d = missing_data.shape
print(d)
print('')

for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print("")

print('')

def get_class(cl):
    if cl == 'Failed':
        marker = 0
    elif cl != 'Failed':
        marker = 1
    return marker

df['class'] = df['End Service Status'].apply(get_class)
e = df
print(e)
print('')

max_throughput = df['MeanDataRateMethodAThroughputKbps'].max()
min_throughput = df['MeanDataRateMethodAThroughputKbps'].min()
print(max_throughput)
print(min_throughput)
print('')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('DT Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Region selection
                                # The default select value is for ALL regions
                                # dcc.Dropdown(id='region-dropdown',...)
                                dcc.Dropdown(id='region-dropdown',
                                    options=[
                                        {'label': 'All Regions', 'value': 'ALL'},
                                        {'label': 'CEN', 'value': 'CEN'},
                                        {'label': 'EAS', 'value': 'EAS'},
                                        {'label': 'KZN', 'value': 'KZN'},
                                        {'label': 'LIM', 'value': 'LIM'},
                                        {'label': 'MPU', 'value': 'MPU'},
                                        {'label': 'NGA', 'value': 'NGA'},
                                        {'label': 'SGC', 'value': 'SGC'},
                                        {'label': 'SGS', 'value': 'SGS'},
                                        {'label': 'WES', 'value': 'WES'},
                                    ],
                                    value='ALL',
                                    placeholder="Select a Region",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful tests for all regions
                                # If a specific region was selected, show the Success vs. Failed counts for the region
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Throughput range (kbps):"),
                                # TASK 3: Add a slider to select throughput
                                #dcc.RangeSlider(id='throughput-slider',...)
                                #html.Div(dcc.RangeSlider(id='throughput-slider',
                                dcc.RangeSlider(id='throughput-slider',
	                                min=0, max=5000, step=500,
	                                marks={0: '0',
		                                1250: '1250',
		                                2500: '2500',
		                                3750: '3750',
		                                5000: '5000'},
                                    value=[min_throughput, max_throughput]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `region-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='region-dropdown', component_property='value'))
def get_pie_chart(entered_region):
    filtered_df = df
    if entered_region == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='GeoRegion',
        title='Total Successful Tests for All Regions')
        return fig
    else:
        # return the outcomes piechart for a selected region
        filtered_df=df[df['GeoRegion']== entered_region]
        filtered_df = filtered_df.groupby(['GeoRegion', 'class']).size().reset_index(name='class count')
        fig2 = px.pie(filtered_df, values='class count',
        names='class',
        title=f'Total Successful Tests for {entered_region}')
        return fig2

# TASK 4:
# Add a callback function for `region-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='region-dropdown', component_property='value'),
              Input(component_id="throughput-slider", component_property="value"))
def get_scatter_chart(entered_region, throughput_slider):
    filtered_df2 = df[(df['MeanDataRateMethodAThroughputKbps']>=throughput_slider[0]) & (df['MeanDataRateMethodAThroughputKbps']<=throughput_slider[1])]
    if entered_region == 'ALL':
        fig3 = px.scatter(filtered_df2, x = 'MeanDataRateMethodAThroughputKbps', y = 'class', color='Test Type',
        title=f'Correlation Dataset: Throughput and Success for All Regions')
        return fig3
    else:
        # return the outcomes scatter chart for a selected site and payload
        filtered_df3=filtered_df2[filtered_df2['GeoRegion']== entered_region]
        fig4 = px.scatter(filtered_df3, x = 'MeanDataRateMethodAThroughputKbps', y = 'class', color='Test Type',
        title=f'Correlation Dataset: Throughput and Success for {entered_region}')
        return fig4

print('')

f = df.shape
print(f)
print('')

g = df['class']
print(g)
print('')

h = df['class'].shape
print(h)

# Run the app
if __name__ == '__main__':
    app.run_server()