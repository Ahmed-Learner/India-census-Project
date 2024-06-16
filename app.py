import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config()

main_df = pd.read_csv('India_census_final.csv')

lst_states = main_df['State'].unique().tolist()
lst_states.insert(0, 'None')

st.sidebar.title("India's Data Viz")

output_container = st.empty()

lst_attributes = ['Population', 'Male', 'Female', 'sex ratio',
                    'Literates', 'Literate Males', 'Literate Females',
                    'Literacy Rate', 'Housholds with Electricity',
                    'Households with Internet']

if 'maps' not in st.session_state:
    st.session_state.maps = False
if 'graphs' not in st.session_state:
    st.session_state.graphs = False

# Sidebar buttons
if st.sidebar.button('Analysis on Maps'):
    st.session_state.maps = not st.session_state.maps
    st.session_state.graphs = False  # Reset the other button state

if st.sidebar.button('Analysis on Graphs'):
    st.session_state.graphs = not st.session_state.graphs
    st.session_state.maps = False  # Reset the other button state

if st.session_state.maps:

    maps_selectbox = st.sidebar.selectbox('Select an Option', ['None', 'Overall India', 'State wise'])

    if maps_selectbox == 'Overall India':

        primary = st.sidebar.selectbox('Select Primary Parameter', lst_attributes)

        secondary = st.sidebar.selectbox('Select Secondary Parameter', lst_attributes)

        map_button = st.sidebar.button('Plot')

        if map_button:

                st.text('* You can see the details by hovering on a particular point.')
                st.text(f'* Size of dot represents -> {primary}')
                st.text(f'* Color of dot represents -> {secondary}')

                fig = px.scatter_mapbox(main_df, lat='Latitude', lon = 'Longitude', size=primary, color=secondary,
                                        zoom = 4, size_max=35, mapbox_style='carto-positron',
                                        width=1200, height=700, hover_name='District')

                st.plotly_chart(fig, use_container_width=True)

    elif maps_selectbox == 'State wise':

        selected_state_sgl_map = st.sidebar.selectbox('Select a State', lst_states)

        if selected_state_sgl_map != 'None':

            primary_sgl_map = st.sidebar.selectbox('Select a Primary Attribute', lst_attributes)

            secondary_sgl_map = st.sidebar.selectbox('Select a Secondary Attribute', lst_attributes)

            plot = st.sidebar.button('Plot')

            if plot:

                st.text('* You can see the details by hovering on a particular point.')
                st.text(f'* Size of dot represents -> {primary_sgl_map}')
                st.text(f'* Color of dot represents -> {secondary_sgl_map}')

                state_df = main_df[main_df['State'] == selected_state_sgl_map]

                fig = px.scatter_mapbox(state_df, lat='Latitude', lon='Longitude', size=primary_sgl_map,
                                        color=secondary_sgl_map,
                                        zoom=6, size_max=35, mapbox_style='carto-positron', width=1200, height=700,
                                        hover_name='District')

                st.plotly_chart(fig, use_container_width=True)

