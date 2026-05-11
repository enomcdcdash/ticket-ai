import pandas as pd

# =========================================
# BASIC KPI SUMMARY
# =========================================
def get_basic_kpi(df):

    summary = {}

    summary["total_rows"] = len(df)

    summary["total_tickets"] = df["Total_Tickets"].sum()

    summary["total_incident"] = df["Total_Incident"].sum()

    summary["total_event"] = df["Total_Event"].sum()

    summary["total_area"] = df["Area"].nunique()

    summary["total_regional"] = df["Regional"].nunique()

    return summary


# =========================================
# TOP REGIONAL TICKET VOLUME
# =========================================
def get_top_regional(df):

    regional_summary = (
        df.groupby("Regional")["Total_Tickets"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return regional_summary


# =========================================
# INCIDENT ANALYSIS
# =========================================
def get_incident_analysis(df):

    incident_summary = (
        df.groupby("Regional")["Total_Incident"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return incident_summary


# =========================================
# EVENT ANALYSIS
# =========================================
def get_event_analysis(df):

    event_summary = (
        df.groupby("Regional")["Total_Event"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return event_summary


# =========================================
# TAKEOVER ANALYSIS
# =========================================
def get_takeover_analysis(df):

    df["Total_Takeover"] = (
        df["Total_Incident_Takeover"]
        + df["Total_Event_Takeover"]
    )

    takeover_summary = (
        df.groupby("Regional")["Total_Takeover"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return takeover_summary


# =========================================
# VISIT ANALYSIS
# =========================================
def get_visit_analysis(df):

    df["Total_Visit"] = (
        df["Total_Incident_Visit"]
        + df["Total_Event_Visit"]
    )

    visit_summary = (
        df.groupby("Regional")["Total_Visit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return visit_summary


# =========================================
# DATASET SUMMARY
# =========================================
def generate_data_summary(df):

    total_tickets = df["Total_Tickets"].sum()

    total_incident = df["Total_Incident"].sum()

    total_event = df["Total_Event"].sum()

    top_regional = get_top_regional(df)

    highest_regional = top_regional.index[0]

    highest_value = top_regional.iloc[0]

    summary = f"""
Telecom KPI Dataset Summary

Total records: {len(df)}

Total tickets: {total_tickets}

Total incidents: {total_incident}

Total events: {total_event}

Highest ticket contributor:
{highest_regional} with {highest_value} tickets.

The dataset contains telecom operational metrics including:
- Ticket volume
- Incident metrics
- Event metrics
- Takeover metrics
- Visit metrics
- Regional operational performance

Operational focus should prioritize:
- High ticket regionals
- High incident regionals
- High takeover areas
- Operational escalation areas
"""

    return summary