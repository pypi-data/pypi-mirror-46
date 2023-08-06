## Installation
To install our package, run the setup file.

<tt>python \<path to code folder\>/setup.py install</tt>

You can also install it in develop mode, or with pip.
The best would be to install it in developper mode with pip with the command

<tt>pip install -e .</tt>

## Libraries
To run the code you need:
 - python 3.5 or above (tested on 3.7.1) to get the @ syntax for numpy matrix multiplication.
 
You will also need the following packages:
 - For the main code:
   - numba: To run loops in C.
   - numpy: Classical matrix library.
   
 - Specific to the Diffrac method:
   - cvxopt: To solve quadratic program.
    
 - For the dataloader part:
   - arff: For splitting MULAN datasets in train and test when not already done.
   - scikit-learn: for reading LIBSVM dataset in a sparse way
   - scikit-multilearn: for reading MULAN dataset in a sparse way

 - When getting to examples, you may encounter:
   - dask distributed: To speed up computations with parallelization.
   - dask job_queue: To run parallelize on several clusters.
   - ipywidgets: To get interactive visualization on notebooks.
   - jupyter notebook: To run notebooks.
   - matplotlib: To visualize plots.
   - pytorch: for semi-supervised experiments and interval regression with neural networks.
   
## Datasets
If you intend to run real data experiments, please download data and provide data path in the file <tt>config.py</tt>.

### MULAN
Multilabel datasets were download at:
 - http://mulan.sourceforge.net/datasets-mlc.html 

### LIBSVM
Classification datasets were download at:
 - https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass.html

## Abbrevations
We used the following abbreviations in the code:

 - IR: interval regression.
 - CL: classification.
 - ML: multilabel.
 - RD: real data.
