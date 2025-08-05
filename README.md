# Meteorologia - Weather Data Analysis Project

A comprehensive data science project for analyzing weather patterns, precipitation data, and meteorological events using advanced geospatial analysis and machine learning techniques.

## 📋 Project Overview

This project analyzes meteorological data including:
- **Precipitation patterns** and rainfall intensity analysis
- **Geospatial mapping** of weather events using various mapping libraries
- **Temporal analysis** of weather patterns over time
- **Machine learning models** for weather prediction
- **Natural language processing** of weather event descriptions
- **Interactive visualizations** using Plotly and Matplotlib

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd meteorologia
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

5. **Download NLTK data** (for text analysis)
   ```python
   import nltk
   nltk.download('stopwords')
   ```

## 📁 Project Structure

```
meteorologia/
├── data/                          # Data files
│   └── raw/                       # Raw data files
│       └── adm_cor_comando/       # Administrative data
├── nbs/                          # Jupyter notebooks
│   ├── data-analysis/            # Main analysis notebooks
│   ├── data-cleaning/            # Data cleaning scripts
│   ├── data-exploration/         # Exploratory data analysis
│   │   ├── alertario/           # Alert system analysis
│   │   ├── charts/              # Chart generation
│   │   ├── maps/                # Mapping analysis
│   │   └── ocorrencias/         # Event analysis
│   ├── dataframe-agent/          # AI-powered data analysis
│   ├── download-tables/          # Data download scripts
│   └── modeling/                 # Machine learning models
├── markdown/                     # Documentation and reports
│   ├── imgs/                     # Generated images
│   └── *.md                      # Analysis reports
├── prompts/                      # AI prompt templates
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Google Cloud API
GENAI_API_KEY=your_google_generative_ai_key

# BigQuery (if using)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### API Keys Required

- **Google Generative AI**: For AI-powered data analysis
- **Google Cloud BigQuery**: For data retrieval (optional)

## 📊 Data Sources

The project works with various meteorological data sources:

- **Alertário System**: Precipitation and weather alert data
- **Administrative Data**: Geographic boundaries and administrative regions
- **Weather Station Data**: Historical weather measurements
- **Event Records**: Weather-related incidents and occurrences

## 🧪 Analysis Components

### 1. Data Exploration (`nbs/data-exploration/`)
- **Preliminary Analysis**: Initial data exploration and statistics
- **Spatial Analysis**: Geographic distribution of weather events
- **Temporal Analysis**: Time-based patterns and trends
- **Chart Generation**: Automated visualization creation

### 2. Data Cleaning (`nbs/data-cleaning/`)
- **Data Quality Checks**: Validation and cleaning procedures
- **Geographic Data Processing**: Shapefile and boundary processing
- **Data Transformation**: Format standardization and enrichment

### 3. Machine Learning (`nbs/modeling/`)
- **CNN Models**: Convolutional neural networks for weather prediction
- **Model Training**: Automated model training pipelines
- **Performance Evaluation**: Model assessment and validation

### 4. AI-Powered Analysis (`nbs/dataframe-agent/`)
- **Natural Language Queries**: Ask questions about your data in plain English
- **Automated Insights**: AI-generated data analysis and visualizations
- **Interactive Exploration**: Conversational data exploration

## 📈 Key Features

### Geospatial Analysis
- **Interactive Maps**: Multiple mapping libraries (Plotly, Matplotlib, Cartopy)
- **Spatial Interpolation**: Kriging and other interpolation methods
- **Geographic Boundaries**: Administrative region analysis

### Visualization
- **Time Series**: Temporal pattern analysis
- **Heatmaps**: Spatial and temporal heatmaps
- **Word Clouds**: Text analysis of weather descriptions
- **Interactive Charts**: Plotly-based interactive visualizations

### Machine Learning
- **Weather Prediction**: CNN models for precipitation forecasting
- **Pattern Recognition**: Automated detection of weather patterns
- **Classification**: Event type classification

## 🚨 Important Notes

### Large Files
Some notebooks contain embedded outputs and may be large. Consider:
- Running notebooks to regenerate outputs
- Using `.ipynb_checkpoints` in `.gitignore`
- Clearing outputs before committing

### API Usage
- Monitor API usage for Google Generative AI
- Implement rate limiting for large datasets
- Cache results when possible

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Usage Examples

### Basic Data Analysis
```python
import pandas as pd
import geopandas as gpd

# Load data
df = pd.read_csv('data/raw/your_data.csv')

# Basic exploration
print(df.head())
print(df.describe())
```

### Geospatial Analysis
```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load geographic data
gdf = gpd.read_file('data/raw/shapefile.shp')

# Create map
fig, ax = plt.subplots(1, 1)
gdf.plot(ax=ax)
plt.show()
```

### AI-Powered Analysis
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Create AI agent
llm = ChatGoogleGenerativeAI(model="gemini-pro")
agent = create_pandas_dataframe_agent(llm, df, verbose=True)

# Ask questions
response = agent.run("What are the main weather patterns in this data?")
```

## 📚 Dependencies

See `requirements.txt` for a complete list of dependencies. Key libraries include:

- **Data Science**: pandas, numpy, scipy
- **Visualization**: matplotlib, seaborn, plotly
- **Geospatial**: geopandas, shapely, cartopy
- **Machine Learning**: scikit-learn, tensorflow
- **AI/LLM**: langchain, google-generativeai

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Weather data providers
- Open-source geospatial libraries
- Google Cloud Platform for AI services

## 📞 Support

For questions or issues:
1. Check the documentation in the `markdown/` folder
2. Review the Jupyter notebooks for examples
3. Open an issue on GitHub

---

**Note**: This project is for research and educational purposes. Always verify data sources and validate results for production use. 