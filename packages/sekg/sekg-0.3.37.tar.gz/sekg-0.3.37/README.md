# sekg
this is library for software engineering knowledge graph.

## description
1. including wrapper for neo4j by py2neo.
2. the preprocess tool for stack overflow html.
3. graph2vec library
4. doc retrieval model

## todo
1. add version helper out of setup

## support
python 3.5 is need, py2neo 4.1.0 must be install in python 3


## Update the library
1. 
    1. update code and test,
    2. update the __version__ in sekg/meta.py, 
    3. update the dependency library in "root/requirements.txt" and in "root/setup.py".
    4. commit it and push to the github
   
2. upload the newest version to pypi.
    the new version pip install package is uploaded to the pipy.

    1.In Linux run upload.sh 
    ```
    ./upload.sh
    twine upload dist/*.tar.gz
    ```
    1. In windows,run upload.bat
    ```
    ./upload.bat
    twine upload dist/*.tar.gz
    ```

4. you can use following command to update the package.
Note: recommand to installing via "https://pypi.tuna.tsinghua.edu.cn/simple" to get the latest version.
```
pip install sekg
pip install -U sekg
pip install -U sekg -i https://pypi.org/simple/
pip install -U sekg -i https://pypi.douban.com/simple
pip install -U sekg -i https://pypi.tuna.tsinghua.edu.cn/simple

```
