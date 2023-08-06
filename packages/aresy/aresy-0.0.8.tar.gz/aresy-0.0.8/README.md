## Home
Built on popular scientific computing toolkits, aresy aims to make it easy to process large-scale data on a single server. aresy treats the whole data flow as a computation graph, where the input data will be put into placeholders, and you can perform nearly any python-based transformation by extending the graph. aresy was designed with the following principles:

- Compatible with python data science ecosystem, such as numpy, pytorch, tensorflow modules.
- Able to process cross-type, cross-domain, cross-granularity data simultaneously.
- Easy to build a large feature generator, a transformer or even a data loader to feed preprocessed data into deep learning models.

## Installation
```shell
python setup.py install
```

## Package Reference

- aresy.formatting
    - aresy.formatting.TSVDataLoader
    - aresy.formatting.TSVPlaceholder

- aresy.preprocessing
    - aresy.preprocessing.WrangleFloat
    - aresy.preprocessing.WrangleStr
    - aresy.preprocessing.WrangleNormalDatetime

- aresy.aggregating
    - aresy.aggregating.Sum
    - aresy.aggregating.Mean
    - aresy.aggregating.Std
    - aresy.aggregating.Max
    - aresy.aggregating.Min
    - aresy.aggregating.Quantile

- aresy.utils
    - aresy.wrap\_outputs\_to\_json
