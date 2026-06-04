import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


COLORS = px.colors.qualitative.Bold


def dwell_chart(avg_dwell: dict):
    zones = list(avg_dwell.keys())
    values = list(avg_dwell.values())

    fig = go.Figure(
        go.Bar(
            x=zones,
            y=values,
            marker_color=COLORS[:len(zones)],
            text=[f"{v:.1f}s" for v in values],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Avg Dwell: %{y:.1f}s<extra></extra>",
        )
    )

    fig.update_layout(
        title="Average Dwell Time by Zone",
        xaxis_title="Zone",
        yaxis_title="Seconds",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        margin=dict(t=50, b=40),
    )

    return fig


def zone_visits_chart(zone_visits: dict):
    zones = list(zone_visits.keys())
    counts = list(zone_visits.values())

    fig = go.Figure(
        go.Bar(
            x=zones,
            y=counts,
            marker_color=COLORS[:len(zones)],
            text=counts,
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Visits: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Zone Visit Counts",
        xaxis_title="Zone",
        yaxis_title="Visits",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        margin=dict(t=50, b=40),
    )

    return fig


def funnel_chart(zone_funnel: dict, conversion_rate: dict):
    foh = zone_funnel.get("FOH", 0)
    cash = zone_funnel.get("CASH_COUNTER", 0)
    rate = conversion_rate.get("FOH_TO_CASH_COUNTER", 0)

    fig = go.Figure(
        go.Funnel(
            y=["FOH (Entry)", "CASH_COUNTER"],
            x=[foh, cash],
            textinfo="value+percent initial",
            marker=dict(color=["#4361ee", "#f72585"]),
            hovertemplate="<b>%{y}</b><br>Visitors: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Conversion Funnel — FOH → CASH_COUNTER ({rate*100:.1f}%)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        margin=dict(t=50, b=20),
    )

    return fig


def occupancy_chart(peak_occupancy: dict):
    zones = list(peak_occupancy.keys())
    values = list(peak_occupancy.values())

    fig = go.Figure(
        go.Bar(
            y=zones,
            x=values,
            orientation="h",
            marker_color=COLORS[:len(zones)],
            text=values,
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Peak: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Peak Occupancy by Zone",
        xaxis_title="Peak Visitors",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        margin=dict(t=50, b=20, l=120),
    )

    return fig


def journeys_table(visitor_paths: dict):
    rows = [
        {
            "Visitor ID": vid,
            "Journey Path": " → ".join(path),
        }
        for vid, path in visitor_paths.items()
        if path
    ]

    return pd.DataFrame(rows)
