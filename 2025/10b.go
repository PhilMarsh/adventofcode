package main

import (
	"aoc2025/set"
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	specs := _load_machine_specs()
	fmt.Println(specs)

	min := _min_presses_for_all_machines(specs, 20)

	fmt.Println(min)
}

type MachineSpec struct {
	// target_lights  int
	buttons_lights  []set.Set[int]
	target_joltages []int
}

func _load_machine_specs() []MachineSpec {
	file, _ := os.Open("10.in")
	scanner := bufio.NewScanner(file)

	var specs []MachineSpec
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		parts := strings.Split(line, " ")
		new_spec := MachineSpec{
			// _parse_target_lights(parts[0]),
			_parse_buttons_lights(parts[1 : len(parts)-1]),
			_parse_target_joltages(parts[len(parts)-1]),
		}
		specs = append(specs, new_spec)
	}

	return specs
}

// func _parse_target_lights(str string) int {
// 	/*
// 		build bitmask with left-most char (i=0) as lowest order bit (exp=2^0).
// 	*/
// 	lights := 0
// 	for i, char := range strings.Trim(str, "[]") {
// 		if char == '#' {
// 			lights += 1 << i
// 		}
// 	}
// 	return lights
// }

func _parse_buttons_lights(str []string) []set.Set[int] {
	buttons_lights := []set.Set[int]{}
	for _, spec := range str {
		light_indexes := strings.Split(strings.Trim(spec, "()"), ",")
		lights := set.Set[int]{}
		for _, index_str := range light_indexes {
			index, _ := strconv.Atoi(index_str)
			lights.Add(index)
		}
		buttons_lights = append(buttons_lights, lights)
	}
	return buttons_lights
}

func _parse_target_joltages(str string) []int {
	joltage_value_strs := strings.Split(strings.Trim(str, "{}"), ",")
	joltages := []int{}
	for _, value_str := range joltage_value_strs {
		value, _ := strconv.Atoi(value_str)
		joltages = append(joltages, value)
	}
	return joltages
}

func _min_presses_for_all_machines(specs []MachineSpec, max_presses int) int {
	sum := 0
	for i, spc := range specs {
		min := _min_presses_for_machine(spc, max_presses)
		fmt.Println(i, spc, min)
		if min == -1 {
			return -i
		}
		sum += min
	}
	return sum
}

func _min_presses_for_machine(spec MachineSpec, max_presses int) int {
	/*
		do linear algebra. solve for presses[0..n] in this system of linear equations:
			joltage[i] = button[0][i]*presses[0] + button[1][i]*presses[1] + ... + button[n][i]*presses[n]
		or more succinctly, as a matrix/vector equation: j=Bp, solve for p.
	*/
	// TODO: i don't really want to bother with this. there are numerous
	// libraries that do this exact thing with various degrees of success.
	// neither reimplementing tons of math code nor pulling down a bunch of
	// math libraries sounds like fun.
	return -1
}
