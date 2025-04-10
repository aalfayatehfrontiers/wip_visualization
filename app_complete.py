import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Data as a multiline string
data = """
bucket_0000,bucket_0001,bucket_0010,bucket_0011,bucket_0100,bucket_0101,bucket_0110,bucket_0111,bucket_1000,bucket_1001,bucket_1010,bucket_1011,bucket_1100,bucket_1101,bucket_1110,bucket_1111,release,number_base_authors,number_complete_authors,number_potential_om,number_potential_um,number_potential_um_fx,score_complete_avg,completeness_percentage
582935,133,108186,1629,144680,63,33607,155,10829036,198513,3434810,167528,5469434,246387,9657286,3798592,2024-07-17,34672974,3798592,0,0,0,2.1563360270163154,0.5390840067540789
587094,130,109990,1627,143715,65,33900,157,10849120,256124,3440493,176607,5478208,309395,9771523,3892145,2024-08-14,35050293,3892145,0,0,0,2.1644730616089287,0.5411182654022322
595591,131,113035,1640,148566,62,33566,152,11001374,258024,3478698,175219,5569941,335281,9870425,3962831,2024-10-02,35544536,3962831,0,0,0,2.1646512139024687,0.5411628034756172
594625,123,117686,1641,143437,64,34083,153,11152880,268453,3542677,190113,5698411,372772,9871799,4178469,2024-11-20,36167386,4178469,0,2920937,1917913,2.1711044032875364,0.5427761008218841
525029,111,97629,1342,133506,87,33593,146,9472001,238848,3118813,168504,4853567,346155,9404366,4176058,2025-01-08,32569755,4176058,568248,3023879,2002490,2.2308270971028183,0.5577067742757046
450761,69,112455,1323,67212,110,28138,214,9574255,199261,3204345,172364,4937085,350717,9176548,4294367,2025-01-22,32569224,4294367,591144,3631221,2291531,2.2343643189042512,0.5585910797260628
431306,73,113426,1378,68591,102,28437,187,10094844,213328,3410678,184416,5225166,398181,9503705,4426898,2025-02-26,34100716,4426898,635386,3757826,2432370,2.2287558712843447,0.5571889678210862
427963,72,112927,1390,68040,98,28501,188,10112261,214082,3432838,189363,5036462,399542,9447498,4508275,2025-03-19,33979500,4508275,657933,3820117,2492028,2.2326083373798906,0.5581520843449727
589126,126,117055,1641,141923,77,33907,152,11116691,265929,3544673,189749,5621818,378782,9863647,4190025,2024-12-11,36055321,4190025,643222,2993207,1977662,2.1735758502885054,0.5433939625721264
427383,78,111390,1378,67735,103,28233,189,9875600,208466,3335328,181304,5012530,380586,9419574,4379552,2025-02-05,33429429,4379552,620497,3704944,2368187,2.2342602980146626,0.5585650745036657
432740,79,113269,1393,69884,98,28564,190,10549847,222833,3485094,194749,5547049,428085,9501700,4556525,2025-03-26,35132099,4556525,662131,3835823,2506101,2.2174426014227047,0.5543606503556762
581969,137,108375,1626,144043,63,33691,155,10723272,198608,3427415,167128,5335627,243564,9668178,3800583,2024-07-24,34434434,3800583,0,0,0,2.1608978384834203,0.5402244596208551
584080,133,110243,1628,142765,64,33507,153,10749682,253898,3433183,178232,5281352,303366,9742375,3894575,2024-08-21,34709236,3894575,0,0,0,2.1683209909892573,0.5420802477473143
588841,134,112204,1639,142480,62,33514,153,10984498,259989,3469115,177354,5450015,319728,9791020,3939956,2024-09-11,35270702,3939956,0,0,0,2.1630579680551865,0.5407644920137966
590323,126,115968,1642,142294,64,33891,152,10943760,267176,3481895,187908,5487508,360343,9817300,4125251,2024-10-30,35555601,4125251,0,2860861,1852632,2.1753144603012053,0.5438286150753013
402737,75,95133,1312,65799,103,27484,176,9601488,206884,3232199,173011,4787644,338088,9598367,4232209,2025-01-15,32762709,4232209,575798,3040931,2012887,2.2443659649756067,0.5610914912439017
430820,75,113239,1369,68985,103,28645,188,10154352,215982,3460667,187076,5184534,404212,9552161,4467549,2025-03-12,34269957,4467549,651560,3808517,2481686,2.2299519663826834,0.5574879915956709
589601,135,109641,1610,145328,64,33887,158,10832457,262626,3445512,176569,5448903,306655,9726196,3886858,2024-08-07,34966200,3886858,0,0,0,2.1634873392018577,0.5408718348004644
593841,135,111976,1627,144267,63,33530,151,11014918,261603,3467358,176935,5646090,324792,9790250,3924166,2024-09-04,35491702,3924166,0,0,0,2.1600791644198973,0.5400197911049743
588036,129,112568,1638,141602,61,33439,153,10950315,253102,3460272,174705,5506918,331665,9816734,3953324,2024-09-25,35324661,3953324,0,0,0,2.1655845756028627,0.5413961439007157
594396,126,118643,1640,143439,77,34229,152,11140782,265935,3576526,191393,5633085,372665,9913493,4193703,2024-11-27,36180284,4193703,0,2938689,1932861,2.1733907616645576,0.5433476904161394
585264,129,113405,1635,141841,64,33731,151,10817373,265305,3476113,185134,5336995,350647,9854788,4051068,2024-10-16,35213643,4051068,0,2855362,1811458,2.177476099249373,0.5443690248123433
431635,73,112768,1369,69047,100,28440,188,10131761,213665,3437237,185597,5231759,399833,9523748,4445191,2025-03-05,34212411,4445191,649905,3781324,2458267,2.228654712466771,0.5571636781166928
558486,135,93200,1604,142752,61,33268,145,10687002,204904,3403786,167500,5397742,246138,9574379,3790589,2024-07-03,34301691,3790589,0,0,0,2.161195522401505,0.5402988806003762
588834,127,113948,1630,142771,64,33763,152,10999827,268464,3477850,186959,5618114,360958,9809554,4105630,2024-10-23,35708645,4105630,0,2858579,1834132,2.171794309193194,0.5429485772982985
432927,78,113853,1379,68421,103,28393,187,9956690,212532,3367093,182612,5103890,387487,9443946,4395310,2025-02-12,33694901,4395310,621657,3734539,2410341,2.231487725694757,0.5578719314236893
435025,83,113315,1306,73221,104,28636,199,10695844,230206,3510528,199887,5705088,450596,9490240,4619316,2025-04-03,35553594,4619316,678458,3843306,2512674,2.214522363055617,0.5536305907639042
590793,129,113333,1648,142891,62,33640,151,11027783,260802,3497062,175900,5527994,338107,9897063,3974705,2024-10-09,35582063,3974705,0,0,0,2.165670804416259,0.5414177011040647
593382,125,118364,1641,143003,77,34115,152,11146396,265642,3562666,190622,5658178,373518,9900839,4190026,2024-12-03,36178746,4190026,629439,2971483,1959999,2.172768039002789,0.5431920097506973
555387,124,104863,1346,138962,77,33255,150,10456306,250866,3321151,180087,5511669,373536,9677300,4157154,2024-12-18,34762233,4157154,645842,3013155,1993703,2.193726104994463,0.5484315262486158
427630,76,113523,1378,68450,102,28348,185,10026038,213562,3394537,183278,5147318,392633,9472122,4411999,2025-02-19,33881179,4411999,628184,3741967,2417111,2.230478077519085,0.5576195193797713
587009,136,110494,1628,143513,64,33497,153,10859461,257141,3440292,176261,5485779,312299,9767982,3897761,2024-08-28,35073470,3897761,0,0,0,2.164357703985377,0.5410894259963442
593612,126,117061,1643,144739,65,34094,150,10987365,265915,3528374,190106,5408001,363055,9850326,4173600,2024-11-13,35658232,4173600,0,2904727,1903291,2.177078942107954,0.5442697355269885
592025,122,116878,1641,142479,64,33998,147,11047003,266997,3530714,189858,5598156,365890,9878732,4153456,2024-11-06,35918160,4153456,0,2877770,1875500,2.174034722268624,0.543508680567156
587431,133,112323,1641,141725,62,33428,154,10958989,252807,3457017,174676,5492338,327602,9803150,3946435,2024-09-18,35289911,3946435,0,0,0,2.164648190810116,0.541162047702529
426204,80,112172,1380,67492,100,28484,189,9952324,208276,3342680,178283,4996640,379411,9292673,4396022,2025-02-15,33335045,4396022,617404,3701562,2400857,2.2325147968893977,0.5578531683378683
""" 

