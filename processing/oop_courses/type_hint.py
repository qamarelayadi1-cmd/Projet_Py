"""
 type hint since python 3.5
 -humane readable of code 
 - Type check from IDE like vscode
"""
b:bool=True
i:int=3
p:float=22/7
s:str=''

l:list[str]=['a','b']
t:tuple[int,...]=(1,2,3)
d:dict[str,float]={'fes':21.4}
S:set[float]={1,3,3.7}

#new type
Vector=list[float]
v:Vector=[]

from typing import (
    Any,
    Final,
    Optional,
    Union
)
any:Any=[{},[]]
MAX:Final[int]=100

opt:Optional[float]=None
def search(key:int)->Union[int,str]:
    return 1