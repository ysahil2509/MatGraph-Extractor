@echo off
REM Startup script for MatGraph Extractor (Windows)

echo =======================================================================
echo    🔬 MatGraph Extractor: AI-Driven Material Knowledge Mining
echo =======================================================================

echo [1/3] Processing 10 scientific XML papers and updating SQLite database...
python scripts\process_papers.py

echo [2/3] Training Random Forest property prediction models...
python models\train_property_predictor.py

echo [3/3] Launching interactive Streamlit application...
streamlit run app\streamlit_app.py
pause
