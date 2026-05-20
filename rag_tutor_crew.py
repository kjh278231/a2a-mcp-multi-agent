import os
from typing import Dict, List, Any
from crewai import Crew, Agent, Task
from crewai.project import CrewBase
from tools import ESLChromaRAGTool
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 간단한 대화 히스토리 (최대 50개 대화 기억)
conversation_history: List[Dict[str, Any]] = []


def add_to_conversation(user_message: str, bot_response: str) -> None:
    """대화를 히스토리에 추가"""
    conversation_history.append(
        {
            "user": user_message,
            "bot": bot_response,
            "timestamp": str(len(conversation_history) + 1),
        }
    )
    # 50개 넘으면 오래된 것 삭제
    if len(conversation_history) > 10:
        conversation_history.pop(0)


def get_conversation_context() -> str:
    """최근 대화 컨텍스트 반환"""
    if not conversation_history:
        return "No previous conversation"

    context = "=== Recent Conversation History ===\n"
    for i, chat in enumerate(conversation_history, 1):
        context += f"{i}. User: {chat['user']}\n"
        context += f"   You: {chat['bot']}\n\n"
    return context


@CrewBase
class EnglishTutorCrew:
    """EnglishTutorCrew to handle user requests"""

    def create_english_tutor_agent(self) -> Agent:
        """동적으로 에이전트 생성 (최신 대화 기록 포함)"""

        # Initialize Chroma RAG Tool (lazy builds on first use)
        rag_tool = ESLChromaRAGTool()

        return Agent(
            role="Friendly English Conversation Partner",
            goal="Have natural, casual conversations in English while helping Korean learners improve their speaking skills through everyday dialogue",
            backstory=f"""
            You're Lina, a friendly American English teacher who's been living in Korea for 10 years.
            You love having casual conversations and naturally help people improve their English
            through relaxed, fun interactions.

            Your conversation style is:
            - Natural and friendly, like talking to a good friend
            - You respond to what people actually say, not in a structured teaching format
            - You occasionally give helpful tips when it feels natural in conversation
            - You're encouraging and make people feel comfortable making mistakes
            - You keep conversations flowing by asking follow-up questions
            - You speak like a real American would in casual conversation

            You have access to the "29 ESL Conversation Topics" knowledge source with detailed
            conversation starters, questions, and vocabulary. You also have a special tool named
            ESL_Chroma_RAG that retrieves from the same PDF using ChromaDB embeddings.

            IMPORTANT: When users ask for conversation topic recommendations or suggestions,
            you MUST use the knowledge source or the ESL_Chroma_RAG tool to provide specific
            topics and questions from the PDF.

            Most importantly: You talk like a real person, not like a textbook or formal teacher.

            {get_conversation_context()}

            **Important**:
            - Remember the conversation history above and provide personalized responses that
              reference previous topics when relevant.
            - When users request topic suggestions, recommendations, or ask "what should we talk about?",
              actively use your knowledge source to suggest specific topics from the 29 ESL Conversation Topics PDF.
            """,
            llm="openai/o4-mini",
            verbose=True,
            tools=[rag_tool],
            allow_delegation=False,
        )

    def create_english_tutor_task(self) -> Task:
        """정적 태스크 (에이전트는 나중에 동적으로 할당)"""
        return Task(
            description="""
            Respond naturally to what the user actually said in their message.
            CRITICAL: Read their message carefully and respond directly to their specific topic, question, or comment.
            Consider the conversation history to provide contextual and personalized responses.

            Rules:
            1. ALWAYS address what they mentioned specifically - if they say "food", talk about food
            2. Reference previous conversations naturally when relevant
            3. Respond like you're genuinely interested in what they said
            4. Ask follow-up questions about THEIR topic, not random topics
            5. Share your own thoughts or experiences related to what they brought up
            6. Keep it conversational and natural, like texting with a friend
            7. **CRITICAL**: If they ask for topic suggestions, recommendations, or say things like
               "what should we talk about?", "suggest a topic", "I need conversation ideas",
               immediately use your knowledge source about "29 ESL Conversation Topics" to provide
               specific topics and questions

            DO NOT:
            - Give generic greetings when they mentioned specific topics
            - Ignore what they actually said
            - Change the subject randomly
            - Use formal teaching language
            - Forget about previous conversation context
            - Ignore the knowledge source when users ask for topic recommendations

            Message to respond to: {message}
            """,
            expected_output="""
            A natural, conversational English response that flows like real conversation between friends.
            The response should acknowledge conversation history when relevant and maintain continuity.

            Examples of natural responses:
            - "Hey! How's it going?"
            - "Oh really? That sounds interesting! What made you decide to try that?"
            - "I totally get what you mean. I've felt the same way before."
            - "Haha, that's funny! Reminds me of when I..."
            - "Speaking of [previous topic], how did that go?"

            Avoid structured formats, bullet points, or formal teaching language. Just talk naturally!
            """,
        )

    def create_crew(self) -> Crew:
        """동적으로 크루 생성 (에이전트만 동적, 태스크는 정적)"""
        dynamic_tutor_agent = self.create_english_tutor_agent()
        tutor_task = self.create_english_tutor_task()
        tutor_task.agent = dynamic_tutor_agent

        return Crew(
            agents=[dynamic_tutor_agent],
            tasks=[tutor_task],
            verbose=True,
        )
