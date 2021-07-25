# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import io

import pandas as pd
import streamlit as st

st.set_page_config(page_title = 'Αλλαγή Κράματος',
                   layout = 'centered',
                   initial_sidebar_state = "auto")

data_path = "https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file}".format(
    user = st.secrets['user'],
    repo = st.secrets['repo'],
    branch = st.secrets['branch'],
    file = st.secrets['file'])

github_session = requests.Session()
github_session.auth = (st.secrets['user'], st.secrets['access_token'])

download = github_session.get(data_path).content

@st.cache
def loadData(download):
    return pd.read_csv(io.StringIO(download.decode('utf-8')),
                       sep = ';',
                       header = 0,
                       index_col = 'ID')

st.title('Αλλαγή κράματος')

password = st.text_input('Κωδικός πρόσβασης',
                         max_chars = 12,
                         key = 'password',
                         type = 'password')

if not password == st.secrets['password']:
    st.stop()

data = loadData(download)
github_session.close()

with st.form(key = 'form'):
    cols_sel = st.beta_columns([0.48, 0.48, 0.02])

    help_alloy0 = 'Κωδικός του κράματος που χυτευόταν έως τώρα'
    with cols_sel[0]:
        alloy0 = st.selectbox('Τρέχον κράμα',
                              data.index,
                              key = 'sel_alloy0',
                              help = help_alloy0)

    help_alloy1 = 'Κωδικός του κράματος που πρόκειται να χυτευτεί'
    with cols_sel[1]:
        alloy1 = st.selectbox('Επόμενο κράμα',
                              data.index,
                              key = 'sel_alloy1',
                              help = help_alloy1)

    submit_button = st.form_submit_button("Ανανέωση δεδομένων")

specs = pd.DataFrame(data = {'0: ' + alloy0: data.loc[alloy0],
                             '1: ' + alloy1: data.loc[alloy1],
                             'Diff': data.loc[alloy1] - data.loc[alloy0]},
                     copy = True)

frame = specs.style.applymap(lambda x: 'color: red' if x < 0
                             else 'color: #ffffff', subset = 'Diff')

if submit_button:
    st.dataframe(frame)
