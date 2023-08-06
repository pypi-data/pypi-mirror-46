# 0.13.0 / 2019-05-19

  * seasalt.ProbaTransformer added

# 0.12.2 / 2019-05-16

  * ignore NaN while fitting pdf1.HistDensity

# 0.12.1 / 2019-04-21

  * wrong stacking fixed in seasalt.MultiOutputClassifier2.fit

# 0.12.0 / 2019-04-20

  * seasalt.MultiBinaryToMultiClass added

# 0.11.0 / 2019-04-17

  * explicit mechansim to load verto transformers with default settings

# 0.10.1 / 2019-04-17

  * Fixed the globals() issue in transformer_custom_settings

# 0.10.0 / 2019-04-17

  * verto.raw1 to copy the raw features with mlxtend's CopyTransformer

# 0.9.2 / 2019-04-17

  * hstack replaced by concatenate in transformer_custom_settings b/c it throws error in production

# 0.9.1 / 2019-04-16

  * loading error fixed

# 0.9.0 / 2019-04-16

  * read "trans*" objects from globals to merge multiple transformers with seasalt.transformer_custom_settings

# 0.8.1 / 2019-04-16

  * verto.gnb1 renamed as verto.nb1

# 0.8.0 / 2019-04-16

  * MultiOutputClassifier2 that can handle fit_params
  * verto.rnd1.RandomFeature for Feature Importance analysis
  * verto.gnb1.SimpleGNB to fit simple NB models and use predictions as features

# 0.7.0 / 2019-04-14

  * OneHot encoded KMeans as feature

# 0.6.0 / 2019-04-14

  * QuantileTransformer added

# 0.5.0 / 2019-04-11

  * Isolation Forest added as verto.out1. Use anomaly score as feature

# 0.4.0 / 2019-04-05

  * Binning transformer verto.pdf1.HistDensity to estimate
    the PDF of a certain value.

# 0.3.1 / 2019-04-04

  * allow to set L1 alpha in verto.dim4.PcaModelSelect

# 0.3.0 / 2019-04-03

  * verto.PcaModelSelect, verto.dim4, dim5, dim5 added

# 0.2.0 / 2019-04-02

  * specified how to generate feature names in verto
  * `verto.dim1` added
  * `seasalt.create_feature_names` and `verto` code adjusted to it

# 0.1.4 / 2019-03-30

  * Fix #2 -- pretty summary

# 0.1.3 / 2019-03-30

  * Fix #3 -- verto.dim2 Pipeline wrapped into PcaMinka class

# 0.1.2 / 2019-03-30

  * Fix #1 -- "__repr__" and "__str__" method of verto.dim3.PcaEv aligned

# 0.1.1 / 2019-03-29

  * modules added in setup.py

# 0.1.0 / 2019-03-25

  * Initial upload

# 0.0.0 / 2018-12-21

  * Pre-release development phase started
