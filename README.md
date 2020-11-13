# q2_microbiome_age
-----------------------
QIIME 2 plugin for applying the microbiome age model trained in the meta-analysis or AGP data to the new microbiome studies.

Read more about the method in our paper:
* Huang S, Haiminen N, Carrieri A-P, Hu R, Jiang L, Parida L, Russell B, Allaband C, Zarrinpar A, Vázquez-Baeza Y, Belda-Ferre P, Zhou H, Kim H-C, Swafford AD, Knight R, Xu ZZ. 2020. Human skin, oral, and gut microbiomes predict chronological age. mSystems 5:e00630-19. https://doi.org/10.1128/mSystems.00630-19.


# Installation

You can install this plugin with conda or by cloning this repo and installing manually.
You need to have QIIME 2 version 2019.1 or later (though earlier versions of this plugin work with earlier versions of QIIME 2).
Also, regardless of which way you install, you need to be in a QIIME 2 environment for this to work.
[Install QIIME 2](https://docs.qiime2.org/2020.8/install/) and activate the QIIME 2 virtual environment (`source activate qiime2-2020.8`) before installing this plugin.

To install from conda, run:

```
conda install -c xx q2_microbiome_age
```

To install from this repo, clone the repo to your computer, `cd` into the main directory, and run:

```
python setup.py install
```

You can check that the installation worked by typing `qiime` on the command line.
The `microbiome_age` plugin should show up in the list of available plugins.


# Using the plugin

The only method in this plugin is `microbiome_age`, which predict the microbiome age for input samples based on the regression model trained in the larger data.

## Preparing your data

You'll need to prepare your ASV table and metadata file for use with this plugin.
Your ASV table should be imported as a [QIIME 2 artifact](https://docs.qiime2.org/2019.1/concepts/#data-files-qiime-2-artifacts), with **ASVs in rows** and **samples in columns**.


