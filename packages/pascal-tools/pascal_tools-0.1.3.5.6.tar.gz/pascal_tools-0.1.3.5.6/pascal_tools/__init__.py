
import pandas as pd
import numpy as np
import unicodedata




def onehot_easy(pandas_df,dummy_before=True,dummy_replace=".",target_name=None,dropNA=True,test_df=None):

    data=pandas_df

    if target_name is not None:
        y=data[[target_name]]
        data=data.drop([target_name],axis=1)

    #a revoir
    if dropNA ==True:
        data=data.dropna(axis=1)
        if test_df is not None:
            test_df=test_df.dropna(axis=1)


    for col in data.columns:

        if isinstance(data[[col]].values[0][0],str):
            prev=[]
            for i in range(data[[col]].drop_duplicates().shape[0]):
                prev.append(data[[col]].drop_duplicates().iloc[i][0])

            dic_col=dict() 
            dic_col_test=dict()       
            for i in prev:
                i_unicode=unicodedata.normalize('NFKD', str(i)).encode('ascii', 'replace').decode('UTF-8')
                dic_col[str(i_unicode)]=np.zeros(data[[col]].shape[0])
                dic_col_test[str(i_unicode)]=np.zeros(data[[col]].shape[0])
        
            for j in range(data[[col]].shape[0]):
                val=data[[col]].values[j][0]
                if test_df is not None and j <= test_df[[col]].shape[0]:
                    val_test=test_df[[col]].values[j][0]


                for i in prev:
                    i_unicode=unicodedata.normalize('NFKD', str(i)).encode('ascii', 'replace').decode('UTF-8')
                    if i_unicode==val : 
                        dic_col[str(i_unicode)][j]=1

                    if test_df is not None and j <= test_df[[col]].shape[0]:
                        if i_unicode==val_test : 
                            dic_col_test[str(i_unicode)][j]=1
                    

            k=0
            new_col=[]
            for i in prev:
                i_unicode=unicodedata.normalize('NFKD', str(i)).encode('ascii', 'replace').decode('UTF-8')
                if k ==0 :
                    X=pd.DataFrame(dic_col[str(i_unicode)])
                    X_test=pd.DataFrame(dic_col_test[str(i_unicode)])
                    k=1
                else:
                    X=pd.concat([X, pd.DataFrame(dic_col[str(i_unicode)])], axis=1)
                    X_test=pd.concat([X_test, pd.DataFrame(dic_col_test[str(i_unicode)])], axis=1)
                    
                if dummy_before==False:
                    new_col.append(col.replace(dummy_replace,".dummy:")+"."+str(i_unicode))
                else:
                    new_col.append("dummy:"+col+"."+str(i_unicode))
            X.columns=new_col
            data=data.drop([col],axis=1)
            data[X.columns]=X 

            if test_df is not None:
                X_test.columns=new_col
                test_df=test_df.drop([col],axis=1)
                test_df[X_test.columns]=X_test 

    if test_df is not None:
        if target_name is not None:
            return data,test_df,y
        else:
            return data,test_df
    else:
        if target_name is not None:
            return data,y
        else:
            return data
