#!/usr/bin/env bash

./bin/spark-submit ./src/words_tweeted.py > ./tweet_output/ft1.txt
python ./src/median_unique.py ./tweet_input/tweets.txt > ./tweet_output/ft2.txt




