from temporalio import workflow
from datetime import timedelta
from activities import Aadhar_Verification
from temporalio.common import RetryPolicy

@workflow.defn
class AadharWorkflow:
    @workflow.run
    async def run(self, data) -> str:
        retryPolicy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=1)
        )
        
        unpackPdf = await workflow.execute_activity(
            Aadhar_Verification.unpackPdf,
            data,
            schedule_to_close_timeout=timedelta(seconds=10),
            retry_policy=retryPolicy
        )
        result = f'Pdf unpacked successfully and saved to {unpackPdf}'
        
        return result
        