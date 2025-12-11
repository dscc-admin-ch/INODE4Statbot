import time
import sys
import os
from sqlalchemyWrapper import (
    schema_db_postgres_statbot_zhaw
)
from few_shot_prompts_statbot import (
    generate_sql_in_context_learning_similar_shots, 
    few_shot_template_baby_names, 
    few_shot_template_divorces_duration_of_marriage_citizenship_categories,
    few_shot_template_stock_vehicles,
    few_shot_template_divorces_duration_of_marriage_age_classes,
    few_shot_template_marriage_citizenship,
    few_shot_template_resident_population_birthplace_citizenship_type,
    zero_shot_template
)
from langchain import LLMChain
import tiktoken
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI


def find_template(table_name):
    
    if table_name == "baby_names_favorite_firstname":
        return few_shot_template_baby_names()
    elif table_name == "divorces_duration_of_marriage_citizenship_categories":
        return few_shot_template_divorces_duration_of_marriage_citizenship_categories()
    elif table_name == "stock_vehicles":
        return few_shot_template_stock_vehicles()
    elif table_name == "divorces_duration_of_marriage_age_classes":
        return few_shot_template_divorces_duration_of_marriage_age_classes()
    elif table_name == "marriage_citizenship":
        return few_shot_template_marriage_citizenship()
    elif table_name == "resident_population_birthplace_citizenship_type":
        return few_shot_template_resident_population_birthplace_citizenship_type()
    else:
        return zero_shot_template()



def query_engineering_and_call(question, table_name, qry_id):

    sys.stderr.write(f"inside query_engineering_and_call" + "/n")
    
    prompt_template = generate_sql_in_context_learning_similar_shots(question, table_name)

    # For testing purposes
    # prompt_template = zero_shot_template()

    model_name = os.environ["MODEL_NAME"]
    model_path = os.environ["MODEL_PATH"]

    inference_server_url = os.environ["INFERENCE_SERVER_URL"]
    deployed_llm_token = os.environ["DEPLOYED_LLM_TOKEN"]

    llm = ChatOpenAI(
        model=model_path + model_name,
        openai_api_key=deployed_llm_token,
        openai_api_base=inference_server_url,
        max_tokens=1500,
        n=1,
        stream=False,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        temperature=0.0
    )

    # llm = ChatOpenAI(
    #     model="/root/.cache/huggingface/" + model_name,
    #     openai_api_key="EMPTY",
    #     openai_api_base=inference_server_url,
    #     max_tokens=1500,
    #     n = 1,
    #     stream = False,
    #     top_p = 1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0,
    #     temperature=0.0
    # )

    tic = time.perf_counter()
    
    llm_chain = prompt_template | llm
    sql = None

    ddl = schema_db_postgres_statbot_zhaw(include_tables=['spatial_unit', table_name],
                             sample_number=5)

    llm_inputs = {
        "input": question,
        "table_info": ddl,
    }

    sys.stderr.write(f"llm_inputs: {llm_inputs}\n")

    prompt_strings = prompt_template.format(input = question, table_info = ddl)
    sys.stderr.write(f"Prompt_string: {prompt_strings}\n")

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
    
    # time 
    toc = time.perf_counter()

    num_tokens = sql.response_metadata['token_usage']['total_tokens']
    sql_response = sql.content
    
    process_time = toc-tic
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
