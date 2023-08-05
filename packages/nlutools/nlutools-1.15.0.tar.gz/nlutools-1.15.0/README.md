# NLUTOOLS: NLU 工具包

nlutools 是一系列模型与算法的nlu工具包，提供以下功能：

1. 切词
2. 切句
3. 词向量
4. 句向量
5. 语言模型
6. 实体
7. 情感分析
8. 关键字提取
9. 句子相似性计算
10. 动宾提取
11. 句子合理性判定
12. 实体相关

## 切词

切词工具暂时提供四种模式，接口函数：cut(text, mode, pos, cut_all)

其中

* text 为要切词的原始文本

* mode 为分词模式，可选值为字符串类型'fast', 'accurate'，其中accurate模式暂时不可用，正在改进中

* pos为词性保留选项，可选值为True、False，其值为True则保留词性，反之则不保留词性

* cut_all为切词粒度控制，可选值为True、False，其值为False则全部保留名词短语，为True则只保留不可切分的名词短语

调用方式为：

```python
from nlutools import tools as nlu
nlu.cut('这是一个能够输出名词短语的分词器，欢迎试用！', pos=True, cut_all=False, mode='fast')
```

返回结果：

```json
{
    'np': ['名词_短语', '分词器'], 
    'text': '这是一个能够输出名词短语的分词器，欢迎试用！', 
    'items': ['这', '是', '一个', '能够', '输出', '名词', '短语', '的', '分词器', ',', '欢迎', '试用', '!'], 
    'pos': ['r', 'v', 'm', 'v', 'v', 'np', 'np', 'uj', 'np', 'x', 'v', 'vn', 'x']
}
```

## 切句

切句工具提供两种模式，接口函数：getSubSentences(text,mode)

其中

* text 为需要进行切句的原始文本

* mode 为切句模式，可选值为 0、1 ，为 0 表示快速模式（规则分句），为 1 则表示精确模式（句法分句）

调用方式：

```python
from nlutools import tools as nlu
nlu.getSubSentences('我喜欢在春天去观赏桃花，在夏天去欣赏荷花，在秋天去观赏红叶，但更喜欢在冬天去欣赏雪景。', mode=1)
```

返回结果：

```json
['我喜欢在春天去观赏桃花', '在夏天去欣赏荷花 在秋天去观赏红叶', '但更喜欢在冬天去欣赏雪景']
```

## 词向量

词向量工具提供以下功能：

1. 获得nlu小组词向量文件，可以根据版本号获取，目前版本号包括：v1.0

   默认是下载最新版。获取到的文件夹下面包含两个文件，一个是词向量文件，一个是字向量文件。

   获取方式如下:

    ```python
    from nlutools import tools as nlu
    nlu.getW2VFile('v1.0', '/local/path/')
    ```

2. 若不想下载词向量文件，可以直接使用一下方式获得词向量：

    ```python
    from nlutools import tools as nlu
    nlu.getWordVec('深度学习')
    # 或者传入多个词
    nlu.getWordVec(['深度学习', '机器学习'])
    ```

3. 获取词向量相似的词:

    ```python
    from nlutools import tools as nlu
    nlu.getMostSimiWords('深度学习', 10)  # 10表示最多返回10个最相似的词
    # 或者传入多个词
    nlu.getMostSimiWords(['深度学习', '机器学习'], 10)
    ```
  
## 句向量

将不同长度的句子转换为固定大小的向量表示

### 基于fasttext
调用方式：

```python
from nlutools import tools as nlu
nlu.getSentenceVec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'])
```

返回结果：

```json
{
    'dimention': 300,  # 维度
    'veclist': [[0.01, ...,0.56],[0.89,...,-0.08]]
}
```
### 基于bert
调用方式：

```python
nlu.getBertSentenceVec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'],'char') # 返回字向量
nlu.getBertSentenceVec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'],'sent') # 返回句向量
```

