import time

from ollama import chat

MODEL = "qwen3:8b"

# 대화 기록 (멀티턴 유지를 위해 messages 리스트에 계속 누적)
messages = [{"role": "system", "content": "당신은 친절한 한국어 AI 어시스턴트입니다."}]

print("준비 완료! ('exit' 입력 시 종료)\n")

while True:
    user_input = input("나> ").strip()

    if user_input.lower() in ("exit", "quit"):
        break
    if not user_input:
        continue

    # 사용자 메시지 추가
    messages.append({"role": "user", "content": user_input})

    # Ollama 서버에 추론 요청
    started_at = time.perf_counter()
    response = chat(
        model=MODEL,
        messages=messages,
        think=False,  # 사고과정 출력 끔 (지원 모델만 적용)
    )
    elapsed_seconds = time.perf_counter() - started_at
    reply = response.message.content.strip()

    # 응답 기록 및 출력
    messages.append({"role": "assistant", "content": reply})
    print(f"AI> {reply}")
    print(f"걸린 시간: {elapsed_seconds:.2f}초\n")
