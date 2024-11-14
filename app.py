# import streamlit as st
# import tensorflow as tf
# import numpy as np
# import pandas as pd
# import json
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime
# from predictor import UnifiedRealEstatePredictor
# from project_types import ProjectType

# def init_predictor():
#     try:
#         predictor = UnifiedRealEstatePredictor()
#         return predictor
#     except Exception as e:
#         st.error(f"خطأ في تهيئة النظام: {str(e)}")
#         return None
# # Define predictor as a global variable
# predictor = None

# def create_streamlit_app():
#     global predictor  # Add this line to use the global predictor
    
#     st.set_page_config(
#         page_title="نظام تحليل الاستثمارات العقارية",
#         page_icon="🏢",
#         layout="wide"
#     )

#     # Initialize predictor at the start
#     if predictor is None:
#         predictor = init_predictor()
#         if predictor is None:
#             st.error("فشل في تهيئة النظام. يرجى المحاولة مرة أخرى.")
#             return

#     # Sidebar section
#     with st.sidebar:
#         st.header("إعدادات النموذج")
#         epochs = st.slider("عدد مرات التدريب", 10, 100, 50)
#         if st.button("تدريب النموذج"):
#             with st.spinner("جاري تدريب النموذج..."):
#                 try:
#                     for project_type in ProjectType:
#                         predictor.train_project_type(project_type, epochs=epochs)
#                     st.success("تم تدريب النموذج بنجاح!")
#                 except Exception as e:
#                     st.error(f"حدث خطأ أثناء التدريب: {str(e)}")
    
#     # Custom CSS for RTL support and styling
#     st.markdown("""
#         <style>
#         .css-1d391kg, .stMarkdown, .stButton, .stSelectbox, .stNumberInput {
#             direction: rtl;
#         }
#         .stButton>button {
#             width: 100%;
#             background-color: #0083B8;
#             color: white;
#         }
#         div[data-testid="stMarkdownContainer"] {
#             text-align: right;
#         }
#         .metric-card {
#             background-color: #f0f2f6;
#             border-radius: 10px;
#             padding: 20px;
#             margin: 10px 0;
#         }
#         .big-number {
#             font-size: 24px;
#             font-weight: bold;
#             color: #0083B8;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    
#     st.title("نظام تحليل الاستثمارات العقارية")
    
#     # Initialize predictor
#     predictor = init_predictor()
    
#     if predictor is None:
#         st.error("فشل في تهيئة النظام. يرجى المحاولة مرة أخرى.")
#         return

#     # Main input form
#     with st.form("analysis_form"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             project_type = st.selectbox(
#                 "نوع المشروع",
#                 options=list(ProjectType),
#                 format_func=lambda x: x.value
#             )
            
#             location = st.selectbox(
#                 "الموقع",
#                 options=list(predictor.location_prices.keys())
#             )
            
#             land_area = st.number_input(
#                 "مساحة الأرض (متر مربع)",
#                 min_value=100,
#                 max_value=50000,
#                 value=1000,
#                 step=100
#             )

#         with col2:
#             floors = st.number_input(
#                 "عدد الطوابق",
#                 min_value=1,
#                 max_value=10,
#                 value=3
#             )
            
#             st.subheader("ظروف السوق")
#             demand_level = st.select_slider(
#                 "مستوى الطلب",
#                 options=[0.8, 1.0, 1.2],
#                 value=1.0,
#                 format_func=lambda x: {0.8: "منخفض", 1.0: "متوسط", 1.2: "مرتفع"}[x]
#             )
            
#             competition_level = st.select_slider(
#                 "مستوى المنافسة",
#                 options=[0.8, 1.0, 1.2],
#                 value=1.0,
#                 format_func=lambda x: {0.8: "منخفض", 1.0: "متوسط", 1.2: "مرتفع"}[x]
#             )

#         submitted = st.form_submit_button("تحليل المشروع")

#     if submitted:
#         try:
#             with st.spinner("جاري تحليل المشروع..."):
#                 market_conditions = {
#                     "demand_level": demand_level,
#                     "competition_level": competition_level
#                 }
                
#                 result = predictor.predict(
#                     project_type=project_type,
#                     location=location,
#                     land_area=land_area,
#                     floors=floors,
#                     market_conditions=market_conditions
#                 )
                
#                 display_results(result)
                
#         except Exception as e:
#             st.error(f"حدث خطأ أثناء التحليل: {str(e)}")

# def display_results(result):
#     """Display prediction results with visualizations"""
#     st.header("نتائج التحليل")
    
#     # Project Details
#     st.subheader("تفاصيل المشروع")
#     details = result["تقرير_تحليل_الاستثمار"]["تفاصيل_المشروع"]
#     cols = st.columns(len(details))
#     for col, (key, value) in zip(cols, details.items()):
#         col.metric(key, value)

