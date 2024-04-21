# LLManager

Manager that lets you use with ease the biggest LLMs.
Available integrations as of 21/04/2022:
- OpenAI
---------------------------------------------------------------

#### Setup

Install the required packages:
```bash
pip install -r requirements.txt
```

Then copy the .env file:
```bash
cp .env.example .env
```
and put your api_key in the dedicated environment variable in the .env file

Then add the useful attributes (e.g. model) in the dedicated *json file* in the [llms folder](src/llmanager/llms/).

```bash
cd src/llmanager/
python main.py --provider=<PROVIDER> # can be one of [openai] 
```


#### Changelog

- [x] LLM base class interaction
- [X] Integration with OpenAI
- [ ] Integration with Gemini
- [ ] Integration with Anthropic
- [ ] Integration with HuggingFace models