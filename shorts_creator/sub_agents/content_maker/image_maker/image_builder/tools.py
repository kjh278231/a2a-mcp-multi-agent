import base64
from openai import AsyncOpenAI
from google.genai import types
from google.adk.tools.tool_context import ToolContext


async def generate_images(tool_context: ToolContext):
    """
    OpenAI의 gpt-image-1 모델을 사용하여 각 장면에 대한 이미지를 생성합니다.
    세로형 이미지를 생성하며, 이미 생성된 이미지는 재사용합니다.

    Args:
        tool_context: 아티팩트를 조회하고 저장하기 위한 ToolContext 객체.

    Returns:
        생성된 모든 이미지 파일의 정보가 포함된 딕셔너리.
    """
    prompt_builder_output = tool_context.state.get("prompt_builder_output")
    opt_prompts = prompt_builder_output.get("opt_prompts")

    existing_artifacts = await tool_context.list_artifacts()

    client = AsyncOpenAI()
    image_results = []

    for prompt in opt_prompts:
        scene_id = prompt.get("scene_id")
        enhanced_prompt = prompt.get("enhanced_prompt")
        filename = f"scene_{scene_id}_image.jpg"

        if filename in existing_artifacts:
            image_results.append(
                {
                    "scene_id": scene_id,
                    "filename": filename,
                }
            )
            continue

        response = await client.images.generate(
            model="gpt-image-2",
            prompt=enhanced_prompt,
            size="1024x1536",
        )

        image_byte_data = base64.b64decode(response.data[0].b64_json)

        artifact = types.Part(
            inline_data=types.Blob(
                mime_type="image/png",
                data=image_byte_data,
            )
        )

        await tool_context.save_artifact(
            filename=filename,
            artifact=artifact,
        )

        image_results.append(
            {
                "scene_id": scene_id,
                "filename": filename,
            }
        )

    return {
        "success": True,
        "image_results": image_results,
        "total_images": len(image_results),
    }
