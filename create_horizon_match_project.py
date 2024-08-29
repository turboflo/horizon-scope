import os

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def create_file(path, content=''):
    with open(path, 'w') as f:
        f.write(content)

def create_project_structure():
    # Create src directory in the current location
    src_dir = 'src'
    create_directory(src_dir)

    # Create horizon_match directory inside src
    root_dir = os.path.join(src_dir, 'horizon_match')
    create_directory(root_dir)

    # Create package structure
    dirs = [
        'domain/entities',
        'application/interfaces',
        'application/use_cases',
        'infrastructure/services',
        'infrastructure/config',
        'presentation',
        'tests'
    ]
    for dir_path in dirs:
        create_directory(os.path.join(root_dir, dir_path))
        create_file(os.path.join(root_dir, dir_path, '__init__.py'))

    # Create main files
    files = {
        'domain/entities/project.py': 'class Project:\n    def __init__(self, id, description):\n        self.id = id\n        self.description = description\n',
        'domain/entities/comparison_result.py': 'class ComparisonResult:\n    def __init__(self, summary, similarity, difference, score, reason):\n        self.summary = summary\n        self.similarity = similarity\n        self.difference = difference\n        self.score = score\n        self.reason = reason\n',
        'application/interfaces/vector_search_service.py': 'from abc import ABC, abstractmethod\n\nclass VectorSearchService(ABC):\n    @abstractmethod\n    async def search(self, query, k):\n        pass\n',
        'application/interfaces/comparison_service.py': 'from abc import ABC, abstractmethod\n\nclass ComparisonService(ABC):\n    @abstractmethod\n    async def compare(self, my_project, existing_project):\n        pass\n',
        'application/use_cases/compare_projects.py': 'class CompareProjects:\n    def __init__(self, vector_search_service, comparison_service):\n        self.vector_search_service = vector_search_service\n        self.comparison_service = comparison_service\n\n    async def execute(self, query, k):\n        similar_projects = await self.vector_search_service.search(query, k)\n        results = []\n        for project in similar_projects:\n            comparison = await self.comparison_service.compare(query, project.description)\n            results.append(comparison)\n        return results\n',
        'infrastructure/services/pinecone_search_service.py': '# Implement PineconeSearchService here\n',
        'infrastructure/services/openai_comparison_service.py': '# Implement OpenAIComparisonService here\n',
        'infrastructure/config/config_manager.py': 'import yaml\n\nclass ConfigManager:\n    def __init__(self, config_path):\n        with open(config_path, "r") as config_file:\n            self.config = yaml.safe_load(config_file)\n\n    def get(self, key, default=None):\n        return self.config.get(key, default)\n',
        'presentation/horizon_match_client.py': 'class HorizonMatchClient:\n    def __init__(self, config):\n        # Initialize services and use cases here\n        pass\n\n    @classmethod\n    def from_config(cls, config_path="config.yml"):\n        # Load config and create client\n        pass\n\n    async def match(self, query, k):\n        # Implement matching logic\n        pass\n',
    }

    for file_path, content in files.items():
        create_file(os.path.join(root_dir, file_path), content)

    # Create config.yml in the src directory
    create_file(os.path.join(src_dir, 'config.yml'), 'OPENAI_API_KEY: "your-openai-api-key"\nPINECONE_API_KEY: "your-pinecone-api-key"\nPINECONE_INDEX: "projects-text-embedding-3-small"\nOPENAI_EMBEDDING_MODEL: "text-embedding-3-small"\n')

    # Create README.md in the src directory
    create_file(os.path.join(src_dir, 'README.md'), '# Horizon Match\n\nAn application for comparing project ideas using vector search and GPT-4-mini.\n')

    # Create requirements.txt in the src directory
    create_file(os.path.join(src_dir, 'requirements.txt'), 'openai==1.3.0\npinecone-client==2.2.4\npyyaml==6.0.1\npydantic==2.5.2\n')

    print("Project structure created successfully in the 'src' directory!")

if __name__ == '__main__':
    create_project_structure()
