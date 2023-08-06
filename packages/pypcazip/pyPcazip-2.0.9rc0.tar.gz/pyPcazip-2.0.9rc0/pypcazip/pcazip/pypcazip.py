#!/usr/bin/env python
"""
 The python version of pcazip!!

 Reproduces the functionality of the old fortran- and C-based versions.

 In essence its wraps a simple set of procedures provided by two modules:
       'cofasu' - trajectory file handling
       'pcz'    - PCA analysis

 Stripped down to the bare essentials, the complete procedure is:

 >>> from MDPlus.analysis.pca import Pcz
 >>> from MDPlus.core import Fasu, Cofasu
 >>>
 >>> f = Fasu('topology.top','trajectory.traj')
 >>> c = Cofasu(f)
 >>> p = Pcz(c)
 >>> p.write('compressed.pcz')

 Everything else is basically analysing and sanity-checking the arguments
 given on the command line.
"""

from __future__ import absolute_import, print_function, division

# General python libraries import.
import os.path as op
import sys
import logging as log
import warnings
#warnings.simplefilter('ignore')

from MDPlus.analysis import pca
#from MDPlus.core import Fasu, Cofasu
import mdio
from MDPlus.utils import pdb2selection
import numpy as np
from time import time
import tempfile

#                        PCAZIP main function (start)                       #
#                                                                           #
#############################################################################

def pcazip(args):

    # Time the complete run time
    time0start = time()

    if args.nompi:
        comm = None
        rank = 0
        size = 1
    else:
        try:
            from mpi4py import MPI
            comm = MPI.COMM_WORLD
            rank = comm.Get_rank()
            size = comm.Get_size()
        except ImportError:
            comm = None
            rank = 0
            size = 1


    if args.verbosity:
        if args.verbosity > 1:
            log.basicConfig(format="%(levelname)s: %(message)s", 
                            level=log.DEBUG)

        elif args.verbosity == 1:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    if args.tests:
        from subprocess import call
        import os
        try:
            tdir = tempfile.mkdtemp()
            log.info('Creating temporary test directory {}'.format(tdir))
            here = os.getcwd()
            os.chdir(tdir)
            call(['wget','-q','-P', tdir,
                     'https://bitbucket.org/ramonbsc/pypcazip/downloads/test200.tar.gz'])
            call(['tar', 'xf', tdir + '/test200.tar.gz', "-C", tdir])
            os.chdir(tdir + '/test')
            call(['./run_tests.sh'])
            os.chdir(here)
            if (rank == 0):
                log.info('Please explore additional testing scripts and related trajectory files as necessary at '+op.expanduser(tdir + '/test'))
        except:
            if (rank == 0):
                log.error('')
                log.error('Error while trying to test the correct installation of the pyPcazip suite tools!')
                log.error('')        
            sys.exit(-1)
        sys.exit(0)
			
            
    '''
    Input filename and topology filename are mandatory. Hence a check on
    these two parameters should be performed:
    '''
    if (args.input is None or args.topology is None):
        if rank == 0:
            log.error('')
            log.error('All or any of the mandatory command line arguments is missing. The correct usage is:')
            log.error( 'python ./pcazip.py -i|--input <input-file> -t|--topology <topology-file> [optional arguments]')
            log.error('')
            log.error('Type "python ./pcazip.py -h" or "python ./pcazip.py --help" for further details.')
            log.error('')
        sys.exit(-1)

    '''
    Multiple trajectory files are permitted.
    The rule is that all the trajectory files must be
    compatible with a single topology file or one topology file must be
    provided for each trajectory file. 
    The same rules operate (independently)
    for the selection and masking options: either there should be one
    selection/mask that applies to ALL trajectory files, or there
    should be one selection/mask for each trajectory file.
    '''

    na = len(args.input)
    nt = len(args.topology)
    if args.selection is None:
        ns = 1
    else:
        ns = len(args.selection)
    if args.mask is not None:
        ns = max(ns, len(args.mask))
    if nt > 1 and nt != na:
        if rank == 0:
            log.error(("Number of topology files must be one, or equal"
                       " to the number of trajectory files."))
        sys.exit(-1)
    if ns > 1 and ns != na:
        if rank == 0:
            log.error(("Number of masks/selections must be one, or equal"
                       " to the number of trajectory files."))
        sys.exit(-1)
    
    '''
    We can now build the key data structures.
    '''
    trajfiles = []
    tops = []
    selections = []
    for i in range(len(args.input)):
        log.debug('Reading trajectory file {0}'.format(i))
        # sort out the selection string:
        if args.selection is None:
            sel = 'all'
        else:
            if len(args.selection) == 1:
                sel = args.selection[0]
            else:
                sel = args.selection[i]
        if args.mask is not None:
            if len(args.mask) == 1:
                sel = pdb2selection(args.mask[0])
            else:
                sel = pdb2selection(args.mask[i])
        # sort out the topology file string:
        if len(args.topology) == 1:
            top = args.topology[0]
        else:
            top = args.topology[i]

        trajfiles.append(args.input[i])
        tops.append(top)
        selections.append(sel)

    # Now we can create the cofasu:
    f = []
    kwargs = {}
    if args.centre is not None:
        kwargs['centre'] = args.centre
        kwargs['pack_into_box'] = True
        if rank == 0:
            log.info('Will place group {0} at centre of box to fix jumps'.format(args.centre))
    #Time reading/gathering of the trajectories in parallel
    if rank == 0:
        log.info('Reading trajectory files...')

    time1start = time()
    traj_all = mdio.mpi_load(trajfiles, top=tops, selection=selections, comm=comm)
    time1end = time()
    if rank == 0:
        log.debug('Time to read trajectory files: {0:.2f} s'.format(time1end -
                  time1start))

    if args.trj_output is not None:
        traj_all.save(args.trj_output)
        if rank == 0:
            log.info('Wrote selected frames and atoms ' 
                     + 'to trajectory file {0}'.format(args.trj_output))

    if args.nopca is False:
        # run the pca analysis:
        if rank == 0:
            if args.weighted:
                log.info('Running mass-weighhted pca analysis')
            else:
                log.info('Running pca analysis')
        time2start = time()
        p = pca.fromtrajectory(traj_all, quality=float(args.quality), 
                               req_evecs=args.evecs,
                               weighted=args.weighted,
                               nofit=args.nofit,
                               fastmethod=args.fast)
        time2end = time()
        if rank == 0:
            log.debug('Time for pcz-analysis: {0:.2f} s'.format(time2end -
                     time2start))
            log.info("Writing compressed trajectory")

        if args.output is not None:
            output_file = args.output
        else:
            # The input trajectory file is a mandatory argument and the check
            # on this has been done previously.
            dir = op.dirname(uniStr[0][0][1])
            base_out_compressed = op.basename(uniStr[0][0][1])
            name_out_compressed = op.splitext(base_out_compressed)[0]
            output_file = op.join(dir, name_out_compressed + "_output.pcz")

        if rank == 0:
            time_write_output_0 = time()
            p.write(output_file)
            time_write_output_1 = time()

        if args.pdb_out is not None:
            traj_all[0].save(args.pdb_out)
        if rank == 0:
            totTime = time() - time0start
            log.debug('Time to write the output file: {0:.2f} s'.format(
                time_write_output_1 - time_write_output_0))
            log.debug('Total run time:: {0:.2f} s\n'.format(totTime))
