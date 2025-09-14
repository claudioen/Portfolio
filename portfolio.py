import streamlit as st
import pandas as pd
from pyairtable import Api
from datetime import datetime

st.set_page_config(
    page_title="Claudio E. Enobas Ese - Portfolio",
    page_icon="👨🏾‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None,
    },
)

# fallback "hard" via CSS to hide items
HIDE_UI = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(HIDE_UI, unsafe_allow_html=True)

# Load current year
today = datetime.today().strftime("%Y")

# Load MaterializeCSS, Material Icons and Font Awesome libraries
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">', unsafe_allow_html=True)
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Base custom styles (structure/spacing)
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
st.html(customStyle)

# ===== Theme-aware accents (use Streamlit theme.primaryColor) =====
def hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join([c*2 for c in h])
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return r, g, b
    except Exception:
        return 21, 101, 192  # fallback to #1565C0

primary_hex = st.get_option("theme.primaryColor") or "#1565C0"
pr, pg, pb = hex_to_rgb(primary_hex)

theme_css = f"""
<style>
  /* Buttons that used to be 'orange darken-3' or 'blue darken-3' now follow the theme primary */
  .btn.orange.darken-3, .btn-large.orange.darken-3,
  .btn.blue.darken-3, .btn-large.blue.darken-3 {{
    background-color: {primary_hex} !important;
  }}

  /* Links that used 'orange-text text-darken-3' now follow the theme primary */
  .orange-text.text-darken-3, .blue-text.text-darken-3 {{
    color: {primary_hex} !important;
  }}

  /* Chips with orange/blue lighten-4 use a soft alpha of the primary */
  .chip.orange.lighten-4, .chip.blue.lighten-4 {{
    background-color: rgba({pr},{pg},{pb}, 0.14) !important;
  }}

  /* Timeline dot follows the primary */
  .timeline-dot {{
    background: {primary_hex};
    box-shadow: 0 0 0 3px rgba({pr},{pg},{pb}, 0.10) inset;
  }}

  /* Make sure icons inherit current text color in both modes */
  .card .card-title, .card .material-icons, .card .fa {{
    color: inherit;
  }}
</style>
"""
st.html(theme_css)

# Load the API Key
AIRTABLE_API_KEY = st.secrets.AIRTABLE_API_KEY  # Create the token at https://airtable.com/create/tokens

# Select Airtable base id
AIRTABLE_BASE_ID='appjIL3JLyUSiFiyg'

# Create the Airtable object
api = Api(AIRTABLE_API_KEY)
# Load the tables
tblprofile = api.table(AIRTABLE_BASE_ID, 'profile')
tblprojects = api.table(AIRTABLE_BASE_ID, 'projects')
tblskills = api.table(AIRTABLE_BASE_ID, 'skills')
tblContacts = api.table(AIRTABLE_BASE_ID, 'contacts')
tblexperience = api.table(AIRTABLE_BASE_ID, 'experience')

# Load the values retrieved from the tables
profile = tblprofile.all()[0]['fields']
name=profile['Name']
profileDescription=profile['Description']
profileTagline=profile['tagline']
linkedInLink=profile['linkedin']
emailLink=profile['email']
githubLink=profile['github']
picture=profile['picture'][0]['url']

# Try to read a CV attachment or a direct URL from the profile
cvUrl = ''
cv_att = profile.get('cv') or profile.get('CV') or profile.get('resume')
if isinstance(cv_att, list) and cv_att:
    cvUrl = cv_att[0].get('url', '')
else:
    cvUrl = profile.get('cvUrl', '')

# Create the profile template with MaterializeCSS classes
profileHTML=f"""
<div class="row">
<h1>{name} <span class="orange-text text-darken-3">Portfolio</span> </h1>
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
                                <a target="_blank" rel="noopener noreferrer" href="https://www.linkedin.com/in/claudioenobas/" class="orange-text text-darken-3"><i class="fa-brands fa-linkedin fa-2xl"></i></a>
                                <a target="_blank" rel="noopener noreferrer" href="https://github.com/claudioen" class="orange-text text-darken-3"><i class="fa-brands fa-github fa-2xl"></i></a>
                                <a href="mailto:claudioenobas@gmail.com" class="orange-text text-darken-3"><i class="fa fa-envelope fa-2xl"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
            """
st.html(profileHTML)

# Create the Streamlit tabs
tabExperience,tabSkils,tabPortfolio,tabContact = st.tabs(['Experience','Skills','Projects','Contact'])

