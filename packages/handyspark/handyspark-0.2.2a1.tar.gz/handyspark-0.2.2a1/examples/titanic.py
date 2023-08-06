import findspark
findspark.init()

from handyspark import Bucket, Quantile, BinaryClassificationMetrics
from handyspark.util import counts_to_df
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StringType, IntegerType, ArrayType, DoubleType
import matplotlib.pyplot as plt

from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.pipeline import Pipeline, PipelineModel
from pyspark.ml.feature import VectorAssembler
import pandas as pd

spark = SparkSession.builder.getOrCreate()

import numpy as np
#sdf = spark.read.parquet('/media/dvgodoy/FILES/D2S/Spark/kmeans_data.parquet')
sdf = spark.read.csv('../tests/rawdata/train.csv', header=True, inferSchema=True)

pdf = pd.read_csv('../tests/rawdata/train.csv')
pret = pdf['Age'].hist()

hdf = sdf.toHandy()

hret = hdf.cols['Embarked'].hist()

from handyspark.plot import strat_histogram
res = hdf.stratify('Pclass').cols['Age'].hist()
hdf2 = hdf.stratify(['Sex', 'Pclass']).fill(categorical=['Embarked'], continuous=['Age'])

hdf.outliers(k=3.)
outliers = hdf.stratify(['Sex', 'Pclass']).fill(continuous=['Age'], strategy=['median']).stratify(['Sex', 'Pclass']).cols[['Fare', 'Age', 'SibSp']].get_outliers(critical_value=.9)
hdf = hdf.fillna(0.0).remove_outliers(critical_value=.1)
hres = hdf.cols[['Survived', 'Pclass']].mutual_info()
mi1 = hdf.stratify('Sex').cols[['Survived', 'Pclass']].mutual_info()
#ent1 = hdf.cols[['Age', 'Pclass']].entropy()
#ent2 = hdf.stratify('Sex').cols['Pclass'].entropy()
#ent3 = hdf.stratify('Sex').cols[['Pclass', 'Embarked']].entropy()
#hdf.stratify(['Sex', Bucket('Age', 2)]).cols['Embarked'].value_counts()
hdf.stratify(['Sex', Bucket('Age', 2)]).cols['Embarked'].hist(figsize=(8, 6))
#hdf.stratify(['_c0']).cols['_c7'].hist()
hdf.stratify(['_c0', Bucket('_c6', 3)]).cols['_c7'].hist()
hdf.stratify(['_c0', Bucket('_c6', 3)]).cols['_c2'].hist()
#hdf.stratify('_c0').cols[['_c1', '_c2']].scatterplot()
#hdf.cols['_c1'].boxplot()

hdf2 = hdf.stratify('Sex').fence('Age')
hdf2.fence('Fare')
print(hdf2.fences_)
print(hdf.cols[['Fare', 'Age']].corr())
print(hdf.stratify('Sex').cols[['Fare', 'Age']].corr())
print(hdf.isnull(ratio=True))
print(hdf.stratify('Sex').isnull(ratio=True))
print(hdf.nunique())
print(hdf.stratify('Sex').nunique())
print(hdf.outliers(ratio=True))
print(hdf.stratify('Sex').outliers(ratio=True))
print(hdf.cols['Embarked'].value_counts())
print(hdf.stratify('Sex').cols['Embarked'].value_counts())
print(hdf.cols['Embarked'].mode())
print(hdf.stratify('Sex').cols['Embarked'].mode())
print(hdf.cols['Age'].mean())
print(hdf.stratify('Sex').cols['Age'].mean())
print(hdf.cols['Age'].median())
print(hdf.stratify('Sex').cols['Age'].median())

hdf.stratify([Bucket('Fare', 3)]).fill(continuous=['Age'], strategy=['mean'])
hdf.stratify(['Sex']).fence(['Fare'])
hdf.outliers(ratio=True)
hdf.stratify(['Sex']).outliers(ratio=True)
#hdf.cols['Fare'].boxplot()
#hdf.cols[['Fare', 'Age']].boxplot()
#hdf.stratify(['Sex']).cols['Fare'].boxplot()
#hdf.stratify([Bucket('Age', 5)]).cols['Fare'].boxplot()
#hdf.stratify(['Sex', 'Embarked']).cols[['Fare', 'Age']].boxplot()
hdf.stratify([Bucket('Age', 5)]).cols['Fare'].hist()
hdf.stratify([Bucket('Age', 5)]).cols['Embarked'].hist()
hdf.stratify([Bucket('Age', 5)]).cols[['Fare', 'Age']].scatterplot()
#hdf.stratify(['Sex']).cols[['Fare', 'Age']].scatterplot()
#hdf.stratify(['Sex', 'Embarked']).cols['Fare'].hist()
#print(hdf.stratify(['Sex', Bucket('Age', 3)]).cols['Embarked'].mode())
#print(hdf.stratify(['Sex']).isnull())
#print(hdf.stratify(['Sex']).cols['Embarked'].nunique())
#print(hdf.stratify(['Sex']).cols['Embarked'].mode())
#print(hdf.cols['Embarked'].mode())

