from app import Controller

# Run this script to start the application    
# make sure you have sounddevice installed 
# (pip install sounddevice / conda install conç da-forge::python-sounddevice)
# also make sure you pynput installed and allow access to input monitoring in your system settings
# (pip install pynput)

if __name__ == "__main__":
    c = Controller()   
    c.run_app()

# https://realpython.com/if-name-main-python/
# https://docs.python.org/3/library/__main__.html
       
              