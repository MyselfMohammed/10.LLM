from estimation_module import run_estimation_flow
from moderation import moderate_input
import datetime
import panel as pn
pn.extension()

CATEGORY_MAP = {
    "Services": ["Individual Product Shifting", "Complete House Shifting", "Estimation"],
    "Billing": ["Payment", "Download Invoice" ],    
    "Booking": ["Reschedule", "Cancellation"],
    "General": ["Write To Us", "Speak To Our Agent", "Feedback"]
}

def get_greeting():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    hour = now.hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

def classify_query_category(query):
    parts = query.strip().lower().split(" under ")
    if len(parts) == 2:
        subtopic, topic = parts
        for category, keywords in CATEGORY_MAP.items():
            if category.lower() == topic.strip().lower():
                for keyword in keywords:
                    if keyword.lower() == subtopic.strip().lower():
                        return category
    return "Unknown"

# ----------------------------------------------------------------------

def assistant_chat():
    # Greeting and intro
    greeting = get_greeting()
    welcome_panel = pn.pane.Markdown(f"""
### {greeting}! 👋

Welcome to the **i-Assist of Packers and Movers (Powered By Hope-AI)** 💼
""")

    # Ask for name
    name_input = pn.widgets.TextInput(name="🧑‍💼 Please Enter Your Name", placeholder="Your Name Here")
    name_greet = pn.pane.Markdown()

    # Estimation output placeholder
    estimation_panel = pn.Column()  # 👈 Placeholder to update dynamically

    # Input moderation and name handling
    def handle_name_submit(event):
        user_name = name_input.value.strip()
        if not user_name:
            name_greet.object = "❌ Please Enter a Valid Name."
            return

        flagged, reasons = moderate_input(user_name)
        if flagged:
            name_greet.object = f"⚠️ Inappropriate input. Reason: {reasons}"
            return

        user_name_title = user_name.title()
        name_greet.object = f"### Welcome, {user_name_title}! 😊\nHow May I Assist You with the details below?\n"
        dropdown_section.visible = True  # 👈 show only after valid name

    name_submit_btn = pn.widgets.Button(name="✅ Continue", button_type="primary")
    name_submit_btn.on_click(handle_name_submit)

    # Dropdowns for topic selection
    category_select = pn.widgets.Select(name="Select Topic", options=list(CATEGORY_MAP.keys()))
    subtopic_select = pn.widgets.Select(name="Select Sub-topic", options=[])

    def update_subtopics(event):
        selected = category_select.value
        subtopic_select.options = CATEGORY_MAP[selected]

    category_select.param.watch(update_subtopics, 'value')

    output_panel = pn.pane.Markdown()

    def handle_final_submit(event):
        selected_subtopic = subtopic_select.value
        selected_category = category_select.value
        full_query = f"{selected_subtopic} under {selected_category}"
        display_query = full_query.title()
    
        flagged, reasons = moderate_input(full_query)
        if flagged:
            output_panel.object = f"⚠️ Please rephrase your query. Reason: {reasons}"
            return
    
        category = classify_query_category(f"{selected_subtopic} under {selected_category}")
    
        if category == "Services":
            subtopic = selected_subtopic.strip().lower()
            if subtopic in ["estimation"]:
                output_panel.object = (
                    f"🧾 You selected: Sub-Topic : ({selected_subtopic}) Under Topic : ({selected_category})\n"
                    f"Let's gather the details for an accurate estimate.\n\n➡️ Scroll below for the estimation panel."
                )
                estimation_ui = run_estimation_flow(name_input.value.strip().title())
                estimation_panel.objects = [estimation_ui]
            else:
                output_panel.object = (
                    f"🤖 You selected: Sub-Topic : ({selected_subtopic}) Under Topic : ({selected_category})\n\n"
                    "We are Working on This !! Please Select Other Available Options to Know More Details."
                )
                estimation_panel.objects = []
    
        elif category == "Billing":
            output_panel.object = (
                f"💳 You selected: **{display_query}**\n"
                "Billing query. You can download your invoice or get payment support."
            )
            estimation_panel.objects = []
    
        elif category == "Booking":
            output_panel.object = (
                f"📅 You selected: **{display_query}**\n"
                "Booking query. You can change, cancel, or reschedule your booking."
            )
            estimation_panel.objects = []
    
        elif category == "General":
            output_panel.object = (
                f"🗣️ You selected: **{display_query}**\n"
                "We're here for general queries like feedback, agent talk, or support via email."
            )
            estimation_panel.objects = []
    
        else:
            output_panel.object = (
                f"🤖 You selected: Sub-Topic : ({selected_subtopic}) Under Topic : ({selected_category})\n\n"
                "We are Working on This !! Please Select Other Available Options to Know More Details."
            )
            estimation_panel.objects = []

    topic_submit_btn = pn.widgets.Button(name="🎯 Submit Query", button_type="primary")
    topic_submit_btn.on_click(handle_final_submit)

    exit_btn = pn.widgets.Button(name="❎ See You Next Time", button_type="danger")
    exit_panel = pn.pane.Markdown("🙏 Thank you for visiting Hope Packers & Movers Assistant. Have a great day!")

    def exit_chat(event):
        output_panel.object = exit_panel.object
        estimation_panel.objects = []

    exit_btn.on_click(exit_chat)

    # Initially hidden until name is valid
    dropdown_section = pn.Column(
        pn.Spacer(height=10),
        category_select,
        subtopic_select,
        topic_submit_btn,
        output_panel,
        estimation_panel,  # 👈 for dynamic content
        exit_btn,
        visible=False
    )

    main_layout = pn.Column(
        welcome_panel,
        name_input,
        name_submit_btn,
        name_greet,
        dropdown_section
    )

    return main_layout
