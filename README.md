# ELEC3848_gp
## Group E12
# Item Recognition with OpenCV
## Environment setting
It is recommended to create a virtual environment with **Conda** and run the program in the virtual environment.
Here are some steps for reference: (suppose you already have `conda`)
1.  Check environment: `conda env list`
2.  Create a new environment (here is): 
    ```
    conda create -n py36tqrcode numpy pandas python=3.9
    ```
    This command creates a new environment called `py36tqrcode` in the conda environment and installs the Python 3.9, NumPy, and Pandas packages in that environment.
4.  Activate the environment: `conda activate py36tqrcode`
5.  Deactive the environment: `conda deactivate`
6. Please make sure that your Python interpreter is corresponding to your python environment. eg:
    ```
    (py36tqrcode) ➜  desktop git:(main) ✗ conda env list
    # conda environments:
    #
    base                     /Users/wodepingguo/opt/anaconda3
    keras                    /Users/wodepingguo/opt/anaconda3/envs/keras
    py36tf1                  /Users/wodepingguo/opt/anaconda3/envs/py36tf1
    py36tqrcode           *  /Users/wodepingguo/opt/anaconda3/envs/py36tqrcode
    tensorflow               /Users/wodepingguo/opt/anaconda3/envs/tensorflow
    ```
    then
    ```
    (py36tqrcode) ➜  desktop git:(main) ✗ /Users/wodepingguo/opt/anaconda3/envs/py36tqrcode/bin/python QRcode.py
    ```