# Display the Experience tab
with tabExperience:
    # Optional CV download button (keeps Materialize look)
    if cvUrl:
        cv_btn_html = f'''
        <div class="row">
          <div class="col s12 right-align">
            <a href="{cvUrl}" class="waves-effect waves-light btn-large white-text orange darken-3" target="_blank" rel="noopener">
              <i class="material-icons left">file_download</i>Download CV
            </a>
          </div>
        </div>
        '''
        st.html(cv_btn_html)

    # View switch: Timeline or Cards
    view_mode = st.selectbox("View", ["Timeline", "Cards"], index=0)

    # Fetch records (sorted: most recent first)
    records = tblexperience.all(sort=['-startYear'])  # or '-startDate'

    # Reusable chips builder
    def chips_html(values):
        if not values:
            return ""
        return "".join(f'<div class="chip green lighten-4">{v}</div>' for v in values)

    # Timeline CSS (primary color injected above in theme_css)
    tl_css = """
    <style>
      .timeline { position: relative; margin: 8px 0 16px 0; padding-left: 28px; }
      .timeline:before { content:""; position:absolute; left:12px; top:0; bottom:0; width:2px; background:#e0e0e0; }
      .timeline-item { position:relative; margin-bottom:18px; }
      .timeline-dot { position:absolute; left:6px; top:8px; width:12px; height:12px; border-radius:50%; }
      .timeline-card { margin-left:8px; }
      .timeline-meta { font-size:0.95rem; color:#757575; margin-bottom:6px; }
      .timeline-logo { height:56px; max-height:56px; object-fit:contain; }
      .timeline .card.small { min-height:auto; }
      @media (min-width: 992px) {
        .timeline .card-content { padding-bottom:10px; }
      }
    </style>
    """

    if view_mode == "Timeline":
        st.html(tl_css)  # inject timeline CSS once

        tl_html = '<div class="timeline">'
        for rec in records:
            f = rec.get('fields', {})
            role = f.get('Role', '')
            company = f.get('Company', '')
            location = f.get('Location', '')
            start = f.get('startYear') or f.get('startDate', '')
            end = f.get('endYear') or f.get('endDate') or 'Present'
            desc = f.get('Description', '')
            techs = f.get('Technologies') or f.get('Skills') or []

            companyLink = f.get('link_company', '')
            companyImageList = f.get('image_company') or []
            companyImageUrl = companyImageList[0]['url'] if companyImageList else ''

            # Safe logo HTML (clickable if link available)
            if companyImageUrl:
                logo_html = f'<img class="timeline-logo" src="{companyImageUrl}">'
                if companyLink:
                    logo_html = f'<a href="{companyLink}" target="_blank" rel="noopener">{logo_html}</a>'
            else:
                logo_html = ""

            tl_html += f"""
            <div class="timeline-item">
              <span class="timeline-dot"></span>
              <div class="timeline-card">
                <div class="card small">
                  <div class="card-content">
                    <div class="row" style="margin-bottom:0;">
                      <div class="col s12 m2">{logo_html}</div>
                      <div class="col s12 m10">
                        <span class="card-title">{role} @ {company}</span>
                        <div class="timeline-meta">{location} • {start} – {end}</div>
                        <p>{desc}</p>
                        <div class="section">{chips_html(techs)}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            """
        tl_html += "</div>"
        st.html(tl_html)

    else:
        # Fallback: original cards grid (unchanged look)
        exp_cards = ""
        for rec in records:
            f = rec.get('fields', {})
            role = f.get('Role', '')
            company = f.get('Company', '')
            location = f.get('Location', '')
            start = f.get('startYear') or f.get('startDate', '')
            end = f.get('endYear') or f.get('endDate') or 'Present'
            desc = f.get('Description', '')
            techs = f.get('Technologies') or f.get('Skills') or []

            companyLink = f.get('link_company', '')
            companyImageList = f.get('image_company') or []
            companyImageUrl = companyImageList[0]['url'] if companyImageList else ''

            if companyImageUrl:
                img_html = f'<img src="{companyImageUrl}">'
                if companyLink:
                    img_html = f'<a href="{companyLink}" target="_blank" rel="noopener">{img_html}</a>'
            else:
                img_html = ""

            exp_cards += f"""
            <div class="col s12 m6">
              <div class="card large">
                <div class="card-image" style="height:150px">
                  {img_html}
                </div>
                <div class="card-content">
                  <span class="card-title">{role} @ {company}</span>
                  <p class="grey-text">{location} • {start} – {end}</p>
                  <p>{desc}</p>
                  <div class="section">{chips_html(techs)}</div>
                </div>
              </div>
            </div>
            """

        expHTML = f'<div class="row">{exp_cards}</div>' if exp_cards else '<div class="row"><div class="col s12"><p>No experience added yet.</p></div></div>'
        st.html(expHTML)

