# Copyright 2025 Jiaqi Liu. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division
import pandas as pd
import altair as alt
import streamlit as st
from functools import reduce

df = pd.read_csv('data.csv')


@st.cache_data
def make_gender_distribution():
    gender_col = df["gender"]
    num_male = 0
    num_female = 0
    for row in gender_col:
        if row == "Male":
            num_male += 1
        else:
            num_female += 1
    female_percentage_chart = make_donut(round(num_female/(num_male + num_female) * 100), 'Females', 'orange')
    male_percentage_chart = make_donut(round(num_male/(num_male + num_female) * 100), 'Males', 'blue')
    return female_percentage_chart, male_percentage_chart


@st.cache_data
def make_day_frequency_distribution(color):
    frequency_df = pd.to_datetime(df["date"], format='%Y-%m-%d').dt.day.value_counts().reset_index()
    frequency_df.columns = ['day', 'frequency']
    return alt.Chart(frequency_df).mark_bar().encode(
        x=alt.X('day:N', title='Day'),
        y=alt.Y('frequency:Q', title='Frequency'),
        tooltip=['day', 'frequency'],
        color=alt.value(color),
    ).properties(
        title='Frequency by Day of Month'
    )

@st.cache_data
def make_hour_frequency_distribution(color):
    frequency_df = pd.to_datetime(df["time"], format='%H:%M:%S').dt.hour.value_counts().reset_index()
    frequency_df.columns = ['hour', 'frequency']
    return alt.Chart(frequency_df).mark_bar().encode(
        x=alt.X('hour:N', title='Time'),
        y=alt.Y('frequency:Q', title='Frequency'),
        color=alt.value(color),
    ).properties(
        title='Frequency by Time of Day'
    )


@st.cache_data
def make_category_frequency_distribution(color):
    frequency_df = pd.DataFrame(
        reduce(lambda x, y: x + y, df["category"].dropna().apply(lambda x: [i.split(':', 1)[0] for i in x.split('，')])),
        columns=['category']
    ).value_counts().reset_index()
    frequency_df.columns = ['category', 'frequency']
    return alt.Chart(frequency_df).mark_bar().encode(
        x=alt.X('category:N', title='Category'),
        y=alt.Y('frequency:Q', title='Frequency'),
        tooltip=['category', 'frequency'],
        color=alt.value(color),
    ).properties(
        title='Category Frequency'
    )

def make_donut(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']

    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100 - input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700,
                          fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text
