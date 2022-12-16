# Cars price prediction (data from drom.ru)

## Requirements

Tested on Windows 11. This project contains .bat scripts for running on Windows

- Windows
- Python 3.10
- `pip install -r requirements.txt`

## Parsing

The hardest thing

Use scripts in parser dir:

1. prefetch.py
2. prefetch_concat.py --input ./prefetch_cars
3. parse_multiple.bat
4. normalize.bat

## Model training

```
cd model
start.bat
```

## Usage

```
cd front
python -m streamlit run MainPage.py
```

Navigate to webpage and use the model.