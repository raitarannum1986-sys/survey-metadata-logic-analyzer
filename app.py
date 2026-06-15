import streamlit as st
import pandas as pd
from collections import Counter


from parsers.xml_parser import load_xml
from parsers.question_extractor import extract_questions
from parsers.logic_extractor import extract_logic
from visualizers.graph_builder import build_basic_flow
import traceback
import plotly.express as px


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Survey Logic Flow Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background: linear-gradient(90deg,#2563eb,#4f46e5);
color:white;
margin-bottom:20px;
">
<h1 style="margin:0;">🔄 Survey Metadata & Logic Analyzer</h1>
<p style="margin:0;">Analyze survey structure, logic and metadata from XML files</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("📂 Survey Tools")

    st.info("""
    Upload XML files to:

    • Extract Questions
    • Visualize Logic Flow
    • Explore XML Structure
    • Analyze Routing
    """)

    st.divider()

    st.write("Version 1.0")



# ==================================================
# FILE UPLOAD
# ==================================================

col1, col2 = st.columns([4,1])

with col1:
    uploaded_file = st.file_uploader(
        "📂 Upload Survey XML File",
        type=["xml"]
    )

with col2:
    st.write("")
    st.write("")
    use_demo = st.button(
        "🎯 Demo Survey",
        use_container_width=True
    )

if use_demo:
    uploaded_file = open(
        "sample_files/demo_survey.xml",
        "rb"
    )



# ==================================================
# MAIN PROCESSING
# ==================================================

if uploaded_file:

    try:

        # ------------------------------------------
        # Load XML
        # ------------------------------------------

        root = load_xml(uploaded_file)



        # ------------------------------------------
        # Extract Data
        # ------------------------------------------
    
        questions, hidden_count = extract_questions(root)
        



        logic_edges = extract_logic(root)

        
        questions_df = pd.DataFrame(questions)
        
        logic_df = pd.DataFrame(logic_edges)

        

        


        

        # ------------------------------------------
        # XML Tag Analysis
        # ------------------------------------------

        tag_counter = Counter()

        for elem in root.iter():
            tag_counter[elem.tag] += 1

        tag_df = (
            pd.DataFrame(
                tag_counter.items(),
                columns=["Tag", "Count"]
            )
            .sort_values("Count", ascending=False)
        )

        unique_tags = sorted(
            
            set(elem.tag for elem in root.iter())
        )

        normal_count = len(
        questions_df[
        questions_df["variable_type"] == "Normal"
    ]
)

        panel_count = len(
            questions_df[
                questions_df["variable_type"] == "Panel"
            ]
        )

        background_count = len(
            questions_df[
                questions_df["variable_type"] == "Background"
            ]
        )

        st.success(
            f"Loaded successfully • "
            f"{len(questions):,} variables • "
            f"{len(logic_edges):,} logic elements • "
            f"{len(unique_tags):,} XML tags"
        )

        # ------------------------------------------
        # Metrics
        # ------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📋 Survey Questions",
                normal_count
            )

        with col2:
            st.metric(
                "👻 Hidden",
                hidden_count
            )

        with col3:
            st.metric(
                "📦 Panel",
                panel_count
            )

        with col4:
            st.metric(
                "🌍 Background",
                background_count
            )
        

        st.subheader("📊 Survey Profile")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Variables", len(questions))

        with col_b:
            st.metric("Logic Elements", len(logic_edges))

        with col_c:
            st.metric("XML Tags", len(unique_tags))


        # ------------------------------------------
        # Tabs
        # ------------------------------------------

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Variables",
            "🔗 Logic Analysis",
            "📊 Survey Flow",
            "🔍 XML Explorer",
            "🔍 Metadata Dashboard",
        
        ]
        )
        # ==========================================
        # QUESTIONS TAB
        # ==========================================

        with tab1:
                st.subheader("Survey Variables")

                if not questions_df.empty:

                    search_var = st.text_input(
                    "Search Variable"
                )
                    
                

                    display_df = questions_df.copy()

                    if search_var:
                        display_df = display_df[
                            display_df["name"]
                            .astype(str)
                            .str.contains(
                                search_var,
                                case=False,
                                na=False
                            )
                        ]

                    variable_types = sorted(
                        questions_df["variable_type"]
                        .dropna()
                        .unique()
                    )


                    selected_types = st.multiselect(
                    "Variable types to Display",
                    options=variable_types,
                    default=[
                        "Normal"
                    ]
                )

                    display_df = display_df[
                    display_df["variable_type"]
                    .isin(selected_types)
                ]

                    st.caption(
                        f"Showing {len(display_df):,} of {len(questions_df):,} variables"
                    )

                    st.download_button(
                    "📥 Download Variables CSV",
                    display_df.to_csv(index=False),
                    file_name="survey_variables.csv",
                    mime="text/csv"
                )

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        height=600
                    )

                    if "variable_type" in questions_df.columns:

                        st.subheader("Variable type Breakdown")

                        variable_counts = (
                            questions_df["variable_type"]
                            .value_counts()
                            .reset_index()
                        )

                        variable_counts.columns = [
                            "variable_type",
                            "count"
                        ]

                        col1, col2 = st.columns([1, 1])

                        with col1:
                            st.dataframe(
                                variable_counts,
                                use_container_width=True
                            )

                        with col2:
                            fig = px.pie(
                                variable_counts,
                                names="variable_type",
                                values="count",
                                title="Variable Distribution"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                    if "type" in questions_df.columns:

                        st.subheader(
                            "Question type Breakdown"
                        )

                        type_counts = (
                            questions_df["type"]
                            .value_counts()
                            .reset_index(name="count")
                        )

                        type_counts.columns = ["type", "count"]

                        col1, col2 = st.columns([1, 1])

                        with col1:
                            st.dataframe(
                                type_counts,
                                use_container_width=True
                            )

                        with col2:
                            fig = px.bar(
                                type_counts,
                                x="type",
                                y="count",
                                title="Question type Distribution"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )


# ==========================================
# VARIABLE INSPECTOR
# ==========================================
                st.caption(
                f"{len(questions_df):,} variables available"
            )

                st.subheader("🔎 Variable Inspector")

                search_text = st.text_input(
                    "Filter Variables"
                )

                filtered_vars = sorted(
                    questions_df[
                        questions_df["name"]
                        .astype(str)
                        .str.contains(
                            search_text,
                            case=False,
                            na=False
                        )
                    ]["name"]
                    .dropna()
                    .unique()
                )

                if filtered_vars:

                    selected_var = st.selectbox(
                        "Select Variable",
                        filtered_vars
                    )

                    record = questions_df[
                        questions_df["name"] == selected_var
                    ].iloc[0]

                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.markdown("**Variable**")
                        st.write(record["name"])

                    with c2:
                        st.metric(
                            "type",
                            record.get("type", "")
                        )

                    with c3:
                        st.metric(
                            "Category",
                            record.get("variable_type", "")
                        )

                    with c4:
                        st.metric(
                            "Entity ID",
                            record.get("entity_id", "")
                        )

                    st.subheader("Variable Details")

                    details_df = pd.DataFrame(
                        {
                            "Attribute": record.index,
                            "Value": record.values
                        }
                    )

                    st.dataframe(
                        details_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.download_button(
                    "📥 Download XML Tag Statistics",
                    tag_df.to_csv(index=False),
                    file_name="xml_tags.csv",
                    mime="text/csv"
                )

                else:

                    st.warning(
                        "No matching variables found."
                    )
# ==========================================
# LOGIC TAB
# ==========================================

        with tab2:

            if logic_df.empty:

                st.warning(
                    "No logic elements detected."
                )

            else:

                st.subheader("📊 Logic Tag Distribution")

                logic_summary = (
                    logic_df["tag"]
                    .value_counts()
                    .reset_index()
                )

                logic_summary.columns = [
                    "Logic Element",
                    "Count"
                ]

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.dataframe(
                        logic_summary,
                        use_container_width=True,
                        hide_index=True
                    )

                with col2:
                    fig = px.bar(
                        logic_summary,
                        x="Logic Element",
                        y="Count",
                        title="Logic Elements Found in XML"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                st.info(
    "Shows frequency of logic-related XML tags detected in the survey structure."
                )

                st.subheader("Logic Elements")

                st.dataframe(
                    logic_df,
                    use_container_width=True,
                    height=500
                )

                st.download_button(
                    "📥 Download Logic CSV",
                    logic_df.to_csv(index=False),
                    file_name="logic_elements.csv",
                    mime="text/csv"
                )


        # ==========================================
        # FLOW TAB
        # ==========================================

        with tab3:

                st.info(
                    "Flow Visualization (Beta) • Displays survey structure and question sequence. Advanced routing visualization is under development."
                )

                flow_questions = [

                    q

                    for q in questions

                    if q["variable_type"] == "Normal"
                    and q["type"] in ["Single", "Multi", "Open", "Grid"]

                ]

                original_count = len(flow_questions)

                if flow_questions:

                    st.caption(
                    f"Total survey questions: {original_count}"
                )

                    MAX_FLOW_NODES = 250

                    

                    if original_count > MAX_FLOW_NODES:
                        st.warning(
                            f"Large survey detected. Showing first {MAX_FLOW_NODES} questions."
                        )

                

                    flow_questions = flow_questions[:MAX_FLOW_NODES]

                    dot = build_basic_flow(
                    flow_questions
                    )

                    dot.attr(rankdir="LR")

                    st.graphviz_chart(
                        dot,
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "No survey questions available for flow diagram."
                    )
            # ==========================================
            # XML EXPLORER
            # ==========================================

        with tab4:

            with st.expander("Top XML Tags"):

                st.dataframe(
                    tag_df.head(25),
                    use_container_width=True
                )
            st.subheader("XML Explorer")

            st.write(
                f"Root Tag: {root.tag}"
            )

            search_text = st.text_input(
                "Search XML Tags"
            )



            filtered_df = tag_df[
                tag_df["Tag"]
                .str.contains(search_text, case=False, na=False)
            ]

            st.dataframe(
            filtered_df,
            use_container_width=True
        )

            st.subheader(
                "Inspect Specific Tag"
            )

            tag_to_inspect = st.text_input(
                "Enter exact tag name"
            )

            if tag_to_inspect:

                count = 0

                
            with st.expander(
                "Preview First 100 XML Elements"
            ):

                preview_data = []

                for elem in list(root.iter())[:100]:

                    preview_data.append(
                        {
                            "Tag": elem.tag,
                            "Attributes": str(elem.attrib)
                        }
                    )

                st.dataframe(
                    pd.DataFrame(
                        preview_data
                    ),
                    use_container_width=True
                )

        with tab5:
            st.subheader("📊 Survey Metadata")

            import os

            if hasattr(uploaded_file, "size"):
                xml_size_mb = round(
                    uploaded_file.size / (1024 * 1024),
                    2
                )
            else:
                xml_size_mb = round(
                    os.path.getsize(uploaded_file.name)
                    / (1024 * 1024),
                    2
                )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Questions", len(questions_df))
            col2.metric("Logic Rules", len(logic_df))
            col3.metric("Question Types", questions_df["type"].nunique())
            col4.metric(
            "XML Size (MB)",
            xml_size_mb
        )

            
            st.subheader("Question type Distribution")

            type_counts = (
                questions_df["type"]
                .value_counts()
                .reset_index()
            )

            type_counts.columns = ["Question type", "Count"]

            st.dataframe(type_counts, use_container_width=True) 

            st.subheader("Question Type Distribution")

            type_counts = questions_df["type"].value_counts()

            var_counts = questions_df["variable_type"].value_counts()

            fig = px.bar(
            x=var_counts.index,
            y=var_counts.values,
            labels={"x":"Variable Type","y":"Count"},
            title="Variable Type Distribution"
        )

            fig = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            labels={"x":"Question Type","y":"Count"},
            title="Question Type Distribution"
        )

            st.plotly_chart(fig, use_container_width=True)

            st.bar_chart(type_counts)  

            st.subheader("Logic Targets")


                 
            st.subheader("Survey Structure")

            summary = {
                "Questions": len(questions_df),
                "Logic Rules": len(logic_df),
                "Unique Question types":
                    questions_df["type"].nunique(),
                "Question types":
                    ", ".join(
                        sorted(
                            questions_df["type"]
                            .dropna()
                            .unique()
                        )
                    )
            }

            st.json(summary)   

            metadata_df = pd.DataFrame([summary])

            st.download_button(
                "📥 Download Metadata",
                metadata_df.to_csv(index=False),
                file_name="survey_metadata.csv",
                mime="text/csv"
            )

            st.subheader("✅ Validation Report")

            v1, v2, v3 = st.columns(3)

            with v1:
                st.metric(
                    "Duplicate Variables",
                    questions_df["name"].duplicated().sum()
                )

            with v2:
                st.metric(
                    "Missing Names",
                    questions_df["name"].isna().sum()
                )

            with v3:
                st.metric(
                    "Missing Entity IDs",
                    questions_df["entity_id"].isna().sum()
                )

            if (
                questions_df["name"].duplicated().sum() == 0
                and questions_df["name"].isna().sum() == 0
            ):
                st.success("✓ Validation Passed")

  
    except Exception as e:
        st.error(f"Error loading XML: {e}")

        with st.expander("Error Details"):
            st.code(traceback.format_exc())
st.caption(
    "Survey Metadata & Logic Analyzer | Version 1.0 | Built with Streamlit & Graphviz"
)



