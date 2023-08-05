from libc.stdio cimport *
from libc.stdlib cimport atoi
from libc.stdlib cimport atof
import sys
import os
import pickle
import multiprocessing as mp
from typing import Dict, List, Tuple
from itertools import combinations
import numpy as np
from scipy.sparse import dok_matrix, csr_matrix, save_npz, load_npz, triu
import time



__module_name__ = 'Graph'
__source__ = 'graph_c.pyx'
__author__ = 'Salvatore Cosentino'
__license__ = 'GPLv3'
__version__ = '0.4'
__maintainer__ = 'Cosentino Salvatore'
__email__ = 'salvo981@gmail.com'



def info() -> None:
    """Functions to create a graph from ortholog tables."""
    print('MODULE NAME:\t%s'%__module_name__)
    print('SOURCE FILE NAME:\t%s'%__source__)
    print('MODULE VERSION:\t%s'%__version__)
    print('LICENSE:\t%s'%__license__)
    print('AUTHOR:\t%s'%__author__)
    print('EMAIL:\t%s'%__email__)



cdef extern from "stdio.h":
    #FILE * fopen ( const char * filename, const char * mode )
    FILE *fopen(const char *, const char *)
    #int fclose ( FILE * stream )
    int fclose(FILE *)
    #ssize_t getline(char **lineptr, size_t *n, FILE *stream);
    ssize_t getline(char **, size_t *, FILE *)



""" Worker functions (1 cpu) """
def consume_merge_inparalog_matrixes(jobs_queue, results_queue, combMtx: csr_matrix, mtxDir: str, outDir: str, removeMerged: bool):
    """Merge inparalog matrixes."""
    while True:
        current_sp  = jobs_queue.get(True, 1)
        if current_sp is None:
            break
        # merge the matrixes
        mtxPath = merge_inparalog_matrixes(current_sp, combMtx=combMtx, inDir=mtxDir, outDir=outDir, removeMerged=removeMerged, debug=False)
        # add the path to the output
        if mtxPath is None:
          results_queue.put((current_sp, False))
        else:
          results_queue.put((current_sp, True))



def consume_write_per_species_mcl_graph(jobs_queue, results_queue, offSetDict: Dict[int, int], mtxDir: str, outDir: str, combMtxPath: str) -> None:
    """Generate MCL graph for the input species."""
    while True:
        current_sp  = jobs_queue.get(True, 1)
        if current_sp is None:
            break
        mclSpGraphPath = write_per_species_mcl_graph(current_sp, offSetDict, mtxDir, outDir, combMtxPath, debug=False)
        # add the path to the output
        results_queue.put((current_sp, mclSpGraphPath))



def consume_create_matrix_from_orthotbl(jobs_queue, results_queue, inDir: str, outDir:str, storeDgraph: bool=False):
    """Parse ortholog table and fill matrixes."""
    aSize: int = -1
    bSize: int = -1
    while True:
        jobTpl  = jobs_queue.get(True, 1)
        if jobTpl is None:
            break
        current_pair, aSize, bSize = jobTpl
        #print(current_pair, aSize, bSize)
        tblDir = os.path.join(inDir, "{:s}".format(current_pair))
        inTbl = os.path.join(tblDir, "table.{:s}".format(current_pair))
        outTpl = create_matrix_from_orthotbl(inTbl=inTbl, outDir=outDir, aSize=aSize, bSize=bSize, storeDgraph=storeDgraph, debug=False)
        # add the matrixes names
        results_queue.put(outTpl)



