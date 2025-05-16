import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objects as go

init_notebook_mode()

tobacco_data = pd.read_csv('./tobacco.csv', usecols=[0, 1, 2, 3, 4, 5])
tobacco_data = tobacco_data.rename(
    columns={'Smoke everyday':'daily_smoker', 'Smoke some days':'weekly_smoker',
             'Former smoker':'former_smoker', 'Never smoked':'never_smoker'})
tobacco_data.columns = tobacco_data.columns.str.lower()

for percents in tobacco_data.columns[2:]:
    tobacco_data[percents] = tobacco_data[percents].str.rstrip('%')
    tobacco_data[percents] = pd.to_numeric(tobacco_data[percents])

# tobacco use in US states only, territories excluded (812 rows)
mask = tobacco_data['state'].isin(
    ['Guam', 'Puerto Rico', 'Virgin Islands', 'Nationwide (States and DC)',
     'Nationwide (States, DC, and Territories)'])
tobacco_usa = tobacco_data[~mask].sort_values(['year', 'state'])

# tobacco use in United States in 1995
tobacco_1995 = tobacco_usa[tobacco_usa.year == 1995]
tobacco_1995.loc[0] = [1996, 'District of Columbia', 14.9, 5.6, 17.8, 61.7]
tobacco_1995.loc[1] = [1997, 'Utah', 11.1, 2.6, 17.2, 69.0]
tobacco_1995.sort_values('state')
tobacco_1995.index = range(51)

# tobacco use in United States in 2010
tobacco_2010 = tobacco_usa[tobacco_usa.year == 2010].sort_values('state')
tobacco_2010.index = range(51)

# define hazard ratio-based weights for each smoking category
risk_weights = {
    'daily_smoker': 2.5,
    'weekly_smoker': 1.72,
    'former_smoker': 1.3,
    'never_smoker': 1.0
}

# compute weighted risk index for each state and round results
# subtracting 100 as a normalization step
tobacco_risk_index_1995 = np.round(tobacco_1995[list(risk_weights)].mul(pd.Series(risk_weights)).sum(axis=1)) - 100
tobacco_risk_index_2010 = np.round(tobacco_2010[list(risk_weights)].mul(pd.Series(risk_weights)).sum(axis=1)) - 100

us_states = np.asarray(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
                        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                        'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                        'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

tobacco_scale = [[0, 'rgb(252, 230, 229)'], [1, 'rgb(229, 5, 0)']]

# build choropleth map showing 2010 tobacco risk by state
data = [dict(
        type = 'choropleth',
        autocolorscale = False,
        colorscale = tobacco_scale,
        showscale = True,
        locations = us_states,
        locationmode = 'USA-states',
        z = tobacco_risk_index_2010,
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 2)
            )
        )]

# overlay state risk values as text labels
data.append(dict(
        type = 'scattergeo',
        locations = us_states,
        locationmode = 'USA-states',
        text = tobacco_risk_index_2010,
        mode = 'text',
        textposition = 'middle center',
        textfont = dict(
            family = 'Arial',
            size = 12,
            color = 'rgb(0, 0, 0)')
        ))

layout = dict(
            title = 'Tobacco-Weighted Mortality Risk Index in 2010',
            height = 600,
            geo = dict(
                scope = 'usa',
                projection = dict(type = 'albers usa'),
                countrycolor = 'rgb(255, 255, 255)',
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)'
            )
        )
        
# display the map
figure = dict(data = data, layout = layout)
iplot(figure)

# plot comparison of 1995 vs 2010 tobacco risk indices
fig = go.Figure(
        data = [
            go.Bar(x=us_states, y=tobacco_risk_index_1995, name='1995'),
            go.Bar(x=us_states, y=tobacco_risk_index_2010, name='2010')
        ],
        layout=go.Layout(
            title="Tobacco-Weighted Mortality Risk Index in 1995 & 2010",
            height=500,
            xaxis=dict(
                tickangle=45,
                title="State"
            ),
            yaxis=dict(
                tickangle=0,
                title="Risk Score"
            ),
        ))
fig.show()