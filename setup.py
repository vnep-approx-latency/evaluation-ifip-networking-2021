from setuptools import setup, find_packages

install_requires = [
    # "gurobipy",  	# install this manually
    # "alib",      	# install this manually
    # "vnep_approx" , 	# install this manually 
    "matplotlib>=2.2,<2.3",
    "numpy",
    "click==6.7",
    "pyyaml",
    "jsonpickle",
]

setup(
    name="evaluation-ifip-networking-2021-py3",
    # version="0.1",
    packages=["evaluation-ifip-networking-2021-py3"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "evaluation-ifip-networking-2021-py3 = evaluation-ifip-networking-2021-py3.cli:cli",
        ]
    }
)
