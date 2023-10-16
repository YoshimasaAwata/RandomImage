if not exist venv\ (
  python -m venv venv
)

call .\venv\Scripts\activate.bat & pip install -r requirements.txt & python .\scripts\random_image.py
