rm -f src-train.txt src-test.txt src-val.txt tgt-train.txt tgt-test.txt tgt-val.txt

cat ../LRT-2610/src-train1.txt ../LRT-2610/src-train2.txt ../small/src-train.txt ../tatoeba/src-train.txt >src-train.txt
cat ../LRT-2610/tgt-train1.txt ../LRT-2610/tgt-train2.txt ../small/tgt-train.txt ../tatoeba/tgt-train.txt >tgt-train.txt

cat ../LRT-2610/src-test.txt ../small/src-test.txt ../tatoeba/src-test.txt >src-test.txt
cat ../LRT-2610/tgt-test.txt ../small/tgt-test.txt ../tatoeba/tgt-test.txt >tgt-test.txt

cat ../LRT-2610/src-val.txt ../small/src-val.txt ../tatoeba/src-val.txt >src-val.txt
cat ../LRT-2610/tgt-val.txt ../small/tgt-val.txt ../tatoeba/tgt-val.txt >tgt-val.txt

