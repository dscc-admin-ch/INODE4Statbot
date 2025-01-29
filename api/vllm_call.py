import time
import sys
import os
from sqlalchemyWrapper import *
#from langchain import OpenAI
from few_shot_prompts_statbot import *
from langchain import LLMChain
import tiktoken
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    # encoding = tiktoken.encoding_for_model(encoding_name)

    # implement an easy way to count token
    num_tokens = len(string.split())
    return num_tokens

def find_template(table_name):
    
    if table_name=="baby_names_favorite_firstname":
        return few_shot_template_baby_names()
    elif table_name =="divorces_duration_of_marriage_citizenship_categories":
        return few_shot_template_divorces_duration_of_marriage_citizenship_categories()
    elif table_name =="stock_vehicles":
        return few_shot_template_stock_vehicles()
    elif table_name =="divorces_duration_of_marriage_age_classes":
        return few_shot_template_divorces_duration_of_marriage_age_classes()
    elif table_name == "marriage_citizenship":
        return few_shot_template_marriage_citizenship()
    elif table_name =="resident_population_birthplace_citizenship_type":
        return few_shot_template_resident_population_birthplace_citizenship_type()
    else:
        return zero_shot_template()
    
    


def query_engineering_and_call(question, table_name, qry_id):
    
    prompt_template = find_template(table_name)

    model_name = os.environ["MODEL_NAME"]

    inference_server_url = os.environ["INFERENCE_SERVER_URL"]

    llm = ChatOpenAI(
        model="/root/.cache/huggingface/" + model_name,
        openai_api_key="EMPTY",
        openai_api_base=inference_server_url,
        max_tokens=1500,
        n = 1,
        stream = False,
        top_p = 1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        temperature=0.0
    )

    tic = time.perf_counter()
    # llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_chain = prompt_template | llm
    sql = None

    ddl = schema_db_postgres_statbot_zhaw(include_tables=['spatial_unit', table_name],
                             sample_number=5)

    llm_inputs = {
        "input": question,
        # "top_k": args.sample_rows,
        "table_info": ddl,
    }

    sys.stderr.write(f"llm_inputs: {llm_inputs}\n")

    prompt_strings = prompt_template.format(input = question, table_info = ddl)
    sys.stderr.write(f"Prompt_string: {prompt_strings}\n")

    # num_tokens = len(f"{llm_inputs}".split())

    # prompts = llm_chain.prep_prompts([llm_inputs])
    # sys.stderr.write(f"Prompts: {prompts}\n")
    # prompt_strings = [p.to_string() for p in prompts[0]]
    # sys.stderr.write(f"Prompt_string: {prompt_strings}\n")

    # check the length:
    # Write function to take string input and return number of tokens
    # num_tokens = num_tokens_from_string(prompt_strings[0], model_name)

    sys.stderr.write(f"Starting  generation:\n")
    while sql is None:
        try:
            # sql = llm_chain.run(**llm_inputs)
            sql = llm_chain.invoke(llm_inputs)
            sys.stderr.write(f"Question: {question}\n")
            sys.stderr.write(f"sql: {sql}\n")
        except Exception as e:
            sys.stderr.write(str(e))
            time.sleep(3)
            pass
    ## time ###
    toc = time.perf_counter()

    num_tokens = sql.response_metadata['token_usage']['total_tokens']
    sql_response = sql.content
    
    process_time=toc-tic
    print(f"Process Time= {process_time:0.4f} second")
    r = {"message": {
        "db_id": table_name,
        "id": qry_id,
        "generated_query": sql_response.replace("\n", " ").replace("\n\n", " ").replace(" ", " ").replace("  ", " "),
        "prompt": prompt_strings,
        "question": question,
        "time": process_time,
        "num_tokens": num_tokens,
    }}

    return r




# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    open_ai_call(question="Give me the babay names in canton zurich 0n 2020",table_name="baby_names_favorite_firstname")

