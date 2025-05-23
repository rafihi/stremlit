import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import google.generativeai as genai
import fitz  # PyMuPDF for extracting text from PDFs
import os
import requests
import io


#ראשון : הגדרות העמוד
st.set_page_config(initial_sidebar_state='expanded',layout="wide")

#לוגו
st.logo("data:image/png;base64,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",size='large')

#right to left
st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: center;
}
p, div, label, h1, h2, h3, h4, h6 {   
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)
# i removed h5 and input

#space out optins in radio sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] .stRadio > div {
            gap: 10px; /* Adjust spacing between options */
        }
    </style>
""", unsafe_allow_html=True)

#background-color: #e3e9eb;
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-image: url('https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGVkdWNhdGlvbnxlbnwwfHwwfHx8MA%3D%3D');
        background-size: cover; /* Ensures the image covers the sidebar area */
        background-position: center; /* Centers the image */
        background-repeat: no-repeat; /* Prevents image tiling */
    }
</style>
""", unsafe_allow_html=True)
    
#sidebar
st.sidebar.title("תוכן עניינים")
page = st.sidebar.radio(" ",["***רמת השכלה מפורטת כלל האוכלוסיה***","***רמת השכלה לפי הורה***","***רמת השכלה עולים ויורדים***","***השכלה לפי פיקוח***","***מפת ישראל - השכלה לפי ישוב***","***צ'אט בוט - מרשם השכלה***"])
st.sidebar.write('#')
st.sidebar.write('#')


# import streamlit.components.v1 as components
# sss = """<div class="flourish-embed flourish-number-ticker" data-src="visualisation/21132982"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21132982/thumbnail" width="100%" alt="number-ticker visualization" /></noscript></div>"""
# with st.sidebar:
#     components.html(sss, height=350)

b = 'רפאל הירש'

st.sidebar.markdown(
    f"""
    <div style="background-color:  #ffffff ; padding: 10px; border-radius: 20px; text-align: center; color: black;">
        יוצר: {b}
    </div>
    """,
    unsafe_allow_html=True)



#עמוד 1
if page == '***רמת השכלה מפורטת כלל האוכלוסיה***':
    st.header(" רמת השכלה מפורטת כלל האוכלוסיה")
    #מגמות כלל האוכלוסיה
    flourish_embed_code = """<div class="flourish-embed flourish-chart" data-src="visualisation/21053009"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21053009/thumbnail" width="100%" alt="chart visualization" /></noscript></div>"""

    st.subheader("גילאי 52-66 בשנים **8002 - 2202** ##")
    #טיקר מספרים
    flourish_embed_code55 = """<div class="flourish-embed flourish-number-ticker" data-src="visualisation/21131573"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21131573/thumbnail" width="100%" alt="number-ticker visualization" /></noscript></div>"""
    st.components.v1.html(flourish_embed_code55, height=150)
    with st.expander('הגדרות והסברים'):
     st.write("""
                    
                    הגרף מציג מגמות מעניינות ברמת ההשכלה בישראל בין השנים 2009 ל-2022. 
                    ניתן לראות עלייה מתמדת, אך איטית, באחוז האזרחים בעלי השכלה אקדמית, שהגיעה לכ-41.3% בשנת 2022. 
                    במקביל, חלה ירידה משמעותית באחוז האזרחים בעלי השכלה נמוכה מסיום בית ספר תיכון, מצד שני, חלה עלייה קלה באחוז בעלי השכלה על-תיכונית שאינה אקדמית,
                    מה שמעיד על מגמה של העלאת רמת ההשכלה הכללית באוכלוסייה.
                    עם זאת, עדיין קיים פער משמעותי בין קבוצות אוכלוסייה שונות ברמת ההשכלה שלהן, כפי שניתן לראות מהשינויים הקטנים יחסית באחוז בעלי השכלה תיכונית או בגרות.""")
    st.markdown("---")
    st.components.v1.html(flourish_embed_code, height=650)

