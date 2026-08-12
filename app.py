!pip install streamlit
!pip install groq
import streamlit as st
import os
import json
from groq import Groq
from google.colab import userdata

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Career & Product Suite",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Student Utility Suite")
st.write("Build V1 applications powered by Groq & Llama 3.3")

api_key = userdata.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Groq API Key not found! Please configure it in your Colab secrets using `userdata.set('GROQ_API_KEY', 'your_api_key')`.")
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "🎯 Resume & Email Tailor",
    "💡 Hackathon MVP Scoper",
    "🎤 AI Interview Coach"
])


# =========================================================
# TAB 1: RESUME TAILOR
# =========================================================

with tab1:

    st.header("Smart Resume & Outreach Tailor")

    col1, col2 = st.columns(2)

    with col1:
        resume_input = st.text_area(
            "Paste Your Resume:",
            height=200,
            placeholder="Paste text here..."
        )

    with col2:
        jd_input = st.text_area(
            "Paste Target Job Description:",
            height=200,
            placeholder="Paste JD here..."
        )

    outreach_type = st.selectbox(
        "Select Output Format:",
        [
            "LinkedIn Summary",
            "LinkedIn DM",
            "Cold Email",
            "Cover Letter"
        ]
    )

    if st.button("Draft Tailored Outreach", type="primary"):

        if not resume_input or not jd_input:

            st.warning(
                "Please provide both Resume and Job Description."
            )

        else:

            PROMPTS = {

                "LinkedIn Summary": f"""
You are an expert career coach. Write a compelling LinkedIn "About"
Summary for the candidate, positioning them for the target Job Description.

STRICT RULES:

1. ONLY use facts, skills, and metrics explicitly stated in the RESUME.
   NO hallucinations.
2. Tone: Professional, forward-looking, and engaging.
3. Maximum 3 short paragraphs.

RESUME:
{resume_input}

JOB DESCRIPTION:
{jd_input}
""",

                "LinkedIn DM": f"""
You are an expert career coach. Write a highly concise LinkedIn Direct
Message (under 75 words) to a recruiter for the target Job Description.

STRICT RULES:

1. ONLY use facts from the RESUME. NO hallucinations.
2. Tone: Direct, polite, and confident.
3. Include a clear Call to Action.

RESUME:
{resume_input}

JOB DESCRIPTION:
{jd_input}
""",

                "Cold Email": f"""
You are an expert career coach. Write a Cold Email to a hiring manager
for the target Job Description.

STRICT RULES:

1. ONLY use facts from the RESUME. NO hallucinations.
2. Must include a catchy, professional Subject Line.
3. Tone: Professional and value-driven.
4. Map 1-2 key resume achievements directly to the job requirements.

RESUME:
{resume_input}

JOB DESCRIPTION:
{jd_input}
""",

                "Cover Letter": f"""
You are an expert career coach. Write a formal Cover Letter for the
target Job Description.

STRICT RULES:

1. ONLY use facts from the RESUME. NO hallucinations.
2. Structure:
   - Formal greeting
   - Engaging opening
   - 2 body paragraphs matching resume skills to JD needs
   - Professional closing

RESUME:
{resume_input}

JOB DESCRIPTION:
{jd_input}
"""
            }

            system_prompt = PROMPTS[outreach_type]

            with st.spinner(
                f"Drafting your {outreach_type}..."
            ):

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": system_prompt
                        }
                    ],
                    temperature=0.3
                )

                st.success("Draft Generated!")

                st.markdown(
                    res.choices[0].message.content
                )

    # =====================================================
    # ADDITIONAL CAREER INSIGHTS
    # =====================================================

    st.divider()

    st.subheader("🔍 Additional Career Insights")

    additional_analysis = st.selectbox(
        "Select Additional Career Insights:",
        [
            "No Additional Analysis",
            "Generate Interview Questions",
            "Analyze Missing Skills",
            "Generate Both"
        ]
    )

    if st.button("Generate Additional Insights"):

        if not resume_input or not jd_input:

            st.warning(
                "Please provide both Resume and Job Description."
            )

        elif additional_analysis == "No Additional Analysis":

            st.info(
                "No additional analysis selected."
            )

        else:

            # =============================================
            # INTERVIEW QUESTIONS
            # =============================================

            if additional_analysis in [
                "Generate Interview Questions",
                "Generate Both"
            ]:

                interview_prompt = f"""
You are an expert technical recruiter and interview coach.

Based ONLY on the candidate's RESUME and the TARGET JOB DESCRIPTION,
generate personalized interview questions.

RESUME:
{resume_input}

TARGET JOB DESCRIPTION:
{jd_input}

Generate questions in the following categories:

1. Technical Questions
- Questions directly related to the technical skills mentioned
  in the job description.

2. Resume-Based Questions
- Questions about the candidate's projects, skills, education,
  internships, or experience mentioned in the resume.

3. Behavioral / HR Questions
- Questions relevant to the candidate and this specific role.

RULES:
- Do NOT invent experience that is not present in the resume.
- Questions should be specific to this candidate and job.
- Avoid generic questions whenever possible.
- Provide approximately 5 questions per category.
- Clearly separate the three categories.
"""

                with st.spinner(
                    "Generating personalized interview questions..."
                ):

                    interview_res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": interview_prompt
                            }
                        ],
                        temperature=0.4
                    )

                    st.subheader(
                        "🎤 Personalized Interview Questions"
                    )

                    st.markdown(
                        interview_res.choices[0].message.content
                    )

            # =============================================
            # MISSING SKILLS ANALYZER
            # =============================================

            if additional_analysis in [
                "Analyze Missing Skills",
                "Generate Both"
            ]:

                skills_prompt = f"""
You are an expert career coach and technical recruiter.

Compare the candidate's RESUME with the TARGET JOB DESCRIPTION
and analyze the candidate's skill gaps.

RESUME:
{resume_input}

TARGET JOB DESCRIPTION:
{jd_input}

Identify:

1. Skills already present in the resume that match the job description.

2. Important skills mentioned in the job description that are
   missing or not clearly demonstrated in the resume.

3. For every missing skill, assign a priority:
   - High
   - Medium
   - Low

4. Give a short recommendation explaining what the candidate
   should learn, practice, or improve for each important missing skill.

RULES:
- ONLY use information actually present in the resume and job description.
- Do NOT claim that the candidate has a skill unless it appears
  in the resume.
- Do NOT invent experience.
- Focus on skills that are genuinely relevant to the target role.
- Keep the analysis practical and concise.
"""

                with st.spinner(
                    "Analyzing skill gaps..."
                ):

                    skills_res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": skills_prompt
                            }
                        ],
                        temperature=0.3
                    )

                    st.subheader(
                        "🧠 Missing Skills Analysis"
                    )

                    st.markdown(
                        skills_res.choices[0].message.content
                    )


