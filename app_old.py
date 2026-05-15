import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Load the Blinkit dataset automatically
@st.cache_data
def load_blinkit_data():
    try:
        file_path = "Tableau BlinkIT Grocery Project U16955293080 (4).csv"
        df = pd.read_csv(file_path)
        
        # Data cleaning and preprocessing
        # Clean Item_Fat_Content column
        df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
            'low fat': 'Low Fat',
            'LF': 'Low Fat',
            'reg': 'Regular'
        })
        
        # Fill missing Item_Weight with median
        df['Item_Weight'].fillna(df['Item_Weight'].median(), inplace=True)
        
        # Fill missing Outlet_Size with mode
        df['Outlet_Size'].fillna(df['Outlet_Size'].mode()[0], inplace=True)
        
        # Create outlet age
        current_year = datetime.now().year
        df['Outlet_Age'] = current_year - df['Outlet_Establishment_Year']
        
        # Create price per unit weight
        df['Price_per_Weight'] = df['Item_MRP'] / df['Item_Weight']
        
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Set page config
st.set_page_config(
    page_title="Blinkit Supply Chain Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B35;
        margin: 0.5rem 0;
    }
    .sidebar-header {
        font-size: 1.2rem;
        color: #FF6B35;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🛒 Blinkit Supply Chain Analytics Dashboard</h1>', unsafe_allow_html=True)

# Load data
df = load_blinkit_data()

if df is not None:
    # Store in session state
    st.session_state['data'] = df
    st.session_state['data_loaded'] = True
    
    # Sidebar for navigation
    st.sidebar.markdown('<p class="sidebar-header">📊 Navigation</p>', unsafe_allow_html=True)
    page = st.sidebar.selectbox(
        "Select Analysis Module:",
        [
            "📈 Overview",
            "📊 Sales Analysis", 
            "🔍 Product Performance",
            "🏪 Outlet Analysis",
            "� Inventory Insights",
            "� Supply Chain Metrics",
            "🎯 Predictive Analytics"
        ]
    )
else:
    st.error("❌ Could not load the Blinkit dataset. Please check if the file exists.")
    st.stop()

# File upload section
def upload_data_section():
    st.markdown("### 📁 Data Upload")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your dataset (CSV/Excel):",
            type=['csv', 'xlsx', 'xls']
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state['data'] = df
                st.success(f"✅ Data uploaded successfully! Shape: {df.shape}")
                
                # Display basic info
                st.markdown("#### 📋 Dataset Overview")
                st.dataframe(df.head())
                
                st.markdown("#### 📊 Dataset Info")
                buffer = st.empty()
                with buffer.container():
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.metric("Rows", df.shape[0])
                    with col_info2:
                        st.metric("Columns", df.shape[1])
                    with col_info3:
                        st.metric("Missing Values", df.isnull().sum().sum())
                
                # Column information
                st.markdown("#### 📝 Column Details")
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Data Type': df.dtypes.values,
                    'Non-Null Count': df.count().values,
                    'Missing Values': df.isnull().sum().values
                })
                st.dataframe(col_info)
                
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with col2:
        if 'data' in st.session_state:
            st.markdown("#### 🎯 Quick Insights")
            df = st.session_state['data']
            
            # Numeric columns summary
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                st.markdown("**Numeric Columns Summary:**")
                st.dataframe(df[numeric_cols].describe().round(2))
            
            # Categorical columns summary
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                st.markdown("**Categorical Columns Summary:**")
                cat_summary = []
                for col in categorical_cols[:5]:  # Show first 5
                    cat_summary.append({
                        'Column': col,
                        'Unique Values': df[col].nunique(),
                        'Top Value': df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'
                    })
                st.dataframe(pd.DataFrame(cat_summary))

