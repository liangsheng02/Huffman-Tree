# Huffman-Tree
A Huffman Tree approach using binary search for text compress/decompress

## How to Use
To compress: 
```python huff-compress.py mobydick.txt [-s {char, word}]```

To decompress:
```python huff-decompress.py mobydick```

To test: 
```python test-harness.py mobydick.txt  [-s {char, word}]```

## Implementation
Two python files huff-compress.py and huff-decompress.py was created in the implementation, Both of the files can be called by command line, and the evaluation file test-harness.py.

The huff-compress.py is aimed to achieve compression of the input text file by Huffman coding on character level or word level. By defining a HuffmanCompress class, these all could be executed in its initializer. Firstly, the to_dic() method read the input text file into a string and then built a dictionary to store symbol-frequency pairs. A regular expression would be used to split the text into a list of words if chose word level. Secondly, the to_tree() method built a Hu􀁼man tree and returned the root of the tree. Here a binary_search() method was used to help speed up the process, which also led to a lower compression ratio. Finally, the compress() method encoded the text into a binary array of codes, and saved the model and compressed text into new files respectively.

The huff-compress.py, conversely, decompressed the text. The readfile() method loaded .pkl and .bin files, and returned the symbol-frequency dictionary. Then, by to_tree() method, the same Huffman tree was reconstructed with the dictionary. At last, decompress() method traversed the Huffman tree in a faster non-recursion way, then decoded the text into readable words and stored it into a .txt file.

## Performance
The performance is shown below.

| level | original | .bin file | .pkl file | build model | encode model | Compress | Decompress |
| :---: | :-------------: | :-----------: | :-----------: | :---------: | :----------: | :-----: | :----------: |
| char  | 1,220,150 bytes | 919,856 bytes |  1,833 bytes  |    0.25s    |    1.24s     | 1.50s |    1.21s     |
| word  | 1,220,150 bytes | 459,860 bytes | 832,473 bytes |    0.35s    |    0.70s     | 1.06s |    0.68s     |

## Improvement
There are two main directions for improvement, one is to increase the speed of compress/decompress, another is to improve the compression rate.

The method which builds the Huffman tree is the key to improve compression rate. With the same symbol-frequency dictionary, there are different ways to construct a Huffman tree, which will lead to different compression rates, since there are many words/characters have the same frequency. In this implementation, a binary search is used when finding the index that a node should be inserted. This speeded up the tree building significantly , while decreased the compression ratio. Because in this way the lengths of many words/characters code tend to be closed. So, instead of binary search, a simple for loop would be better for compression rate. In addition, according to the performance, the
compressed file of character level would be smaller than word level, while the encode file would be larger than using word-based model.

For the speed of compress/decompress, there are two main aspects. First, the sorting method that just discussed will influence the compression rate and speed when building model. Second is the traverse method when encoding model and encoding model. When encoding model, a more intuitive approach is to use recursion, which would be just a little bit slower than iteration. However, when decoding model, recursion may cost much more time than iteration.

As to the difference between word level and character level in this implementation, it's obviously that character level compress or decompress is slower than word level. And the model file (.pkl) of character level would be smaller than that of word level, while the encode file (.bin) would be larger than using word-based model. This is related to the size of the text file. When the size of the text increase, the frequency of the same word also increase, so that the size of the model 􀁿le would be increase slowly, the total size of model file and encode file using word level would be larger than character level. So, when the size of text file is not very large (e.g. mobydick.txt), character level would be better.
