
import pandas as pd
import numpy as np
import unicodedata




def onehot_easy(pandas_df,dummy_before=True,dummy_replace=".",target_is_a_column=False,target_name="NULL"):

    data=pandas_df.dropna(axis=1)

    if target_is_a_column==True:
        y=data[[target_name]]
        data=data.drop([target_name],axis=1)


    for col in data.columns:
        if isinstance(data[[col]].values[0][0],str):
            prev=[]
            for i in range(data[[col]].drop_duplicates().shape[0]):
                prev.append(data[[col]].drop_duplicates().iloc[i][0])

            dic_col=dict()        
            for i in prev:
                i_unicode=unicodedata.normalize('NFKD', str(i)).encode('ascii', 'replace')
                dic_col[str(i_unicode)]=np.zeros(data[[col]].shape[0])
        
            for j in range(data[[col]].shape[0]):
                val=data[[col]].values[j][0]
                for i in prev:
                    i_unicode=unicodedata.normalize('NFKD', str(i)).encode('ascii', 'replace')
                    if i_unicode==val : 
                        dic_col[str(i_unicode)][j]=1

            k=0
            new_col=[]
            for i in prev:
                i_unicode=unicodedata.normalize('NFKD', str(i)).encode('ascii', 'replace')
                if k ==0 :
                    X=pd.DataFrame(dic_col[str(i_unicode)])
                    k=1
                else:
                    X=pd.concat([X, pd.DataFrame(dic_col[str(i_unicode)])], axis=1)
                    
                if dummy_before==False:
                    new_col.append(col.replace(dummy_replace,".dummy:")+"."+i_unicode)
                else:
                    new_col.append("dummy:"+col+"."+i_unicode)
            X.columns=new_col
            data=data.drop([col],axis=1)
            data[X.columns]=X
    
    if target_is_a_column == True:
        return data,y
    else:
        return data
