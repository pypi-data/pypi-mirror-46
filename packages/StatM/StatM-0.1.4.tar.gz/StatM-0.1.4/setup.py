import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StatM",
    packages = ['StatM'],
    version="0.1.4",
    author="Prince Canuma",
    author_email="prince.gdt@gmail.com",
    description="This package implements 3 key Numerical Analysis iterative algorithms",
    long_description="This package implements 3 key Numerical Analisys "
                "iterative methods: Bisection, Regula-Falsi and Secant",
    long_description_content_type="text/markdown",
    url="https://github.com/Blaizzy/Boring_weekends/tree/master/statistics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],

)