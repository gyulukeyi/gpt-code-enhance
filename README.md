# gpt-code-enhancer 

A simple enhancer for a code base with GPT.

## Setup 

```sh 
python -m venv .venv 
source .venv/bin/activate 
pip install -r requirements.txt
```

You will additionally need a valid OpenAI API key to make API calls. 
To enroll your key, either:
- set the key to your system's `OPENAI_API_KEY` environmental variable 
- make a file name `.env` in `src/gpt_code_enhance/` and add a line:
    - `OPENAI_API_KEY=<YOUR_API_KEY>`

## Use

See `python app.py --help`