if st.session_state.graphs:

    graph_selectbox = st.sidebar.selectbox('Select the analysis mode', ['None', 'Analysis on Two Plots',
                                                                        'Analysis on a Single Plot'])

    if graph_selectbox != 'None':

        if graph_selectbox == 'Analysis on Two Plots':

            select_box_tow_plots = st.sidebar.selectbox('Select type of Graph', ['Line chart', 'Bar chart'])

            if select_box_tow_plots == 'Line chart':

                state1 = st.sidebar.selectbox('Select 1st State', lst_states[1:])
                df1 = main_df[main_df['State'] == state1]

                state2 = st.sidebar.selectbox('Select 2nd State', lst_states[1:])
                df2 = main_df[main_df['State'] == state2]

                on_attribute = st.sidebar.selectbox('Select an Attribute to be analyzed', lst_attributes)

                plot = st.sidebar.button('Plot')

                if plot:

                    st.text('* You can see the details by hovering on a particular point.')
                    fig = make_subplots(rows=1, cols=2, subplot_titles=(f'For {state1}', f'For {state2}'))

                    fig.add_trace(
                        go.Scatter(x=df1['District'], y=df1[on_attribute], hovertext=df1['District'], name=state1),
                        row=1, col=1
                        )

                    fig.add_trace(
                        go.Scatter(x=df2['District'], y=df2[on_attribute], hovertext=df2['District'], name=state2),
                        row=1, col=2
                        )

                    fig.update_xaxes(title_text=f"Districts of {state1}", row=1, col=1)
                    fig.update_yaxes(title_text=f"{on_attribute} of {state1}", row=1, col=1)

                    fig.update_xaxes(title_text=f"Districts of {state2}", row=1, col=2)
                    fig.update_yaxes(title_text=f"{on_attribute} of {state2}", row=1, col=2)

                    fig.update_layout(title_text=f"""* State wise Line Graph on {state1} and {state2} for {on_attribute} .""")

                    st.plotly_chart(fig, use_container_width=True)

            elif select_box_tow_plots == 'Bar chart':

                state1 = st.sidebar.selectbox('Select 1st State', lst_states[1:])
                df1 = main_df[main_df['State'] == state1]

                state2 = st.sidebar.selectbox('Select 2nd State', lst_states[1:])
                df2 = main_df[main_df['State'] == state2]

                on_attribute_bar = st.sidebar.selectbox('Select an Attribute.',lst_attributes)

                plot = st.sidebar.button('Plot')

                if plot:

                    st.text('* You can see the details by hovering on a particular Bar.')
                    st.text(f'* Bar represents -> {on_attribute_bar}')

                    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'For {state1}', f'For {state2}'))

                    fig.add_trace(
                        go.Bar(x=df1[on_attribute_bar], y=df1['District'], orientation='h', hovertext=df1['District'],
                               name=state1),
                        row=1, col=1
                        )

                    fig.add_trace(
                        go.Bar(x=df2[on_attribute_bar], y=df2['District'], orientation='h', hovertext=df2['District'],
                               name=state2),
                        row=2, col=1
                        )

                    fig.update_xaxes(title_text=f"{on_attribute_bar} of {state1}", row=1, col=1)
                    fig.update_yaxes(title_text=f"Districts of {state1}", row=1, col=1)

                    fig.update_xaxes(title_text=f"{on_attribute_bar} of {state2}", row=2, col=1)
                    fig.update_yaxes(title_text=f"Districts of {state2}", row=2, col=1)

                    fig.update_layout(title_text=f"* Bar chart for {state1} and {state2} on {on_attribute_bar}",
                                      height=1100, width=1200)

                    st.plotly_chart(fig, use_container_width=True)

        elif graph_selectbox == 'Analysis on a Single Plot':

            state = st.sidebar.selectbox('Select 1st State', lst_states[1:])

            analysis_on  = st.sidebar.selectbox('Select an attribute',lst_attributes)

            plot = st.sidebar.button('Plot')

            if plot:

                st.text('* You can see the details by hovering on a particular Point.')
                st.text(f'* Line represents -> {analysis_on}')

                fig = px.line(main_df[main_df['State'] == 'Andhra Pradesh'], x='District', y=analysis_on,
                              title=f'{analysis_on} of {state}', hover_name=analysis_on)
                fig.update_traces(textposition="top center")

                st.plotly_chart(fig, use_container_width=True)

