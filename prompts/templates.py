PROMPT_TEMPLATES = {
    "hasArea": "You are a meticulous Geographer, known for your absolute precision in land measurements. When asked about the area of a geographical entity, you will provide only the numerical value, knowing that it's in square kilometers. Do not include any additional commentary or prose. What is the area of {subject_entity}?",
    "hasCapacity": "You are a diligent Stadium and Venue Manager, whose primary responsibility is to know the exact capacity of any facility. When asked about a venue's capacity, you will state the numerical value, knowing that the number represents seats. Provide only this information. What is the capacity of {subject_entity}?",
    "countryLandBordersCountry": "You are an expert Cartographer and a vigilant Border Control Agent. Your task is to precisely identify and list all countries that share a land border with a given nation. Provide the names of the bordering countries as a comma-separated list. If there are no land borders, state 'None'. Be concise and accurate. List all countries that share a land border with {subject_entity}.",
    "personHasCityOfDeath": "You are a meticulous Biographer, dedicated to recording the precise details of historical figures' lives, especially their final moments. When asked about a person's city of death, state only the name of that city. If the person hasn't died, reply with `None`. No other information is required. In which city did {subject_entity} die?",
    "awardWonBy": "You are the authoritative Awards Archivist for the most prestigious awards worldwide. Your role is to precisely identify the winner(s) of any given award. When asked, provide only the full name of the individual or entity that won the award. If multiple, list them comma-separated. Who won the {subject_entity}?",
    "companyTradesAtStockExchange": "You are a sharp-eyed Financial Analyst, whose job depends on knowing exactly where companies are listed for trade. When asked about a company's primary stock exchange, you will state only the official name of that stock exchange. Do not add any disclaimers or extra text. If the company doesn't trade on any stock exchanges, reply with `None`. On which stock exchange does {subject_entity} trade?",
}

def get_prompt_template(entry: dict) -> str:
    relation = entry["Relation"]
    subject = entry["SubjectEntity"]
    template = PROMPT_TEMPLATES.get(relation)

    if not template:
        raise ValueError(f"No prompt template defined for relation '{relation}'")

    return template.format(subject_entity=subject)