import sys
import os
from tqdm import tqdm

import logging

sys.path.append(os.path.abspath(".."))

import requests
from openai import OpenAI
from prompts.templates import get_prompt_template

LOGGER = logging.Logger(__name__, level=logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(HANDLER)
HANDLER.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

class QwenLLM:
    def __init__(self, api_key: str, base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, prompt: str, system_prompt:  str = (
    "You are a highly precise factual knowledge extractor. For every query, you will first reason internally "
    "to ensure accuracy, and then provide only the requested factual entity. "
    "If there are multiple answers, separate them with a comma. "
    "If there are no answers to the question, provide an empty string. Don't write anything else. Just answer with thr string '[]'"
    "If you don't know the answer, or if the entity doesn't exist, just say 'I don't know'")) -> str | None:
        response = self.client.chat.completions.create(
            model="qwen3-8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            extra_body={"enable_thinking": False},
            max_tokens=256,
            temperature=0,
            # top_p=0.1,
            # logprobs=True
        )
        reply = response.choices[0].message.content

        # self.messages.append({"role": "assistant", "content": reply})

        return reply

    # def reset(self):
    #     self.messages = [{"role": "system", "content": "You are a helpful assistant. Do not use markdown or special characters. Your answer should contain only the answer, without any additional text. Write all numbers without commas for thousands (e.g., 1234 not 1,234), and always use a dot (`.`) as the decimal separator (e.g., 1234.56 not 1234,56)."}]
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
            get_prompt_template(inp) for inp in inputs
        ]

        outputs = []
        for prompt in prompts:
            response = self.chat(prompt)
            LOGGER.info(f"Response: {response}")
            outputs.append(response.strip())

        results = []
        for inp, output in tqdm(zip(inputs, outputs)):
            LOGGER.info(f"Input: {inp}, Output: {output}")
            
            # Handle specific relation types
            if inp["Relation"] in ["hasArea", "hasCapacity"]:
                # For numerical answers (e.g., area, capacity), keep as single string
                object_entities = output
                wikidata_ids = output
            else:
                # For other relations, process the output
                if output.strip() == "None":
                    object_entities = []
                    wikidata_ids = ""
                else:
                    # Split into list of entities
                    object_entities = output.split(", ")
                    # Get Wikidata IDs for each entity
                    wikidata_ids = self.get_wikidata_idq(output)
            
            results.append({
                "SubjectEntityID": inp["SubjectEntityID"],
                "SubjectEntity": inp["SubjectEntity"],
                "Relation": inp["Relation"],
                "ObjectEntities": object_entities,
                "ObjectEntitiesID": wikidata_ids,
            })

        return results


