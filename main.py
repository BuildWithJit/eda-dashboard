import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

warnings.filterwarnings("ignore")

# Configure page settings
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for beautiful styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stAlert {
        border-radius: 10px;
    }
    
    .upload-section {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9ff;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    # Main header
    st.markdown('<h1 class="main-header">EDA Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">Upload your CSV file and get comprehensive data insights instantly</p>',
        unsafe_allow_html=True,
    )

    # File upload section
    st.markdown("## 📁 Data Upload")

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type=["csv"],
                help="Upload a CSV file to start your exploratory data analysis",
            )

    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)

            # Store in session state
            st.session_state["data"] = df
            st.session_state["uploaded"] = True

            # Show sidebar only when file is uploaded
            st.sidebar.title("🔧 Dashboard Controls")
            st.sidebar.markdown("---")

            # Success message
            st.success(
                f"✅ Successfully loaded **{uploaded_file.name}** with {len(df)} rows and {len(df.columns)} columns!"
            )

            # Display data overview
            display_data_overview(df)

        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("💡 Please ensure your file is a valid CSV format")


def display_data_overview(df):
    """Display comprehensive data overview"""

    st.markdown("---")
    st.markdown("## 📋 Data Overview")

    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("📏 Total Rows", f"{len(df):,}")
    with col2:
        st.metric("📊 Total Columns", len(df.columns))
    with col3:
        st.metric(
            "💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB"
        )
    with col4:
        missing_cells = df.isnull().sum().sum()
        st.metric("❌ Missing Values", f"{missing_cells:,}")
    with col5:
        duplicate_rows = df.duplicated().sum()
        st.metric("🔄 Duplicate Rows", f"{duplicate_rows:,}")

    # Tabbed interface for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🔍 Data Preview",
            "📊 Statistics",
            "🧹 Data Quality",
            "📋 Column Info",
            "🎯 Quick Insights",
        ]
    )

    with tab1:
        display_data_preview(df)

    with tab2:
        display_statistics(df)

    with tab3:
        display_data_quality(df)

    with tab4:
        display_column_info(df)

    with tab5:
        display_quick_insights(df)


def display_data_preview(df):
    """Display data preview with head and tail"""

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔝 First 10 Rows")
        st.dataframe(df.head(10), use_container_width=True)

    with col2:
        st.markdown("### 🔚 Last 10 Rows")
        st.dataframe(df.tail(10), use_container_width=True)

    # Show random sample
    st.markdown("### 🎲 Random Sample (5 rows)")
    st.dataframe(df.sample(min(5, len(df))), use_container_width=True)


def display_statistics(df):
    """Display statistical summary"""

    # Separate numerical and categorical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    if numerical_cols:
        st.markdown("### 📈 Numerical Columns Statistics")
        numerical_stats = df[numerical_cols].describe()
        st.dataframe(numerical_stats, use_container_width=True)

        # Additional statistics
        st.markdown("### 📊 Additional Numerical Insights")
        additional_stats = pd.DataFrame(
            {
                "Skewness": df[numerical_cols].skew(),
                "Kurtosis": df[numerical_cols].kurtosis(),
                "Median": df[numerical_cols].median(),
                "Mode": df[numerical_cols].mode().iloc[0]
                if len(df[numerical_cols].mode()) > 0
                else None,
            }
        )
        st.dataframe(additional_stats, use_container_width=True)

    if categorical_cols:
        st.markdown("### 📝 Categorical Columns Summary")
        categorical_summary = []

        for col in categorical_cols:
            categorical_summary.append(
                {
                    "Column": col,
                    "Unique Values": df[col].nunique(),
                    "Most Frequent": df[col].mode()[0]
                    if len(df[col].mode()) > 0
                    else "N/A",
                    "Most Frequent Count": df[col].value_counts().iloc[0]
                    if len(df[col].value_counts()) > 0
                    else 0,
                    "Most Frequent %": f"{(df[col].value_counts().iloc[0] / len(df) * 100):.1f}%"
                    if len(df[col].value_counts()) > 0
                    else "0%",
                }
            )

        categorical_df = pd.DataFrame(categorical_summary)
        st.dataframe(categorical_df, use_container_width=True)


