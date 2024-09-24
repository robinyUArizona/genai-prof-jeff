
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
    for i in range(1, num_payments + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        amortization_data.append([i, monthly_payment, principal_payment, interest_payment, max(balance, 0)])

    # Create DataFrame
    df = pd.DataFrame(amortization_data, columns=['Month', 'Payment', 'Principal', 'Interest', 'Balance'])
    return df

# Streamlit App
st.title('Loan Amortization Calculator')

# Input Fields
loan_amount = st.number_input('Loan Amount', value=300000.0, min_value=0.0, step=1000.0)
annual_rate = st.number_input('Annual Interest Rate (%)', value=7.5, min_value=0.0, step=0.1)
years = st.number_input('Loan Term (years)', value=30, min_value=1, step=1)

# Calculate amortization table
if st.button('Calculate Amortization Table'):
    amortization_df = calculate_amortization(loan_amount, annual_rate, years)
    st.write(f'Monthly Payment: ${amortization_df["Payment"][0]:,.2f}')
    st.dataframe(amortization_df)

    # Downloadable CSV
    csv = amortization_df.to_csv(index=False)
    st.download_button(label="Download Amortization Table as CSV", data=csv, file_name='amortization_schedule.csv', mime='text/csv')
