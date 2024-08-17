import os
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event
from llama_index.llms.openai import OpenAI
import asyncio


from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)

# `pip install llama-index-llms-openai` if you don't already have it
from llama_index.llms.openai import OpenAI

class JokeEvent(Event):
    joke: str


class JokeFlow(Workflow):
    llm = OpenAI("gpt-4o-mini")

    @step()
    async def generate_joke(self, ev: StartEvent) -> JokeEvent:

        prompt = f"Write a story for a SQL murder mystery game."
        response = await self.llm.acomplete(prompt)

        print('original joke: ', response)
        st.write(response)

        return JokeEvent(joke=str(response))

    @step()
    async def critique_joke(self, ev: JokeEvent) -> StopEvent:
        joke = ev.joke

        prompt = f"Using this SQL murder mystery game, come up with db tables needed for the game: {joke}"
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=str(response))


async def main():
    w = JokeFlow(timeout=60, verbose=False)
    result = await w.run()
    print(str(result))
    st.write(result)


run = st.button('run')

if run:
    import asyncio

    asyncio.run(main())
