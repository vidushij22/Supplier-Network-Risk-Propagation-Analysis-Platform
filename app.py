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

# Load Blinkit dataset automatically
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
            "📦 Inventory Insights",
            "🚚 Supply Chain Metrics",
            "🎯 Predictive Analytics"
        ]
    )
else:
    st.error("❌ Could not load the Blinkit dataset. Please check if the file exists.")
    st.stop()

# Overview page
def overview_page():
    st.markdown("## 📈 Blinkit Supply Chain Overview")
    
    # Key metrics
    st.markdown("### 🎯 Key Performance Indicators")
    
    metrics_row1 = st.columns(4)
    metrics_row2 = st.columns(4)
    
    with metrics_row1[0]:
        total_products = df['Item_Identifier'].nunique()
        st.metric("Total Products", total_products)
    
    with metrics_row1[1]:
        total_sales = df['Item_Outlet_Sales'].sum()
        st.metric("Total Sales", f"₹{total_sales:,.2f}")
    
    with metrics_row1[2]:
        total_outlets = df['Outlet_Identifier'].nunique()
        st.metric("Total Outlets", total_outlets)
    
    with metrics_row1[3]:
        avg_sales = df['Item_Outlet_Sales'].mean()
        st.metric("Avg Sales per Item", f"₹{avg_sales:.2f}")
    
    with metrics_row2[0]:
        avg_item_weight = df['Item_Weight'].mean()
        st.metric("Avg Item Weight", f"{avg_item_weight:.2f} kg")
    
    with metrics_row2[1]:
        avg_mrp = df['Item_MRP'].mean()
        st.metric("Avg MRP", f"₹{avg_mrp:.2f}")
    
    with metrics_row2[2]:
        avg_outlet_age = df['Outlet_Age'].mean()
        st.metric("Avg Outlet Age", f"{avg_outlet_age:.1f} years")
    
    with metrics_row2[3]:
        data_quality = (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        st.metric("Data Quality", f"{data_quality:.1f}%")
    
    # Data visualization
    st.markdown("### 📊 Data Visualization")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown("#### 📈 Sales Distribution")
        fig = px.histogram(
            df, 
            x='Item_Outlet_Sales', 
            title="Sales Distribution",
            color_discrete_sequence=['#FF6B35'],
            nbins=50
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        st.markdown("#### 🏪 Outlet Performance")
        outlet_sales = df.groupby('Outlet_Identifier')['Item_Outlet_Sales'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=outlet_sales.index,
            y=outlet_sales.values,
            title="Total Sales by Outlet",
            color_discrete_sequence=['#FF6B35']
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Product categories
    st.markdown("### 🛍️ Product Categories Analysis")
    
    cat_col1, cat_col2 = st.columns(2)
    
    with cat_col1:
        category_sales = df.groupby('Item_Type')['Item_Outlet_Sales'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=category_sales.index,
            y=category_sales.values,
            title="Sales by Product Category",
            color_discrete_sequence=['#FF6B35']
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with cat_col2:
        category_count = df['Item_Type'].value_counts()
        fig = px.pie(
            values=category_count.values,
            names=category_count.index,
            title="Product Category Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# Sales Analysis page
def sales_analysis_page():
    st.markdown("## 📊 Sales Analysis")
    
    # Sales by different dimensions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Sales by Fat Content")
        fat_sales = df.groupby('Item_Fat_Content')['Item_Outlet_Sales'].agg(['sum', 'mean', 'count'])
        st.dataframe(fat_sales.round(2))
        
        fig = px.bar(
            x=fat_sales.index,
            y=fat_sales['sum'],
            title="Total Sales by Fat Content",
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📍 Sales by Outlet Location")
        location_sales = df.groupby('Outlet_Location_Type')['Item_Outlet_Sales'].agg(['sum', 'mean', 'count'])
        st.dataframe(location_sales.round(2))
        
        fig = px.bar(
            x=location_sales.index,
            y=location_sales['sum'],
            title="Total Sales by Location Type",
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sales vs MRP analysis
    st.markdown("### 📈 Sales vs MRP Analysis")
    
    fig_scatter = px.scatter(
        df,
        x='Item_MRP',
        y='Item_Outlet_Sales',
        color='Item_Type',
        title="Sales vs MRP by Product Category",
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Sales by outlet size
    st.markdown("### 🏪 Sales by Outlet Size")
    
    size_sales = df.groupby('Outlet_Size')['Item_Outlet_Sales'].agg(['sum', 'mean', 'count'])
    fig_size = px.bar(
        x=size_sales.index,
        y=size_sales['mean'],
        title="Average Sales by Outlet Size",
        color_discrete_sequence=['#FF6B35']
    )
    st.plotly_chart(fig_size, use_container_width=True)

# Product Performance page
def product_performance_page():
    st.markdown("## 🔍 Product Performance Analysis")
    
    # Top products by sales
    st.markdown("### 🏆 Top Products by Sales")
    
    top_products = df.groupby('Item_Identifier')['Item_Outlet_Sales'].sum().sort_values(ascending=False).head(20)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            x=top_products.index,
            y=top_products.values,
            title="Top 20 Products by Total Sales",
            color_discrete_sequence=['#FF6B35']
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Top Products Summary")
        top_products_df = pd.DataFrame({
            'Product_ID': top_products.index,
            'Total_Sales': top_products.values
        })
        st.dataframe(top_products_df.head(10))
    
    # Product weight analysis
    st.markdown("### ⚖️ Product Weight Analysis")
    
    weight_analysis = df.groupby('Item_Type')['Item_Weight'].agg(['mean', 'median', 'std']).round(2)
    st.dataframe(weight_analysis)
    
    fig_weight = px.box(
        df,
        x='Item_Type',
        y='Item_Weight',
        title="Weight Distribution by Product Category",
        color_discrete_sequence=['#FF6B35']
    )
    fig_weight.update_xaxes(tickangle=45)
    st.plotly_chart(fig_weight, use_container_width=True)
    
    # Price per weight analysis
    st.markdown("### 💰 Price per Unit Weight Analysis")
    
    price_weight = df.groupby('Item_Type')['Price_per_Weight'].mean().sort_values(ascending=False)
    
    fig_price_weight = px.bar(
        x=price_weight.index,
        y=price_weight.values,
        title="Average Price per Unit Weight by Category",
        color_discrete_sequence=['#FF6B35']
    )
    fig_price_weight.update_xaxes(tickangle=45)
    st.plotly_chart(fig_price_weight, use_container_width=True)

# Outlet Analysis page
def outlet_analysis_page():
    st.markdown("## 🏪 Outlet Analysis")
    
    # Outlet performance overview
    st.markdown("### 📊 Outlet Performance Overview")
    
    outlet_summary = df.groupby('Outlet_Identifier').agg({
        'Item_Outlet_Sales': ['sum', 'mean', 'count'],
        'Item_MRP': 'mean',
        'Outlet_Age': 'first',
        'Outlet_Size': 'first',
        'Outlet_Location_Type': 'first',
        'Outlet_Type': 'first'
    }).round(2)
    
    outlet_summary.columns = ['Total_Sales', 'Avg_Sales', 'Item_Count', 'Avg_MRP', 'Outlet_Age', 'Outlet_Size', 'Location_Type', 'Outlet_Type']
    st.dataframe(outlet_summary.sort_values('Total_Sales', ascending=False))
    
    # Outlet type analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏬 Sales by Outlet Type")
        outlet_type_sales = df.groupby('Outlet_Type')['Item_Outlet_Sales'].sum()
        fig = px.pie(
            values=outlet_type_sales.values,
            names=outlet_type_sales.index,
            title="Sales Distribution by Outlet Type"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📍 Sales by Location Type")
        location_sales = df.groupby('Outlet_Location_Type')['Item_Outlet_Sales'].sum()
        fig = px.bar(
            x=location_sales.index,
            y=location_sales.values,
            title="Total Sales by Location Type",
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Outlet age vs performance
    st.markdown("### 📅 Outlet Age vs Performance")
    
    age_performance = df.groupby('Outlet_Identifier').agg({
        'Outlet_Age': 'first',
        'Item_Outlet_Sales': 'sum'
    }).reset_index()
    
    fig_age = px.scatter(
        age_performance,
        x='Outlet_Age',
        y='Item_Outlet_Sales',
        title="Outlet Age vs Total Sales",
        color='Outlet_Identifier',
        size='Item_Outlet_Sales'
    )
    st.plotly_chart(fig_age, use_container_width=True)

# Inventory Insights page
def inventory_insights_page():
    st.markdown("## 📦 Inventory Insights")
    
    # Item visibility analysis
    st.markdown("### 👁️ Item Visibility Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        visibility_sales = df.groupby('Item_Type')['Item_Visibility'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=visibility_sales.index,
            y=visibility_sales.values,
            title="Average Item Visibility by Category",
            color_discrete_sequence=['#FF6B35']
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Visibility vs Sales correlation
        fig_scatter = px.scatter(
            df,
            x='Item_Visibility',
            y='Item_Outlet_Sales',
            color='Item_Type',
            title="Visibility vs Sales",
            opacity=0.6
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Weight distribution
    st.markdown("### ⚖️ Weight Distribution Analysis")
    
    weight_stats = df.groupby('Item_Type')['Item_Weight'].describe().round(2)
    st.dataframe(weight_stats)
    
    # Fat content analysis
    st.markdown("### 🥩 Fat Content Analysis")
    
    fat_analysis = df.groupby(['Item_Type', 'Item_Fat_Content'])['Item_Outlet_Sales'].sum().unstack()
    fig_fat = px.imshow(
        fat_analysis.fillna(0),
        title="Sales by Product Type and Fat Content",
        color_continuous_scale="RdYlBu",
        aspect="auto"
    )
    st.plotly_chart(fig_fat, use_container_width=True)
    
    st.dataframe(fat_analysis.round(2).fillna(0))

# Supply Chain Metrics page
def supply_chain_metrics_page():
    st.markdown("## 🚚 Supply Chain Metrics")
    
    # MRP vs Sales correlation
    st.markdown("### 💰 MRP vs Sales Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation matrix
        numeric_cols = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Age', 'Item_Outlet_Sales']
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(
            corr_matrix,
            title="Correlation Matrix",
            color_continuous_scale="RdYlBu",
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Correlation Values")
        st.dataframe(corr_matrix.round(3))
    
    # Price sensitivity analysis
    st.markdown("### 📈 Price Sensitivity Analysis")
    
    # Create price buckets
    df['Price_Bucket'] = pd.cut(df['Item_MRP'], 
                               bins=[0, 50, 100, 150, 200, 250, float('inf')],
                               labels=['<50', '50-100', '100-150', '150-200', '200-250', '>250'])
    
    price_bucket_sales = df.groupby('Price_Bucket')['Item_Outlet_Sales'].agg(['sum', 'mean', 'count'])
    
    fig_price = px.bar(
        x=price_bucket_sales.index,
        y=price_bucket_sales['mean'],
        title="Average Sales by Price Bucket",
        color_discrete_sequence=['#FF6B35']
    )
    st.plotly_chart(fig_price, use_container_width=True)
    
    st.dataframe(price_bucket_sales.round(2))
    
    # Outlet efficiency metrics
    st.markdown("### 🏪 Outlet Efficiency Metrics")
    
    outlet_efficiency = df.groupby('Outlet_Identifier').agg({
        'Item_Outlet_Sales': 'sum',
        'Item_Identifier': 'count'
    })
    outlet_efficiency['Sales_per_Item'] = outlet_efficiency['Item_Outlet_Sales'] / outlet_efficiency['Item_Identifier']
    outlet_efficiency = outlet_efficiency.sort_values('Sales_per_Item', ascending=False)
    
    fig_efficiency = px.bar(
        x=outlet_efficiency.index[:10],
        y=outlet_efficiency['Sales_per_Item'][:10],
        title="Top 10 Outlets by Sales per Item",
        color_discrete_sequence=['#FF6B35']
    )
    fig_efficiency.update_xaxes(tickangle=45)
    st.plotly_chart(fig_efficiency, use_container_width=True)
    
    st.dataframe(outlet_efficiency.round(2).head(10))

# Predictive Analytics page
def predictive_analytics_page():
    st.markdown("## 🎯 Predictive Analytics")
    
    # Sales prediction features
    st.markdown("### 📊 Sales Prediction Analysis")
    
    # Feature correlation with sales
    numeric_cols = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Age']
    
    correlations = []
    for col in numeric_cols:
        corr = df[col].corr(df['Item_Outlet_Sales'])
        correlations.append({'Feature': col, 'Correlation': corr})
    
    corr_df = pd.DataFrame(correlations).sort_values('Correlation', key=abs, ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_corr = px.bar(
            corr_df,
            x='Feature',
            y='Correlation',
            title="Feature Correlation with Sales",
            color='Correlation',
            color_continuous_scale="RdYlBu"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.dataframe(corr_df)
    
    # Simple regression analysis
    st.markdown("### 📈 Sales vs MRP Regression")
    
    fig_regression = px.scatter(
        df,
        x='Item_MRP',
        y='Item_Outlet_Sales',
        title="Sales vs MRP with Trend Line",
        trendline="ols",
        color_discrete_sequence=['#FF6B35']
    )
    st.plotly_chart(fig_regression, use_container_width=True)
    
    # Category-wise sales patterns
    st.markdown("### 🛍️ Category-wise Sales Patterns")
    
    category_patterns = df.groupby('Item_Type')['Item_Outlet_Sales'].describe().round(2)
    st.dataframe(category_patterns)
    
    # Create box plots for top categories
    top_categories = df['Item_Type'].value_counts().head(5).index
    df_top = df[df['Item_Type'].isin(top_categories)]
    
    fig_box = px.box(
        df_top,
        x='Item_Type',
        y='Item_Outlet_Sales',
        title="Sales Distribution for Top 5 Categories",
        color_discrete_sequence=['#FF6B35']
    )
    fig_box.update_xaxes(tickangle=45)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Recommendations based on data
    st.markdown("### 💡 Data-Driven Recommendations")
    
    recommendations = []
    
    # Find best performing categories
    best_categories = df.groupby('Item_Type')['Item_Outlet_Sales'].mean().sort_values(ascending=False).head(3)
    recommendations.append(f"🏆 Focus on top-performing categories: {', '.join(best_categories.index)}")
    
    # Find optimal price range
    optimal_price = df.groupby(pd.cut(df['Item_MRP'], bins=5))['Item_Outlet_Sales'].mean().idxmax()
    recommendations.append(f"💰 Optimal price range: {optimal_price}")
    
    # Find best outlet type
    best_outlet = df.groupby('Outlet_Type')['Item_Outlet_Sales'].mean().sort_values(ascending=False).index[0]
    recommendations.append(f"🏪 Best performing outlet type: {best_outlet}")
    
    # Visibility impact
    high_visibility = df[df['Item_Visibility'] > df['Item_Visibility'].median()]['Item_Outlet_Sales'].mean()
    low_visibility = df[df['Item_Visibility'] <= df['Item_Visibility'].median()]['Item_Outlet_Sales'].mean()
    if high_visibility > low_visibility:
        recommendations.append("👁️ Increase item visibility to boost sales")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")

# Main navigation
if page == "📈 Overview":
    overview_page()
elif page == "📊 Sales Analysis":
    sales_analysis_page()
elif page == "🔍 Product Performance":
    product_performance_page()
elif page == "🏪 Outlet Analysis":
    outlet_analysis_page()
elif page == "📦 Inventory Insights":
    inventory_insights_page()
elif page == "🚚 Supply Chain Metrics":
    supply_chain_metrics_page()
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
