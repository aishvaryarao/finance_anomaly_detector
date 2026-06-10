import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
import base64

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Sample user ID (in real app, this would come from login)
USER_ID = 1

API_BASE_URL = "http://localhost:8000/api"

app.layout = html.Div([
    html.Div([
        html.H1("Finance Anomaly Detector", style={"textAlign": "center", "marginBottom": "30px"}),
    ], style={"backgroundColor": "#5d6265", "color": "white", "padding": "20px"}),
    
    html.Div([
        # Upload Section
        html.Div([
            html.H2("Upload Bank Statement"),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select CSV/PDF File')
                ]),
                style={
                    'width': '100%',
                    'height': '100px',
                    'lineHeight': '100px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px 0',
                    'backgroundColor': "#575757",
                    'cursor': 'pointer'
                },
                multiple=False
            ),
            html.Div(id='upload-status', style={"marginTop": "10px", "fontSize": "16px"})
        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "marginBottom": "20px"}),
        
        # Statistics
        html.Div([
            html.Div([
                html.H3("Total Transactions"),
                html.H2(id='total-transactions', children="0")
            ], style={"flex": 1, "padding": "20px", "backgroundColor": "white", "borderRadius": "8px", "margin": "10px"}),
            
            html.Div([
                html.H3("Anomalies Detected"),
                html.H2(id='total-anomalies', children="0", style={"color": "red"})
            ], style={"flex": 1, "padding": "20px", "backgroundColor": "white", "borderRadius": "8px", "margin": "10px"}),
            
            html.Div([
                html.H3("Total Spent"),
                html.H2(id='total-spent', children="$0")
            ], style={"flex": 1, "padding": "20px", "backgroundColor": "white", "borderRadius": "8px", "margin": "10px"}),
        ], style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"}),
        
        # Charts
        html.Div([
            html.Div([
                html.H3("Category Breakdown"),
                dcc.Graph(id='category-pie-chart')
            ], style={"flex": 1, "padding": "20px", "backgroundColor": "white", "borderRadius": "8px", "margin": "10px"}),
            
            html.Div([
                html.H3("Spending Trends"),
                dcc.Graph(id='spending-line-chart')
            ], style={"flex": 1, "padding": "20px", "backgroundColor": "white", "borderRadius": "8px", "margin": "10px"}),
        ], style={"display": "flex", "justifyContent": "space-around"}),
        
        # Anomalies Table
        html.Div([
            html.H3("Recent Anomalies"),
            html.Div(id='anomalies-table', style={"padding": "20px"})
        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "marginTop": "20px"}),
        
    ], style={"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"}),
    
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
], style={"backgroundColor": "#0F0F0F", "minHeight": "100vh", "padding": "20px"})

@callback(
    [Output('total-transactions', 'children'),
     Output('total-anomalies', 'children'),
     Output('total-spent', 'children'),
     Output('category-pie-chart', 'figure'),
     Output('spending-line-chart', 'figure'),
     Output('anomalies-table', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    try:
        # Fetch transactions
        response = requests.get(f"{API_BASE_URL}/transactions?user_id={USER_ID}")
        transactions_data = response.json()
        transactions = transactions_data.get("transactions", [])
        
        # Fetch anomalies
        response = requests.get(f"{API_BASE_URL}/transactions/anomalies?user_id={USER_ID}")
        anomalies_data = response.json()
        anomalies = anomalies_data.get("anomalies", [])
        
        # Calculate metrics
        total_transactions = len(transactions)
        total_anomalies = len(anomalies)
        total_spent = sum(float(t.get("amount", 0)) for t in transactions)
        
        # Category breakdown
        categories = {}
        for t in transactions:
            cat = t.get("category", "Other")
            categories[cat] = categories.get(cat, 0) + float(t.get("amount", 0))
        
        pie_fig = px.pie(
            values=list(categories.values()),
            names=list(categories.keys()),
            title="Spending by Category"
        )
        
        # Spending trends
        df = pd.DataFrame(transactions)
        if len(df) > 0:
            df["date"] = pd.to_datetime(df["date"])
            daily_spend = df.groupby("date")["amount"].sum().reset_index()
            line_fig = px.line(daily_spend, x="date", y="amount", title="Daily Spending")
        else:
            line_fig = go.Figure()
            line_fig.add_annotation(text="No data available")
        
        # Anomalies table
        if anomalies:
            anomaly_rows = []
            for a in anomalies[:10]:  # Show last 10
                anomaly_rows.append(html.Tr([
                    html.Td(a.get("date", "N/A")),
                    html.Td(a.get("description", "N/A")),
                    html.Td(f"${float(a.get('amount', 0)):.2f}"),
                    html.Td(a.get("reason", "Unusual amount"))
                ]))
            
            table = html.Table([
                html.Thead(html.Tr([
                    html.Th("Date"),
                    html.Th("Description"),
                    html.Th("Amount"),
                    html.Th("Reason")
                ])),
                html.Tbody(anomaly_rows)
            ], style={"width": "100%", "borderCollapse": "collapse"})
        else:
            table = html.P("No anomalies detected", style={"color": "green", "fontSize": "16px"})
        
        return (
            f"{total_transactions}",
            f"{total_anomalies}",
            f"${total_spent:.2f}",
            pie_fig,
            line_fig,
            table
        )
    except Exception as e:
        return "Error", "Error", "Error", {}, {}, html.P(f"Error: {str(e)}")

@callback(
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    prevent_initial_call=True
)
def upload_file(contents, filename):
    if contents is None:
        return ""

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        files = {
            "file": (filename, decoded)
        }

        data = {
            "user_id": 1
        }

        response = requests.post(
            f"{API_BASE_URL}/upload/",
            files=files,
            data=data
        )

        if response.status_code == 200:
            result = response.json()
            return (
                f"Uploaded successfully! "
                f"Processed {result['transactions_processed']} transactions, "
                f"found {result['anomalies_detected']} anomalies."
            )
        else:
            return f"Upload failed: {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=8050)