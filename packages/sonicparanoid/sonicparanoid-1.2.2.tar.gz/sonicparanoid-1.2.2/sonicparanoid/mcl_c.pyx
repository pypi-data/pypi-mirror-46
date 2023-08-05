"""Functions to create graph and matrixes from ortholog tables."""
from libc.stdio cimport *
from libc.stdlib cimport atoi
from libc.stdlib cimport atof
import sys
import os
import pickle
from typing import Dict, List, Tuple, Deque, Set
import numpy as np
import multiprocessing as mp
from shutil import copyfileobj
from collections import deque
from sonicparanoid import sys_tools as systools
# import Cython module for graph and matrixes creation
from sonicparanoid import graph_c


__module_name__ = 'MCL'
__source__ = 'mcl_c.pyx'
__author__ = 'Salvatore Cosentino'
__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Cosentino Salvatore'
__email__ = 'salvo981@gmail.com'



""" FUNCTIONS """
def info():
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



def concatenate_files(fPaths: Deque[str], removeProcessed: bool = False, chunkSize: int = 10, debug: bool = False):
  """Concatenate a multiple files into a single one"""
  if debug:
    print("\nconcatenate_files :: START")
    print("Files to be concatenated (sequencially):\t{:d}".format(len(fPaths)))
    print("Remove merged files: {:s}".format(str(removeProcessed)))
    print("Write chunks of {:d} Megabytes".format(chunkSize))
  # concatenate to the first file
  f1 = fPaths.popleft()
  qLen: int = len(fPaths)
  # open in append mode
  with open(f1,'ab') as wfd:
      # while there are file to concatenate
      while len(fPaths) > 0:
          qLen = len(fPaths)
          f = fPaths.popleft()
          if not os.path.isfile(f):
            sys.stderr.write("\nERROR: {:s}\nis not a valid file.\n")
            sys.exit(-2)
          if debug:
            print("Concatenating: {:s}\tremaining files: {:d}".format(os.path.basename(f), qLen))
          with open(f,'rb') as fd:
              copyfileobj(fd, wfd, 1024*1024*chunkSize)
              if removeProcessed:
                os.remove(f)



def run_mcl(mclGraph: str, outPath: str, inflation: float = 1.5, threads: int = 4, removeInput: bool = False, debug: bool = False):
  """Perform MCL clustering."""
  if debug:
    print("\nrun_mcl :: START")
    print("Input MCL graph: {:s}".format(mclGraph))
    print("Output file with clusters: {:s}".format(outPath))
    print("Remove input graph file:\t{:s}".format(str(removeInput)))
    print("Inflation rate:\t{:.2f}".format(inflation))
    print("Threads:\t{:d}".format(threads))
  if not os.path.isfile(mclGraph):
    sys.stderr.write("\nERROR: the MCL input file {:s}\nwas not found.\n")
    sys.exit(-2)

  # make sure MCL is installed
  # check if mcl has been installed
  mclPath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcl_package/bin/mcl')
  if os.path.isfile(mclPath):
    if debug:
      print("MCL is installed at {:s}".format(mclPath))
  else:
    sys.stderr.write("\nERROR: the MCL program was not found.\nPlease try to re-install SonicParanoid.\n")
    sys.exit(-5)

  # file for the MCL log
  mclLogStderr = os.path.join(os.path.dirname(outPath), "mcl.stderr.txt")
  mclLogStdout = os.path.join(os.path.dirname(outPath), "mcl.stdout.txt")
  # Run MCL
  # MCL run example
  # mcl mcl_graph_1-4_species_test.txt -o mcl_4sp_out.txt -I 1.5 -te 8 -V all
  ### USE SYSTEM INSTALLATION ###
  # from sh import mcl
  ###############################

  import sh
  mcl = sh.Command(mclPath)
  mcl(mclGraph, "-o", outPath, "-I", inflation, "-te", threads, "-V", "all", _out=mclLogStdout, _err=mclLogStderr)

  # make sure the output file was created
  if not os.path.isfile(outPath):
    sys.stderr.write("\nERROR: MCL output file was not created, something went wrong.\n")
    sys.exit(-5)

  # remove the input graph if required
  if removeInput:
    os.remove(mclGraph)



