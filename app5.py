
import streamlit as st
import pandas as pd

# Function to calculate loan amortization
def calculate_amortization(loan_amount, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    num_payments = years * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

    # Create amortization schedule
    amortization_data = []
    balance = loan_amount
    total_interest = 0
    for i in range(1, num_payments + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        total_interest += interest_payment
        amortization_data.append([i, monthly_payment, principal_payment, interest_payment, max(balance, 0)])

    # Create DataFrame
    df = pd.DataFrame(amortization_data, columns=['Month', 'Payment', 'Principal', 'Interest', 'Balance'])
    return df, monthly_payment, total_interest

# Initialize session state to store calculations
if 'calculations' not in st.session_state:
    st.session_state['calculations'] = []

# Streamlit App
st.title('Loan Amortization Calculator')

# Input Fields
loan_amount = st.number_input('Loan Amount', value=300000.0, min_value=0.0, step=1000.0)
annual_rate = st.number_input('Annual Interest Rate (%)', value=7.5, min_value=0.0, step=0.1)
years = st.number_input('Loan Term (years)', value=30, min_value=1, step=1)

# Calculate amortization table
if st.button('Calculate Amortization Table'):
    amortization_df, monthly_payment, total_interest = calculate_amortization(loan_amount, annual_rate, years)
    st.write(f'Monthly Payment: ${monthly_payment:,.2f}')
    st.write(f'Total Interest Paid: ${total_interest:,.2f}')
    st.dataframe(amortization_df)

    # Save the current calculation to session state
    st.session_state['calculations'].append({
        'Loan Amount': loan_amount,
        'Annual Rate (%)': annual_rate,
        'Years': years,
        'Monthly Payment': monthly_payment,
        'Total Interest': total_interest
    })

# Display saved calculations
if st.session_state['calculations']:
    st.subheader('Saved Loan Calculations')
    comparison_df = pd.DataFrame(st.session_state['calculations'])
    st.dataframe(comparison_df)

    # Downloadable CSV of all saved calculations
    csv = comparison_df.to_csv(index=False)
    st.download_button(label="Download Comparison Table as CSV", data=csv, file_name='loan_comparisons.csv', mime='text/csv')

    # Clear all calculations
    if st.button('Clear All Calculations'):
        st.session_state['calculations'].clear()
