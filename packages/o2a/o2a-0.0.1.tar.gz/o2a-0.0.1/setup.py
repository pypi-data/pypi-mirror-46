import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="o2a",
    version="0.0.1",
    author="Jarek Potiuk, Szymon Przedwojski, Kamil Breguła, Feng Lu, Cameron Moberg",
    author_email="jarek.potiuk@polidea.com, szymon.przedwojski@polidea.com, "
                 "kamil.bregula@polidea.com, fenglu@google.com, cjmoberg@google.com",
    description="Oozie To Airflow migration tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoogleCloudPlatform/oozie-to-airflow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