# =========================================================
# TAB 2: HACKATHON SCOPER
# =========================================================

with tab2:

    st.header("Hackathon MVP Scoper")

    raw_idea = st.text_input(
        "Enter your rough project idea:",
        placeholder="e.g., An app that tracks gym equipment usage in real-time"
    )

    tools_available = st.multiselect(
        "Select tools you know how to use:",
        [
            "Python",
            "Streamlit",
            "HTML/CSS",
            "React",
            "Groq API",
            "Gemini API",
            "Supabase",
            "Firebase",
            "SQL"
        ],
        default=[
            "Python",
            "Streamlit",
            "Groq API"
        ]
    )

    if st.button("Scope Project MVP", type="primary"):

        if not raw_idea:

            st.warning(
                "Please enter a project idea."
            )

        else:

            scoping_prompt = f"""
You are a Senior Technical Product Manager.

Scope a 24-hour hackathon MVP for this idea:
{raw_idea}

AVAILABLE TECH STACK:
{', '.join(tools_available)}

INSTRUCTIONS:

1. Define the core problem in 1 sentence.
2. List 3 key features for V1 that CAN be built using ONLY
   the available tech stack.
3. Output STRICT JSON format matching this schema:

{{
  "project_title": "Catchy Name",
  "problem_statement": "1 sentence",
  "mvp_features": [
      "Feature A",
      "Feature B",
      "Feature C"
  ],
  "tech_stack_mapping": "How the chosen tools will be used"
}}
"""

            with st.spinner(
                "Scoping MVP requirements..."
            ):

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": scoping_prompt
                        }
                    ],
                    response_format={
                        "type": "json_object"
                    },
                    temperature=0.4
                )

                json_data = json.loads(
                    res.choices[0].message.content
                )

                st.subheader(
                    f"📌 Project: {json_data.get('project_title')}"
                )

                st.write(
                    f"**Core Problem:** "
                    f"{json_data.get('problem_statement')}"
                )

                st.markdown(
                    "**MVP Feature Scope:**"
                )

                for feature in json_data.get(
                    "mvp_features", []
                ):

                    st.markdown(
                        f"- {feature}"
                    )

                st.info(
                    f"**Tech Stack Plan:** "
                    f"{json_data.get('tech_stack_mapping')}"
                )


