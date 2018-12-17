# -*- coding: utf-8 -*-
import os, pickle, argparse, time


class Node(object):
    def __init__(self, char=None):
        self.char = char
        self.left = None
        self.right = None


class HuffmanDecoder(object):
    def __init__(self, file):
        self.file = os.path.splitext(file)[0]
        self.text_code, self.text_string = self.__readfile()
        self.root = self.__to_tree()
        self.final_text = self.__decompress()
        print('done:', len(self.final_text), 'chars')

    def __readfile(self):
        """
        Load pkl and bin files, and convert the binary array into a long string.
        :return: word-frequency dictionary, and the string of compressed code
        """
        text_code = pickle.load(open(self.file + '-symbol-model.pkl', 'rb'))
        padding = text_code.pop('padding_length')
        text_bin = open(self.file + '.bin', 'rb').read()
        text_string = (''.join([bin(i)[2:].zfill(8) for i in text_bin]))[:-padding]
        return text_code, text_string

    def __to_tree(self):
        """
        Rebuild the huffman tree.
        :return: root of the huffman tree
        """
        root = Node(None)
        for char in self.text_code.keys():
            node = root
            for code in self.text_code[char]:
                if code == '0':
                    node.left = node.left if node.left else Node(None)
                    node = node.left
                else:
                    node.right = node.right if node.right else Node(None)
                    node = node.right
            node.char = char
        return root

    def __decompress(self):
        """
        Decompress by traverse the huffman tree, no recursion. Save decompressed txt file.
        :return: decompressed text
        """
        final_text = ''
        node = self.root
        for i in self.text_string:
            node = node.left if i == "0" else node.right
            if node.char:
                final_text += node.char
                node = self.root
        open(self.file + "-decompressed.txt", 'w', encoding='utf-8', newline='\n').write(final_text)
        return final_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="pass infile to huff-compress/decompress for compression/decompression")
    args = parser.parse_args()
    start = time.time()
    decompress = HuffmanDecoder(args.infile)
    end = time.time()
    print("decode the compressed file: ", end - start)
