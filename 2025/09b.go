package main

import (
	"aoc2025/vector"
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func main() {
	tiles := _load_tiles()

	max_rect, area := tiles.maximal_rectangle()

	fmt.Println(max_rect)
	fmt.Println(area)
}

type Vertex vector.Vector
type RectilinearPolygon []Vertex
type RectilinearEdge [2]Vertex

type PointPlacement int

const (
	PERIMETER PointPlacement = iota
	INTERIOR
	EXTERIOR
)

func _load_tiles() RectilinearPolygon {
	file, _ := os.Open("09.in")
	scanner := bufio.NewScanner(file)

	var tiles RectilinearPolygon
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}

		parts := strings.Split(line, ",")
		tile := make(Vertex, 2)
		for i := range tile {
			value, _ := strconv.Atoi(parts[i])
			tile[i] = float64(value)
		}
		tiles = append(tiles, tile)
	}

	return tiles
}

func make_rectangle(left_top Vertex, right_bottom Vertex) RectilinearPolygon {
	left_bottom := Vertex{left_top[0], right_bottom[1]}
	right_top := Vertex{right_bottom[0], left_top[1]}
	return RectilinearPolygon{left_top, right_top, right_bottom, left_bottom}
}

func (self RectilinearPolygon) maximal_rectangle() (RectilinearPolygon, int) {
	max_area := 0
	var max_rect RectilinearPolygon
	for i := 0; i < len(self)-1; i++ {
		for j := i + 1; j < len(self); j++ {
			v1 := self[i]
			v2 := self[j]
			new_rect := make_rectangle(v1, v2)
			// In general, `contains_polygon()` takes O(self*other) time.
			// But in this case, other is new_rect which is a const O(4), so it's
			// just O(4*self) = O(self), making this whole algo O(self^3).
			if self.contains_polygon(new_rect) {
				new_area := _area(v1, v2)
				if new_area > max_area {
					max_area = new_area
					max_rect = new_rect
				}
			}
		}
	}
	return max_rect, max_area
}

func (self RectilinearPolygon) edges() func(yield func(RectilinearEdge) bool) {
	return func(yield func(RectilinearEdge) bool) {
		for i, v1 := range self {
			v2 := self[(i+1)%len(self)]
			edge := RectilinearEdge{v1, v2}
			still_going := yield(edge)
			if !still_going {
				return
			}
		}
	}
}

func (self RectilinearPolygon) contains_polygon(other RectilinearPolygon) bool {
	/*
		In general, a polygon A contains another polygon B when the boundary of B is
		entirely within the boundary of A. This requires:
			1. The boundaries of A and B do not cross (they may overlap).
			2. Some point on the boundary of B is not outside of A (may be on perimeter).
		For rectilinear polygons, we can restate this as:
			1. No vertexes of B are in the exterior of A.
			2. No vertexes of A are in the interior of B.
			3. No edges of A cross any edges of B.
	*/
	for self_edge := range self.edges() {
		if other.has_interior_point(self_edge[0]) {
			return false
		}
	}
	for other_edge := range other.edges() {
		if self.has_exterior_point(other_edge[0]) {
			return false
		}
	}
	for self_edge := range self.edges() {
		for other_edge := range other.edges() {
			if self_edge.crosses(other_edge) {
				return false
			}
		}
	}
	return true
}

func (self RectilinearPolygon) has_perimeter_point(point Vertex) bool {
	return self.point_placement(point) == PERIMETER
}

func (self RectilinearPolygon) has_interior_point(point Vertex) bool {
	return self.point_placement(point) == INTERIOR
}

func (self RectilinearPolygon) has_exterior_point(point Vertex) bool {
	return self.point_placement(point) == EXTERIOR
}

func (self RectilinearPolygon) point_placement(point Vertex) PointPlacement {
	// To determine interior/exterior, ray trace left to count the number of
	// perimeter crossings. Odd crossings means inside; even means outside.
	py := point[1]
	px := point[0]
	ray := RectilinearEdge{Vertex{-1, py}, Vertex{px, py}}
	num_crossings := 0
	for edge := range self.edges() {
		if edge.contains_point(point) {
			return PERIMETER
		} else if edge.overlaps(ray) || edge.crosses(ray) {
			num_crossings += 1
		}
	}
	if num_crossings%2 == 0 {
		return EXTERIOR
	} else {
		return INTERIOR
	}
}

func (self RectilinearEdge) is_vertical() bool {
	return self[0][0] == self[1][0]
}

func (self RectilinearEdge) contains_point(point Vertex) bool {
	px := point[0]
	py := point[1]
	if self.is_vertical() {
		self_x := self[0][0]
		self_y1 := math.Min(self[0][1], self[1][1])
		self_y2 := math.Max(self[0][1], self[1][1])
		if px == self_x {
			if self_y1 <= py && py <= self_y2 {
				return true
			}
		}
	} else {
		self_y := self[0][1]
		self_x1 := math.Min(self[0][0], self[1][0])
		self_x2 := math.Max(self[0][0], self[1][0])
		if py == self_y {
			if self_x1 <= px && px <= self_x2 {
				return true
			}
		}
	}
	return false
}

func (self RectilinearEdge) transpose() RectilinearEdge {
	return RectilinearEdge{
		Vertex{self[0][1], self[0][0]},
		Vertex{self[1][1], self[1][0]},
	}
}

func (self RectilinearEdge) overlaps(other RectilinearEdge) bool {
	/*
		Check for colinear parallel lines with some overlap.
	*/
	if self.is_vertical() {
		if other.is_vertical() {
			self_x := self[0][0]
			self_y1 := math.Min(self[0][1], self[1][1])
			self_y2 := math.Max(self[0][1], self[1][1])
			other_x := self[0][0]
			other_y1 := math.Min(other[0][1], other[1][1])
			other_y2 := math.Max(other[0][1], other[1][1])
			return self_x == other_x && (other_y1 < self_y2 && self_y1 < other_y2)
		} else {
			return false
		}
	} else {
		if other.is_vertical() {
			return false
		} else {
			return self.transpose().overlaps(other.transpose())
		}
	}
}

func (self RectilinearEdge) crosses(other RectilinearEdge) bool {
	/*
		Check for full crossing, ie: both extending to the space on both sides of each
		other, not simply overlapping.
	*/
	if self.is_vertical() {
		if other.is_vertical() {
			return false
		} else {
			self_x := self[0][0]
			self_y1 := math.Min(self[0][1], self[1][1])
			self_y2 := math.Max(self[0][1], self[1][1])
			other_y := other[0][1]
			other_x1 := math.Min(other[0][0], other[1][0])
			other_x2 := math.Max(other[0][0], other[1][0])
			return (other_x1 < self_x && self_x < other_x2) && (self_y1 < other_y && other_y < self_y2)
		}
	} else {
		if other.is_vertical() {
			return other.crosses(self)
		} else {
			return false
		}
	}
}

func _area(v1 Vertex, v2 Vertex) int {
	rect := vector.Vector(v1).Minus(vector.Vector(v2)).Abs()
	return int(rect[0]+1) * int(rect[1]+1)
}