""" Job processing Functions """
def create_matrix_from_orthotbl_parallel(pairsList: List[str], runDir: str=os.getcwd(), orthoDbDir: str=os.getcwd(), outDir: str=os.getcwd(), threads: int=4, debug: bool=False):
    """Compute paralog matrixes in parallel."""
    if debug:
        print("\ncreate_matrix_from_orthotbl_parallel :: START")
        print("Pairs to be processed:\t{:d}".format(len(pairsList)))
        print("Run directory: {:s}".format(runDir))
        print("Directory with ortholog tables: {:s}".format(orthoDbDir))
        print("Output directory: {:s}".format(outDir))
        print("Threads:{:d}".format(threads))
    # load the size of each input proteomes
    pcklPath = os.path.join(runDir, 'protein_counts.pckl')
    if not os.path.isfile(pcklPath):
      sys.stderr.write("\nERROR: the pickle file with the proteome sizes\n{:s}\nis missing in the run directory\n".format(pcklPath))
      sys.exit(-2)
    else:
      with open(pcklPath, "rb") as ifd:
        spSizes = pickle.load(ifd)

    # Start timer
    sys.stdout.write('\nCreating orthology matrixes...\n')
    timer_start = time.perf_counter()

    #sys.exit("DEBUG :: create_matrix_from_orthotbl_parallel :: after loading proteome sizes.")
    # create the queue and start adding
    ortho2mtx_queue = mp.Queue(maxsize=len(pairsList) + threads)

    # fill the queue with the pairs
    for pair in pairsList:
        sys.stdout.flush()
        spA, spB = pair.split("-", 1)
        ortho2mtx_queue.put((pair, spSizes[spA], spSizes[spB]))

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        ortho2mtx_queue.put(None)
    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(pairsList))

    # call the method inside workers
    runningJobs = [mp.Process(target=consume_create_matrix_from_orthotbl, args=(ortho2mtx_queue, results_queue, orthoDbDir, outDir, False)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    while True:
        try:
            resTpl = results_queue.get(False, 0.01)
            resPair: str = resTpl[0].rsplit(".", 1)[0]
            if debug:
              sys.stdout.write("Matrixes created for pair {:s}\t{:s}\n".format(resPair, str(resTpl)))
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

    sys.stdout.write('Ortholog matrixes creation elapsed time (seconds):\t{:s}\n'.format(str(round(time.perf_counter() - timer_start, 3))))



def merge_inparalog_matrixes_parallel(spArray, combMtxPath: str, inDir: str=os.getcwd(), outDir: str=os.getcwd(), threads: int=4,  removeMerged: bool=False, debug: bool=False):
    """MCL graph for a species from matrixes in parallel."""
    if debug:
        print("\nmerge_inparalog_matrixes_parallel :: START")
        print("Species for which the graph will created:\t{:d}".format(len(spArray)))
        print("Path to the combination matrix:\t{:s}".format(combMtxPath))
        print("Input directory: {:s}".format(inDir))
        print("Output directory: {:s}".format(outDir))
        print("Threads:{:d}".format(threads))
        print("Remove merged matrixes:\t{:s}".format(str(removeMerged)))

    # check that the matrix with combinations exists
    if not os.path.isfile(combMtxPath):
      sys.stderr.write("\nERROR: the file with the combination matrix\n{:s}\nwas not found!\n".format(combMtxPath))
      sys.exit(-2)
    # load the matrix
    combMtx = load_npz(combMtxPath) # this an upper triangular matrix

    # create the queue and start adding the species
    sp_queue = mp.Queue(maxsize=len(spArray) + threads)

    # fill the queue with the pairs
    for tmpSp in spArray:
        sys.stdout.flush()
        sp_queue.put(tmpSp)

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        sp_queue.put(None)
    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(spArray))

    #sys.exit("DEBUG :: merge_inparalog_matrixes_parallel :: before starting jobs...")

    # call the method inside workers
    runningJobs = [mp.Process(target=consume_merge_inparalog_matrixes, args=(sp_queue, results_queue, combMtx, inDir, outDir, removeMerged)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    # Dictionary with False if the merging failed
    resDict: Dict[int, bool] = {}

    while True:
        try:
            processedSp, mergeOk = results_queue.get(False, 0.01)
            if not mergeOk:
              sys.stdout.write("Merging in-paralogs for species {:d} failed.\n".format(processedSp))
              resDict[processedSp] = False
            else:
              resDict[processedSp] = True
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
    # return the sorted dictionary with the paths
    return dict(sorted(resDict.items()))



def write_per_species_mcl_graph_parallel(spArray, runDir: str=os.getcwd(), mtxDir: str=os.getcwd(), outDir: str=os.getcwd(), threads: int=4, debug: bool=False) -> Dict[int, str]:
    """MCL graph for a species from matrixes in parallel."""
    if debug:
        print("\nwrite_per_species_mcl_graph_parallel :: START")
        print("Species for which the graph will created:\t{:d}".format(len(spArray)))
        print("Run directory: {:s}".format(runDir))
        print("Directory with Matrixes: {:s}".format(mtxDir))
        print("Output directory: {:s}".format(outDir))
        print("Threads:{:d}".format(threads))

    # load the size of each input proteomes
    pcklPath = os.path.join(runDir, "protein_counts.pckl")
    # compute offsets
    offSetDict = compute_offsets(pcklPath)[0]
    # path to the combination matrix
    combMtxPath = os.path.join(runDir, "combination_mtx.npz")
    # create the queue and start adding the species
    sp_queue = mp.Queue(maxsize=len(spArray) + threads)

    # fill the queue with the pairs
    for tmpSp in spArray:
        sys.stdout.flush()
        sp_queue.put(tmpSp)

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        sp_queue.put(None)
    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(spArray))
    #sys.exit("DEBUG :: write_per_species_mcl_graph_parallel :: before starting jobs...")

    # call the method inside workers
    runningJobs = [mp.Process(target=consume_write_per_species_mcl_graph, args=(sp_queue, results_queue, offSetDict, mtxDir, outDir, combMtxPath)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    # output dictionary which associate
    # a species ID to a the path of MCL subgraph created for it
    mclSpGraphDict: Dict[int, str] = {}

    while True:
        try:
            processedSp, spGraphPath = results_queue.get(False, 0.01)
            if debug:
              sys.stdout.write("MCL graph for species {:d} created\n{:s}\n".format(processedSp, spGraphPath))
            # add the path to the dictionary
            mclSpGraphDict[processedSp] = spGraphPath
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
    # return the sorted dictionary with the paths
    return dict(sorted(mclSpGraphDict.items()))



""" Other functions """
def compute_offsets(protCntPckl: str, debug: bool=False):
    """Compute index offsets for each species from pickle with sizes"""
    if debug:
        print("\ncompute_offsets :: START")
        print("Pickle with proteome sizes: {:s}".format(protCntPckl))
    # check that the file the protein counts exists
    if not os.path.isfile(protCntPckl):
      sys.stderr.write("\nERROR: the file with the protein count\n{:s}\nwas not found!\n".format(protCntPckl))
      sys.exit(-2)
    # load the protein count
    with open(protCntPckl, "rb") as ifd:
      protCnt = pickle.load(ifd)
    # fill the dictionary with offsets
    offSetDict: Dict[int, int] = {}
    sizeDict: Dict[int, int] = {}
    accumulator: int = 0
    prevCnt: int = 0
    loopCnt: int = 0
    for spId, pCnt in protCnt.items():
      sizeDict[int(spId)] = pCnt
      if loopCnt == 0:
        offSetDict[int(spId)] = 0
      else:
        accumulator += prevCnt
        offSetDict[int(spId)] = accumulator
      prevCnt = pCnt
      loopCnt += 1
    # print some debug
    if debug:
      for spId, offset in offSetDict.items():
        print("sp={:d}\tproteins={:d}\toffset={:d}".format(spId, protCnt[str(spId)], offset))
    # free some memory
    del protCnt, prevCnt, accumulator, loopCnt
    # return the dictionary
    return (offSetDict, sizeDict)



def create_graph_from_pckls(pcklApath: str, pcklBpath: str, outDir: str, debug: bool=False) -> str:
    import networkx as nx
    """Load ortholog relationships from pickle of tuple and generate a graph."""
    if debug:
        print("\ncreate_graph_from_pckls :: START")
        print("Pickle for species A:\t{:s}".format(pcklApath))
        print("Pickle for species B:\t{:s}".format(pcklBpath))
        print("Output directory:\t{:s}".format(outDir))
    if not os.path.isfile(pcklApath):
        sys.stderr.write("\nERROR: the pickle was not found.")
        sys.exit(-2)
    if not os.path.isfile(pcklBpath):
        sys.stderr.write("\nERROR: the pickle was not found.")
        sys.exit(-2)

    # generate a directed graph from the connections stored in the pickles
    gA = nx.DiGraph()
    gAinp = nx.DiGraph() # will only contain inparalog relations
    gAmain = nx.DiGraph() # only relations interspecies relationships (no_inparalogs)
    # load the pickle for A
    with open(pcklApath, "rb") as pcklA:
      for subGraph in pickle.load(pcklA):
        for source, connections in subGraph.items():
          for c in connections:
            #print(source, c[0], c[1])
            #gA.add_edge(int(source.split(".", 1)[-1]), int(c[0].split(".", 1)[-1]),weight=c[1])
            gA.add_edge(source, c[0],weight=c[1])

            # add inparalog relations if possible
            if int(source.split(".", 1)[0]) == int(c[0].split(".", 1)[0]): # then it is an inparalog
              #print(int(source.split(".", 1)[0]), int(c[0].split(".", 1)[0]))
              #break
              #gAinp.add_edge(int(source.split(".", 1)[-1]), int(c[0].split(".", 1)[-1]),weight=c[1])
              gAinp.add_edge(source, c[0],weight=c[1])
            else:
              gAmain.add_edge(source, c[0],weight=c[1])

    # edges to text
    tmpEdgesFilePath = os.path.join(outDir, "test.weighted_edges_A.txt")
    nx.write_weighted_edgelist(gA, tmpEdgesFilePath)
    tmpEdgesFilePath = os.path.join(outDir, "test.weighted_edges_A_inparalogs.txt")
    nx.write_weighted_edgelist(gAinp, tmpEdgesFilePath)
    tmpEdgesFilePath = os.path.join(outDir, "test.weighted_edges_A_main.txt")
    nx.write_weighted_edgelist(gAmain, tmpEdgesFilePath)

    # to pickle
    tmpEdgesFilePath = os.path.join(outDir, "test.graph_A.pckl")
    nx.write_gpickle(gA, tmpEdgesFilePath)
    tmpEdgesFilePath = os.path.join(outDir, "test.graph_A_inparalogs.pckl")
    nx.write_gpickle(gAinp, tmpEdgesFilePath)
    tmpEdgesFilePath = os.path.join(outDir, "test.weighted_edges_A_main.pckl")
    nx.write_gpickle(gAmain, tmpEdgesFilePath)

    gB = nx.DiGraph()
    gBinp = nx.DiGraph() # inparalog relations only
    # load the pickle for B
    with open(pcklBpath, "rb") as pcklB:
      for subGraph in pickle.load(pcklB):
        for source, connections in subGraph.items():
          for c in connections:
            #print(source, c[0], c[1])
            gB.add_edge(int(source.split(".", 1)[-1]), int(c[0].split(".", 1)[-1]),weight=c[1])
            #gB.add_edge(source, c[0],weight=c[1])

            # add inparalog relations if possible
            if int(source.split(".", 1)[0]) == int(c[0].split(".", 1)[0]): # then it is an inparalog
              gBinp.add_edge(int(source.split(".", 1)[-1]), int(c[0].split(".", 1)[-1]),weight=c[1])

    # edges to text
    tmpEdgesFilePath = os.path.join(outDir, "test.weighted_edges_B.txt")
    nx.write_weighted_edgelist(gB, tmpEdgesFilePath)
    tmpEdgesFilePath = os.path.join(outDir, "test.weighted_edges_B_inparalogs.txt")
    nx.write_weighted_edgelist(gBinp, tmpEdgesFilePath)
    tmpEdgesFilePath = os.path.join(outDir, "test.graph_B_inparalogs.pckl")
    nx.write_gpickle(gBinp, tmpEdgesFilePath)

    # to pickle
    tmpEdgesFilePath = os.path.join(outDir, "test.graph_B.pckl")
    nx.write_gpickle(gB, tmpEdgesFilePath)



def create_matrix_from_orthotbl(inTbl: str, outDir: str, aSize: int, bSize: int, storeDgraph: bool=False, debug: bool=False) -> Tuple[str, str, str]:
    """Load ortholog relationships from pickle of tuple to a matrix."""
    if debug:
        print("\ncreate_matrix_from_orthotbl :: START")
        print("Table path: {:s}".format(inTbl))
        print("Output directory:\t{:s}".format(outDir))
        print("Size A:\t{:d}".format(aSize))
        print("Size B:\t{:d}".format(bSize))
        print("Store a directed graph for orthologs:\t{:s}".format(str(storeDgraph)))

    if not os.path.isfile(inTbl):
        sys.stderr.write("\nERROR: the ortholog table\n{:s}\nwas not found.".format(inTbl))
        sys.exit(-2)

    if storeDgraph:
      import networkx as nx
      G = nx.DiGraph()

    # extract the species names
    pairName = os.path.basename(inTbl).split(".", 1)[-1]
    spA, spB = pairName.split("-", 1)
    spA = int(spA)
    spB = int(spB)

    # define temporary variables
    clstrLx: str = "" # part from species A
    clstrRx: str = "" # part from species B
    lxDict: [str, float]
    lxDictInp: [str, float]
    lxDictMain: [str, float]
    rxDict: [str, float]
    rxDictInp: [str, float]
    rxDictMain: [str, float]

    # will store parts (left or right) of each clusters
    tmpList: List[str]

    # other variables
    cdef int rdCnt
    rdCnt = 0
    #cdef float tmpSc
    #tmpSc = 0.
    tmpSc: float = 0.
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

    # example of line to be parsed
    # 334	64	1.1110 0.051 1.943 1.0	2.16 1.0 2.653 0.18

    # output dictionary (a digest for each file name)
    relDict: Dict[int, Dict[str, List[Tuple[str, str, float]]]]
    relList: List[Dict[int, Dict[str, List[Tuple[str, str, float]]]]] = []
    relListLx: List[Dict[str, List[Tuple[str, str, float]]]] = []
    relListRx: List[Dict[str, List[Tuple[str, str, float]]]] = []

    # use to check if a given protein appears multiple times in the input table
    repeatTrapLx: Doct[str, int] = {}
    repeatTrapRx: Doct[str, int] = {}

    # use to check if a given protein appears multiple times in the input table
    # instantiate the matrixes
    AB = dok_matrix((aSize, bSize), dtype=np.float32)
    Ai = dok_matrix((aSize, aSize), dtype=np.float32)
    Bi = dok_matrix((bSize, bSize), dtype=np.float32)
    inParaRel: List[ Tuple[int, int] ] = []

    # counters
    orthoWrt: int = 0
    inparaWrtA: int = 0
    inparaWrtB: int = 0

    while True:
        read = getline(&line, &l, cfile)
        if read == -1:
            break

        # if the first letter is a 'O' then it is the cluster headers
        if line.decode()[0] == "O":
          continue
        rdCnt += 1
        relDict = {1:{}, 2:{}}
        # split the cluster string
        flds = line.rstrip(b"\n").rsplit(b"\t", 2)
        #print(flds)
        clstrLx: str = flds[1].decode()
        clstrRx: str = flds[2].decode()
        # temporary dictionaries
        lxDict = {}
        lxDictInp = {}
        lxDictMain = {}
        rxDict = {}
        rxDictInp = {}
        rxDictMain = {}

        # extract orthologs from the left part of the cluster
        # example: 3.1653 1.0 3.373 0.385 -> gene1 1.0 gene2 0.385
        tmpList = clstrLx.split(" ")
        for i, ortho in enumerate(tmpList):
          if i % 2 == 0: # then we add the element to the dictionary
            tmpSc = round(float(tmpList[i+1]), 3)
            tmpIdx = int(ortho.split(".", 1)[1]) - 1
            if not tmpIdx in repeatTrapLx:
              repeatTrapLx[tmpIdx] = 1
            else:
              #sys.exit("\nERROR: the protein {:s} from species A was found in multiple ortholog relations...".format(tmpIdx))
              repeatTrapLx[tmpIdx] += 1
              continue
            lxDict[tmpIdx] = tmpSc
            if tmpSc < 1:
              lxDictInp[tmpIdx] = tmpSc
            else:
              lxDictMain[tmpIdx] = tmpSc

        # extract the right part
        tmpList = clstrRx.split(" ")
        #print("rx_tmp_list:", tmpList)
        for i, ortho in enumerate(tmpList):
          if i % 2 == 0: # then we add the element to the dictionary
            tmpSc = round(float(tmpList[i+1]), 3)
            tmpIdx = int(ortho.split(".", 1)[1]) - 1
            if not tmpIdx in repeatTrapRx:
              repeatTrapRx[tmpIdx] = 1
            else:
              #sys.exit("\nERROR: the protein {:s} from species A was found in multiple ortholog relations...".format(tmpIdx))
              repeatTrapRx[tmpIdx] += 1
              continue
            rxDict[tmpIdx] = tmpSc
            if tmpSc < 1:
              if not ortho in rxDictInp: # this check should be removed later!
                #rxDictInp[ortho] = tmpSc
                rxDictInp[tmpIdx] = tmpSc
              else:
                print("ERROR: inparalog {:s} was already in the dictionary!".format(ortho))
                sys.exit(-5)
            else:
              #rxDictMain[ortho] = tmpSc
              rxDictMain[tmpIdx] = tmpSc
        lxOrthoList = list(lxDict.keys())
        rxOrthoList = list(rxDict.keys())

        #if debug:
        #  print("\nCompute scores and add orthologs to matrix for current cluster...")
        #  print(clstrLx, clstrRx)
        # extract the ortholog scores in a array
        rxSc = np.array(list(rxDict.values()))
        for orthoLx, tmpSc in lxDict.items():
          # compute the weights
          wArr = (rxSc + tmpSc)/2.
          #print("\ncurrent:\t", orthoLx, tmpSc)
          i = orthoLx
          # search for orthologs to store in AB
          for idx, orthoRx in enumerate(rxOrthoList):
            # add the connection (if not between InParalogs)
            j = orthoRx

            ''' AVOID INTER-SPECIES INPARALOGS
            # add the relation if at least one of the 2 is main ortholog
            if not (orthoLx in lxDictInp and orthoRx in rxDictInp):
              tmpW = wArr[idx]
              #print("Candidate ortholog...")
              #print("{:s} -> {:s}".format(orthoLx, orthoRx))
              #print("{:d} -> {:d}".format(i, j))
              #relDict[1][orthoLx].append((orthoRx, round(w[i], 3)))
              # ADD THIS PART
              if not AB[i, j]:
                AB[i, j] = round(tmpW, 3)
                # add edge to the graph if required
            #'''

            #''' Allow interspecies in-paralogs
            # add the relation (includes also relations amongst inparalogs)
            # from different species
            tmpW = wArr[idx]
            #print("Candidate ortholog...")
            #print("{:s} -> {:s}".format(orthoLx, orthoRx))
            #print("{:d} -> {:d}".format(i, j))
            #relDict[1][orthoLx].append((orthoRx, round(w[i], 3)))
            # ADD THIS PART
            if not AB[i, j]:
              AB[i, j] = round(tmpW, 3)
            #'''

        # variable used to store the weight for inparalogs
        tmpInpaW: float = 0.

        # search for in-paralogs to store in Ai (for the left part)
        # compute all the possible combinations
        #print("\nadd inparalogs relations for {:d} paralogs in species {:d}...".format(len(lxOrthoList), spA))
        inParaRel = list(combinations(sorted(lxOrthoList), r=2))
        #print(inParaRel)

        for tplIdx in inParaRel:
          i, j = tplIdx
          tmpInpaW = round( (lxDict[i] + lxDict[j]) / 2. , 3)
          # make sure that the matrix is upper triangular
          if i > j: # below the diagonal
            #print("i > j", i, j)
            # swap the indexes
            tmpJ = i
            tmpI = j
            #print("swapped(i, j)", tmpI, tmpJ)
            if not Ai[tmpI, tmpJ]:
              print(str(Ai[tmpI, tmpJ]))
              Ai[tmpI, tmpJ] = tmpInpaW
              inparaWrtA += 1
              continue
          elif i == j:
            diagCntA += 1
            print("same!", i, j)
            print("This should not happen!")
            sys.exit("DEBUG :: filling InParalog matrix for A")
          else:
            if not Ai[i, j]:
              Ai[i, j] = tmpInpaW
              inparaWrtA += 1

        # search for in-paralogs to store in Ai (for the left part)
        # compute all the possible combinations
        #print("\nadd inparalogs relations for {:d} paralogs in species {:d}...".format(len(rxOrthoList), spB))
        inParaRel = list(combinations(sorted(rxOrthoList), r=2))
        #print(inParaRel)
        for tplIdx in inParaRel:
          i, j = tplIdx
          tmpInpaW = round( (rxDict[i] + rxDict[j]) / 2. , 3)
          # make sure that the matrix is upper triangular
          if i > j: # below the diagonal
            #print("i > j", i, j)
            # swap the indexes
            tmpJ = i
            tmpI = j
            #print("swapped(i, j)", tmpI, tmpJ)
            if not Bi[tmpI, tmpJ]:
              print(str(Bi[tmpI, tmpJ]))
              Bi[tmpI, tmpJ] = tmpInpaW
              inparaWrtB += 1
              continue
          elif i == j:
            diagCntB += 1
            print("same!", i, j)
            print("This should not happen!")
            sys.exit("DEBUG :: filling InParalog matrix for A")
          else:
            if not Bi[i, j]:
              Bi[i, j] = tmpInpaW
              inparaWrtB += 1
        #print("Cluster processing done!\n")
        #sys.exit("DEBUG :: create_matrix_from_orthotbl")

    # print the current ortholog matrix
    #print(AB.todense())
    # store the matrix with orthologs
    # convert to a CSR matrix
    AB = AB.tocsr()
    AB_name = "{:s}.npz".format(pairName)
    tmpMatxFilePath = os.path.join(outDir, AB_name)
    save_npz(tmpMatxFilePath, AB, compressed=False)
    # convert to a CSR matrix and save
    Ai = Ai.tocsr()
    Ai_name = "{:s}_i{:d}.npz".format(pairName, spA)
    tmpMatxFilePath = os.path.join(outDir, Ai_name)
    save_npz(tmpMatxFilePath, Ai, compressed=False)
    # convert to a CSR matrix and save
    Bi = Bi.tocsr()
    Bi_name = "{:s}_i{:d}.npz".format(pairName, spB)
    tmpMatxFilePath = os.path.join(outDir, Bi_name)
    save_npz(tmpMatxFilePath, Bi, compressed=False)

    if debug:
      print("\nOrtholog relations in matrix for {:s}:\t{:d}".format(pairName, AB.nnz))
      print("Inparalog relations in matrix for species {:d}:\t{:d}".format(spA, Ai.nnz))
      print("Inparalog relations in matrix for species {:d}:\t{:d}".format(spB, Bi.nnz))
    # return names of created matrixes
    return(AB_name, Ai_name, Bi_name)



'''
def dump_inpara_adjacency(mtxPath: str, sp: int, outDir: str, dumpGraph: bool = False, debug: bool=False) -> str:
    """Load inparalogs from matrix and store a dictionary with adjacency paths."""
    if not os.path.isfile(mtxPath):
        sys.stderr.write("\nERROR: the matrix file\n{:s}\n was not found.".format(mtxPath))
        sys.exit(-2)
    # define the input species
    bname: str = os.path.basename(mtxPath).rsplit(".", 1)[0] # remove extension and directory name
    currentSp: str = str(sp)

    if debug:
        print("\ndump_inpara_adjacency :: START")
        print("Input matrix:\t{:s}".format(mtxPath))
       # print("Proteome pair:\t{:s}".format(pair))
        print("Current proteome:\t{:s}".format(currentSp))
        print("Output directory:\t{:s}".format(outDir))
        print("Output graph file:\t{:s}".format(str(dumpGraph)))

    #sys.exit("DEBUG :: dump_inpara_adjacency")

    # load the matrix file
    M = load_npz(mtxPath)
    # add the transpose
    M = M + M.transpose()
    # create the directed graph
    G = nx.from_scipy_sparse_matrix(M, create_using=nx.DiGraph)
    # extract dict with adjacency
    edjDict = {x[0]:x[1] for x in G.adjacency() if len(x[1])>0}
    # dump it in a pickle
    pcklPath = os.path.join(outDir, "{:s}_adj.pckl".format(bname))
    with open(pcklPath, "wb") as ofd:
      pickle.dump(edjDict, ofd)
    if debug:
      print("In-paralog nodes with degree > 0 for proteome {:s}:\t{:d}".format(currentSp, len(edjDict)))
    # dump the graph if requested
    if dumpGraph:
      # view using Cythoscape
      nx.write_graphml(G, os.path.join(outDir, "{:s}.graphml".format(bname)))
    return pcklPath



def dump_ortho_adjacency(mtxPath: str, outDir: str, dumpGraph: bool = False, debug: bool=False) -> str:
    """Load orthologs from matrix and store a dictionary with adjacency paths."""
    if not os.path.isfile(mtxPath):
        sys.stderr.write("\nERROR: the matrix file\n{:s}\n was not found.".format(mtxPath))
        sys.exit(-2)
    # define the input species
    bname: str = os.path.basename(mtxPath).rsplit(".", 1)[0] # remove extension and directory name
    sp1, sp2 = bname.split("-", 1)
    if debug:
        print("\ndump_ortho_adjacency :: START")
        print("Input matrix:\t{:s}".format(mtxPath))
        print("Proteome pair:\t{:s}".format(bname))
        print("Output directory:\t{:s}".format(outDir))
        print("Output graph file:\t{:s}".format(str(dumpGraph)))

    # create the Graph
    G = nx.DiGraph()
    # load the matrix file
    M = load_npz(mtxPath)
    # iterate through the matrix and fill the graph
    nnzR, nnzC = M.nonzero()
    for i, row in enumerate(nnzR):
      col = nnzC[i]
      orthoW = M[row, col]
      # add the node to the graph
      #G.add_edge(row, col, weight=orthoW)
      #G.add_edge(col, row, weight=orthoW)
      # to avoid the possibility of self-loop
      # use string IDs instead
      rowStr = "{:s}.{:d}".format(sp1, row)
      colStr = "{:s}.{:d}".format(sp2, col)
      G.add_edge(rowStr, colStr, weight=orthoW)
      G.add_edge(colStr, rowStr, weight=orthoW)
      if col == row:
        print("WARNING: row and column are same ({:d}, {:d}). This could be a self loop.".format(row, col))

    # extract dict with adjacency
    edjDict = {x[0]:x[1] for x in G.adjacency() if len(x[1])>0}
    # dump it in a pickle
    pcklPath = os.path.join(outDir, "{:s}_adj.pckl".format(bname))
    with open(pcklPath, "wb") as ofd:
      pickle.dump(edjDict, ofd)
    if debug:
      print("Orthology nodes with degree > 0 for pair {:s}:\t{:d}".format(bname, len(edjDict)))
    # dump the graph if requested
    if dumpGraph:
      # view using Cythoscape
      nx.write_graphml(G, os.path.join(outDir, "{:s}.graphml".format(bname)))

    return pcklPath
'''



def merge_inparalog_matrixes(sp: int, combMtx: csr_matrix, inDir: str, outDir: str, removeMerged: bool=True, debug: bool=False):
    """Merge all inparalog matrixes for a given species into a single one."""
    if debug:
        print("\nmerge_inparalog_matrixes :: START")
        print("Species:\t{:d}".format(sp))
        print("Shape of matrix with combinations:\t{:s}".format(str(combMtx.shape)))
        print("Input directory:\t{:s}".format(inDir))
        print("Output directory:\t{:s}".format(outDir))
        #print("Path to the matrix with species combinations:{:s}".format(combMtxPath))
    # extract the column and row corresponding to the input species
    spMtxIdx = sp - 1 # adjust the species idx (matrixes idxs start from 0)
    rowSpY = combMtx.getrow(spMtxIdx).toarray().nonzero()[1] # only keep the column idx (Y), the row is spMtxIdx
    colSpX = combMtx.getcol(spMtxIdx).toarray().nonzero()[0] # only keep the row idx (X), the column is spMtxIdx
    # save the combinations in a dictionary
    combDict: Dict[Tuple[int, int], None] = {}
    # extract from row non-zero indexes
    for cIdx in colSpX:
      combDict[(cIdx, spMtxIdx)] = None
    # extract from row non-zero indexes
    for rIdx in rowSpY:
      combDict[(spMtxIdx, rIdx)] = None

    # matrix with count for ortholog appearance
    mtxShape = (0, 0)
    accMtx = None
    masterM = None
    if debug:
      print("Combinations found species {:d}:".format(sp))
    for i, tpl in enumerate(combDict):
      sp1, sp2 = tpl
      mPath = os.path.join(inDir, "{:d}-{:d}_i{:d}.npz".format(sp1+1, sp2+1, sp))
      if debug:
        print("\n", str(tpl))
        print("sp1 =", sp1, "sp2 =", sp2, "sp =", sp)
        print("Adding values from {:s} to the master inparalog matrix...".format(os.path.basename(mPath)))
      if not os.path.isfile(mPath):
        sys.stderr.write("\nERROR: the matrix file\n{:s}\nwas not found!\n".format(mPath))
        sys.exit(-2)
      # load the inparalog matrix
      M = load_npz(mPath)
      # initialize the count matrix if required
      if accMtx is None:
        mtxShape = M.shape
        if mtxShape[0] != mtxShape[1]:
          sys.stderr.write("\nERROR: the inparalog matrix must be a n x n matrix where n is the size number of proteins in the proteome for species {:d}!\n".format(sp))
          sys.exit(-5)
        # initilize the matrix as the ceiling of that with inparalogs
        accMtx = csr_matrix(M.ceil(), dtype=np.int8)
        # create an array of zeros
        # create the sparse matrix for the appearence counts
        # the ceiling of each value will be taken and stored as int8 type
        # and then converted to an upper triangular matrix
        accMtx = triu(csr_matrix(M.ceil(), dtype=np.int8), k=0)
        # set the master matrix as the one the first one loaded (M)
        masterM = M.copy()
        if debug:
          print("\nFirst initialization...")
          print("masterM info:")
          print(type(masterM))
          print(masterM.shape, masterM.nnz)
          print("M info:")
          print(type(M))
          print(M.shape, M.nnz)
          print("accMtx info:")
          print(type(accMtx))
          print(accMtx.shape, accMtx.nnz, "\n")
        if removeMerged:
          os.remove(mPath)
        continue
      # update the accumulator and sum the values in matrixes
      else:
        if debug:
          print("\nMatrix merging step...")
          print("M info:")
          print(type(M))
          print(M.shape, M.nnz)
          print("accMtx info:")
          print(type(accMtx))
          print(accMtx.shape, accMtx.nnz)
          print("masterM info:")
          print(type(masterM))
          print(masterM.shape, masterM.nnz, "\n")
        # sum the inparalog scores
        masterM = masterM + M
        # increment the accumulator
        accMtx = accMtx + triu(csr_matrix(M.ceil(), dtype=np.int8), k=0)
      # remove the merged matrix if required
      if removeMerged:
        os.remove(mPath)

    ##### NOTE #####
    # Because division by 0 would give a NaN which need to be stored in memory
    # better to iterate thrhough the non-zero indexes and perform the divisions
    ################

    nnzR, nnzC = masterM.nonzero()
    for i, row in enumerate(nnzR):
      # the use row and column nnzC[i] to access the values
      col = nnzC[i]
      currentVal = masterM[row, col]
      #print(row, col, currentVal, accMtx[row, col])
      # this should never happen
      if currentVal == 0:
        sys.exit("No value can be 0, make sure that the accumulator matrix and inparalog marix refer to the same species.")
      masterM[row, col] = round(currentVal / accMtx[row, col], 3)

    if debug:
      print("masterM info after all merging:")
      print(type(masterM))
      print(masterM.shape)
      print(masterM.nnz)
    # make sure there are non NaN in the master matrix
    # store the matrix as a csr
    outMtxPath = os.path.join(outDir, "master_i{:d}.npz".format(sp))
    save_npz(outMtxPath, masterM, compressed=False)
    # return the output path
    return outMtxPath



# NOTE consider generating the connections by iterating the matrix of inparalogs instead of generating the graph
def write_per_species_mcl_graph(sp: int, offSetDict: Dict[int, int], mtxDir: str, outDir: str, combMtxPath: str, debug: bool=False):
    """Merge all inparalog matrixes for a given species into a single one."""
    if debug:
        print("\nwrite_per_species_mcl_graph :: START")
        print("Species:\t{:d}".format(sp))
        print("Species offsets:\t{:d}".format(len(offSetDict)))
        print("Directory with matrixes:\t{:s}".format(mtxDir))
        print("Output directory:\t{:s}".format(outDir))
        print("Path to the matrix with species combinations:{:s}".format(combMtxPath))
    # check that the matrix with combinations exists
    if not os.path.isfile(combMtxPath):
      sys.stderr.write("\nERROR: the file with the combination matrix\n{:s}\nwas not found!\n".format(combMtxPath))
      sys.exit(-2)

    # load the matrix
    ### NOTE: there could be a problem with species indexes when
    ### considering subset of species (e.g., 1,2,5)
    ### This issue can be handle by proving a list of the species
    ### to be considered in the run and skip those when loading the combinations
    M = load_npz(combMtxPath) # this an upper triangular matrix
    # extract the column and row corresponding to the input species
    spMtxIdx = sp - 1 # adjust the species idx (matrixes idxs start from 0)
    rowSpY = M.getrow(spMtxIdx).toarray().nonzero()[1] # only keep the column idx (Y), the row is spMtxIdx
    colSpX = M.getcol(spMtxIdx).toarray().nonzero()[0] # only keep the row idx (X), the column is spMtxIdx
    # save the combinations in a dictionary
    combDict: Dict[Tuple[int, int], None] = {}
    # extract from row non-zero indexes
    for cIdx in colSpX:
      combDict[(cIdx, spMtxIdx)] = None
    # extract from row non-zero indexes
    for rIdx in rowSpY:
      combDict[(spMtxIdx, rIdx)] = None
    if debug:
      print("Combinations found for species {:d}:".format(sp))
      print(str(combDict))
    # free memory
    del M

    # create dictionary with adjacensies
    masterAdjDict: Dict[int, Dict[int, float]] = {}

    # load adjacency from master inparalog matrix
    mtxPath = os.path.join(mtxDir, "master_i{:d}.npz".format(sp))
    if debug:
      print("Loading in-paralog matrix:\n{:s}".format(mtxPath))
    M = load_npz(mtxPath)
    # add the transpose
    M = M + M.transpose()

    # create an array with the gene ids for the current species
    # as they would be in the MCL graph
    colIdx = np.array(np.arange(M.shape[0]))

    # add offset the indexes
    tmpOffset: int = offSetDict[sp]
    if tmpOffset > 0:
      colIdx = colIdx + tmpOffset

    if debug:
      print("\nIndexes for species {:d} after adding a offset of {:d}".format(sp, tmpOffset))
      print("Elements:\t{:d}".format(len(colIdx)))
      print("Start:\t{:d}".format(colIdx.min()))
      print("End:\t{:d}".format(colIdx.max()))

    # initialize the master dictionary that will contain the graph edjes
    masterAdjDict = {x:{} for x in colIdx}
    del colIdx

    # iterate through the matrix and fill the graph
    nnzR, nnzC = M.nonzero()
    # add the offSets to the non-zero row and columns
    mclRows = nnzR + tmpOffset
    mclCols = nnzC + tmpOffset
    for i, row in enumerate(nnzR):
      # the use row and column nnzC[i] to access the values
      col = nnzC[i]
      # extract the values and fill the dictionary
      currentW = M[row, col]
      mclRow = mclRows[i]
      mclCol = mclCols[i]
      # add the entry in the master dictionary
      masterAdjDict[mclRow][mclCol] = currentW
      if debug:
        print("row: {:d}->{:d}\tcol: {:d}->{:d}\t{:.3f}".format(row, mclRow, col, mclCol, currentW))
        print("{:d} ->\t{:s}\n".format(mclRow, str(masterAdjDict[mclRow])))

    if debug:
      print("### Finished processing the in-paralog matrix {:s} ###".format(os.path.basename(mtxPath)))
      print("In-paralog nodes in connection dictionary:\t{:d}".format(len(masterAdjDict)))

    # Extract the adjacency for orthologs
    # set to true if the the current species is the second in the pair
    transpose: bool = False

    # for each combination in combDict
    for tpl in combDict:
      if debug:
        print("Processing idx pair {:s}, with {:d} being the current species.\n".format(str(tpl), sp))
      sp1, sp2 = tpl
      mtxPath = os.path.join(mtxDir, "{:d}-{:d}.npz".format(sp1+1, sp2+1, sp))
      if not os.path.isfile(mtxPath):
        sys.stderr.write("\nERROR: the ortholog matrix file\n{:s}\nwas not found!\n".format(mtxPath))
        sys.exit(-2)
      # load the ortholog matrix
      M = load_npz(mtxPath)
      # set the transpose flag
      if sp2 + 1 == sp:
        if debug:
          print("INFO: The transpose of {:s} must be used for species {:d}".format(os.path.basename(mtxPath), sp))
        traspose = True
        M = M.transpose()
        colOffset = offSetDict[sp1 + 1]
      else:
        traspose = False
        colOffset = offSetDict[sp2 + 1]

      # set the offsets for row and column indexes
      rowOffset = tmpOffset
      if debug:
        print("Loaded ortholog matrix\n{:s}".format(mtxPath))
        print("Row offset\t{:d}".format(rowOffset))
        print("Column offset\t{:d}\n".format(colOffset))

      # iterate through the matrix and fill the graph
      nnzR, nnzC = M.nonzero()
      # add the offSets to the non-zero row and columns
      mclRows = nnzR + rowOffset
      mclCols = nnzC + colOffset
      # clear the graph and edje dictionary
      #G.clear()
      #edjDict.clear()
      for i, row in enumerate(nnzR):
        # the use row and column nnzC[i] to access the values
        col = nnzC[i]

        currentW = M[row, col]
        mclRow = mclRows[i]
        mclCol = mclCols[i]
        # add the entry in the master dictionary
        masterAdjDict[mclRow][mclCol] = currentW
        if debug:
          print("row: {:d}->{:d}\tcol: {:d}->{:d}\t{:.3f}".format(row, mclRow, col, mclCol, currentW))
          print("{:d} ->\t{:s}\n".format(mclRow, str(masterAdjDict[mclRow])))

      if debug:
        print("### Finished processing the ortholog matrix {:s} ###".format(os.path.basename(mtxPath)))

    # create the graph file
    spGraphPath = os.path.join(outDir, "mcl_graph_{:d}.txt".format(sp))
    # open the output file
    ofd = open(spGraphPath, "wt")
    # write the content of the master dictionary in the graph file
    for source, connections in masterAdjDict.items():
      ofd.write("{:d}    ".format(source))
      for prot, weight in connections.items():
        if weight == 1:
          ofd.write("{:d}:1 ".format(prot))
        else:
          ofd.write("{:d}:{:.3f} ".format(prot, weight))
      ofd.write("$\n")
    ofd.close()
    # return the path to the graph file
    return spGraphPath
