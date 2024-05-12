# LLManager

Manager that lets you use with ease the biggest LLMs.
- [OpenAI](https://platform.openai.com/docs/api-reference)
- [Anthropic](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Google Gemini](https://ai.google.dev/gemini-api/docs/get-started/python?hl=en)
- [Ollama](https://ollama.com/library) supported models (LLama, Mistral, Phi, LLava, DBRX, Orca, Vicuna)

---------------------------------------------------------------

#### Setup

Clone the repo and move to the root directory `llmanager`
Then install the required packages with:
```bash
pip install -r requirements.txt
```

Then copy the .env file:
```bash
cp .env.example .env
```
and put your *api_key* (if required) in the dedicated environment variable in the [.env](.env). file

Move to the root directory:
```bash
cd src/llmanager/
```

#### LLM Config

In the [llms folder](src/llmanager/llms/configs/) there is a single config file for each provider.
Add the useful attributes (e.g. *model*, *stream, *json_mode*) in the dedicated **json file**.

#### Run

Run the desired LLM with:
```bash
python main.py --provider=<PROVIDER> # can be one of [openai, google, anthropic, ollama]
```

Otherwise, build your custom pipeline inside the [src folder](src/llmanager/) with:

```python
from llm import LLM
from provider import Provider
from llm_config import LLMConfig

llm = LLM(
    config = LLMConfig(
        provider=Provider.ANTHROPIC,
        model="claude-3-opus-20240229",
        stream=True,
        #json_mode=False,
        #temperature=1.0,
    )
)
#llm.list_models()
llm.chat_loop()
```

#### Changelog

- [x] LLM base class interaction
- [X] Integration with OpenAI
- [X] Integration with Anthropic
- [X] Integration with Gemini
- [x] Integration with LLama
- [X] Integration with Mistral
- [X] Integration with Mixtral
- [X] Integration with DBRX
- [X] Integration with Orca
- [X] Integration with Vicuna
- [X] Integration with Phi
- [X] Integration with LLava


#### TODO:

- [X] Allow for listing available models for each provider
- [X] Allow for streaming
- [ ] Allow for more choices (n)
- [ ] Allow for multi-modality