#     # Financial Analysis
#     st.subheader("التحليل المالي")
#     financials = result["تقرير_تحليل_الاستثمار"]["توقعات_التمويل"]
    
#     # Costs
#     st.write("التكاليف")
#     costs_cols = st.columns(3)
#     costs = financials["تكاليف_المشروع"]
#     for i, (key, value) in enumerate(costs.items()):
#         if isinstance(value, str):
#             costs_cols[i % 3].metric(key, value)
    
#     # Revenues
#     st.write("الإيرادات")
#     revenue_cols = st.columns(3)
#     revenues = financials["الإيرادات_المتوقعة"]
#     for i, (key, value) in enumerate(revenues.items()):
#         revenue_cols[i % 3].metric(key, value)

#     # Market Analysis
#     st.subheader("تحليل السوق")
#     market = result["تقرير_تحليل_الاستثمار"]["تحليل_السوق"]
#     market_cols = st.columns(len(market))
#     for col, (key, value) in zip(market_cols, market.items()):
#         col.metric(key, value)

#     # Performance Indicators
#     st.subheader("مؤشرات الأداء")
#     performance = result["تقرير_تحليل_الاستثمار"]["مؤشرات_الأداء"]
#     perf_cols = st.columns(len(performance))
#     for col, (key, value) in zip(perf_cols, performance.items()):
#         col.metric(key, value)

#     # Additional Details if available
#     if "تفاصيل_إضافية" in result["تقرير_تحليل_الاستثمار"]:
#         st.subheader("تفاصيل إضافية")
#         additional = result["تقرير_تحليل_الاستثمار"]["تفاصيل_إضافية"]
#         add_cols = st.columns(len([k for k, v in additional.items() if not isinstance(v, list)]))
#         col_idx = 0
#         for key, value in additional.items():
#             if isinstance(value, list):
#                 st.write(f"{key}:", ", ".join(value))
#             else:
#                 add_cols[col_idx].metric(key, value)
#                 col_idx += 1

#     # Download button for full report
#     st.download_button(
#         label="تحميل التقرير الكامل",
#         data=json.dumps(result, ensure_ascii=False, indent=2),
#         file_name=f"real_estate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#         mime="application/json"
#     )

# if __name__ == "__main__":
#     create_streamlit_app()



import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from predictor import UnifiedRealEstatePredictor
from project_types import ProjectType
from formulas import UnifiedCalculator  # Add this import

def init_systems():
    try:
        predictor = UnifiedRealEstatePredictor()
        calculator = UnifiedCalculator()  # Add calculator initialization
        return predictor, calculator
    except Exception as e:
        st.error(f"خطأ في تهيئة النظام: {str(e)}")
        return None, None

# Define global variables
predictor = None
calculator = None  # Add calculator

def create_streamlit_app():
    global predictor, calculator  # Update global variables
    
    st.set_page_config(
        page_title="نظام تحليل الاستثمارات العقارية",
        page_icon="🏢",
        layout="wide"
    )

    # Initialize systems at the start
    if predictor is None or calculator is None:
        predictor, calculator = init_systems()
        if predictor is None or calculator is None:
            st.error("فشل في تهيئة النظام. يرجى المحاولة مرة أخرى.")
            return

    # Sidebar section
        # Sidebar section
        # Sidebar section
    with st.sidebar:
        st.header("System Settings")
        analysis_type = st.radio(
            "Analysis Type",
            ["Predictive Analysis", "Detailed Analysis"],
            index=0
        )
        if analysis_type == "Predictive Analysis":
            epochs = st.slider("Training Epochs", 2, 10, 5)
            batch_size = st.slider("Batch Size", 64, 512, 128)
            if st.button("Train Model"):
                with st.spinner("Training in progress..."):
                    try:
                        for project_type in ProjectType:
                            predictor.train_project_type(project_type, epochs=epochs)
                        st.success("Model trained successfully!")
                    except Exception as e:
                        st.error(f"Training error: {str(e)}")

    # Main input form
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_type = st.selectbox(
                "Project Type",
                options=list(ProjectType),
                format_func=lambda x: x.value
            )
            
            location = st.selectbox(
                "Location",
                options=list(predictor.location_prices.keys())
            )
            
            land_area = st.number_input(
                "Land Area (sq m)",
                min_value=100,
                max_value=50000,
                value=1000,
                step=100
            )

        with col2:
            floors = st.number_input(
                "Number of Floors",
                min_value=1,
                max_value=10,
                value=3
            )
            
            if analysis_type == "Predictive Analysis":
                st.subheader("Market Conditions")
                demand_level = st.select_slider(
                    "Demand Level",
                    options=[0.8, 1.0, 1.2],
                    value=1.0,
                    format_func=lambda x: {0.8: "Low", 1.0: "Medium", 1.2: "High"}[x]
                )
                
                competition_level = st.select_slider(
                    "Competition Level",
                    options=[0.8, 1.0, 1.2],
                    value=1.0,
                    format_func=lambda x: {0.8: "Low", 1.0: "Medium", 1.2: "High"}[x]
                )

        submitted = st.form_submit_button("Analyze Project")

    if submitted:
        try:
            with st.spinner("جاري تحليل المشروع..."):
                if analysis_type == "تحليل تنبؤي":
                    market_conditions = {
                        "demand_level": demand_level,
                        "competition_level": competition_level
                    }
                    result = predictor.predict(
                        project_type=project_type,
                        location=location,
                        land_area=land_area,
                        floors=floors,
                        market_conditions=market_conditions
                    )
                    display_prediction_results(result)
                else:
                    # Handle detailed analysis based on project type
                    result = calculate_detailed_analysis(
                        calculator=calculator,
                        project_type=project_type,
                        land_area=land_area,
                        location=location,
                        floors=floors
                    )
                    display_detailed_results(result)
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء التحليل: {str(e)}")

