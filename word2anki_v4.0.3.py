""" 
4.0.3 相较于 4.0.2
1. 增加了 prompt 参数自定义功能, 可以调节例句数量, few-shot, prompt语言, 自定义单词等等
2. 通过统计、计算与实验, 默认每线性每次制作的单词数为10, 调整Max_token为3500
3. 可以自动翻译prompt, 方便其他语言学习的需求
4. 增加了提醒与基本的教程，避免初次使用出现比较大的问题。
"""
import openai, _thread, math, time

def prompt_maker(example_count):
    prompt_left = f"As the creator of flashcards, make flashcards based on provided vocabulary. Humans need at least {example_count} example sentences containing the vocabulary to understand a word. The workload of making example sentences is huge, so it is hoped that the Meaning and example sentences can be automatically generated for the vocabulary.The flashcards are output in the form of a Markdown table (Word/Meaning/Example Sentences). Each flashcard contains a vocabulary, Meaning, and {example_count} example sentences. Make sure there are {example_count} example sentences, each numbered, and separated by <br> like this:| Word | Meaning | Example Sentences ||-|-|-|| | | "
    prompt_right = "| The first letter of each vocabulary should be capitalized. There should be no extra text outside of the table. Each vocabulary should have only one flashcard. The meaning and example sentences should be as simple as possible for beginners to understand. You can create example sentences flexibly while adhering to the premise. words: "
    for i in range(1,example_count + 1):
        prompt_process = prompt_left + f"{i}.<br>"
        prompt_left = prompt_process

    global prompt_1
    prompt_1 = prompt_left + prompt_right

def prompt_translate(language, prompt):
    prompt_translate_process = f"Please translate precisely to {language}, without any additional content besides the translation: " + "\"\"\"" + prompt + "\"\"\""
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens = 2000,
    messages=[
        {"role": "user", "content": prompt_translate_process}
    ]
    )
    message = completion.choices[0].message
    content = message.get("content", "")

    global prompt_1
    prompt_1 = content
    print("prompt: ", prompt_1, "\n")

def thread_real_count_cul():
    word_list = word_all.split(", ")
    word_count = len(word_list)
    each_thread_word_count = math.ceil(word_count / thread_all_count)

    global word_dict
    word_dict = {}
    word_splited = word_all.split(", ")
    chunks = [word_splited[i:i+each_thread_word_count] for i in range(0, len(word_splited), each_thread_word_count)]
    count_1 = 0

    for chunk in chunks:
        count_1 += 1
        word_dict[f"第{count_1}线程"] = ", ".join(chunk)

    global thread_real_count
    thread_real_count = len(word_dict) # 实际线程数
    print(f"实际线程：{thread_real_count}")
    
    return thread_real_count

def word2anki_each_thread(a):
    print(f"第{a}线程开始运行")
    time.sleep(a/10)

    text = word_dict[f"第{a}线程"]
    words = text.split(", ")
    chunks = [words[i:i+each_thread_each_make_word_count] for i in range(0, len(words), each_thread_each_make_word_count)]
    count_2 = 0
    file = open(f"output{a}.md", "w")

    for chunk in chunks:
        count_2 += 1
        print(f"第{a}线程-第{count_2}次开始运行")
        prompt_2 = prompt_1 + "\"\"\" " + ", ".join(chunk) + "\"\"\""

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens = max_tokens_set,
        messages=[
            {"role": "user", "content":prompt_2}
        ]
        )
        message = completion.choices[0].message
        content = message.get("content", "")
        
        file = open(f'output{a}.md', 'a')
        file.write(content + '\n')
        file.close()

        print(f"第{a}线程-第{count_2}次结束运行")
    
    with open(f'output{a}.md', 'r') as f1: # 打开原始文档，以只读模式 'r' 打开，使用 with 语句可以自动关闭文件
        content = f1.read() # 读取原始文档的内容
        with open("output_all.md", 'a') as f2: # 打开目标文档，以添加模式 'a' 打开
            f2.write(content) # 将原始文档的内容写入到目标文档中

