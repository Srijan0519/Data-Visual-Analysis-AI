import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

class GraphAnalyzer:
    def __init__(self):
        """
        Initialize the GraphAnalyzer with a pre-trained model for generating plot suggestions.
        Using FLAN-T5-small for its efficiency and good performance on structured tasks.
        """
        self.model_name = "google/flan-t5-small"
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            
            # Initialize the pipeline
            self.generator = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=100,
                device="cuda" if torch.cuda.is_available() else "cpu"
            )
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            st.error(f"Error loading model: {str(e)}")
            
    def generate_plot_suggestions(self, df):
        """Generate plot suggestions based on the dataframe structure."""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            prompt = f"""Given a dataset with:
            Numeric columns: {', '.join(numeric_cols)}
            Categorical columns: {', '.join(categorical_cols)}
            Suggest 3 different types of plots."""
            
            response = self.generator(prompt, max_length=100)[0]['generated_text']
            suggestions = response.split('\n')
            return [s for s in suggestions if s.strip()]
            
        except Exception as e:
            st.error(f"Error generating plot suggestions: {str(e)}")
            return []

    def create_plot(self, df, plot_type, x_col, y_col=None, color_col=None):
        """Create various types of plots based on user selection."""
        try:
            if plot_type == "Histogram":
                fig = px.histogram(df, x=x_col)
            elif plot_type == "Scatter Plot":
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
            elif plot_type == "Box Plot":
                fig = px.box(df, x=x_col, y=y_col)
            elif plot_type == "Bar Plot":
                fig = px.bar(df, x=x_col, y=y_col)
            elif plot_type == "Line Plot":
                fig = px.line(df, x=x_col, y=y_col)
            else:
                raise ValueError(f"Unsupported plot type: {plot_type}")
            
            return fig
        except Exception as e:
            st.error(f"Error creating plot: {str(e)}")
            return None

# Streamlit app code
def main():
    st.title("Graph Analyzer")
    
    # Initialize the analyzer
    analyzer = GraphAnalyzer()
    
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())
        
        # Get plot suggestions
        suggestions = analyzer.generate_plot_suggestions(df)
        
        # Plot selection
        plot_type = st.selectbox(
            "Select plot type",
            ["Histogram", "Scatter Plot", "Box Plot", "Bar Plot", "Line Plot"]
        )
        
        # Column selection based on plot type
        x_col = st.selectbox("Select X column", df.columns)
        
        y_col = None
        color_col = None
        if plot_type != "Histogram":
            y_col = st.selectbox("Select Y column", df.columns)
            color_col = st.selectbox("Select color column (optional)", ["None"] + list(df.columns))
        
        if st.button("Generate Plot"):
            fig = analyzer.create_plot(
                df, 
                plot_type, 
                x_col, 
                y_col,
                None if color_col == "None" else color_col
            )
            if fig:
                st.plotly_chart(fig)

if __name__ == "__main__":
    main()