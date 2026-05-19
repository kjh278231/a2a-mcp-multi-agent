def split_message(text: str, max_length: int) -> list[str]:
    """text를 max_length 이하의 여러 조각으로 나눕니다."""
    if max_length <= 0:
        raise ValueError("max_length는 1 이상이어야 합니다.")

    if text == "":
        return []

    result: list[str] = []
    current = ""

    # 줄바꿈을 가장 우선하는 분할 기준으로 사용합니다.
    for line in text.split("\n"):
        # 한 줄이 max_length보다 길면 먼저 강제로 잘라냅니다.
        line_parts = [
            line[index:index + max_length]
            for index in range(0, len(line), max_length)
        ] or [""]

        for part in line_parts:
            if current == "":
                current = part
                continue

            # 줄 단위로 묶을 수 있으면 줄바꿈을 보존해서 현재 조각에 추가합니다.
            candidate = current + "\n" + part
            if len(candidate) <= max_length:
                current = candidate
            else:
                result.append(current)
                current = part

    if current != "":
        result.append(current)

    return result


def test_short_text():
    text = "짧은 텍스트입니다."

    result = split_message(text, 30)

    assert result == ["짧은 텍스트입니다."]


def test_exact_max_length_text():
    text = "a" * 30

    result = split_message(text, 30)

    assert result == ["a" * 30]


def test_split_by_newline():
    text = "aaaaaaaaaaaaaa\nbbbbbbbbbbbbbb\ncccccccccccccc"

    result = split_message(text, 30)

    assert result == ["aaaaaaaaaaaaaa\nbbbbbbbbbbbbbb", "cccccccccccccc"]


def test_force_split_long_text_without_newline():
    text = "a" * 75

    result = split_message(text, 30)

    assert result == ["a" * 30, "a" * 30, "a" * 15]


def test_mixed_newline_and_force_split():
    text = "짧은 줄\n" + ("b" * 65) + "\n마지막 줄"

    result = split_message(text, 30)

    assert result == ["짧은 줄", "b" * 30, "b" * 30, "b" * 5 + "\n마지막 줄"]


def test_empty_string():
    text = ""

    result = split_message(text, 30)

    assert result == []


if __name__ == "__main__":
    test_short_text()
    test_exact_max_length_text()
    test_split_by_newline()
    test_force_split_long_text_without_newline()
    test_mixed_newline_and_force_split()
    test_empty_string()

    print("모든 테스트를 통과했습니다~")
