#
# Copyright 2019, Julian Catchen <jcatchen@illinois.edu>
#
# This file is part of RADinitio.
#
# RADinitio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RADinitio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RADinitio. If not, see <http://www.gnu.org/licenses/>.
#

import os, sys, argparse
import msprime
import radinitio as ri

usage = '''\
radinitio --genome path --chromosomes path --out-dir dir [(demographic model options)] [(library options)]

Input/Output files:
    -g, --genome:        Path to reference genome (fasta file, may be gzipped). (Required)
    -l, --chromosomes:   File containing the list of chromosomes (one per line) to simulate. (Required)
    -o, --out-dir:       Path to an output directory where all files will be written. Will be created and must not exist. (Required)

Demographic model (simple island model)
    -p, --n-pops:        Number of populations in the island model  (default = 2)
    -n, --pop-eff-size:  Effective population size of simulated demes  (default = 5000)
    -s, --n-seq-indv:    Number of individuals sampled from each population  (default = 10)

Library preparation/sequencing:
    -b, --library-type:  Library type (sdRAD or ddRAD)  (default = 'sdRAD')
    -e, --enz:           Restriction enzyme (SbfI, PstI, EcoRI, BamHI, etc.)  (default = 'SbfI')
    -d, --enz2:          Second restriction enzyme for double digest (MspI, MseI, AluI, etc.)  (default = 'MspI')
    -c, --pcr-cycles:    Number of PCR cycles  (default = 0)
    -v, --coverage:      Sequencing coverage  (default = 20)
'''

def parse_args():
    p = argparse.ArgumentParser(prog='radinitio')
    p.add_argument('-g', '--genome',       required=True)
    p.add_argument('-l', '--chromosomes',  required=True)
    p.add_argument('-o', '--out-dir',      required=True)
    p.add_argument('-p', '--n-pops',       type=int, default=2)
    p.add_argument('-n', '--pop-eff-size', type=float, default=5e3)
    p.add_argument('-s', '--n-seq-indv',   type=int, default=10)
    p.add_argument('-b', '--library-type', default='sdRAD')
    p.add_argument('-e', '--enz',          default='SbfI')
    p.add_argument('-d', '--enz2',         default='MspI')
    p.add_argument('-c', '--pcr-cycles',   type=int, default=0)
    p.add_argument('-v', '--coverage',     type=int, default=20)

    # Overwrite the help/usage behavior.
    p.format_usage = lambda : usage
    p.format_help = p.format_usage

    # Check input arguments
    args = p.parse_args()
    args.out_dir = args.out_dir.rstrip('/')
    assert args.n_pops >= 1
    assert os.path.exists(args.genome)
    assert os.path.exists(args.chromosomes)
    if os.path.exists(args.out_dir):
        sys.exit("Error: '{}': cannot create directory (already exist).".format(args.out_dir))

    return args

def main():
    args = parse_args()

    # Msprime parameters
    # Create the population(s).
    pops = [
        msprime.PopulationConfiguration(
            sample_size = 2 * args.n_seq_indv,
            initial_size = args.pop_eff_size,
            growth_rate = 0.0)
        for i in range(args.n_pops) ]
    msprime_simulate_args = {
        'mutation_rate' : 7e-8,
        'population_configurations' : pops }
    if args.n_pops > 1:
        # Create the (symmetric) migration matrix.
        # In msprime, each element `M[j,k]` of the migration matrix defines the fraction
        # of population `j` that consists of migrants from population `k` in each generation.
        # Additionally, there should be zeroes on the diagonal.
        pop_immigration_rate = 0.001 # Total per-population per-generation immigration rate.
        m = pop_immigration_rate / (args.n_pops - 1)
        migration_matrix = [ [
                0 if k == j else m
                for k in range(args.n_pops) ]
                for j in range(args.n_pops) ]
        msprime_simulate_args['migration_matrix'] = migration_matrix

    chromosomes = open(args.chromosomes).read().split()
    recomb_rate = 3e-8

    # RADinito options
    muts_opts = ri.MutationModel()
    library_opts = ri.LibraryOptions(
        library_type = args.library_type,
        renz_1 = args.enz,
        renz_2 = args.enz2,
        coverage=args.coverage)
    pcr_opts = ri.PCRDups(
        pcr_c = args.pcr_cycles)

    # Call radinitio.simulate
    ri.simulate(
        out_dir = args.out_dir,
        genome_fa = args.genome,
        chromosomes = chromosomes,
        chrom_recomb_rates = recomb_rate,
        msprime_simulate_args = msprime_simulate_args,
        library_opts = library_opts,
        mutation_opts = muts_opts,
        pcr_opts = pcr_opts)

if __name__ == '__main__':
    main()