# Overview page
def overview_page():
    st.markdown("## 📈 Supply Chain Overview")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first in the 'Data Upload & Exploration' section.")
        return
    
    df = st.session_state['data']
    
    # Key metrics
    st.markdown("### 🎯 Key Performance Indicators")
    
    # Try to identify common supply chain metrics
    metrics_row1 = st.columns(4)
    metrics_row2 = st.columns(4)
    
    with metrics_row1[0]:
        # Try to find orders column
        order_cols = [col for col in df.columns if 'order' in col.lower()]
        if order_cols:
            st.metric("Total Orders", len(df))
        else:
            st.metric("Total Records", len(df))
    
    with metrics_row1[1]:
        # Try to find revenue/amount column
        revenue_cols = [col for col in df.columns if any(x in col.lower() for x in ['revenue', 'amount', 'price', 'total'])]
        if revenue_cols and revenue_cols[0] in df.columns:
            total_revenue = df[revenue_cols[0]].sum()
            st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
        else:
            st.metric("Columns", df.shape[1])
    
    with metrics_row1[2]:
        # Try to find date column
        date_cols = [col for col in df.columns if any(x in col.lower() for x in ['date', 'time', 'created'])]
        if date_cols and date_cols[0] in df.columns:
            try:
                df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
                unique_days = df[date_cols[0]].dt.date.nunique()
                st.metric("Active Days", unique_days)
            except:
                st.metric("Date Columns", len(date_cols))
        else:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    with metrics_row1[3]:
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        st.metric("Data Quality", f"{100 - missing_pct:.1f}%")
    
    # Data visualization
    st.markdown("### 📊 Data Visualization")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown("#### 📈 Data Distribution")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Select column for distribution:", numeric_cols)
            
            fig = px.histogram(
                df, 
                x=selected_col, 
                title=f"Distribution of {selected_col}",
                color_discrete_sequence=['#FF6B35']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        st.markdown("#### 🔍 Correlation Matrix")
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(
                corr_matrix,
                title="Correlation Matrix",
                color_continuous_scale="RdYlBu",
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📋 Need at least 2 numeric columns for correlation analysis")

# Demand Forecasting page
def demand_forecasting_page():
    st.markdown("## 🔍 Demand Forecasting")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first.")
        return
    
    df = st.session_state['data']
    
    st.markdown("### 📊 Demand Analysis")
    
    # Try to identify demand-related columns
    demand_cols = [col for col in df.columns if any(x in col.lower() for x in ['demand', 'quantity', 'sales', 'order'])]
    date_cols = [col for col in df.columns if any(x in col.lower() for x in ['date', 'time'])]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if demand_cols:
            selected_demand = st.selectbox("Select demand metric:", demand_cols)
        else:
            selected_demand = st.selectbox("Select numeric column:", df.select_dtypes(include=[np.number]).columns.tolist())
    
    with col2:
        if date_cols:
            selected_date = st.selectbox("Select date column:", date_cols)
        else:
            st.info("📅 No date columns found. Using index.")
            selected_date = None
    
    if selected_demand:
        # Time series analysis
        if selected_date and selected_date in df.columns:
            try:
                df[selected_date] = pd.to_datetime(df[selected_date])
                df_sorted = df.sort_values(selected_date)
                
                # Plot time series
                fig = px.line(
                    df_sorted, 
                    x=selected_date, 
                    y=selected_demand,
                    title=f"Demand Trend: {selected_demand}",
                    color_discrete_sequence=['#FF6B35']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Simple moving average
                window_size = st.slider("Moving Average Window:", min_value=3, max_value=30, value=7)
                df_sorted[f'{selected_demand}_MA'] = df_sorted[selected_demand].rolling(window=window_size).mean()
                
                fig_ma = go.Figure()
                fig_ma.add_trace(go.Scatter(
                    x=df_sorted[selected_date], 
                    y=df_sorted[selected_demand],
                    mode='lines',
                    name='Actual Demand',
                    line=dict(color='#FF6B35')
                ))
                fig_ma.add_trace(go.Scatter(
                    x=df_sorted[selected_date], 
                    y=df_sorted[f'{selected_demand}_MA'],
                    mode='lines',
                    name=f'{window_size}-day Moving Average',
                    line=dict(color='#004E89', width=2)
                ))
                fig_ma.update_layout(title=f"Demand with {window_size}-day Moving Average")
                st.plotly_chart(fig_ma, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error processing date column: {str(e)}")
        else:
            # Simple distribution analysis
            fig = px.histogram(
                df, 
                x=selected_demand,
                title=f"Distribution of {selected_demand}",
                color_discrete_sequence=['#FF6B35']
            )
            st.plotly_chart(fig, use_container_width=True)

# Inventory Analysis page
def inventory_analysis_page():
    st.markdown("## 📦 Inventory Analysis")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first.")
        return
    
    df = st.session_state['data']
    
    st.markdown("### 📊 Inventory Metrics")
    
    # Look for inventory-related columns
    inventory_cols = [col for col in df.columns if any(x in col.lower() for x in ['inventory', 'stock', 'quantity', 'available'])]
    product_cols = [col for col in df.columns if any(x in col.lower() for x in ['product', 'item', 'sku'])]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if inventory_cols:
            selected_inventory = st.selectbox("Select inventory metric:", inventory_cols)
        else:
            selected_inventory = st.selectbox("Select numeric column:", df.select_dtypes(include=[np.number]).columns.tolist())
    
    with col2:
        if product_cols:
            selected_product = st.selectbox("Select product identifier:", product_cols)
        else:
            selected_product = st.selectbox("Select grouping column:", df.columns.tolist())
    
    if selected_inventory and selected_product:
        # Inventory summary by product
        inventory_summary = df.groupby(selected_product)[selected_inventory].agg(['sum', 'mean', 'count']).reset_index()
        inventory_summary.columns = [selected_product, 'Total_Inventory', 'Avg_Inventory', 'Transaction_Count']
        
        st.markdown("#### 📋 Inventory Summary by Product")
        st.dataframe(inventory_summary.sort_values('Total_Inventory', ascending=False).head(10))
        
        # Top products visualization
        fig = px.bar(
            inventory_summary.head(10),
            x=selected_product,
            y='Total_Inventory',
            title=f"Top 10 Products by {selected_inventory}",
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Inventory distribution
        fig_dist = px.histogram(
            inventory_summary,
            x='Total_Inventory',
            title="Inventory Distribution Across Products",
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig_dist, use_container_width=True)

# Delivery Optimization page
def delivery_optimization_page():
    st.markdown("## 🚚 Delivery Optimization")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first.")
        return
    
    df = st.session_state['data']
    
    st.markdown("### 📊 Delivery Analytics")
    
    # Look for delivery-related columns
    delivery_cols = [col for col in df.columns if any(x in col.lower() for x in ['delivery', 'shipping', 'transport'])]
    time_cols = [col for col in df.columns if any(x in col.lower() for x in ['time', 'duration', 'delay'])]
    location_cols = [col for col in df.columns if any(x in col.lower() for x in ['location', 'address', 'city', 'area'])]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if delivery_cols:
            selected_delivery = st.selectbox("Select delivery metric:", delivery_cols)
        else:
            selected_delivery = st.selectbox("Select numeric column:", df.select_dtypes(include=[np.number]).columns.tolist())
    
    with col2:
        if time_cols:
            selected_time = st.selectbox("Select time metric:", time_cols)
        else:
            selected_time = None
    
    if selected_delivery:
        # Delivery performance metrics
        st.markdown("#### 📈 Delivery Performance")
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            avg_delivery = df[selected_delivery].mean()
            st.metric("Average", f"{avg_delivery:.2f}")
        
        with metrics_col2:
            median_delivery = df[selected_delivery].median()
            st.metric("Median", f"{median_delivery:.2f}")
        
        with metrics_col3:
            std_delivery = df[selected_delivery].std()
            st.metric("Std Dev", f"{std_delivery:.2f}")
        
        # Distribution plot
        fig = px.histogram(
            df,
            x=selected_delivery,
            title=f"Distribution of {selected_delivery}",
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Time series if available
        if selected_time and selected_time in df.columns:
            fig_time = px.scatter(
                df,
                x=selected_time,
                y=selected_delivery,
                title=f"{selected_delivery} vs {selected_time}",
                color_discrete_sequence=['#FF6B35']
            )
            st.plotly_chart(fig_time, use_container_width=True)

# Performance Metrics page
def performance_metrics_page():
    st.markdown("## 📈 Performance Metrics")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first.")
        return
    
    df = st.session_state['data']
    
    st.markdown("### 🎯 Key Performance Indicators")
    
    # Calculate various metrics
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        # Metrics grid
        metrics_grid = st.columns(4)
        
        for i, col in enumerate(numeric_cols[:8]):  # Show first 8 metrics
            with metrics_grid[i % 4]:
                if df[col].dtype in ['int64', 'float64']:
                    st.metric(
                        col.replace('_', ' ').title(),
                        f"{df[col].sum():,.2f}" if df[col].sum() > 1000 else f"{df[col].sum():.2f}",
                        f"Avg: {df[col].mean():.2f}"
                    )
        
        # Performance trends
        st.markdown("#### 📊 Performance Trends")
        
        selected_metrics = st.multiselect(
            "Select metrics to compare:",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if selected_metrics:
            # Create correlation heatmap
            if len(selected_metrics) > 1:
                corr_data = df[selected_metrics].corr()
                fig = px.imshow(
                    corr_data,
                    title="Metrics Correlation Matrix",
                    color_continuous_scale="RdYlBu",
                    aspect="auto"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Distribution comparison
            fig_dist = make_subplots(
                rows=2, cols=2,
                subplot_titles=selected_metrics[:4] if len(selected_metrics) >= 4 else selected_metrics
            )
            
            for i, metric in enumerate(selected_metrics[:4]):
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                fig_dist.add_trace(
                    go.Histogram(x=df[metric], name=metric, marker_color='#FF6B35'),
                    row=row, col=col
                )
            
            fig_dist.update_layout(title="Metrics Distribution Comparison")
            st.plotly_chart(fig_dist, use_container_width=True)

# Predictive Analytics page
def predictive_analytics_page():
    st.markdown("## 🎯 Predictive Analytics")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Please upload data first.")
        return
    
    df = st.session_state['data']
    
    st.markdown("### 🔮 Predictive Modeling")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ Need at least 2 numeric columns for predictive analysis.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_col = st.selectbox("Select target variable:", numeric_cols)
    
    with col2:
        feature_cols = st.multiselect(
            "Select feature variables:",
            [col for col in numeric_cols if col != target_col],
            default=[col for col in numeric_cols if col != target_col][:3]
        )
    
    if target_col and feature_cols:
        # Simple linear regression visualization
        if len(feature_cols) >= 1:
            selected_feature = feature_cols[0]
            
            fig = px.scatter(
                df,
                x=selected_feature,
                y=target_col,
                title=f"{target_col} vs {selected_feature}",
                trendline="ols",
                color_discrete_sequence=['#FF6B35']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature importance (simplified)
            st.markdown("#### 📊 Feature Correlation with Target")
            
            correlations = []
            for feature in feature_cols:
                corr = df[feature].corr(df[target_col])
                correlations.append({'Feature': feature, 'Correlation': corr})
            
            corr_df = pd.DataFrame(correlations).sort_values('Correlation', key=abs, ascending=False)
            
            fig_corr = px.bar(
                corr_df,
                x='Feature',
                y='Correlation',
                title="Feature Correlation with Target",
                color='Correlation',
                color_continuous_scale="RdYlBu"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.dataframe(corr_df)

# Main navigation
if page == "📊 Data Upload & Exploration":
    upload_data_section()
elif page == "📈 Overview":
    overview_page()
elif page == "🔍 Demand Forecasting":
    demand_forecasting_page()
elif page == "📦 Inventory Analysis":
    inventory_analysis_page()
elif page == "🚚 Delivery Optimization":
    delivery_optimization_page()
elif page == "📈 Performance Metrics":
    performance_metrics_page()
elif page == "🎯 Predictive Analytics":
    predictive_analytics_page()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Blinkit Supply Chain Analytics Dashboard | Built with Streamlit</p>
        <p>🚀 Real-time insights for supply chain optimization</p>
    </div>
    """,
    unsafe_allow_html=True
)
