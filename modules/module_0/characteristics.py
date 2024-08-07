import random
from gpt2 import ExplorerLLM

EXPLORER_COUNT = 1

def get_characteristics():

    llm = ExplorerLLM()
    characteristics = []

    for i in range(EXPLORER_COUNT):
        print(f"\n\n######################### Explorer {i} #########################\n")
        # Randomly select a personality and complete the survey
        selected_personality = random.choice(list(llm.personalities.keys()))
        survey_responses = llm.complete_survey(selected_personality)

        # Analyze survey responses with the LLM
        characteristics.append(llm.analyze_responses(survey_responses, max_length=300))
        print("Extracted characteristics by LLM:", characteristics[i])

    return characteristics

if __name__ == "__main__":
    characteristics = get_characteristics()