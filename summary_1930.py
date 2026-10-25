# summary_1930.py - builds a short summary to read out when calling 1930.
# Nothing is stored or sent anywhere. Demo uses fake data only.

def build_summary(lang, when, amount, how, txn_id, receiver, caller_claim, caller_number):
    if lang == "mr-IN":
        lines = [
            "नमस्कार, मी सायबर फसवणुकीची तक्रार करत आहे.",
            f"वेळ: {when}.",
            f"रक्कम: {amount} रुपये.",
            f"पैसे कसे पाठवले: {how}.",
            f"व्यवहार क्रमांक: {txn_id}.",
            f"ज्या खात्यात किंवा UPI वर पैसे गेले: {receiver}.",
            f"फोन करणारा स्वतःला म्हणाला: {caller_claim}.",
            f"त्याचा फोन नंबर: {caller_number}.",
            "कृपया हे खाते लवकरात लवकर गोठवण्याची विनंती आहे.",
        ]
    else:
        lines = [
            "नमस्ते, मैं साइबर धोखाधड़ी की शिकायत कर रहा हूँ।",
            f"समय: {when}।",
            f"राशि: {amount} रुपये।",
            f"पैसे कैसे भेजे: {how}।",
            f"ट्रांजैक्शन आईडी: {txn_id}।",
            f"जिस खाते या UPI में पैसे गए: {receiver}।",
            f"कॉल करने वाले ने खुद को बताया: {caller_claim}।",
            f"उसका फोन नंबर: {caller_number}।",
            "कृपया इस खाते को जल्द से जल्द रोकने की कार्रवाई करें।",
        ]
    return "\n".join(lines)