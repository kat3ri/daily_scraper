"""Sample test data for testing without API calls."""

SAMPLE_REDDIT_POSTS = [
    {
        'source': 'reddit',
        'subreddit': 'MachineLearning',
        'title': '[R] New Efficient Attention Mechanism Reduces Transformer Compute by 40%',
        'url': 'https://arxiv.org/abs/2401.12345',
        'permalink': 'https://reddit.com/r/MachineLearning/comments/test1',
        'score': 342,
        'num_comments': 87,
        'created_utc': '2024-01-25T10:30:00',
        'author': 'researcher_ai',
        'selftext': 'We introduce FlashAttention-3, a new attention mechanism that reduces computational complexity while maintaining performance...',
        'is_self': False
    },
    {
        'source': 'reddit',
        'subreddit': 'LocalLLaMA',
        'title': 'New Quantization Method: Running 70B Models on 16GB VRAM',
        'url': 'https://github.com/example/quant-method',
        'permalink': 'https://reddit.com/r/LocalLLaMA/comments/test2',
        'score': 1245,
        'num_comments': 234,
        'created_utc': '2024-01-25T09:15:00',
        'author': 'ml_hacker',
        'selftext': 'I developed a new quantization approach that allows running 70B parameter models on consumer GPUs...',
        'is_self': True
    },
    {
        'source': 'reddit',
        'subreddit': 'StableDiffusion',
        'title': 'SDXL-Turbo: Real-time Image Generation at 512x512',
        'url': 'https://huggingface.co/stabilityai/sdxl-turbo',
        'permalink': 'https://reddit.com/r/StableDiffusion/comments/test3',
        'score': 892,
        'num_comments': 156,
        'created_utc': '2024-01-25T08:45:00',
        'author': 'sd_enthusiast',
        'selftext': 'Stability AI just released SDXL-Turbo which can generate high quality images in under 1 second...',
        'is_self': False
    }
]

SAMPLE_GITHUB_REPOS = [
    {
        'source': 'github',
        'full_name': 'microsoft/phi-3',
        'name': 'phi-3',
        'title': 'microsoft/phi-3',
        'url': 'https://github.com/microsoft/phi-3',
        'description': 'Official repository for Phi-3, a family of powerful small language models',
        'stars': 8234,
        'forks': 456,
        'language': 'Python',
        'topics': ['machine-learning', 'llm', 'phi'],
        'created_at': '2024-01-24T15:00:00Z',
        'updated_at': '2024-01-25T10:00:00Z',
        'created_utc': '2024-01-24T15:00:00Z'
    },
    {
        'source': 'github',
        'full_name': 'mlc-ai/web-llm',
        'name': 'web-llm',
        'title': 'mlc-ai/web-llm',
        'url': 'https://github.com/mlc-ai/web-llm',
        'description': 'Run LLMs entirely in your browser using WebGPU',
        'stars': 5621,
        'forks': 234,
        'language': 'TypeScript',
        'topics': ['llm', 'webgpu', 'browser'],
        'created_at': '2024-01-23T12:00:00Z',
        'updated_at': '2024-01-25T09:30:00Z',
        'created_utc': '2024-01-23T12:00:00Z'
    }
]

SAMPLE_HUGGINGFACE_ITEMS = [
    {
        'source': 'huggingface',
        'type': 'models',
        'title': 'mistralai/Mixtral-8x22B-Instruct-v0.1',
        'url': 'https://huggingface.co/mistralai/Mixtral-8x22B-Instruct-v0.1',
        'description': 'Mixtral 8x22B is a mixture of experts model with outstanding performance',
        'metadata': {'likes': '2.3k', 'downloads': '150k'},
        'created_utc': '2024-01-25T07:00:00'
    },
    {
        'source': 'huggingface',
        'type': 'datasets',
        'title': 'Open-Orca/SlimOrca-Dedup',
        'url': 'https://huggingface.co/datasets/Open-Orca/SlimOrca-Dedup',
        'description': 'High-quality deduplicated instruction dataset for training LLMs',
        'metadata': {'likes': '543', 'downloads': '45k'},
        'created_utc': '2024-01-24T16:00:00'
    }
]

def get_sample_data():
    """Get sample data for testing."""
    return SAMPLE_REDDIT_POSTS + SAMPLE_GITHUB_REPOS + SAMPLE_HUGGINGFACE_ITEMS
