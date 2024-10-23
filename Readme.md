# Data Visualization Assistant

A Streamlit application that combines data visualization with AI-powered plot suggestions using the FLAN-T5 model.

## Features
- CSV file upload and analysis
- AI-generated plot suggestions
- Interactive plot creation
- Multiple visualization types
- Containerized deployment

## Prerequisites
- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone 
cd 
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
Open your browser and navigate to `http://localhost:8501`

## Project Structure
- `app/`: Contains the main application code
  - `main.py`: Streamlit application entry point
  - `graph_analyzer.py`: Graph analysis and plotting logic
  - `requirements.txt`: Python dependencies
- `data/`: Directory for data files (mounted as a volume)
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Container orchestration

## Usage
1. Upload a CSV file using the file uploader
2. Review the data overview
3. Check AI-generated plot suggestions
4. Select plot type and parameters
5. Generate and interact with the visualization

## Development
To modify the application:
1. Update the code in the `app/` directory
2. Rebuild the container: `docker-compose up --build`

## Notes
- The application uses FLAN-T5-small model for plot suggestions
- Data persistence is handled through the mounted volume in `data/`
- The container is configured with memory limits for stability