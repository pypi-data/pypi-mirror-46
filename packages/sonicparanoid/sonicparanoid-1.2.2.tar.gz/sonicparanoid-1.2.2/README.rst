SonicParanoid
=============

A fast, accurate and easy to use orthology inference tool.

Description
===========

SonicParanoid is a stand-alone software for the identification of orthologous relationships among multiple species. SonicParanoid is an open source software released under the GNU GENERAL PUBLIC LICENSE, Version 3.0 (GPLv3), implemented in Python3, Cython, and C++. It works on Linux and Mac OSX. The software is designed to run using multiple processors and proved to be up to 1245X faster then InParanoid, 166X faster than Proteinortho, and 172X faster than OrthoFinder 2.0 with an accuracy comparable to that of well-established orthology inference tools.
Thanks to its speed, accuracy, and usability SonicParanoid substantially relieves the difficulties of orthology inference for biologists who need to construct and maintain their own genomic datasets.

SonicParanoid was tested on the 2011 version of a benchmark proteome dataset provided by the Quest for Orthologs (QfO) consortium (https://questfororthologs.org), and its accuracy was assessed, and compared to that of other 13 methods, using a publicly available orthology benchmarking service (http://orthology.benchmarkservice.org).

SonicParanoid is available at http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid.

Citation
===========

> Salvatore Cosentino and Wataru Iwasaki (2018) SonicParanoid: fast, accurate and easy orthology inference. Bioinformatics

> Volume 35, Issue 1, 1 January 2019, Pages 149–151,

> https://doi.org/10.1093/bioinformatics/bty631

Changelog
===========

1.2.2 (May 13, 2019)
 - Fix: solved bug that caused MCL to be not properly combined on some Linux distributions
 - Info: migrated to `GitLab`__

__ https://gitlab.com/salvo981/sonicparanoid2

1.2.1 (May 10, 2019)
 - Fix: solved bug related to random missing alignments
 - Info: this issue was first described in `here`__

__ https://bitbucket.org/salvocos/sonicparanoid/issues/2/two-problems-with-qfo2011

1.2.0 (April 26, 2019)
 - Change: Markov Clstering (MCL) is now used by default for the creation of ortholog groups
 - Enhancement: the MCL inflation can be controlled through the parameter --inflation
 - Enhancement: Output file with single-copy ortholog groups
 - Feature: single-linkage clustering for ortholog groups creation through the --single-linkage parameter
 - Enhancement: added secondary program to filter ortholog groups
 - Info: type "sonicparanoid-extract --help" to see the list of options
 - Enhancement: Filter ortholog groups by species ID
 - Enhancement: Filter ortholog groups by species composition (e.g., only groups with given number of species)
 - Enhancement: Extract FASTA sequences of orthologs in selected groups
 - Fix: The correct version of SonicParanoid is now shown in the help
 - Others: General bug fixes and under-the-hood improvements

1.1.2 (March, 2019)
 - Enhancement: Filter ortholog groups by species ID
 - Enhancement: Filter ortholog groups by species composition (e.g., only groups with given number of species)
 - Enhancement: Extract FASTA files corresponding orthologs in selected groups
 - Fix: The correct version of SonicParanoid is now shown in the help

1.1.1 (January 24, 2019)
 - Enhancement: No restriction on file names
 - Enhancement: No restriction on symbols used in FASTA headers
 - Enhancement: Added file with genes that could not be inserted in any group (not orthologs)
 - Enhancement: Added some statistics on the predicted ortholog groups
 - Enhancement: Update runs are automatically detected
 - Enhancement: Improved inference of in-paralogs
 - Change: The directory structure has been redesigned to better support run updated

1.0.14 (October 19, 2018)
 - Enhancement: a warning is shown if non-protein sequences are given in input
 - Enhancement: upgraded to MMseqs2 6-f5a1c
 - Enhancement: SonicParanoid is now available through Bioconda (https://bioconda.github.io/recipes/sonicparanoid/README.html)

1.0.13 (September 18, 2018)
 - Fix: allow FASTA headers containing the '@' symbol

1.0.12 (September 7, 2018)
 - Improved accuracy
 - Added new sensitivity mode (most-sensitive)
 - Fix: internal input directory is wiped at every new run
 - Fix: available disk space calculation

1.0.11 (August 7, 2018)
 - Added new program (sonicparanoid-extract) to process output multi-species clusters
 - Added the possibility to analyse only 2 proteomes
 - Added support for Python3.7
 - Python3 versions: 3.5, 3.6, 3.7
 - Upgraded MMseqs2 (commit: a856ce, August 6, 2018)

1.0.9 (May 10, 2018)
 - First public release
 - Python3 versions: 3.4, 3.5, 3.6
