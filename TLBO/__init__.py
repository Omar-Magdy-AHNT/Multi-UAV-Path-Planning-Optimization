import time

print("Initializing TLBO package...", end='', flush=True)

for _ in range(10):  
    print(".", end='', flush=True)
    time.sleep(0.7)  

from .TLBO_Param import *         # Import everything from Data.py
from .TLBO_Const1 import *        # Import everything from Const1.py
from .TLBO_Const2 import *        # Import everything from Const2.py
from .TLBO_Const3 import *        # Import everything from Const3.py
from .TLBO_Const4 import *        # Import everything from Const4.py
from .TLBO_Const5 import *        # Import everything from Const4.py
from .TLBO_ObjFunc1 import *      # Import everything from OF1.py
from .TLBO_ObjFunc2 import *      # Import everything from OF2.py
from .TLBO_ObjFunc3 import *      # Import everything from OF2.py
from .TLBO_CreateMap import *     # Import everything from createmap.py
from .TLBO_Code import *               # Import everything from milestone4.py
print("\nTLBO package loaded successfully")
