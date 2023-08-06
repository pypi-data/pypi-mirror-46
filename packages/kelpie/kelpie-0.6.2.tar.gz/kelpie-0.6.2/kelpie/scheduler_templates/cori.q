#!/bin/bash -l
#SBATCH -J {job-name}
#SBATCH -N {nodes}
#SBATCH -t {walltime}
#SBATCH -q {qos}
#SBATCH -A {account}
#SBATCH -C {constraint}
#SBATCH -L {license}
#SBATCH -o {output}

ulimit -s unlimited
export OMP_NUM_THREADS=1

{modules}

source activate kelpie
kelpie -m graze -l {run_location} {calculation_params}
