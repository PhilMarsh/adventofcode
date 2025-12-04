package main

import (
	"bufio"
	"fmt"
	"math"
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
		sum_power += _max_power(batteries, 12)
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

func _max_power(batteries []int, num_activated int) int {
	total_power := 0
	next_start_index := 0
	for exponent := num_activated - 1; exponent >= 0; exponent-- {
		max_digit := -1
		max_offset := -1
		for offset, value := range batteries[next_start_index : len(batteries)-exponent] {
			if value > max_digit {
				max_digit = value
				max_offset = offset
			}
		}
		total_power += int(math.Pow(10, float64(exponent))) * max_digit
		next_start_index += max_offset + 1
	}
	return total_power
}
