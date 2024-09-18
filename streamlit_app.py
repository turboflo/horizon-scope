import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from horizon_scope.presentation.streamlit_presentation import main

if __name__ == "__main__":
    main()
