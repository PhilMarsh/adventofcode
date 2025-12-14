package main

import (
	"aoc2025/set"
	"bufio"
	"fmt"
	"os"
	"slices"
	"strings"
)

func main() {
	graph := _load_devices()
	// fmt.Println(graph)

	required_node_names := NameSet(set.Make([]string{"dac", "fft"}))
	num_paths := _count_paths_through(graph, "svr", "out", required_node_names)
	fmt.Println(num_paths)
}

type Node struct {
	name       string
	next_names []string
}

type Graph map[string]Node

func _load_devices() Graph {
	file, _ := os.Open("11.in")
	scanner := bufio.NewScanner(file)

	graph := Graph{}
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		parts := strings.Split(line, " ")
		node := Node{
			strings.Trim(parts[0], ":"),
			parts[1:],
		}
		graph[node.name] = node
	}

	return graph
}

type NameSet = set.Set[string]

func name_set_key(self NameSet) string {
	names := slices.Collect(self.Iter())
	slices.Sort(names)
	return strings.Join(names, ",")
}

func name_set_from_key(key string) NameSet {
	if key == "" {
		return NameSet{}
	} else {
		return set.Make(strings.Split(key, ","))
	}
}

func _count_paths_through(graph Graph, from string, to string, needed NameSet) int {
	type NeededSeenPathCounts = map[string]int

	cache := map[string]NeededSeenPathCounts{}

	var _count_paths_cached func(at string) NeededSeenPathCounts
	_count_paths_cached = func(at string) NeededSeenPathCounts {
		cached_counts, is_cached := cache[at]
		if is_cached {
			return cached_counts
		}

		result := NeededSeenPathCounts{}
		at_needed_name_set := NameSet{}
		if needed.Has(at) {
			at_needed_name_set.Add(at)
		}

		if at == to {
			result[name_set_key(at_needed_name_set)] = 1
		} else {
			for _, next := range graph[at].next_names {
				for sub_key, sub_count := range _count_paths_cached(next) {
					sub_name_set := name_set_from_key(sub_key)
					result_needed_key := name_set_key(at_needed_name_set.Union(sub_name_set))
					_, has := result[result_needed_key]
					if !has {
						result[result_needed_key] = 0
					}
					result[result_needed_key] += sub_count
				}
			}
		}

		cache[at] = result
		return result
	}

	path_counts := _count_paths_cached(from)
	fmt.Println(path_counts)
	result_count, has := path_counts[name_set_key(needed)]
	if has {
		return result_count
	} else {
		return 0
	}
}