#print(mutual_info(sdf.withColumn('Sex', F.when(F.col('Sex') == 'male', 1).otherwise(0)), ['Pclass', 'Sex', 'Survived']))
#print(hdf.assign(x=ArrayType(DoubleType()).ret(lambda Fare: Fare.apply(lambda v: [v, v*2]))).take(1))
from typing import List, Dict
def make_list(Fare) -> List[float]:
    return Fare.apply(lambda v: [v, v*2])
def make_dict(Fare) -> Dict[float, bool]:
    return Fare.apply(lambda v: {v: v > 100})
#print(hdf.assign(x=ArrayType(DoubleType()).ret(make_list)).take(1))
print(hdf.assign(x=make_list).take(1))
# NOT IMPLEMENTED
#print(hdf.assign(x=make_dict).take(1))

hdf4 = hdf.fence(['Fare', 'Age'])
print(hdf4.fences_)
ft = hdf4.transformers.fencer()
new_hdf = ft.transform(hdf)
print(new_hdf.select(F.max('Fare'), F.max('Age')).take(1))

print(hdf.assign(FindMr=hdf.pandas['Name'].str.find(sub='Mr.')).take(1))
print(hdf.assign(FindMr=IntegerType.ret(lambda Name: Name.str.find(sub='Mr.'))).take(1))
print(hdf.assign(x=StringType.ret(lambda Fare: (Fare * 2).map('${:,.2f}'.format))).take(1))

# from pyspark.sql.functions import udf
# @udf('double')
# def myfunc(Fare):
#     return Fare * y
# print(hdf.select(myfunc('Fare')).take(1))
assem = VectorAssembler(inputCols=['Pclass', 'Survived'], outputCol='features')
vc = assem.transform(hdf).handy.value_counts('features')
print(counts_to_df(vc, ['Pclass', 'Survived'], 100))

hdf3 = hdf.stratify([Quantile('Fare', 5), 'Sex']).fill('Age', strategy='median')
hdf3 = hdf.stratify(['Pclass', 'Sex']).fill('Age', strategy='median')
ht = hdf3.transformers.imputer()
new_hdf = ht.transform(hdf)

hdf = hdf.assign(logFare=lambda Fare: np.log(Fare + 1))
print(hdf.pandas.abs('Fare', alias='absFare').take(1))
print(hdf.pandas.str.find('Name', sub='Mr.', alias='FindMr').take(1))

assem = VectorAssembler(inputCols=['Pclass', 'Age', 'Fare'], outputCol='features')
rf = RandomForestClassifier(labelCol='Survived')
pipe = Pipeline(stages=[ht, assem, rf])
data = hdf.select('Pclass', 'Age', 'Fare', 'Survived').dropna()
model = pipe.fit(data)
# model.save('pipeline.parquet')

pred = model.transform(data).handy
bcm = BinaryClassificationMetrics(pred.to_metrics_RDD('probability', 'Survived'))
print(bcm.confusionMatrix(.3))
print(bcm.areaUnderROC)
df = bcm.getMetricsByThreshold()
print(df.toPandas())

sdf2 = spark.read.csv('../rawdata/train.csv', header=True, inferSchema=True)
hdf3 = hdf.stratify(['Pclass', 'Sex']).fill(continuous='Age', strategy='median')
hdf3.stratify([Bucket('Age', 3), 'Sex']).boxplot('Fare', figsize=(12, 6)).savefig('boxplot1.png', type='png')
hdf3.stratify(['Pclass', 'Sex']).boxplot(['Fare', 'Age'], figsize=(12, 6)).savefig('boxplot2.png', type='png')
hdf3.stratify(['Pclass', 'Sex']).hist('Fare', figsize=(12, 6)).savefig('hist1.png', type='png')
hdf3.stratify(['Pclass', 'Sex']).hist('Embarked', figsize=(12, 6)).savefig('hist2.png', type='png')
hdf3.stratify(['Pclass', 'Sex']).scatterplot('Fare', 'Age', figsize=(12, 6)).savefig('scatter.png', type='png')
print(hdf3.stratify([Bucket('Age', 5), 'Sex']).mode('Fare'))
print(hdf3.stratify(['Pclass', 'Sex']).sample(withReplacement=False, fraction=.1).show())
print(hdf3.stratify(['Pclass', 'Sex']).corr_matrix(['Fare', 'Age']))
print(hdf.value_counts('Embarked'))
print(hdf3.statistics_)
hdf2 = hdf3.fill(sdf2)
print(hdf.corr_matrix())

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
hdf = hdf.fill(continuous='Age', categorical=['Embarked'], strategy='median')
hdf.hist('Embarked', ax=ax1)
hdf.hist('Fare', ax=ax2)
hdf.scatterplot('Fare', 'Age', ax=ax3)
hdf.boxplot('Fare', ax=ax4)

fig.tight_layout()
fig.savefig('eda.png', format='png')
