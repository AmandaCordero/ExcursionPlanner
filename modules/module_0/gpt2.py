from transformers import GPT2LMHeadModel, GPT2Tokenizer

class ExplorerLLM:
    def __init__(self, model_name="gpt2-medium"):
        # Load the model and tokenizer
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        
        # Define personalities
        self.personalities = {
            "Adventurous Explorer": "I love adventures and extreme challenges. I always seek to explore the unknown and push my limits.",
            "Nature Lover": "I enjoy connecting with nature. I prefer the tranquility of forests and observing wildlife in their natural habitat.",
            "Artistic Photographer": "I seek to capture the beauty of nature through my lens. I am always on the lookout for unique landscapes and fleeting moments.",
            "Family Explorer": "I like to share outdoor experiences with my family, prioritizing safety and group fun.",
            "Competitive Athlete": "I appreciate intense physical activities and sports challenges during my hikes. I always strive to improve my skills.",
            "Curious Historian": "I am interested in discovering the history and culture of the places I visit. I am fascinated by historical sites and local stories.",
            "Birdwatcher": "I am passionate about ornithology and enjoy observing and documenting various bird species in their natural habitats.",
            "Solitary Minimalist": "I prefer solo hikes, enjoying the silence and simplicity of nature. Less is more in my world.",
            "Water Enthusiast": "I love being near rivers, lakes, and beaches. I enjoy aquatic activities and the serenity that water offers.",
            "Botanical Enthusiast": "I have a great interest in the flora of the regions I visit. I love learning about plants and their unique properties.",
        }

    def generate_response(self, prompt, max_length=150):
        # Tokenize input and generate response
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def complete_survey(self, personality):
        description = self.personalities[personality]
        print(f"### Personality: {personality}")
        print(f"Description: {description}\n")

        # Survey questions with personalized prompts
        questions = [
            "1. What is your full name?",
            "2. How old are you?",
            "3. What is your gender?",
            "4. How often do you participate in hiking activities?",
            "5. How many people usually accompany you on your hikes?",
            "6. What do you consider your level of experience in hiking?",
            "7. Have you participated in activities such as hiking, climbing, mountain biking, kayaking, camping, or bird watching?",
            "8. Do you have experience navigating by GPS or maps?",
            "9. Have you received any first aid training?",
            "10. What type of landscape do you prefer for your hikes?",
            "11. What is your favorite season for hiking?",
            "12. What motivates you the most when going on a hike?",
            "13. How important is privacy to you during a hike?",
            "14. Which of the following aspects would you like to improve during a hike?",
            "15. What type of accommodation do you prefer during a hike?",
            "16. What level of comfort do you expect during the hike?",
            "17. Which of the following facilities do you consider essential?",
            "18. Would you like to have guides during the hike?",
            "19. How long do you prefer a hike to last?",
            "20. Do you have any medical conditions we should consider when planning your hike?",
            "21. How would you rate your current physical condition?",
            "22. Are you willing to participate in physically demanding activities?",
            "23. Would you like to receive safety and health information before the hike?",
            "24. Do you have any suggestions or additional comments about your hiking preferences?",
        ]

        responses = []
        # Generate responses for each question
        for question in questions:
            prompt = f"{description} {question}"
            response = self.generate_response(prompt)
            responses.append(response)
            print(f"{question}\nResponse: {response}\n")

        return responses

    def analyze_responses(self, responses):
        # Consolidate responses into a single text
        responses_text = " ".join(responses)

        # Prompt to extract characteristics from the text
        prompt = (
            f"Analyze the following text and extract characteristics of the explorer. "
            f"Text: {responses_text} "
            "Characteristics to extract: experience, landscape interest, motivation, "
            "comfort, physical condition, preferred hike duration, guide usage, "
            "concern for safety and health, and preferred group size. "
            "Provide a summary in the following format: "
            "Experience: [value], Landscape Interest: [value], Motivation: [value], "
            "Comfort: [value], Physical Condition: [value], Duration: [value], "
            "Guide Usage: [value], Safety and Health: [value], Group Size: [value]."
        )

        # Generate analyzed response by the LLM
        characteristics_response = self.generate_response(prompt, max_length=150)

        # Parse the response to obtain characteristics
        characteristics = {}
        for line in characteristics_response.split(','):
            if ':' in line:
                key, value = line.split(':')
                characteristics[key.strip().lower()] = int(value.strip())

        return characteristics

