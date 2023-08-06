*ReLERNN*
*Recombination Landscape Estimation using Recurrent Neural Networks*
====================================================================

ReLERNN uses deep learning to infer the genome-wide landscape of recombination from as few as two diploid samples.
This repository contains the code and instructions required to run ReLERNN, and includes example files to ensure everything is working properly.   

## Instalation on linux
ReLERNN is installed using the supplied setup.py file. All dependencies will be automatically installed via pip.
Use the following commands to install ReLERNN:

'''
$ git clone https://github.com/kern-lab/ReLERNN.git
$ cd ReLERNN
$ python setup.py install
'''

It should be as simple as that.

## Testing ReLERNN
An example VCF file (10 haploid samples) and a shell script for running ReLERNN's four modules is located in $/ReLERNN/examples.
To test the functionality of ReLERNN simply use the following commands:

'''
$ cd examples
$ bash example_pipeline.sh
'''

Provided everything worked as planned, $ReLERNN/examples/example_output/ should be populated with a few directories along with the files: example.PREDICT.txt and example.PREDICT.BSCORRECT.txt.
The latter is the finalized output file with your recombination rate estimates.

The above example took X seconds to complete on a Xeon machine using four CPUs and one NVIDIA GeForce Titan X GPU.
Note that the parameters used for this example were only designed to test the success of the installation, not to make accurate predictions.
Please use guidlines below for the best results when analyzing real data.
While it is possible to run ReLERNN without a dedicated GPU, if you do try this, you are going to have a bad time.