st.sidebar.text('')
st.sidebar.text('Want to see the codes?')
code = st.sidebar.button('Yes')
if code:
    codes = '''
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config()

main_df = pd.read_csv('India_census_final.csv')

lst_states = main_df['State'].unique().tolist()
lst_states.insert(0, 'None')

st.sidebar.title("India's Data Viz")

output_container = st.empty()

lst_attributes = ['Population', 'Male', 'Female', 'sex ratio',
                    'Literates', 'Literate Males', 'Literate Females',
                    'Literacy Rate', 'Housholds with Electricity',
                    'Households with Internet']

if 'maps' not in st.session_state:
    st.session_state.maps = False
if 'graphs' not in st.session_state:
    st.session_state.graphs = False

# Sidebar buttons
if st.sidebar.button('Analysis on Maps'):
    st.session_state.maps = not st.session_state.maps
    st.session_state.graphs = False  # Reset the other button state

if st.sidebar.button('Analysis on Graphs'):
    st.session_state.graphs = not st.session_state.graphs
    st.session_state.maps = False  # Reset the other button state

if st.session_state.maps:

    maps_selectbox = st.sidebar.selectbox('Select an Option', ['None', 'Overall India', 'State wise'])

    if maps_selectbox == 'Overall India':

        primary = st.sidebar.selectbox('Select Primary Parameter', lst_attributes)

        secondary = st.sidebar.selectbox('Select Secondary Parameter', lst_attributes)

        map_button = st.sidebar.button('Plot')

        if map_button:

                st.text('* You can see the details by hovering on a particular point.')
                st.text(f'* Size of dot represents -> {primary}')
                st.text(f'* Color of dot represents -> {secondary}')

                fig = px.scatter_mapbox(main_df, lat='Latitude', lon = 'Longitude', size=primary, color=secondary,
                                        zoom = 4, size_max=35, mapbox_style='carto-positron',
                                        width=1200, height=700, hover_name='District')

                st.plotly_chart(fig, use_container_width=True)

    elif maps_selectbox == 'State wise':

        selected_state_sgl_map = st.sidebar.selectbox('Select a State', lst_states)

        if selected_state_sgl_map != 'None':

            primary_sgl_map = st.sidebar.selectbox('Select a Primary Attribute', lst_attributes)

            secondary_sgl_map = st.sidebar.selectbox('Select a Secondary Attribute', lst_attributes)

            plot = st.sidebar.button('Plot')

            if plot:

                st.text('* You can see the details by hovering on a particular point.')
                st.text(f'* Size of dot represents -> {primary_sgl_map}')
                st.text(f'* Color of dot represents -> {secondary_sgl_map}')

                state_df = main_df[main_df['State'] == selected_state_sgl_map]

                fig = px.scatter_mapbox(state_df, lat='Latitude', lon='Longitude', size=primary_sgl_map,
                                        color=secondary_sgl_map,
                                        zoom=6, size_max=35, mapbox_style='carto-positron', width=1200, height=700,
                                        hover_name='District')

                st.plotly_chart(fig, use_container_width=True)

if st.session_state.graphs:

    graph_selectbox = st.sidebar.selectbox('Select the analysis mode', ['None', 'Analysis on Two Plots',
                                                                        'Analysis on a Single Plot'])

    if graph_selectbox != 'None':

        if graph_selectbox == 'Analysis on Two Plots':

            select_box_tow_plots = st.sidebar.selectbox('Select type of Graph', ['Line chart', 'Bar chart'])

            if select_box_tow_plots == 'Line chart':

                state1 = st.sidebar.selectbox('Select 1st State', lst_states[1:])
                df1 = main_df[main_df['State'] == state1]

                state2 = st.sidebar.selectbox('Select 2nd State', lst_states[1:])
                df2 = main_df[main_df['State'] == state2]

                on_attribute = st.sidebar.selectbox('Select an Attribute to be analyzed', lst_attributes)

                plot = st.sidebar.button('Plot')

                if plot:

                    st.text('* You can see the details by hovering on a particular point.')
                    fig = make_subplots(rows=1, cols=2, subplot_titles=(f'For {state1}', f'For {state2}'))

                    fig.add_trace(
                        go.Scatter(x=df1['District'], y=df1[on_attribute], hovertext=df1['District'], name=state1),
                        row=1, col=1
                        )

                    fig.add_trace(
                        go.Scatter(x=df2['District'], y=df2[on_attribute], hovertext=df2['District'], name=state2),
                        row=1, col=2
                        )

                    fig.update_xaxes(title_text=f"Districts of {state1}", row=1, col=1)
                    fig.update_yaxes(title_text=f"{on_attribute} of {state1}", row=1, col=1)

                    fig.update_xaxes(title_text=f"Districts of {state2}", row=1, col=2)
                    fig.update_yaxes(title_text=f"{on_attribute} of {state2}", row=1, col=2)

                    fig.update_layout(title_text=f"""* State wise Line Graph on {state1} and {state2} for {on_attribute} .""")

                    st.plotly_chart(fig, use_container_width=True)

            elif select_box_tow_plots == 'Bar chart':

                state1 = st.sidebar.selectbox('Select 1st State', lst_states[1:])
                df1 = main_df[main_df['State'] == state1]

                state2 = st.sidebar.selectbox('Select 2nd State', lst_states[1:])
                df2 = main_df[main_df['State'] == state2]

                on_attribute_bar = st.sidebar.selectbox('Select an Attribute.',lst_attributes)

                plot = st.sidebar.button('Plot')

                if plot:

                    st.text('* You can see the details by hovering on a particular Bar.')
                    st.text(f'* Bar represents -> {on_attribute_bar}')

                    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'For {state1}', f'For {state2}'))

                    fig.add_trace(
                        go.Bar(x=df1[on_attribute_bar], y=df1['District'], orientation='h', hovertext=df1['District'],
                               name=state1),
                        row=1, col=1
                        )

                    fig.add_trace(
                        go.Bar(x=df2[on_attribute_bar], y=df2['District'], orientation='h', hovertext=df2['District'],
                               name=state2),
                        row=2, col=1
                        )

                    fig.update_xaxes(title_text=f"{on_attribute_bar} of {state1}", row=1, col=1)
                    fig.update_yaxes(title_text=f"Districts of {state1}", row=1, col=1)

                    fig.update_xaxes(title_text=f"{on_attribute_bar} of {state2}", row=2, col=1)
                    fig.update_yaxes(title_text=f"Districts of {state2}", row=2, col=1)

                    fig.update_layout(title_text=f"* Bar chart for {state1} and {state2} on {on_attribute_bar}",
                                      height=1100, width=1200)

                    st.plotly_chart(fig, use_container_width=True)

        elif graph_selectbox == 'Analysis on a Single Plot':

            state = st.sidebar.selectbox('Select 1st State', lst_states[1:])

            analysis_on  = st.sidebar.selectbox('Select an attribute',lst_attributes)

            plot = st.sidebar.button('Plot')

            if plot:

                st.text('* You can see the details by hovering on a particular Point.')
                st.text(f'* Line represents -> {analysis_on}')

                fig = px.line(main_df[main_df['State'] == 'Andhra Pradesh'], x='District', y=analysis_on,
                              title=f'{analysis_on} of {state}', hover_name=analysis_on)
                fig.update_traces(textposition="top center")

                st.plotly_chart(fig, use_container_width=True)
    '''
    st.code(codes, language='python')

