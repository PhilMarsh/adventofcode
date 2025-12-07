package main

import (
	"aoc2025/set"
	"bufio"
	"fmt"
	"os"
	"strings"
)

const START = 'S'
const SPLITTER = '^'

func main() {
	state, splitters := _load_diagram()

	num_splits := _count_splits(state, splitters)

	fmt.Println(num_splits)
}

type Index int

func _load_diagram() (set.Set[Index], []set.Set[Index]) {
	file, _ := os.Open("07.in")
	scanner := bufio.NewScanner(file)

	var start Index
	var splitters []set.Set[Index]
	i := 0
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		splitters = append(splitters, set.Set[Index]{})
		for j, char := range line {
			if char == START {
				start = Index(j)
			} else if char == SPLITTER {
				splitters[i].Add(Index(j))
			}
		}

		i += 1
	}

	state := set.Make([]Index{start})
	return state, splitters
}

func _count_splits(state set.Set[Index], splitters []set.Set[Index]) int {
	total_splits := 0
	for _, split_set := range splitters {
		next, num_splits := _next_state(state, split_set)
		state = next
		total_splits += num_splits
	}
	return total_splits
}

func _next_state(state set.Set[Index], splitters set.Set[Index]) (set.Set[Index], int) {
	next := state.Clone()
	num_splits := 0
	for j := range splitters.Iter() {
		if next.Has(j) {
			num_splits += 1

			next.Remove(j)
			// Don't need to check bounds because we know the input doesn't have
			// splitters on the edges.
			next.Add(j - 1)
			next.Add(j + 1)
		}
	}
	return next, num_splits
}
