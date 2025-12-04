package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const OCCUPIED = '@'
const MAX_OCCUPIED_NEIGHBORS = 3

func main() {
	diagram := _load_diagram()

	num_accessible := _count_accessible(diagram)

	fmt.Printf("%d\n", num_accessible)
}

func _load_diagram() [][]int {
	file, _ := os.Open("04.in")
	scanner := bufio.NewScanner(file)

	var diagram [][]int
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		row := make([]int, len(line))
		for i, cell := range line {
			if cell == OCCUPIED {
				row[i] = 1
			}
		}
		diagram = append(diagram, row)
	}
	return diagram
}

func _count_accessible(diagram [][]int) int {
	count := 0
	for i, row := range diagram {
		for j := range row {
			if diagram[i][j] == 1 && _count_occupied_neighbors(diagram, i, j) <= MAX_OCCUPIED_NEIGHBORS {
				count += 1
			}
		}
	}
	return count
}

func _count_occupied_neighbors(diagram [][]int, row_index int, col_index int) int {
	height := len(diagram)
	width := len(diagram[0])

	count := 0
	for _, i := range []int{-1, 0, 1} {
		row_i := row_index + i
		if row_i < 0 || row_i >= height {
			continue
		}
		for _, j := range []int{-1, 0, 1} {
			if i == 0 && j == 0 {
				continue
			}
			col_i := col_index + j
			if col_i < 0 || col_i >= width {
				continue
			}
			count += diagram[row_i][col_i]
		}
	}
	return count
}
