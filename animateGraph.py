import numpy as np
import pandas as pd
from dash import html, Input, Output, dcc, dash
import plotly.express as px
import mysql.connector

list = ["Aggregate", "Bananas", "Oranges", "Bread", "Tomatoes", "Chicken", "Electricity", "Eggs", "Gas", "Ground Beef", "Utilities", "Milk"]
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="priceInfo"
)
cursor = mydb.cursor()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H4(
        "How badly am I getting fucked?",
        style={"textAlign": "center"},
    ),
    html.P("Select an item to compare"),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": item, "value": item} for item in list],
        value="Bananas",
        clearable=False,
    ),
    dcc.Graph(id="comparison"),
])

def table_Builder(i):
    cursor.execute("SELECT Date, Price FROM info where name = %s", (i,))
    res = cursor.fetchall()
    df = pd.DataFrame.from_records(res)
    return df

def dict_Builder(i):
    list_Item = table_Builder(i)
    item = {
        "Name": i,
        "Price": [e for e in list_Item[1]],
        "Date": [e for e in list_Item[0]],
    }
    return item


def aggregate_Builder():
    query = "SELECT Name, Date, Price FROM info"
    cursor.execute(query)
    res = cursor.fetchall()

    df = pd.DataFrame.from_records(
        res,
        columns=["Name", "Date", "Price"]
    )

    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
    df["Price"] = df["Price"].astype(float)

    fig = px.line(df, x="Date", y="Price", color="Name")

    df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

    z = np.polyfit(df["Date_ordinal"], df["Price"], 1)
    p = np.poly1d(z)

    fig.add_scatter(
        x=df["Date"],
        y=p(df["Date_ordinal"]),
        mode="lines",
        name="Overall Trend",
        line=dict(color="black", width=3, dash="dash")
    )

    fig.update_xaxes(nticks=10)

    return fig


@app.callback(
    Output("comparison", "figure"),
    Input("dropdown", "value"))
def display_comparison(dropdown):
    if(dropdown == "Aggregate"):
        return aggregate_Builder()
    else:
        df = dict_Builder(dropdown)
        df = pd.DataFrame.from_records(
            df,
            columns=["Name", "Date", "Price"]
        )
        df["Date"] = pd.to_datetime(df["Date"], format="mixed")
        fig = px.scatter(
            df,
            x="Date",
            y="Price",
            color="Name",
            title="Price Trends"
        )

        df["Price"] = df["Price"].astype(float)


        df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

        z = np.polyfit(df["Date_ordinal"], df["Price"], 1)
        p = np.poly1d(z)

        fig.add_scatter(
            x=df["Date"],
            y=p(df["Date_ordinal"]),
            mode="lines",
            name="Overall Trend",
            line=dict(color="black", width=3, dash="dash")
        )

        fig.update_traces(mode="lines")
        fig.update_xaxes(nticks=10)
        return fig

app.run(debug=True)
