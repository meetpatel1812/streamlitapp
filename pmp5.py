import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# File path for the Excel file
EXCEL_FILE_PATH = 'projects.xlsx'

# Function to load data from Excel
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        # Convert 'Date' column to string
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
        # Ensure the new column exists in case it was added later
        if 'Total Contribution Correct' not in df.columns:
            df['Total Contribution Correct'] = df.apply(
                lambda row: (row['Meet\'s Contribution (%)'] + row['Spandan\'s Contribution (%)'] + row['Srey\'s Contribution (%)']) == 100,
                axis=1
            )
        return df
    except FileNotFoundError:
        # Initialize DataFrame with columns if the file does not exist
        return pd.DataFrame(columns=[
            'Number', 'Client Name', 'Business Name', 'Date', 'Services',
            'Payment Got (%)', 'Quote', 'Amount Total', 'Transfer Method',
            'Meet\'s Contribution (%)', 'Meet\'s Part', 'Spandan\'s Contribution (%)',
            'Spandan\'s Part', 'Srey\'s Contribution (%)', 'Srey\'s Part',
            'Total Contribution Correct'
        ])

# Function to save data to Excel
def save_data(df):
    # Convert 'Date' column to datetime before saving
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.to_excel(EXCEL_FILE_PATH, index=False)

# Sidebar for input
st.sidebar.header('Create/Update Project')

number = st.sidebar.text_input('Number')
client_name = st.sidebar.text_input('Client Name')
business_name = st.sidebar.text_input('Business Name')
date = st.sidebar.date_input('Date')
services = st.sidebar.selectbox('Services', ['Business cards/flyer', 'Web Development'], key='services_selectbox')
payment_got_percentage = st.sidebar.number_input('Payment Got (%)', min_value=0.0, max_value=100.0, format="%.2f", key='payment_got')
quote = st.sidebar.number_input('Quote', min_value=0.0, format="%.2f", key='quote')
amount_total = st.sidebar.number_input('Amount Total', min_value=0.0, format="%.2f", key='amount_total')
transfer_method = st.sidebar.selectbox('Transfer Method', ['Account', 'Cash'], key='transfer_method')

meet_contribution = st.sidebar.number_input('Meet\'s Contribution (%)', min_value=0.0, max_value=100.0, format="%.2f", key='meet_contribution')
spandan_contribution = st.sidebar.number_input('Spandan\'s Contribution (%)', min_value=0.0, max_value=100.0, format="%.2f", key='spandan_contribution')
srey_contribution = st.sidebar.number_input('Srey\'s Contribution (%)', min_value=0.0, max_value=100.0, format="%.2f", key='srey_contribution')

# Handling form submission
if st.sidebar.button('Submit'):
    payment_got = (payment_got_percentage * amount_total) / 100
    meet_part = (meet_contribution * payment_got) / 100
    spandan_part = (spandan_contribution * payment_got) / 100
    srey_part = (srey_contribution * payment_got) / 100

    new_row = pd.DataFrame({
        'Number': [number],
        'Client Name': [client_name],
        'Business Name': [business_name],
        'Date': [date],
        'Services': [services],
        'Payment Got (%)': [payment_got_percentage],
        'Quote': [quote],
        'Amount Total': [amount_total],
        'Transfer Method': [transfer_method],
        'Meet\'s Contribution (%)': [meet_contribution],
        'Meet\'s Part': [meet_part],
        'Spandan\'s Contribution (%)': [spandan_contribution],
        'Spandan\'s Part': [spandan_part],
        'Srey\'s Contribution (%)': [srey_contribution],
        'Srey\'s Part': [srey_part],
        'Total Contribution Correct': [(meet_contribution + spandan_contribution + srey_contribution) == 100]
    })

    df = load_data()  # Reload data from Excel

    if number in df['Number'].values:
        # Update existing entry
        df.loc[df['Number'] == number] = new_row.values[0]
    else:
        # Add new row to DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    # Save DataFrame to Excel
    save_data(df)

# Display existing entries with edit options
st.title('Project Management Dashboard')

df = load_data()  # Reload data from Excel

# Editing selected entry
st.sidebar.header('Edit Project')

# Select an entry to edit
edit_number = st.sidebar.selectbox('Select Project Number to Edit', options=df['Number'].tolist(), key='edit_number')

