from openai import OpenAI

class FakeLLM:
    def __init__(self, base_url, api_key, model_identifier):
        pass

    def withpromttext(self, prompt):
        return "fakeanswer"

class LLM:
    def __init__(self, base_url, api_key, model_identifier):
        self.client = OpenAI(
          base_url=base_url,
          api_key=api_key,
        )
        self.model_identifier = model_identifier

    def withpromttext(self, prompt):
        completion = self.client.chat.completions.create(
        model=self.model_identifier,
        temperature=0,
        messages=[
            {
              "role": "user",
              "content": f"{prompt}"
            }
          ]
        )
        return completion.choices[0].message.content

    def withpromptfile(self, promptfile):
        with open(promptfile) as f:
            prompt=f.read()
        return withpromttext(prompt)