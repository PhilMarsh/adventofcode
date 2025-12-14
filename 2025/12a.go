package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	shapes, regions := _load_shapes_and_regions()
	// fmt.Println(shapes)
	// fmt.Println(regions)

	region_fits := _count_region_fits(regions, shapes)
	fmt.Println("CANNOT_FIT", region_fits[CANNOT_FIT])
	fmt.Println("NO_PACKING_NEEDED", region_fits[NO_PACKING_NEEDED])
	fmt.Println("REQUIRES_PACKING", region_fits[REQUIRES_PACKING])
}

type Shape [][]bool

type Region struct {
	width  int
	height int
	counts []int
}

type RegionFit int

const (
	CANNOT_FIT RegionFit = iota
	NO_PACKING_NEEDED
	REQUIRES_PACKING
)

func _load_shapes_and_regions() ([]Shape, []Region) {
	file, _ := os.Open("12.in")
	scanner := bufio.NewScanner(file)

	var shapes []Shape
	var regions []Region

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		} else if line[len(line)-1] == ':' {
			new_shape := Shape{}
			for scanner.Scan() {
				row_str := strings.TrimSpace(scanner.Text())
				if row_str == "" {
					break
				} else {
					new_row := make([]bool, len(row_str))
					for i, cell := range row_str {
						new_row[i] = (cell == '#')
					}
					new_shape = append(new_shape, new_row)
				}
			}
			shapes = append(shapes, new_shape)
		} else {
			parts := strings.Split(line, " ")

			size_parts := strings.Split(parts[0], "x")
			width, _ := strconv.Atoi(size_parts[0])
			height, _ := strconv.Atoi(strings.Trim(size_parts[1], ":"))

			counts := make([]int, len(parts)-1)
			for i, count_str := range parts[1:] {
				count, _ := strconv.Atoi(count_str)
				counts[i] = count
			}
			new_region := Region{
				width,
				height,
				counts,
			}
			regions = append(regions, new_region)
		}
	}

	return shapes, regions
}

func _count_region_fits(regions []Region, shapes []Shape) map[RegionFit]int {
	region_fits := map[RegionFit]int{
		CANNOT_FIT:        0,
		NO_PACKING_NEEDED: 0,
		REQUIRES_PACKING:  0,
	}

	for i, reg := range regions {
		fit := _region_fit(reg, shapes)
		region_fits[fit] += 1

		if fit == REQUIRES_PACKING {
			fmt.Println(fit, i, reg)
			fmt.Println(" --- TODO: IMPLEMENT PACKING ALGO ---")
		}
	}

	return region_fits
}

func _region_fit(region Region, shapes []Shape) RegionFit {
	min_required_size := 0
	max_required_size := 0
	for i, shp := range shapes {
		count := region.counts[i]
		min_required_size += _min_shape_size(shp) * count
		max_required_size += _max_shape_size(shp) * count
	}
	region_size := region.width * region.height

	if region_size < min_required_size {
		return CANNOT_FIT
	} else if region_size >= max_required_size {
		return NO_PACKING_NEEDED
	} else {
		return REQUIRES_PACKING
	}
}

func _min_shape_size(shape Shape) int {
	count := 0
	for _, row := range shape {
		for _, cell := range row {
			if cell {
				count += 1
			}
		}
	}
	return count
}
func _max_shape_size(shape Shape) int {
	height := len(shape)
	width := 0
	for _, row := range shape {
		if len(row) > width {
			width = len(row)
		}
	}
	return height * width
}