if edit_number:
    # Find the row to edit
    edit_row = df[df['Number'] == edit_number].iloc[0]
    
    st.sidebar.write(f"Editing Project: {edit_number}")

    # Pre-fill the sidebar inputs with the existing data
    client_name = st.sidebar.text_input('Client Name', edit_row['Client Name'], key='edit_client_name')
    business_name = st.sidebar.text_input('Business Name', edit_row['Business Name'], key='edit_business_name')
    services = st.sidebar.selectbox('Services', ['Business cards/flyer', 'Web Development'], index=['Business cards/flyer', 'Web Development'].index(edit_row['Services']), key='edit_services')
    payment_got_percentage = st.sidebar.number_input('Payment Got (%)', min_value=0.0, max_value=100.0, format="%.2f", value=float(edit_row['Payment Got (%)']), key='edit_payment_got')
    quote = st.sidebar.number_input('Quote', min_value=0.0, format="%.2f", value=float(edit_row['Quote']), key='edit_quote')
    amount_total = st.sidebar.number_input('Amount Total', min_value=0.0, format="%.2f", value=float(edit_row['Amount Total']), key='edit_amount_total')
    transfer_method = st.sidebar.selectbox('Transfer Method', ['Account', 'Cash'], index=['Account', 'Cash'].index(edit_row['Transfer Method']), key='edit_transfer_method')

    meet_contribution = st.sidebar.number_input('Meet\'s Contribution (%)', min_value=0.0, max_value=100.0, format="%.2f", value=float(edit_row['Meet\'s Contribution (%)']), key='edit_meet_contribution')
    spandan_contribution = st.sidebar.number_input('Spandan\'s Contribution (%)', min_value=0.0, max_value=100.0, format="%.2f", value=float(edit_row['Spandan\'s Contribution (%)']), key='edit_spandan_contribution')
    srey_contribution = st.sidebar.number_input('Srey\'s Contribution (%)', min_value=0.0, max_value=100.0, format="%.2f", value=float(edit_row['Srey\'s Contribution (%)']), key='edit_srey_contribution')

    if st.sidebar.button('Update'):
        payment_got = (payment_got_percentage * amount_total) / 100
        meet_part = (meet_contribution * payment_got) / 100
        spandan_part = (spandan_contribution * payment_got) / 100
        srey_part = (srey_contribution * payment_got) / 100

        updated_row = pd.DataFrame({
            'Number': [edit_number],
            'Client Name': [client_name],
            'Business Name': [business_name],
            'Date': [edit_row['Date']],  # Keep the old date
            'Services': [services],
            'Payment Got (%)': [payment_got_percentage],
            'Quote': [quote],
            'Amount Total': [amount_total],
            'Transfer Method': [transfer_method],
            'Meet\'s Contribution (%)': [meet_contribution],
            'Meet\'s Part': [meet_part],
            'Spandan\'s Contribution (%)': [spandan_contribution],
            'Spandan\'s Part': [spandan_part],
            'Srey\'s Contribution (%)': [srey_contribution],
            'Srey\'s Part': [srey_part],
            'Total Contribution Correct': [(meet_contribution + spandan_contribution + srey_contribution) == 100]
        })

        df = load_data()  # Reload data from Excel
        # Remove the old row and add the updated row
        df = df[df['Number'] != edit_number]
        df = pd.concat([df, updated_row], ignore_index=True)

        # Save DataFrame to Excel
        save_data(df)

# Display the DataFrame
st.write('### Projects DataFrame')
st.dataframe(df)

# Create bar graph
st.write('### Client Payment Got (%)')
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(kind='bar', x='Client Name', y='Payment Got (%)', ax=ax, color='skyblue')
plt.xticks(rotation=45)
plt.xlabel('Client Name')
plt.ylabel('Payment Got (%)')
plt.title('Client Name vs Payment Got (%)')
st.pyplot(fig)


# Create table for clients whose total contributions are not 100%
df = load_data()  # Reload data from Excel

# Filter rows where Payment Got (%) is not equal to 100%
incorrect_payment_df = df[df['Payment Got (%)'] != 100]

# Display the filtered DataFrame with only 'Client Name' and 'Payment Got (%)'
st.write('### Clients with Payment Got (%) Not Equal to 100%')
st.dataframe(incorrect_payment_df[['Client Name', 'Payment Got (%)']])
