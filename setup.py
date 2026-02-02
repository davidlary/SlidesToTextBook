from setuptools import setup, find_packages

setup(
    name="slides-to-textbook",
    version="2.0.0",
    author="Dr. David Lary",
    author_email="davidlary@me.com",
    description="Convert PDF lecture slides to LaTeX textbooks with AI-powered content generation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/davidlary/SlidesToTextBook",
    project_urls={
        "Bug Reports": "https://github.com/davidlary/SlidesToTextBook/issues",
        "Source": "https://github.com/davidlary/SlidesToTextBook",
        "Documentation": "https://github.com/davidlary/SlidesToTextBook/blob/main/README.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # PDF processing
        "pdfplumber>=0.9.0",
        "PyPDF2>=3.0.0",
        "pytesseract>=0.3.10",
        # AI APIs
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
        # Research and bibliography
        "scholarly>=1.7.0",
        "bibtexparser>=1.4.0",
        # LaTeX and templates
        "jinja2>=3.1.0",
        "pylatex>=1.4.0",
        # Utilities
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        # Portrait generation (external CLI tool)
        # Note: portrait-generator must be installed separately from:
        # https://github.com/davidlary/PortraitGenerator
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-timeout>=2.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "sphinx>=7.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "slides2tex=slides_to_textbook.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="pdf latex textbook education ai machine-learning slides conversion",
)
