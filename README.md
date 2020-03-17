Download infrasound waveform with webscrayping from 高知工科大学インフラサウンド観測ネットワークシステム
====

Download Infrasound waveform data witch get from 高知工科大学インフラサウンド観測ネットワークシステム with webscrayping and how to preprocess raw data.
And resampling and linear interpolation for trainig set and test set.

Flow
====
Copy InfsPreprocessing/Infs/ and rename folder(user) -> input infrasound URL(user) -> download
-> move no data -> resampling -> linear interpolation -> make graph of raw data

Usage
====
1. Copy this folder to ../InfsPreprocess/Infs and change name for in the following format.  
ex, Sakurazima_Ontake_Higashikorimoto_20181114_0043_24point2Pa  
2. Input Infrasound data URL to sample.csv of 2 row.
3. Run as follow if you prosess 2.  
`$ bash download.sh`
4. Run as follow because of preprocess row data in raw_data directory.  
`$ bash preprocessing_one_eruption.sh`

Requirement
====
Python 3.6.5  
numpy 1.14.3, matplotlib 2.2.2, pandas 0.23.0
