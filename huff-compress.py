# -*- coding: utf-8 -*-
import os, re, array, pickle, argparse, time, sys


class Node(object):
    def __init__(self, char=None, value=None):
        self.char = char
        self.value = value
        self.left = None
        self.right = None


def binary_search(target, arr):
    """
    Binary search method for a sorted list of Node class objects.
    :param target: a Node object
    :param arr: a sorted list of Node objects
    :return: the index that target should insert into arr
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid].value < target.value:
            left = mid + 1
        elif arr[mid].value > target.value:
            right = mid - 1
        else:
            return mid
    return -1


class HuffmanCompress(object):
    def __init__(self, level, text_path):
        start1 = time.time()
        self.text_path, self.level = text_path, level
        self.text, self.text_fre = self.__to_dic()
        self.root, self.text_code = self.__to_tree()
        end1 = time.time()
        print('build the symbol model: ', end1 - start1)
        start2 = time.time()
        self.__compress()
        end2 = time.time()
        print('encode the symbol model: ', end2 - start2)

    def __to_dic(self):
        """
        Build a dictionary to store words and their frequency.
        :return: a string of input txt file, and a word-frequency dictionary
        """
        with open(self.text_path, encoding='utf-8') as f:
            text = f.read()
        if self.level == 'word':
            text = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(text)
            # Get words and punctuations. Another method: text = [i for i in re.split(r'(\W)', text) if i != '']
        text_fre = {}
        for i in range(len(text)):
            word = text[i]
            text_fre[word] = text_fre[word] + 1 if word in text_fre.keys() else 1
        return text, text_fre

    def __to_tree(self):
        """
        Build huffman tree.
        :return: root of the huffman tree, and a empty dictionary to store word-code pairs later.
        """
        nodes_list = [Node(char, self.text_fre[char]) for char in self.text_fre.keys()]
        nodes_list.sort(key=lambda node: node.value)
        while len(nodes_list) > 1:
            parent_node = Node(None, nodes_list[0].value + nodes_list[1].value)
            parent_node.left = nodes_list.pop(0)
            parent_node.right = nodes_list.pop(0)
            index = binary_search(parent_node, nodes_list)
            nodes_list.insert(index, parent_node)
        root = nodes_list[0]
        text_code = {}
        return root, text_code

    def __traverse(self, node, binary_code=''):
        """
        Traverse the huffman tree by recursion to give each word a code.
        :param node: a Node class object, initial value = root
        :param binary_code: the code of current node, initial value = ''
        """
        code_list = binary_code
        if node.char:
            self.text_code[node.char] = code_list
        else:
            self.__traverse(node.left, code_list+'0')
            self.__traverse(node.right, code_list+'1')

    def __padding(self):
        """
        Convert input txt file into a long string text_code, and add '0' at the end to ensure its length is a multiple of 8.
        :return: string, number of padding '0's
        """
        self.__traverse(self.root)
        text_code = ''.join([self.text_code[char] for char in self.text])
        if len(text_code) % 8 != 0:
            padding = (8 - (len(text_code) % 8))
            text_code += '0' * padding
        else:
            padding = 0
        return text_code, padding

    def __to_binary(self):
        """
        Build a binary array to store the code of input txt file.
        :return: binary array, number of padding '0's
        """
        text_code, padding = self.__padding()
        string = ''
        compress_text = array.array('B')
        for i in text_code:
            string += i
            if len(string) == 8:
                compress_text.append(int(string, 2))
                string = ''
        return compress_text, padding

    def __compress(self):
        """
        Compress input txt file.
        """
        compress_text, padding = self.__to_binary()
        compress_text.tofile(open(os.path.splitext(self.text_path)[0] + '.bin', "wb"))
        self.text_code['padding_length'] = padding
        pickle.dump(self.text_code, open(os.path.splitext(self.text_path)[0] + '-symbol-model.pkl', "wb"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="specify character- or word-based Huffman encoding", choices=["char", "word"])
    parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
    args = parser.parse_args()
    start = time.time()
    compress = HuffmanCompress(args.s, args.infile)
    end = time.time()
    print("compress time: ", end - start)