import google.generativeai as genai
import os
import json
import asyncio
import time
from typing import Dict, List, Any, Optional
from google.generativeai.types import generation_types
from rate_limiter import GeminiRateLimiter
from prompt_templates import GeminiPrompts

class GeminiSkepticAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.rate_limiter = GeminiRateLimiter()
        self.prompts = GeminiPrompts()
        
        # Generation config for consistent results
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.2,
            top_p=0.8,
            top_k=40,
            max_output_tokens=4096,
        )
    
    async def analyze_article(self, article_content: str, article_metadata: Dict, stages: set = None) -> Dict[str, Any]:
        """
        Complete multi-stage analysis of the article

        Args:
            article_content: The content of the article to analyze.
            article_metadata: Metadata about the article.
            stages: A set of strings representing which analysis stages to run. 
                    If None, all stages are run. 
                    Available stages: {'claims', 'language', 'red_flags', 'verification', 'entities', 'counter_arguments', 'assessment'}
        """
        if stages is None:
            stages = {'claims', 'language', 'red_flags', 'verification', 'entities', 'counter_arguments', 'assessment'}

        print(f"🔍 Starting analysis with stages: {stages}...")
        
        analysis_results = {
            'metadata': article_metadata,
            'analysis_timestamp': self._get_timestamp(),
        }
        
        try:
            # Pre-analysis Step (always runs)
            print("  🤔 Performing pre-analysis...")
            pre_analysis_monologue = await self._pre_analyze_article(article_content)
            analysis_results['pre_analysis'] = pre_analysis_monologue

            # Stage 1: Core Claims Extraction
            if 'claims' in stages:
                print("  📋 Extracting core claims...")
                analysis_results['claims'] = await self._extract_claims(article_content, pre_analysis_monologue)
            
            # Stage 2: Language & Tone Analysis
            if 'language' in stages:
                print("  🎭 Analyzing language and tone...")
                analysis_results['language_analysis'] = await self._analyze_language(article_content, pre_analysis_monologue)
            
            # Stage 3: Bias & Red Flags Detection
            if 'red_flags' in stages:
                print("  🚩 Detecting bias and red flags...")
                analysis_results['red_flags'] = await self._detect_red_flags(article_content, pre_analysis_monologue)
            
            # Stage 4: Verification Questions
            if 'verification' in stages:
                print("  ❓ Generating verification questions...")
                analysis_results['verification'] = await self._generate_verification_questions(
                    article_content, analysis_results.get('claims', {}.get('core_claims', []))
                )
            
            # Stage 5: Entity Recognition (Bonus Feature)
            if 'entities' in stages:
                print("  🏷️ Extracting key entities...")
                analysis_results['entities'] = await self._extract_entities(article_content, pre_analysis_monologue)
            
            # Stage 6: Counter-Argument Simulation (Bonus Feature)
            if 'counter_arguments' in stages:
                print("  ⚖️ Generating counter-arguments...")
                analysis_results['counter_arguments'] = await self._generate_counter_arguments(
                    analysis_results.get('claims', {}.get('core_claims', [])), 
                    analysis_results.get('language_analysis', {})
                )
            
            # Stage 7: Overall Assessment
            if 'assessment' in stages:
                print("  📊 Generating overall assessment...")
                analysis_results['overall_assessment'] = await self._generate_overall_assessment(
                    analysis_results
                )
            
            print("✅ Analysis complete!")
            return analysis_results
            
        except Exception as e:
            print(f"❌ Analysis error: {str(e)}")
            raise e

    async def _pre_analyze_article(self, article_content: str) -> str:
        """Generate an internal monologue/pre-analysis of the article."""
        await self.rate_limiter.wait_if_needed()
        prompt = self.prompts.pre_analysis_prompt(article_content)
        try:
            response = await self._generate_content(prompt)
            return response
        except Exception as e:
            return f"Pre-analysis failed: {str(e)}"

    async def _extract_claims(self, article_content: str, context: str) -> Dict[str, Any]:
        """Extract and categorize factual claims"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.claims_extraction_prompt(article_content)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'claims extraction')
        except Exception as e:
            return {'error': f'Claims extraction failed: {str(e)}', 'claims': []}
    
    async def _analyze_language(self, article_content: str, context: str) -> Dict[str, Any]:
        """Analyze language patterns and tone"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.language_analysis_prompt(article_content)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'language analysis')
        except Exception as e:
            return {'error': f'Language analysis failed: {str(e)}'}
    
    async def _detect_red_flags(self, article_content: str, context: str) -> Dict[str, Any]:
        """Detect bias indicators and red flags"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.bias_detection_prompt(article_content)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'red flags detection')
        except Exception as e:
            return {'error': f'Red flags detection failed: {str(e)}', 'red_flags': []}
    
    async def _generate_verification_questions(self, article_content: str, claims: List[str]) -> Dict[str, Any]:
        """Generate questions for fact verification"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.verification_questions_prompt(article_content, claims)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'verification questions')
        except Exception as e:
            return {'error': f'Verification questions failed: {str(e)}', 'questions': []}
    
    async def _extract_entities(self, article_content: str, context: str) -> Dict[str, Any]:
        """Extract key entities and suggest research"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.entity_extraction_prompt(article_content)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'entity extraction')
        except Exception as e:
            return {'error': f'Entity extraction failed: {str(e)}', 'entities': []}
    
    async def _generate_counter_arguments(self, claims: List[str], language_analysis: Dict) -> Dict[str, Any]:
        """Generate counter-arguments and alternative perspectives"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.counter_argument_prompt(claims, language_analysis)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'counter arguments')
        except Exception as e:
            return {'error': f'Counter argument generation failed: {str(e)}', 'counter_arguments': []}
    
    async def _generate_overall_assessment(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate overall credibility assessment"""
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.prompts.overall_assessment_prompt(analysis_results)
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response, 'overall assessment')
        except Exception as e:
            return {'error': f'Overall assessment failed: {str(e)}'}
    
    async def _generate_content(self, prompt: str, retries: int = 3, delay: int = 5) -> str:
        """Generate content using Gemini with error handling, retries, and safety checks."""
        for attempt in range(retries):
            try:
                response = await self.model.generate_content_async(
                    prompt,
                    generation_config=self.generation_config,
                    # safety_settings=... # Consider adding safety settings if needed
                )
                
                # Check for prompt feedback indicating a block
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    raise generation_types.BlockedPromptError(
                        f"Prompt blocked due to {response.prompt_feedback.block_reason.name}: "
                        f"{response.prompt_feedback.safety_ratings}"
                    )

                # Access text safely
                return response.text

            except generation_types.BlockedPromptError as e:
                print(f"❌ Attempt {attempt + 1}/{retries}: Prompt blocked. {e}")
                # This is a final error, no need to retry
                raise Exception(f"Gemini API error: Prompt was blocked. {e}") from e

            except Exception as e:
                # Catch-all for other potential API errors (e.g., network issues, 500 errors)
                print(f"⚠️ Attempt {attempt + 1}/{retries}: Gemini API error: {e}")
                if attempt + 1 == retries:
                    raise Exception(f"Gemini API error after {retries} attempts: {e}") from e
                
                # Exponential backoff
                await asyncio.sleep(delay * (2 ** attempt))
        
        # This line should not be reached if retries are exhausted
        raise Exception("Gemini API failed to generate content after multiple retries.")
    
    def _parse_json_response(self, response: str, operation: str) -> Dict[str, Any]:
        """Parse JSON response with fallback handling"""
        try:
            # Clean the response by finding the first '{' and the last '}'
            start_index = response.find('{')
            end_index = response.rfind('}')
            if start_index != -1 and end_index != -1:
                json_str = response[start_index:end_index+1]
                return json.loads(json_str)
            else:
                raise json.JSONDecodeError("No JSON object found", response, 0)
        except json.JSONDecodeError:
            # Fallback for malformed JSON
            print(f"⚠️ Warning: Failed to parse JSON for '{operation}'. Using raw response.")
            return {
                'raw_response': response,
                'parsed': False,
                'operation': operation,
                'error': 'JSONDecodeError'
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
''
