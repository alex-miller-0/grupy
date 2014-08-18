#!/bin/bash
#$ -V    #Inherit the submission environment
#$ -cwd  # Start job in submission directory
#$ -N test     # Job Name
#$ -j y  # Combine stderr and stdout
#$ -o $JOB_NAME.o$JOB_ID         # Name of the output file (eg. myMPI.oJobID)
#$ -pe 12way 24  # Requests 12 tasks/node, 24 cores total
#$ -q normal       # Queue name normal
#$ -l h_rt=20:00:00      # Run time (hh:mm:ss) - 1.5 hours
#$ -A ABO3
set -x   # Echo commands, use set echo with csh


PREFIX="PbS"

# calculations


INFILE="$PREFIX.in"
OUTFILE="$PREFIX.out"

cat > $INFILE << EOF
&CONTROL
wf_collect=.false.,
calculation ='scf',
restart_mode = 'from_scratch',
prefix='$PREFIX',
pseudo_dir='/work/02599/asmiller/pseudo/gbrv/pbe_GBRV/',
tstress=.true.,
tprnfor=.true.,
etot_conv_thr=1.0D-4,
forc_conv_thr=5.0D-8,
/
&SYSTEM
input_dft='pbesol',
ibrav=0,
celldm(1)=11.21853606d0,
nat=2,
ntyp=2,
ecutwfc=50,
ecutrho=600,
occupations = 'fixed',
/
&ELECTRONS
electron_maxstep=100,
conv_thr = 1.0D-10,
mixing_mode = 'plain',
mixing_beta = 0.7d0,
diagonalization = 'cg',
diago_cg_maxiter = 100
/
&IONS
ion_dynamics='bfgs',
/
&CELL
cell_dynamics='bfgs',
press=0.d0
/
ATOMIC_SPECIES
Pb 207.2d0 pb_pbe_v1.uspp.F.UPF
S 32.06d0  s_pbe_v1.2.uspp.F.UPF

CELL_PARAMETERS
   0.000000000d0   0.496881597d0   0.496881597d0
   0.496881597d0   0.000000000d0   0.496881597d0
   0.496881597d0   0.496881597d0   0.000000000d0

ATOMIC_POSITIONS crystal
Pb 0.0d0 0.0d0 0.0d0
S 0.5d0 0.5d0 0.5d0

K_POINTS automatic
12 12 12 0 0 0 

EOF

ibrun pw.x -npool 2 < $INFILE > $OUTFILE

INFILE="$PREFIX.ph.in"
OUTFILE="$PREFIX.ph.out"

cat > $INFILE << EOF 
Dispersion
&inputph
tr2_ph=1.0d-16,
epsil=.true.,
ldisp=.true.,
nq1=4, nq2=4, nq3=4,
prefix='$PREFIX',
fildyn='$PREFIX.dyn',
/


EOF

ibrun ph.x -npool 2 < $INFILE > $OUTFILE


