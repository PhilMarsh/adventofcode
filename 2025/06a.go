package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	worksheet_table := _load_raw_worksheet_table()

	problems := _parse_problems(worksheet_table)

	sum := _sum_results(problems)

	fmt.Printf("%d\n", sum)
}

type Problem struct {
	values    []int
	operation func([]int) int
}

func (self Problem) result() int {
	return self.operation(self.values)
}

func sum(values []int) int {
	/*
		The go stdlib really doesn't have a sum() function.
	*/

	result := 0
	for _, val := range values {
		result += val
	}
	return result
}

func product(values []int) int {
	/*
		The go stdlib really doesn't have a product() function.
	*/

	if len(values) == 0 {
		return 0
	}

	result := 1
	for _, val := range values {
		result *= val
	}
	return result
}

func _load_raw_worksheet_table() [][]string {
	file, _ := os.Open("06.in")
	scanner := bufio.NewScanner(file)

	var worksheet_table [][]string
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		var row []string
		for _, cell := range strings.Split(line, " ") {
			// Skip justification whitespace.
			if len(cell) != 0 {
				row = append(row, cell)
			}
		}
		worksheet_table = append(worksheet_table, row)
	}

	return worksheet_table
}

func _parse_problems(worksheet_table [][]string) []Problem {
	problems := make([]Problem, len(worksheet_table[0]))

	for _, row := range worksheet_table[:len(worksheet_table)-1] {
		for j, cell := range row {
			value, _ := strconv.Atoi(cell)
			problems[j].values = append(problems[j].values, value)
		}
	}

	for j, cell := range worksheet_table[len(worksheet_table)-1] {
		if cell == "+" {
			problems[j].operation = sum
		} else if cell == "*" {
			problems[j].operation = product
		} else {
			fmt.Println("[ERROR] operation:", cell)
		}
	}

	return problems
}

func _sum_results(problems []Problem) int {
	result := 0
	for _, prob := range problems {
		result += prob.result()
	}
	return result
}
