import sys
import os

# Add the project root directory and src directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(project_root, "src")
sys.path.extend([project_root, src_path])

from horizon_scope.presentation.streamlit_presentation import main

if __name__ == "__main__":
    main()