if __name__ == "__main__":
    openai.api_key = "<API-KEY>" 
    # openai.api_base = "https://openai.api2d.net/v1" #第三方服务
    # 默认词汇是10个测试词汇，你可以进行修改。请注意不要一开始就大量制卡，一定要多次尝试，避免损失。
    word_all = "compromise, departure, behalf, graph, diplomatic, thief, herb, subsidy, cast, fossil"
    # 默认prompt是 word2anki_prompts_v2.2, 依据学习观与罗肖尼的理论制作。默认prompt您也可以自行修改。
    prompt_0 = "As the creator of flashcards, make flashcards based on provided vocabulary. Humans need at least 12 example sentences containing the vocabulary to understand a word. The workload of making example sentences is huge, so it is hoped that the Meaning and example sentences can be automatically generated for the vocabulary.The flashcards are output in the form of a Markdown table (Word/Meaning/Example Sentences). Each flashcard contains a vocabulary, Meaning, and 12 example sentences. Make sure there are 12 example sentences, each numbered, and separated by <br> like this:| Word | Meaning | Example Sentences ||-|-|-|| | | 1.<br>2.<br>3.<br>4.<br>5.<br>6.<br>7.<br>8.<br>9.<br>10.<br>11.<br>12.<br>| The first letter of each vocabulary should be capitalized. There should be no extra text outside of the table. Each vocabulary should have only one flashcard. The meaning and example sentences should be as simple as possible for beginners to understand. You can create example sentences flexibly while adhering to the premise. words: "
    # 每个线程中每次制作时，制作多少个单词
    each_thread_each_make_word_count = 10 
    # 线程数
    thread_all_count = 10
    # 最大 token
    max_tokens_set = 3500
    # 计数变量，没有实际含义
    num = 0
    
    choice_1 = input("是否自定义? Y-自定义参数、语言与词汇等；N-使用默认参数、默认词汇。你可以在运行前修改默认参数, 不用重复设置。\n(Y/N)>>>")
    if choice_1 == "Y":
        example_count = int(input("例句数量\n>>>"))
        prompt_maker(example_count)
        
        choice_2 = input("是否更改语言? 如果你需要制作英语外的卡片, 选择此项。\n(Y/N)>>>")
        if choice_2 == "Y":
            language = input("卡片语言\n>>>")
            print("请稍等，脚本正在自动翻译prompt中")
            prompt_translate(language, prompt_1)
        elif choice_2 == "N":
            pass

        choice_3 = input("是否修改参数？如果你更改了前项, 需要修改参数。\n(Y/N)>>>")
        if choice_3 == "Y":
            print("请注意, 如果你是第一次使用, 请不要一开始就大量转制卡片。你需要少量多次地尝试, 避免在大量制卡时出现问题, 造成损失。你尤其要注意以下几个参数的设置, 它们会极大地影响成功率。")
            thread_all_count = int(input("线程数：类似于同时有几个人帮你搬砖头, 可以大大提高效率。\n>>>"))
            each_thread_each_make_word_count = int(input("每线程每次词汇量：类似于同时几个人帮你搬砖头, 每个人面前有一堆砖头, 要搬运很多次，每线程每次词汇量就是每次要搬运的量。由于 GPT 存在 4096 个 token的上限, 每次能搬运的量是受限的, 数量越多效率越高, 但不建议超过10。\n>>>"))
            max_tokens_set = int(input("最大token：这是每次GPT能够生成卡片的上限，由于用户的prompt也算作token，所以你需要提前计算好冗余。10个词汇一般设置为3500\n>>>"))
        elif choice_3 == "N":
            pass

        choice_4 = input("是否自定义词汇? 如果你想使用其他语言或者除默认词汇的其他词汇，可以选择此项(Y/N)\n>>>")
        if choice_4 == "Y":
            word_all = input("请输入自定义词汇，每个词汇间用逗号与一个空格分割(, ),注意不要错用中文逗号(，)。如果不是, 您可以通过GPT利用[词汇间用一个逗号与一个空格分割(, ): \"<词汇>\"]来格式化。如果词汇数量多，可以修改并添加到默认词汇的变量中，也就是word_all\n>>>")
        elif choice_4 == "N":
            pass
        
        choice_5 = input("是否开始制作卡片?\n(Y/N)>>>")
        if choice_5 == "Y":
            pass
        elif choice_5 == "N":
            exit()
    elif choice_1 == "N":
        prompt_1 = prompt_0
    
    thread_real_count_cul()
    file = open("output_all.md", "w") 
    
    try:
        while num < thread_real_count:
            num += 1
            _thread.start_new_thread( word2anki_each_thread, (num,) )
    except:
        print ("Error: 无法启动线程")
    while 1:
        pass