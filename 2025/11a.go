package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	graph := _load_devices()
	fmt.Println(graph)

	num_paths := _count_paths(graph, "you", "out")
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

func _count_paths(graph Graph, from string, to string) int {
	if from == to {
		return 1
	}
	count := 0
	for _, next := range graph[from].next_names {
		count += _count_paths(graph, next, to)
	}
	return count
}
