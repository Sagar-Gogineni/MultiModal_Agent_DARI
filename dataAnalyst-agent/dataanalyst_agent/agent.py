from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
from dataanalyst_agent.retriever import query_engine 
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dataanalyst_agent.ingest import ingest_images
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

@tool
def mm_retriever_tool(query:str) -> str:
    """MultiModal Retriever"""
    response=query_engine(query_str=query)
    return response

tools=[mm_retriever_tool]
memory = InMemoryChatMessageHistory(session_id="test-session")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are DARI short for Data Analysis for Real-time Insights.\n
         Role: Friendly data scientist that specializes in reading data-heavy reports and extracting insights regarding the social media activity on a media brand space.\n
         Instructions:
         Evaluate if the query from the user is analytical in nature. If not, reply to the user politely and re-steer the conversation to be about analytics or follow up on analytics. Do not allow the conversation to diverge from these topics.\n
         If the question regards analytics or follow up on analytics, select an appropriately sized subgroup of charts and comments that are helpful to answer the query. Create a context data strucutre to be used in future analysis as a working dataset containing this narrower, more relevant, set of information.\n
         Formulate a plan to answer the query using the information at hand using agent scratchpad.\n
         Execute the plan from the point above.\n
         Judge if the analysis adequately answered the user query. \n
         If the answer is informative, reply to the user and ask for follow ups.\n
         Always access tools which provide you with latest context and data. Always Answer user queries soely on this data.
         Dont get too chatty.\n
         """ ),
        # First put the history
        ("placeholder", "{chat_history}"),
        # Then the new input
        ("human", "{input}"),
        # Finally the scratchpad
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "test-session"}}

# agent_executor.invoke({"input": query})
# print(agent_with_chat_history.invoke({"input": "give me an overview of the points where we're doing worse than in the last reporting period"},config)['output'])













# openai_api_key = os.getenv("OPENAI_API_KEY")

# template = """This is a conversation between a human and a bot:

# {chat_history}

# Write a summary of the conversation for {input}:
# """

# prompt = PromptTemplate(input_variables=["input", "chat_history"], template=template)
# memory = ConversationBufferMemory(memory_key="chat_history")

# prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
# suffix = """Begin!"

# {chat_history}
# Question: {input}
# {agent_scratchpad}"""





# prompt = StructuredChatAgent.create_prompt(
#     prefix=prefix,
#     tools=tools,
#     suffix=suffix,
#     input_variables=["input", "chat_history", "agent_scratchpad"],
# )

# llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

# llm_chain = LLMChain(llm=llm, prompt=prompt)
# agent = StructuredChatAgent(llm_chain=llm_chain, verbose=True, tools=tools)

# agent_chain = AgentExecutor.from_agent_and_tools(
#     agent=agent, verbose=True, memory=memory, tools=tools
# )

# Answering the first prompt requires usage of the Reddit search tool.
# rep=agent_chain.run(input="give me an overview of the points where we're doing worse than in the last reporting period")
# print(rep)