def display_data_quality(df):
    """Display data quality assessment"""

    # Missing values analysis
    st.markdown("### ❌ Missing Values Analysis")

    missing_data = pd.DataFrame(
        {
            "Column": df.columns,
            "Missing Count": df.isnull().sum(),
            "Missing Percentage": (df.isnull().sum() / len(df) * 100).round(2),
            "Data Type": df.dtypes.astype(str),
        }
    )
    missing_data = missing_data[missing_data["Missing Count"] > 0].sort_values(
        "Missing Percentage", ascending=False
    )

    if len(missing_data) > 0:
        st.dataframe(missing_data, use_container_width=True)

        # Visualize missing values
        if len(missing_data) > 0:
            fig = px.bar(
                missing_data,
                x="Column",
                y="Missing Percentage",
                title="Missing Values by Column",
                color="Missing Percentage",
                color_continuous_scale="Reds",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("🎉 No missing values found in the dataset!")

    # Duplicate rows
    st.markdown("### 🔄 Duplicate Rows Analysis")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        st.warning(
            f"⚠️ Found {duplicates} duplicate rows ({duplicates / len(df) * 100:.1f}% of data)"
        )
        st.dataframe(df[df.duplicated()], use_container_width=True)
    else:
        st.success("✅ No duplicate rows found!")


def display_column_info(df):
    """Display detailed column information"""

    st.markdown("### 📋 Column Information")

    column_info = []
    for col in df.columns:
        column_info.append(
            {
                "Column Name": col,
                "Data Type": str(df[col].dtype),
                "Non-Null Count": df[col].count(),
                "Null Count": df[col].isnull().sum(),
                "Unique Values": df[col].nunique(),
                "Memory Usage (bytes)": df[col].memory_usage(deep=True),
            }
        )

    info_df = pd.DataFrame(column_info)
    st.dataframe(info_df, use_container_width=True)

    # Data types distribution
    st.markdown("### 📊 Data Types Distribution")
    dtype_counts = df.dtypes.value_counts()

    fig = px.pie(
        values=dtype_counts.values,
        names=dtype_counts.index,
        title="Distribution of Data Types",
    )
    st.plotly_chart(fig, use_container_width=True)


def display_quick_insights(df):
    """Display quick automated insights"""

    st.markdown("### 🎯 Quick Insights")

    insights = []

    # Dataset size insight
    if len(df) > 100000:
        insights.append(
            "📊 **Large Dataset**: This is a large dataset with over 100k rows. Consider sampling for initial exploration."
        )
    elif len(df) < 100:
        insights.append(
            "📊 **Small Dataset**: This is a small dataset with less than 100 rows. Statistical analyses may have limited power."
        )

    # Missing data insight
    missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_percentage > 20:
        insights.append(
            f"❌ **High Missing Data**: {missing_percentage:.1f}% of your data is missing. Consider data imputation strategies."
        )
    elif missing_percentage > 5:
        insights.append(
            f"⚠️ **Moderate Missing Data**: {missing_percentage:.1f}% of your data is missing. Review missing data patterns."
        )
    else:
        insights.append(
            "✅ **Clean Data**: Low missing data percentage. Good data quality!"
        )

    # Duplicates insight
    duplicate_percentage = (df.duplicated().sum() / len(df)) * 100
    if duplicate_percentage > 5:
        insights.append(
            f"**Duplicate Concern**: {duplicate_percentage:.1f}% duplicate rows found. Consider deduplication."
        )

    # Column types insight
    numerical_cols = len(df.select_dtypes(include=[np.number]).columns)
    categorical_cols = len(df.select_dtypes(include=["object"]).columns)

    if numerical_cols > categorical_cols * 2:
        insights.append(
            "**Numerical Heavy**: Dataset is primarily numerical. Great for statistical analysis and ML models."
        )
    elif categorical_cols > numerical_cols * 2:
        insights.append(
            "**Categorical Heavy**: Dataset is primarily categorical. Consider encoding strategies for ML."
        )
    else:
        insights.append(
            "⚖️ **Balanced Mix**: Good balance of numerical and categorical features."
        )

    # Memory usage insight
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    if memory_mb > 100:
        insights.append(
            f"**Memory Usage**: Dataset uses {memory_mb:.1f} MB. Consider data optimization for large-scale analysis."
        )

    # Display insights
    for insight in insights:
        st.markdown(f"- {insight}")

    if not insights:
        st.info(
            "No specific insights detected. Your data looks standard for exploratory analysis!"
        )


if __name__ == "__main__":
    main()
