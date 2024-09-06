import streamlit as st

from projections import Mortgage, Property, PropertyInvestment


def main():
    st.title("Property Investment Little Helper")

    # Section: Investment details
    st.header("Investment Details")
    investment_outlook_years = st.slider("Investment Outlook (Years)", 5, 30, 10)

    # Section: Mortgage details
    st.header("Mortgage Details")
    price = st.number_input("Property Price (€)", value=300000)
    tax_rate = st.slider("Property Purchase Tax Rate (%)", 0.0, 30.0, 10.0, 5.0, format="%.0f%%") / 100
    down_payment_rate = st.slider("Down Payment Rate (%)", 0.0, 30.0, 20.0, 5.0, format="%.0f%%") / 100
    mortgage_rate = st.slider("Mortgage Rate (%)", 0.0, 5.0, 3.0, 0.1, format="%.1f%%") / 100
    years = st.slider("Mortgage Term (Years)", 10, 30, 30)

    # Section: property details
    st.header("Property Details")
    property_growth_rate = st.slider("Property Anual Growth Rate (%)", 0.0, 7.0, 2.0, 0.5, format="%.1f%%") / 100
    annual_net_income = st.number_input("Monthly Net Income", value=1200) * 12

    mortgage = Mortgage(price, down_payment_rate, mortgage_rate, years)
    property = Property(price, property_growth_rate, tax_rate, annual_net_income)

    # Create PropertyInvestment instance
    investment = PropertyInvestment(property, mortgage, 0, investment_outlook_years)
    investment.run()

    # Display Mortgage summary in a nice layout
    st.header("Mortgage Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Mortgage down payment:", f"€{price * down_payment_rate:,.0f}")
    col2.metric("Property tax payment:", f"€{price * tax_rate:,.0f}")
    col3.metric("Initial Inversion:", f"€{price * (tax_rate + down_payment_rate):,.0f}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Installment", f"€{mortgage.installment:,.0f}")
    col2.metric("Loan Amount", f"€{mortgage.loan_amount:,.0f}")
    col3.metric(f"Total Payment Over {years} Years", f"€{mortgage.total_payment:,.0f}")

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
