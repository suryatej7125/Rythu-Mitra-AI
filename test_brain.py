from brain import get_agriculture_answer

# This is the question received from Gnani Speech-to-Text
farmer_question = "నమస్కారం నా పత్తి పంట ఆకులు పసుపు రంగులోకి మారుతున్నాయి దీనికి కారణం ఏమిటి"

print("\nFarmer's Question:")
print(farmer_question)

print("\nRythu Mitra AI is thinking...")

result = get_agriculture_answer(farmer_question)

if result["success"]:

    print("\nCrop Identified:", result["crop"])
    print("Keywords Matched:", result["matched_keywords"])

    print("\nRythu Mitra AI Answer:")
    print(result["answer_te"])

else:

    print("\nRythu Mitra AI:")
    print(result["answer_te"])