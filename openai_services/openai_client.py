from dotenv import load_dotenv
from openai import APIError, OpenAI, types
from aiogram.dispatcher.storage import FSMContextProxy


load_dotenv()

client = OpenAI()


async def send_report_to_ai(
    data: FSMContextProxy, recursed: bool = False
) -> types.chat.chat_completion_message.ChatCompletionMessage:
    report = create_report_from_json_data(data)
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ти повинен аналізувати звіт та відповідати, що ти думаеш",
                },
                {
                    "role": "user",
                    "content": report,
                },
            ],
        )
        return completion.choices[0].message.content
    except APIError:
        # Handle API error, e.g. retry or log
        if recursed:
            return "Some problems on OpenAI side"
        else:
            return send_report_to_ai(data=data, recursed=True)
    except Exception as e:
        print("some problems with OpenAI: " + str(e))


def create_report_from_json_data(data: FSMContextProxy) -> str:
    try:
        report = data["choosing_location"]
        for i in range(1, 6):
            report += f"\nПункт {i} - {data[f'checklist_{i}']['comment']}"
            if data[f"checklist_{i}"]["file_path"]:
                report += f", шлях до зображення: {data[f'checklist_{i}']['file_path']}"
        return report
    except KeyError:
        print("report key error")
        return "Помилка у зібраних даних"
    except Exception as e:
        print(f"Error: {e}")
        return "Помилка обробки даних"
