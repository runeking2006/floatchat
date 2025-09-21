import plotly.express as px
import pandas as pd
import plotly.graph_objects as go  # optional for type hint

# Time-series plot
def plot_time_series(df: pd.DataFrame, y_column: str, title: str = "Time-series") -> go.Figure:
    fig = px.line(df, y=y_column, title=title)
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_white",
        height=400
    )
    return fig

# Float map plot
def plot_float_map(df: pd.DataFrame, tooltip_col: str = None) -> go.Figure:
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        hover_name=tooltip_col if tooltip_col else None,
        zoom=1,
        height=400
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig
