import json
from helper_functions import llm
import pandas as pd


# Load the excel file as a dataframe
df = pd.read_excel('docs/Schemes.xlsx')

# converting the df into a dictionary where the elements in the first columns are the keys and the elements of the same row are the values
result = df.set_index(df.columns[0]).to_dict(orient='index')

def filter_programmes(df, school, scheme, student_type):
    # Filter the dataframe to include only rows where the programmes parameters match the school, scheme and student_type of the student. These values are inputted through the streamlit widgets
    df_filtered = df[(df['School'] == school) &
                     (df['Student Type'] == student_type) &
                     (df['Scheme Type'] == scheme)]
    return df_filtered

# checks if the student's per capita income matches the eligibility criteria of a financial programme. If it matches, return 'Valid'. Else, return 'Invalid'
def check_programme_eligibility(eligibility_criteria, pci):
    delimiter = "####"

    # Check if the eligibility criteria includes PCI
    if 'PCI' not in eligibility_criteria:
        return 'Valid'  # If 'PCI' is not present, it's valid

    # Prepare the system message
    system_message = f"""
    Your role is to determine if the eligibility criteria is valid based on the provided Per Capita Income (PCI).
    
    Here are the steps you should follow:
    1) If the term 'PCI' does not appear in the eligibility criteria, the eligibility is valid.
    2) If the term 'PCI' appears:
       a) Identify the conditions mentioned (e.g., smaller than, greater than, lesser than or equal to).
       b) Check if the PCI fits within the criteria defined in the eligibility criteria.

    Give me only 1 word as output. Either 
    1) Valid
    2) Invalid    
    
    Example eligibility criteria and decisions:
    
    eligibility criteria: Financially needy undergraduates
    Output: Valid

    eligibility criteria: Students with Per Capita Income (PCI) smaller than $2,500 
    PCI: 2000
    Output: Valid

    eligibility criteria: Students with Per Capita Income (PCI) greater than $750 and smaller than $1,100
    PCI: 1500
    Output: Invalid

    eligibility criteria: International Students with Per Capita Income (PCI) smaller than S$1,200
    PCI: 1000
    Output: Valid

    eligibility criteria: Singapore Citizens with Per Capita Income (PCI) lesser than or equal to S$1,900
    PCI: 2000
    Output: Invalid

    eligibility criteria: For students with PSEA funds in their own/siblings' account.
    Output: Valid
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{eligibility_criteria}{delimiter}"},
        {'role': 'user', 
         'content': f"PCI: {pci}"}
    ]

    # Call to the LLM to determine the eligibility
    ans = llm.get_completion_by_messages(messages)
    
    # Check if the output is empty or doesn't make sense
    if not ans.strip() or "please provide" in ans.lower():
        return 'Valid'  # If no relevant criteria were provided, return Valid

    return ans

# filters the dataframe from the above filter_programmes further by filtering for programmes which match the financial status of the student using the check_programme_eligibility function
def filter_further(df, pci):
    # Apply the check_programme_eligibility function row-wise and filter for 'Valid' results
    df_further = df[df['Eligibility'].apply(lambda eligibility: check_programme_eligibility(eligibility, pci) == 'Valid')]
    return df_further

# this is for the 2nd use case where a user can ask for general information about financial aid programmes.
def give_info(df, user_query): 
    delimiter = "####"

    system_message = f"""
    You will be provided with a user query enclosed by {delimiter} below on financial aid programmes on information about various financial aid programmes.

    You will be able to obtain the information needed from the dataframe {df}. Structure your answer as follows.

    1) Determine the programme category that would interest the user
    2) List the financial aid programmes from {df} that would be most relevant to the user
    3) Provide several ways how the user would be able to benefit from the benefits of the financial aid programmes. Be as creative as you want
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_query}{delimiter}"},
    ]
    
    ans = llm.get_completion_by_messages(messages)
    return ans


    



