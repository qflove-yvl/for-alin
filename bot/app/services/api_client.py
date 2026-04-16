import httpx

from app.config import settings


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(self):
        self.base_url = settings.api_base_url.rstrip("/")

    async def _request(self, method: str, path: str, *, json_body: dict | None = None):
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.request(method, url, json=json_body)
                response.raise_for_status()
                return response.json() if response.content else {}
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:300]
            raise APIClientError(f"API error {exc.response.status_code}: {detail}")
        except httpx.HTTPError as exc:
            raise APIClientError(f"Network error while calling API: {exc}")

    async def create_user(self, telegram_id: int, username: str | None):
        return await self._request(
            "POST",
            "/users/",
            json_body={"telegram_id": telegram_id, "username": username},
        )

    async def create_poll(self, owner_id: int, title: str, description: str):
        return await self._request(
            "POST",
            "/polls/",
            json_body={
                "owner_id": owner_id,
                "title": title,
                "description": description,
                "is_active": True,
            },
        )

    async def create_question(
        self,
        poll_id: int,
        text: str,
        q_type: str,
        order: int,
        options_json: str | None = None,
    ):
        return await self._request(
            "POST",
            "/questions/",
            json_body={
                "poll_id": poll_id,
                "text": text,
                "type": q_type,
                "order": order,
                "options_json": options_json,
            },
        )

    async def user_polls(self, user_id: int):
        return await self._request("GET", f"/polls/user/{user_id}")

    async def poll_questions(self, poll_id: int):
        return await self._request("GET", f"/polls/{poll_id}/questions")

    async def submit_answer(self, user_id: int, question_id: int, answer: str):
        return await self._request(
            "POST",
            "/answers/",
            json_body={"user_id": user_id, "question_id": question_id, "answer": answer},
        )

    async def poll_results(self, poll_id: int):
        return await self._request("GET", f"/polls/{poll_id}/results")
