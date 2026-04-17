import httpx
import asyncio

WEBHOOK_URL ="https://webhook.site/bf024303-c832-42df-9c03-92329ab03461" 

async def send_webhook(payload: dict):
    
    retries = 3

    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(WEBHOOK_URL, json=payload)
                print("Sending webhook to:", WEBHOOK_URL)
                print("PAYLOAD:", payload)
                print("STATUS:", response.status_code)

                if response.status_code == 200:
                    print("Webhook sent successfully")
                    return

        except Exception as e:
            print(f"Attempt {attempt+1} failed")

        # exponential backoff
        await asyncio.sleep(2 ** attempt)   # 1s, 2s, 4s

    print("Webhook failed after retries")