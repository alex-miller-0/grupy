#!/bin/bash
#$ -V    #Inherit the submission environment
#$ -cwd  # Start job in submission directory
#$ -N gete_disp     # Job Name
#$ -j y  # Combine stderr and stdout
#$ -o $JOB_NAME.o$JOB_ID         # Name of the output file (eg. myMPI.oJobID)
#$ -pe 12way 36  # Requests 12 tasks/node, 24 cores total
#$ -q normal       # Queue name normal
#$ -l h_rt=24:00:00      # Run time (hh:mm:ss) - 1.5 hours
#$ -A ABO3
set -x   # Echo commands, use set echo with csh


PREFIX="GeTe_d"

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
celldm(1)=11.35649987d0,
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
Ge 72.63d0 ge_pbe_v1.uspp.F.UPF
Te 127.6d0 te_pbe_v1.uspp.F.UPF

CELL_PARAMETERS
   0.000000000d0  -0.399246222d0   0.578673564d0
   0.345757371d0   0.199623111d0   0.578673564d0
  -0.345757371d0   0.199623111d0   0.578673564d0

ATOMIC_POSITIONS crystal
Ge       0.006052773d0   0.006052773d0   0.006052773d0
Te       0.483947227d0   0.483947227d0   0.483947227d0

K_POINTS automatic
12 12 12 0 0 0 

EOF

ibrun pw.x -npool 3 < $INFILE > $OUTFILE

INFILE="$PREFIX.ph.in"
OUTFILE="$PREFIX.ph.out"

cat > $INFILE << EOF 
Dispersion
&inputph
tr2_ph=1.0d-16,
epsil=.true.,
ldisp=.true.,
prefix='$PREFIX',
fildyn='$PREFIX.dyn',
nq1=6, nq2=6, nq3=6
/


EOF

ibrun ph.x -npool 3 < $INFILE > $OUTFILE

rm *.wf*

