README
======

SimLoRD - Simulate long Read Data
---------------------------------

SimLoRD is a read simulator for third generation sequencing reads and is
currently focused on the Pacific Biosciences SMRT error model.

Reads are simulated from both strands of a provided or randomly
generated reference sequence.

Features
~~~~~~~~

-  The reference can be read from a FASTA file or randomly generated
   with a given GC content. It can consist of several chromosomes, whose
   structure is respected when drawing reads. (Simulation of genome
   rearrangements may be incorporated at a later stage.)
-  The read lengths can be determined in four ways: drawing from a
   log-normal distribution (typical for genomic DNA), sampling from an
   existing FASTQ file (typical for RNA), sampling from a a text file
   with integers (RNA), or using a fixed length
-  Quality values and number of passes depend on fragment length.
-  Provided subread error probabilities are modified according to number
   of passes
-  Outputs reads in FASTQ format and alignments in SAM format

System requirements
~~~~~~~~~~~~~~~~~~~

-  `python3 <https://www.python.org/>`__
-  `scipy <http://www.scipy.org/>`__
-  `numpy <http://www.numpy.org/>`__
-  `pysam <http://pysam.readthedocs.org/en/latest/>`__
-  `dinopy <https://bitbucket.org/HenningTimm/dinopy>`__

We recommend using
`miniconda <http://conda.pydata.org/miniconda.html#miniconda>`__ and
creating an environment for SimLoRD

::

    # Create and activate a new environment called simlord
    conda create -n simlord python=3 pip numpy scipy cython
    source activate simlord

    # Install packages that are not available with conda from pip
    pip install pysam
    pip install dinopy
    pip install simlord

    # You now have a 'simlord' script; try it:
    simlord --help

    # In case of a new version update as follows:
    pip install simlord --upgrade 

    # To switch back to your normal environment, use
    source deactivate

Platform support
~~~~~~~~~~~~~~~~

SimLoRD is a pure Python program. This means that it runs on any
operating system (OS) for which Python 3 and the other packages are
available.

Example usage
~~~~~~~~~~~~~

**Example 1:** Simulate 10000 reads for the reference ref.fasta, use the
default options for simulation and store the reads in ``myreads.fastq``
and the alignment in ``myreads.sam``.


::

    simlord  --read-reference ref.fasta -n 10000  myreads


**Example 2:** Generate a reference with 10 mio bases GC content 0.6
(i.e., probability 0.3 for both C and G; thus 0.2 probability for both A
and T), store the reference as random.fasta, and simulate 10000 reads
with default options, store reads as ``myreads.fastq``, do not store
alignments.

::

    simlord --generate-reference 0.6 10000000 --save-reference random.fasta\
            -n 10000 --no-sam  myreads


**Example 3:** Simulate reads from the given ``reference.fasta``, using
a fixed read length of 5000 and custom subread error probabilities (12%
insertion, 12% deletion, 2% substitution). As before, save reads as
``myreads.fastq`` and ``myreads.sam``.

::

    simlord --read-reference reference.fasta  -n 10000 -fl 5000\
            -pi 0.12 -pd 0.12 -ps 0.02  myreads


A full list of parameters, as well as their documentation, can be found `here <https://bitbucket.org/genomeinformatics/simlord/wiki/Home>`__.

Last Changes
~~~~~~~~~~~~

**Version 1.0.2 (2017-03-17)**

*New Features*

- Draw chromosomes for reads weighted with their length instead of equal distributed. This leads to a equal distributed read coverage over the chromosomes. Previous behaviour with equal probabilities for each chromosome can be activated with parameter --uniform-chromosome-probability.

- Parameter --coverage: Determine number of reads depending on the desired read coverage of the whole reference genome.

- Parameter --without-ns: Sample the reads only from regions completly without Ns.

Warning: Using --without-ns may lead to biased read coverage depending on the size of contigs without Ns and the expected readlength.

*Bugs fixed*

- CIGAR string had sometimes wrong count of last match because of false extension after deletion.


**Version 1.0.1 (2017-01-03)**

*Bugs fixed*

- Removed nargs=1 at parameter --probability-threshold leading to an error when changing the parameter.

**Version 1.0.0 (2016-07-13)**

*API Changes*

- Changed SEQ in SAM file to reverse complemented read instead of the original read for reads mapping to the reverse complement of the reference.

Example:
::

    reference       ATCG     read   CAAT
    true alignment  ||X|
                    ATTG

    Before: SEQ CAAT and CIGAR string 2=1X1=
    Now:    SEQ ATTG and CIGAR string 2=1X1=


License
~~~~~~~

SimLoRD is Open Source and licensed under the `MIT
License <http://opensource.org/licenses/MIT>`__.