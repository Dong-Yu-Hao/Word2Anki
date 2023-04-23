import openai

openai.api_key = "fk194869-1QiRYNZA8BfJsve6eXsd3nEfULeTKtk1" 
openai.api_base = "https://openai.api2d.net/v1" # 注意这里结尾有 /v1
### input words that you want
text = "consecutive, upgrade, associate, accurately, strictly, leak"
words = text.split(", ")
chunks = [words[i:i+30] for i in range(0, len(words), 30)]
count = 0
file = open("output.txt", "w")

for chunk in chunks:
    count += 1
    print(f"第{count}次运行")
    print("本次制作的单词是[", ", ".join(chunk), "]")
    prompts = """As a professional flashcard maker, your task is to create a set of flashcards based on the words provided. The format for each card should be a markdown table with three columns: word, definition, and example sentences. Each card should contain one word, its definition, and four example sentences. Please ensure that each word is included in the set and that there is only one flashcard per word. Keep the flashcards simple and clear, with definitions and example sentences that are understandable for someone with a vocabulary of 2000 words. For clarity, please number each example sentence and separate them using <br>. Use this format for each card: | Word | Definition | Example Sentences | |------|------------|------------------| | | | 1.<br>2.<br>3.<br>4.<br>| Please note that you have flexibility in how you present the information within these guidelines.Please do not have any text outside of the table.The first letter of each word needs to be capitalized.
    words:\"""" + ", ".join(chunk) + "\""

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens = 3000,
    messages=[
        {"role": "user", "content":prompts}
    ]
    )

    message = completion.choices[0].message
    content = message.get("content", "")
    print(content)
    file = open('output.txt', 'a')
    file.write(content + '\n')
    file.close()
    print("已成功加入到文件中，开始下一次运行")