# Display the Skills tab
with tabSkils:
    # Load skills once
    raw_records = tblskills.all(sort=['-Level'])

    # Normalize records (supports 'Categories' multi-select or 'Category' single-select)
    items = []
    for r in raw_records:
        f = r.get('fields', {})
        name = f.get('Name', '')
        notes = f.get('Notes', '')
        level = int(f.get('Level', 0) or 0)
        start_year = f.get('startYear', '')
        # Categories handling
        cats = f.get('Categories')
        if cats is None:
            cats = f.get('Category')
        if isinstance(cats, str):
            cats = [cats]
        if not isinstance(cats, list):
            cats = []
        cats = [c for c in cats if c] or ['Other']

        items.append({
            "name": name,
            "notes": notes,
            "level": level,
            "start_year": start_year,
            "categories": cats,
            "primary": cats[0]  # first category as primary for grouping/sorting
        })

    if not items:
        st.html('<p>No skills found.</p>')
    else:
        # Build available categories
        all_categories = sorted({c for it in items for c in it["categories"]})

        # UI controls
        col1, col2 = st.columns([2,2])
        with col1:
            selected_cats = st.multiselect(
                "Filter by categories",
                options=all_categories,
                default=[],
                placeholder="Choose one or more categories"
            )
        with col2:
            sort_choice = st.selectbox(
                "Sort by",
                [
                    "Primary category (A→Z), Level (High→Low)",
                    "Level (High→Low)",
                    "Experience (High→Low)",
                    "Name (A→Z)"
                ],
                index=0
            )

        # Apply category filter (keep skills having at least one selected category)
        if selected_cats:
            filtered = [it for it in items if any(c in selected_cats for c in it["categories"])]
        else:
            filtered = items

        # Helpers
        def years_of_exp(it):
            try:
                return int(today) - int(it["start_year"]) if it["start_year"] else -1
            except Exception:
                return -1

        # Sorting
        if sort_choice == "Level (High→Low)":
            filtered.sort(key=lambda it: (-it["level"], it["name"].lower()))
        elif sort_choice == "Experience (High→Low)":
            filtered.sort(key=lambda it: (-years_of_exp(it), -it["level"], it["name"].lower()))
        elif sort_choice == "Name (A→Z)":
            filtered.sort(key=lambda it: it["name"].lower())
        else:  # "Primary category (A→Z), Level (High→Low)"
            filtered.sort(key=lambda it: (it["primary"].lower(), -it["level"], it["name"].lower()))

        # Build HTML cards (same style)
        skills_html = ""
        for it in filtered:
            # Stars
            stars = "".join(
                '<i class="material-icons">star</i>' if i <= it["level"] else '<i class="material-icons">star_border</i>'
                for i in range(1, 6)
            )
            # Experience text
            yrs = years_of_exp(it)
            since_txt = f'{it["start_year"]} - More than {yrs} years' if yrs >= 0 else '—'
            # Category chips (use theme primary via CSS override)
            chips = "".join(f'<div class="chip orange lighten-4" style="margin-top:6px">{c}</div>' for c in it["categories"])

            skillHTML = f"""                    
                <div class="col s12 m4">
                    <div class="card small">
                        <div class="card-content">
                            <span class="card-title">{it["name"]}</span>
                            <p>{it["notes"]}</p>
                            <div class="section">{chips}</div>
                        </div>
                        <div class="card-action">
                            <div class="col s12 m6">
                                <p>Level:<br/>{stars}</p>
                            </div>
                            <div class="col s12 m6">
                                <p>Since:<br/>{since_txt}</p>
                            </div>
                        </div>
                    </div>
                </div>
            """
            skills_html += skillHTML

        container_html = f'<div class="row">{skills_html}</div>'
        st.html(container_html)

with tabPortfolio:
    projects=""
    skillsHTML=""
    knowledgeHTML=""
    # Loop creating the project templates
    for project in tblprojects.all():
        projectid= project['id']
        project=project["fields"]
        projectName = project['Name']
        projectDescription = project['Description']
        # Create the list of Skills and Knowledge
        projectSkils = project['skills']
        skillsHTML=[f'<div class="chip green lighten-4">{p}</div>' for p in projectSkils]
        skillsHTML="".join(skillsHTML)
        projectKnowledge = project['Knowledge']
        knowledgeHTML=[f'<div class="chip orange lighten-4">{p}</div>' for p in projectKnowledge]
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
                        <a target="_blank" rel="noopener noreferrer" href="{projectLink}" class="waves-effect waves-light btn-large white-text orange darken-3"><i class="material-icons left">open_in_new</i>View</a>                        
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
