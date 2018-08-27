# Qiime 2 chemical structural and compositional similarity plugin for metabolomics data

This is a [QIIME 2](https://qiime2.org/) plugin computing the chemical structural and compositional dissimilarity metric in metabolomics data retrieved from [GNPS](https://gnps.ucsd.edu/).

## Installation

Once QIIME2 is [installed](https://docs.qiime2.org/2018.2/install/), activate your QIIME2 environment:
```
source activate qiime2-2018.6
```

and install the q2-cscs plugin with:

```
conda install -c askerdb q2-cscs
qiime dev refresh-cache
```

## Why use the chemical structural and compositional similarity (CSCS) distance metric over traditional distance metrics for metabolomics data?


The chemical structural and compositional similarity (CSCS) is a measure of chemical similarity proposed by [Sedio and coworkers](https://esajournals.onlinelibrary.wiley.com/doi/abs/10.1002/ecy.1689). It is a measure, which takes into account the chemical structural relatedness of the compounds detected within a sample submitted to tandem mass spectrometry (MS/MS) and analysed using mass spectral molecular networking ([Watrous et al., 2012](http://www.pnas.org/content/109/26/E1743.long); [Wang et al., 2016](https://www.nature.com/articles/nbt.3597)). Mass spectral molecular networks provide information about the structural relatedness of mass spectral features through a cosine score. This score is retrieved from a modified cosine calculation, taking into account the relative intensities of the fragment ions as well as the precursor *m/z* difference ([Watrous et al., 2012](http://www.pnas.org/content/109/26/E1743.long)). A) exemplifies a mass spectral molecular network. Nodes represent mass spectral features, whereas edges represent their structural relatedness (cosine score). CSCS integrates the cosine score into the compositional similarity calculation, for a detailed description consult [Sedio and coworkers](https://esajournals.onlinelibrary.wiley.com/doi/abs/10.1002/ecy.1689). The distance matrix, which is computed through q2-cscs represents the chemical structural and compositional dissimilarity for all pairs of samples in a feature table and corresponds to 1-CSCS. 

![](Example/PCoAs_UnitTest.jpg)

Given a hypothetical dataset, comprising 6 samples and a total of 10 mass spectral features with structural relatedness as depicted in A), CSCS depicts chemical differences between the samples more accurately (C) than for example the Bray-Curtis distance (B). Using CSCS samples sharing structurally related compounds (A) cluster more closely together in PCoA space. In contrast, using the Bray-Curtis distance, Samples 1 and 3, as well as Samples 4 and 5, can not be differentiated in PCoA space and samples sharing structurally related mass spectral features do not cluster.

## Files produced

The plugin generates one file:
  1. A `DistanceMatrix` type file [.qza]: This is the distance matrix computed using the chemical structural and compositional similarity metric. This distance matrix can for example be used for interactive PCoA in QIIME2 using [Emperor](https://academic.oup.com/gigascience/article-lookup/doi/10.1186/2047-217X-2-16).

## Examples

### 1) Unit testing with a small mock dataset

You can test whether the q2-cscs plugin is working properly, by calculating the pair-wise chemical structural and compositional dissimilarity metric on a small mock dataset.

#### Activate your qiime2 conda environment

To start the analyses activate your qiime2 conda environment: 

```
source activate qiime2-2018.6
```

#### Download the mock dataset

To compute the the chemical structural and compositional dissimilarity metric for all pairs of samples you will need two input files. A mass spectral feature table as well as an edges file containing pairwise cosine scores for all features provided in the feature table. 
You can download both a small mass spectral feature table ('small_GNPS_buckettable.qza') as well as an edges file ('small_GNPS_edges.tsv') from this Github repository:

```
wget https://raw.githubusercontent.com/madeleineernst/q2-cscs/master/tests/data/small_GNPS_buckettable.qza
wget https://raw.githubusercontent.com/madeleineernst/q2-cscs/master/tests/data/small_GNPS_edges.tsv
```

#### Compute the chemical structural and compositional dissimilarity metric for all pairs of samples in the mock dataset

To compute the chemical structural and compositional dissimilarity metric for all pairs of samples in the mock dataset type:
```
qiime cscs cscs --p-css-edges small_GNPS_edges.tsv --i-features small_GNPS_buckettable.qza --p-cosine-threshold 0.5 --p-normalization --o-distance-matrix small_cscs_distance_matrix.qza
```

The output file 'small_cscs_distance_matrix.qza' will contain the chemical structural and compositional dissimilarity metric for all pairs of samples within the mock dataset. You can open the 'small_cscs_distance_matrix.qza' file in a text editor (e.g. TextWrangler). The resulting distance-matrix should look as follows:

|  | Sample1 | Sample2 | Sample3 | Sample4 | Sample5 | Sample6 |
| :---         |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |
| Sample1   | 0   | 0.3502028286872648   | 0.6389226293131565   | 1   | 1   | 1   | 
| Sample2   |  0.3502028286872648  | 0   | 0.4405475372495642   | 1   | 1   | 1   |
| Sample3   |  0.6389226293131565  | 0.4405475372495642   | 0   | 1   | 1   | 1   | 
| Sample4   |  1  | 1   | 1   | 0   | 0.47084725634476177   | 0.9262994161594104   | 
| Sample5   |  1  | 1   | 1   | 0.47084725634476177   | 0   | 0.1819155452246134   | 
| Sample6   |  1  | 1   | 1   | 0.9262994161594104   | 0.1819155452246134   | 0   |  


### 2) Compute the chemical structural and compositional dissimilarity for a real-world dataset

#### Download mass spectral molecular network data from GNPS

To compute the chemical structural and compositional dissimilarity metric for all pairs of samples you will need two input files. A mass spectral feature table as well as an edges file containing pairwise cosine scores for all features provided in the feature table. Both files can be downloaded from https://gnps.ucsd.edu/ after performing mass spectral molecular networking. 
The example dataset used here can be accessed at [https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=5729dd0f7a47475abc879e164c237f56](https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=5729dd0f7a47475abc879e164c237f56). On the GNPS Job Status page select the “Download Bucket Table” option (1.). The feature table (a.) as well as the edges file (b.) will be contained within the unzipped folders and files from the .zip file that is downloaded:

![](Example/GNPS_Download.png)

To follow the example given here, you can also download the files shown above from GNPS using the command line:
```
curl -d "" 'https://gnps.ucsd.edu/ProteoSAFe/DownloadResult?task=5729dd0f7a47475abc879e164c237f56&view=download_cluster_buckettable' -o GNPS_output.zip
```

Then unzip the downloaded folder ('GNPS_output.zip') to a folder named 'GNPS_output/', copy the features and edges file to your working directory and rename them to 'GNPS_buckettable.tsv' and 'GNPS_edges.tsv':

```
unzip -d GNPS_output/ GNPS_output.zip
cp GNPS_output/METABOLOMICS-SNETS-5729dd0f-download_cluster_buckettable-main.tsv GNPS_buckettable.tsv
cp GNPS_output/networkedges_selfloop/c8a76183cbe644a194408b514ba51632.pairsinfo GNPS_edges.tsv
```

Mass spectral data as well as associated metadata used in this example have been compiled from [van der Hooft and co-workers (2017)](https://pubs.acs.org/doi/abs/10.1021/acs.analchem.7b01391). To visualize chemical dissimilarity across samples in an interactive PCoA space also download the metadata file provided in this Github repository:

```
wget https://raw.githubusercontent.com/madeleineernst/q2-cscs/master/Example/MappingFile_UrineSamples.txt
```

#### Activate your qiime2 conda environment

To start the analyses activate your qiime2 conda environment: 

```
source activate qiime2-2018.6
```

#### Convert your mass spectral feature table to the .qza format

Before you can calculate the chemical structural and compositional dissimilarity matrix, you need to convert your feature table (GNPS_buckettable.tsv) from the .tsv format to the .qza format.

First, convert the .tsv feature table (GNPS_buckettable.tsv) to a .biom feature table (GNPS_buckettable.biom):

```
biom convert -i GNPS_buckettable.tsv -o GNPS_buckettable.biom --table-type="OTU table" --to-hdf5
```

Then convert the .biom feature table (GNPS_buckettable.biom) to a .qza feature table (GNPS_buckettable.qza):

```
qiime tools import --type 'FeatureTable[Frequency]' --input-path GNPS_buckettable.biom --output-path GNPS_buckettable.qza
```
#### Compute the chemical structural and compositional dissimilarity metric for all pairs of samples in your feature table

To compute the chemical structural and compositional dissimilarity metric for all pairs of samples in your feature table type:

```
qiime cscs cscs --p-css-edges GNPS_edges.tsv --i-features GNPS_buckettable.qza --p-cosine-threshold 0.5 --p-normalization --o-distance-matrix cscs_distance_matrix.qza
```

Besides the mass spectral feature table (GNPS_buckettable.qza) and the edges file (GNPS_edges.tsv), you can specify two parameters:

`--p-cosine-threshold`: Minimum cosine score that must occur between two features to be included in the calculation. All cosine scores below this threshold will be set to 0. Set this parameter to the same value as you specified during mass spectral molecular network analysis on GNPS in the “Min Pairs Cos” option, if you want to integrate structural relationships as displayed in your network. The default value is set to 0.6.\
`--p-normalization`: This parameter will perform Total Ion Current (TIC) normalization of your feature table prior to calculating the chemical structural and compositional dissimilarity metric.

Once the computation completed, the results will be saved in a distance matrix in the .qza format (here ‘cscs_distance_matrix.qza’). You can use this distance matrix to visualize the chemical structural and compositional dissimilarity across your samples in an interactive PCoA space using [Emperor](https://academic.oup.com/gigascience/article-lookup/doi/10.1186/2047-217X-2-16).

#### Visualize the chemical structural and compositional dissimilarity in interactive PCoA space 

To create PCos from the chemical structural and compositional dissimilarity matrix type:

```
qiime diversity pcoa --i-distance-matrix cscs_distance_matrix.qza --o-pcoa cscs_PCoA.qza
```

To create an interactive ordination plot of the above created PCoA with integrated sample metadata, prepare a [metadata file](https://docs.qiime2.org/2018.6/tutorials/metadata/). You can find a metadata file for this example dataset within the *Example* folder. Make sure that the Sample IDs provided in the metadata file correspond to the Sample IDs in your distance_matrix.qza file. Then type:

```
qiime emperor plot --i-pcoa cscs_PCoA.qza --m-metadata-file MappingFile_UrineSamples.txt --o-visualization cscs_PCoA.qzv
```

To visualize the interactive PCoA type:

```
qiime tools view cscs_PCoA.qzv
```

Or drag and drop the cscs_PCoA.qzv file to:
[https://view.qiime2.org/](https://view.qiime2.org/)

#### Compare the chemical structural and compositional dissimilarity to the Bray-Curtis dissimilarity

If you want to compare the chemical structural and compositional distance to traditional distance metrics such as Bray-Curtis in PCoA space, you can calculate Bray-Curtis distances for the same feature table using QIIME 2:

```
qiime diversity beta --i-table GNPS_buckettable.qza  --p-metric braycurtis --o-distance-matrix braycurtis_GNPS_buckettable.qza

qiime diversity pcoa --i-distance-matrix braycurtis_GNPS_buckettable.qza --o-pcoa braycurtis_PCoA.qza

qiime emperor plot --i-pcoa braycurtis_PCoA.qza --m-metadata-file MappingFile_UrineSamples.txt --o-visualization braycurtis_PCoA.qzv
```

![](Example/PCoAs_Urine.jpg)

In our example, the chemical structural and compositional dissimilarity metric revealed a stronger age-dependent gradient of urine samples (B) when compared to the Bray-Curtis dissimilarity (A).

To compare both metrics, you can also run a Mantel test and/or a Procrustes analysis:

```
qiime diversity mantel --i-dm1 cscs_distance_matrix.qza --i-dm2 braycurtis_GNPS_buckettable.qza --o-visualization mantel.qzv
qiime diversity procrustes-analysis --i-reference braycurtis_PCoA.qza --i-other cscs_PCoA.qza --output-dir ./procrustes-out
qiime emperor procrustes-plot --i-reference-pcoa procrustes-out/transformed_reference.qza --i-other-pcoa procrustes-out/transformed_other.qza --m-metadata-file MappingFile_UrineSamples.txt --o-visualization procrustes-out/plot.qzv
```


