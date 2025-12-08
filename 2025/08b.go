package main

import (
	"aoc2025/set"
	"aoc2025/vector"
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	boxes := _load_boxes()

	last_box_indexes := _combine_all_circuits(boxes)

	last_box_a := boxes[last_box_indexes[0]]
	last_box_b := boxes[last_box_indexes[1]]

	x_coord_product := int(last_box_a[0]) * int(last_box_b[0])

	fmt.Println(x_coord_product)
}

func _load_boxes() []vector.Vector3 {
	file, _ := os.Open("08.in")
	scanner := bufio.NewScanner(file)

	var boxes []vector.Vector3
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		parts := strings.Split(line, ",")
		box := vector.Vector3{}
		for i := range box {
			value, _ := strconv.ParseFloat(parts[i], 32)
			box[i] = value
		}
		boxes = append(boxes, box)
	}

	return boxes
}

func _combine_all_circuits(boxes []vector.Vector3) [2]int {
	circuits := map[int]set.Set[int]{}
	boxes_to_circuits := map[int]int{}
	// Every box starts in its own isolated circuit.
	for i := range len(boxes) {
		circuits[i] = set.Make([]int{i})
		boxes_to_circuits[i] = i
	}

	index_pairs := [][2]int{}
	for i := 0; i < len(boxes)-1; i++ {
		for j := i + 1; j < len(boxes); j++ {
			index_pairs = append(index_pairs, [2]int{i, j})
		}
	}
	sort.Slice(
		index_pairs,
		func(i int, j int) bool {
			return _box_distance(boxes, index_pairs[i]) < _box_distance(boxes, index_pairs[j])
		},
	)

	for _, indexes := range index_pairs {
		box_i := indexes[0]
		box_j := indexes[1]
		circuit_i := boxes_to_circuits[box_i]
		circuit_j := boxes_to_circuits[box_j]
		if circuit_i == circuit_j {
			continue
		}
		for box_k := range circuits[circuit_i].Iter() {
			circuits[circuit_j].Add(box_k)
			boxes_to_circuits[box_k] = circuit_j
		}
		delete(circuits, circuit_i)

		if len(circuits) == 1 {
			return indexes
		}
	}

	return [2]int{-1, -1}
}

func _box_distance(boxes []vector.Vector3, index_pair [2]int) float64 {
	return boxes[index_pair[0]].Minus(boxes[index_pair[1]]).Magnitude()
}
