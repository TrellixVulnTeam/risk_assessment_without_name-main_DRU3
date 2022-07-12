from __future__ import annotations


from phase_1.utilities import *
from phase_2.connecting_api import *
from phase_1.ocr_extraction import *
from supplier_scoring import *
from utilities import *
from urllib.request import urlopen

import json
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os


CURRENT_PATH = os.getcwd()
TEST_FILE_FOLDER = CURRENT_PATH + "/test_file/"


##############################################################################################################################
#CROSS ANALYSIS MODULE                                                                                                       #
##############################################################################################################################

def cross_analysis():
    data = pd.read_csv(TEST_FILE_FOLDER + "OtherName_Version - Copy.csv", header=0, dtype={"FIPS": str}).drop_duplicates()
    data = data.drop(["Client Representative"],axis=1)
    data = data.fillna("No Information")
    data = preprocessing_dataframe(data)

    with st.expander("FSSC Audit Summarise Data"):
        st.write(data)
    
    st.markdown("### Audit Report Nonconformities Summarize")
    minor, major, critical = st.columns(3)
    with minor:
        st.metric("Minor Nonconformities", sum(data["Minor Nonconformities"]))
        st.markdown("__Supplier C - Chanhassen__ : 17")
        st.markdown("__Supplier F - Cincinnati__ : 10")
    with major:
        st.metric("Major Nonconformities", 1)
        st.markdown("__Supplier B - Cedar Rapids__ : 1")
    with critical:
        st.metric("Critical Nonconformities", 0)
    
    
    non_conformance_type, audit_type = st.columns(2)
    
    with non_conformance_type:
        st.markdown("### Nonconformities Type Percentage")
        nc_type = ["Facility and Location Issues", "Paperwork Issues", "Food Integrity Issues"]
        per = [27,19,11]
        nonconformities_type = go.Figure(data=[go.Pie(labels=nc_type, values=per)])
        nonconformities_type.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=12, showlegend=False)
        nonconformities_type.update_layout(margin=dict(l=10, r=400, t=10, b=50), width=800,height=500)
        st.plotly_chart(nonconformities_type)
    
    with audit_type:
        st.markdown("### Audit Recommendation")
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        audit_type_classify = ["Recertification", "Surveillance Stage 1", "Surveillance Stage 2"]
        per_at = [2,3,1]
        at_graph = go.Figure(data=[go.Pie(labels=audit_type_classify, values=per_at, textinfo='label+value')])
        at_graph.update_traces(hoverinfo='label+percent', textinfo='label+value', showlegend=False)    
        at_graph.update_layout(margin=dict(l=10, r=400, t=10, b=50), width=800,height=500)
        st.plotly_chart(at_graph)
    
    st.markdown("### Correction Index Ranking")
    sup_name = ["Supplier A", "Supplier B", "Supplier C", "Supplier D", "Supplier E", "Supplier F"]
    value = [90, 85, 70, 65, 10, 5]
    corr_index = pd.DataFrame({"Correction Index %": value}, index=sup_name)
    st.table(corr_index.style.apply(highlight_greaterthan, threshold=50, column=['Correction Index %'], axis=1))
    with st.expander("Description and Explaination for Correction Index"):
        st.markdown("__Description__: The bar represent the percentage of Correction Index of a supplier. The number of Correction Index calculated base on polarity (positive and negative) in non-conformance comment + other factors (such as audit recommendation, previous audit type, etc.)")
        st.markdown("__Why this chart__: Viewer can choose to see the bar chart or a table of correction index number. You can hover the mouse in to look more clearly")
    
    st.markdown("### Supplier Non-conformities Map Distribution")
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    fig_3 = px.choropleth(data, geojson=counties, locations="FIPS", color="Minor Nonconformities",
                            color_continuous_scale="Viridis",
                            range_color=(0,12),
                            scope="usa",
                            labels = {"Minor Nonconformities": "minor"}
                            )
    fig_3.update_layout(width=1300, height=800, margin=dict(l = 0, r=60, b=40, t=40))
    st.plotly_chart(fig_3)
    with st.expander("Description and Explaination for Map Graph"):
        st.markdown("__Description__: The graph represent the location of the facility specifically and the size of dot will represent the number of non-conformities that the facility have.")
        st.markdown("__Why this chart__: Well this chart easy to understand right ? This will be use for the future pathway as well such as Predict the Supplier Sustainability")
    
    st.markdown("### Other Related Information")
    st.markdown("All __100% nonconformities__ have been closed from the last audit report")
    st.markdown("__33% of the Audit Report__ has the Minor Nonconformities higher than the average")
    st.markdown("__30% of the Audit Report__ are in _Audit Type Surveillance Stage 1_ and __70% of Audit Report__ are in _Audit Type Surveillance Stage 2_")

