"""Contact form and floating portfolio assistant for Streamlit."""

from __future__ import annotations

import html
import re
import smtplib
from email.message import EmailMessage

import streamlit as st


_INITIAL_MESSAGE = (
    "Hello! I’m Yana’s portfolio assistant. "
    "I can answer questions about her projects, experience, "
    "skills and approach to product design."
)

_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def init_chat_state() -> None:
    """Initializes the contact form and chat state."""
    st.session_state.setdefault("contact_form_open", False)
    st.session_state.setdefault(
        "portfolio_chat_messages",
        [{"role": "assistant", "content": _INITIAL_MESSAGE}],
    )


def create_chat_response(question: str) -> str:
    """Creates controlled responses about the portfolio."""
    normalized = " ".join(question.lower().split())

    if any(term in normalized for term in ("hallo", "hello", "hi", "guten tag", "hey")):
        return (
            "Hello! Great to have you here. "
            "You can ask me about Yana’s projects, Product Design and UX/UI experience, "
            "data analytics skills, or how to get in touch."
        )

    if any(term in normalized for term in ("projekt", "projekte", "project", "projects", "portfolio")):
        return (
            "Yana’s portfolio combines more than 10 years of UX/UI and Product Design experience "
            "with additional expertise in Data Analytics and Data Science. Her work includes projects for "
            "Murrelektronik, OPTIMA, MeaPuna and Mercedes-Benz, as well as "
            "data-informed projects using Power BI, Python and Streamlit."
        )

    if any(term in normalized for term in ("erfahrung", "beruf", "experience", "career", "senior", "product design", "ux", "ui")):
        return (
            "Yana brings more than 10 years of experience in UX/UI and Product Design "
            "and in designing complex digital products. She combines "
            "user-centered design, end-to-end ownership, technical understanding and data-informed product thinking."
        )

    if any(
        term in normalized
        for term in (
            "python",
            "sql",
            "power bi",
            "pandas",
            "data",
            "daten",
            "skill",
            "kompetenz",
            "competency",
            "competencies",
            "skills",
            "machine learning",
        )
    ):
        return (
            "Yana’s core competencies include Product Design, UX strategy, UX research, interaction design, "
            "user flows, information architecture, prototyping, usability testing, UI design and design systems. "
            "Her additional data skills include Python, SQL, Power BI and data visualization."
        )

    if any(term in normalized for term in ("end-to-end", "arbeitsweise", "prozess", "ansatz", "approach", "process", "workflow")):
        return (
            "Her approach is end-to-end and user-centered: "
            "understand the context, define the problem, design and prototype solutions, validate assumptions, "
            "and collaborate with engineering to deliver and evolve the product."
        )

    if any(term in normalized for term in ("kontakt", "contact", "email", "e-mail", "erreichen", "nachricht", "message", "reach")):
        return (
            "Please use the “Get in touch” button in the contact section. "
            "You can send Yana a direct message through the contact form."
        )

    if any(term in normalized for term in ("standort", "ort", "location", "based", "gaildorf")):
        return "Yana is based in Gaildorf, Germany."

    return (
        "I don’t currently have a specific portfolio answer for that. "
        "Try asking me about Yana’s projects, Product Design experience, skills, "
        "design approach or contact options."
    )


def _required_secret(name: str) -> str:
    value = st.secrets.get(name)
    if value is None or str(value).strip() == "":
        raise KeyError(name)
    return str(value).strip()


def send_contact_email(
    *,
    name: str,
    sender_email: str,
    company: str,
    message: str,
) -> tuple[bool, str]:
    """Sends a contact request via SMTP."""
    try:
        smtp_host = _required_secret("SMTP_HOST")
        smtp_port = int(_required_secret("SMTP_PORT"))
        smtp_user = _required_secret("SMTP_USER")
        smtp_password = _required_secret("SMTP_PASSWORD")
        contact_email = _required_secret("CONTACT_EMAIL")

        use_ssl = bool(st.secrets.get("SMTP_USE_SSL", False))
        use_starttls = bool(st.secrets.get("SMTP_USE_STARTTLS", not use_ssl))

        mail = EmailMessage()
        mail["Subject"] = f"New portfolio inquiry from {name}"
        mail["From"] = smtp_user
        mail["To"] = contact_email
        mail["Reply-To"] = sender_email
        mail.set_content(
            f"""
New contact request via the portfolio

Name: {name}
Email: {sender_email}
Company: {company or "Not provided"}

Message:
{message}
""".strip()
        )

        if use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(mail)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.ehlo()
                if use_starttls:
                    server.starttls()
                    server.ehlo()
                server.login(smtp_user, smtp_password)
                server.send_message(mail)

        return True, (
            "Thank you! Your message has been sent to Yana successfully. "
            "She can reply directly to the email address you provided."
        )

    except KeyError:
        return False, (
            "Email delivery is not fully configured yet. "
            "Please check the .streamlit/secrets.toml file."
        )
    except ValueError:
        return False, "SMTP_PORT must be a valid number."
    except (OSError, smtplib.SMTPException) as exc:
        return False, (
            "Your message could not be sent right now. "
            "Please try again later. "
            f"Technical details: {type(exc).__name__}"
        )


