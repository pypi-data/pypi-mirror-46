#!/bin/zsh

# # # SHELL SCRIPT TO TEST VARIOUS USE CASES OF BOSS CODE
# # # these take about ~10 minutes to run

# make script stop at first error
set -e

# directory for storing output
rm -rf test_results
mkdir -p test_results

# run boss
echo "Running test 1/4"
boss op input_files/LennardJones
./move.sh test_results/LennardJones
echo "Running test 2/4"
boss op input_files/SineCosine
./move.sh test_results/SineCosine
echo "Running test 3/4"
boss op input_files/2dPeriodic
./move.sh test_results/2dPeriodic
echo "Running test 4/4"
boss op input_files/alanine
./move.sh test_results/alanine

# define a utility function
is_small () {
    comp1=$(echo $1'>'0.2 | bc -l)
    comp2=$(echo $1'<'-0.2 | bc -l)
    if [ $comp1 -eq 1 ]; then
        echo "Warning: Wrong value detected in an output file '$2'"
    elif [ $comp2 -eq 1 ]; then
        echo "Warning: Wrong value detected in an output file '$2'"
    fi
}

# check that correct minima where found
echo "Checking for correct values"
set +e # make script tolerate errors temporarily
line=($(grep "Global minimum prediction" -A 1 test_results/LennardJones/boss.out | tail -1))
minx=$(echo ${line[1]}); miny=$(echo ${line[2]})
minx=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$minx")
minx=$(echo $minx - 1.0 | bc -l)
is_small "$minx" test_results/LennardJones/boss.out
miny=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$miny")
miny=$(echo $miny + 2.0 | bc -l)
is_small "$miny" test_results/LennardJones/boss.out

line=($(grep "Global minimum prediction" -A 1 test_results/SineCosine/boss.out | tail -1))
minx=$(echo ${line[1]}); miny=$(echo ${line[2]})
minx=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$minx")
minx=$(echo $minx -0.75 | bc -l)
is_small "$minx" test_results/SineCosine/boss.out
miny=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$miny")
miny=$(echo $miny + 2.0 | bc -l)
is_small "$miny" test_results/SineCosine/boss.out

line=($(grep "Global minimum prediction" -A 1 test_results/2dPeriodic/boss.out | tail -1))
miny=$(echo ${line[3]})
miny=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$miny")
miny=$(echo $miny + 1.0 | bc -l)
is_small "$miny" test_results/2dPeriodic/boss.out

line=($(grep "Global minimum prediction" -A 1 test_results/alanine/boss.out | tail -1))
minx1=$(echo ${line[1]}); minx2=$(echo ${line[2]}); minx3=$(echo ${line[3]})
minx4=$(echo ${line[4]}); miny=$(echo ${line[5]})
minx1=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$minx1")
minx1=$(echo $minx1 - 64.69 | bc -l)
is_small "$minx1" test_results/alanine/boss.out
minx2=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$minx2")
minx2=$(echo $minx2 - 183.09 | bc -l)
is_small "$minx2" test_results/alanine/boss.out
minx3=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$minx3")
minx3=$(echo $minx3 - 200.14 | bc -l)
is_small "$minx3" test_results/alanine/boss.out
minx4=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$minx4")
minx4=$(echo $minx4 - 182.27 | bc -l)
is_small "$minx4" test_results/alanine/boss.out
miny=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<<"$miny")
miny=$(echo $miny - 14.489 | bc -l)
is_small "$miny" test_results/alanine/boss.out
set -e # make script tolerate errors no more

# finish
cd ..
echo -e "\nBOSS TESTS COMPLETED SUCCESFULLY!\n--- If there were warnings, check manually whether and how\nthey made test_results/ different from correct_results/ ---\n"


