import httpx

from app.config import settings


class APIClient:
    def __init__(self):
        self.base_url = settings.api_base_url.rstrip("/")

    async def create_user(self, telegram_id: int, username: str | None):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.base_url}/users/",
                json={"telegram_id": telegram_id, "username": username},
            )
            response.raise_for_status()
            return response.json()

    async def create_poll(self, owner_id: int, title: str, description: str):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.base_url}/polls/",
                json={
                    "owner_id": owner_id,
                    "title": title,
                    "description": description,
                    "is_active": True,
                },
            )
            response.raise_for_status()
            return response.json()

    async def create_question(
        self,
        poll_id: int,
        text: str,
        q_type: str,
        order: int,
        options_json: str | None = None,
    ):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.base_url}/questions/",
                json={
                    "poll_id": poll_id,
                    "text": text,
                    "type": q_type,
                    "order": order,
                    "options_json": options_json,
                },
            )
            response.raise_for_status()
            return response.json()

    async def user_polls(self, user_id: int):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.base_url}/polls/user/{user_id}")
            response.raise_for_status()
            return response.json()

    async def poll_questions(self, poll_id: int):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.base_url}/polls/{poll_id}/questions")
            response.raise_for_status()
            return response.json()

    async def submit_answer(self, user_id: int, question_id: int, answer: str):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.base_url}/answers/",
                json={"user_id": user_id, "question_id": question_id, "answer": answer},
            )
            return response

    async def poll_results(self, poll_id: int):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.base_url}/polls/{poll_id}/results")
            response.raise_for_status()
            return response.json()
