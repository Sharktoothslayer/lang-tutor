import httpx
import json
import logging
from typing import Dict, List, Any, Optional
from app.core.config import settings
from app.services.spaced_repetition import SpacedRepetitionService

logger = logging.getLogger(__name__)

class OllamaService:
    """
    Service for interacting with Ollama local LLM for AI-powered conversations
    and language learning assistance.
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.temperature = settings.OLLAMA_TEMPERATURE
        self.max_tokens = settings.OLLAMA_MAX_TOKENS
        self.client = httpx.AsyncClient(timeout=30.0)
        self.spaced_repetition = SpacedRepetitionService()
    
    async def initialize(self):
        """Initialize the Ollama service and check model availability."""
        try:
            # Check if Ollama is running
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                if self.model not in model_names:
                    logger.warning(f"Model {self.model} not found. Available models: {model_names}")
                    # Try to pull the model
                    await self._pull_model()
                else:
                    logger.info(f"Model {self.model} is available")
            else:
                logger.error(f"Failed to connect to Ollama: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error initializing Ollama service: {e}")
    
    async def _pull_model(self):
        """Pull the specified model from Ollama."""
        try:
            logger.info(f"Pulling model {self.model}...")
            response = await self.client.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model}
            )
            if response.status_code == 200:
                logger.info(f"Successfully pulled model {self.model}")
            else:
                logger.error(f"Failed to pull model {self.model}: {response.status_code}")
        except Exception as e:
            logger.error(f"Error pulling model: {e}")
    
    async def generate_conversation_response(
        self,
        user_message: str,
        user_id: str,
        conversation_context: List[Dict[str, str]] = None,
        target_language: str = "es",
        difficulty_level: int = 1,
        known_words: List[str] = None,
        new_words_to_introduce: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate an AI response for language learning conversation.
        
        Args:
            user_message: The user's message
            user_id: User ID for personalization
            conversation_context: Previous conversation messages
            target_language: Target language for learning
            difficulty_level: Current difficulty level (1-5)
            known_words: Words the user already knows
            new_words_to_introduce: New words to introduce in this response
        """
        try:
            # Build the prompt for language learning
            prompt = self._build_conversation_prompt(
                user_message,
                target_language,
                difficulty_level,
                known_words,
                new_words_to_introduce,
                conversation_context
            )
            
            # Generate response from Ollama
            response = await self._generate_response(prompt)
            
            # Extract vocabulary used and new words introduced
            vocabulary_used = self._extract_vocabulary(response, known_words or [])
            new_words_introduced = self._extract_new_words(response, known_words or [])
            
            # Adjust difficulty based on response quality
            difficulty_adjustment = self._calculate_difficulty_adjustment(
                response, user_message, difficulty_level
            )
            
            return {
                'response_text': response,
                'vocabulary_used': vocabulary_used,
                'new_words_introduced': new_words_introduced,
                'difficulty_adjustment': difficulty_adjustment,
                'target_language': target_language,
                'response_quality': self._assess_response_quality(response, target_language)
            }
            
        except Exception as e:
            logger.error(f"Error generating conversation response: {e}")
            return {
                'response_text': f"Lo siento, tengo un problema técnico. ¿Podrías repetir tu mensaje?",
                'vocabulary_used': [],
                'new_words_introduced': [],
                'difficulty_adjustment': 0,
                'target_language': target_language,
                'response_quality': 'error'
            }
    
    def _build_conversation_prompt(
        self,
        user_message: str,
        target_language: str,
        difficulty_level: int,
        known_words: List[str],
        new_words_to_introduce: List[str],
        conversation_context: List[Dict[str, str]]
    ) -> str:
        """Build a comprehensive prompt for the AI conversation."""
        
        # Base instruction
        prompt = f"""You are a helpful language tutor for {target_language or 'Italian'}. Your goal is to help the student learn through natural conversation.

IMPORTANT RULES:
1. Always respond in {target_language} unless specifically asked otherwise
2. Use simple, clear language appropriate for difficulty level {difficulty_level}
3. Reinforce vocabulary the student already knows
4. Gradually introduce new words naturally
5. Keep responses conversational and engaging
6. Correct major errors gently and naturally
7. Use context clues to help understanding

Student's known vocabulary: {', '.join(known_words[:20]) if known_words else 'Beginner level'}

New words to introduce in this response: {', '.join(new_words_to_introduce) if new_words_to_introduce else 'None'}

Difficulty level: {difficulty_level}/5 (1=beginner, 5=advanced)

Conversation context:
"""
        
        # Add conversation context
        if conversation_context:
            for msg in conversation_context[-5:]:  # Last 5 messages
                prompt += f"{msg['role']}: {msg['content']}\n"
        
        prompt += f"""
Student: {user_message}

Tutor (respond in {target_language}):"""
        
        return prompt
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response from Ollama using the chat API."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                                                      return "Mi dispiace, non posso rispondere in questo momento."
                
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {e}")
                               return "Mi dispiace, c'è un problema tecnico."
    
    def _extract_vocabulary(self, response: str, known_words: List[str]) -> List[str]:
        """Extract vocabulary words used in the response."""
        # Simple word extraction - could be enhanced with NLP
        words = response.lower().split()
        vocabulary = []
        
        for word in words:
            # Clean the word
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 2 and clean_word in known_words:
                vocabulary.append(clean_word)
        
        return list(set(vocabulary))
    
    def _extract_new_words(self, response: str, known_words: List[str]) -> List[str]:
        """Extract new words that weren't in the known vocabulary."""
        words = response.lower().split()
        new_words = []
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if (len(clean_word) > 2 and 
                clean_word not in known_words and 
                clean_word not in new_words):
                new_words.append(clean_word)
        
        return new_words[:3]  # Limit to 3 new words per response
    
    def _calculate_difficulty_adjustment(
        self,
        response: str,
        user_message: str,
        current_difficulty: int
    ) -> int:
        """Calculate if difficulty should be adjusted based on response quality."""
        # Simple heuristics for difficulty adjustment
        response_length = len(response.split())
        user_length = len(user_message.split())
        
        # If response is much longer than user message, might be too complex
        if response_length > user_length * 3:
            return -1  # Decrease difficulty
        
        # If response is very short, might be too simple
        elif response_length < user_length * 0.5:
            return 1  # Increase difficulty
        
        return 0  # No adjustment needed
    
    def _assess_response_quality(self, response: str, target_language: str) -> str:
        """Assess the quality of the AI response."""
        # Simple quality assessment
        if len(response) < 10:
            return "too_short"
        elif len(response) > 200:
            return "too_long"
        else:
            return "good"
    
    async def generate_practice_exercise(
        self,
        target_language: str,
        difficulty_level: int,
        vocabulary_focus: List[str] = None,
        exercise_type: str = "conversation"
    ) -> Dict[str, Any]:
        """Generate practice exercises for language learning."""
        try:
            prompt = f"""Generate a {exercise_type} exercise in {target_language} for difficulty level {difficulty_level}.

Focus vocabulary: {', '.join(vocabulary_focus) if vocabulary_focus else 'General vocabulary'}

Create an engaging exercise that:
1. Uses appropriate language level
2. Incorporates the focus vocabulary naturally
3. Provides clear instructions
4. Includes example responses
5. Is fun and interactive

Format the response as JSON with:
- exercise_type
- instructions
- vocabulary_used
- example_responses
- difficulty_rating
"""
            
            response = await self._generate_response(prompt)
            
            # Try to parse JSON response
            try:
                exercise_data = json.loads(response)
                return exercise_data
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    'exercise_type': exercise_type,
                    'instructions': response,
                    'vocabulary_used': vocabulary_focus or [],
                    'example_responses': [],
                    'difficulty_rating': difficulty_level
                }
                
        except Exception as e:
            logger.error(f"Error generating practice exercise: {e}")
            return {
                'exercise_type': exercise_type,
                'instructions': f"Error generating exercise: {str(e)}",
                'vocabulary_used': [],
                'example_responses': [],
                'difficulty_rating': difficulty_level
            }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose() 