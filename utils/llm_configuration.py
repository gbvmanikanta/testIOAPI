import os
from datetime import datetime

from langchain.chat_models import ChatOpenAI
import config

llm_model = "gpt-4o-mini"
temperature = 0.5
benchmark_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")

llm = ChatOpenAI(model=llm_model, openai_api_key=config.OPENAI_API_KEY, temperature=0.5, top_p=0.9)
