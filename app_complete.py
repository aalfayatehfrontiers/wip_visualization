import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    df_filtered = df_authors_contactable[
        (df_authors_contactable['release_date'].dt.date >= start_date) & 
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
section = st.sidebar.radio(
    "Select a Section",
    ("Completeness", "Contactable", "Disambiguation"),
    index=0  # Default section is Contactable
)

# Add icons for each section
icon_completeness = ":bar_chart:"  # Replace with a person icon if needed
icon_contactable = ":email:"  # Email icon
icon_disambiguation = ":gear:"  # Engine icon

# Show the selected section content
if section == "Completeness":
    st.sidebar.markdown(f"**{icon_completeness} Completeness**")
    show_completeness()
elif section == "Contactable":
    st.sidebar.markdown(f"**{icon_contactable} Contactable**")
    show_contactable()
elif section == "Disambiguation":
    st.sidebar.markdown(f"**{icon_disambiguation} Disambiguation**")
    show_disambiguation()
