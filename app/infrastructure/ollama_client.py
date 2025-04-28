from ollama import Client
import os
import logging

logger = logging.getLogger(__name__)

class OllamaClientWrapper:
    def __init__(self):
        self.client = Client(
            host=f"http://{os.getenv('OLLAMA_HOST', 'localhost')}:{os.getenv('OLLAMA_PORT', '11434')}"
        )
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

    def generate_description(self, animal_name: str) -> str:
        prompt = f"Опиши основные визуальные признаки животного {animal_name} используя 15 или меньше слов на русском"
        try:
            logger.info(f"Generating description for animal: {animal_name}")
            response = self.client.generate(model=self.model, prompt=prompt)
            description = response["response"].strip()
            logger.info(f"Description generated successfully for {animal_name}")
            return description
        except Exception as e:
            logger.error(f"Failed to generate description for {animal_name}: {str(e)}")
            return f"Description unavailable for {animal_name} due to an error."