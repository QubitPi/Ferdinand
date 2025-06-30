# Copyright 2025 Jiaqi Liu. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import visualization

st.set_page_config(
    page_title="Data Analytics",
    page_icon="📈",
    layout="wide",
)

with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

import base64
import streamlit.components.v1 as components
with open("logo.png", "rb") as f:
    data = f.read()
data_url = base64.b64encode(data).decode("utf-8")
html_code = f"""
<div align="center"><img width="120px" src="data:image/png;base64,{data_url}" alt="Your Image"></div>
"""
components.html(html_code)

st.markdown("<h1 style='text-align: center; color: #fafafa;'>My Organization</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #fafafa;'>Data Analytics Platform</h2>", unsafe_allow_html=True)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login(fields={'Form name':'Internal Access Only', 'Username':'Username', 'Password':'Password', 'Login':'Login', 'Captcha':'Captcha'})
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"]:
    with st.sidebar:
        st.title('📊 Data Analytics')

        color_map = {
            "Blue": "#1f77b4",
            "Orange": "#ff7f0e",
            "Green": "#2ca02c",
            "Red": "#d62728",
            "Purple": "#9467bd",
            "Brown": "#8c564b",
            "Pink": "#e377c2",
            "Gray": "#7f7f7f",
            "Cyan": "#17becf"
        }

        selected_color = color_map[st.selectbox('Please select display color', color_map.keys())]

    st.write('___')
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.markdown("<h2 style='text-align: center; color: #fafafa;'>Data Analytics Platform</h2>", unsafe_allow_html=True)

    st.write('___')

    col = st.columns((1.5, 4.5, 2), gap='medium')

    with col[0]:
        st.markdown('#### Gender')

        female_percentage_chart, male_percentage_chart = visualization.make_gender_distribution()
        left_column, right_column = st.columns(2)
        left_column.write('Female')
        left_column.altair_chart(female_percentage_chart)
        right_column.write('Male')
        right_column.altair_chart(male_percentage_chart)

    with col[1]:
        st.markdown('#### Time')

        st.altair_chart(visualization.make_day_frequency_distribution(selected_color))
        left_column, right_column = st.columns(2)
        left_column.altair_chart(visualization.make_hour_frequency_distribution(selected_color))
        right_column.altair_chart(visualization.make_category_frequency_distribution(selected_color))


elif st.session_state["authentication_status"] is False:
    st.error('Incorrect Username or Password')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter Username and Password to continue')
