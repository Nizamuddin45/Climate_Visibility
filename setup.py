from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:    # file ka path denge wo return krenge list str me yaha file ka path requirements.txt hojayega kyuki function ke andr hai
    '''
    This function will return the list of requirements
    '''

    requirements = []
    with open(file_path)as file_obj:
        requirements=file_obj.readlines()
        # requirements = [req.replace("\n"," ")  for req in requirements]# ab alag alag line read krega to \n bhi krelga isliye \n na dede download ke waqt isliye hum ise replace krdenge with a blank
        requirements = [req.strip() for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements    



setup(
    name="VISIBILITY_PROJECT",
    version="0.0.1",
    author="Nizam",
    author_email="udnizam45@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt'),
)