package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	fresh_id_ranges := _load_inventory()

	num_fresh := _count_fresh_possible(fresh_id_ranges)

	fmt.Printf("%d\n", num_fresh)
}

type Id int

type IdRange struct {
	first Id
	last  Id
}

func (self IdRange) size() int {
	return int(self.last - self.first + 1)
}

func (self IdRange) contains(id Id) bool {
	return self.first <= id && id <= self.last
}

func _load_inventory() []IdRange {
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

	return fresh_id_ranges
}

func _count_fresh_possible(fresh_id_ranges []IdRange) int {
	merged_ranges := _merge_ranges(fresh_id_ranges)
	return _sum_range_sizes(merged_ranges)
}

func _merge_ranges(id_ranges []IdRange) []IdRange {
	var sorted_merged []IdRange

	for _, new_range := range id_ranges {
		var new_merged []IdRange
		start_offset := -1
		for i, existing_range := range sorted_merged {
			if existing_range.last < new_range.first {
				// before new_range.
				new_merged = append(new_merged, existing_range)
			} else {
				start_offset = i
				break
			}
		}

		if start_offset == -1 {
			new_merged = append(new_merged, new_range)
		} else {
			new_first := min(sorted_merged[start_offset].first, new_range.first)
			new_last := new_range.last
			end_offset := -1
			for i, existing_range := range sorted_merged[start_offset:] {
				if existing_range.first <= new_range.last {
					// extend merged range.
					new_last = max(new_last, existing_range.last)
				} else {
					end_offset = start_offset + i
					break
				}
			}

			new_merged = append(new_merged, IdRange{first: new_first, last: new_last})

			if end_offset != -1 {
				// rest after merged range.
				new_merged = append(new_merged, sorted_merged[end_offset:]...)
			}
		}
		sorted_merged = new_merged
	}
	return sorted_merged
}

func _sum_range_sizes(id_ranges []IdRange) int {
	total := 0
	for _, rng := range id_ranges {
		total += rng.size()
	}
	return total
}