def calculate_detailed_analysis(calculator, project_type, land_area, location, floors):
    """Handle detailed analysis calculations based on project type"""
    params = {
        "land_area": land_area,
        "location": location,
    }
    
    if project_type not in [ProjectType.VILLA, ProjectType.SINGLE_VILLA, ProjectType.RESIDENTIAL_COMPOUND, ProjectType.ADMIN_BUILDING]:
        params["floors"] = floors

    if project_type == ProjectType.SHOPPING_MALL:
        return calculator.calculate_mall_context(**params)
    elif project_type == ProjectType.RESIDENTIAL:
        return calculator.calculate_residential_context(**params)
    elif project_type == ProjectType.COMMERCIAL:
        return calculator.calculate_commercial_context(**params)
    elif project_type == ProjectType.MIXED_USE:
        return calculator.calculate_mixed_use_context(**params)
    elif project_type == ProjectType.VILLA:
        return calculator.calculate_villa_context(**params)
    elif project_type == ProjectType.SINGLE_VILLA:
        return calculator.calculate_villa_analysis(**params)
    elif project_type == ProjectType.RESIDENTIAL_COMPOUND:
        params["effective_land_ratio"] = 0.40
        return calculator.calculate_compound_analysis(**params)
    elif project_type == ProjectType.ADMIN_BUILDING:
        return calculator.calculate_admin_building_analysis(**params)

def display_prediction_results(result):
    """Display AI prediction results"""
    st.header("نتائج التحليل")
    
    # Project Details
    st.subheader("تفاصيل المشروع")
    details = result["تقرير_تحليل_الاستثمار"]["تفاصيل_المشروع"]
    cols = st.columns(len(details))
    for col, (key, value) in zip(cols, details.items()):
        col.metric(key, value)

    # Financial Analysis
    st.subheader("التحليل المالي")
    financials = result["تقرير_تحليل_الاستثمار"]["توقعات_التمويل"]
    
    # Costs
    st.write("التكاليف")
    costs_cols = st.columns(3)
    costs = financials["تكاليف_المشروع"]
    for i, (key, value) in enumerate(costs.items()):
        if isinstance(value, str):
            costs_cols[i % 3].metric(key, value)
    
    # Revenues
    st.write("الإيرادات")
    revenue_cols = st.columns(3)
    revenues = financials["الإيرادات_المتوقعة"]
    for i, (key, value) in enumerate(revenues.items()):
        revenue_cols[i % 3].metric(key, value)

    # Market Analysis
    st.subheader("تحليل السوق")
    market = result["تقرير_تحليل_الاستثمار"]["تحليل_السوق"]
    market_cols = st.columns(len(market))
    for col, (key, value) in zip(market_cols, market.items()):
        col.metric(key, value)

    # Performance Indicators
    st.subheader("مؤشرات الأداء")
    performance = result["تقرير_تحليل_الاستثمار"]["مؤشرات_الأداء"]
    perf_cols = st.columns(len(performance))
    for col, (key, value) in zip(perf_cols, performance.items()):
        col.metric(key, value)

    # Download button for full report
    st.download_button(
        label="تحميل التقرير الكامل",
        data=json.dumps(result, ensure_ascii=False, indent=2),
        file_name=f"real_estate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def display_detailed_results(result):
    """Display detailed formula-based results"""
    st.header("نتائج التحليل التفصيلي")
    
    # Convert the result to a more readable format
    st.json(result, expanded=False)
    
    # Download button for full report
    st.download_button(
        label="تحميل التقرير الكامل",
        data=json.dumps(result, ensure_ascii=False, indent=2),
        file_name=f"detailed_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if __name__ == "__main__":
    create_streamlit_app()