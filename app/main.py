import streamlit as st
from graph_analyzer import GraphAnalyzer
import pandas as pd
from io import StringIO

def main():
    st.set_page_config(page_title="Data Visualization Assistant", layout="wide")
    st.title("📊 Interactive Data Visualization Assistant")
    
    # Initialize the graph analyzer
    analyzer = GraphAnalyzer()
    
    # File upload
    st.header("1. Upload Your Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Display basic data info
            st.header("2. Data Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.write("First few rows of your data:")
                st.dataframe(df.head())
            with col2:
                st.write("Data Info:")
                buffer = StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())
            
            # Generate and display plot suggestions
            st.header("3. AI-Generated Plot Suggestions")
            suggestions = analyzer.generate_plot_suggestions(df)
            for i, suggestion in enumerate(suggestions, 1):
                st.write(f"{i}. {suggestion}")
            
            # Plot creation interface
            st.header("4. Create Your Plot")
            
            # Plot type selection
            plot_type = st.selectbox(
                "Select plot type:",
                ["Histogram", "Scatter Plot", "Box Plot", "Bar Plot", "Line Plot"]
            )
            
            # Column selection based on plot type
            cols = df.columns.tolist()
            x_col = st.selectbox("Select X-axis column:", cols)
            
            if plot_type != "Histogram":
                y_col = st.selectbox("Select Y-axis column:", cols)
                color_col = st.selectbox("Select color column (optional):", ["None"] + cols)
                color_col = None if color_col == "None" else color_col
            else:
                y_col = None
                color_col = None
            
            # Create and display plot
            if st.button("Generate Plot"):
                fig = analyzer.create_plot(df, plot_type, x_col, y_col, color_col)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()