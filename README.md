### Persian Generative Chatbot

A repo dedicated to different approaches in building a Persian Generative Chatbot.

### Data

We need a dataset of conversation pairs to build a chatbot.

### 1- Ninisite

[ninisite](ninisite.com) is a persian forum with millions of conversation pairs on different life-style topics. We wrote a [simple script](/data/ninisite/) to crawl the conversation pairs, like the following sample:

```
{
    "topic": "بیمارستان هدایت تهران برای زایمان چطوره؟",
    "question": [
        "سلام خانما",
        "من تو بیمارستان میلاد برای بارداری و زایمان پرونده دارم.اما بیمار کرونایی بستری داره و فعلا هم تعطیله.",
        "شنیدم بیمارستان هدایت فقط زنان و زایمانه؟کسی چکاپ های بارداری و زایمانش رو تو هدایت انجام داده؟راضی بودین؟",
        "لطفا راهنماییم کنید"
        ],
    "answer": [
        "آره من 26سال پیش اونجا بدنیا اومدم مامانم ک خیلی تعریف میکرد ."
        ]
}
```

The following table shows some stats on the process of crawling the dataset (The table is getting updatad constantly).

| Total Targeted Topics |  Crawled  | Crawled Conversation Pairs |  Size  |
| :-------------------: | :-------: | :------------------------: | :----: |
|        636921         | 8871 (1%) |           206507           | 175 MB |
