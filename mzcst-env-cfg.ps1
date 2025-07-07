# mzcst-test
conda create -n mzcst-test python=3.10.16
conda activate mzcst-test
conda install pytorch=2.5.1=cuda126_mkl_py310_h5866544_316 torchvision torchaudio pyyaml ipykernel seaborn dill pandas pyglet importlib-metadata setuptools gym pygame numpy scipy matplotlib h5py build twine
pip install --upgrade tomli tomli-w
pip install --no-index --find-links "C:/Program Files (x86)/CST Studio Suite 2024/Library/Python/repo/simple" cst-studio-suite-link
pip install -e .


# 封包

python -m build



# API token
# 测试服

python -m twine upload --repository testpypi dist/* --verbose


# 安装
pip install -i https://test.pypi.org/simple/ mzcst-2024
pip install -i https://test.pypi.org/simple/ --upgrade mzcst-2024


# 正式服
python -m twine upload dist/* --verbose


pip install mzcst-2024
pip install --upgrade mzcst-2024



#恢复环境
conda env create --file=mzcst-test-raw.yml
conda env create --file=mzcst-test-without-target.yml



