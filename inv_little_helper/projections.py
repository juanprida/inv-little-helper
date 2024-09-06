import pandas as pd
import plotly.graph_objects as go


class Mortgage:
    def __init__(self, price, down_payment_rate, mortgage_rate, years):
        self.price = price
        self.down_payment_rate = down_payment_rate
        self.down_payment = down_payment_rate * price
        self.loan_amount = price * (1 - down_payment_rate)
        self.mortgage_rate = mortgage_rate
        self.years = years
        self.mortgage_rate_month = mortgage_rate / 12
        self.n_installments = years * 12

        self.installment = self._compute_installment()
        self.annual_installment = self.installment * 12
        self.total_payment = self.installment * self.n_installments

        # Lists to store the breakdown
        self.principal_payments = []
        self.interest_payments = []
        self.cumulative_principal = []
        self.cumulative_interest = []

        self._compute_payment_breakdown()

    def _compute_installment(self):
        return (
            self.loan_amount
            * (self.mortgage_rate_month * (1 + self.mortgage_rate_month) ** self.n_installments)
            / ((1 + self.mortgage_rate_month) ** self.n_installments - 1)
        )

    def _compute_payment_breakdown(self):
        remaining_balance = self.loan_amount
        cumulative_principal = 0
        cumulative_interest = 0

        for month in range(1, self.n_installments + 1):
            interest_payment = remaining_balance * self.mortgage_rate_month
            principal_payment = self.installment - interest_payment

            # Update remaining balance
            remaining_balance -= principal_payment

            # Store payments
            self.principal_payments.append(principal_payment)
            self.interest_payments.append(interest_payment)

            # Update cumulative values
            cumulative_principal += principal_payment
            cumulative_interest += interest_payment

            self.cumulative_principal.append(cumulative_principal)
            self.cumulative_interest.append(cumulative_interest)

    def compute_remaining_loan(self, n_installments_paid_years):
        return (
            self.loan_amount
            * (
                (1 + self.mortgage_rate_month) ** self.n_installments
                - (1 + self.mortgage_rate_month) ** (n_installments_paid_years * 12)
            )
            / ((1 + self.mortgage_rate_month) ** self.n_installments - 1)
        )


class Property:
    def __init__(self, mortgage, price, years, growth_rate, annual_income, purchase_tax_rate, initial_extra_expenses):
        self.m = mortgage
        self.price = price
        self.years = years
        self.growth_rate = growth_rate
        self.annual_income = annual_income
        self.purchase_tax_rate = purchase_tax_rate
        self.initial_extra_expenses = initial_extra_expenses

    def compute_property_value(self, years=None):
        if years is None:
            years = self.years
        return self.price * (1 + self.growth_rate) ** (years - 1)

    def run(self):
        self.rent_benefits = self._compute_rent_benefits()
        self.selling_benefits = self._compute_selling_benefits()

        # Total benefits
        self.benefits = self._compute_benefits()
        self.cum_benefits = self._compute_cum_benefits(self.benefits)

        self.npv = sum(self.benefits)
        self.profitability_index = self.npv / -self.selling_benefits[0]
        self.payback_period = next(t for t, cum_benefit in enumerate(self.cum_benefits) if cum_benefit >= 0) + 1
        self.irr = ((sum(self.benefits)) / -self.selling_benefits[0]) ** (1 / (self.years - 1)) - 1
        self.rent_to_price_ratio = (sum(self.rent_benefits) / len(self.rent_benefits)) / self.price

    def _compute_rent_benefits(self):
        return [self.annual_income - self.m.annual_installment for t in range(0, self.years)]

    def _compute_selling_benefits(self):
        selling_benefit = [0] * self.years
        selling_benefit[0] = (
            -(self.price * (self.m.down_payment_rate + self.purchase_tax_rate)) - self.initial_extra_expenses
        )
        selling_benefit[-1] = self.compute_property_value() - self.m.compute_remaining_loan(self.years)
        return selling_benefit

    def _compute_benefits(self):
        return [self.rent_benefits[t] + self.selling_benefits[t] for t in range(self.years)]

    def _compute_cum_benefits(self, benefits):
        return [sum(benefits[: i + 1]) for i in range(len(benefits))]

    def plot_time_series(self, name, values):
        # Create a DataFrame for easy plotting
        df = pd.DataFrame(
            {
                "Year": list(range(self.years)),
                name: [(v / 1000) for v in values],
            }
        )

        # Create the figure with subplots
        fig = go.Figure()

        # Add the cumulative discounted benefits
        fig.add_trace(
            go.Scatter(
                x=df["Year"], y=df[name], mode="lines+markers", name=name, line=dict(width=2), marker=dict(size=6)
            )
        )

        fig.update_layout(
            title=f"{name} Over Time",
            xaxis_title="Year",
            yaxis_title="Amount",
            title_font=dict(size=24),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            yaxis=dict(
                title_font=dict(size=18),
                tickfont=dict(size=14),
                tickformat=",.1f",  # Removes decimals
                tickprefix="€",  # Adds euro sign before the value
                ticksuffix="K",  # Adds "K" suffix for thousands
            ),
        )

        return fig