# Reading the data into a pandas DataFrame
df_all_kpis = pd.read_csv(StringIO(data))

# Function for Completeness section
def show_completeness():
    st.title("Profile Completeness Details")
    # st.write("This section is all about completeness.")
    # Add content related to Completeness here

# Function for Contactable section
def show_contactable():
    st.title("Profile Contactable Details")
    # st.write("This section contains Profile Contactable Details.")
    
    # Creating a pandas DataFrame (This assumes 'data' is already defined somewhere)
    # Example structure for df_authors_contactable
    data = {
        'release_date': ['2025-01-01', '2025-02-01', '2025-03-01'],
        'contactable_authors': [50, 60, 70],
        'non_contactable_authors': [30, 25, 20],
    }
    
    df_authors_contactable = pd.DataFrame(data)

    # Convert 'release_date' to datetime
    df_authors_contactable['release_date'] = pd.to_datetime(df_authors_contactable['release_date'])
    df_authors_contactable = df_authors_contactable.sort_values(by='release_date')

    # Extract unique dates from the 'release_date' column
    unique_dates = pd.to_datetime(df_authors_contactable['release_date']).dt.date.unique()

    # Sort dates
    unique_dates.sort()

    # Display Start Date and End Date Selectors
    start_date = st.selectbox("Select Start Release Date", options=unique_dates, index=0)
    end_date = st.selectbox("Select End Release Date", options=unique_dates, index=len(unique_dates) - 1)

    # Filter the DataFrame based on the selected start and end date range
    df_filtered = df_authors_contactable[(
        df_authors_contactable['release_date'].dt.date >= start_date) & 
        (df_authors_contactable['release_date'].dt.date <= end_date)
    ] 

    if not df_filtered.empty:
        # Calculate the overall contactable percentage at the end date
        end_data = df_filtered[df_filtered['release_date'].dt.date == end_date].iloc[-1]
        contactable_end = end_data['contactable_authors']
        non_contactable_end = end_data['non_contactable_authors']
        
        overall_contactable_percentage = (contactable_end / (contactable_end + non_contactable_end)) * 100

        # Calculate the percentage change for contactable authors from start to end date
        start_data = df_filtered[df_filtered['release_date'].dt.date == start_date].iloc[0]
        contactable_start = start_data['contactable_authors']
        pct_change_contactable = ((contactable_end - contactable_start) / contactable_start) * 100

        # Create the line plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_filtered['release_date'],
            y=df_filtered['contactable_authors'],
            mode='lines',
            name='Contactable Authors'
        ))
        fig.add_trace(go.Scatter(
            x=df_filtered['release_date'],
            y=df_filtered['non_contactable_authors'],
            mode='lines',
            name='Non-Contactable Authors'
        ))

        # Update layout with customized title
        fig.update_layout(
            title=dict(
                text="Contactable Trend",
                font=dict(
                    size=25,        # Set your desired font size
                    weight='normal' # Set the font weight to normal to remove bold
                )
            ),
            xaxis=dict(
                title="Release Date",
                rangeslider=dict(visible=True),
                type="date"
            ),
            yaxis=dict(title="# Authors"),
            showlegend=True
        )
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)

        # Apply custom CSS to adjust font sizes and layout
        st.markdown("""
        <style>
        .big-font {
            font-size: 100px !important;
            text-align: left;
        }
        .small-font {
            font-size: 36px !important;
            text-align: left;
        }
        .title-font {
            font-size: 25px !important;
            font-weight: bold;
            text-align: left;
        }
        .numbers-container {
            display: flex;
            justify-content: left;
            align-items: left;
            gap: 30px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Display Overall Contactable Percentage Title
        st.markdown('<div class="title-font">Overall Percentage Contactable</div>', unsafe_allow_html=True)
        
        # Corrected f-string formatting for color and arrow symbols
        color = "green" if pct_change_contactable >= 0 else "red"
        arrow_symbol = "▲" if pct_change_contactable >= 0 else "▼"
        
        # Display numbers side by side in the same column
        st.markdown(f'''
            <div class="numbers-container">
                <div class="big-font">{overall_contactable_percentage:.2f}%</div>
                <div class="small-font" style="color: {color};">
                    {arrow_symbol} {pct_change_contactable:.2f}%
                </div>
            </div>
        ''', unsafe_allow_html=True)

    else:
        st.warning("No data available for the selected date range.")

# Function for Disambiguation section
def show_disambiguation():
    st.title("Profile Disambiguation Details ")
    # st.write("This section is about Disambiguation.")
    # Add content related to Disambiguation here

# Create a sidebar with navigation
st.sidebar.title("Navigate")

# Add icons for each section
icon_completeness = ":clipboard:"  # Person or profile icon
icon_contactable = ":email:"  # Email icon
icon_disambiguation = ":gear:"  # Engine icon

# Use markdown to display the icon and section name inline in the radio button
section = st.sidebar.radio(
    "Select a Section",
    (
        f"{icon_completeness} Completeness", 
        f"{icon_contactable} Contactable", 
        f"{icon_disambiguation} Disambiguation"
    ),
    index=0  # Default section is Completeness
)

# Show the selected section content
if section == f"{icon_completeness} Completeness":
    show_completeness()
elif section == f"{icon_contactable} Contactable":
    show_contactable()
elif section == f"{icon_disambiguation} Disambiguation":
    show_disambiguation()