def _portrait_header(
    *,
    portrait_data_url: str | None,
    subtitle: str,
) -> None:
    safe_portrait = html.escape(portrait_data_url or "", quote=True)
    avatar_html = (
        f'<img src="{safe_portrait}" alt="Portrait of Yana">'
        if safe_portrait
        else '<span aria-hidden="true">YP</span>'
    )

    st.html(
        f"""
        <div class="portfolio-chat">
            <div class="portfolio-chat-header">
                <div class="portfolio-chat-avatar">
                    {avatar_html}
                    <span class="portfolio-chat-status" aria-hidden="true"></span>
                </div>
                <div>
                    <strong>Yana Pfalzgraf</strong>
                    <span>{html.escape(subtitle)}</span>
                </div>
            </div>
        </div>
        """
    )


@st.dialog("Contact Yana", width="small")
def contact_form_dialog(portrait_data_url: str | None = None) -> None:
    """Displays the contact form."""
    init_chat_state()
    _portrait_header(
        portrait_data_url=portrait_data_url,
        subtitle="Send a direct message",
    )

    st.markdown("### Send me a message")
    st.caption(
        "Required fields are marked with *. Your information will only be used "
        "to process your contact request."
    )

    with st.form("portfolio_contact_form", clear_on_submit=False):
        name = st.text_input("Name *", max_chars=100)
        sender_email = st.text_input("Email address *", max_chars=180)
        company = st.text_input("Company", max_chars=140)
        message = st.text_area(
            "Message *",
            height=150,
            max_chars=3000,
            placeholder=(
                "For example: We’d like to speak with you about a Senior Product Designer "
                "opportunity on our product team."
            ),
        )
        privacy_accepted = st.checkbox(
            "I consent to the processing of the information I provide "
            "for the purpose of handling this contact request. *"
        )

        submitted = st.form_submit_button(
            "Send message →",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        clean_name = name.strip()
        clean_email = sender_email.strip()
        clean_company = company.strip()
        clean_message = message.strip()

        if len(clean_name) < 2:
            st.error("Please enter your name.")
        elif not _EMAIL_PATTERN.match(clean_email):
            st.error("Please enter a valid email address.")
        elif len(clean_message) < 10:
            st.error("Please enter a slightly more detailed message.")
        elif not privacy_accepted:
            st.error("Please confirm that your information may be processed for this request.")
        else:
            with st.spinner("Sending message …"):
                success, feedback = send_contact_email(
                    name=clean_name,
                    sender_email=clean_email,
                    company=clean_company,
                    message=clean_message,
                )

            if success:
                st.success(feedback)
                st.balloons()
            else:
                st.error(feedback)

    st.divider()

    if st.button(
        "Close",
        key="close_contact_form",
        use_container_width=True,
    ):
        st.session_state["contact_form_open"] = False
        st.rerun()

    st.html(
        '<p class="portfolio-chat-note">'
        "The form only sends the information you explicitly submit."
        "</p>"
    )


def render_floating_chat(portrait_data_url: str | None = None) -> None:
    """Renders a floating portfolio assistant in the bottom-right corner."""
    init_chat_state()

    with st.popover(
        "💬 Questions about Yana’s portfolio?",
        key="floating_portfolio_chat",
        help="Open portfolio assistant",
    ):
        _portrait_header(
            portrait_data_url=portrait_data_url,
            subtitle="Portfolio assistant · available now",
        )

        history = st.container(height=300)
        with history:
            for message in st.session_state["portfolio_chat_messages"]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        prompt = st.chat_input(
            "Ask a question about the portfolio …",
            key="floating_portfolio_chat_input",
        )

        if prompt:
            st.session_state["portfolio_chat_messages"].append(
                {"role": "user", "content": prompt}
            )
            st.session_state["portfolio_chat_messages"].append(
                {"role": "assistant", "content": create_chat_response(prompt)}
            )
            st.rerun()

        if st.button(
            "Restart chat",
            key="reset_floating_portfolio_chat",
            use_container_width=True,
        ):
            st.session_state["portfolio_chat_messages"] = [
                {"role": "assistant", "content": _INITIAL_MESSAGE}
            ]
            st.rerun()

        st.html(
            '<p class="portfolio-chat-note">'
            "This assistant answers questions based on the content of this portfolio."
            "</p>"
        )
