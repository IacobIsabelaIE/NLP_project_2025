PROMPT_TEMPLATES = {
    "hasArea": (
        "What is the area of {subject_entity} in square kilometers? Answer only with a number (e.g., 1234.56), no units.\n\n"
        "Q: What is the area of Lošinj in square kilometers?\n"
        "A: 74.36\n\n"
        "Q: What is the area of Ilha da Queimada Grande in square kilometers?\n"
        "A: 0.43\n\n"
        "Q: What is the area of Estonia in square kilometers?\n"
        "A: 45335\n\n"
        "Q: What is the area of {subject_entity} in square kilometers?\n"
        "A:"
    ),
    "hasCapacity": (
        "You are a Stadium Records Analyst. Provide only the seating capacity of the venue as a number (no words, no commentary).\n\n"
        "Q: What is the seating capacity of Q10276978 in Pernambuco?\n"
        "A: 5000\n\n"
        "Q: What is the seating capacity of University Stadium in Georgia?\n"
        "A: 9500\n\n"
        "Q: What is the seating capacity of Bakhshi Stadium in Srinagar?\n"
        "A: 30000\n\n"
        "Q: What is the seating capacity of {subject_entity}?\n"
        "A:"
    ),
    "awardWonBy": (
        "You are an Awards Archivist. Provide a comma-separated list of people or entities who have been awarded the {subject_entity}. Respond only with names.\n\n"
        "Q: Who has been awarded the Sakharov Prize?\n"
        "A: Alexei Yurchak, Vladimir Bukovsky, Andrei Sakharov\n\n"
        "Q: Who has been awarded the Nobel Peace Prize?\n"
        "A: Martin Luther King Jr., Malala Yousafzai, Nelson Mandela\n\n"
        "Q: Who has been awarded the Turing Award?\n"
        "A: Alan Turing, John Backus, Ada Lovelace\n\n"
        "Q: Who has been awarded the {subject_entity}?\n"
        "A:"
    ),
    "companyTradesAtStockExchange": (
        "You are a stock analyst. Provide a comma-separated list of stock exchanges where the company is listed. "
        "If there are no answers to this question (e.g., the company is not listed anywhere), reply only with the string '[]'. "
        "If you don't know the answer or if the entity doesn't exist, reply with 'I don't know'.\n\n"
        "Q: On which stock exchange is Bharti Airtel listed?\n"
        "A: Bombay Stock Exchange\n\n"
        "Q: On which stock exchange is RPS Group listed?\n"
        "A: London Stock Exchange\n\n"
        "Q: On which stock exchange is United Wire Factories Co. listed?\n"
        "A: Saudi Stock Exchange\n\n"
        "Q: On which stock exchange is {subject_entity} listed?\n"
        "A:"
    ),

    "countryLandBordersCountry": (
        "You are a geopolitical analyst. List all countries sharing a direct land border with {subject_entity}, separated by commas. If there are no answers to this question, like there is no country near the entity mentioned, reply only with the string '[]'. Nothing else should be generated.  If you don't know the answer, or if the entity doesn't exist, reply with 'I don't know'.\n\n"
        "Q: Which countries share a land border with Ethiopia?\n"
        "A: Djibouti, Eritrea, Kenya, Somalia, South Sudan, Sudan\n\n"
        "Q: Which countries share a land border with Russia?\n"
        "A: Azerbaijan, Belarus, China, Estonia, Finland, Georgia, Kazakhstan, North Korea, Latvia, Lithuania, Mongolia, Norway, Poland, Ukraine\n\n"
        "Q: Which countries share a land border with Bangladesh?\n"
        "A: India, Myanmar\n\n"
        "Q: Which countries share a land border with {subject_entity}?\n"
        "A:"
    ),
    "personHasCityOfDeath": (
        "You are a biographical archivist. Provide only the city where {subject_entity} died. If the person is alive, reply only with the string '[]'. Nothing else should be generated. If you don't know the answer, or if the entity doesn't exist, reply with 'I don't know'.\n\n"
        "Q: In which city did Nerses Bedros XIX Tarmouni die?\n"
        "A: Beirut\n\n"
        "Q: In which city did Juan Luis Galiardo die?\n"
        "A: Madrid\n\n"
        "Q: In which city did John Hurt die?\n"
        "A: Norfolk\n\n"
        "Q: In which city did {subject_entity} die?\n"
        "A:"
    )
}


def get_prompt_template(entry: dict) -> str:
    relation = entry["Relation"]
    subject = entry["SubjectEntity"]
    template = PROMPT_TEMPLATES.get(relation)

    if not template:
        raise ValueError(f"No prompt template defined for relation '{relation}'")

    return template.format(subject_entity=subject)