# =========================================================
# TAB 3: AI INTERVIEW COACH
# =========================================================

with tab3:

    st.header("🎤 AI Interview Coach")

    st.write(
        "Practice for your target role with personalized "
        "AI-generated interview questions."
    )

    col1, col2 = st.columns(2)

    with col1:

        interview_resume = st.text_area(
            "Paste Your Resume:",
            height=220,
            placeholder="Paste your resume here..."
        )

    with col2:

        interview_jd = st.text_area(
            "Paste Target Job Description:",
            height=220,
            placeholder="Paste the job description here..."
        )

    interview_type = st.selectbox(
        "Select Interview Type:",
        [
            "Technical Interview",
            "HR / Behavioral Interview",
            "Project-Based Interview",
            "Mixed Interview"
        ]
    )

    number_of_questions = st.selectbox(
        "Number of Questions:",
        [5, 10, 15]
    )

    if st.button(
        "Generate Interview Questions",
        type="primary"
    ):

        if not interview_resume or not interview_jd:

            st.warning(
                "Please provide both your Resume and Job Description."
            )

        else:

            interview_coach_prompt = f"""
You are an expert interviewer and career coach.

Your task is to prepare a personalized interview for a candidate
based on their resume and the target job description.

CANDIDATE RESUME:
{interview_resume}

TARGET JOB DESCRIPTION:
{interview_jd}

INTERVIEW TYPE:
{interview_type}

NUMBER OF QUESTIONS:
{number_of_questions}

INSTRUCTIONS:

1. Generate exactly {number_of_questions} interview questions.

2. Make the questions highly relevant to the target job.

3. Use the candidate's actual resume, projects, skills,
   education, and experience when creating personalized questions.

4. Do not invent any experience, skill, project, or achievement
   that is not present in the resume.

5. For a Technical Interview:
   Focus on technical skills, tools, technologies, and concepts
   mentioned in the job description.

6. For an HR / Behavioral Interview:
   Focus on motivation, communication, teamwork, strengths,
   weaknesses, challenges, and career goals.

7. For a Project-Based Interview:
   Focus on the projects and experiences mentioned in the resume.

8. For a Mixed Interview:
   Include a balanced combination of technical, project-based,
   and behavioral questions.

9. Number every question clearly.

10. Do not provide answers. Only provide the interview questions.

11. Start with easier questions and gradually increase the difficulty.

Format the response as:

## Interview Questions

1. Question
2. Question
3. Question
...
"""

            with st.spinner(
                "Preparing your personalized interview..."
            ):

                interview_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": interview_coach_prompt
                        }
                    ],
                    temperature=0.5
                )

                st.success(
                    "Your personalized interview is ready! 🎯"
                )

                st.markdown(
                    interview_response.choices[0].message.content
                )
