package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	problems := _load_problems()

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

func _load_problems() []Problem {
	file, _ := os.Open("06.in")
	scanner := bufio.NewScanner(file)

	var table_lines []string
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			break
		}

		table_lines = append(table_lines, line)
	}

	values_lines := table_lines[:len(table_lines)-1]
	ops_line := table_lines[len(table_lines)-1]

	// Mumbers may appear to be justified left or right, but operators are always left.
	// Add an extra ";" as a termination op.
	var problem_op_char_indexes []int
	for j, char := range ops_line + ";" {
		if char != ' ' {
			problem_op_char_indexes = append(problem_op_char_indexes, j)
		}
	}

	problems := make([]Problem, len(problem_op_char_indexes)-1)
	for index, prob := range problems {
		j := problem_op_char_indexes[index]
		next_j := problem_op_char_indexes[index+1]
		num_values := next_j - j

		for offset := range num_values {
			val_str := ""
			for _, line := range values_lines {
				val_str += string(line[j+offset])
			}
			val_str = strings.TrimSpace(val_str)
			if val_str != "" {
				value, _ := strconv.Atoi(val_str)
				prob.values = append(prob.values, value)
			}
		}

		op := ops_line[j]
		if op == '+' {
			prob.operation = sum
		} else if op == '*' {
			prob.operation = product
		} else {
			fmt.Println("[ERROR] operation:", op)
		}

		problems[index] = prob
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
