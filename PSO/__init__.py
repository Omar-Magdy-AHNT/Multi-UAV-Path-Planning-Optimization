import time
print("Initializing PSO package...", end='', flush=True)

for _ in range(10):  # Adjust this range for how many dots you want
    print(".", end='', flush=True)
    time.sleep(0.7)  # Adjust the sleep time to control the speed

from .PSO_Param import *         # Import everything from Data.py
from .PSO_Const1 import *        # Import everything from Const1.py
from .PSO_Const2 import *        # Import everything from Const2.py
from .PSO_Const3 import *        # Import everything from Const3.py
from .PSO_Const4 import *        # Import everything from Const4.py
from .PSO_Const5 import *        # Import everything from Const4.py
from .PSO_ObjFunc1 import *      # Import everything from OF1.py
from .PSO_ObjFunc2 import *      # Import everything from OF2.py
from .PSO_ObjFunc3 import *      # Import everything from OF2.py
from .PSO_CreateMap import *     # Import everything from createmap.py
from .PSO_Code import *          # Import everything from Code.py
print("\nPSO package loaded successfully")
