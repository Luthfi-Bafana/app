import json
from helper_functions import llm
import pandas as pd


# Load the excel file as a dataframe
df = pd.read_excel('docs/Schemes.xlsx')

# converting the df into a dictionary where the elements in the first columns are the keys and the elements of the same row are the values
result = df.set_index(df.columns[0]).to_dict(orient='index')


def identify_financial_programs(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with queries from university students seeking out financial aid programmes. \
    The student query will be enclosed in
    the pair of {delimiter}.

    Decide if the query is relevant to any specific programmes
    in the Python dictionary below, which each key is a `financial aid programme`
    and the values are the following details of the 'financial aid programmes'
    1) School
    2) Student Type
    3) Scheme Type
    4) Eligibility
    5) Benefits and Award

    If there are any relevant programmes found, output the following information : a) `financial programme name' , b) Eligibility and c) the associated `Benefits and Awards` 
    for each relevant course found

    {result}

    If are no relevant courses are found, output the following : No relevant courses found.

    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    programmes_response = llm.get_completion_by_messages(messages)
    return programmes_response
    
'''
def get_course_details(list_of_relevant_category_n_course: list[dict]):
    course_names_list = []
    for x in list_of_relevant_category_n_course:
        course_names_list.append(x.get('course_name')) # x["course_name"]

    list_of_course_details = []
    for course_name in course_names_list:
        list_of_course_details.append(dict_of_courses.get(course_name))
    return list_of_course_details


def generate_response_based_on_course_details(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is asking about course, \
    understand the relevant course(s) from the following list.
    All available courses shown in the json data below:
    {product_details}

    Step 2:{delimiter} Use the information about the course to \
    generate the answer for the customer's query.
    You must only rely on the facts or information in the course information.
    Your response should be as detail as possible and \
    include information that is useful for customer to better understand the course.

    Step 3:{delimiter}: Answer the customer in a friendly tone.
    Make sure the statements are factually accurate.
    Your response should be comprehensive and informative to help the \
    the customers to make their decision.
    Complete with details such rating, pricing, and skills to be learnt.
    Use Neural Linguistic Programming to construct your response.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>

    Make sure to include {delimiter} to separate every step.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer


def process_user_message(user_input):
    delimiter = "```"

    # Process 1: If Courses are found, look them up
    category_n_course_name = identify_category_and_courses(user_input)
    print("category_n_course_name : ", category_n_course_name)

    # Process 2: Get the Course Details
    course_details = get_course_details(category_n_course_name)
    df = pd.DataFrame(course_details) # this converts course details list into a dataframe (challenge 3)

    # Process 3: Generate Response based on Course Details
    reply = generate_response_based_on_course_details(user_input, course_details)

    # Process 4: Append the response to the list of all messages
    return reply, df # df is for challenge 3
'''