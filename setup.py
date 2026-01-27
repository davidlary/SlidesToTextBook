from setuptools import setup, find_packages

setup(
    name="slides-to-textbook",
    version="1.0.0",
    author="Dr. David Lary",
    description="Convert PDF lecture slides to LaTeX textbooks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/davidlary/SlidesToTextBook",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.9.0",
        "PyPDF2>=3.0.0",
        "pytesseract>=0.3.10",
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
        "scholarly>=1.7.0",
        "bibtexparser>=1.4.0",
        "jinja2>=3.1.0",
        "pylatex>=1.4.0",
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
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
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
