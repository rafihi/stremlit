import streamlit as st

st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
p, div, input, label, h1, h2, h3, h4, h5, h6 {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

st.title( "רמת ההשכלה בישראל")

st.write("רפאל הירש 06.01.25")
st.write("")
st.write("")

st.header("השכלה לפי פיקוח רב שנתי")

st.subheader("גילאי 25-66 ##")

flourish_embed_code = """
<div class="flourish-embed flourish-chart" data-src="visualisation/21046767"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21046767/thumbnail" width="100%" alt="chart visualization" /></noscript></div>"""

st.components.v1.html(flourish_embed_code, height=600)


