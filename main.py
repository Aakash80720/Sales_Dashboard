import pandas as pd
import streamlit as str
import plotly.express as px


class Sidebar:
    def __init__(self, data):
        self.data_selection = None
        self.Data = data
        str.sidebar.header("Filter option")
        self.filter()

    def filter(self):
        city = str.sidebar.multiselect(
            "Select cities",
            options=self.Data["City"].unique(),
            default=self.Data["City"].unique(),
        )

        customerType = str.sidebar.multiselect(
            "select Customer Type",
            options=self.Data["Customer_type"].unique(),
            default=self.Data["Customer_type"].unique(),
        )

        gender = str.sidebar.multiselect(
            "Gender Type",
            options=self.Data["Gender"].unique(),
            default=self.Data["Gender"].unique(),
        )

        self.data_selection = self.Data.query(
            "City == @city & Customer_type == @customerType & Gender == @gender"
        )

    def getDataSelection(self):
        return self.data_selection


class Dashboard:
    def __init__(self, data):
        self.selection = None
        self.sidebar = None
        self.data = data
        self.sidebarCall()
        self.Header()
        self.charts()

    def sidebarCall(self):
        self.sidebar = Sidebar(self.data)

    def Header(self):
        str.write(
            'Aakash Project :sunglasses:'
        )
        str.title(":bar_chart: Sales Dashboard")
        str.markdown("##")

        self.selection = self.sidebar.getDataSelection()
        total_sales = int(self.selection["Total"].sum())
        avg_rating = round(self.selection["Rating"].mean(), 1)
        star_rating = ":star:" * int(round(avg_rating, 0))
        avg_sale = round(self.selection["Total"].mean(), 2)

        left, middle, right = str.columns(3)
        with left:
            str.subheader("Total Sales : ")
            str.subheader(f"Rupees RS.{total_sales}")

        with middle:
            str.subheader("Average Rating")
            str.subheader(f"{avg_rating} {star_rating}")

        with right:
            str.subheader("Average Sale per Transaction")
            str.subheader(f"Rupees RS.{avg_sale}")

        str.markdown("---")

    def charts(self):
        charts = Charts(self.selection)
        charts.view()


class Charts:
    def __init__(self, data):
        self.selection = data

    def view(self):
        left, right = str.columns(2)
        sales_by_product = (
            self.selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
        )
        str.dataframe(self.selection)
        fig_product_sales = px.bar(
            sales_by_product,
            x="Total",
            y=sales_by_product.index,
            orientation="h",
            title="<b>Sales by Product Line</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_by_product),
            template="plotly_white",
        )

        fig_product_sales.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        sales_by_hour = (
            self.selection.groupby(by=["hour"]).sum()[["Total"]]
        )
        fig_hourly_sales = px.bar(
            sales_by_hour,
            x=sales_by_hour.index,
            y="Total",
            title="<b>Sales by Hour</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
            template="plotly_white",
        )

        fig_hourly_sales.update_layout(
            xaxis=(dict(tickmode="linear")),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )
        left.plotly_chart(fig_product_sales)
        right.plotly_chart(fig_hourly_sales)


if __name__ == '__main__':
    str.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_char:",
        layout="wide",
    )


    @str.cache
    def get_data_from_excel():
        df = pd.read_excel(
            io='supermarkt_sales.xlsx',
            sheet_name='Sales',
            usecols='B:R',
            skiprows=3,
            nrows=1000,
            engine='openpyxl',
        )
        df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
        return df


    df = get_data_from_excel()
    dashboard = Dashboard(df)

    hide_style = """
    <style>
    #MainMenu{visibility : hidden;}
    footer{visibility : hidden;}
    header{visibility : hidden;}
    </style>
    """
    str.markdown(hide_style,unsafe_allow_html=True)