def remap_mcl_groups(mclGrps: str, outPath: str, runDir: str = os.getcwd(), writeFlat: bool = False, debug: bool = False):
  """Create SonicParanoid groups from raw MCL clusters."""
  if debug:
    print("\nremap_mcl_groups :: START")
    print("Input MCL clusters: {:s}".format(str(mclGrps)))
    print("Output groups file: {:s}".format(str(outPath)))
    print("Run directory: {:s}".format(runDir))
    print("Write file with flat groups:\t{:s}".format(str(writeFlat)))
  if not os.path.isfile(mclGrps):
    sys.stderr.write("\nERROR: the MCL cluster file\n{:s}\nwas not found.\n".format(mclGrps))
    sys.exit(-2)
  # load the offsets and protein counts
  protCntPcklPath = os.path.join(runDir, "protein_counts.pckl")
  # compute the offsets
  offsetDict = graph_c.compute_offsets(protCntPcklPath, debug=debug)[0]
  # create arrays with offsets and species
  spArray = np.array(list(offsetDict.keys()), dtype=np.uint16)
  offsetArray = np.array(list(offsetDict.values()), dtype=np.uint32)
  # create the output cluster and write the header
  ofd = open(outPath, "wt")
  # create file with "flat" groups
  flatFd = None
  if writeFlat:
    flatName: str = "flat.{:s}".format(os.path.basename(outPath))
    flatFd = open(os.path.join(os.path.dirname(outPath), flatName), "wt")
    # write the header
    flatFd.write("group_id\t")
    flatFd.write("{:s}\n".format("\t".join(["%d" % x for x in spArray])))
  spNamesInHdr = ["%d\tavg_score_sp%d" % (x, i+1) for i, x in enumerate(spArray)]
  ofd.write('group_id\tgroup_size\tsp_in_grp\tseed_ortholog_cnt\t%s\n'%('\t'.join(spNamesInHdr)))
  del spNamesInHdr
  # create the file with not clustered proteins
  soiltaryOutPath = os.path.join(os.path.dirname(outPath), "not_assigned_genes.{:s}".format(os.path.basename(outPath)))
  ofdNotAssigned = open(soiltaryOutPath, "wt")
  # dictionary to map offsets to species ids
  offset2spDict = {val:k for k, val in offsetDict.items()}
  # buffer string
  tmpStr: str = ""
  # keep track of the species with non clustered proteins
  # that are being processed
  notClusteredSpId: Int = 0
  # species count
  totSp: int = len(spArray)
  # will contain the genes to be added to the output table
  tmpSonicGrpDict: Dict[int, Dict[str, None]]
  # will contain protein that could not be clustered and its species id
  tmpNotAssigendTpl: Tuple[int, str]
  # contains the size of sonicpara groups
  grpSize: int = 0
  # contains the number of species in a given group
  spInGrpDict: Dict[int, None] = {}
  # flag to control the processing
  process: bool = False
  # start reading the input clusters
  ifd = open(mclGrps, "rt")
  # skip the first 7 lines
  for i in range(7):
    ifd.readline()
  cnt: int = 0
  clstrCnt: int = 0
  for dln in ifd:
    cnt += 1
    if len(dln) == 2:
      break # end of the cluster file
    dln = dln[:-1] # remove the newline
    #print(dln)
    # check if it a single cluster or a new one
    if dln[0] != " ":
      # remove the orthogroup id
      tmpStr += dln.split(" ", 1)[-1].lstrip(" ")
      if tmpStr[-1] == "$":
        tmpStr = tmpStr[:-2]
        process = True
      else:
        process = False
        continue
    else:
      tmpStr = "%s %s" % (tmpStr, dln.lstrip(" "))
      # check if it is the end of the cluster
      if tmpStr[-1] == "$":
        tmpStr = tmpStr[:-2]
        # process the clusters
        process = True
    # process the cluster if required
    if process:
      # put the string in buckets based on the offsets
      tmpArray = np.array([int(x) for x in tmpStr.split(" ")], dtype=np.uint32)
      grpSize = len(tmpArray)
      spInGrpDict.clear()
      # initialize the dictionary with empty dictionaries
      tmpSonicGrpDict = {x:{} for x in spArray}
      # iterate throught the array and find the species
      for x in tmpArray:
        # get the offset by finding the rightmost index with True
        offsetIdx = (x >= offsetArray).nonzero()[0][-1]
        tmpOffset: int = offsetArray[offsetIdx]
        tmpSpId: int = spArray[offsetIdx]
        if not tmpSpId in spInGrpDict:
          spInGrpDict[tmpSpId] = None
        # compute species ID
        tmpId: str = "{:d}.{:d}".format(tmpSpId, x - tmpOffset + 1)
        if debug:
          print("\nsearching species for {:d} in {:s}".format(x, str(tmpArray)))
          print("Offsets:", offsetArray)
          print("Species:", spArray)
          print(x >= offsetArray)
          print("offsetIdx={:d} found_offset={:d}".format(offsetIdx, tmpOffset))
          print("species_from_array:\t{:d}".format(tmpSpId))
          print("mapping:\t{:d} -> {:s}".format(x, tmpId))

        if len(tmpArray) == 1:
          tmpNotAssigendTpl = (tmpSpId, tmpId)
        else:
          # add the id to the proper species dictionary
          if not tmpId in tmpSonicGrpDict[tmpSpId]:
            tmpSonicGrpDict[tmpSpId][tmpId] = None
          else:
            sys.exit("\nMultiple protein in groups!!!\nImpossible!")
      # process the MCL group and write it in the output
      clstrCnt += 1
      # reset the string
      tmpStr: str = ""
      process = False
      # NOTE: for now we do not write scores...
      if grpSize > 1:
        ofd.write("{:d}\t{:d}\t{:d}\t{:d}\t".format(clstrCnt, grpSize, len(spInGrpDict), grpSize))
        if writeFlat:
          flatFd.write("{:d}\t".format(clstrCnt))

        # now write orthologs by species
        loopCnt: int = 0
        for spParalogs in tmpSonicGrpDict.values():
          loopCnt += 1
          if len(spParalogs) == 0:
            ofd.write("*\t0")
            if writeFlat:
              flatFd.write("*")
          else:
            ofd.write("{:s}\t1".format(",".join(spParalogs)))
            if writeFlat:
              flatFd.write("{:s}".format(",".join(spParalogs)))
          # terminate the cluster line
          if loopCnt == totSp:
            ofd.write("\n")
            if writeFlat:
              flatFd.write("\n")
          else:
            ofd.write("\t")
            if writeFlat:
              flatFd.write("\t")
      else: # write the gene in the file with not clustered paralogs
        currentNotAssignedSpId, solitaryPara = tmpNotAssigendTpl
        if notClusteredSpId == 0:
          ofdNotAssigned.write("#{:d}\n".format(currentNotAssignedSpId))
          notClusteredSpId = currentNotAssignedSpId
        elif notClusteredSpId != currentNotAssignedSpId:
          ofdNotAssigned.write("\n#{:d}\n".format(currentNotAssignedSpId))
          notClusteredSpId = currentNotAssignedSpId
        # write the protein id
        ofdNotAssigned.write("{:s}\n".format(solitaryPara))
  # close output files
  ofdNotAssigned.close()
  ofd.close()
  if writeFlat:
    flatFd.close()

  if debug:
    print("\n#Processed clusters lines:\t{:d}".format(cnt))
    print("#Single clusters:\t{:d}".format(clstrCnt))


