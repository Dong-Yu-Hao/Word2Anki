# Word2Anki
>这几乎是最好的语言学习方式。如果不是，我倒想试试你的。

## 为什么要做Word2Anki？
在漫漫语言学习路上，我一直没有放弃对效率的追求。我们在学校中接受的教育是，学语言就是要把单词、语法和语用都背下来，这套方法确实可以应付考试与一部分生活场景，但是就如许多人一样，当有人问出 "How are you？" 之后，你却只能回答 "I'm fine, Thank you."。学习的目的是为了让我们处理我们从未见过的情景，但背诵只能让我们应对有限的情景。
直到某天我接触到了新的学习理论，一个是来源于[ Yjango ](https://space.bilibili.com/344849038)的[《背多少单词才会说英语？5000 还不够吗？【学习观 | 问与答02】》](https://www.bilibili.com/video/BV1GV411S7Cb/)，另一个是[ 罗肖尼Shawney ](https://space.bilibili.com/323794482)的[《【高能干货】这个视频将会颠覆你对英语学习的认知——总述·阅读篇》](https://www.bilibili.com/video/BV1aD4y127GE/)。这两个视频总结后能够得出一个理论，语言学习需要在***正确情景***下多看***难度适度***的***句子***。
问题是市面上几乎不存在这样的产品，有些软件会给出例句，但同时也会给出无法消去的中文，这就是无法满足情景的要求。看原著能够获得正确的情景，但难度会过高过低，无法控制。而传统的背单词软件最大的问题就是他是在背单词，而不是在学英语。所以为了解决以上问题，我开发了Word2Anki，希望用我稚嫩的技术解决这些问题。

## Word2Anki 是什么？
Word2Anki 是一个自动为单词附加释义、例句的工具。W2A 会根据你的语言能力使用 GPT 为每一个单词附加一个源语言释义与几个源语言例句。能够同时满足「可理解性输入假说」与「学习观」的理论。经过实测，学习效率确实有了极大的提升。比如说学完当天我去看电影，当主人公沉入水中时，我脑海中思考使用的是英文"Sank"而不是中文。

Word2Anki 会 生成 Markdown 格式的表格。
| Word        | Definition                                              | Example Sentences                                                                                                 |
|-------------|---------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Consecutive | Following in order without interruption                 | 1. The team won five consecutive games.<br>2. They have lived in the same house for five consecutive years.<br>3. Mary got three consecutive A's on her tests.<br>4. There were three consecutive days of rain.<br> |
| Upgrade     | To improve or make better                                | 1. The company plans to upgrade their software.<br>2. She upgraded to a bigger car.<br>3. We need to upgrade our security measures.<br>4. The restaurant upgraded their menu. <br>          |

## 如何使用 Word2Anki？
### 1.收集单词
首先您需要收集单词，这里我推荐使用COCA的语料库高频词汇，它收集了语料库中出现频率最多的词汇。在文件中我也附上了COCA5000词供您测试。
### 2.格式化单词
您需要使用一个逗号与一个空格（", "）分割每一个单词，这不需要手工操作，您可以直接让向ChatGPT提出要求。
### 3.调试代码
3.0. ~您需要先安装 Python 与 VS Code~

3.1. 首先您需要有 OpenAI 的官方库：您可以通过 `pip install openai` 的方式获得，如果是Python3可以使用`pip3 install openai`。如果下载过慢可以使用代理。

3.2. 您需要输入您的 OpenAI KEY：您可以使用[OpenAI的官方API](https://platform.openai.com/account/usage)，也可以使用[第三方的API](https://api2d.com/)，第三方API可以在国内为您提供更稳定的链接与更快的速度。您需要填写API KEY 与服务端点。
```python
openai.api_key = "<API-KEY>" #不管是第三方还是官方的 API KEY 都输入到这里即可
#如果你用的是官方API就把此行删掉或者注释掉, 如果是第三方就填写第三方的服务端点，比如API2D的服务端点就是：https://openai.api2d.net/v1
openai.api_base = "<服务端点>" 
```
3.3. 非必须，如果您需要转制非英语的单词，可以把Prompts通过GPT翻译为其他语言。翻译完成后要按照格式正确放回。
```markdown
prompts = As a professional flashcard maker, your task is to create a set of flashcards based on the words provided. The format for each card should be a markdown table with three columns: word, definition, and example sentences. Each card should contain one word, its definition, and {num_example} example sentences. Please ensure that each word is included in the set and that there is only one flashcard per word. Keep the flashcards simple and clear, with definitions and example sentences that are understandable for someone with a vocabulary of {difficulty} words. For clarity, please number each example sentence and separate them using <br>. Use this format for each card: | Word | Definition | Example Sentences | |------|------------|------------------| | | | 1.<br>2.<br>3.<br>4.<br>| Please note that you have flexibility in how you present the information within these guidelines.Please do not have any text outside of the table.
words:
```
3.4. 在text中填入您需要制卡的单词，随后运行此脚本即可。脚本会自动在同文件夹内生成一个 output.txt 用来存储每次产生的表格。虽然没有设计多线程，但您可以使用spread_words.py将单词分成多份,例如将5000词分成10份500词。然后复制多份脚本，为每一份脚本修改其中的output.txt命名，就可以简陋地多线程运行。
```python
# 原有的命名，每个脚本中有两处，都需要修改
file = open("output.txt", "w")
file = open('output.txt', 'a')

# 修改后的命名，你需要为每一份脚本设置一个不同的命名，不能重复。
file = open("output1.txt", "w")
file = open('output1.txt', 'a')
```
3.5. 制作中止了怎么办？由于不明机制，使用API时会储存原有的所有问答，您只需要重启脚本就能重新获得所有的内容。不会消耗Token。

### 4.转换表格
脚本结束运行后，所有内容会以Markdown表格的形式储存在 output.txt 文件中，您可以输入至Notion一类Markdown编辑器中，然后将表格复制到 Excel 或 Numbers 中，将表格排序，删除掉所有表头，如有需要也可以用表格自带的功能[去掉所有相同项目](https://support.microsoft.com/zh-cn/office/%E7%AD%9B%E9%80%89%E5%94%AF%E4%B8%80%E5%80%BC%E6%88%96%E5%88%A0%E9%99%A4%E9%87%8D%E5%A4%8D%E5%80%BC-ccf664b0-81d6-449b-bbe1-8daaec1e83c2)。最后导出为CSV表格即可输入AnkiCard。

### 5.设置Anki
[![iSrWrC.png](https://i.328888.xyz/2023/04/23/iSrWrC.png)](https://imgloc.com/i/iSrWrC)
1. 下载并打开Anki后，点击浏览
2. 找到笔记模版并点击，右键管理创建一个新的笔记模版
3. 添加一个笔记模版
4. 选择你需要的模版（可以直接选择 Basic），创建一个笔记模版
5. 确定

[![iSrtAE.png](https://i.328888.xyz/2023/04/23/iSrtAE.png)](https://imgloc.com/i/iSrtAE)
1. 选择你刚刚创建的笔记模版
2. 点击字段
3. 添加新的字段
4. 为新的字段命名
5. 确定

[![iSrU9Q.png](https://i.328888.xyz/2023/04/23/iSrU9Q.png)](https://imgloc.com/i/iSrU9Q)
1. 通过重命名与重排位置，让字段如图所示。最后选择确定

[![iSrDBH.png](https://i.328888.xyz/2023/04/23/iSrDBH.png)](https://imgloc.com/i/iSrDBH)
0. 将CSV文件拖入Anki
1. 将分隔符设置为逗号
2. 选择你刚刚创建的笔记模版
3. 选择你要放置卡片的位置，建议直接选择默认
4. 设置好字段匹配
5. 导入


### 6.使用
完成以上操作即可使用，如果您不喜欢顺序学习，也可以用Anki将卡片[随机排序](https://www.bilibili.com/video/BV12g411a7kj/)。
