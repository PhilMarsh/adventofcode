package main

import (
	"aoc2025/vector"
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	tiles := _load_tiles()

	area := _largest_area(tiles)

	fmt.Println(area)
}

type Tile = vector.Vector

func _load_tiles() []Tile {
	file, _ := os.Open("09.in")
	scanner := bufio.NewScanner(file)

	var tiles []Tile
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		parts := strings.Split(line, ",")
		tile := make(Tile, 2)
		for i := range tile {
			value, _ := strconv.Atoi(parts[i])
			tile[i] = float64(value)
		}
		tiles = append(tiles, tile)
	}

	return tiles
}

func _largest_area(tiles []Tile) int {
	area := 0
	for i := 0; i < len(tiles)-1; i++ {
		for j := i + 1; j < len(tiles); j++ {
			new_area := _area(tiles[i], tiles[j])
			if new_area > area {
				area = new_area
			}
		}
	}
	return area
}

func _area(t1 Tile, t2 Tile) int {
	rect := t1.Minus(t2).Abs()
	return int(rect[0]+1) * int(rect[1]+1)
}
