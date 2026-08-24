from pathlib import Path
import html
import streamlit as st
import base64
import mimetypes

from chatbot import (
    contact_form_dialog,
    init_chat_state,
    render_floating_chat,
)

BASE_DIR = Path(__file__).parent
PORTRAIT_PATH = BASE_DIR / "assets" / "images" / "yp_image.png"
def get_image_data_url(relative_path: str) -> str:
    image_path = BASE_DIR / relative_path

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "application/octet-stream"

    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"

def get_base64_image(path: Path) -> str:
    with path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


portrait_base64 = get_base64_image(PORTRAIT_PATH)

clock_icon = get_image_data_url("assets/icons/clock.svg")
workflow_icon = get_image_data_url("assets/icons/workflow.svg")
chart_icon = get_image_data_url("assets/icons/chart-column-big.svg")

users_icon = get_image_data_url("assets/icons/users.svg")
search_icon = get_image_data_url("assets/icons/search.svg")
lightbulb_icon = get_image_data_url("assets/icons/lightbulb.svg")
target_icon = get_image_data_url("assets/icons/crosshair.svg")
growth_icon = get_image_data_url("assets/icons/chart-column-decreasing.svg")
st.set_page_config(
    page_title="Yana Pfalzgraf | Senior UX/UI Product Designer  ",
    page_icon="YP",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_chat_state()


def open_contact_form() -> None:
    """Öffnet ausschließlich das Kontaktformular.

    Streamlit erlaubt pro Skriptlauf nur einen Dialog. Deshalb wird ein
    eventuell geöffnetes Projekt zuerst geschlossen.
    """
    st.session_state["active_project_index"] = None
    st.session_state["contact_form_open"] = True


st.html(BASE_DIR / "assets" / "style.css")
st.html(
    """
    <style>
    /* Dialog insgesamt breiter */
    div[data-testid="stDialog"] > div[role="dialog"] {
        width: min(1500px, 97vw) !important;
        max-width: 1500px !important;
        max-height: 94vh !important;
        overflow-y: auto !important;
        border-radius: 18px !important;
    }


    /* Hauptbild im Projekt-Dialog */
    .case-image-frame {
        width: 100%;
        max-width: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        border: 1px solid #dbe3df;
        border-radius: 16px;
        background: #f7f9f8;
    }

    .case-image-frame img {
        width: 100%;
        max-width: none;
        height: auto;
        display: block;
        object-fit: contain;
    }

    .case-counter {
        margin-top: 0.45rem;
        margin-bottom: 0.9rem;
        text-align: center;
        color: #64736e;
        font-size: 0.85rem;
    }

    /* Unterer Informationsbereich: exakt drei Spalten */
    .case-description-grid {
        display: grid;
        grid-template-columns: 1.15fr 1fr 1.15fr;
        gap: 3rem;
        align-items: start;

        margin-top: 1.5rem;
        padding: 1.7rem 0 1.8rem;
        border-top: 1px solid #dfe5e1;
    }

    .case-description-grid section {
        min-width: 0;
    }

    .case-description-grid h4 {
        margin: 0 0 0.85rem;
        color: #1f5a49;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }

    .case-description-grid p {
        margin: 0;
        color: #3e4d48;
        font-size: 0.91rem;
        line-height: 1.65;
    }

    /* Abstand zwischen Rolle und Tools */
    .case-tools-heading {
        margin-top: 1.45rem !important;
    }

    /* Tools nebeneinander */
    .case-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        align-items: center;
    }

    .case-chip {
        display: inline-flex;
        align-items: center;
        padding: 0.4rem 0.65rem;

        border: 1px solid #d6dfda;
        border-radius: 999px;
        background: #f5f7f6;

        color: #29483e;
        font-size: 0.78rem;
        white-space: nowrap;
    }

    /* Highlights */
    .case-highlights {
        display: grid;
        gap: 0.7rem;
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .case-highlights li {
        display: flex;
        align-items: flex-start;
        gap: 0.55rem;

        color: #3e4d48;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .case-check {
        width: 1.15rem;
        height: 1.15rem;
        flex: 0 0 1.15rem;

        display: inline-flex;
        align-items: center;
        justify-content: center;

        margin-top: 0.05rem;
        border-radius: 50%;
        background: #1f5a49;
        color: white;

        font-size: 0.7rem;
        font-weight: 700;
    }

    /* Trennlinie vor der Projekt-Navigation */
    .case-project-footer-divider {
        margin: 0;
        padding-top: 1rem;
        border-top: 1px solid #dfe5e1;
    }

    /* Projektzähler in der Mitte */
    .case-project-counter {
        padding: 0.8rem 0;
        text-align: center;
        color: #43534d;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Footer-Buttons */
    div[data-testid="stDialog"] button {
        min-height: 42px;
        border-radius: 8px;
    }

    /* Erst auf kleinen Displays untereinander */
    @media (max-width: 720px) {
        .case-description-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
    }

    /* Lokale Lucide-Icons */
    .expertise-icon img {
        width: 25px;
        height: 25px;
        display: block;
        object-fit: contain;
        filter: brightness(0) invert(1);
    }

    .process-icon img {
        width: 24px;
        height: 24px;
        display: block;
        object-fit: contain;
        opacity: 0.78;
    }

    /* About / Expertise: tighter spacing and exact top alignment */
    .expertise-section {
        margin-bottom: 2.6rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: flex-start;
    }

    .section-heading {
        margin-top: 0 !important;
    }

    </style>
    """
)

PROJECTS_UX = [
    {
        "title": "Murrelektronik",
        "subtitle": "Product Design · UX/UI · Prototyping · Stakeholder Collaboration",
        "image": "assets/images/murrelektronik.svg",
        "card_image": "assets/images/Murrelektronik.svg",
        "cover_image": "assets/images/Murrelektronik.svg",
        "description": "Designed a user-centered experience for a digital installation platform that guides employees visually and interactively through complex wiring workflows.",
        "tags": ["UX Research", "UI Design", "Figma", "Prototyping"],

        "gallery": [
        "assets/images/Murrelektronik.svg",
        "assets/images/murrelektronik4.svg",
        "assets/images/murrelektronik5.svg",
        "assets/images/murrelektronik6.svg",
        ],
    },
    {
        "title": "OPTIMA",
        "subtitle": "Product Design · Enterprise Software · Industrial UX",
        "image": "assets/images/optima.svg",
        "card_image": "assets/images/optima.svg",
        "cover_image": "assets/images/optima.svg",
        "description": "Designed end-to-end UX/UI solutions for industrial software workflows, from early product concepts and interaction models to intuitive, implementation-ready interfaces.",
        "tags": ["User Flows", "Sketch", "Adobe XD", "Design System"],

        "gallery": [
        "assets/images/optima.svg",
        "assets/images/optima2.svg",
        "assets/images/optima3.svg",
        "assets/images/optima4.svg",
        ],
    },
    {
        "title": "MeaPuna",
        "subtitle": "Product Design · SAP Fiori/UI5 · UX Engineering",
        "image": "assets/images/meapuna.svg",
        "card_image": "assets/images/meapuna.svg",
        "cover_image": "assets/images/meapuna.svg",
        "description": "Owned UX/UI design and SAPUI5 frontend implementation across two software products, bridging product thinking, interaction design and technical delivery from concept to production.",
        "tags": ["SAP UI5 Programming","SAP Fiori Apps Reference Library", "Wireframes", "Usability"],

        "gallery": [
        "assets/images/meapuna.svg",
        "assets/images/meapuna.svg",
        "assets/images/meapuna2.svg",
        "assets/images/meapuna3.svg",
        ],
    },
    {
        "title": "Mercedes-Benz / CINTEO",
        "subtitle": "Product Design · Automotive Commerce · Agile Collaboration",
        "image": "assets/images/mercedes.svg",
        "card_image": "assets/images/cinteo.svg",
        "cover_image": "assets/images/cinteo.svg",
        "description": "Created user-centered product concepts for digital automotive commerce experiences, translating business requirements into intuitive customer journeys and interaction patterns.",
        "tags": ["Interaction Design", "Axure", "Automotive", "UI"],

        "gallery": [
        "assets/images/cinteo.svg",
        "assets/images/cinteo4.svg",
        "assets/images/cinteo2.svg",
        "assets/images/cinteo_suche_3.svg",
        ],
    },
]

PROJECTS_DATA = [
    {
        "title": "Project 01 · AutoScout24",
        "subtitle": "Data Analytics · Power BI · DAX · Python",
        "image": "assets/images/data_prediction.svg",
        "card_image": "assets/images/dsi1.svg",
        "cover_image": "assets/images/dsi1.svg",
        "description": (
           "Data product case study using the AutoScout24 dataset: used-car market analysis, pricing patterns, brand and model comparison, interactive filters and KPIs, DAX measures, Power Query and a star schema — with a strong focus on clear decision-oriented dashboard UX."
        ),
        "tags": [
            "Power BI",
            "Data Analytics",
            "Dashboard Design",
            "DAX",
            "Python",
            "Power Query",
            "ML",
        ],
        "gallery": [
            "assets/images/dsi1.svg",
            "assets/images/dsi2.svg",
            "assets/images/dsi3.svg",
            "assets/images/dsi4.svg",
            "assets/images/dsi5.svg",
            "assets/images/dsi6.svg",
            "assets/images/dsi7.svg",
        ],
    },
    {
        "title": "Project 02 · PlatePilot Navigator",
        "subtitle": "Recommendation Product · Scoring Model · Streamlit · Python",
        "image": "assets/images/data_forecasting.svg",
        "card_image": "assets/images/platepilot_navigator_cover.svg",
        "cover_image": "assets/images/platepilot_navigator_cover.svg",
        "description": "Designed and built a restaurant recommendation product with personalized filters, a weighted scoring model, map integration, location-based discovery and interactive data visualization — combining UX thinking, product logic and Python implementation.",
        "demo_url": "https://platpilotnavigatorapp.streamlit.app/",
        "tags": ["Python", "Streamlit", "Pandas", "Scikit-learn", "NumPy", "Folium", "GeoPy", "Parquet"],

        "gallery": [
        "assets/images/ppnavigator_new.svg",
        "assets/images/ppnavigator_new_2.svg",
        ],
    },
    {
        "title": "Project 03 · Olympic Games",
        "subtitle": "Data Analytics · Power BI · DAX · Python",
        "image": "assets/images/olympic_dashboard.svg",
        "card_image": "assets/images/olympic_dashboard.svg",
        "cover_image": "assets/images/olympic_dashboard.svg",
        "description": (
    "Interactive analytics case study built around Olympic Games data, including a star schema, DAX measures, participation trends, country dominance, gender representation and historical developments — translated into an accessible dashboard experience."
),
        "tags": ["Power BI", "Data Visualization", "DAX", "Power Query"],

        "gallery": [
        "assets/images/olympic_dashboard.svg",
        "assets/images/2_seite_olympic_dashboard.svg"
        ],
    },
]

# Zusätzliche Daten für die Projekt-Detailansicht.
# Pro Projekt kannst du später mehrere Bilder in "gallery" ergänzen.
ALL_PROJECTS = PROJECTS_UX + PROJECTS_DATA

for project in ALL_PROJECTS:
    project.setdefault("card_image", project["image"])
    project.setdefault("cover_image", project["card_image"])
    project.setdefault("gallery", [project["cover_image"]])
    project.setdefault("role", project["subtitle"])
    project.setdefault("highlights", project["tags"])
    project.setdefault("tools", project["tags"])


UX_VISIBLE_CARDS = 3
UX_MAX_START = max(0, len(PROJECTS_UX) - UX_VISIBLE_CARDS)

if "ux_carousel_start" not in st.session_state:
    st.session_state["ux_carousel_start"] = 0

if "active_project_index" not in st.session_state:
    st.session_state["active_project_index"] = None


@st.dialog("Project", width="large")
def project_dialog(project: dict) -> None:
    project_index = next(
        (
            index
            for index, item in enumerate(ALL_PROJECTS)
            if item["title"] == project["title"]
        ),
        0,
    )

    project_key = (
        project["title"]
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("·", "_")
    )

    gallery = project.get("gallery") or [project["cover_image"]]
    gallery_index_key = f"gallery_index_{project_key}"

    if gallery_index_key not in st.session_state:
        st.session_state[gallery_index_key] = 0

    current_image_index = (
        st.session_state[gallery_index_key] % len(gallery)
    )

    current_image = get_image_data_url(
        gallery[current_image_index]
    )

    # Hauptbild über die volle Dialogbreite
    st.html(
        f"""
        <div class="case-image-frame">
            <img
                src="{current_image}"
                alt="{html.escape(project['title'])} – view {current_image_index + 1}"
            >
        </div>

        <div class="case-counter">
            Image {current_image_index + 1} of {len(gallery)}
        </div>
        """
    )

    # Navigation für Bilder innerhalb desselben Projekts
    if len(gallery) > 1:
        image_prev, image_count, image_next = st.columns(
            [1, 0.25, 1],
            vertical_alignment="center",
        )

        with image_prev:
            if st.button(
                "← Previous image",
                key=f"previous_image_{project_key}",
                use_container_width=True,
            ):
                st.session_state[gallery_index_key] = (
                    current_image_index - 1
                ) % len(gallery)
                st.rerun()

        with image_count:
            st.html(
                f"""
                <div class="case-counter">
                    {current_image_index + 1} / {len(gallery)}
                </div>
                """
            )

        with image_next:
            if st.button(
                "Next image →",
                key=f"next_image_{project_key}",
                use_container_width=True,
            ):
                st.session_state[gallery_index_key] = (
                    current_image_index + 1
                ) % len(gallery)
                st.rerun()
     

    tools_html = "".join(
        f'<span class="case-chip">{html.escape(tool)}</span>'
        for tool in project.get("tools", project["tags"])
    )

    highlights_html = "".join(
        f"""
        <li>
            <span class="case-check">✓</span>
            {html.escape(highlight)}
        </li>
        """
        for highlight in project.get(
            "highlights",
            project["tags"],
        )
    )

    # Beschreibung unterhalb der Galerie
    st.html(
        f"""
        <div class="case-description-grid">
            <section>
                <h4>About the project</h4>
                <p>{html.escape(project["description"])}</p>
            </section>

            <section>
                <h4>My role</h4>
                <p>
                    {html.escape(
                        project.get("role", project["subtitle"])
                    )}
                </p>

                <h4 class="case-tools-heading">
                    Tools & technologies
                </h4>

                <div class="case-chip-row">
                    {tools_html}
                </div>
            </section>

            <section>
                <h4>Highlights</h4>
                <ul class="case-highlights">
                    {highlights_html}
                </ul>
            </section>
        </div>
        """
    )

    if project.get("demo_url"):
        st.link_button(
            "🚀 Open PlatePilot app",
            project["demo_url"],
            use_container_width=False,
        )


    # Footer: zwischen Projekten wechseln
    st.html('<div class="case-project-footer-divider"></div>')

    previous_project_index = (
        project_index - 1
    ) % len(ALL_PROJECTS)

    next_project_index = (
        project_index + 1
    ) % len(ALL_PROJECTS)

    footer_left, footer_center, footer_right = st.columns(
        [1, 0.22, 1],
        vertical_alignment="center",
    )

    with footer_left:
        if st.button(
            "← Previous project",
            key=f"previous_project_{project_key}",
            use_container_width=True,
        ):
            st.session_state["active_project_index"] = (
                previous_project_index
            )
            st.rerun()

    with footer_center:
        st.html(
            f"""
            <div class="case-project-counter">
                {project_index + 1} / {len(ALL_PROJECTS)}
            </div>
            """
        )

    with footer_right:
        if st.button(
            "Next project →",
            key=f"next_project_{project_key}",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["active_project_index"] = (
                next_project_index
            )
            st.rerun()


def project_card(project: dict) -> None:
    image_src = get_image_data_url(project["card_image"])

    tags = "".join(
        f'<span class="project-tag">{html.escape(tag)}</span>'
        for tag in project["tags"]
    )

    project_key = (
        project["title"]
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("·", "_")
        .replace(".", "_")
    )

    # Karte und Streamlit-Button liegen in einem gemeinsamen Container.
    # Dadurch kann CSS alle Karten gleich hoch machen und den Button
    # zuverlässig am unteren Rand ausrichten.
    with st.container(key=f"project_card_{project_key}"):
        st.html(
            f"""
            <article class="project-card">

                <div class="project-image-wrapper">
                    <img
                        src="{image_src}"
                        alt="{html.escape(project['title'])}"
                    >
                </div>

                <div class="project-content">
                    <h3>{html.escape(project['title'])}</h3>
                    <p class="project-subtitle">{html.escape(project['subtitle'])}</p>
                    <p class="project-description">{html.escape(project['description'])}</p>
                    <div class="project-tags">{tags}</div>
                </div>
            </article>
            """
        )

        if st.button(
            "View case study →",
            key=f"open_project_{project['title']}",
            use_container_width=True,
        ):
            # Es darf pro Streamlit-Lauf nur ein Dialog geöffnet werden.
            st.session_state["contact_form_open"] = False
            st.session_state["active_project_index"] = ALL_PROJECTS.index(project)
            st.rerun()


def section_header(kicker: str, title: str, text: str = "") -> None:
    st.html(
        f"""
        <div class="section-heading">
            <span>{html.escape(kicker)}</span>
            <h2>{html.escape(title)}</h2>
            {f'<p>{html.escape(text)}</p>' if text else ''}
        </div>
        """
    )


# Custom portfolio header. Replace links when the pages are ready.
st.html(
    """
    <header class="site-header">
        <a class="brand" href="#home">
            <span class="brand-mark">YP</span>
            <span>YANA PFALZGRAF</span>
        </a>
        <nav>
            <a href="#about">About</a>
            <a href="#projects">Work</a>
            <a href="#skills">Expertise</a>
        </nav>
        <a class="header-cta" href="#contact">Contact</a>
    </header>
    """
)

# Hero
st.html('<span id="home" class="anchor"></span>')
hero_text, hero_visual = st.columns([1.08, 0.92], gap="large", vertical_alignment="center")

with hero_text:
    st.html(
        """
        <section class="hero-copy">
            <p class="eyebrow">HELLO, I’M YANA</p>
            <h1>Senior Product Designer<br><span>UX/UI · Complex Digital Products</span></h1>
            <p class="hero-lead">
                I bring <b>10+ years of experience</b> designing digital products — from UX strategy,
                research and interaction design to prototyping, design systems and implementation.
                I turn complex user and business requirements into clear, intuitive product experiences.
            </p>
            <div class="hero-actions">
                <a class="button primary" href="#projects">View selected work →</a>
                <a class="button secondary" href="#about">About me</a>
            </div>
        </section>
        """
    )

with hero_visual:
    st.html(
        f"""
        <div class="portrait-wrap">
            <img
                src="data:image/jpeg;base64,{portrait_base64}"
                class="portrait-image"
                alt="Portrait of Yana Pfalzgraf"
            >
        </div>
        """
    )

# Kompetenzkarten und End-to-End-Prozess mit lokalen Lucide-SVGs
st.html(
    f"""
    <section class="expertise-section" aria-label="Experience and design approach">
        <div class="expertise-cards">
            <article class="expertise-card">
                <div class="expertise-icon" aria-hidden="true">
                    <img src="{clock_icon}" alt="">
                </div>
                <div class="expertise-card-copy">
                    <p class="expertise-number">10+</p>
                    <h3>Years in Product Design</h3>
                    <p>More than a decade across UX/UI, product design and complex digital products — from early discovery to delivery.</p>
                </div>
            </article>

            <article class="expertise-card">
                <div class="expertise-icon" aria-hidden="true">
                    <img src="{workflow_icon}" alt="">
                </div>
                <div class="expertise-card-copy">
                    <p class="expertise-kicker">END-TO-END OWNERSHIP</p>
                    <h3>From ambiguity to product clarity</h3>
                    <p>I structure complex requirements, define user flows, prototype solutions, validate decisions and collaborate closely with engineering through implementation.</p>
                </div>
            </article>

            <article class="expertise-card">
                <div class="expertise-icon" aria-hidden="true">
                    <img src="{chart_icon}" alt="">
                </div>
                <div class="expertise-card-copy">
                    <p class="expertise-kicker">DESIGN + DATA</p>
                    <h3>User needs. Business goals. Evidence.</h3>
                    <p>My data analytics background strengthens how I frame product questions, evaluate evidence and communicate design decisions.</p>
                </div>
            </article>
        </div>

        <div class="process-panel">
            <p class="process-eyebrow">MY APPROACH: END-TO-END &amp; USER-CENTERED</p>
            <div class="process-flow">
                <div class="process-step">
                    <div class="process-icon" aria-hidden="true">
                        <img src="{users_icon}" alt="">
                    </div>
                    <h4>Understand</h4>
                    <p>Frame user needs, context and business goals</p>
                </div>

                <span class="process-arrow" aria-hidden="true">→</span>

                <div class="process-step">
                    <div class="process-icon" aria-hidden="true">
                        <img src="{search_icon}" alt="">
                    </div>
                    <h4>Define</h4>
                    <p>Structure requirements, flows and product constraints</p>
                </div>

                <span class="process-arrow" aria-hidden="true">→</span>

                <div class="process-step">
                    <div class="process-icon" aria-hidden="true">
                        <img src="{lightbulb_icon}" alt="">
                    </div>
                    <h4>Design</h4>
                    <p>Explore concepts and prototype interactions</p>
                </div>

                <span class="process-arrow" aria-hidden="true">→</span>

                <div class="process-step">
                    <div class="process-icon" aria-hidden="true">
                        <img src="{target_icon}" alt="">
                    </div>
                    <h4>Validate</h4>
                    <p>Test assumptions and refine with users and stakeholders</p>
                </div>

                <span class="process-arrow" aria-hidden="true">→</span>

                <div class="process-step">
                    <div class="process-icon" aria-hidden="true">
                        <img src="{growth_icon}" alt="">
                    </div>
                    <h4>Deliver & evolve</h4>
                    <p>Partner with engineering and improve the product over time</p>
                </div>
            </div>
        </div>
    </section>
    """
)


# About & skills
# Keep both section headings on exactly the same vertical level.
# The anchors live outside the columns so they do not create extra spacing.
st.html(
    '<span id="about" class="anchor"></span>'
    '<span id="skills" class="anchor"></span>'
)
about_col, skills_col = st.columns(
    [0.95, 1.05],
    gap="large",
    vertical_alignment="top",
)

with about_col:
    section_header("PROFILE", "About me")
    st.markdown(
        """
I am a **Senior Product Designer with 10+ years of experience in UX/UI and digital product development**. I have worked across complex B2B, industrial, automotive and enterprise software contexts, translating user needs and business requirements into intuitive, scalable product experiences.

My work spans **UX strategy, research, user flows, information architecture, interaction design, low- to high-fidelity prototyping, usability testing, UI design and design systems**. I am comfortable taking ownership from early ambiguity through implementation and collaborating closely with product owners, stakeholders and engineering teams.

My additional background in **Data Science & Analytics** — including Python, SQL, Power BI, KPIs and data visualization — adds an evidence-driven layer to my product design practice and helps me connect qualitative user insight with quantitative product signals.
        """
    )

with skills_col:
    section_header("EXPERTISE", "Core competencies")
    skills = [
        "Product Design", "UX Strategy", "UX Research", "User-Centered Design",
        "Interaction Design", "User Flows", "Information Architecture",
        "Low- to High-Fidelity Prototyping", "Usability Testing & Validation",
        "UI Design", "Design Systems", "Figma", "Axure RP", "Adobe XD",
        "Stakeholder Collaboration", "Engineering Collaboration", "Agile Product Development",
        "Independent Ownership", "Data Visualization", "Product Analytics Thinking",
        "Python", "SQL", "Power BI",
    ]
    st.html(
        '<div class="skills-grid">'
        + "".join(f'<span>{html.escape(skill)}</span>' for skill in skills)
        + "</div>"
    )

# Projects
st.html('<span id="projects" class="anchor"></span>')
section_header(
    "SELECTED WORK",
    "Case studies",
    "A selection of product design work across enterprise software, automotive experiences and data-informed digital products.",
)

# Product Design / UX/UI first
st.html('<div class="project-category"><span>PRODUCT DESIGN · UX/UI</span></div>')

# Desktop: three cards visible. The arrows move the carousel by one card.
ux_start = min(
    max(0, st.session_state["ux_carousel_start"]),
    UX_MAX_START,
)
st.session_state["ux_carousel_start"] = ux_start
visible_ux_projects = PROJECTS_UX[ux_start:ux_start + UX_VISIBLE_CARDS]

with st.container(key="ux_project_carousel"):
    left_arrow, card_1, card_2, card_3, right_arrow = st.columns(
        [0.13, 1, 1, 1, 0.13],
        gap="medium",
        vertical_alignment="center",
    )

    with left_arrow:
        if st.button(
            "←",
            key="ux_carousel_previous",
            disabled=ux_start == 0,
            help="Previous projects",
            use_container_width=True,
        ):
            st.session_state["ux_carousel_start"] = max(0, ux_start - 1)
            st.rerun()

    for column, project in zip(
        (card_1, card_2, card_3),
        visible_ux_projects,
    ):
        with column:
            project_card(project)

    with right_arrow:
        if st.button(
            "→",
            key="ux_carousel_next",
            disabled=ux_start >= UX_MAX_START,
            help="More projects",
            use_container_width=True,
        ):
            st.session_state["ux_carousel_start"] = min(
                UX_MAX_START,
                ux_start + 1,
            )
            st.rerun()

    if UX_MAX_START > 0:
        dots = "".join(
            '<span class="carousel-dot active" aria-current="true"></span>'
            if index == ux_start
            else '<span class="carousel-dot"></span>'
            for index in range(UX_MAX_START + 1)
        )
        st.html(
            f'<div class="carousel-dots" aria-label="Carousel position">{dots}</div>'
        )


# Data-informed work second
st.html('<div class="project-category data"><span>DATA-INFORMED PRODUCT CASES</span></div>')

# Exactly three data projects in a static grid.
data_cols = st.columns(3, gap="medium")
for column, project in zip(data_cols, PROJECTS_DATA):
    with column:
        project_card(project)


# Dialogstatus zentral auswerten. Streamlit erlaubt pro Skriptlauf nur
# einen geöffneten Dialog. Projekt- und Kontakt-Dialog sind daher exklusiv.
active_project_index = st.session_state.get("active_project_index")
contact_form_is_open = st.session_state.get("contact_form_open", False)

# Falls durch einen alten Session-State beide Werte gesetzt sind, hat das
# Kontaktformular Vorrang und der Projektstatus wird bereinigt.
if contact_form_is_open and active_project_index is not None:
    st.session_state["active_project_index"] = None
    active_project_index = None

if active_project_index is not None:
    project_dialog(ALL_PROJECTS[active_project_index])

# CTA
st.html('<span id="contact" class="anchor"></span>')

with st.container(key="contact_banner"):
    contact_copy, contact_action = st.columns(
        [4.2, 1.25],
        gap="large",
        vertical_alignment="center",
    )

    with contact_copy:
        st.html(
            """
            <div class="contact-banner-copy">
                <p class="eyebrow">CONTACT</p>
                <h2>Let’s build thoughtful digital products.</h2>
                <p>
                    I’m open to senior Product Design and UX/UI opportunities where complex problems,
                    strong collaboration and end-to-end ownership matter.
                </p>
            </div>
            """
        )

    with contact_action:
        st.button(
            "Get in touch →",
            key="open_portfolio_chat_button",
            type="primary",
            use_container_width=True,
            on_click=open_contact_form,
        )
        st.caption("Opens the contact form.")

# Nur einen Dialog pro Skriptlauf öffnen. Durch das if/elif kann das
# Kontaktformular nicht gleichzeitig mit dem Projekt-Dialog erscheinen.
contact_form_is_open = st.session_state.get("contact_form_open", False)
active_project_index = st.session_state.get("active_project_index")

if contact_form_is_open and active_project_index is None:
    contact_form_dialog(
        portrait_data_url=f"data:image/jpeg;base64,{portrait_base64}"
    )
elif active_project_index is None:
    # Den schwebenden Chat nur rendern, wenn kein anderer Dialog aktiv ist.
    # Falls render_floating_chat intern ebenfalls st.dialog verwendet, wird
    # dadurch die StreamlitAPIException zuverlässig verhindert.
    render_floating_chat(
        portrait_data_url=f"data:image/jpeg;base64,{portrait_base64}"
    )


footer_html = """
<footer>
    <div class="footer-intro">
        <strong>YANA PFALZGRAF</strong>
        <p>
            Senior Product Designer · UX/UI · Data-Informed Products.
            Turning complex requirements into excellent user experience.</br>

        </p>
    </div>

    <div class="footer-links">
        <strong>LINKS</strong>
        <p>
            <a href="https://www.linkedin.com/in/yana-pfalzgraf-610669136/"
               target="_blank"
               rel="noopener noreferrer">LinkedIn | </a>

            <a href="https://www.xing.com/profile/Yana_Pfalzgraf"
               target="_blank"
               rel="noopener noreferrer">XING |</a>

            <a href="https://github.com/yanapfalzgraf"
               target="_blank"
               rel="noopener noreferrer">GitHub</a>
        </p>
    </div>

    <div class="footer-contact">
        <strong>CONTACT</strong>
        <p>
            Yana Pfalzgraf </br>
            Falkenstrasse 37</br>
            74405 Gaildorf</br>
            0176-32958972</br>
            yanapfalzgraf@googlemail.com
        </p>
    </div>
</footer>
"""

st.html(footer_html)