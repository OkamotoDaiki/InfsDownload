Download infrasound waveform with webscrayping from ���m�H�ȑ�w�C���t���T�E���h�ϑ��l�b�g���[�N�V�X�e�� webscrayping and how to preprocess raw data
====

Download Infrasound waveform data witch get from ���m�H�ȑ�w�C���t���T�E���h�ϑ��l�b�g���[�N�V�X�e��.
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
3. Run as follow if you prosess 1. 
$ bash download.sh
4. Run as follow because of preprocess row data in raw_data directory.
$ bash preprocessing_one_eruption.sh

version
20200313 v0.5
Add README.md

(forget) v0.4
Became possible to run multi script at once with shell-script.
Execution command

>>>bash preprocessing_one_eruption.sh

20191117 v0.3
If user forget processing 4., tell error.

(forget) v0.2
�_�E�����[�hURL�݂̂����s�����悤�ɁAraw_data�t�H���_�ɕۑ������悤�ɂ����B
�ڍׁFdownload.py�ɂāA�_�E�����[�hURL�ȊO���w�肳���ƁAValueError�ƂȂ������AValueError��������邱�ƂŃG���[�𖳎��ł���悤�ɂȂ����B



