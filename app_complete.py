import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO
from plotly.subplots import make_subplots

# Data as a multiline string
data = """
bucket_0000,bucket_0001,bucket_0010,bucket_0011,bucket_0100,bucket_0101,bucket_0110,bucket_0111,bucket_1000,bucket_1001,bucket_1010,bucket_1011,bucket_1100,bucket_1101,bucket_1110,bucket_1111,release,number_base_authors,number_complete_authors,number_contactable_authors,percentage_complete_authors,percentage_contactable_authors,number_potential_om,number_potential_om_wretractions,number_potential_um,number_potential_um_fx,score_complete_avg,completeness_score_percentage,score_contactable_avg,contactable_score_percentage,kpi_undermerge,kpi_overmerge,kpi_overmerge_ret
567344,149,110248,1674,136607,62,32234,152,10799577,326267,3562367,289025,5389521,331487,9421336,3916725,2024-10-09,34884775,3916725,3224412,0.11227605739179915,0.09243035106289205,0,0,0,0,2.1632282564528507,0.5408070641132127,2.1297196843035393,0.5324299210758848,0.0,0.0,0.0
575482,150,113736,1668,137390,65,32866,155,10700426,278934,3455488,223072,5393117,355660,9502781,4084199,2024-10-30,34855189,4084199,3365806,0.11717621155346482,0.0965654210051766,0,0,2860861,1852632,2.1763697221667626,0.5440924305416907,2.1453193382483167,0.5363298345620792,0.6475784737531813,0.0,0.0
588328,150,117832,1674,141251,78,33791,155,11097625,281496,3606091,220474,5604041,378034,9836717,4192615,2024-12-18,36100352,4192615,3556337,0.11613778724373656,0.09851252973932222,652817,14611,3013155,1993703,2.1741560857910747,0.5435390214477687,2.1480805505719167,0.5370201376429792,0.6616662601160578,0.018083397081557543,0.00040473289567924436
506146,97,128604,1654,78790,115,30461,225,10289936,230787,3574717,231853,5068345,356195,9543084,4371043,2025-01-22,34412052,4371043,3800621,0.1270207019331483,0.11044447451142989,601389,13650,3631221,2291531,2.2139867741685384,0.5534966935421346,2.1904924762987106,0.5476231190746776,0.6310634907652275,0.01747611563530126,0.0003966633550361949
492720,109,134203,1712,80670,107,31011,199,10861074,245768,3854237,244622,5314393,400766,10020997,4521596,2025-02-19,36204184,4521596,3970199,0.1248915318737746,0.10966133085612426,640360,14718,3741967,2417111,2.2112540362738184,0.5528135090684546,2.1897640891450556,0.5474410222862639,0.6459466371563405,0.017687458444029563,0.00040652759913053143
553463,153,105930,1652,133877,63,31365,153,10398846,322017,3331726,272718,5271577,302027,9024826,3795863,2024-08-28,33546256,3795863,3013673,0.11315310417949473,0.08983634418100189,0,0,0,0,2.1623345985316513,0.5405836496329128,2.1236659614116102,0.5309164903529026,0.0,0.0,0.0
573185,150,111535,1655,137609,65,32681,155,10735923,279762,3439752,223607,5513023,355869,9455712,4059628,2024-10-23,34920311,4059628,3328401,0.11625406199847418,0.09531418548935604,0,0,2858579,1834132,2.1724787617154955,0.5431196904288739,2.1408081102141385,0.5352020275535346,0.6416236878533005,0.0,0.0
579006,149,115076,1669,138382,65,33179,150,10821908,279060,3502967,221662,5517156,361713,9601574,4116862,2024-11-06,35290578,4116862,3408108,0.11665612277588652,0.09657274528062419,0,0,2877770,1875500,2.1752676309240386,0.5438169077310097,2.1452518573087693,0.5363129643271923,0.6517199081233038,0.0,0.0
582217,152,115468,1671,140937,66,33333,153,10768116,275206,3484650,216925,5336904,359208,9612436,4140594,2024-11-13,35068036,4140594,3444088,0.11807316497564906,0.09821160215530747,0,0,2904727,1903291,2.1791033578270538,0.5447758394567634,2.1496476164219747,0.5374119041054937,0.6552392014808965,0.0,0.0
586176,150,116466,1672,140561,65,33554,156,11005057,279019,3533913,217582,5651243,370306,9720574,4159479,2024-11-20,35815973,4159479,3471801,0.11613474803546452,0.09693443202003754,0,0,2920937,1917913,2.1729113990565048,0.5432278497641262,2.1445594400018115,0.5361398600004529,0.6566088210735117,0.0,0.0
587130,149,117674,1675,141002,78,33761,155,11028186,278586,3588116,220362,5595817,370698,9800925,4181164,2024-11-27,35945478,4181164,3504860,0.11631961049453843,0.09750489338325116,0,0,2938689,1932861,2.1750761806533774,0.5437690451633443,2.1473214516718904,0.5368303629179726,0.6577290077309984,0.0,0.0
588263,150,117818,1676,141235,78,33790,155,11086117,279501,3604277,220478,5608737,378113,9835264,4190202,2024-12-11,36085854,4190202,3539674,0.11611757892718848,0.09809034864465173,648509,14562,2993207,1977662,2.1743776938187467,0.5435944234546867,2.1477725038736786,0.5369431259684196,0.6607167496267381,0.017971280380395045,0.0004035376300087009
505947,114,138488,1714,83473,107,31748,204,11548383,256570,4073430,262998,5757573,439064,10274227,4707546,2025-03-26,38081586,4707546,4172338,0.12361738295248523,0.1095631363672721,677078,15105,3835823,2506101,2.1998139730839994,0.5499534932709998,2.1798652503601086,0.5449663125900271,0.653341147388709,0.017779669155586115,0.00039664839589401553
509298,123,139297,1627,86845,113,31860,213,11719944,268679,4113984,274204,5923184,462240,10301372,4778138,2025-04-03,38611121,4778138,4249663,0.12375030499632476,0.11006318619964439,693991,15191,3843306,2512674,2.1975985105431155,0.5493996276357789,2.1780542450450997,0.5445135612612749,0.6537793243629313,0.01797386302252141,0.00039343587045815117
512708,144,87139,1624,129151,58,30072,144,9892190,261687,3015649,237951,5098935,231365,8464802,3625098,2024-07-03,31588717,3625098,2556569,0.11475926673438494,0.08093297996243405,0,0,0,0,2.1598804408548786,0.5399701102137197,2.1068453017575863,0.5267113254393966,0.0,0.0,0.0
540240,147,102769,1647,131334,60,30740,154,10071950,261123,3160493,247447,5073748,230926,8714432,3659642,2024-07-24,32226852,3659642,2567848,0.11355878011293191,0.07968038578512106,0,0,0,0,2.1590463443342216,0.5397615860835554,2.1060522448795185,0.5265130612198796,0.0,0.0,0.0
571202,151,109697,1666,141981,62,32071,153,10744748,324778,3518182,285544,5418959,328125,9351785,3898027,2024-10-02,34727131,3898027,3192304,0.11224730888365066,0.0919253594545429,0,0,0,0,2.1619102942883477,0.5404775735720869,2.1276689110885663,0.5319172277721416,0.0,0.0,0.0
457264,101,111070,1635,76985,107,29687,185,10318173,241797,3635439,245616,4911625,343901,9912831,4302810,2025-01-15,34589226,4302810,3717014,0.12439740629061778,0.1074616124685762,586007,13475,3040931,2012887,2.2222453893591028,0.5555613473397757,2.1974146516027853,0.5493536629006963,0.6619311651596173,0.016941893987451467,0.0003895721748731816
561965,149,109119,1664,134517,61,31888,154,10665221,321771,3471043,281861,5341143,323955,9260046,3882058,2024-09-25,34386615,3882058,3162609,0.11289445035517454,0.0919720943745117,0,0,0,0,2.1627725206450243,0.5406931301612561,2.1276598757976033,0.5319149689494008,0.0,0.0,0.0
588074,149,117788,1676,141191,78,33783,155,11083757,281805,3601686,220911,5634476,372252,9830158,4184351,2024-12-03,36092290,4184351,3518293,0.11593476058183064,0.09748045912298721,634373,14491,2971483,1959999,2.1738084505028636,0.5434521126257159,2.146510570540135,0.5366276426350337,0.6596029659264414,0.01757641313421786,0.00040149849178314814
549432,150,105497,1651,132647,63,31318,153,10269279,319578,3299438,270303,5060590,293322,8969412,3787094,2024-08-21,33089927,3787094,2993144,0.11444854502096666,0.09045483841653686,0,0,0,0,2.166242161851853,0.5415605404629632,2.1265913339730247,0.5316478334932562,0.0,0.0,0.0
497208,108,134751,1712,80944,107,31126,201,10955918,247666,3890777,247091,5397648,406703,10086714,4543316,2025-02-26,36521990,4543316,3994177,0.12439946454177332,0.10936361901418844,648205,14801,3757826,2432370,2.209769620987246,0.5524424052468115,2.1885373168329547,0.5471343292082387,0.6472811673558062,0.01774834832384544,0.00040526269242174373
499543,107,137065,1714,81481,107,31613,202,11098418,250640,3998349,256634,5241751,410107,10183111,4652433,2025-03-19,36843275,4652433,4114230,0.12627631501271264,0.1116684116707866,672605,15074,3820117,2492028,2.212759669166218,0.5531899172915545,2.1920215561727345,0.5480053890431836,0.6523433706349832,0.0182558418055941,0.0004091384384260085
559161,150,108114,1664,134410,61,31646,153,10580736,322765,3407275,278543,5252081,310538,9115035,3849240,2024-09-11,33951572,3849240,3098596,0.11337442637413078,0.09126517028430967,0,0,0,0,2.160847250312887,0.5402118125782217,2.1239795906946517,0.5309948976736629,0.0,0.0,0.0
550603,146,104293,1631,133369,61,31056,157,10230292,321560,3230314,262359,5198326,294775,8831626,3758572,2024-08-07,32949140,3758572,2937062,0.11407193025371831,0.08913926129786695,0,0,0,0,2.1619694778073115,0.5404923694518279,2.121034600599591,0.5302586501498977,0.0,0.0,0.0
560411,150,108684,1665,134366,61,31815,155,10639630,318896,3443738,279955,5318741,319340,9211244,3869392,2024-09-18,34238243,3869392,3133500,0.11301374314096667,0.09152046733239202,0,0,0,0,2.161977529045518,0.5404943822613795,2.1261166935464533,0.5315291733866133,0.0,0.0,0.0
491274,111,133459,1709,80170,109,30872,198,10732426,242438,3786960,241322,5257074,394713,9921508,4491420,2025-02-12,35805763,4491420,3937930,0.12543846642787643,0.10998034031560786,633139,14659,3734539,2410341,2.212587761361209,0.5531469403403022,2.1907894268305355,0.5476973567076339,0.6454186179338334,0.01768260042384797,0.00040940336894929453
565380,149,110642,1660,136351,64,32513,153,10574813,288851,3499703,248674,5211338,345090,9419817,4001067,2024-10-16,34436265,4001067,3276106,0.11618760048454732,0.095135346414601,0,0,2855362,1811458,2.176068833248902,0.5440172083122256,2.142938440042786,0.5357346100106966,0.6344057250884476,0.0,0.0
499288,108,135471,1705,81625,106,31255,202,11023538,248096,3939630,249321,5410135,408796,10142979,4568641,2025-03-05,36740896,4568641,4021754,0.12434756626512321,0.109462599932239,663135,14865,3781324,2458267,2.209555640668099,0.5523889101670247,2.188529016820929,0.5471322542052323,0.6501074755826266,0.018048961026971143,0.00040459002415183345
549767,147,104913,1648,132709,63,31205,156,10293157,322131,3261045,265265,5236034,297980,8913329,3770699,2024-08-14,33180248,3770699,2961957,0.11364288175302367,0.08926868177718261,0,0,0,0,2.162375760422285,0.5405939401055713,2.122239441971621,0.5305598604929053,0.0,0.0,0.0
562112,151,107607,1651,135332,62,31495,151,10579987,325001,3380759,275872,5439021,315080,9079582,3826503,2024-09-04,34060366,3826503,3060995,0.11234474109878913,0.08986970369020697,0,0,0,0,2.157848861635838,0.5394622154089594,2.120425452856261,0.5301063632140652,0.0,0.0,0.0
560242,138,111647,1660,136547,90,34299,151,10151749,267184,3450990,210998,4966735,350984,9671878,4232290,2025-01-08,34147582,4232290,3639360,0.12394113293292626,0.10657738518645332,575790,13383,3023879,2002490,2.21020598178811,0.5525514954470275,2.1846287388664885,0.5461571847166221,0.6622255718565458,0.016861808839056306,0.00039191647596014263
484894,111,130057,1708,79458,109,30671,200,10644305,243535,3737907,238996,5159308,387478,9859297,4468927,2025-02-05,35466961,4468927,3913892,0.12600253514813406,0.1103531819374093,631742,14518,3704944,2368187,2.214286924667721,0.5535717311669303,2.192174739752865,0.5480436849382162,0.6391964358975466,0.01781212661552818,0.0004093387082135399
500154,110,136634,1703,81766,108,31528,201,11068384,249041,3984525,252277,5371469,413632,10209011,4597901,2025-03-12,36898444,4597901,4053260,0.12460961768469153,0.1098490765626865,665341,14956,3808517,2481686,2.210949843847074,0.5527374609617685,2.190092975194293,0.5475232437985732,0.6516147886434536,0.01803168176956188,0.0004053287450278391
513584,125,139558,1621,87354,113,31909,210,11715179,271107,4127052,275290,5813032,458881,10316534,4791261,2025-04-09,38542810,4791261,4266153,0.12431011127626657,0.110686091647184,710490,15312,3865327,2531144,2.1988452061486954,0.5497113015371738,2.179306153339624,0.544826538334906,0.6548330839796995,0.01843378829929629,0.00039727253928813184
540619,143,102484,1650,131776,60,30628,154,10144418,260454,3138606,245852,5199349,233233,8671386,3651375,2024-07-17,32352187,3651375,2564335,0.11286331276460537,0.07926311133154615,0,0,0,0,2.15434245604478,0.538585614011195,2.1017040053582776,0.5254260013395694,0.0,0.0,0.0
482098,107,129674,1715,78982,107,30612,199,10502526,240733,3713260,238632,4992485,378186,9809499,4454513,2025-01-29,35053328,4454513,3888639,0.12707817642878302,0.11093494460782725,618104,14354,3678899,2345298,2.218525813012676,0.554631453253169,2.195736593113213,0.5489341482783032,0.6374999694201988,0.017633247262570904,0.00040949036279807726
""" 

