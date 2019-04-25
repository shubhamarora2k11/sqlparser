# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:27:22 2019

@author: SA066118
"""

import sqlparse
import re
x=0




def gettheworkdone(query):
    global x
    
    #print("item",x,"\n",query)
    x+=1
    
    #print("Query: \n", query)
    selects = re.search(r'select\s+', query)
    froms = re.search(r'from\s+', query)
    wheres = re.search(r'where\s+', query)
    innerjoins = re.search(r'inner\sjoin\s+', query)
    leftjoins = re.search(r'left\sjoin\s+', query)
    rightjoins = re.search(r'right\sjoin\s+', query)
    fulljoins = re.search(r'full\souter\sjoin\s+', query)
    
    if selects is None or froms is None:
        return
    
    loq = len(query)
    w,i,l,r,f,m = loq,loq,loq,loq,loq,loq
    
    #print(w,i,l,r,f,m)
    
    if wheres:
        w = wheres.start()
    if innerjoins:
        i = innerjoins.start()
    if leftjoins:
        l = leftjoins.start()
    if rightjoins:
        r = rightjoins.start()
    if fulljoins:
        f = fulljoins.start()    
    
    
    m = min(w,i,l,r,f)
    
    #print(selects, froms, wheres ,innerjoins, leftjoins, rightjoins, fulljoins)
    #print("m: ", m, type(m))
    
    #print(w,i,l,r,f,m)
    
    table_string = query[froms.end():m]
    
    #print(table_string)
    
    tables = table_string.split(',')
    
    final_tables = []

    for tab in tables:
        final_tables.append(tab.strip())
        
    #print(final_tables)
    
    tablealias = {}
    
    for t in final_tables:
        p = re.search(r'(\w+)\sas\s(\w+)', t)
        q = re.search(r'(\w+)\s(\w+)', t)
        r = re.search(r'(\w+)', t)
        
        if p is not None:
            pattern = re.compile(r'(\w+)\s+as\s+(\w+)')   
            for (table, alias) in re.findall(pattern, t):
                tablealias[alias]=table
            
            pattern = re.compile(r'join\s+(\w+)\s+as\s+(\w+)\s')

            for (table, alias) in re.findall(pattern, query):
                #   print(table, alias)
                tablealias[alias]=table
                
        elif q is not None:
            pattern = re.compile(r'(\w+)\s+(\w+)')   
            for (table, alias) in re.findall(pattern, t):
                tablealias[alias]=table
                
            pattern = re.compile(r'join\s+(\w+)\s+(\w+)\s')
            for (table, alias) in re.findall(pattern, query):
                #   print(table, alias)
                tablealias[alias]=table
                
        elif r is not None:
            pattern = re.compile(r'(\w+)')   
            for (table) in re.findall(pattern, t):
                tablealias[table]=table
                
            pattern = re.compile(r'join\s+(\w+)\s+')
            for (table) in re.findall(pattern, query):
                #   print(table, alias)
                tablealias[table]=table
    
    #print(tablealias)
    print ("\nTables Used: ")
    for xyz in tablealias.values():
        print (xyz)
    
    columns_string = query[selects.end():froms.start()]
    #print("col string: ",columns_string)
    tempcolumns  = (columns_string.split(','))

    #print(tempcolumns)

    columns = []

    for col in tempcolumns:
        columns.append(col.strip())
    
    #print(columns)
    
    pattern = re.compile(r'(\w+)\.(\w+)')
    pattern2 = re.compile(r'(\w+)')


    import pandas as pd

    df = pd.DataFrame(columns=['Table','Column'])

    count = 0

    for col in columns:
        
        p = re.search(r'(\w+)\.(\w+)', col)
        q = re.search(r'(\w+)', col)
        
     #   print(p,q, col)
        
        if p is not None:
            for (table, column) in re.findall(pattern, col):
                #print(tablealias[table], column)
                df.loc[count]= [tablealias[table], column]
                count+=1
        elif q is not None:    
            for (column) in re.findall(pattern2, col):
      #          print(column)
                df.loc[count]= ["", column]
                count+=1
                
    #print(df)
    print ("\nColumns Used: ")
    for xyz in range(len(df['Column'])):
        print (df['Column'][xyz])
        
    print()

def main():
    
    file = open('file.txt','r')

    sql = ""

    for line in file:
        sql += line

    file.close()

    queries = sqlparse.split(sql)

    formatted = []
    for i in queries:
        formatted.append(sqlparse.format(i, reindent=True, keyword_case='upper'))

    #print(formatted[2])

    for item in formatted:
        query = item.lower()
    
   
        query = re.sub(
                r"\*", 
                "all", 
                query
                )
        query = re.sub('(--.*)', ' ', query)
    
    
    
        pattern = re.compile(r'select\s+')
        allselects = [(m.start(0), m.end(0)) for m in re.finditer(pattern, query)]
        
       # print(allselects)
    
        if len(allselects) ==1:
            gettheworkdone(query)
            
        else:
            for i in range(len(allselects)):
        #        print(i, len(allselects)-1)
                
                beg = allselects[i][0]
                if i==len(allselects)-1:
                    end = len(query)
                else:
                    end = allselects[i+1][0]
                
         #       print(allselects[i])
                
                if i==len(allselects)-1:
                    end = len(query)
          #      print("begend",beg,end)
                
                subquery = query[beg:end]
                
           #     print("sub\n",subquery)
                gettheworkdone(subquery)

main()    