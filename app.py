import base64

import streamlit as st

from make_timecard import make_timecards


st.set_option('deprecation.showfileUploaderEncoding', False)


def app():
    st.title("Hi Satoko San!!!")
    uploaded_file = st.file_uploader("Upload your CSV here!", type=['csv'])
    
    if uploaded_file is not None:        
        timecards = make_timecards(uploaded_file)
        st.write("Here's the timecards!")
        st.write(timecards)
        st.markdown(get_table_download_link(timecards), unsafe_allow_html=True)


def get_table_download_link(df):
    """
    Generates a link allowing the data in a given panda dataframe to be 
    downloaded
    ---
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


if __name__ == "__main__":
    app()