# Reading the data into a pandas DataFrame
df_all_kpis = pd.read_csv(StringIO(data))

def show_completeness():
    st.title("Profile Completeness Details")

    # Convert 'release' to datetime and sort
    df_all_kpis['release'] = pd.to_datetime(df_all_kpis['release'])
    df_all_kpis.sort_values('release', inplace=True)

    # Sidebar date range selection
    unique_releases = df_all_kpis['release'].dt.date.unique()
    start_date = st.selectbox("Select Start Release Date", options=unique_releases, index=0)
    end_date = st.selectbox("Select End Release Date", options=unique_releases, index=len(unique_releases) - 1)

    # Filter data
    df_filtered = df_all_kpis[
        (df_all_kpis['release'].dt.date >= start_date) &
        (df_all_kpis['release'].dt.date <= end_date)
    ].copy()

    if df_filtered.empty:
        st.warning("No data available for the selected date range.")
        return

    # Extract rows for selected start and end dates
    end_row = df_filtered[df_filtered['release'].dt.date == end_date].iloc[-1]
    start_row = df_filtered[df_filtered['release'].dt.date == start_date].iloc[0]

    # --------------------------------
    # 1) OVERALL COMPLETENESS BLOCK
    # --------------------------------
    completeness_pct = end_row['percentage_complete_authors'] * 100
    pct_change = ((end_row['number_complete_authors'] - start_row['number_complete_authors']) / start_row['number_complete_authors']) * 100
    color = "green" if pct_change >= 0 else "red"
    arrow = "▲" if pct_change >= 0 else "▼"

    st.markdown('<h3 style="font-size: 25px; font-family: Arial, sans-serif; color: black;">Overall Completeness</h3>', unsafe_allow_html=True)
    st.markdown(f'''
        <div style="display: flex; align-items: baseline; gap: 10px;">
            <div style="font-size: 48px;">{completeness_pct:.2f}%</div>
            <div style="font-size: 18px; color: {color};">{arrow} {pct_change:.2f}%</div>
        </div>
        <div style="font-size: 16px; color: gray;">Target 20% by Q4</div>
    ''', unsafe_allow_html=True)

    # --------------------------------
    # 2) COMPLETENESS TREND LINE PLOT
    # --------------------------------
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_filtered['release'],
        y=df_filtered['number_complete_authors'],
        mode='lines',
        name='Complete Authors',
        line=dict(color='royalblue', width=3)
    ))
    fig1.add_hline(
        y=5_000_000,
        line_dash="dash",
        line_color="green",
        annotation_text="Target",
        annotation_position="top right",
        annotation_font=dict(
        size=12,
        color="green"  # Change this to the color you want for the annotation text)
    ))
    fig1.update_layout(
        title="Completeness Trend",
        xaxis_title="Release Date",
        yaxis_title="# Authors",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
    )
    # Display the plot
    st.plotly_chart(fig1, use_container_width=True)

    # --------------------------------
    # 3) BARPLOT: BUCKET COMPLETENESS %
    # --------------------------------
    # Extract only columns starting with 'bucket_'
    bucket_cols = [col for col in df_all_kpis.columns if col.startswith('bucket_')]
    end_data = end_row[bucket_cols]
    
    # Derive metrics based on position of 1s in bucket name
    name_pct = end_data[end_data.index.str[7] == '1'].sum() / end_row['number_base_authors'] * 100
    affiliation_pct = end_data[end_data.index.str[8] == '1'].sum() / end_row['number_base_authors'] * 100
    hindex_pct = end_data[end_data.index.str[9] == '1'].sum() / end_row['number_base_authors'] * 100
    email_pct = end_data[end_data.index.str[10] == '1'].sum() / end_row['number_base_authors'] * 100
    all_criteria_pct = end_row['percentage_complete_authors'] * 100
    
    categories = ['Name', 'Affiliation', 'H-Index >= 1', 'Valid Email', 'All Criteria Met']
    values = [name_pct, affiliation_pct, hindex_pct, email_pct, all_criteria_pct]
    
    # Sort the categories and values by the percentage value in descending order
    sorted_categories, sorted_values = zip(*sorted(zip(categories, values), key=lambda x: x[1], reverse=False))
    
    # Create the figure
    fig2 = go.Figure()
    
    # Adding the 100% bars (overlapping the actual percentage bars)
    fig2.add_trace(go.Bar(
        y=sorted_categories,
        x=[100] * len(sorted_values),  # Each category gets a 100% value
        marker_color=['#a3c9ff' if cat != 'All Criteria Met' else '#c1e8c1' for cat in sorted_categories],  # Lighter blue and green colors
        orientation='h',  # Horizontal bars
        marker=dict(
            line=dict(
                width=3,  # Adjust border width to make the contour visible
                color=['darkgreen' if cat == 'All Criteria Met' else 'rgba(255,255,255,0)' for cat in sorted_categories]  # Dark green for the "All Criteria Met" bars
            )
        ),
        showlegend=False  # This disables the legend for the 100% bars
    ))
    
    # Adding the actual percentage bars (filled proportionally based on percentage)
    fig2.add_trace(go.Bar(
        y=sorted_categories,
        x=sorted_values,  # The actual percentage values (proportional to 100%)
        text=[f"{v:.2f}%" for v in sorted_values],  # Show percentage inside the bar
        textposition='outside',  # Position the text inside the bar
        textfont=dict(color="black", size=14),  # Set text color and size
        marker_color=['#5e8eff' if cat != 'All Criteria Met' else '#6ebd6e' for cat in sorted_categories],  # Darker blue and green colors
        name='Actual Percentage',
        orientation='h'
    ))
    
    # Define the colors for tick labels
    # tick_colors = ['#c1e8c1' if cat == 'All Criteria Met' else '#a3c9ff' for cat in sorted_categories]
    
    # Update layout for better visualization
    fig2.update_layout(
        title="Completeness by Criterion",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
        barmode='overlay',  # Overlay bars to allow overlapping
        showlegend=False,  # Remove the legend selector
        xaxis=dict(
            showgrid=False,  # Remove gridlines
            zeroline=False,  # Remove zero line
            showticklabels=False,  # Remove x-axis tick labels
        ),
        yaxis=dict(
            showgrid=False,  # Remove gridlines
            zeroline=False,  # Remove zero line
            showticklabels=True,  # Show y-axis tick labels (category names)
            tickvals=sorted_categories,  # Ensure tick labels are set properly
            ticktext=sorted_categories,  # Show the correct labels on the y-axis
            tickfont=dict(
                size=12,
                family="Arial, sans-serif, 'Comic Sans MS', sans-serif",
                color='gray'  # Default color for all categories
            ),
            tickmode='array',  # Specify that we are using an array of custom values for ticks
        ),
        plot_bgcolor='white',  # Set background to white
        margin=dict(l=50, r=50, t=50, b=50)  # Add margins for spacing
    )
    
    # Apply conditional colors to y-axis tick labels
    # fig2.layout.yaxis.tickfont.color = tick_colors
    
    # Show the plot
    st.plotly_chart(fig2, use_container_width=True)

    # --------------------------------
    # 4) AVERAGE SCORE LINE PLOT
    # --------------------------------
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_filtered['release'],
        y=df_filtered['score_complete_avg'],
        mode='lines+markers',
        name='Avg Score',
        line=dict(color='purple', width=3)
    ))
    fig3.update_layout(
        title="Average Completeness Score",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
        xaxis_title="Release Date"
    )
    st.plotly_chart(fig3, use_container_width=True)
    # Display latest value with custom styling
    # Display latest value with custom styling and lighter purple background
    st.markdown(f"""
        <div style="background-color: #f0f0f0; color: purple; padding: 20px; border-radius: 10px; font-size: 25px;">
            Current Average Completeness Score: <strong>{end_row['score_complete_avg']:.2f}/4</strong>
        </div>
    """, unsafe_allow_html=True)

