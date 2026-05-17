CATEGORIES = [
    'Sanitation','Infrastructure','Water Supply','Electricity',
    'Public Safety','Healthcare','Education','Transportation',
    'Environment','Animal Control','General'
]

def process_message(message: str, step: int, session_data: dict) -> dict:
    msg = message.strip()

    if step == 0:
        return {
            'response': "👋 Hello! I'm GrievanceAI — your civic complaint assistant.\n\nI'll help you file a complaint in just a few steps. Let's start!\n\n**What is your name?**",
            'next_step': 1, 'session_data': session_data, 'done': False, 'options': None
        }

    elif step == 1:
        session_data['name'] = msg
        return {
            'response': f"Nice to meet you, **{msg}**! 😊\n\n**What is the title of your complaint?**\n_(Keep it short, e.g., 'Broken road near market')_",
            'next_step': 2, 'session_data': session_data, 'done': False, 'options': None
        }

    elif step == 2:
        session_data['title'] = msg
        cats = '\n'.join(f"{i+1}. {c}" for i, c in enumerate(CATEGORIES))
        return {
            'response': f"Got it! ✅\n\n**Choose a category:**\n\n{cats}\n\n_Reply with the number or name_",
            'next_step': 3, 'session_data': session_data, 'done': False, 'options': CATEGORIES
        }

    elif step == 3:
        try:
            idx = int(msg) - 1
            session_data['category'] = CATEGORIES[idx] if 0 <= idx < len(CATEGORIES) else 'General'
        except ValueError:
            matched = next((c for c in CATEGORIES if c.lower() in msg.lower() or msg.lower() in c.lower()), 'General')
            session_data['category'] = matched
        return {
            'response': f"Category: **{session_data['category']}** 🏷️\n\n**Please describe your complaint in detail.**\n_(The more detail you give, the better we can help)_",
            'next_step': 4, 'session_data': session_data, 'done': False, 'options': None
        }

    elif step == 4:
        session_data['description'] = msg
        return {
            'response': "Thank you! 📝\n\n**What is the location of the issue?**\n_(Street name, landmark, or area)_",
            'next_step': 5, 'session_data': session_data, 'done': False, 'options': None
        }

    elif step == 5:
        session_data['location'] = msg
        desc_preview = session_data.get('description', '')[:80]
        if len(session_data.get('description', '')) > 80:
            desc_preview += '...'
        summary = (
            f"Here's your complaint summary:\n\n"
            f"📋 **Title:** {session_data.get('title')}\n"
            f"🏷️ **Category:** {session_data.get('category')}\n"
            f"📍 **Location:** {session_data.get('location')}\n"
            f"📄 **Description:** {desc_preview}\n\n"
            f"**Shall I submit this complaint?**"
        )
        return {
            'response': summary,
            'next_step': 6, 'session_data': session_data, 'done': False,
            'options': ['✅ Yes, submit', '❌ No, cancel']
        }

    elif step == 6:
        if 'yes' in msg.lower() or 'submit' in msg.lower():
            return {
                'response': "✅ **Complaint submitted successfully!**\n\nYou can track its status in **My Complaints**. Our team will review it shortly.\n\nIs there anything else I can help you with? Type **hi** to start over.",
                'next_step': 0, 'session_data': {}, 'done': True,
                'options': None, 'complaint_data': session_data
            }
        else:
            return {
                'response': "❌ Complaint cancelled.\n\nNo worries! Type **hi** anytime to start a new complaint.",
                'next_step': 0, 'session_data': {}, 'done': False, 'options': None
            }

    return {
        'response': "I didn't understand that. Could you please try again?",
        'next_step': step, 'session_data': session_data, 'done': False, 'options': None
    }