返回结果：
```
返回的字向量维度为768，句子做大长度为128个字
返回的句向量维度为768
```

## 语言模型

待补充

## 实体

待补充

## 情感分析

返回句子的情感极性，暂时支持正向和负向情感
方法: predictEmotion(sentences,prob)
参数说明：
* sentences 输入的文本，str list
* prob 值为False，不返回预测句子的情感预测得分，只返回情感类别（pos或者neg）；值为True，则都返回。

调用方式：

```python
from nlutools import tools as nlu
nlu.predictEmotion(['这家公司很棒','这家公司很糟糕'], prob=False)
```

返回结果：

```json
{
    'text': ['这家公司很棒','这家公司很糟糕'],
    'labels': ['pos','neg']
}
```

## 关键字提取
方法：getKeywords(content,topk,with_weight)

参数说明：
* content 为输入文本，str
* topk 为最大返回关键字个数，int
* with_weight 是否返回关键字的权值， boolean

调用方式：
```python
from nlutools import tools as nlu
nlu.getKeywords('主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作',4,True)
```
返回结果：
```json
{'weights': [9.64244, 9.36891, 6.2782, 5.69476], 'keywords': ['机器学习算法', '神经网络', '训练', '模型']}
```


## 句子相似度计算
方法: getSentenceSimi(text1,text2,precision)

参数说明：
* text1 为待计算句子1
* text2 为待计算句子2
* precision 为计算结果刻度，如1000，则返回0~1000的值

调用方式：
```python
from nlutools import tools as nlu
nlu.getSentenceSimi('你家的地址是多少','你住哪里',1000)
```
返回结果:
```json
{'result': 7340}
```

## 动宾提取
方法: getVOB(content,mode）
参数说明:
* content 输入文本，str
* mode 提取模式，可选值为 fast 或accurate， str

调用方式：
```python
from nlutools import tools as nlu
nlu.getVOB('要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作','fast')

```
返回结果：
```json
{'content': [['编写', ' 代码']]}
```

## 句子合理性判别
方法： getSentenceRationality(text,with_word_prob)
参数说明：
* text, 带判定句子,类型是list
* with_word_prob,返回结果中是否包含每个词合理性的概率，str，取值范围为 'true' 或 'false'

调用方式：
```python
from nlutools import tools as nlu
nlu.getSentenceRationality(['床前明月光，疑是地上霜', '床前星星光，疑是地上霜', '床前白月光，疑是地上霜'],'false')
```

返回结果：
```json
 {
    'text': ['床前明月光，疑是地上霜', '床前星星光，疑是地上霜', '床前白月光，疑是地上霜'],//类型list
    'ppl': [63.4301, 187.3655, 71.4521],//每个句子的困惑度，数值越低表示句子越合理， 类型list
    'word_prob': [[0.0665, 0.578, 0.1343, 0.7778, 0.0024, 0.9114, 0.3427, 0.078, 0.0005, 0.0295, 0.0], [0.0105, 0.0326, 0.0016, 0.0744, 0.0022, 0.2793, 0.0401, 0.0795, 0.0024, 0.0309, 0.0], [0.0625, 0.4036, 0.0017, 0.1975, 0.0414, 0.8488, 0.2936, 0.0862, 0.0009, 0.0255, 0.0]] //对应每个句子中每个字的合理性概率，类型list
 }
```

## 实体相关
方法：doEntityTask(text,m)
参数说明：
* text， 待分析的句子，类型是list
* m，待调用的实体服务类型，类型是str，可选值暂时只有'ner'

调用方式：
```python
from nlutools import tools as nlu
nlu.doEntityTask(["我毕业于北京大学"],'ner')
```
返回结果：
```json
 [[{'boundary': [4, 8], 'type': 'school', 'text': '北京大学', 'entityIdCandidates': [{'entityName': '', 'entityID': '0', 'score': 1.0}]}]]
```
