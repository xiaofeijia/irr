import numpy as np
from scipy.optimize import root
import streamlit as st

# Streamlit app
st.title("Internal Rate of Return (IRR) Calculator")
st.markdown("Calculate the IRR for a series of annual deposits and a final payout.")

# Input parameters
col1, col2, col3 = st.columns(3)
with col1:
    annual_deposit = st.number_input("Annual Deposit", value=-4062.50, step=100.0)
with col2:
    deposit_years = st.number_input("Years of Deposits", value=20, min_value=1, step=1)
with col3:
    final_amount = st.number_input("Final Amount", value=495913.00, step=1000.0)
total_years = st.number_input("Total Investment Period (Years)", value=46, min_value=1, step=1)

# Calculate IRR
if st.button("Calculate IRR"):
    # Generate cash flows
    cash_flows = [annual_deposit] * deposit_years + [0] * (total_years - deposit_years) + [final_amount]
    
    # Define NPV function
    def npv(r):
        return sum(cf / (1 + r) ** (i + 1) for i, cf in enumerate(cash_flows))
    
    # Solve for IRR
    sol = root(npv, x0=0.05)
    if sol.success:
        irr = sol.x[0]
        st.success(f"**IRR = {irr:.4f} or {irr * 100:.2f}%**")
        
        # Show cash flows
        st.subheader("Cash Flow Timeline")
        st.write(f"First {deposit_years} years: Annual deposit of ${annual_deposit:,.2f}")
        st.write(f"Next {total_years - deposit_years} years: No deposits")
        st.write(f"Final year: Payout of ${final_amount:,.2f}")
        
        # Display cash flows as a table
        st.table(
            [{"Year": i+1, "Cash Flow": f"${cf:,.2f}"} 
             for i, cf in enumerate(cash_flows)]
        )
    else:
        st.error("Failed to converge. Try adjusting the inputs.")

        # """ git init
        #     git add irr_calculator.py
        #     git commit -m "First commit"
        #     git branch -M main
        #     git remote add irr https://github.com/xiaofeijia/irr_calculator.git
        #     git push -u irr main """