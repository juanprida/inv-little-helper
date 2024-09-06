import streamlit as st

from projections import Mortgage, Property


def main():
    st.title("Property Investment Little Helper")

    # Section: Investment details
    st.header("Investment Details")
    investment_outlook_years = st.slider("Investment Outlook (Years)", 5, 30, 10)

    # Section: Mortgage details
    st.header("Mortgage Details")
    property_price = st.number_input("Property Price (€)", value=300000)
    property_purchase_tax_rate = (
        st.slider("Property Purchase Tax Rate (%)", 0.0, 30.0, 10.0, 5.0, format="%.0f%%") / 100
    )
    mortgage_down_payment_rate = st.slider("Down Payment Rate (%)", 0.0, 50.0, 20.0, 5.0, format="%.0f%%") / 100
    property_other_expenses = st.number_input("Other Expenses (€)", value=0)
    mortgage_rate = st.slider("Mortgage Rate (%)", 0.0, 5.0, 3.0, 0.1, format="%.1f%%") / 100
    mortgage_years = st.slider("Mortgage Term (Years)", 10, 30, 30)

    # Section: property details
    st.header("Property Details")
    property_growth_rate = st.slider("Property Anual Growth Rate (%)", 0.0, 15.0, 2.0, 0.5, format="%.1f%%") / 100
    property_annual_net_income = st.number_input("Monthly Net Income", value=1200) * 12

    mortgage = Mortgage(property_price, mortgage_down_payment_rate, mortgage_rate, mortgage_years)

    # Create PropertyInvestment instance
    investment = Property(
        mortgage=mortgage,
        price=property_price,
        years=investment_outlook_years,
        growth_rate=property_growth_rate,
        annual_income=property_annual_net_income,
        purchase_tax_rate=property_purchase_tax_rate,
        initial_extra_expenses=property_other_expenses,
    )

    investment.run()

    # Display Mortgage summary in a nice layout
    st.header("Mortgage Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mortgage down payment:", f"€{property_price * mortgage_down_payment_rate:,.0f}")
    col2.metric("Property tax payment:", f"€{property_price * property_purchase_tax_rate:,.0f}")
    col3.metric("Other expenses:", f"€{property_other_expenses:,.0f}")
    col4.metric(
        "Initial Inversion:",
        f"€{property_price * (mortgage_down_payment_rate + property_purchase_tax_rate) + property_other_expenses:,.0f}",
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Installment", f"€{mortgage.installment:,.0f}")
    col2.metric("Loan Amount", f"€{mortgage.loan_amount:,.0f}")
    col3.metric(f"Total Payment Over {mortgage_years} Years", f"€{mortgage.total_payment:,.0f}")

    st.header("Investment Summary")
    # Display key metrics with metrics and columns for better structure
    col1, col2, col3 = st.columns(3)
    col1.metric("IRR", f"{investment.irr * 100:.1f}%")
    col2.metric("Payback Period", f"{investment.payback_period} years")
    col3.metric("NPV", f"€ {investment.npv:,.0f}")

    # Second row for additional metrics
    col1, col2 = st.columns(2)
    col1.metric("Profitability Index (PI)", f"{investment.profitability_index:.2f}")
    col2.metric("Rent to Price Ratio", f"{investment.rent_to_price_ratio * 100:.2f}%")

    # Plot investment analysis
    st.subheader("Investment Analysis")

    benefits_fig = investment.plot_time_series("Benefits", investment.benefits)
    st.plotly_chart(benefits_fig)

    benefits_fig = investment.plot_time_series("Cumulative benefits", investment.cum_benefits)
    st.plotly_chart(benefits_fig)


if __name__ == "__main__":
    main()
