import streamlit as st
import pandas as pd
from pyairtable import Api 
from datetime import datetime

st.set_page_config(
    page_title="Claudio Eghosasere Enobas Ese - Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load current year
today = datetime.today().strftime("%Y")

# Load MaterializeCSS, Material Icons and Font Awesome libraries

# https://materializecss.com/
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">', unsafe_allow_html=True)
# https://materializecss.com/icons.html
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)
# https://fontawesome.com/start
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Add custom styles to improve the design
customStyle ="""
            <style type="text/css">
            /*Increase the size of the cards*/
            .card.large{
                height:550px!important;
            }
            /*Increase available content space*/
            .card.large .card-content{
                max-height:fit-content!important;
            }
            /* Increase the font size of Streamlit tabs*/
            button[data-baseweb="tab"] p{
                font-size:20px!important;
            }
            /* Remove default Streamlit header spacing */
            div[data-testid="stAppViewBlockContainer"]{
                padding-top:0px;
            }
            </style>
            """
# Load the styles
st.html(customStyle)

# Load the API Key
AIRTABLE_API_KEY = st.secrets.AIRTABLE_API_KEY # Create the token at this link https://airtable.com/create/tokens

# Select Airtable base id
AIRTABLE_BASE_ID='appjIL3JLyUSiFiyg'

# Create the Airtable object
api = Api(AIRTABLE_API_KEY)
# Load the tables
tblprofile = api.table(AIRTABLE_BASE_ID, 'profile')
tblprojects = api.table(AIRTABLE_BASE_ID, 'projects')
tblskills = api.table(AIRTABLE_BASE_ID, 'skills')
tblContacts = api.table(AIRTABLE_BASE_ID, 'contacts')

# Load the values retrieved from the tables
profile = tblprofile.all()[0]['fields']
name=profile['Name']
profileDescription=profile['Description']
profileTagline=profile['tagline']
linkedInLink=profile['linkedin']
xLink=profile['x']
githubLink=profile['github']
picture=profile['picture'][0]['url']

# Create the profile template with MaterializeCSS classes
# https://materializecss.com/
profileHTML=f"""
<div class="row">
<h1>{name} <span class="blue-text text-darken-3">Portfolio</span> </h1>
<h5>{profileTagline}</h5>
</div>
<div class="row">
    <div class="col s12 m12">
        <div class="card">
            <div class="card-content">
                <div class="row">                    
                    <div class="col s12 m2">
                        <img class="circle responsive-img" src="{picture}">
                    </div>
                        <div class="col s12 m10 ">
                            <span class="card-title">About me</span>
                            <p>{profileDescription}</p>
                            <div class="card-action">
                            <a href="https://www.linkedin.com/in/claudioenobas/" class="blue-text text-darken-3"><i class="fa-brands fa-linkedin fa-2xl"></i></a>
                            <a href="https://github.com/claudioen" class="blue-text text-darken-3"><i class="fa-brands fa-github fa-2xl"></i></a>
                            <a href="https://x.com/" class="blue-text text-darken-3"><i class="fa-brands fa-x-twitter fa-2xl"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
            """
# Display the generated HTML
st.html(profileHTML)

# Create the Streamlit tabs
tabSkils,tabPortfolio,tabContact =st.tabs(['My skills','My projects','Contact'])

# Display the Skills tab
with tabSkils:
    skills=""
    # Loop creating the Skills templates
    for skill in tblskills.all(sort=['-Level']):
        # st.write(skill['fields'])
        skill=skill['fields']
        skillName = skill['Name']
        skillDescription = skill['Notes']    
        skillLevel = skill['Level']
        skillStars=""
        # Create rating with stars
        for i in range(1,6):
            if i<=skillLevel:
                # Full star
                skillStars=skillStars+'<i class="material-icons">star</i>'
            else:
                # Empty star
                skillStars=skillStars+'<i class="material-icons">star_border</i>'
                
        skillYears = skill['startYear']   
        # Calculate years of experience
        skillExperience = int(today) -int(skillYears)
        # Skill card template
        skillHTML = f"""                    
                <div class="col s12 m4">
                    <div class="card small">
                        <div class="card-content">
                            <span class="card-title">{skillName}</span>
                            <p>{skillDescription}</p>
                        </div>
                        <div class="card-action">
                            <div class="col s12 m6">
                                <p>Level:<br/> {skillStars}</p>
                            </div>
                            <div class="col s12 m6">
                                <p fon>Since:<br/> {skillYears} - More than {skillExperience} years</p>
                            </div>
                        </div>
                    </div>
                </div>
                    """
        skills=skills+skillHTML
    skillsHTML=f"""
            <div class="row">            
                {skills}       
            </div>       
        """     
    # Display skills
    st.html(skillsHTML) 
with tabPortfolio:       
    projects=""
    skillsHTML=""
    knowledgeHTML=""
    # Loop creating the project templates
    for project in tblprojects.all():
        # st.write(skill['fields'])
        projectid= project['id']
        project=project["fields"]
        projectName = project['Name']        
        projectDescription = project['Description']    
        # Create the list of Skills and Knowledge
        projectSkils = project['skills']
        skillsHTML=[f'<div class="chip green lighten-4">{p}</div>' for p in projectSkils]
        skillsHTML="".join(skillsHTML)
        projectKnowledge = project['Knowledge']        
        knowledgeHTML=[f'<div class="chip blue lighten-4">{p}</div>' for p in projectKnowledge]
        knowledgeHTML="".join(knowledgeHTML)
        
        projectLink = project['link'] 
        projectImageUrl = project['image'][0]['url']        
        # Project card template
        projectHTML = f"""                    
                <div class="col s12 m6">
                    <div class="card large">                    
                        <div class="card-image" style="height:200px">
                            <a href="{projectLink}"><img src="{projectImageUrl}"></a>
                        </div>                        
                        <div class="card-content">
                            <span class="card-title">{projectName}</span>                                                        
                            <p>{projectDescription}</p>
                            <div class="row hide-on-small-only">
                            <div class="col s12 m6">
                            <h6>Knowledge:</h6>
                            {knowledgeHTML}
                            </div>
                            <div class="col s12 m6">
                            <h6>Skills:</h6>
                            {skillsHTML}
                            </div>
                            </div>
                        </div>  
                        <div class="card-action right-align">
                        <a href="{projectLink}" class="waves-effect waves-light btn-large white-text blue darken-3"><i class="material-icons left">open_in_new</i>View</a>                        
                        </div>                                               
                    </div>
                </div>
                    """
        projects=projects+projectHTML
    projectsHTML=f"""
            <div class="row">            
                {projects}       
            </div>       
        """     
    # Display projects
    st.html(projectsHTML)        
with tabContact:
    st.info("If you think I can help you with some of your projects or entrepreneurships, send me a message I'll contact you as soon as I can. I'm always glad to help")
    with st.container(border=True):
        parName = st.text_input("Your name")
        parEmail = st.text_input("Your email")
        parPhoneNumber = st.text_input("WhatsApp phone number, with country code")
        parNotes = st.text_area("What can I do for you")
        btnEnviar = st.button("Send",type="primary")
    if btnEnviar:
        # Create the contact record
        tblContacts.create({"Name":parName,"email":parEmail,"phoneNumber":parPhoneNumber,"Notes":parNotes})
        st.toast("Message sent")
st.markdown('<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>', unsafe_allow_html=True)
