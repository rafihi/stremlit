import streamlit as st

st.title( "stremlit try: sunglasses:")

st.write("Rafi Hirsch")

st.title("My Flourish Visualization")

flourish_embed_code = """
<div class="flourish-embed flourish-chart" data-src="visualisation/21046767"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21046767/thumbnail" width="100%" alt="chart visualization" /></noscript></div>"""

st.components.v1.html(flourish_embed_code, height=600)