# Function for Contactable section
def show_contactable():
    st.title("Profile Contactable Details")

    # Original Data
    data = {
        "release_date": [
            "2024-01-04", "2024-09-18", "2024-10-30", "2023-09-07", "2024-05-02", "2024-11-13", "2024-12-18", 
            "2023-08-31", "2023-08-03", "2025-02-12", "2024-04-18", "2023-10-26", "2024-05-16", "2024-02-08", 
            "2024-03-21", "2024-02-15", "2024-07-24", "2024-03-07", "2023-08-24", "2024-11-20", "2025-01-22", 
            "2023-07-13", "2023-09-14", "2024-06-26", "2025-03-19", "2024-02-22", "2025-03-26", "2023-11-09", 
            "2024-04-04", "2024-09-04", "2025-02-19", "2024-01-18", "2024-04-25", "2024-04-11", "2024-05-29", 
            "2024-10-02", "2025-01-29", "2024-02-01", "2024-07-03", "2025-02-05", "2024-08-14", "2024-10-09", 
            "2025-03-05", "2024-05-09", "2023-06-15", "2024-12-11", "2024-07-17", "2024-05-22", "2023-11-23", 
            "2023-09-22", "2024-10-23", "2025-02-26", "2024-02-29", "2025-01-08", "2024-11-27", "2024-08-07", 
            "2025-04-03", "2024-08-21", "2024-06-19", "2023-08-17", "2023-12-04", "2024-06-05", "2023-11-16", 
            "2025-01-15", "2024-09-25", "2023-12-14", "2024-11-06", "2024-01-11", "2024-06-12", "2024-08-28", 
            "2024-09-11", "2024-03-14", "2023-06-01", "2024-01-25", "2024-10-16", "2025-04-09"
        ]
        ,
            "contactable_authors": [
                2401045, 3133611, 3365920, 2177008, 2498479, 3444200, 3556451, 2174578, 2171952, 3938055, 2487745, 
                2330906, 2513370, 2440823, 2470018, 2445955, 2567961, 2456602, 2173302, 3471915, 3800768, 2168703, 
                2179020, 2555179, 4114358, 2450035, 4172468, 2316096, 2479308, 3061102, 3970325, 2429413, 2494133, 
                2483220, 2521810, 3192414, 3888765, 2437831, 2556673, 3914019, 2962071, 3224521, 4021884, 2505263, 
                2158447, 3539788, 2564448, 2516114, 2332185, 2306798, 3328513, 3994305, 2453509, 3639472, 3504973, 
                2937177, 4249801, 2993255, 2537459, 2173564, 2342518, 2523993, 2322837, 3717134, 3162719, 2348941, 
                3408217, 2408993, 2528582, 3013784, 3098705, 2463843, 2154091, 2432701, 3276216, 4266288
            ],
            "non_contactable_authors": [
                7702231, 9978995, 10254081, 6730326, 8993439, 10342316, 10506827, 6599616, 6080600, 10505943, 8810056, 
                6492458, 9157048, 8049600, 8481752, 8124345, 9837007, 8279583, 6451054, 10441848, 10144045, 5840612, 
                6856121, 9510931, 10753001, 8175029, 10841257, 6818896, 8686440, 9876629, 10603478, 7847162, 8922390, 
                8703896, 9292669, 10089622, 10406058, 7973030, 9563443, 10445076, 9753318, 10145926, 10721193, 9106290, 
                5324936, 10519623, 9789095, 9242200, 7071370, 6481522, 10219663, 10667052, 8239720, 10299146, 10511032, 
                9684234, 10861782, 9794722, 9555361, 6358781, 7340930, 9372221, 6989028, 10528379, 10011427, 7524933, 
                10343548, 7768536, 9457266, 9838423, 9897369, 8385618, 5300196, 7911001, 10177334, 10873626
            ],
            "total_authors": [
                10103276, 13112606, 13620001, 8907334, 11491918, 13786516, 14063278, 8774194, 8252552, 14443998, 
                11297801, 8823364, 11670418, 10490423, 10951770, 10570300, 12404968, 10736185, 8624356, 13913763, 
                13944813, 8009315, 9035141, 12066110, 14867359, 10625064, 15013725, 9134992, 11165748, 12937731, 
                14573803, 10276575, 11416523, 11187116, 11814479, 13282036, 14294823, 10410861, 12120116, 14359095, 
                12715389, 13370447, 14743077, 11611553, 7483383, 14059411, 12353543, 11758314, 9403555, 8788320, 
                13548176, 14661357, 10693229, 13938618, 14016005, 12621411, 15111583, 12787977, 12092820, 8532345, 
                9683448, 11896214, 9311865, 14245513, 13174146, 9873874, 13751765, 10177529, 11985848, 12852207, 
                12996074, 10849461, 7454287, 10343702, 13453550, 15139914
            ]
    }
    
    # DataFrame creation
    df = pd.DataFrame(data)
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['month'] = df['release_date'].dt.to_period('M').dt.to_timestamp()
    
    # Group by month and calculate mean
    df_monthly = df.groupby('month').mean(numeric_only=True).reset_index()
    
    # Create a formatted label for dropdown display
    df_monthly['month_label'] = df_monthly['month'].dt.strftime('%b-%Y')  # E.g., Jan-2024
    
    # Create a mapping from label to actual datetime
    month_label_to_date = dict(zip(df_monthly['month_label'], df_monthly['month']))
    
    # Dropdowns using labels
    start_label = st.selectbox("Select Start Month", options=df_monthly['month_label'].tolist(), index=0)
    end_label = st.selectbox("Select End Month", options=df_monthly['month_label'].tolist(), index=len(df_monthly) - 1)
    
    # Get actual dates from labels
    start_month = month_label_to_date[start_label]
    end_month = month_label_to_date[end_label]
    
    # Filter data
    df_filtered = df_monthly[
        (df_monthly['month'] >= start_month) &
        (df_monthly['month'] <= end_month)
    ]
    
    if not df_filtered.empty:
        start_data = df_filtered[df_filtered['month'] == start_month].iloc[0]
        end_data = df_filtered[df_filtered['month'] == end_month].iloc[-1]
    
        contactable_start = start_data['contactable_authors']
        contactable_end = end_data['contactable_authors']
        non_contactable_end = end_data['non_contactable_authors']
    
        overall_contactable_percentage = (contactable_end / (contactable_end + non_contactable_end)) * 100
        pct_change_contactable = ((contactable_end - contactable_start) / contactable_start) * 100
    
        # Add total authors column
        df_filtered['total_authors'] = df_filtered['contactable_authors'] + df_filtered['non_contactable_authors']
    
        # Create a subplot with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Line chart for contactable authors (primary y-axis)
        fig.add_trace(go.Scatter(
            x=df_filtered['month'],
            y=df_filtered['contactable_authors'],
            mode='lines',
            name='Contactable Audience'
        ), secondary_y=False)
        
        # Bar chart for total authors (secondary y-axis)
        fig.add_trace(go.Bar(
            x=df_filtered['month'],
            y=df_filtered['total_authors'],
            name='Total Authors',
            marker=dict(color='lightgray'),
            opacity=0.5
        ), secondary_y=True)
        
        # Update layout with your original style
        fig.update_layout(
            title=dict(
                text="Contactable Trend",
                font=dict(size=25, weight='normal')
            ),
            xaxis_title="Month",
            yaxis_title="⟨Y⟩ Authors",  # Left axis (Contactable)
            barmode='overlay',
            showlegend=True
        )
        
        # Update right y-axis label (optional: blank if not needed)
        fig.update_yaxes(
            title_text="",  # Right axis title can be empty or reused
            secondary_y=True
        )

        # Format helper
        def format_number(number):
            if number >= 1_000_000:
                return f"{number / 1_000_000:.2f}M"
            elif number >= 1_000:
                return f"{number / 1_000:.2f}K"
            return f"{number:.2f}"

        # Styling
        st.markdown("""
        <style>
            .big-font {
                font-size: 48px !important;
                text-align: left;
            }
            .small-font {
                font-size: 18px !important;
                text-align: left;
            }
            .title-container {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .title-font {
                font-size: 25px !important;
                font-weight: bold;
            }
            .numbers-container {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
            .subtitle-font {
                font-size: 16px !important;
                font-weight: normal;
                color: gray;
                text-align: left;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(
            """
            <style>
                .title-row {
                    display: flex;
                    align-items: center;
                }
        
                .title-font {
                    font-size: 25px !important;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }
        
                .tooltip-container {
                    position: relative;
                    display: inline-block;
                }
        
                .info-icon {
                    cursor: pointer;
                    font-size: 16px;
                }
        
                /* The modal container */
                .modal {
                    display: none;
                    position: fixed;
                    z-index: 1;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    overflow: auto;
                    padding-top: 60px;
                }
        
                /* Modal content */
                .modal-content {
                    background-color: #fefefe;
                    margin: 5% auto;
                    padding: 20px;
                    border: 1px solid #888;
                    width: 80%;
                    max-width: 600px;
                    border-radius: 8px;
                    font-size: 14px;
                    line-height: 1.6;
                }
        
                /* Close button */
                .close {
                    color: #aaa;
                    float: right;
                    font-size: 28px;
                    font-weight: bold;
                }
        
                .close:hover,
                .close:focus {
                    color: black;
                    text-decoration: none;
                    cursor: pointer;
                }
            </style>
        
            <div class="title-row">
                <div class="title-font">
                    Percentage Change Contactable Authors
                    <span class="tooltip-container">
                        <span class="info-icon" onclick="showModal()">ℹ️</span>
                    </span>
                </div>
            </div>
        
            <!-- Modal content -->
            <div id="myModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModal()">&times;</span>
                    <b>1. Contactable Author</b><br>
                    • H-Index ≥ 1<br>
                    • Affiliated<br>
                    • Year ≥ 2022<br>
                    • Verified email<br><br>
        
                    <b>2. Calc:</b><br>
                    • Δ% = (end − start) / start ×100<br>
                    • % = end / (end + non) ×100<br><br>
        
                    <b>3. Period:</b><br>
                    Based on monthly selection.
                </div>
            </div>
        
            <script>
                // Show the modal
                function showModal() {
                    document.getElementById("myModal").style.display = "block";
                }
        
                // Close the modal
                function closeModal() {
                    document.getElementById("myModal").style.display = "none";
                }
            </script>
            """,
            unsafe_allow_html=True
        )

        arrow = "▲" if pct_change_contactable >= 0 else "▼"
        color = "green" if pct_change_contactable >= 0 else "red"
        contactable_end_formatted = format_number(contactable_end)

        st.markdown(f'''
            <div class="numbers-container">
                <div class="big-font" style="color: {color};">
                    {arrow} {pct_change_contactable:.2f}%
                </div>
                <div class="subtitle-font">
                    <strong>Current number of contactable profiles</strong> is <strong>{contactable_end_formatted}</strong>, 
                    which represents <strong>{overall_contactable_percentage:.2f}%</strong> of all active authors.
                </div>
            </div>
        ''', unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected date range.")
        
# Function for Disambiguation section
def show_disambiguation():
    st.title("Profile Disambiguation Details ")
    # Custom styling for subtitles (underlined, bigger font, white background with black border)
    st.markdown("""
    <style>
        .subtitle-box {
            background-color: white;  /* White background */
            color: black;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 30px;  /* Bigger font size */
            font-weight: bold;
            border: 2px solid black;  /* Black border */
            border-radius: 5px;  /* Optional: rounded corners */
        }
    </style>
    """, unsafe_allow_html=True)

    # Add subtitles inside black boxes
    st.markdown('<div class="subtitle-box">Overmerged Metrics</div>', unsafe_allow_html=True)
    # Convert 'release' to datetime and sort
    df_all_kpis['release'] = pd.to_datetime(df_all_kpis['release'])
    df_all_kpis.sort_values('release', inplace=True)

    # Sidebar date range selection
    unique_releases = df_all_kpis['release'].dt.date.unique()
    start_date = st.selectbox("Select Start Release Date", options=unique_releases, index=0)
    end_date = st.selectbox("Select End Release Date", options=unique_releases, index=len(unique_releases) - 1)

    # Filter data
    df_filtered = df_all_kpis[
        (df_all_kpis['release'].dt.date >= start_date) &
        (df_all_kpis['release'].dt.date <= end_date)
    ].copy()

    if df_filtered.empty:
        st.warning("No data available for the selected date range.")
        return

    # Extract rows for selected start and end dates
    end_row = df_filtered[df_filtered['release'].dt.date == end_date].iloc[-1]
    start_row = df_filtered[df_filtered['release'].dt.date == start_date].iloc[0]

    # --------------------------------
    # 1) OVERALL OVERMERGED BLOCK
    # --------------------------------
    overmerged_pct = (end_row['number_potential_om_wretractions']  / end_row['number_base_authors']) * 100
    pct_change = ((end_row['number_potential_om_wretractions'] - start_row['number_potential_om_wretractions']) / start_row['number_potential_om_wretractions']) * 100
    color = "red" if pct_change >= 0 else "green"
    arrow = "▲" if pct_change >= 0 else "▼"

    st.markdown('<h3 style="font-size: 25px; font-family: Arial, sans-serif; color: black;">Overall OM profiles with Retractions </h3>', unsafe_allow_html=True)
    st.markdown(f'''
        <div style="display: flex; align-items: baseline; gap: 10px;">
            <div style="font-size: 48px;">{overmerged_pct:.2f}%</div>
            <div style="font-size: 18px; color: {color};">{arrow} {pct_change:.2f}%</div>
        </div>
    ''', unsafe_allow_html=True)

    # --------------------------------
    # 2) OVERMERGED TREND LINE PLOT
    # --------------------------------
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_filtered['release'],
        y=df_filtered['number_potential_om_wretractions'],
        mode='lines',
        name='Overmerged with Retractions Authors',
        line=dict(color='#5f9ea0', width=3)
    ))
    fig1.update_layout(
        title="Overmerged with Retractions Trend",
        xaxis_title="Release Date",
        yaxis_title="# Authors",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
    )

    # Display the plot
    st.plotly_chart(fig1, use_container_width=True)

    # --------------------------------
    # 3) OVERMERGED PERCENTAGE TREND LINE PLOT
    # --------------------------------
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_filtered['release'],
        y=df_filtered['number_potential_om_wretractions']/df_filtered['number_base_authors']* 100,
        mode='lines+markers',
        name='% OM with Retractions Authors',
        line=dict(color='#5f9ea0', width=1.5)
    ))
    fig2.update_layout(
        title="% OM with Retractions Overtime",
        xaxis_title="Release Date",
        yaxis_title="Percentage (%)",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
    )

    # Display the plot
    st.plotly_chart(fig2, use_container_width=True)
    # Add the subtitles
    st.markdown('<div class="subtitle-box">Undermerged Metrics</div>', unsafe_allow_html=True)
    # --------------------------------
    # 4) OVERALL UNDERMERGED BLOCK
    # --------------------------------
    undermerged_ratio_fixed = (end_row['number_potential_um_fx']  / end_row['number_potential_um'])
    pct_change_um = ((end_row['number_potential_um_fx'] - start_row['number_potential_um_fx']) / start_row['number_potential_um_fx']) * 100
    color = "green" if pct_change_um >= 0 else "red"
    arrow = "▲" if pct_change_um >= 0 else "▼"

    st.markdown('<h3 style="font-size: 25px; font-family: Arial, sans-serif; color: black;">Overall Ratio UM Profiles Fixed </h3>', unsafe_allow_html=True)
    st.markdown(f'''
        <div style="display: flex; align-items: baseline; gap: 10px;">
            <div style="font-size: 48px;">{undermerged_ratio_fixed:.2f}</div>
            <div style="font-size: 18px; color: {color};">{arrow} {pct_change_um:.2f}%</div>
        </div>
    ''', unsafe_allow_html=True)    

    # --------------------------------
    # 5) UNDERMERGED FIXED TREND LINE PLOT
    # --------------------------------
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_filtered['release'],
        y=df_filtered['number_potential_um_fx'],
        mode='lines',
        name='Undermerged fixed Authors',
        line=dict(color='#a6b4c1', width=3)
    ))
    fig3.update_layout(
        title="UM Authors Fixed Trend",
        xaxis_title="Release Date",
        yaxis_title="# Authors",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
    )
    # Display the plot
    st.plotly_chart(fig3, use_container_width=True)

    # --------------------------------
    # 6) UNDERMERGED FIXED RATIO TREND LINE PLOT
    # --------------------------------
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=df_filtered['release'],
        y=df_filtered['number_potential_um_fx']  / df_filtered['number_potential_um'],
        mode='lines+markers',
        name='Ratio UM Authors Fixed',
        line=dict(color='#a6b4c1', width=1.5)
    ))
    fig4.update_layout(
        title="Ratio UM Authors Fixed Overtime",
        xaxis_title="Release Date",
        yaxis_title="Ratio (um-fixed/um-potential)",
        title_font=dict(size=25, family="Arial, sans-serif", color="black"),
    )

    # Display the plot
    st.plotly_chart(fig4, use_container_width=True)

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
