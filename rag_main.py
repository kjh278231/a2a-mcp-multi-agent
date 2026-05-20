from rag_tutor_crew import EnglishTutorCrew, add_to_conversation


def main() -> None:
    """터미널 텍스트 대화형 영어 회화 튜터."""
    print("=" * 60)
    print("English Conversation Tutor (텍스트 모드)")
    print("영어로 자유롭게 대화해 보세요. 'exit', 'quit', '종료' 로 종료.")
    print("=" * 60)

    while True:
        try:
            user_message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSee you next time!")
            break

        if not user_message:
            continue
        if user_message.lower() in ("exit", "quit", "종료"):
            print("See you next time!")
            break

        # 최신 대화 기록이 포함된 크루를 동적으로 생성
        tutor_crew = EnglishTutorCrew()
        crew = tutor_crew.create_crew()
        result = crew.kickoff(inputs={"message": user_message})

        # 대화를 히스토리에 저장
        bot_response = result.raw
        add_to_conversation(user_message, bot_response)

        print(f"\nTutor: {bot_response}")


if __name__ == "__main__":
    main()
