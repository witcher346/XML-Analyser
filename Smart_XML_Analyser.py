#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import sys


# In[199]:


def find_origin_btn(input_origin_file):
    with open(input_origin_file, 'r') as html:
        contents = html.read()
        
        soup = BeautifulSoup(contents, features='html.parser')
        
        btn = soup.find('a', {'id': 'make-everything-ok-button'})
        
        return btn


# In[139]:


def count_children(tag):
    tags_parent = tag.parent
    children = [x for x in list(tags_parent.children) if x != '\n' and x.name == tag.name]
    for i, child in zip(range(0, len(children)), children):
        if child == tag:
            return i


# In[144]:


def build_path(tag):
    path = str(tag.name)
    parent = ''
    while True:
        parent = str(tag.parent.name)
        if parent == 'body':
            path = parent + '/' + path
            break
        else:
            index = count_children(tag.parent)
            if index > 0:
                path = parent + f'[{index}]' + '/' + path
            else:
                path = parent + '/' + path
            tag = tag.parent

    return f'html/{path}'


# In[145]:


find_origin_btn('sample-0-origin.html')


# In[219]:


def find_different_btn(input_diff_file, origin_file):
    with open(input_diff_file, 'r') as html:
        contents = html.read()

        soup = BeautifulSoup(contents, features='html.parser')
        
        buttons = soup.find_all('a', {'class': 'btn'})
        
        original_btn = find_origin_btn(origin_file)
        original_btn.attrs.pop('id', None)
        
        similarity_count = 0
        
        for btn in buttons:
            if len(btn.attrs) == len(btn.attrs):
                
                for attr_dif_btn, attr_origin_btn in zip(btn.attrs, original_btn.attrs):
                    similarity_count += 1 if btn.attrs[attr_dif_btn] == original_btn.attrs[attr_origin_btn] else 0
                    
                similarity_count += 1 if btn.text == original_btn.text else 0
                
                if similarity_count > 2:
                    path = build_path(btn)
                    return path
                else:
                    continue


# In[220]:


find_different_btn('sample-2-container-and-clone.html', 'sample-0-origin.html')


# In[221]:


def analyse(input_origin_file, input_diff_file):
    path = find_different_btn(input_diff_file, input_origin_file)
    print(path)


# In[222]:


analyse(sys.argv[1], sys.argv[2])


# In[ ]:




