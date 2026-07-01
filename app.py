import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

# --- App Initialization & Server Hook for Cloud Deployment ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server  # <--- Exposes Flask to Render's Gunicorn instance

# --- Custom Premium Dark Theme Panel Style ---
PANEL_STYLE = {
    "backgroundColor": "#0d0e12",
    "borderRadius": "10px",
    "border": "1px solid #1e2230",
    "padding": "15px",
    "height": "100%",
    "overflow": "hidden",
    "boxShadow": "0 4px 20px rgba(0, 0, 0, 0.6)"
}

# --- 3D Globe Generation Engine ---
def get_globe_figure(zoom_into_delhi=False):
    theta = np.linspace(0, 2 * np.pi, 80)
    phi = np.linspace(0, np.pi, 80)
    x = np.outer(np.cos(theta), np.sin(phi))
    y = np.outer(np.sin(theta), np.sin(phi))
    z = np.outer(np.ones(np.size(theta)), np.cos(phi))
    
    fig = go.Figure(data=[go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, '#020813'], [0.5, '#0a1931'], [1, '#000000']],
        showscale=False, opacity=0.9, hoverinfo='skip'
    )])
    
    # Delhi Coordinate Vectors
    lat, lon = np.radians(28.6139), np.radians(77.2090)
    dx = np.cos(lat) * np.cos(lon)
    dy = np.cos(lat) * np.sin(lon)
    dz = np.sin(lat)
    
    fig.add_trace(go.Scatter3d(
        x=[dx], y=[dy], z=[dz],
        mode='markers+text', text=["📍 New Delhi Focus"],
        marker=dict(size=10, color='#ff3333', symbol='circle'),
        textfont=dict(color="#ffffff", size=11, family="sans-serif")
    ))
    
    eye_distance = 0.7 if zoom_into_delhi else 1.5
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            camera=dict(
                eye=dict(x=dx*eye_distance, y=dy*eye_distance, z=dz*eye_distance) if zoom_into_delhi else dict(x=1.3, y=1.3, z=1.1)
            )
        )
    )
    return fig

