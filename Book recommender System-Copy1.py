#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
books = pd.read_csv('BX-Books.csv', sep=";", error_bad_lines=False, encoding='latin-1')


# In[3]:


books.columns


# In[4]:


books=books[['ISBN','Book-Title','Book-Author','Year-Of-Publication','Publisher']]


# In[5]:


books.head(2)


# In[ ]:





# In[6]:


books.rename(columns={'Book-Title':'title','Book-Author':'author','Year-Of-Publication':'Year','Publisher':'publisher'},inplace=True)


# In[ ]:





# In[7]:


books.rename(columns={'Book-Title':'title','Book-Author':'author','Year-Of-Publication':'year','Publisher':'publisher'},inplace=True)


# In[8]:


books.head(2)


# In[9]:


users=pd.read_csv('BX-Users.csv',sep=";",error_bad_lines=False,encoding='latin-1')


# In[10]:


users.head(2)


# In[11]:


users.rename(columns={'User-ID':'user_id','Location':'location','Age':'age'},inplace=True)


# In[12]:


ratings=pd.read_csv('BX-Book-Ratings.csv',sep=";",error_bad_lines=False,encoding='latin-1')


# In[13]:


ratings.head(2)


# In[14]:


ratings.rename(columns={'User-ID':'user_id','Book-Rating':'rating'},inplace=True)


# In[15]:


ratings.head(2)


# In[16]:


books.shape


# In[17]:


books.shape


# In[18]:


ratings.shape


# In[19]:


users.shape


# In[32]:


ratings.head(2)


# In[33]:


ratings['user_id'].value_counts()


# In[34]:


ratings['user_id'].value_counts().shape


# In[35]:


x = ratings['user_id'].value_counts()>200
x[x]


# In[36]:


x[x].shape


# In[37]:


y=x[x].index
y


# In[38]:


ratings=ratings[ratings['user_id'].isin(y)]


# In[39]:


ratings.shape


# In[40]:


ratings.head()


# In[41]:


ratings_with_books=ratings.merge(books,on='ISBN')


# In[42]:


ratings_with_books.shape


# In[43]:


number_rating=ratings_with_books.groupby('title')['rating'].count().reset_index()


# In[44]:


number_rating.rename(columns={'rating':'number of ratings'},inplace=True)


# In[45]:


number_rating


# In[46]:


final_rating=ratings_with_books.merge(number_rating,on='title')


# In[47]:


final_rating.shape


# In[48]:


final_rating.shape


# In[49]:


final_rating=final_rating[final_rating['number of ratings']>=50]


# In[50]:


final_rating.shape


# In[51]:


final_rating.drop_duplicates(['user_id','title'],inplace=True)


# In[52]:


final_rating.shape


# In[53]:


book_pivot=final_rating.pivot_table(columns='user_id',index='title',values='rating')


# In[54]:


book_pivot


# In[55]:


book_pivot.fillna(0,inplace=True)


# In[56]:


book_pivot


# In[57]:


book_pivot.shape


# In[58]:


from scipy.sparse import csr_matrix
book_sparse=csr_matrix(book_pivot)


# In[59]:


type(book_sparse)


# In[60]:


from sklearn.neighbors import NearestNeighbors
model=NearestNeighbors(algorithm='brute')


# In[61]:


model.fit(book_sparse)


# In[62]:


book_pivot.index==237


# In[63]:


distances, suggestions=model.kneighbors(book_pivot.iloc[164,:].values.reshape(1,-1),n_neighbors=6)


# In[64]:


book_pivot


# In[65]:


distances


# In[66]:


suggestions


# In[67]:


for i in range(len(suggestions)):
    print(book_pivot.index[suggestions[i]])


# In[68]:


book_pivot.index[164]


# In[69]:


np.where(book_pivot.index=='Animal Farm')[0][0]


# In[73]:


def recommend_book(book_name):
    book_id=np.where(book_pivot.index==book_name)[0][0]
    distances, suggestions=model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1,-1),n_neighbors=6)
    
    for i in range(len(suggestions)):
        if i==0:
            print(book_pivot.index[suggestions[i]])
        if not i:
            print(book_pivot.index[suggestions[i]])
        


     


# In[74]:


recommend_book('Animal Farm')


# In[ ]:




