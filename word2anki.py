import openai

# 在此处输入你的API与服务端点
openai.api_key = "<API-KEY>" 
openai.api_base = "<服务端点>" 

# 在此处调节参数
num_example = str(input("请输入你需要几个例句，一般为3~5个>>>"))
print("下面输入你需要的抽认卡释义与例句的难度，由于单词本身就是难度 i+1 的可理解输入，难度建议尽量调低一些，可以采用自己真实词汇量的一半。首次使用时可以用几个单词测试一下输出的难度是否符合 i+1")
difficulty = str(input("请输入难度，用词汇量衡量，使用整数>>>"))

# 在text中填入你需要制卡的单词，请注意格式
text = "consecutive, upgrade, associate, accurately, strictly, leak"
words = text.split(", ")
# 由于Token的限制，每次可以制作的单词数量是有限制的，根据经验设置为每次制作30个单词，如果您需要也可以适当修改调整。
chunks = [words[i:i+30] for i in range(0, len(words), 30)]
count = 0
# 此处将创建一个txt文件存储表格
file = open("output.txt", "w")

for chunk in chunks:
    count += 1
    print(f"第{count}次运行")
    print("本次制作的单词是[", ", ".join(chunk), "]")
    # 您可以通过更改 Prompts 的语言改变最终输出的内容。使用ChatGPT即可翻译。
    prompts = f"""As a professional flashcard maker, your task is to create a set of flashcards based on the words provided. The format for each card should be a markdown table with three columns: word, definition, and example sentences. Each card should contain one word, its definition, and {num_example} example sentences. Please ensure that each word is included in the set and that there is only one flashcard per word. Keep the flashcards simple and clear, with definitions and example sentences that are understandable for someone with a vocabulary of {difficulty} words. For clarity, please number each example sentence and separate them using <br>. Use this format for each card: | Word | Definition | Example Sentences | |------|------------|------------------| | | | 1.<br>2.<br>3.<br>4.<br>| Please note that you have flexibility in how you present the information within these guidelines.Please do not have any text outside of the table.
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