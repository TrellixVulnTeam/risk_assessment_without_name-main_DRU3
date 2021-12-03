import streamlit as st
import plotly.graph_objects as go
from random import seed
import random
import pandas as pd
import time

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

def main_features():
    st.title("Supplier Scoring")
    st.markdown("> __Scorecard of a supplier based on different type of information that gather from Otrafy platform, GFSI Document and multiple databases__")
    st.markdown("> __The score based on the historical data of the supplier. The statistical information will update monthly and change over the time based on the historical info of the supplier__")
    
    with st.expander("Supplier Information"):
        st.markdown("__Organisation Name__: Supplier Z")
        st.markdown("__Location__: Hong Kong, China")
        st.markdown("__Contact Person__: Zhengmu Li")
        st.markdown("__FEI Number__: 1000140016")
    
    gfsi_count, correction_index, current_state_gfsi, inspection_sum = st.columns(4)
    with gfsi_count:
        st.metric("Number of GFSI Document", 10, "+ 2 documents")
    
    with correction_index:
        st.metric("Average Correction Index Percentage", "90%", "+10% from last updated")
        
    with current_state_gfsi:
        st.metric("Current State of GFSI Document Recommendation", "Recertification", "Remain Improved")
    
    with inspection_sum:
        st.metric("Total Inspection", 18, "+ 1 from last updated", delta_color="inverse")
    
    recall_count, refusal_count, warning_letter_count, location_risk, import_aleart   = st.columns(5)
    with recall_count:
        st.metric("Recall Number From 2013 - 2021", 20, "+ 1 from the last updated", delta_color="inverse")
    with refusal_count:
        st.metric("Import Refusal", 3, "No Increase", delta_color="off")
    with warning_letter_count:
        st.metric("Warning Letter", 1, "No Increase", delta_color="off")
    with import_aleart:
        st.metric("Import Alert", "0")
    with location_risk:
        st.metric("Supplier Location Risk", "High")
    
    st.metric("OVERALL", "LOW RISK")
    
    
    
    inspection_type, inspection_count = st.columns([2,2])
    
    with inspection_count:
        st.header("Inspection by Year")
        seed(20)
        fig_inspection_count = go.Figure()
        fig_inspection_count.add_trace(go.Bar(
            y=['2017', '2018', '2019', "2020","2021"],
            x= random.sample(range(0, 5), 5),
            name='No Action Indicated (NAI)',
            orientation='h',
            marker=dict(
                color='rgba(100, 240, 120, 1)',
                line=dict(color='rgba(23, 66, 21, 1.0)', width=3)
            )
        ))
        fig_inspection_count.add_trace(go.Bar(
            y=['2017', '2018', '2019', "2020","2021"],
            x=random.sample(range(0, 5), 5),
            name='Voluntary Action Indicated (VAI)',
            orientation='h',
            marker=dict(
                color='rgba(227,105,39,1)',
                line=dict(color='rgba(214, 139, 81, 1.0)', width=3)
            )
        ))
        fig_inspection_count.add_trace(go.Bar(
            y=['2017', '2018', '2019', "2020","2021"],
            x=[0,1,0,0,0],
            name='Official Action Indicated (OAI)',
            orientation='h',
            marker=dict(
                color='rgba(227,39,39,1)',
                line=dict(color='rgba(212,57,57, 1.0)', width=3)
            )
        ))

        fig_inspection_count.update_layout(
            barmode='stack', 
            yaxis_title="Year", 
            xaxis_title="Count", 
            margin=dict(l=20, r=100, t=10, b=50), 
            width=700,
            height=400)
        st.plotly_chart(fig_inspection_count)
    
    with inspection_type:
        st.header("Inspection by Type")
        colors = ['rgba(100, 240, 120, 1)', 'rgba(227,105,39,1)', 'rgba(227,39,39,1)']
        insp_type = ["No Action Indicated (NAI)", "Voluntary Action Indicated (VAI)", "Official Action Indicated (OAI)"]
        per = [10,7,1]
        inspection_type_graph = go.Figure(data=[go.Pie(labels=insp_type, values=per, textinfo='label+value')])
        inspection_type_graph.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=15, showlegend=False, marker=dict(colors=colors))
        inspection_type_graph.update_layout(margin=dict(l=10, r=400, t=10, b=50), width=900,height=400)
        
        st.plotly_chart(inspection_type_graph)
    
    st.header("Number of Nonconformities in 3PA")
    date_list = ["2014","2015","2016", "2017", "2018", "2019", "2020", "2021"]
    minor_nc = [20,15,13,10,9,9,7,5]
    major_nc = [0,0,0,1,1,0,0,0]
    critical_nc = [0,0,0,0,0,0,0,0]
        
    chart_data = pd.DataFrame({"Date":sorted(date_list),"Minor":minor_nc, "Major":major_nc, "Critical":critical_nc})
    nc_line = go.Figure()
    nc_line.add_trace(go.Scatter(x=chart_data["Date"], y=chart_data["Minor"], mode="lines+markers", name="Minor Nonconformities"))
    nc_line.add_trace(go.Scatter(x=chart_data["Date"], y=chart_data["Major"], mode="lines+markers", name="Major Nonconformities"))
    nc_line.add_trace(go.Scatter(x=chart_data["Date"], y=chart_data["Critical"], mode="lines+markers", name="Critical Nonconformities"))
    nc_line.update_layout(
                   xaxis_title='Date Updated',
                   yaxis_title='Number of Nonconformities',
                   margin=dict(l=10, r=400, t=10, b=50), width=1500,height=400)
    nc_line.update_xaxes(showgrid=False, zeroline=False)
    #nc_line.update_yaxes(showgrid=False, zeroline=False)
    st.plotly_chart(nc_line)
    
    st.header("")
    
    
    

    
    
    
    