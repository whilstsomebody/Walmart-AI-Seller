from .speech_to_text import get_transcript
from .text_to_speech import TTS


class ConversationManager:
    def __init__(self, assistant):
        intro_message = "Hello! I am your Sales agent from the Walmart Team. How can I help you today?"
        print(intro_message)
        TTS().speak(intro_message)
        self.transcription_response = ""
        self.assistant = assistant

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        # Loop indefinitely until "goodbye" is said
        while True:
            await get_transcript(handle_full_sentence)
            
            # Check for "goodbye" to exit the loop
            if "goodbye" in self.transcription_response.lower():
                # Check if there is other text before 'goodbye'
                user_text = self.transcription_response.lower().replace("goodbye", "").strip()
                if user_text:
                    # Respond to the user's message before saying goodbye
                    llm_response = self.assistant.invoke(self.transcription_response)
                    print(f"AI: {llm_response}")
                    TTS().speak(llm_response)
                else:
                    farewell_message = "Thank you for asking your queries! Feel free to ask anything if you need help again. Goodbye!"
                    print(f"AI: {farewell_message}")
                    TTS().speak(farewell_message)
                break
            
            llm_response = self.assistant.invoke(self.transcription_response)
            print(f"AI: {llm_response}")

            tts = TTS()
            tts.speak(llm_response)

            # Reset transcription_response for the next loop iteration
            self.transcription_response = ""