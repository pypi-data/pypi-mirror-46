```
import gensim
# datatype=np.float 最快
# datatype=np.float 最省内存
model = gensim.models.KeyedVectors.load_word2vec_format('./Tencent_AILab_ChineseEmbedding.txt', datatype=np.float)
```

[无监督词向量][1]


---
[1]: https://x-algo.cn/index.php/2018/11/12/3083/