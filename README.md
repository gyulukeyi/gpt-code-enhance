# gpt-code-enhance

A simple enhancer for enhancing a code base with GPT.

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

## What it does 

Code writing with LLM is getting popular. However, it can sometimes 
cause headaches when the writing process is done on code-to-code basis. 
Motivated by an [article by withmantle](https://blog.withmantle.com/code-conversion-using-ai/), 
here is a very simple implementation of codebase-conditioned code enhancer.

### Codebase mode 

By default, the `app.py` will run in "codebase mode". In this mode, each 
enhancing is done by:

1. gather all source codes under the project root 
2. make a single markdown representation of the source codes 
3. call GPT to improve a single source code 
4. get enhanced code. 
    - If a code is longer than output token limit (4096), try calling further for entire code 

The key is that when more than two files are being enhanced, the _entire_ 
steps from 1 to 4 are repeated. This way, GPT will get the fresh context 
whenever the API call is made. 

#### But isn't it expensive?

OpenAI puts lower rates for input tokens. With this script, you are making 
calls with very long input, with relatively short output. So using this is 
often cheaper than you think. For example, enhancing this package itself 
costs less than 0.01 USD with GPT-4o-mini.

But if price is your concern, change the `LARGET_TOKEN_WARNING_THRESHOLD` 
value in `src/gpt_code_enhance/__init__.py`. The call pipe then will warn 
your when the context token length is larger than the set value. If warning 
is sent, the app will ask for your confirmation to make actual API calls.

#### I want to use other model 

The default model is `gpt-4o-mini`. Feel free to change the `MODEL` variable in 
`src/gpt_code_enhance/__init__.py`. You could also define your own `caller` for 
custom chatbots. 

#### My codebase is large 

OpenAI's recent models allows 128K context length. This means OpenAI models can 
handle inputs of up to 128K tokens. When your context is beyond this, the app will 
warn you first. If the context length is indeed beyond OpenAI's limit, the API call 
will send back the error accordingly. If so, you should look for chatbots with longer 
context window, like Gemini. 

Otherwise, consider enhancing your code portion by portion. By passing a sub-package as 
a project root, you can reduce your context length while still offering contexts GPT can 
refer to when generating codes.

If your codebase is large, but within the context limit, and irritated with length warning, 
increase the value of `LARGET_TOKEN_WARNING_THRESHOLD` in `src/gpt_code_enhance/__init__.py`.

### Single code mode 

The app also supports enhancing single code -- at least for Python and TypeScript (more to come). 
Here, to improve the enhance performance, few steps are taken:

1. GPT is asked to explain the code
2. GPT's explanation is added to the input 
3. With GPT's explanation, GPT is then called to enhance the code 

This understand-enhance loop worked better for me, particularly when the code 
includes some complex logics.

You can use single code mode by passing `-s` argument, e.g., `python app.py -s -i mycode.py` 

## Intended use 

This code works best in CLI environment in a git directory. 
For instance, set an alias in your `.bashrc` will give you are handy shortcut 
to enhance your code. 

Since GPT can always fail, be sure to save a copy (or commit your changes) **before** 
letting GPT to "enhance" your code. If it is a git directory, a gitdiff tool is 
excellent for reviewing the changes.

Work little to big. Do not "enhance" entire code at once. Rather, enhance a small module, 
review, make edits, and move on to the other small module. Small bug in a utility function 
is far more manageable than the entire system crashes.

For this reason, in codebase mode, codes to enhance are searched non-recursively.  
