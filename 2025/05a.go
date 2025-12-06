package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	fresh_id_ranges, available_ids := _load_inventory()

	num_fresh := _count_fresh_available(fresh_id_ranges, available_ids)

	fmt.Printf("%d\n", num_fresh)
}

type Id int

type IdRange struct {
	first Id
	last  Id
}

func (self IdRange) contains(id Id) bool {
	return self.first <= id && id <= self.last
}

func _load_inventory() ([]IdRange, []Id) {
	file, _ := os.Open("05.in")
	scanner := bufio.NewScanner(file)

	var fresh_id_ranges []IdRange
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}
		parts := strings.Split(line, "-")
		first, _ := strconv.Atoi(parts[0])
		last, _ := strconv.Atoi(parts[1])
		fresh_id_ranges = append(fresh_id_ranges, IdRange{first: Id(first), last: Id(last)})
	}

	var available_ids []Id
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}
		id, _ := strconv.Atoi(line)
		available_ids = append(available_ids, Id(id))
	}

	return fresh_id_ranges, available_ids
}

func _count_fresh_available(fresh_id_ranges []IdRange, available_ids []Id) int {
	num_fresh := 0
	for _, id := range available_ids {
		for _, id_range := range fresh_id_ranges {
			if id_range.contains(id) {
				num_fresh += 1
				break
			}
		}
	}
	return num_fresh
}
