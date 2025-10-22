# setup.py
from setuptools import setup, find_packages

setup(
    name="ufc-analytics",
    version="1.0.0",
    description="UFC Data Analysis Dashboard with Machine Learning",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "scikit-learn>=1.3.0",
        "xgboost>=1.7.0",
        "joblib>=1.2.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "tqdm>=4.65.0",
    ],
    python_requires=">=3.8",
)