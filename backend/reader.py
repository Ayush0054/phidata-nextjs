from phi.agent import Agent , RunResponse
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.model.openai.chat import OpenAIChat
from phi.storage.agent.postgres import PgAgentStorage
from phi.document.chunking.agentic import AgenticChunking
from phi.utils.log import logger

from typing import List, Dict, Any
import json

class ReadingCompanionSystem:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.vector_db = PgVector(table_name="readpal_knowledge", db_url=db_url)
        self.current_sections = {}
        self.reading_progress = {}
        self.knowledge_bases = {}  # Cache for knowledge bases
        self.agents = {}  # Cache for agents
        
    def create_knowledge_base(self, pdf_url: str):
        try:
            logger.info(f"Starting knowledge base creation for URL: {pdf_url}")
            knowledge_base = PDFUrlKnowledgeBase(
                urls=[pdf_url],
                vector_db=self.vector_db,
                chunking_strategy=AgenticChunking()
            )
            logger.info("Loading knowledge base into database...")
            knowledge_base.load(recreate=True)
            # Force initialization and loading of documents
           
            logger.info(f"Successfully created knowledge base with {knowledge_base} documents")
            
            if knowledge_base == 0:
                logger.error("No documents were loaded into the knowledge base")
                raise ValueError("Failed to load any documents from the PDF URL")
            
            return knowledge_base
            
        except Exception as e:
            logger.error(f"Error creating knowledge base: {str(e)}")
            raise

    def setup_qa_agent(self, knowledge_base):
        return Agent(
            name="QA Assistant",
            role="Answer specific questions about the book content",
            model=OpenAIChat(id="gpt-4o"),
            knowledge=knowledge_base,
            storage=PgAgentStorage(table_name="qa_agent", db_url=self.db_url),
            instructions=[
                "You are a knowledgeable reading companion who has thoroughly read this book.",
                "Always base your answers on the specific content from the book.",
                "Include direct quotes or references when possible to support your answers.",
                "If information isn't explicitly mentioned in the text, say so clearly.",
                "Keep responses focused and relevant to the question asked.",
                "If the question is unclear, ask for clarification."
            ],
            search_knowledge=True,
            markdown=True
        )

    def setup_summary_agent(self, knowledge_base):
        return Agent(
            name="Summarization Assistant",
            role="Generate concise summaries of book sections",
            model=OpenAIChat(id="gpt-4o"),
            knowledge=knowledge_base,
            storage=PgAgentStorage(table_name="summary_agent", db_url=self.db_url),
            instructions=[
                "Create clear, structured summaries based on the actual content of the book.",
                "Include major plot points, key events, and significant character developments.",
                "Organize summaries with clear sections or bullet points for readability.",
                "Maintain chronological order of events when summarizing.",
                "Highlight important themes or recurring elements.",
                "Keep summaries objective and based strictly on the text.",
                "Include chapter or section references when relevant."
            ],
            search_knowledge=True,
            markdown=True
        )

    def setup_insight_agent(self, knowledge_base):
        return Agent(
            name="Insight Generator",
            role="Generate deeper insights and discussion points",
            model=OpenAIChat(id="gpt-4o"),
            knowledge=knowledge_base,
            storage=PgAgentStorage(table_name="insight_agent", db_url=self.db_url),
            instructions=[
                "Analyze the document thoroughly to extract meaningful insights",
                "Identify and explain key themes, patterns, and concepts",
                "Support all insights with specific examples from the text",
                "Consider the historical or cultural context when relevant",
                "Highlight important relationships between different ideas",
                "Discuss significant implications of the main points",
                "Focus on both explicit and implicit meanings in the text",
                "Maintain objectivity while providing analytical depth",
                "Structure insights in a clear, organized manner"
            ],
            search_knowledge=True,
            markdown=True
        )

    def setup_personalization_agent(self, knowledge_base):
        return Agent(
            name="Personalization Assistant",
            role="Provide personalized reading suggestions and track progress",
            model=OpenAIChat(id="gpt-4o"),
            knowledge=knowledge_base,
            storage=PgAgentStorage(table_name="personalization_agent", db_url=self.db_url),
            instructions=[
                "Track user's reading progress and interests",
                "Suggest relevant sections based on user's preferences",
                "Identify connections between different parts of the text",
                "Provide personalized reading paths",
                "Highlight sections that align with user's interests",
                "Adapt suggestions based on user's comprehension level",
                "When updating progress, respond with a confirmation message"
            ],
            search_knowledge=True,
            markdown=True
        )

    def update_reading_progress(self, section: str, progress: float) -> Dict[str, Any]:
        """Update reading progress for a specific section"""
        self.reading_progress[section] = progress
        return {"status": "success", "progress": self.reading_progress}

    def get_section_suggestions(self, user_interests: List[str]) -> List[str]:
        """Generate personalized section suggestions based on user interests"""
        return [section for section in self.current_sections 
                if any(interest in section.lower() for interest in user_interests)]

    def get_or_create_knowledge_base(self, pdf_url: str):
        """Get existing knowledge base or create new one if not exists"""
        if pdf_url not in self.knowledge_bases:
            logger.info(f"Creating new knowledge base for URL: {pdf_url}")
            self.knowledge_bases[pdf_url] = self.create_knowledge_base(pdf_url)
        return self.knowledge_bases[pdf_url]

    def get_or_create_agents(self, pdf_url: str):
        """Get existing agents or create new ones if not exists"""
        if pdf_url not in self.agents:
            knowledge_base = self.get_or_create_knowledge_base(pdf_url)
            self.agents[pdf_url] = {
                "qa": self.setup_qa_agent(knowledge_base),
                "summary": self.setup_summary_agent(knowledge_base),
                "insight": self.setup_insight_agent(knowledge_base),
                "personalization": self.setup_personalization_agent(knowledge_base)
            }
        return self.agents[pdf_url]

class ReadingCompanionWorkflow:
    def __init__(self, db_url: str):
        self.reading_system = ReadingCompanionSystem(db_url=db_url)
        self.session_state = {}
        self.user_preferences = {}

    def process_book(self, pdf_url: str):
        """Get or create agents for the given PDF URL"""
        return self.reading_system.get_or_create_agents(pdf_url)

    def get_personalized_response(self, agent, query: str, user_id: str, 
                                interests: List[str] = None) -> Dict[str, Any]:
        """Get personalized responses based on user preferences"""
        if interests:
            self.user_preferences[user_id] = interests
        
        context = {
            "user_interests": self.user_preferences.get(user_id, []),
            "reading_progress": self.reading_system.reading_progress
        }
        
        response = self.get_response(agent, query, json.dumps(context))
        return {
            "content": response.content,
            "suggestions": self.reading_system.get_section_suggestions(
                self.user_preferences.get(user_id, [])
            )
        }

    def get_response(self, agent, query: str, context: str = None) -> RunResponse:
        input_text = query
        if context:
            input_text = f"Context: {context}\nQuery: {query}"
        
        # Use run() instead of chat()
        response = agent.run(input_text)
        return response