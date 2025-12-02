package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const DIAL_START = 50
const DIAL_SIZE = 100

func main() {
	file, _ := os.Open("02.in")
	scanner := bufio.NewScanner(file)

	sum_invalid := 0
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		ranges := _parse_ranges_csv(line)
		for _, r := range ranges {
			for i := r.first; i <= r.last; i++ {
				if !_is_valid_product_id(i) {
					sum_invalid += i
				}
			}
		}
	}
	fmt.Printf("%d\n", sum_invalid)
}

type Range struct {
	first int
	last  int
}

func _parse_ranges_csv(line string) []Range {
	range_strs := strings.Split(line, ",")
	var ranges []Range
	for _, str := range range_strs {
		ranges = append(ranges, _parse_range(str))
	}
	return ranges
}
func _parse_range(range_str string) Range {
	parts := strings.Split(range_str, "-")
	first, _ := strconv.Atoi(parts[0])
	last, _ := strconv.Atoi(parts[1])
	return Range{first: first, last: last}
}

func _is_valid_product_id(id int) bool {
	id_str := strconv.Itoa(id)
	if len(id_str)%2 == 1 {
		return true
	}
	half_str := id_str[:len(id_str)/2]
	if id_str != half_str+half_str {
		return true
	}
	return false
}
