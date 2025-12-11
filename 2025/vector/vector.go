package vector

import (
	"math"
)

// TODO: how can we genericize the number of dimensions?
type Vector3 [3]float64

func (self Vector3) Magnitude() float64 {
	sum := 0.0
	for _, val := range self {
		sum += math.Pow(val, 2)
	}
	return math.Pow(sum, 0.5)
}

func (self Vector3) Minus(other Vector3) Vector3 {
	result := Vector3{}
	for i := range self {
		result[i] = self[i] - other[i]
	}
	return result
}

func (self Vector3) Abs() Vector3 {
	result := Vector3{}
	for i := range self {
		result[i] = math.Abs(self[i])
	}
	return result
}

type Number interface {
	~int | ~float64
}

// We'll just assume our vectors are always the same size for now 🤷‍♀️
type Vector []float64

func (self Vector) Magnitude() float64 {
	sum := 0.0
	for _, val := range self {
		sum += math.Pow(val, 2)
	}
	return math.Pow(sum, 0.5)
}

func (self Vector) Minus(other Vector) Vector {
	result := make(Vector, len(self))
	for i := range self {
		result[i] = self[i] - other[i]
	}
	return result
}

func (self Vector) Abs() Vector {
	result := make(Vector, len(self))
	for i := range self {
		result[i] = math.Abs(self[i])
	}
	return result
}
