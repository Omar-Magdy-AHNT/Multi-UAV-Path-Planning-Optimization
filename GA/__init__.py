import time
print("Initializing GA package...", end='', flush=True)

for _ in range(10):  # Adjust this range for how many dots you want
    print(".", end='', flush=True)
    time.sleep(0.7)  # Adjust the sleep time to control the speed

from .GA_Param import *         # Import everything from Data.py
from .GA_Const1 import *        # Import everything from Const1.py
from .GA_Const2 import *        # Import everything from Const2.py
from .GA_Const3 import *        # Import everything from Const3.py
from .GA_Const4 import *        # Import everything from Const4.py
from .GA_Const5 import *        # Import everything from Const4.py
from .GA_ObjFunc1 import *      # Import everything from OF1.py
from .GA_ObjFunc2 import *      # Import everything from OF2.py
from .GA_ObjFunc3 import *      # Import everything from OF2.py
from .GA_CreateMap import *     # Import everything from createmap.py
from .GA_Code import *               # Import everything from milestone4.py
print("\nGA package loaded successfully")
