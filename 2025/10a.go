package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
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
	target_lights  int
	buttons_lights []int
	// TODO(10b): joltages
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
			_parse_target_lights(parts[0]),
			_parse_buttons_lights(parts[1 : len(parts)-1]),
			// TODO(10b): _parse_joltages(parts[len(parts)-1]),
		}
		specs = append(specs, new_spec)
	}

	return specs
}

func _parse_target_lights(str string) int {
	/*
		build bitmask with left-most char (i=0) as lowest order bit (exp=2^0).
	*/
	lights := 0
	for i, char := range strings.Trim(str, "[]") {
		if char == '#' {
			lights += 1 << i
		}
	}
	return lights
}

func _parse_buttons_lights(str []string) []int {
	buttons_lights := []int{}
	for _, spec := range str {
		light_indexes := strings.Split(strings.Trim(spec, "()"), ",")
		lights := 0
		for _, index_str := range light_indexes {
			index, _ := strconv.Atoi(index_str)
			lights += 1 << index
		}
		buttons_lights = append(buttons_lights, lights)
	}
	return buttons_lights
}

// func _parse_joltages(str string) ??? {
// 	TODO: 10b
// }

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
		basic BFS of combos with removal (because pressing a button twice is
		the same as not pressing it at all.)
	*/

	// Include index in set elements for uniqueness, in case multiple buttons
	// have the same bit mask.
	if len(spec.buttons_lights) < max_presses {
		max_presses = len(spec.buttons_lights)
	}
	for combo_size := 0; combo_size <= max_presses; combo_size++ {
		for combo := range _yield_combos(spec.buttons_lights, combo_size) {
			lights := 0
			for _, button_lights := range combo {
				lights ^= button_lights
			}
			if lights == spec.target_lights {
				return combo_size
			}
		}
	}
	return -1
}

func _yield_combos[T any](values []T, combo_size int) func(func([]T) bool) {
	return func(yield func([]T) bool) {
		if combo_size <= 0 {
			yield([]T{})
			return
		} else {
			for i, val := range values {
				combo_head := []T{val}
				combo_tails := _yield_combos(_removed(values, i), combo_size-1)
				for tail := range combo_tails {
					combo := append(combo_head, tail...)
					still_going := yield(combo)
					if !still_going {
						return
					}
				}
			}
		}
	}
}

func _removed[T any](values []T, index int) []T {
	before := slices.Clone(values[:index])
	after := values[index+1:]
	return append(before, after...)
}
