package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	file, _ := os.Open("03.in")
	scanner := bufio.NewScanner(file)

	sum_power := 0
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		batteries := _parse_batteries(line)
		sum_power += _max_power(batteries)
	}
	fmt.Printf("%d\n", sum_power)
}

func _parse_batteries(line string) []int {
	var batteries []int
	for _, value_str := range strings.Split(line, "") {
		value, _ := strconv.Atoi(value_str)
		batteries = append(batteries, value)
	}
	return batteries
}

func _max_power(batteries []int) int {
	max_tens := -1
	max_tens_index := -1
	for index, value := range batteries[:len(batteries)-1] {
		if value > max_tens {
			max_tens = value
			max_tens_index = index
		}
	}

	max_ones := -1
	for _, value := range batteries[max_tens_index+1:] {
		if value > max_ones {
			max_ones = value
		}
	}

	return (max_tens * 10) + max_ones
}