#עמוד 2
if page == '***רמת השכלה לפי הורה***':
    st.header('רמת ההשכלה לפי רמת השכלת ההורה')
    with st.expander('הגדרות והסברים'):
     st.write("")
    st.markdown("---") 
    st.subheader('קשר בין רמת ההשכלה לבין רמת ההשכלה של ההורה')

           #השכלת אם 
    flourish_embed_code11 = ("""<div class="flourish-embed flourish-scatter" data-src="visualisation/21091340"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21091340/thumbnail" width="100%" alt="scatter visualization" /></noscript></div>""")
    flourish_embed_code12 = ("""<div class="flourish-embed flourish-scatter" data-src="visualisation/21080916"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21080916/thumbnail" width="100%" alt="scatter visualization" /></noscript></div>""")

    if "show_graph" not in st.session_state:
        st.session_state.show_graph = False

    # Function to toggle graph visibility
    def toggle_graph1():
        st.session_state.show_graph = not st.session_state.show_graph

    # Add a button to toggle the graph visibility
    if st.button("מתאם", on_click=toggle_graph1):
        pass

    # Display the Flourish embed graph if the state is set to True
    if st.session_state.show_graph:
        col1, col2 = st.columns(2)
        with col1:
         st.components.v1.html(flourish_embed_code11, height=650)
        with col2:
         st.components.v1.html(flourish_embed_code12, height=650)
    # #השכלת אב אחוזים מקובץ
    flourish_embed_code13 = ("""<div class="flourish-embed flourish-pictogram" data-src="visualisation/21092416"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21092416/thumbnail" width="100%" alt="pictogram visualization" /></noscript></div>""")
    st.components.v1.html(flourish_embed_code13, height=650)
    # #השכלת אם אחוזים מקובץ
    flourish_embed_code14 = ("""<div class="flourish-embed flourish-pictogram" data-src="visualisation/21097218"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21097218/thumbnail" width="100%" alt="pictogram visualization" /></noscript></div>""")
    st.components.v1.html(flourish_embed_code14, height=650)
    st.subheader('רמת ההשכלה לפי מספר ילדים - 2202')
    flourish_embed_code99 = ("""<div class="flourish-embed flourish-chart" data-src="visualisation/21186004"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21186004/thumbnail" width="100%" alt="chart visualization" /></noscript></div>""")
    st.components.v1.html(flourish_embed_code99, height=650)


#עמוד 3
if page == '***רמת השכלה עולים ויורדים***':
    st.header('השכלה של עולים ויורדים לפי שנים')
    with st.expander('הגדרות והסברים'):
     st.write("""יורדים מהארץ הינם יורדים חדשים שלא הופיעו בשנה הקודמת כיורדים. 
                  בנוסף, יורדים אשר יש להם אזרחות, אך לא תושבות, אינם נחשבים בחישוב זה. 
                  כמו כן, אוכלוסיית היורדים לא כלולה באוכלוסיית המרשם שמוצגת בכל החלקים האחרים של הודעה זו.""")
        #יורדים
    st.markdown("---") 
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

if page == '***השכלה לפי פיקוח***':
    st.header('השכלה של בוגרי מערכת החינוך לפי סוג פיקוח')
    with st.expander('הגדרות והסברים'):
     st.write("")
    st.markdown("---")
    flourish_embed_code = """<div class="flourish-embed flourish-chart" data-src="visualisation/21046767"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/21046767/thumbnail" width="100%" alt="chart visualization" /></noscript></div>"""
    st.components.v1.html(flourish_embed_code, height=650)


#טעינת נתונים למפה


