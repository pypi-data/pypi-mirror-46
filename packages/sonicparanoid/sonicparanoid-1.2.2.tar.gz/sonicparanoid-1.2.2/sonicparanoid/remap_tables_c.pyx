from libc.stdio cimport *
from libc.stdlib cimport atoi
from libc.stdlib cimport atof
import sys
import os
import pickle
import multiprocessing as mp
from typing import Dict, List

cdef extern from "stdio.h":
    #FILE * fopen ( const char * filename, const char * mode )
    FILE *fopen(const char *, const char *)
    #int fclose ( FILE * stream )
    int fclose(FILE *)
    #ssize_t getline(char **lineptr, size_t *n, FILE *stream);
    ssize_t getline(char **, size_t *, FILE *)



### Worker functions (1 cpu) ###
def consume_remap_pairwise_relations(jobs_queue, results_queue, new2OldHdrAllSp: Dict[str, Dict[str, str]]) -> None:
    """Remap pairsire relation using 1 cpu."""
    # jobs_queue contains tuples with input and output paths
    while True:
        current_input = jobs_queue.get(True, 1)
        if current_input is None:
            break
        inTbl, outTbl = current_input
        # extract he species names
        rawPair = os.path.basename(inTbl)
        A, B = rawPair[6:].split("-", 1)
        remappedPair = os.path.basename(outTbl)
        # remap pairwise relations
        if A == B:
          remap_pairwise_relations(inTbl, outTbl, new2OldHdrAllSp[A], new2OldHdrAllSp[A], debug=False)
        else:
          remap_pairwise_relations(inTbl, outTbl, new2OldHdrAllSp[A], new2OldHdrAllSp[B], debug=False)
        # add the computed pair
        results_queue.put((rawPair, remappedPair))



