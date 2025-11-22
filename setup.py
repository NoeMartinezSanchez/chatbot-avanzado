from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="chatbot-propedeutico",
    version="1.0.0",
    author="Noe Martinez Sanchez",
    author_email="tu-email@ejemplo.com",
    description="ChatBot avanzado para el módulo propedéutico de Prepa en Línea SEP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "chatbot": ["data/*.json", "templates/*.html", "static/css/*.css", "static/js/*.js"],
    },
    entry_points={
        "console_scripts": [
            "chatbot-propedeutico=app:main",
        ],
    },
)