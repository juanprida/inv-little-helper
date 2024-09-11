import streamlit as st
from projections import Mortgage, Property


def main():
    # Customize the overall theme and appearance of the app
    st.set_page_config(page_title="Property Investment Helper", layout="wide", initial_sidebar_state="expanded")

    st.title("🏡 Property Investment Little Helper")

    # Sidebar for general inputs and details
    st.sidebar.header("Investment Setup")
    investment_outlook_years = st.sidebar.slider("Investment Outlook (Years)", 5, 30, 10)

    # Section: Mortgage details
    st.sidebar.header("Mortgage Details")
    property_price = st.sidebar.number_input("Property Price (€)", value=float(300000), format="%.0f")
    property_purchase_tax_rate = (
        st.sidebar.slider("Property Purchase Tax Rate (%)", 0.0, 30.0, 10.0, 5.0, format="%.0f%%") / 100
    )
    mortgage_down_payment_rate = st.sidebar.slider("Down Payment Rate (%)", 0.0, 50.0, 20.0, 5.0, format="%.0f%%") / 100
    property_other_expenses = st.sidebar.number_input("Other Expenses (€)", value=float(0), format="%.0f")
    mortgage_rate = st.sidebar.slider("Mortgage Rate (%)", 0.0, 5.0, 3.0, 0.1, format="%.1f%%") / 100
    mortgage_years = st.sidebar.slider("Mortgage Term (Years)", 10, 30, 30)

    # Section: Property details
    st.sidebar.header("Property Details")
    property_growth_rate = (
        st.sidebar.slider("Property Annual Growth Rate (%)", 0.0, 15.0, 2.0, 0.5, format="%.1f%%") / 100
    )
    property_annual_net_income = st.sidebar.number_input("Monthly Net Income", value=1200) * 12

    # Create instances of Mortgage and Property classes
    mortgage = Mortgage(property_price, mortgage_down_payment_rate, mortgage_rate, mortgage_years)
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

    # Use tabs to organize sections and outputs
    tab1, tab2, tab3 = st.tabs(["🏠 Mortgage Summary", "📈 Investment Summary", "📊 Charts"])

    with tab1:
        st.subheader("Mortgage Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Down Payment", f"€{property_price * mortgage_down_payment_rate:,.0f}")
        col2.metric("📊 Property Tax", f"€{property_price * property_purchase_tax_rate:,.0f}")
        col3.metric("💸 Other Expenses", f"€{property_other_expenses:,.0f}")
        col4.metric(
            "🔑 Initial Investment",
            f"€{property_price * (mortgage_down_payment_rate + property_purchase_tax_rate) + property_other_expenses:,.0f}",
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📆 Monthly Installment", f"€{mortgage.installment:,.0f}")
        col2.metric("💼 Loan Amount", f"€{mortgage.loan_amount:,.0f}")
        col4.metric(f"🏦 Total Payment ({mortgage_years} Years)", f"€{mortgage.total_payment:,.0f}")

    with tab2:
        st.subheader("Investment Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("📈 IRR", f"{investment.irr * 100:.1f}%")
        col2.metric("⌛ Payback Period", f"{investment.payback_period} years")
        col3.metric("💹 NPV", f"€ {investment.npv:,.0f}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Profitability Index (PI)", f"{investment.profitability_index:.2f}")
        col2.metric("🏠 Rent to Price Ratio", f"{investment.rent_to_price_ratio * 100:.2f}%")

    with tab3:
        st.subheader("Investment Analysis Charts")

        benefits_fig = investment.plot_time_series("Benefits", investment.benefits)
        st.plotly_chart(benefits_fig, use_container_width=True)

        cum_benefits_fig = investment.plot_time_series("Cumulative Benefits", investment.cum_benefits)
        st.plotly_chart(cum_benefits_fig, use_container_width=True)

        price_per_year = [investment.compute_property_value(y) for y in range(investment_outlook_years + 1)]
        price_fig = investment.plot_time_series("Price of the Property", price_per_year)
        st.plotly_chart(price_fig, use_container_width=True)

        principal_due_per_year = [
            mortgage.loan_amount - mortgage.cumulative_principal[y] for y in range(investment_outlook_years + 1)
        ]
        principal_due_fig = investment.plot_time_series("Principal Due", principal_due_per_year)
        st.plotly_chart(principal_due_fig, use_container_width=True)

        principal_paid_fig = investment.plot_time_series(
            "Principal Paid", mortgage.cumulative_principal[: investment_outlook_years + 1]
        )
        st.plotly_chart(principal_paid_fig, use_container_width=True)

        interest_paid_fig = investment.plot_time_series(
            "Interest Paid", mortgage.cumulative_interest[: investment_outlook_years + 1]
        )
        st.plotly_chart(interest_paid_fig, use_container_width=True)


if __name__ == "__main__":
    main()