# --- Master Layout Framework ---
app.layout = dbc.Container([
    
    # HEADER BAR (6% Viewport Height)
    dbc.Row([
        dbc.Col(html.Div([
            html.Span("URBAN", style={"color": "#ff4d4d", "fontWeight": "800", "fontSize": "22px"}),
            html.Span("COOL AI", style={"color": "#fff", "fontWeight": "700", "fontSize": "22px", "marginLeft": "4px"}),
            html.Small(" | Space-Based Climate Intelligence & Optimization Command Room", className="text-muted ms-2 small")
        ]), width=8, className="d-flex align-items-center"),
        dbc.Col(html.Div("ISRO HACKATHON 2026", className="text-muted text-end text-uppercase small font-weight-bold"), width=4, className="d-flex align-items-center justify-content-end")
    ], style={"height": "6vh", "borderBottom": "1px solid #161924", "padding": "0 20px", "backgroundColor": "#050608"}, className="mx-0"),
    
    # APPLICATION WORKSPACE GRID (94% Viewport Height)
    dbc.Row([
        
        # COLUMN 1: METRICS & EXCEL DATA MATRIX
        dbc.Col([
            html.Div([
                html.H6("📊 MODEL PERFORMANCES", style={"color": "#ff4d4d", "fontSize": "11px", "fontWeight": "bold", "letterSpacing": "0.5px"}, className="mb-2"),
                html.Div([
                    html.Table([
                        html.Tr([html.Th("Metric"), html.Th("RF Model"), html.Th("XGB Model")]),
                        html.Tr([html.Td("R² Score"), html.Td("0.937", className="text-success"), html.Td("0.906")]),
                        html.Tr([html.Td("RMSE"), html.Td("0.940"), html.Td("1.140", className="text-danger")])
                    ], className="table table-sm table-borderless text-white mb-2", style={"fontSize": "11px"})
                ], style={"backgroundColor": "#020205", "borderRadius": "6px", "padding": "8px"}, className="mb-3"),
                
                html.H6("🌱 SIMULATED COOLING EFFECTS", style={"color": "#ff9f43", "fontSize": "11px", "fontWeight": "bold"}, className="mb-2"),
                html.Div([
                    html.Div([html.Small("Scenario A (NDVI Max):"), html.Span(" -0.44°C", className="float-end text-info")], className="mb-1 small"),
                    html.Div([html.Small("Scenario B (Cool Roofs):"), html.Span(" -0.68°C", className="float-end text-info")], className="mb-1 small"),
                    html.Div([html.Small("Scenario C (Water Rest.):"), html.Span(" -0.80°C", className="float-end text-info")], className="mb-1 small"),
                    html.Div([html.Small("Scenario D (Combined):"), html.Span(" -0.95°C", className="float-end text-success font-weight-bold")], className="small")
                ], style={"backgroundColor": "#020205", "borderRadius": "6px", "padding": "8px"}, className="mb-3"),

                html.H6("📈 TOP VARIABLE CONTRIBUTIONS", style={"color": "#28c76f", "fontSize": "11px", "fontWeight": "bold"}, className="mb-1"),
                html.Table([
                    html.Tr([html.Td("col_coord (22.1%)"), html.Td("NDBI (17.5%)")]),
                    html.Tr([html.Td("NDVI_NDE (8.0%)"), html.Td("row_coord (5.6%)")]),
                    html.Tr([html.Td("dist_from_water (5.2%)"), html.Td("Humidity (3.9%)")])
                ], className="table table-sm text-muted table-borderless m-0", style={"fontSize": "10px"}),
                
                dbc.Button("RUN ANALYSIS (FLY-TO)", id="btn-trigger", color="danger", className="w-100 mt-3 font-weight-bold btn-sm")
            ], style=PANEL_STYLE)
        ], width=3, style={"padding": "10px", "height": "94vh"}),
        
        # COLUMN 2: THE 3D EARTH GLOBE
        dbc.Col([
            html.Div([
                dcc.Graph(id='globe', figure=get_globe_figure(), style={"height": "100%", "width": "100%"}, config={'displayModeBar': False})
            ], style={**PANEL_STYLE, "backgroundColor": "#000000"})
        ], width=3, style={"padding": "10px", "height": "94vh"}),
        
        # COLUMN 3: GIS MAPS & SHAP PLOTS (TABBED CONTROLS WITH CORRECTED FIXED ASSETS PATHS)
        dbc.Col([
            dbc.Row([
                # GIS Output Row Half
                dbc.Col(html.Div([
                    html.P("🗺️ HIGH-RES GEOSPATIAL MAPS", style={"color": "#00ffd6", "fontSize": "11px", "fontWeight": "bold", "margin": "0 0 4px 0"}),
                    dbc.Tabs([
                        dbc.Tab(html.Img(src="assets/heat_risk_map.png", style={"width": "100%", "height": "32vh", "objectFit": "contain"}), label="Heat Risk Map"),
                        dbc.Tab(html.Img(src="assets/5_tier_heat_map.png", style={"width": "100%", "height": "32vh", "objectFit": "contain"}), label="5-Tier Heat Map")
                    ])
                ], style=PANEL_STYLE), width=12, style={"height": "47vh", "paddingBottom": "5px"}),
                
                # SHAP Explanation Row Half
                dbc.Col(html.Div([
                    html.P("🧬 AI INTERPRETATION (SHAP)", style={"color": "#b388ff", "fontSize": "11px", "fontWeight": "bold", "margin": "0 0 4px 0"}),
                    dbc.Tabs([
                        dbc.Tab(html.Img(src="assets/shap_plot_v2.png", style={"width": "100%", "height": "32vh", "objectFit": "contain"}), label="SHAP Density"),
                        dbc.Tab(html.Img(src="assets/shap_bar_v2.png", style={"width": "100%", "height": "32vh", "objectFit": "contain"}), label="SHAP Feature Bar")
                    ])
                ], style=PANEL_STYLE), width=12, style={"height": "47vh", "paddingTop": "5px"})
            ], className="h-100")
        ], width=3, style={"padding": "10px", "height": "94vh"}),

        # COLUMN 4: COST DEPLOYMENT ARCHITECTURE
        dbc.Col([
            html.Div([
                html.H6("💰 SMART BUDGET PLANNING INTERVENTIONS", style={"color": "#00ffd6", "fontSize": "11px", "fontWeight": "bold"}, className="mb-3"),
                
                html.Label("Define Allocation Limit (INR)", className="text-muted small mb-1"),
                dcc.Slider(id='budget-slider', min=5, max=50, step=5, value=20, marks={i: f'₹{i}L' for i in range(10, 51, 10)}),
                
                html.Hr(style={"borderColor": "#32dc7ea0"}, className="my-4"),
                html.P("Optimized Solution Deployment Vector:", className="text-info small mb-2"),
                
                html.Div(id='cost-strategy-output', style={"fontSize": "11px", "color": "#fff"})
            ], style=PANEL_STYLE)
        ], width=3, style={"padding": "10px", "height": "94vh"})
        
    ], style={"backgroundColor": "#050608", "margin": "0"}, className="w-100")
    
], fluid=True, style={"backgroundColor": "#050608", "height": "100vh", "overflow": "hidden", "padding": "0"})


# --- Functional Dynamic Interactions ---
@app.callback(
    Output('globe', 'figure'),
    Input('btn-trigger', 'n_clicks'),
    prevent_initial_call=True
)
def run_fly_to(n_clicks):
    if n_clicks is None:
        return dash.no_update
    return get_globe_figure(zoom_into_delhi=True)


@app.callback(
    Output('cost-strategy-output', 'children'),
    Input('budget-slider', 'value')
)
def update_cost_allocation(budget_value):
    if budget_value is None:
        return ""
        
    if budget_value <= 15:
        return html.Div([
            html.Strong("📍 Action Profile Alpha (Low Budget Focus)"),
            html.Div("• Cool Roof Engineering Coverages: ₹10 Lakhs", className="mt-1 text-muted"),
            html.Div("• Rapid Afforestation Seedings: ₹5 Lakhs", className="text-muted"),
            html.H5("-1.12°C Targeted Reduction", className="text-success mt-4")
        ])
    elif budget_value <= 35:
        return html.Div([
            html.Strong("📍 Action Profile Beta (Moderate Scaling)"),
            html.Div("• Regional Water Restorations: ₹20 Lakhs", className="mt-1 text-muted"),
            html.Div("• High Albedo Materials Coating: ₹10 Lakhs", className="text-muted"),
            html.H5("-1.85°C Targeted Reduction", className="text-success mt-4")
        ])
    else:
        return html.Div([
            html.Strong("📍 Action Profile Gamma (Max Combined Impact)"),
            html.Div("• Integrated Macro Green Belts Mapping", className="mt-1 text-muted"),
            html.Div("• Global Cool Infrastructure Architecture Deployment", className="text-muted"),
            html.Div("• Total Allocated Expense Plan: ₹45 Lakhs", className="text-muted"),
            html.H5("-2.87°C Maximum System Drop", className="text-success mt-4")
        ])


if __name__ == '__main__':
    app.run(debug=True)
