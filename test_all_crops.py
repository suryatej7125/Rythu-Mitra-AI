from brain import get_agriculture_answer

test_questions = [
    {
        "crop": "COTTON",
        "question": "నా పత్తి పంట ఆకులు పసుపు రంగులోకి మారుతున్నాయి"
    },
    {
        "crop": "PADDY",
        "question": "నా వరి పంటలో కాండం తొలిచే పురుగు సమస్య ఉంది"
    },
    {
        "crop": "CHILLI",
        "question": "నా మిరప మొక్కల ఆకులు ముడుచుకుంటున్నాయి"
    },
    {
        "crop": "UNKNOWN",
        "question": "నాకు వాతావరణం గురించి చెప్పండి"
    }
]

print("\n================================")
print("       RYTHU MITRA AI")
print("    AGRICULTURE BRAIN TEST")
print("================================")

for test in test_questions:

    print("\nTesting:", test["crop"])
    print("Question:", test["question"])

    result = get_agriculture_answer(test["question"])

    if test["crop"] == "UNKNOWN":

        if not result["success"]:
            print("PASS: Safe fallback working!")
        else:
            print("FAIL: Unexpected knowledge match!")

    elif result["success"]:

        print("PASS: Knowledge found!")
        print("Crop:", result["crop"])
        print("Answer:", result["answer_te"])

    else:
        print("FAIL: Knowledge not found!")

print("\n================================")
print("         TEST COMPLETED")
print("================================")