import os
from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from env import OPENAI_API_KEY
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

PDF_FILENAME = "29ESLConversationTopic.pdf"
PERSIST_DIR = os.path.join(".chroma", "esl_topics")

CHUNK_SIZE = 800  # 한 번에 잘라낼 텍스트의 최대 길이 (문자 수) : 문서를 너무 길게 넣으면 벡터 임베딩이 부정확해짐. 너무 짧게 나누면 문맥이 끊겨서 검색 시 정보 손실 발생.
CHUNK_OVERLAP = 100  # 인접 청크 간에 겹치는 텍스트 길이를 지정.
TOP_K = 4  # Retrieval 단계에서 검색할 청크 개수.
QA_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3


class ESLChromaRAGToolInput(BaseModel):
    # 사용자 질문을 받아 PDF 기반으로 응답을 생성
    question: str = Field(..., description="ESL 주제 PDF를 사용해 답변할 질문")


class ESLChromaRAGTool(BaseTool):
    name: str = "ESL_Chroma_RAG"
    description: str = (
        "Retrieves from '29 ESL Conversation Topics' PDF via ChromaDB and answers questions."
    )

    def _qa(self, question):
        #  인덱싱, 리트리버
        os.makedirs("DB", exist_ok=True)
        pdf_path = os.path.join("knowledge", "29ESLConversationTopic.pdf")

        # 기존 인덱스가 존재하는지?
        embeddings = OpenAIEmbeddings()
        try:
            has_index = bool(os.listdir("DB"))
        except FileNotFoundError:
            has_index = False
        if has_index:
            vectordb = Chroma(
                persist_directory="DB",
                embedding_function=embeddings,
            )
        else:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            # chunk
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            vectordb = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory="DB",
            )
        # =========================================================
        # RETRIEVAL (Post-Retrieval)
        # ---------------------------------------------------------
        # 사용자 질문 → 임베딩 → 유사 청크 검색(k=TOP_K)
        # → 검색된 청크를 LLM 입력으로 넣어 답변 생성
        # =========================================================
        retriever = vectordb.as_retriever(search_kwargs={"k": TOP_K})
        llm = ChatOpenAI(model=QA_MODEL, temperature=TEMPERATURE)

        # RetrievalQA: 검색 결과를 LLM과 결합해 답변 생성
        return RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=retriever
        ).run(question)

    # =========================================================
    # 실행 단계 (RAG 전체 호출)
    # ---------------------------------------------------------
    # 1. _ensure_qa()로 인덱스 확보
    # 2. 질문 수행 → 검색된 청크 기반 LLM 답변 생성
    # =========================================================
    def _run(self, question: str):
        try:
            return self._qa(question)
        except Exception as e:
            return f"Chroma RAG 사용 중 오류: {e}"
