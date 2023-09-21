# with a deployment, if not writing out to absolute file path
# or saving to Cloud or Docker volume,
# output will be written to temporary directory and deleted
# so we'll just persist the result to storage

import httpx
from prefect import flow, task, get_run_logger


@task
def fetch_cat_fact():
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]


@task(persist_result=True)
def formatting(fact: str):
    return fact.title()


@flow
def pipe(key: str):
    logger = get_run_logger()
    logger.info("Hi {key}")
    fact = fetch_cat_fact()
    formatted_fact = formatting(fact)


if __name__ == "__main__":
    pipe(key="original_key")
