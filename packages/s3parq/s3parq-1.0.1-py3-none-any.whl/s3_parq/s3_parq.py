import boto3
from .publish_parq import S3PublishParq
from .fetch_parq import S3FetchParq
import pandas as pd
import sys
import logging


class S3Parq:

    def __init__(self, **kwargs):
        self._set_kwargs_as_attrs(**kwargs)
        self.logger = logging.getLogger(__name__)

    def publish(self, dataset: str = None, bucket: str = None, dataframe: pd.DataFrame = None, prefix: str = None, partitions: iter = None)->None:
        # this round-about setting of args gives IDEs back hinting and adds mechanical type checking.
        for attr, val in {"dataset": dataset, "bucket": bucket, "dataframe": dataframe, "partitions": partitions, "prefix": prefix}.items():
            if val is not None:
                self._set_kwargs_as_attrs({attr: val})
                self.logger.debug(
                    f"Set publish instance value {attr} to {val}")
        required_attributes = ('dataset', 'bucket', 'dataframe',)
        self._check_required_attr(required_attributes)

        pub = S3PublishParq(dataset=self._dataset,
                      bucket=self._bucket,
                      dataframe=self._dataframe,
                      prefix=getattr(self, "_prefix", ''),
                      partitions=getattr(self, "_partitions", [])
                      )
        return pub.publish()

    def fetch(self, dataset: str = None, bucket: str = None, filters: dict = None, prefix: str = None)->None:
        # this round-about setting of args gives IDEs back hinting and adds mechanical type checking.
        for attr, val in {"dataset": dataset, "bucket": bucket, "filters": filters, "prefix": prefix}.items():
            if val is not None:
                self._set_kwargs_as_attrs({attr: val})
                self.logger.debug(f"Set fetch instance value {attr} to {val}")

        required_attributes = ('dataset', 'bucket',)
        self._check_required_attr(required_attributes)
        
        fetcher = S3FetchParq(dataset=self._dataset,
                    bucket=self._bucket,
                    filters=getattr(self,"_filters",dict()),
                    prefix=getattr(self,"_prefix",'')
                    )
        
        return fetcher.fetch()

    @property
    def dataset(self)->str:
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: str)->None:
        self._type_check_attr('dataset', dataset)
        self._dataset = dataset

    @property
    def bucket(self)->str:
        return self._bucket

    @bucket.setter
    def bucket(self, bucket: str)->None:
        self._type_check_attr('bucket', bucket)
        self._bucket = bucket

    @property
    def dataframe(self)->pd.DataFrame:
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame)->None:
        self._type_check_attr('dataframe', dataframe)
        # cannot support timedelta at this time
        for tp in dataframe.dtypes:
            if tp.name.startswith('timedelta'):
                fail_message = "Sorry, pyarrow does not support parquet conversion of timedelta columns to parquet."
                self.logger.critical(fail_message)
                raise NotImplementedError(fail_message)

        self._dataframe = dataframe

    @property
    def filters(self)->dict:
        return self._filters

    @filters.setter
    def filters(self, filters: dict)->None:
        self._type_check_attr('filters', filters)
        self._filters = filters

    @property
    def prefix(self)->str:
        return self._prefix

    @prefix.setter
    def prefix(self, prefix: str)->None:
        self._type_check_attr('prefix', prefix)
        self._prefix = prefix

    def _check_required_attr(self, attributes: iter)->None:
        """ make sure all required attributes are set before running.
            The sys._getframe bit is the name of the calling function (in this case S3Parq.fetch / S3Parq.publish).
        """
        for required_attr in attributes:
            if not hasattr(self, required_attr):
                fail_message = f"Unable to call S3Parq.{sys._getframe(1).f_code.co_name}; missing required attribute {required_attr}"
                self.logger.critical(fail_message)
                raise ValueError(fail_message)

    def _type_check_attr(self, attr: str, value)->None:
        """ checks typing of attribute and throws error if it is incorrect."""
        for k in [('dataset', str,),
                  ('bucket', str,),
                  ('prefix', str,),
                  ('partitions',list,),
                  ('dataframe', pd.DataFrame,),
                  ('filters', dict,)]:
            if attr == k[0]:
                if not isinstance(value, k[1]):
                    fail_message = f"Bad value for {attr}; {value} is not an instance of {k[1]}"
                    self.logger.critical(fail_message)
                    raise TypeError(fail_message)

    def _set_kwargs_as_attrs(self, **kwargs)->None:
        """ type check and set instance attributes."""
        for key in kwargs.keys():
            self._type_check_attr(key, kwargs[key])
            self.__dict__["_"+key] = kwargs[key]