##############################################################################################################################
#SINGLE ANALYSIS MODULE                                                                                                      #
##############################################################################################################################
def single_analysis():
    data = pd.read_csv(TEST_FILE_FOLDER + "OtherName_Version - Copy.csv", header=0, dtype={"FIPS": str}).drop_duplicates()
    data = data.drop(["Client Representative"],axis=1)
    data = data.fillna("No Information")
    data = preprocessing_dataframe(data)
    
    st.markdown("You choose file: __Company A Buffalo City Facility Audit Jan-July 2020.pdf__")
    

    value = main_phase_2("General Mills", "Iowa")
    with st.expander("Basic Information"):
        st.markdown("__Organisation Name__: Company A")
        st.markdown("__City__: Buffalo")
        st.markdown("__State__: New York")
    
    with st.expander("Audit Information"):
        minor_non, major_non, crit_non, audit_rec, audit_type = st.columns(5)
        minor_non.metric("Total Minor Nonconformities", sum(data["Minor Nonconformities"]), "10", delta_color="inverse")
        major_non.metric("Total Major Nonconformities", 5, "0")
        crit_non.metric("Total Critical Nonconformities", 0, delta_color="inverse")
        audit_rec.metric("Audit Recommendation", "PASS")
        audit_type.metric("Audit Type", "Recertification")
    
    st.write("We find something similar of __FDA Recall Database__")
    
    with st.expander("Company A Related Recall FDA Recall"):
        recalling_firm_count = 0
        for i in range(len(value)):
            if value[i]["recalling_firm"] == "General Mills, Inc":
                recalling_firm_count += 1
        
        st.markdown(f"__Company A__ was got recalled __{recalling_firm_count} times in the last 4 years__")
            
        city_count = 0
        for i in range(len(value)):
            if value[i]["city"] == "Buffalo":
                city_count += 1
        st.markdown(f"__Buffalo City__ has __{city_count} recall cases in the last 4 years__")
        
        top_5_product = []
        for i in range(len(value)):
            if value[i]["recalling_firm"] == "General Mills, Inc":
                top_5_product.append(cleaning_product_name(value[i]["product_description"]))
        
        st.write(f"Top 5 nearest products got called by FDA from Company A: __{top_5_product[:5]}__")
        st.write("100% of product is __Food Recall__ / 100% of product has been __Terminated__")
        st.write("With __30% of cases is Class I__, __70% of cases is Class II__ in ranking of dangerous")
    
    with st.expander("Buffalo City Location Related FDA Recall"):
        st.markdown("With __Buffalo City__ separately, there has been 31 times cases happened at here in the last 4 years")
        st.markdown("Top 5 Product recent got recall at Buffalo City: __Wegmans Milk Chocolate Sucker, Cake Truffles, ALL NATURAL ANCIENT GRAIN BREAD, GRANDMA'S perogies POTATO & BACON PEROGIES, Signature SELECT Vanilla Ice Cream & White Cake ICE CREAM CAKE__")
        st.markdown("Top 5 Firms got recall: __Landies Candies, Inc., Rich Products Corp, BUFFALO SAV, INC., The Sausage Maker, Inc., Upstate Niagara Cooperative, Inc.__")
    
    with st.expander("FDA Adverse Event (Product Poisoned)"):
        st.write("__Company A__ has 199 times got report about product poisoned by FDA from 2015")
        st.write("The most recent product recalled: A Cheerios, Multigrain Cheerios, Chip Cookie")
        st.write("Most of the reactions are: __Headache, Diarrhoea, Coeliac Disease__")
    
    st.write("We also found some interested information about some similar product got food poisoned at __Buffalo City__ of the __Company A__")
    with st.expander("Food Poisoned Report Cases"):
        st.write("Newest retailer got reported by consumer: __Red Lobster, Jersey Mike's Subs, Applebee's Grill + Bar__")
        st.write("Newest food got reported similar like Company A: __Red Lobster, Grill Fish, Fish'n'Chip__  ")
        st.write("Top reactions: __Nausea, Diarrhea, Vomitting__")
    
    st.write("Some basic info about the __Company A__ in Food Data Centre Database")
    with st.expander("Food Data Centre Info:"):
        st.write("More than 80% of products in Company A have Dairy product")

