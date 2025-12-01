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
	file, _ := os.Open("01.in")
	scanner := bufio.NewScanner(file)

	position := DIAL_START
	zeros := 0
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		rotation := _parse_rotation(line)
		for range rotation.distance {
			position = (position + rotation.direction) % DIAL_SIZE
			if position == 0 {
				zeros += 1
			}
		}
	}
	fmt.Printf("%d\n", zeros)
}

type Rotation struct {
	direction int
	distance  int
}

func _parse_rotation(line string) Rotation {
	distance_str, is_left := strings.CutPrefix(line, "L")
	var direction int
	if is_left {
		direction = -1
	} else {
		distance_str, _ = strings.CutPrefix(line, "R")
		direction = 1
	}

	distance, _ := strconv.Atoi(distance_str)
	return Rotation{
		direction: direction,
		distance:  distance,
	}

}
