from setuptools import setup, find_packages

setup(
    name="auto-file-organizer",
    version="0.1.0",   # 👈 版本号
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "organize=auto_file_organizer.organizer:main"
        ]
    },
)
