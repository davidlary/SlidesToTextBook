import logging
from typing import List, Dict, Any
from slides_to_textbook.utils.api_clients import AIClient
from scholarly import scholarly

class TopicResearcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ai_client = AIClient()

    def research_topic(self, topic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich topic data with historical context and citations.
        """
        title = topic_data.get("title", "")
        self.logger.info(f"Researching topic: {title}")
        
        # 1. AI Research for History/Context
        context = self._get_historical_context(title, topic_data.get("people", []))
        
        # 2. Scholarly search for citations (simplified for now)
        citations = self._find_key_papers(title, topic_data.get("concepts", []))
        
        return {
            **topic_data,
            "research": {
                "historical_context": context,
                "citations": citations
            }
        }

    def _get_historical_context(self, topic: str, people: List[str]) -> str:
        prompt = f"""
        Provide a detailed historical context for the machine learning topic: "{topic}".
        Include:
        - Origin of the key concepts
        - Key figures involved (specifically mentioned: {', '.join(people)})
        - Timeline of development
        - Etymology of terms if relevant
        
        Write in an engaging, narrative style suitable for a textbook introduction.
        """
        
        try:
            return self.ai_client.generate_text(prompt, system_prompt="You are a history of science expert.", model="claude")
        except Exception as e:
            self.logger.error(f"Failed to get historical context: {e}")
            return "Historical context unavailable."

    def _find_key_papers(self, topic: str, concepts: List[str]) -> List[Dict[str, Any]]:
        """
        Search for seminal papers using scholarly.
        """
        results = []
        # Limit to top 3 search queries to avoid rate limits
        queries = [topic] + concepts[:2]
        
        for q in queries:
            try:
                # search_pubs returns a generator
                search_query = scholarly.search_pubs(q)
                pub = next(search_query, None)
                if pub:
                    # Fill structure for bibliography
                    results.append({
                        "title": pub['bib'].get('title'),
                        "author": pub['bib'].get('author'),
                        "year": pub['bib'].get('pub_year'),
                        "url": pub.get('pub_url', ''),
                        "entry_type": "article" # simplistic assumption
                    })
            except Exception as e:
                self.logger.warning(f"Scholarly search failed for {q}: {e}")
        
        return results
