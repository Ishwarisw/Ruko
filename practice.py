# practice.py - synthetic practice calls. All made up. No real people, numbers or accounts.

PRACTICE = [
    {
        "title": "Call 1",
        "voice": "Deepak",
        "text": "नमस्ते, मैं सीबीआई से बोल रहा हूँ। आपके आधार से मनी लॉन्ड्रिंग हुई है। "
                "आप डिजिटल अरेस्ट में हैं। यह बात किसी को मत बताइए और अभी पैसे ट्रांसफर कीजिए।",
        "is_scam": True,
        "why": "Real police or CBI never arrest anyone over a video call. The caller demands secrecy "
               "and urgent money transfer. That is the classic digital-arrest scam.",
    },
    {
        "title": "Call 2",
        "voice": "Nalini",
        "text": "नमस्ते, आपका कूरियर कल सुबह दस बजे आपके घर पहुँचेगा। कृपया घर पर रहिएगा।",
        "is_scam": False,
        "why": "No money is asked, no threat, no secrecy. Still, if a delivery caller asks for "
               "an OTP or payment, stop and check with the company yourself.",
    },
    {
        "title": "Call 3",
        "voice": "Deepak",
        "text": "मैं आपके बैंक के फ्रॉड डिपार्टमेंट से बोल रहा हूँ। आपका खाता खतरे में है। "
                "अभी जो कोड आपके फोन पर आया है वह बताइए, वरना खाता बंद हो जाएगा।",
        "is_scam": True,
        "why": "Banks never ask you to read out an OTP or code. The caller creates fear and urgency.",
    },
    {
        "title": "Call 4",
        "voice": "Nalini",
        "text": "बेटा, मैं शाम को बाज़ार जा रही हूँ। कुछ मंगाना हो तो बता देना।",
        "is_scam": False,
        "why": "An ordinary family message. No money demand, no pressure, no secrecy.",
    },
    {
        "title": "Call 5",
        "voice": "Deepak",
        "text": "बधाई हो, आपने लॉटरी जीती है। इनाम पाने के लिए पहले पाँच हज़ार रुपये "
                "प्रोसेसिंग फीस के रूप में भेजिए।",
        "is_scam": True,
        "why": "A real prize never asks you to pay first. Paying a fee to receive money is a known scam.",
    },
    {
        "title": "Call 6",
        "voice": "Nalini",
        "text": "आपके बैंक की तरफ से सूचना है कि आपके खाते में वेतन जमा हो गया है। "
                "किसी को अपना ओटीपी न बताएं।",
        "is_scam": False,
        "why": "A normal bank alert. It gives you information and warns you NOT to share an OTP. "
               "It asks for nothing.",
    },
]