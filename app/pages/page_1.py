import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")


# Initialize pygwalker communication
init_streamlit_comm()


# When using `use_kernel_calc=True`, you should cache your pygwalker html, if you don't want your memory to explode
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    # If you want to use feature of saving chart config, set `debug=True`
    html = get_streamlit_html(df, spec="./gw0.json", use_kernel_calc=True, debug=False)
    return html


@st.cache_data
def get_df() -> pd.DataFrame:
    return pd.read_csv(
        "/Users/yoannfaure/Library/CloudStorage/OneDrive-Personnel/2. Yoann Personnel/14. Pro_Perso/1. Formation Data/Datascientest/VsCode/NBA/data/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.csv"
    )


df = get_df()

components.html(get_pyg_html(df), width=1300, height=1000, scrolling=True)
