import streamlit as st
from PIL import Image

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# Create two columns
col1, col2 = st.columns(2)

# Display the first chart in the first column
with col1:
    st.title(f"🇮🇱 רמת ההשכלה בישראל")
    st.subheader("גילאי 25-66 בשנים **8002 - 2202** ##")
    st.write("יוצר: רפאל הירש")
    # Display the second chart in the second column
with col2:
    col21, col22 = st.columns(2) 

    with col21:
        st.write()
        
    with col22:
        st.image("data:image/png;base64,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", width=200)

#right to left
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

st.write("")
st.write("")

#לפי פיקוח
st.subheader("השכלה לפי פיקוח ממלכתי/דתי/חרדי ")
flourish_embed_code = """<div class="flourish-embed flourish-chart" data-src="visualisation/21046767"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21046767/thumbnail" width="100%" alt="chart visualization" /></noscript></div>"""
st.components.v1.html(flourish_embed_code, height=650)

#השכלת אם 
flourish_embed_code1 = """<div class="flourish-embed flourish-sankey" data-src="visualisation/21049208"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21049208/thumbnail" width="100%" alt="sankey visualization" /></noscript></div>"""
#st.components.v1.html(flourish_embed_code1, height=600)


#st.header("השכלה לפי השכלת אב")
#flourish pikuch
flourish_embed_code2 = """<div class="flourish-embed flourish-sankey" data-src="visualisation/21048102"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21048102/thumbnail" width="100%" alt="sankey visualization" /></noscript></div>"""
#st.components.v1.html(flourish_embed_code2, height=600)


# Create two columns
col1, col2 = st.columns(2)

# Display the first chart in the first column
with col1:
    st.subheader("השכלה לפי השכלת אם")
    st.components.v1.html(flourish_embed_code1, height=650)

# Display the second chart in the second column
with col2:
    st.subheader("השכלה לפי השכלת אב")
    st.components.v1.html(flourish_embed_code2, height=650)






#יורדים
flourish_embed_code2 = """<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/21049406"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21049406/thumbnail" width="100%" alt="bar-chart-race visualization" /></noscript></div>"""
#עולים
flourish_embed_code1 = """<div class="flourish-embed flourish-chart" data-src="visualisation/21049878"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21049878/thumbnail" width="100%" alt="chart visualization" /></noscript></div>"""




# Create two columns
col1, col2 = st.columns(2)

# Display the first chart in the first column
with col1:
    st.subheader("השכלת עולים לפי שנת עלייה")
    st.components.v1.html(flourish_embed_code1, height=650)

# Display the second chart in the second column
with col2:
    st.subheader("השכלת יורדים לפי שנה")
    st.components.v1.html(flourish_embed_code2, height=650)






