import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import AadharWorkflow
from activities import Aadhar_Verification

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(
        client,
        task_queue="aadhar_queue",
        workflows=[AadharWorkflow],
        activities=[Aadhar_Verification().unpackPdf],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
