{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ba17be24",
   "metadata": {},
   "outputs": [],
   "source": [
    "# coding: utf-8\n",
    "try:\n",
    "    import urllib.request\n",
    "except ImportError:\n",
    "    raise ImportError('You should use Python 3.x')\n",
    "import os.path\n",
    "import gzip\n",
    "import pickle\n",
    "import os\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "url_base = 'http://yann.lecun.com/exdb/mnist/'\n",
    "key_file = {\n",
    "    'train_img':'train-images-idx3-ubyte.gz',\n",
    "    'train_label':'train-labels-idx1-ubyte.gz',\n",
    "    'test_img':'t10k-images-idx3-ubyte.gz',\n",
    "    'test_label':'t10k-labels-idx1-ubyte.gz'\n",
    "}\n",
    "\n",
    "dataset_dir = os.path.dirname(os.path.abspath(__file__))\n",
    "save_file = dataset_dir + \"/mnist.pkl\"\n",
    "\n",
    "train_num = 60000\n",
    "test_num = 10000\n",
    "img_dim = (1, 28, 28)\n",
    "img_size = 784\n",
    "\n",
    "\n",
    "def _download(file_name):\n",
    "    file_path = dataset_dir + \"/\" + file_name\n",
    "    \n",
    "    if os.path.exists(file_path):\n",
    "        return\n",
    "\n",
    "    print(\"Downloading \" + file_name + \" ... \")\n",
    "    urllib.request.urlretrieve(url_base + file_name, file_path)\n",
    "    print(\"Done\")\n",
    "    \n",
    "def download_mnist():\n",
    "    for v in key_file.values():\n",
    "       _download(v)\n",
    "        \n",
    "def _load_label(file_name):\n",
    "    file_path = dataset_dir + \"/\" + file_name\n",
    "    \n",
    "    print(\"Converting \" + file_name + \" to NumPy Array ...\")\n",
    "    with gzip.open(file_path, 'rb') as f:\n",
    "            labels = np.frombuffer(f.read(), np.uint8, offset=8)\n",
    "    print(\"Done\")\n",
    "    \n",
    "    return labels\n",
    "\n",
    "def _load_img(file_name):\n",
    "    file_path = dataset_dir + \"/\" + file_name\n",
    "    \n",
    "    print(\"Converting \" + file_name + \" to NumPy Array ...\")    \n",
    "    with gzip.open(file_path, 'rb') as f:\n",
    "            data = np.frombuffer(f.read(), np.uint8, offset=16)\n",
    "    data = data.reshape(-1, img_size)\n",
    "    print(\"Done\")\n",
    "    \n",
    "    return data\n",
    "    \n",
    "def _convert_numpy():\n",
    "    dataset = {}\n",
    "    dataset['train_img'] =  _load_img(key_file['train_img'])\n",
    "    dataset['train_label'] = _load_label(key_file['train_label'])    \n",
    "    dataset['test_img'] = _load_img(key_file['test_img'])\n",
    "    dataset['test_label'] = _load_label(key_file['test_label'])\n",
    "    \n",
    "    return dataset\n",
    "\n",
    "def init_mnist():\n",
    "    download_mnist()\n",
    "    dataset = _convert_numpy()\n",
    "    print(\"Creating pickle file ...\")\n",
    "    with open(save_file, 'wb') as f:\n",
    "        pickle.dump(dataset, f, -1)\n",
    "    print(\"Done!\")\n",
    "\n",
    "def _change_one_hot_label(X):\n",
    "    T = np.zeros((X.size, 10))\n",
    "    for idx, row in enumerate(T):\n",
    "        row[X[idx]] = 1\n",
    "        \n",
    "    return T\n",
    "    \n",
    "\n",
    "def load_mnist(normalize=True, flatten=True, one_hot_label=False):\n",
    "    \"\"\"MNIST 데이터셋 읽기\n",
    "    \n",
    "    Parameters\n",
    "    ----------\n",
    "    normalize : 이미지의 픽셀 값을 0.0~1.0 사이의 값으로 정규화할지 정한다.\n",
    "    one_hot_label : \n",
    "        one_hot_label이 True면、레이블을 원-핫(one-hot) 배열로 돌려준다.\n",
    "        one-hot 배열은 예를 들어 [0,0,1,0,0,0,0,0,0,0]처럼 한 원소만 1인 배열이다.\n",
    "    flatten : 입력 이미지를 1차원 배열로 만들지를 정한다. \n",
    "    \n",
    "    Returns\n",
    "    -------\n",
    "    (훈련 이미지, 훈련 레이블), (시험 이미지, 시험 레이블)\n",
    "    \"\"\"\n",
    "    if not os.path.exists(save_file):\n",
    "        init_mnist()\n",
    "        \n",
    "    with open(save_file, 'rb') as f:\n",
    "        dataset = pickle.load(f)\n",
    "    \n",
    "    if normalize:\n",
    "        for key in ('train_img', 'test_img'):\n",
    "            dataset[key] = dataset[key].astype(np.float32)\n",
    "            dataset[key] /= 255.0\n",
    "            \n",
    "    if one_hot_label:\n",
    "        dataset['train_label'] = _change_one_hot_label(dataset['train_label'])\n",
    "        dataset['test_label'] = _change_one_hot_label(dataset['test_label'])    \n",
    "    \n",
    "    if not flatten:\n",
    "         for key in ('train_img', 'test_img'):\n",
    "            dataset[key] = dataset[key].reshape(-1, 1, 28, 28)\n",
    "\n",
    "    return (dataset['train_img'], dataset['train_label']), (dataset['test_img'], dataset['test_label']) \n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    init_mnist()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
