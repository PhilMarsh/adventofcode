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
	start, splitters := _load_diagram()

	num_timelines := _count_timelines(start, splitters)

	fmt.Println(num_timelines)
}

type Index int

func _load_diagram() (Index, []set.Set[Index]) {
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

	return start, splitters
}

func _count_timelines(pos Index, splitters []set.Set[Index]) int {
	cache := map[int]map[Index]int{}
	for depth := range splitters {
		cache[depth] = map[Index]int{}
	}

	var _count_memoized func(depth int, pos Index, splitters []set.Set[Index]) int
	_count_memoized = func(depth int, pos Index, splitters []set.Set[Index]) int {
		depth_cache := cache[depth]
		cached_pos_count, is_cached := depth_cache[pos]
		if is_cached {
			return cached_pos_count
		}

		if len(splitters) == 0 {
			return 1
		}
		split_set := splitters[0]
		next_splitters := splitters[1:]
		total_timelines := 0
		if split_set.Has(pos) {
			// Don't need to check bounds because we know the input doesn't have
			// splitters on the edges.
			total_timelines += _count_memoized(depth+1, pos-1, next_splitters)
			total_timelines += _count_memoized(depth+1, pos+1, next_splitters)
		} else {
			total_timelines += _count_memoized(depth+1, pos, next_splitters)
		}

		depth_cache[pos] = total_timelines
		return total_timelines
	}

	return _count_memoized(0, pos, splitters)
}
