import sys
import os
import re
from tqdm import tqdm

import logging

sys.path.append(os.path.abspath(".."))

import requests
from openai import OpenAI
from prompts.templates import get_prompt_template, PERSONA_PROMPTS

LOGGER = logging.Logger(__name__, level=logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(HANDLER)
HANDLER.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

class QwenLLM:
    def __init__(self, api_key: str, base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, prompt: str, system_prompt: str = 'Given a question, your task is to provide the correct answer based on the user\'s question and instructions. If there are multiple answers, separate them with a comma and be exhaustive. If there are no answers, type \"None\"') -> str | None:
        response = self.client.chat.completions.create(
            model="qwen3-8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            extra_body={"enable_thinking": False},
            # max_tokens=256,
            temperature=0.3,
            # top_p=0.1,
            # logprobs=True
        )
        reply = response.choices[0].message.content

        # self.messages.append({"role": "assistant", "content": reply})

        return reply

    def get_wikidata_idq(self, entity: str) -> str:
        item = str(entity).strip()

        if not item or item == "None":
            return ""

        try:
            # If item can be converted to an integer, return it directly
            return str(int(item))
        except ValueError:
            # If not, proceed with the Wikidata search
            try:
                url = (f"https://www.wikidata.org/w/api.php"
                       f"?action=wbsearchentities"
                       f"&search={item}"
                       f"&language=en"
                       f"&format=json")
                data = requests.get(url).json()
                # Return the first id (Could upgrade this in the future)
                return str(data["search"][0]["id"])
            except Exception as e:
                # logger.error(f"Error getting Wikidata ID for `{item}`: {e}")
                return item

    def get_predictions(self, inputs: list) -> list:
        prompts = [
            get_prompt_template(inp, PERSONA_PROMPTS) for inp in inputs
        ]

        outputs = []
        for prompt in prompts:
            response = self.chat(prompt)
            LOGGER.info(f"Response: {response}")
            outputs.append(response.strip()) # type: ignore

        results = []
        for inp, output in tqdm(zip(inputs, outputs)):
            LOGGER.info(f"Input: {inp}, Output: {output}")
            if inp["Relation"] in ["hasArea", "hasCapacity"]:
                object_entities = [output]
                wikidata_ids = [output]
            else:
                object_entities = output.split(", ")
                wikidata_ids = self.get_wikidata_idq(output)
            results.append({
                "SubjectEntityID": inp["SubjectEntityID"],
                "SubjectEntity": inp["SubjectEntity"],
                "Relation": inp["Relation"],
                "ObjectEntities": object_entities,
                "ObjectEntitiesID": wikidata_ids,
            })

        return results