data = pd.DataFrame([
    {"שם עיר": "אופקים", "סך תושבים": 19747, "ממוצע שנות לימוד": 12.67, "אחוז אקדמאים": "16%"},
    {"שם עיר": "ירושלים", "סך תושבים": 498671, "ממוצע שנות לימוד": 12.62, "אחוז אקדמאים": "20%"},
    {"שם עיר": "אור יהודה", "סך תושבים": 20934, "ממוצע שנות לימוד": 12.32, "אחוז אקדמאים": "16%"},
    {"שם עיר": "אור עקיבא", "סך תושבים": 12282, "ממוצע שנות לימוד": 12.71, "אחוז אקדמאים": "21%"},
    {"שם עיר": "אילת", "סך תושבים": 37649, "ממוצע שנות לימוד": 12.65, "אחוז אקדמאים": "17%"},
    {"שם עיר": "אלעד", "סך תושבים": 21777, "ממוצע שנות לימוד": 12.62, "אחוז אקדמאים": "10%"},
    {"שם עיר": "אריאל", "סך תושבים": 11099, "ממוצע שנות לימוד": 13.62, "אחוז אקדמאים": "32%"},
    {"שם עיר": "אשדוד", "סך תושבים": 126697, "ממוצע שנות לימוד": 12.96, "אחוז אקדמאים": "22%"},
    {"שם עיר": "אשקלון", "סך תושבים": 85893, "ממוצע שנות לימוד": 12.94, "אחוז אקדמאים": "24%"},
    {"שם עיר": "באר יעקב", "סך תושבים": 15403, "ממוצע שנות לימוד": 13.41, "אחוז אקדמאים": "33%"},
    {"שם עיר": "באר שבע", "סך תושבים": 119251, "ממוצע שנות לימוד": 13.19, "אחוז אקדמאים": "26%"},
    {"שם עיר": "בית שמש", "סך תושבים": 65424, "ממוצע שנות לימוד": 12.61, "אחוז אקדמאים": "15%"},
    {"שם עיר": "ביתר עילית", "סך תושבים": 27376, "ממוצע שנות לימוד": 12.48, "אחוז אקדמאים": "8%"},
    {"שם עיר": "בני ברק", "סך תושבים": 94179, "ממוצע שנות לימוד": 12.56, "אחוז אקדמאים": "8%"},
    {"שם עיר": "בת ים", "סך תושבים": 72172, "ממוצע שנות לימוד": 12.63, "אחוז אקדמאים": "21%"},
    {"שם עיר": "גבעת זאב", "סך תושבים": 10227, "ממוצע שנות לימוד": 13.17, "אחוז אקדמאים": "22%"},
    {"שם עיר": "גבעת שמואל", "סך תושבים": 15141, "ממוצע שנות לימוד": 14.68, "אחוז אקדמאים": "51%"},
    {"שם עיר": "גבעתיים", "סך תושבים": 33675, "ממוצע שנות לימוד": 14.70, "אחוז אקדמאים": "54%"},
    {"שם עיר": "גדרה", "סך תושבים": 15987, "ממוצע שנות לימוד": 13.73, "אחוז אקדמאים": "36%"},
    {"שם עיר": "גן יבנה", "סך תושבים": 14744, "ממוצע שנות לימוד": 13.49, "אחוז אקדמאים": "30%"},
    {"שם עיר": "גני תקווה", "סך תושבים": 12214, "ממוצע שנות לימוד": 14.35, "אחוז אקדמאים": "48%"},
    {"שם עיר": "דימונה", "סך תושבים": 22607, "ממוצע שנות לימוד": 12.59, "אחוז אקדמאים": "15%"},
    {"שם עיר": "הוד השרון", "סך תושבים": 36356, "ממוצע שנות לימוד": 14.30, "אחוז אקדמאים": "47%"},
    {"שם עיר": "הרצלייה", "סך תושבים": 56034, "ממוצע שנות לימוד": 14.12, "אחוז אקדמאים": "44%"},
    {"שם עיר": "זכרון יעקב", "סך תושבים": 13719, "ממוצע שנות לימוד": 14.39, "אחוז אקדמאים": "44%"},
    {"שם עיר": "חדרה", "סך תושבים": 58087, "ממוצע שנות לימוד": 12.99, "אחוז אקדמאים": "25%"},
    {"שם עיר": "חולון", "סך תושבים": 106843, "ממוצע שנות לימוד": 13.01, "אחוז אקדמאים": "25%"},
    {"שם עיר": "חיפה", "סך תושבים": 156365, "ממוצע שנות לימוד": 13.83, "אחוז אקדמאים": "38%"},
    {"שם עיר": "חריש", "סך תושבים": 14342, "ממוצע שנות לימוד": 13.34, "אחוז אקדמאים": "30%"},
    {"שם עיר": "טבריה", "סך תושבים": 27209, "ממוצע שנות לימוד": 12.43, "אחוז אקדמאים": "14%"},
    {"שם עיר": "טירת כרמל", "סך תושבים": 16340, "ממוצע שנות לימוד": 12.77, "אחוז אקדמאים": "22%"},
    {"שם עיר": "יבנה", "סך תושבים": 30044, "ממוצע שנות לימוד": 13.230787, "אחוז אקדמאים": "29.32%"},
    {"שם עיר": "יהוד-מונוסון", "סך תושבים": 17484, "ממוצע שנות לימוד": 13.442345, "אחוז אקדמאים": "31.41%"},
    {"שם עיר": "יקנעם עילית", "סך תושבים": 14730, "ממוצע שנות לימוד": 13.724499, "אחוז אקדמאים": "35.39%"},
    {"שם עיר": "ירושלים", "סך תושבים": 498671, "ממוצע שנות לימוד": 12.619081, "אחוז אקדמאים": "20.12%"},
    {"שם עיר": "כפר יונה", "סך תושבים": 15755, "ממוצע שנות לימוד": 13.459411, "אחוז אקדמאים": "32.45%"},
    {"שם עיר": "כפר סבא", "סך תושבים": 53997, "ממוצע שנות לימוד": 14.112280, "אחוז אקדמאים": "43.95%"},
    {"שם עיר": "כרמיאל", "סך תושבים": 27477, "ממוצע שנות לימוד": 13.489346, "אחוז אקדמאים": "30.73%"},
    {"שם עיר": "לוד", "סך תושבים": 44838, "ממוצע שנות לימוד": 12.314208, "אחוז אקדמאים": "16.60%"},
    {"שם עיר": "מבשרת ציון", "סך תושבים": 14057, "ממוצע שנות לימוד": 14.076644, "אחוז אקדמאים": "39.86%"},
    {"שם עיר": "מגדל העמק", "סך תושבים": 15645, "ממוצע שנות לימוד": 12.778773, "אחוז אקדמאים": "20.38%"},
    {"שם עיר": "מודיעין עילית", "סך תושבים": 31038, "ממוצע שנות לימוד": 12.479105, "אחוז אקדמאים": "5.25%"},
    {"שם עיר": "מודיעין-מכבים-רעות", "סך תושבים": 55761, "ממוצע שנות לימוד": 14.517803, "אחוז אקדמאים": "48.79%"},
    {"שם עיר": "מעלה אדומים", "סך תושבים": 22610, "ממוצע שנות לימוד": 13.318434, "אחוז אקדמאים": "27.92%"},
    {"שם עיר": "מעלות-תרשיחא", "סך תושבים": 13843, "ממוצע שנות לימוד": 13.142942, "אחוז אקדמאים": "25.97%"},
    {"שם עיר": "נהרייה", "סך תושבים": 37348, "ממוצע שנות לימוד": 13.348558, "אחוז אקדמאים": "29.18%"},
    {"שם עיר": "נוף הגליל", "סך תושבים": 26913, "ממוצע שנות לימוד": 13.017353, "אחוז אקדמאים": "25.66%"},
    {"שם עיר": "נס ציונה", "סך תושבים": 26601, "ממוצע שנות לימוד": 14.116044, "אחוז אקדמאים": "42.83%"},
    {"שם עיר": "נשר", "סך תושבים": 13299, "ממוצע שנות לימוד": 13.675150, "אחוז אקדמאים": "33.85%"},
    {"שם עיר": "נתיבות", "סך תושבים": 23657, "ממוצע שנות לימוד": 12.746535, "אחוז אקדמאים": "16.65%"},
    {"שם עיר": "נתניה", "סך תושבים": 123797, "ממוצע שנות לימוד": 13.115908, "אחוז אקדמאים": "27.65%"},
    {"שם עיר": "עכו", "סך תושבים": 31501, "ממוצע שנות לימוד": 12.529035, "אחוז אקדמאים": "19.16%"},
    {"שם עיר": "עפולה", "סך תושבים": 34161, "ממוצע שנות לימוד": 12.819169, "אחוז אקדמאים": "21.66%"},
    {"שם עיר": "ערד", "סך תושבים": 14563, "ממוצע שנות לימוד": 12.727286, "אחוז אקדמאים": "17.91%"},
    {"שם עיר": "פרדס חנה-כרכור", "סך תושבים": 24527, "ממוצע שנות לימוד": 13.642721, "אחוז אקדמאים": "35.76%"},
    {"שם עיר": "פתח תקווה", "סך תושבים": 141162, "ממוצע שנות לימוד": 13.488574, "אחוז אקדמאים": "32.67%"},
    {"שם עיר": "צפת", "סך תושבים": 18961, "ממוצע שנות לימוד": 12.724565, "אחוז אקדמאים": "17.42%"},
    {"שם עיר": "קדימה-צורן", "סך תושבים": 13439, "ממוצע שנות לימוד": 13.915972, "אחוז אקדמאים": "40.02%"},
    {"שם עיר": "קריית אונו", "סך תושבים": 21660, "ממוצע שנות לימוד": 14.535836, "אחוז אקדמאים": "49.60%"},
    {"שם עיר": "קריית אתא", "סך תושבים": 34903, "ממוצע שנות לימוד": 12.868393, "אחוז אקדמאים": "22.01%"},
    {"שם עיר": "קריית ביאליק", "סך תושבים": 24481, "ממוצע שנות לימוד": 13.240555, "אחוז אקדמאים": "28.75%"},
    {"שם עיר": "קריית גת", "סך תושבים": 34566, "ממוצע שנות לימוד": 12.523638, "אחוז אקדמאים": "17.19%"},
    {"שם עיר": "קריית ים", "סך תושבים": 22516, "ממוצע שנות לימוד": 12.753016, "אחוז אקדמאים": "21.86%"},
    {"שם עיר": "קריית מוצקין", "סך תושבים": 27169, "ממוצע שנות לימוד": 13.398307, "אחוז אקדמאים": "31.83%"},
    {"שם עיר": "קריית מלאכי", "סך תושבים": 14514, "ממוצע שנות לימוד": 12.183430, "אחוז אקדמאים": "14.31%"},
    {"שם עיר": "קריית שמונה", "סך תושבים": 13828, "ממוצע שנות לימוד": 12.807203, "אחוז אקדמאים": "20.39%"},
    {"שם עיר": "ראש העין", "סך תושבים": 41957, "ממוצע שנות לימוד": 13.624574, "אחוז אקדמאים": "33.87%"},
    {"שם עיר": "ראשון לציון", "סך תושבים": 148044, "ממוצע שנות לימוד": 13.366782, "אחוז אקדמאים": "30.87%"},
    {"שם עיר": "רחובות", "סך תושבים": 78589, "ממוצע שנות לימוד": 13.857703, "אחוז אקדמאים": "37.66%"},
    {"שם עיר": "רמלה", "סך תושבים": 45027, "ממוצע שנות לימוד": 12.114326, "אחוז אקדמאים": "13.66%"},
    {"שם עיר": "רמת גן", "סך תושבים": 93549, "ממוצע שנות לימוד": 14.089227, "אחוז אקדמאים": "42.82%"},
    {"שם עיר": "רמת השרון", "סך תושבים": 24587, "ממוצע שנות לימוד": 14.436776, "אחוז אקדמאים": "48.94%"},
    {"שם עיר": "רעננה", "סך תושבים": 44643, "ממוצע שנות לימוד": 14.332212, "אחוז אקדמאים": "46.50%"},
    {"שם עיר": "שדרות", "סך תושבים": 18446, "ממוצע שנות לימוד": 12.865587, "אחוז אקדמאים": "21.91%"},
    {"שם עיר": "שוהם", "סך תושבים": 14122, "ממוצע שנות לימוד": 14.440458, "אחוז אקדמאים": "47.38%"},
    {"שם עיר": "תל אביב -יפו", "סך תושבים": 294955, "ממוצע שנות לימוד": 14.248440, "אחוז אקדמאים": "46.43%"}
    # Add more rows as needed...
])
# Coordinates extracted from the geocoding results
coordinates = {
    "אור יהודה": (32.0270045, 34.8629898),
    "אור עקיבא": (32.5090151, 34.9195677),      
    "אילת": (29.5569348, 34.9497949),
    "אופקים": (31.307984, 34.623876),
    "אלעד": (32.0500659, 34.9521522),
    "ירושלים": (31.7901047, 35.2032791),
    "אריאל": (32.101755, 35.174367),
    "אשדוד": (31.7977314, 34.6529922),
    "אשקלון": (31.6644874, 34.5730157),
    "באר יעקב": (31.9443532, 34.8398648),
    "באר שבע": (31.2457442, 34.7925181),
    "בית שמש": (31.746214, 34.9886825),
    "ביתר עילית": (31.6995816, 35.1061772),
    "בני ברק": (32.0873899, 34.8324376),
    "בת ים": (32.0154565, 34.7505283),
    "גבעת שמואל": (32.0769463, 34.8524656),
    "גבעתיים": (32.0729606, 34.8113279),
    "גדרה": (31.8117747, 34.7803882),
    "גן יבנה": (31.787109, 34.7096635),
    "גני תקווה": (32.0604256, 34.8760954),
    "דימונה": (31.0686612, 35.0366482),
    "הוד השרון": (32.1561974, 34.8930354),
    "זכרון יעקב": (32.5711587, 34.9529966),
    "חדרה": (32.43699, 34.9198258),
    "חולון": (32.0193121, 34.7804076),
    "חיפה": (32.8191218, 34.9983856),
    "חריש": (32.45964, 35.0510843),
    "טבריה": (32.7938522, 35.5328566),
    "טירת כרמל": (32.7613834, 34.9715506),
    "יבנה": (31.8768863, 34.7382974),
    "יהוד מונוסון": (32.0331756, 34.8907527),
    "יקנעם עילית": (32.6480601, 35.0943545),
    "ירושלים": (31.7788242, 35.2257626),
    "כפר יונה": (32.314504, 34.9321169),
    "כפר סבא": (32.1773471, 34.907459),
    "כרמיאל": (32.9159104, 35.293429),
    "לוד": (31.9489012, 34.8884857),
    "מבשרת ציון": (31.8057198, 35.152731),
    "מגדל העמק": (32.6765744, 35.2413237),
    "מודיעין-מכבים-רעות": (31.9085744, 35.0069297),
    "אחדות ישראל": (31.79129415, 35.30821679460022),
    "מעלות תרשיחא": (33.0157394, 35.2759666), 
    "מעלה אדומים": (31.784756, 35.308291),
    "נהריה": (33.006306, 35.0945579),
    "נוף הגליל": (32.7023065, 35.3183216),
    "נס ציונה": (31.9295577, 34.7990609),
    "נשר": (32.7708797, 35.0381249),
    "נתיבות": (31.4213546, 34.5884252),
    "נתניה": (32.3286181, 34.8566246),
    "עכו": (32.9281731, 35.0756378),
    "עפולה": (32.6075587, 35.2890861),
    "ערד": (31.2612199, 35.214581),
    "פרדס חנה - כרכור": (32.475041, 34.9761087),
    "פתח תקווה": (32.0877639, 34.8859985),
    "צפת": (32.9646301, 35.502451),
    "קדימה - צורן": (32.2764459, 34.9125436),
    "קריית אונו": (32.0591691, 34.8594303),
    "קריית אתא": (32.8074348, 35.1172559),
    "קריית ביאליק": (32.836685849999995, 35.08933425565027),
    "קריית גת": (31.6031494, 34.7779274),
    "קריית ים": (32.84674545, 35.07017111795361),
    "קריית מוצקין": (32.83905315, 35.08038934735784),
    "קריית מלאכי": (31.728968, 34.745991),
    "קרית שמונה": (33.2074733, 35.5707828),
    "ראש העין": (32.0952929, 34.9533225),
    "ראשון לציון": (31.9635712, 34.8101149),
    "רחובות": (31.8952532, 34.8105616),
    "רמלה": (31.9279988, 34.8623473),
    "רמת גן": (32.0686867, 34.8246812),
    "רמת השרון": (32.1431276, 34.8380853),
    "רעננה": (32.1860244, 34.8678359),
    "שדרות": (31.526474, 34.5969696),
    "שהם": (32.0004845, 34.9465419),
    "תל־אביב–יפו": (32.0852997, 34.7818064)
    # Add more cities as needed...
}

