#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:08:54 2021

@author: kumardeepanshuverma
"""
import heapq
import os
class BinaryTreeNode:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.right=None
        self.left=None
    def __lt__(self,other):
        return self.frequency<self.other
    def __eq__(self,other):
        return self.frequency==self.other
class Huffmancoding:
    def __int__(self,path):
        self,path=path
        self.__heap=[]
        self.__codes={}
        self.__reversecodes={}
    def __make_frequency_dict(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            freq_dict[char]+=1
        return freq_dict
    def __buildheap(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            binarytreenode=BinaryTreeNode(key, frequency)
            heapq.heappush(self.__buildheap,binarytreenode)
    def __buildtree(self):
        while (len(self.__heap)>1):
            binarytree_node_1=heapq.heappop(self.__heap)
            binarytree_node_2=heapq.heappop(self.__heap)
            freq_sum=binarytree_node_1+binarytree_node_2
            newnode=BinaryTreeNode(None,freq_sum)
            newnode.left=binarytree_node_1
            newnode.right=binarytree_node_2
            heapq.heappushpop(self.__heap,newnode)
        return
    def __buildcodesHelper(self,root,curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__codes[root.value]=curr_bits
            self.__reversecodes[curr_bits]=root.value
            return
        self.__buildcodesHelper(root.left, curr_bits+"0")
        self.__buildcodesHelper(root.right, curr_bits+"1")
    def __buildcodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildcodesHelper(root,"")
    def __getencodedtext(self,text):
        encoded_text=" "
        for char in text:
            encoded_text+=self.__codes[char]
        return encoded_text
    def __getpaddedencodedtext(self,encoded_text):
        padded_amount=8-(len(encoded_text)%8)
        for i in range(padded_amount):
            encoded_text+='0'
        padded_info={"0.08b"}.format(padded_amount)
        padded_Encoded_text=padded_amount+encoded_text
        return padded_Encoded_text
    def __getbytesarray(self,padded_Encoded_text):
        array=[]
        for i in range(0,len(padded_Encoded_text),8):
            byte=padded_Encoded_text[i:i+8]
            array.append(int(byte))
        return array
    
    def compress(self):
        #Get the file from path
        file_name,file_extension=os.path.splitext(self.path)
        #Read text from file
        output_path=file_name+".bin"
        with open(self.path,'r+') as file,open(output_path,'wb') as output:
            text=file.read()
            text=text.rstrip()
        #make freq dictionary using the text
        text="ncebedwdjeb"
        freq_dict=self.__make_frequency_dict(text)
        #Construct heap from freq_dict
        self.__buildheap(freq_dict)
        #construct the binary tree from heap
        self.__buildtree()
        #construct codes from the binary tree
        self.__buildcodes()
        #creating the encoded text using the codes
        encoded_text=self.__getencodedtext(text)
        #put this encoded text into the binary file
        padded_Encoded_text=self.__getpaddedencodedtext(encoded_text)
        #pad this encoded path
        bytes_array=self.__getbytesarray(padded_Encoded_text)
        final_bytes=bytes(bytes_array)
        output.write(final_bytes)
        print('compressed')
        return output_path
        #return this binary file as output
    def __removepadding(self,text):
        padded_info=text[:8]
        extra_padding=int(padded_info,2)
        text=text[8:]
        text_after_padding_removed=text[:-1*extra_padding]
        return text_after_padding_removed
    def __decodetext(self,text):
        decoded_text=" "
        current_bits=" "
        for bit in text:
            current_bits+=bit
            if current_bits in self.__reversecodes:
                character=self.__reversecodes[current_bits]
                decoded_text+=character
                current_bits=" "
        return decoded_text
    def decompress(self,input_path):
        filenmae,file_extension=os.path.splitext(self.path)
        output_path=filenmae+"decompress"+".txt"
        with open(input_path,'rb')as file,open(output_path,'w')as output:
            bit_string=" "
            byte=file.read()
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read()
            actual_text=self.removepadding(bit_string)
            decompressed_text=self.__decodetext(actual_text)
            output.write(decompressed_text)
            return
        
path='users/desktop/sample.txt'
h=Huffmancoding(path)
output_path=h.compress()
h.decompress(output_path)