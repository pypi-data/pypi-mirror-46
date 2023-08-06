"""
A module that collects together external sources of data.

The goal of this module is to give access to the same interface used in the
rest of the library in a somewhat sane manner.
"""
import numpy
import pandas as pd

from .base import BaseFeature


__all__ = ('ExternalData', )


class ExternalData(BaseFeature):
    '''
    Load external data and merge them based on some key.

    Parameters
    ----------
    input_type : str, default='label'
        Specifies the format the input values will be (currently, this only
        accepts values of 'label'). Note: these labels must by values that
        match the values defined by the `merge_key`.

    n_jobs : int, default=1
        Specifies the number of processes to create when generating the
        features. Positive numbers specify a specifc amount, and numbers less
        than 1 will use the number of cores the computer has.

    data_loaders : list of callable, default=None
        This is a collection of callable objects that return Pandas dataframes
        with data to be used. All of these objects will be called with no
        parameters, so the functions should be constructed accordingly.

    merge_key : str or list, default=None
        The feature columns to use to merge multiple datasets. If using Pandas
        dataframes, these should be the names of the columns that will be used
        to do an inner join on the data. If there is only one dataset, then
        this can be left as None.

    use_outer_join : bool, default=False
        Whether or not to do an outer join when merging collected datasets.

    use_only_numeric : bool, default=True
        Whether or not to only include numeric columns (as defined by
        numpy.number).

    drop_nans : bool, default=True
        Whether or not to drop any columns that contain nan values.

    Attributes
    ----------
    _merged : Pandas.Dataframe
        The final fully merged dataframe indexed by the merge_key.

    _valid_columns : tuple of str
        The list of columns where the datatypes are numbers and there are no
        nan values.
    '''
    ATTRIBUTES = ("_merged", )
    LABELS = ("_valid_columns", )

    def __init__(self, input_type='label', n_jobs=1, data_loaders=None,
                 merge_key=None, use_outer_join=False, use_only_numeric=True,
                 drop_nans=True):
        super(ExternalData, self).__init__(input_type=input_type,
                                           n_jobs=n_jobs)
        self.data_loaders = data_loaders
        self.merge_key = merge_key
        self.use_outer_join = use_outer_join
        self.use_only_numeric = use_only_numeric
        self.drop_nans = drop_nans
        self._merged = None
        self._valid_columns = None

    def fit(self, X, y=None):
        data = []
        for loader in self.data_loaders:
            data.append(loader())

        join_type = 'outer' if self.use_outer_join else 'inner'
        merged = data[0]
        for i, x in enumerate(data[1:]):
            merged = pd.merge(merged, x, on=self.merge_key, how=join_type,
                              suffixes=('', '_D%d' % i+1))

        self._merged = merged.set_index(self.merge_key)

        base = self._merged
        if self.use_only_numeric:
            base = base.select_dtypes(numpy.number)
        if self.use_drop_nans:
            base = base.dropna(axis=1)

        self._valid_columns = tuple(base.keys())
        return self

    def convert_input(self, X):
        if self.input_type != 'label':
            raise ValueError('This only accepts input_types of "label"')
        return X

    def _para_transform(self, X):
        self.check_fit()
        X = self.convert_input(X)
        results = self._merged.loc[X]
        return results[list(self._valid_columns)].values
