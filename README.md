## Installation

### Prerequisites
- Python 3.9 or higher
- pip (comes with Python)

### Setup

**Windows:**
```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

**Mac/Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration
```
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Start Server



```
python -m src.main
```
or
```
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```