##############################################################################################################################
#SUPPLIER SCORING MODULE                                                                                                     #
##############################################################################################################################
    
        
def main():
    data = pd.DataFrame()
        
    
    add_selectbox = st.sidebar.selectbox(
        "How do you want to analysis the files ?",
        ("Cross-Analysis", "Single File Analysis", "Supplier Scoring")
    )
    
    if add_selectbox == "Cross-Analysis":
        st.title("Risk Assessment 3PA")
        st.markdown("> __Analysis the 3PA documents base on different attribute and connecting with outside database__")
        st.markdown("> __Please look at the instruction before start surfing the web.__")
        st.markdown("> __With each of the graph, there will be an explanation on the uses and purpose of using this specific graph__")
        with st.expander("Instruction"):
            st.markdown("__When you first open the app, please follow the instruction here to have the best experience__")
            st.markdown("On the top right corner of the app, there is a __3 line button__, please press on that one and choose __Setting__ ")
            st.markdown("After that, under the __APPEARANCE__ tab, please tick __WIDE MODE__")
            st.markdown("This would improve your experience on the website. Thank you")
        with st.sidebar.expander("Defition and Usage:"):
            st.write("The uses of cross-analysis is to help user compare between all of the files that they upload on when doing risk analysis on Otrafy. This give the user a clearer view of all of the files without spending time to read")
        cross_analysis()
    
    elif add_selectbox == "Single File Analysis":
        st.title("Risk Assessment 3PA")
        st.markdown("> __Analysis the 3PA documents base on different attribute and connecting with outside database__")
        st.markdown("> __Please look at the instruction before start surfing the web.__")
        st.markdown("> __With each of the graph, there will be an explanation on the uses and purpose of using this specific graph__")
        with st.expander("Instruction"):
            st.markdown("__When you first open the app, please follow the instruction here to have the best experience__")
            st.markdown("On the top right corner of the app, there is a __3 line button__, please press on that one and choose __Setting__ ")
            st.markdown("After that, under the __APPEARANCE__ tab, please tick __WIDE MODE__")
            st.markdown("This would improve your experience on the website. Thank you")
        with st.sidebar.expander("Defition and Usage:"):
            st.write("With Single File Analysis, user will focus on one specific file that they interested in or they curious to understand more about the file specifically.")
        single_analysis()
    
    elif add_selectbox == "Supplier Scoring":
        with st.sidebar.expander("Defition and Usage:"):
            st.write("A score-card to given user a clearer view of a supplier based multiple of aspect such as Recall /Alerts in last 24 months, History of Food Fraud, GFSI and Other Certificate etc.")
        main_features()

if __name__ == "__main__":
    main()