### Job processing Functions
def remap_pairwise_relations_parallel(pairsFile, runDir=os.getcwd(), orthoDbDir=os.getcwd(), threads=4, debug=False) -> None:
    """Remap pairwise ortholog relations in parallel."""
    if debug:
        print('\nremap_pairwise_relations_parallel :: START')
        print('File with pairs to be mapped: {:s}'.format(pairsFile))
        print('Run directory: {:s}'.format(runDir))
        print('Directory with ortholog relations to be mapped: {:s}'.format(orthoDbDir))
        print('Threads:{:d}'.format(threads))
    # get input files paths
    inPaths: List[str] = []
    # Use the file with pairs
    for pair in open(pairsFile, "r"):
      pair = pair[:-1]
      tmpPath = os.path.join(orthoDbDir, "{:s}/table.{:s}".format(pair, pair))
      if os.path.isfile(tmpPath):
        inPaths.append(tmpPath)
      else:
        sys.stderr.write("\nERROR: the ortholog relationship file for the pair {:s} was not found!\n".format(pair))
        sys.exit(-5)
    if debug:
      print("Pairwise tables to be remapped:\t{:d}".format(len(inPaths)))
    # output directory for remapped tables
    remapOutDir = os.path.join(runDir, "pairwise_orthologs/")
    # load the species IDs mapping
    speciesFile = os.path.join(runDir, "species.tsv")
    id2SpDict: Dict[str, str] = {}
    for ln in open(speciesFile, "r"):
      mapId, spName, d1 = ln.split("\t", 2)
      if not mapId in id2SpDict:
        id2SpDict[mapId] = spName

    # create the queue and start adding
    remap_queue = mp.Queue(maxsize=len(inPaths) + threads)

    # load all mapping dictionaries
    new2OldHdrAllSp: Dict[str, Dict[str, str]] = {}

    # fill the queue with the file paths
    for fpath in inPaths:
        sys.stdout.flush()
        bname = os.path.basename(fpath)
        A, B = bname[6:].split("-", 1)
        # load the mapping dictionaries if necessary
        if A not in new2OldHdrAllSp:
          # load the pickle
          tmpPickle = os.path.join(runDir, "hdr_{:s}.pckl".format(A))
          with open(tmpPickle, "br") as fd:
            new2OldHdrAllSp[A] = pickle.load(fd)
        # now do the same thing for B
        if B not in new2OldHdrAllSp:
          # load the pickle
          tmpPickle = os.path.join(runDir, "hdr_{:s}.pckl".format(B))
          with open(tmpPickle, "br") as fd:
            new2OldHdrAllSp[B] = pickle.load(fd)
        # prepare the output name
        tmpOutPath = os.path.join(remapOutDir, "{:s}-{:s}".format(id2SpDict[A], id2SpDict[B]))
        remap_queue.put((fpath, tmpOutPath))

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        remap_queue.put(None)
    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(inPaths))

    # call the method inside workers
    runningJobs = [mp.Process(target=consume_remap_pairwise_relations, args=(remap_queue, results_queue, new2OldHdrAllSp)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    while True:
        try:
            rawPair, remapPair = results_queue.get(False, 0.01)
            #debug = True
            if debug:
              sys.stdout.write('Remapping done for:\t{:s} -> {:s}\n'.format(rawPair, remapPair))
        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()



#### Other functions ####

def remap_pairwise_relations(inTbl: str, outTbl: str, old2NewHdrDictA: Dict[str, str], old2NewHdrDictB: Dict[str, str], debug=False) -> None:
    """Read a table with pairwise relations and add the original FASTA header."""
    if debug:
        print("\nremap_pairwise_relations (Cython) :: START")
        print("Input table: %s"%inTbl)
        print("Output table: %s"%outTbl)
        print("Headers to remap for species A:\t%d"%len(old2NewHdrDictA))
        print("Headers to remap for species B:\t%d"%len(old2NewHdrDictB))
    if not os.path.isfile(inTbl):
        sys.stderr.write('\nThe file %s was not found,\nplease provide a valid input path.\n'%inTbl)
        sys.exit(-2)

    # sample table line
    #OrtoId	Score	OrtoA	OrtoB
    #14\t620\t1.49 1.0\t3.1653 1.0 3.373 0.385

    # define the variables
    clstrId: str = ""
    clstrSc: str = ""
    clstrLx: str = "" # part from species A
    clstrRx: str = "" # part from species B
    newClstr: str = "" # remapped string
    # list to be used during the split
    tmpListLx: List[str] = []
    tmpListRx: List[str] = []

    # other variables
    cdef int rdCnt
    rdCnt = 0
    cdef int wrtCnt
    wrtCnt = 0
    # define file names and file descriptor pointer in C
    filename_byte_string = inTbl.encode("UTF-8")
    cdef char* inTbl_c = filename_byte_string
    #file pointer
    cdef FILE* cfile
    # varibales for files and lines
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    #open the pairwise ortholog table
    cfile = fopen(inTbl_c, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, "No such file or directory: '%s'" % inTbl_c)

    # open the output file
    ofd = open(outTbl, "w")
    # read the file, remap the ids and write in the new output table
    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break
        rdCnt += 1

        # if the last letter is a 'B' then it is the cluster headers
        if line.decode()[-2] == "B":
          ofd.write(line.decode())
          wrtCnt += 1
          continue
        # split the cluster string
        flds = line.split(b'\t', 3)
        clstrId: str = flds[0].decode()
        clstrSc: str = flds[1].decode()
        clstrLx: str = flds[2].decode()
        clstrRx: str = flds[3].decode()

        # map elements of the left part of the cluster
        # example: 3.1653 1.0 3.373 0.385 -> gene1 1.0 gene2 0.385
        tmpListLx = clstrLx.split(" ")
        for i, val in enumerate(tmpListLx):
          if i % 2 == 0: # then we map the FASTA header
            tmpListLx[i] = old2NewHdrDictA[val]

        # map elements of the right part of the cluster
        tmpListRx = clstrRx.split(" ")
        for i, val in enumerate(tmpListRx):
          if i % 2 == 0: # then we map the FASTA header
            tmpListRx[i] = old2NewHdrDictB[val]

        ofd.write("{:s}\t{:s}\t{:s}\t{:s}".format(clstrId, clstrSc, " ".join(tmpListLx), " ".join(tmpListRx)))
        wrtCnt += 1

    #close input file
    fclose(cfile)