# Add latitude and longitude columns
data["Latitude"] = data["שם עיר"].map(lambda city: coordinates[city][0] if city in coordinates else None)
data["Longitude"] = data["שם עיר"].map(lambda city: coordinates[city][1] if city in coordinates else None)


# Remove cities without coordinates
data = data.dropna(subset=["Latitude", "Longitude"])
flourish_embed_code24 = ("""<div class="flourish-embed flourish-scatter" data-src="visualisation/14738347"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/14738347/thumbnail" width="100%" alt="scatter visualization" /></noscript></div>""")
if page == '***מפת ישראל - השכלה לפי ישוב***':
    # Streamlit interface
    st.header("מפת ישראל - השכלה לפי ישוב")
    st.markdown("הקטע הזה מציג את מפת ישראל, המראה את ההשכלה לפי ישוב.")

    if "show_graph" not in st.session_state:
        st.session_state.show_graph = False

    # Function to toggle graph visibility
    def toggle_graph():
        st.session_state.show_graph = not st.session_state.show_graph

    # Add a button to toggle the graph visibility
    if st.button("מתאם שנות לימוד ואחוז אקדמאים", on_click=toggle_graph):
        pass

    # Display the Flourish embed graph if the state is set to True
    if st.session_state.show_graph:
        st.components.v1.html(flourish_embed_code24, height=650)


    # Creating the map
    with st.expander('הגדרות והסברים'):
        st.write("נכללו ערים מעל 000,02 תושבים")
    st.markdown("---") 
    m = folium.Map(location=[31.0461, 34.8516], zoom_start=8)

    for _, row in data.iterrows():
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 14px; text-align: right; direction: rtl; padding: 5px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);">
            <b style="color: #333;">שם עיר:</b> {row['שם עיר']}<br>
            <b style="color: #333;">סך תושבים:</b> {row['סך תושבים']}<br>
            <b style="color: #333;">ממוצע שנות לימוד:</b> {row['ממוצע שנות לימוד']}<br>
            <b style="color: #333;">אחוז אקדמאים:</b> {row['אחוז אקדמאים']}
        </div>
        """
        popup = folium.Popup(popup_html, max_width=300)

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup,
            icon=folium.Icon(color="blue", icon="user"),
        ).add_to(m)


    st_folium(m, width=1400, height=1000)

#############################################################

def extract_text_from_pdf(pdf_paths):
    text = ""
    for pdf_path in pdf_paths:
        # Open the PDF using fitz.open, handle both paths and BytesIO objects
        if isinstance(pdf_path, io.BytesIO):  # Check if it's a BytesIO object
            try:
                doc = fitz.open(stream=pdf_path.getvalue(), filetype="pdf")  # Open using the bytes and filetype
            except fitz.FileDataError:
                print(f"Skipping invalid PDF: {pdf_path}")  # Print a message for invalid PDFs
                continue  # Move to the next PDF
        else:
            doc = fitz.open(pdf_path)  # Open using the file path if it's not a BytesIO object

        for page in doc:
            text += page.get_text("text") + "\n"
    return text

pdf_url = "https://www.cbs.gov.il/he/mediarelease/DocLib/2025/040/06_25_040b.pdf"

response = requests.get(pdf_url)

pdf_paths = []

# Check if the request was successful and content type is PDF
if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
    # Get the PDF content as bytes
    pdf_content = response.content

    # Create an in-memory file-like object using BytesIO
    pdf_file = io.BytesIO(pdf_content)
    pdf_paths.append(pdf_file)
else:
    print(f"Skipping URL: {pdf_url} (Status: {response.status_code}, Content-Type: {response.headers.get('content-type', 'Unknown')})")

pdf_text = extract_text_from_pdf(pdf_paths)

API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCcbPr9UOv_ggP1M4xfEsHVQv7WWjCDy_o")
genai.configure(api_key=API_KEY)

# Initialize chat model
model = genai.GenerativeModel("gemini-pro")



# Convert DataFrame to a list of dictionaries
city_data = data.to_dict(orient="records")



def get_response(user_question):
    try:
        response = model.generate_content([
            "You are an AI assistant answering based on provided Israel Education Register data.",
            f"Here is the city data: {city_data}",
            f"Here is the general education data: {pdf_text}",
            f"The user question: {user_question}"
        ])
        return response.text
    except:
        return "הגעת למגבלת השאלות המותרת .. נסה שוב יותר מאוחר "


if page == "***צ'אט בוט - מרשם השכלה***":
    st.header("צ'אט בוט - מרשם השכלה")
    col1, col2 = st.columns(2)
    with col1:
         st.markdown(f"""בינה מלאכותית מבוססת נתוני מרשם ההשכלה כפי שפורסמו: """)
    with col2:
         st.page_link(pdf_url, label="להודעה המלאה", icon= '🎓')
    user_question = st.text_input("הקלד שאלה..")
    
    if st.button("קבל תשובה"):
        if user_question:
            with st.spinner("אנא המתן..."):
                answer = get_response(user_question)  # Get AI response
            st.write("#### מרשם השכלה:")
            st.markdown(f'##### {answer}')  # Use markdown for styling
        else:
            st.warning("אנא הקלד שאלה לפני קבלת תשובה..")

