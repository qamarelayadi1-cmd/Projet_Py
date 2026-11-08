"""
    polymorphisme:
    object: abstraite supper class dont herite toutes les classes 
    -str,list,tuple,set
    -len() et la methode polymorphe :meme nom dont toutes les classes 
"""
def sum_length(l:list[object])->int:
    sum=0
    for obj in l: 
            sum=sum +len(obj)
    return sum
class Malware :
      name:str='Malware'

if __name__ == "__main__":
     virus:Malware=Malware()
     print(Malware.name)
     virus.name='virus'
     virus.signature='01010001'
     print(virus.name)
     """ vector:list[object]=['1234',[],(1,2,3),{2,4}]
     print(sum_length(vector)) """