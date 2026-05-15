# 🛒 Blinkit Supply Chain Analytics Dashboard

A comprehensive data science project for analyzing and optimizing the Blinkit food and groceries supply chain using Streamlit.

## 📋 Features

### 📊 Data Upload & Exploration
- Support for CSV and Excel file uploads
- Automatic data type detection and validation
- Missing value analysis
- Column summary statistics

### 📈 Supply Chain Overview
- Key Performance Indicators (KPIs)
- Data quality metrics
- Interactive visualizations
- Correlation analysis

### 🔍 Demand Forecasting
- Time series analysis
- Moving average calculations
- Demand trend visualization
- Seasonal pattern detection

### 📦 Inventory Analysis
- Stock level monitoring
- Product-wise inventory summary
- Inventory distribution analysis
- Reorder point calculations

### 🚚 Delivery Optimization
- Delivery performance metrics
- Route efficiency analysis
- Time-based delivery patterns
- Geographic distribution

### 📈 Performance Metrics
- Multi-metric correlation analysis
- Performance trend monitoring
- Statistical summaries
- Comparative analysis

### 🎯 Predictive Analytics
- Feature correlation analysis
- Simple regression modeling
- Feature importance ranking
- Target variable prediction

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd blinkit-supply-chain-analytics
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
blinkit-supply-chain-analytics/
├── app.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md             # Project documentation
└── data/                 # Data directory (create as needed)
    └── sample_data.csv   # Sample dataset (optional)
```

## 📊 Data Requirements

The dashboard is designed to work with various supply chain datasets. It automatically detects and analyzes:

### Expected Columns:
- **Order Information**: order_id, order_date, order_amount
- **Product Details**: product_id, product_name, category, price
- **Inventory Data**: stock_level, quantity, warehouse_id
- **Delivery Information**: delivery_time, delivery_address, delivery_status
- **Customer Data**: customer_id, customer_location
- **Supplier Information**: supplier_id, lead_time, reliability

### Supported File Formats:
- CSV files (.csv)
- Excel files (.xlsx, .xls)

## 🎨 Dashboard Components

### Navigation Sidebar
- Easy switching between different analysis modules
- Intuitive icon-based navigation
- Responsive design

### Interactive Visualizations
- **Plotly Charts**: Interactive plots with zoom, pan, and hover
- **Correlation Heatmaps**: Variable relationship analysis
- **Time Series Plots**: Trend analysis over time
- **Distribution Charts**: Statistical distributions

### Real-time Metrics
- Dynamic KPI cards
- Auto-updating statistics
- Data quality indicators

## 🔧 Customization

### Adding New Analysis Modules
1. Create a new function in `app.py`
2. Add the module to the sidebar navigation
3. Implement the analysis logic
4. Add appropriate visualizations

### Styling
- Custom CSS in the app.py file
- Color scheme: Orange (#FF6B35) and Blue (#004E89)
- Responsive design for mobile devices

## 📈 Advanced Features

### Machine Learning Integration
The dashboard is ready for advanced ML integration:
- Demand forecasting models
- Inventory optimization algorithms
- Route optimization
- Predictive maintenance

### Database Integration
Can be extended to connect with:
- PostgreSQL
- MySQL
- MongoDB
- Redis for caching

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Seaborn**: Statistical data visualization
- **Matplotlib**: Plotting library
- **Scikit-learn**: Machine learning (ready for integration)

## 📝 Usage Instructions

1. **Upload Data**: Start by uploading your dataset in the "Data Upload & Exploration" section
2. **Explore Overview**: Get a quick summary of your supply chain data
3. **Analyze Demand**: Use the demand forecasting module to understand patterns
4. **Monitor Inventory**: Check inventory levels and optimize stock
5. **Optimize Delivery**: Analyze delivery performance and identify bottlenecks
6. **Track Performance**: Monitor KPIs and performance metrics
7. **Predict Outcomes**: Use predictive analytics for forecasting

## 🎯 Key Benefits

- **Real-time Insights**: Instant data analysis and visualization
- **User-friendly Interface**: No coding knowledge required
- **Comprehensive Analysis**: Covers all major supply chain aspects
- **Scalable**: Can handle large datasets efficiently
- **Customizable**: Easy to modify and extend

## 📞 Support

For any issues or questions:
1. Check the data format requirements
2. Ensure all dependencies are installed
3. Verify your dataset contains the required columns
4. Check the Streamlit console for error messages

## 🚀 Future Enhancements

- Real-time data streaming
- Advanced ML models integration
- Geographic mapping with Folium
- Automated report generation
- Email notifications for alerts
- Multi-user support with authentication

