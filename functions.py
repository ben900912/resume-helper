import os
import openai
import keys
from pathlib import Path
from pprint import pprint
import requests
from affinda import AffindaAPI, TokenCredential
from affinda.models import WorkspaceCreate, CollectionCreate
import json
from io import BytesIO

openai.api_key = keys.openai_key

def get_respond(input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input,
        max_tokens=100,
        temperature=0,
        n = 1 
        )
    return (response.choices[0].text) 

def resume_ph(file, name_in):
# First get the organisation, by default your first one will have free credits
    token = keys.token
   

    credential = TokenCredential(token=token)
    client = AffindaAPI(credential=credential)
    my_organisation = client.get_all_organizations()[0]

# And within that organisation, create a workspace, for example for Recruitment:
    workspace_body = WorkspaceCreate(
        organization=my_organisation.identifier,
        name= name_in, #change this everytime
    )
    recruitment_workspace = client.create_workspace(body=workspace_body)

    # Finally, create a collection that will contain our uploaded documents, for example resumes, by selecting the
    # appropriate extractor
    collection_body = CollectionCreate(
        name= name_in, workspace=recruitment_workspace.identifier, extractor="resume"
    )
    resume_collection = client.create_collection(collection_body)

    # Now we can upload a resume for parsing


    resume = client.create_document(file= file, collection=resume_collection.identifier)

    resume_dict = resume.as_dict()
    job = resume_dict['data']['profession']
    location = resume_dict['data']["location"]['city']
    cat = resume_dict['data']["education"][0]['accreditation']['education']
    return [job, location, cat]
    
#print(get_respond("define beach"))

def get_image(input):
    image = openai.Image.create(
    prompt=input,
    n=2,
    size="1024x1024"
    )
    print(image['data'][0]['url'])

#----------------------------------------------------------resume phrase--------------------------------------------------------------------------


#--------------------------------------------------job string-------------------------------------------------------------------------

def job_search(query, date_posted, employment_types, numpages):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {"query":query,"num_pages": numpages,"date_posted":date_posted,"employment_types":employment_types, "num_pages":numpages}

    headers = {
        'X-RapidAPI-Key': keys.rapid,
        'X-RapidAPI-Host': 'jsearch.p.rapidapi.com'
    }
    job_list = []
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    job_list = data['data']    
    return job_list


# with open("job_results.json", "w") as fp:
#     fp.write(json.dumps(job_search(query = 'electrical engineer', date_posted = 'all', employment_types = 'fulltime', numpages = 1), indent=2))