# TO DO: implement the species skip properly
def write_mcl_matrix(spArray, spSkipArray, runDir: str = os.getcwd(), mtxDir: str = os.getcwd(), outDir: str = os.getcwd(), threads: int = 4, removeProcessed: bool = False, debug: bool = False):
  """Generate the input matrix for MCL."""
  if debug:
    print("\nwrite_mcl_matrix :: START")
    print("Species for which the MCL graph will created:\t{:d}".format(len(spArray)))
    print("Species that will be skipped in the MCL graph creation:\t{:d}".format(len(spSkipArray)))
    print("Run directory: {:s}".format(runDir))
    print("Directory with ortholog matrixes: {:s}".format(mtxDir))
    print("Output directory: {:s}".format(runDir))
    print("Threads:{:d}".format(threads))
    print("Remove merged subgraphs:\t{:s}".format(str(removeProcessed)))

  # check that the array with species is not empty
  if len(spArray) == 0:
    sys.stderr.write("ERROR: you must provide at least 1 species for which the graph must be created.")
    sys.exit(-6)

  # create the main output MCL graph
  mclGraphPath = os.path.join(outDir, "mcl_input_graph.txt")
  # compute offsets
  offsetDict, sizeDict = graph_c.compute_offsets(os.path.join(runDir, "protein_counts.pckl"), debug=debug)
  mtxSize = sum(list(sizeDict.values()))

  '''
  (mclheader
  mcltype matrix
  dimensions 10300x10300
  )

  (mclmatrix
  begin
  '''
  ofd = open(mclGraphPath, "wt")
  # write the MCL graph header
  ofd.write("(mclheader\nmcltype matrix\ndimensions %dx%d\n)\n\n(mclmatrix\nbegin\n\n" %(mtxSize, mtxSize))
  ofd.close()
  # create the graph of each species
  subgraphsPaths = graph_c.write_per_species_mcl_graph_parallel(spArray, runDir=runDir, mtxDir=mtxDir, outDir=outDir, threads=threads, debug=debug)
  # fill a deque with the keys
  subgraphsPaths = deque(subgraphsPaths.values(), maxlen=len(subgraphsPaths) + 1)
  # add the main matrix file to the left of the deque
  subgraphsPaths.appendleft(mclGraphPath)
  # now concatenate the subgraphs
  concatenate_files(subgraphsPaths, removeProcessed=removeProcessed, chunkSize=10, debug=debug)
  # close the MCL matrix file
  with open(mclGraphPath, "at") as ofd:
    ofd.write(")")
  # return the graph
  return mclGraphPath
