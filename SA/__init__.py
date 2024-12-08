import time
print("Initializing SA package...", end='', flush=True)

for _ in range(10):  # Adjust this range for how many dots you want
    print(".", end='', flush=True)
    time.sleep(0.7)  # Adjust the sleep time to control the speed
from .SA_Const1 import *        # Import everything from Const1.py
from .SA_Const2 import *        # Import everything from Const2.py
from .SA_Const3 import *        # Import everything from Const3.py
from .SA_Const4 import *        # Import everything from Const4.py
from .SA_Const5 import *        # Import everything from Const4.py
from .SA_ObjFunc1 import *      # Import everything from OF1.py
from .SA_ObjFunc2 import *      # Import everything from OF2.py
from .SA_ObjFunc3 import *      # Import everything from OF2.py
from .SA_Code import *               # Import everything from SA.py
from .SA_Param import *         # Import everything from Data.py
from .SA_CreateMap import *     # Import everything from createmap.py
print("\nSA package loaded successfully")
