import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

from plotly.offline import iplot, init_notebook_mode

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

# tobacco use in United States in 2010
tobacco_2010 = tobacco_usa[tobacco_usa.year == 2010].sort_values('state')
tobacco_2010.index = range(51)

tobacco_risk_index = np.asarray(tobacco_2010['daily_smoker'] * 2.5 + tobacco_2010['weekly_smoker'] * 1.72 + tobacco_2010['former_smoker'] * 1.3 + tobacco_2010['never_smoker'])

us_states = np.asarray(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
                        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                        'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                        'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

tobacco_scale = [[0, 'rgb(252, 230, 229)'], [1, 'rgb(229, 5, 0)']]

data = [dict(
        type = 'choropleth',
        autocolorscale = False,
        colorscale = tobacco_scale,
        showscale = True,
        locations = us_states,
        locationmode = 'USA-states',
        z = tobacco_risk_index,
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 2)
            )
        )]

layout = dict(
         title = 'Tobacco-Weighted Mortality Risk Index in 2010',
         width = 1024,
         height = 768,
         geo = dict(
             scope = 'usa',
             projection = dict(type = 'albers usa'),
             countrycolor = 'rgb(255, 255, 255)',
             showlakes = True,
             lakecolor = 'rgb(255, 255, 255)')
         )

figure = dict(data = data, layout = layout)
iplot(figure)