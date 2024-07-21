from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ADD "estimated_days_to_complete" INT NOT NULL;
        ALTER TABLE "task" ADD "actual_days_to_complete" INT;
        ALTER TABLE "task" ADD "hours_spent" INT;
        ALTER TABLE "task" ADD "employee_id" INT;
        ALTER TABLE "task" DROP COLUMN "time_complete_in_days";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ADD "time_complete_in_days" INT;
        ALTER TABLE "task" DROP COLUMN "estimated_days_to_complete";
        ALTER TABLE "task" DROP COLUMN "actual_days_to_complete";
        ALTER TABLE "task" DROP COLUMN "hours_spent";
        ALTER TABLE "task" DROP COLUMN "employee_id";"""
