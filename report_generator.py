# report_generator.py
from typing import Dict, Any, List
from datetime import datetime

class MarkdownReportGenerator:
    def __init__(self):
        pass
    
    def generate_report(self, article_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Generate comprehensive Markdown report
        """
        report_sections = [
            self._generate_header(article_data, analysis),
            self._generate_article_info(article_data),
            self._generate_claims_section(analysis.get('claims', {})),
            self._generate_language_analysis_section(analysis.get('language_analysis', {})),
            self._generate_red_flags_section(analysis.get('red_flags', {})),
            self._generate_verification_section(analysis.get('verification', {})),
            self._generate_entities_section(analysis.get('entities', {})),
            self._generate_counter_arguments_section(analysis.get('counter_arguments', {})),
            self._generate_overall_assessment_section(analysis.get('overall_assessment', {})),
            self._generate_footer(analysis)
        ]
        
        return "\n\n".join(filter(None, report_sections))
    
    def _generate_header(self, article_data: Dict, analysis: Dict) -> str:
        """Generate report header"""
        title = article_data.get('metadata', {}).get('title', 'Untitled Article')
        
        return f"""# 🔍 Digital Skeptic Analysis Report

**Article:** {title}  
**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Powered by:** Gemini-1.5-pro

---"""
    
    def _generate_article_info(self, article_data: Dict) -> str:
        """Generate article information section"""
        metadata = article_data.get('metadata', {})
        
        return f"""## 📰 Article Information

- **Title:** {metadata.get('title', 'Not found')}
- **Author:** {metadata.get('author', 'Not found')}
- **Publication:** {metadata.get('domain', 'Unknown')}
- **URL:** {article_data.get('url', 'Not provided')}
- **Content Length:** {article_data.get('extracted_length', 0)} characters"""
    
    def _generate_claims_section(self, claims_data: Dict) -> str:
        """Generate claims analysis section"""
        if not claims_data or 'error' in claims_data:
            return f"""## 📋 Core Claims Analysis

❌ **Analysis Error:** {claims_data.get('error', 'Unknown error occurred')}"""
        
        claims_list = claims_data.get('core_claims', [])
        if not claims_list:
            return """## 📋 Core Claims Analysis

ℹ️ **No specific factual claims identified** in this article."""
        
        certainty = claims_data.get('analysis_certainty', 'N/A')
        section = f"""## 📋 Core Claims Analysis (Certainty: {certainty})\n"""
        
        for i, claim in enumerate(claims_list, 1):
            section += f"""
### Claim {i}
- **Statement:** {claim.get('claim', 'Not specified')}
- **Type:** {claim.get('type', 'Unknown')}
- **Confidence Level:** {claim.get('confidence_level', 'Unknown')}
- **Evidence Provided:** {claim.get('evidence_provided', 'None')}
- **Verifiability:** {claim.get('verifiability', 'Unknown')}"""
        
        section += f"\n\n**Summary:** {claims_data.get('claim_summary', 'No summary available')}"
        
        return section
    
    def _generate_language_analysis_section(self, language_data: Dict) -> str:
        """Generate language analysis section"""
        if not language_data or 'error' in language_data:
            return f"""## 🎭 Language & Tone Analysis

❌ **Analysis Error:** {language_data.get('error', 'Unknown error occurred')}"""
        
        certainty = language_data.get('analysis_certainty', 'N/A')
        section = f"""## 🎭 Language & Tone Analysis (Certainty: {certainty})

- **Overall Tone:** {language_data.get('overall_tone', 'Unknown')}
- **Language Intensity:** {language_data.get('language_intensity', 'Unknown')}
- **Certainty Level:** {language_data.get('certainty_level', 'Unknown')}
- **Reasoning Type:** {language_data.get('reasoning_type', 'Unknown')}"""
        
        # Add loaded language examples
        loaded_examples = language_data.get('loaded_language_examples', [])
        if loaded_examples:
            section += "\n\n### 🎯 Loaded Language Examples"
            for example in loaded_examples:
                section += f"\n- **\"{example.get('phrase', 'N/A')}\"** - {example.get('type', 'Unknown')} bias: {example.get('impact', 'No description')}"
        
        # Add hedging vs absolute language
        hedging = language_data.get('hedging_language', [])
        absolute = language_data.get('absolute_statements', [])
        
        if hedging:
            section += f"\n\n### 🤔 Hedging Language\n" + "\n".join([f"- \"{phrase}\"" for phrase in hedging])
        
        if absolute:
            section += f"\n\n### ❗ Absolute Statements\n" + "\n".join([f"- \"{phrase}\"" for phrase in absolute])
        
        return section
    
    def _generate_red_flags_section(self, red_flags_data: Dict) -> str:
        """Generate red flags section"""
        if not red_flags_data or 'error' in red_flags_data:
            return f"""## 🚩 Bias & Red Flags

❌ **Analysis Error:** {red_flags_data.get('error', 'Unknown error occurred')}"""
        
        certainty = red_flags_data.get('analysis_certainty', 'N/A')
        bias_level = red_flags_data.get('bias_risk_level', 'Unknown')
        
        # Determine emoji based on bias level
        bias_emoji = {
            'LOW': '✅',
            'MEDIUM': '⚠️', 
            'HIGH': '🚨'
        }.get(bias_level, '❓')
        
        section = f"""## 🚩 Bias & Red Flags (Certainty: {certainty})

**Overall Bias Risk:** {bias_emoji} **{bias_level}**

**Article Balance:** {red_flags_data.get('overall_balance', 'Unknown')}"""
        
        # Add red flags
        red_flags = red_flags_data.get('red_flags', [])
        if red_flags:
            section += "\n\n### Identified Issues"
            for flag in red_flags:
                severity_emoji = {'Minor': '⚪', 'Moderate': '🟡', 'Major': '🔴'}.get(flag.get('severity'), '❓')
                section += f"""
#### {severity_emoji} {flag.get('category', 'Unknown')} Issue - {flag.get('severity', 'Unknown')}
- **Issue:** {flag.get('issue', 'Not specified')}
- **Example:** "{flag.get('example', 'No example provided')}"
- **Why problematic:** {flag.get('explanation', 'No explanation provided')}"""
        
        # Add missing perspectives
        missing = red_flags_data.get('missing_perspectives', [])
        if missing:
            section += f"\n\n### 👥 Missing Perspectives\n" + "\n".join([f"- {perspective}" for perspective in missing])
        
        return section
    
    def _generate_verification_section(self, verification_data: Dict) -> str:
        """Generate verification questions section"""
        if not verification_data or 'error' in verification_data:
            return f"""## ❓ Verification Questions

❌ **Analysis Error:** {verification_data.get('error', 'Unknown error occurred')}"""
        
        section = """## ❓ Verification & Fact-Checking Guide"""
        
        questions = verification_data.get('verification_questions', [])
        if questions:
            section += "\n\n### 🔍 Key Verification Questions"
            for i, q in enumerate(questions, 1):
                difficulty_emoji = {'Easy': '🟢', 'Moderate': '🟡', 'Difficult': '🔴'}.get(q.get('difficulty'), '❓')
                section += f"""
#### {i}. {difficulty_emoji} {q.get('question', 'No question')}
- **Related Claim:** {q.get('claim_related', 'Not specified')}
- **Method:** {q.get('verification_method', 'Not specified')}
- **Suggested Sources:** {', '.join(q.get('suggested_sources', []))}"""
        
        # Add quick checks
        quick_checks = verification_data.get('quick_checks', [])
        if quick_checks:
            section += f"\n\n### ⚡ Quick Fact Checks\n" + "\n".join([f"- {check}" for check in quick_checks])
        
        return section
    
    def _generate_entities_section(self, entities_data: Dict) -> str:
        """Generate entities section"""
        if not entities_data or 'error' in entities_data:
            return f"""## 🏷️ Key Entities

❌ **Analysis Error:** {entities_data.get('error', 'Unknown error occurred')}"""
        
        section = """## 🏷️ Key Entities & Research Suggestions"""
        
        # Add people
        people = entities_data.get('people', [])
        if people:
            section += "\n\n### 👥 Key People"
            for person in people:
                priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(person.get('research_priority'), '❓')
                section += f"""
#### {priority_emoji} {person.get('name', 'Unknown')}
- **Role:** {person.get('role', 'Not specified')}
- **Credibility Factors:** {', '.join(person.get('credibility_factors', []))}"""
        
        # Add organizations
        orgs = entities_data.get('organizations', [])
        if orgs:
            section += "\n\n### 🏢 Organizations"
            for org in orgs:
                section += f"""
#### {org.get('name', 'Unknown')}
- **Type:** {org.get('type', 'Not specified')}
- **Relevance:** {org.get('relevance', 'Not specified')}
- **Potential Bias:** {org.get('potential_bias', 'None identified')}"""
        
        return section
    
    def _generate_counter_arguments_section(self, counter_data: Dict) -> str:
        """Generate counter-arguments section"""
        if not counter_data or 'error' in counter_data:
            return f"""## ⚖️ Alternative Perspectives

❌ **Analysis Error:** {counter_data.get('error', 'Unknown error occurred')}"""
        
        section = """## ⚖️ Alternative Perspectives & Counter-Arguments"""
        
        counter_args = counter_data.get('counter_arguments', [])
        if counter_args:
            section += "\n\n### 🔄 Counter-Arguments"
            for i, arg in enumerate(counter_args, 1):
                strength_emoji = {'Strong': '💪', 'Moderate': '👍', 'Weak': '👎'}.get(arg.get('strength'), '❓')
                section += f"""
#### {i}. {strength_emoji} Alternative View ({arg.get('strength', 'Unknown')} argument)
- **Original Claim:** {arg.get('original_claim', 'Not specified')}
- **Counter-Perspective:** {arg.get('counter_perspective', 'Not provided')}
- **Supporting Reasoning:** {arg.get('supporting_reasoning', 'Not provided')}
- **Evidence Type Needed:** {arg.get('evidence_type', 'Not specified')}"""
        
        # Add skeptical questions
        skeptical_qs = counter_data.get('skeptical_questions', [])
        if skeptical_qs:
            section += f"\n\n### 🤔 Questions a Skeptic Would Ask\n" + "\n".join([f"- {q}" for q in skeptical_qs])
        
        return section
    
    def _generate_overall_assessment_section(self, assessment_data: Dict) -> str:
        """Generate overall assessment section"""
        if not assessment_data or 'error' in assessment_data:
            return f"""## 📊 Overall Assessment

❌ **Analysis Error:** {assessment_data.get('error', 'Unknown error occurred')}"""
        
        credibility_level = assessment_data.get('credibility_level', 'Unknown')
        score_data = assessment_data.get('credibility_score', {})
        score = score_data.get('value', 'N/A')
        reasoning = score_data.get('reasoning', 'No reasoning provided.')
        
        # Determine emoji based on credibility
        credibility_emoji = {
            'Very High': '🟢',
            'High': '🔵', 
            'Medium': '🟡',
            'Low': '🟠',
            'Very Low': '🔴'
        }.get(credibility_level, '❓')
        
        section = f"""## 📊 Overall Credibility Assessment

**Credibility Score:** {score}/100  
**Level:** {credibility_emoji} **{credibility_level}**

**Reasoning:** {reasoning}

### 💡 Reader Guidance
- **Trust Level:** {assessment_data.get('reader_guidance', {}).get('trust_level', 'Unknown')}
- **Verification Needed:** {assessment_data.get('reader_guidance', {}).get('verification_needed', 'Unknown')}
- **Seek Additional Sources:** {assessment_data.get('reader_guidance', {}).get('additional_sources', 'Unknown')}

### ✅ Key Strengths"""
        
        strengths = assessment_data.get('key_strengths', [])
        if strengths:
            section += "\n" + "\n".join([f"- {strength}" for strength in strengths])
        else:
            section += "\n- No specific strengths identified"
        
        section += "\n\n### ⚠️ Key Concerns"
        concerns = assessment_data.get('key_concerns', [])
        if concerns:
            section += "\n" + "\n".join([f"- {concern}" for concern in concerns])
        else:
            section += "\n- No significant concerns identified"
        
        section += f"\n\n### 📝 Recommendation\n{assessment_data.get('recommendation', 'No specific recommendation provided')}"
        
        section += f"\n\n### 🎯 Summary\n{assessment_data.get('summary', 'No summary available')}"
        
        return section
    
    def _generate_footer(self, analysis: Dict) -> str:
        """Generate report footer"""
        return f"""---

## ℹ️ About This Analysis

This analysis was generated by **Digital Skeptic AI** using Google's Gemini-1.5-pro language model. The analysis includes:

- ✅ **Core Claims Extraction** - Identification and categorization of factual claims
- ✅ **Language Analysis** - Tone, bias, and rhetorical patterns
- ✅ **Red Flag Detection** - Potential bias indicators and logical fallacies  
- ✅ **Verification Guide** - Specific questions and fact-checking suggestions
- ✅ **Entity Recognition** - Key people and organizations requiring research
- ✅ **Counter-Arguments** - Alternative perspectives and opposing viewpoints
- ✅ **Credibility Assessment** - Overall reliability evaluation

**Disclaimer:** This analysis is intended to assist critical thinking and should not replace human judgment or professional fact-checking services.

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
