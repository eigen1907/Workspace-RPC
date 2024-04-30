
### conda(micromamba) setup

```sh
conda activate [가상환경 이름]
pip install jupyter
pip install ipykernel
python -m ipykernel install --user --name [가상환경 이름] --display-name "[jupyter에 표시될 kernel의 이름]"
```

```sh
mm activate ds4hep
pip install jupyter
pip install ipykernel
python -m ipykernel install --user --name py39 --display-name "py39-jupyter"
```